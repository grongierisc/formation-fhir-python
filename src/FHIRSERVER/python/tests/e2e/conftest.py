"""
E2E test configuration for FHIR server tests.

The fixture detects a running docker-compose stack or accepts an explicit URL
via the FHIR_BASE_URL environment variable.

Before yielding the URL, it reloads the FHIR Python customization inside the
IRIS container so that local source changes are picked up without a full
container restart.

Run with the stack already up (``docker compose up -d``) then::

    pytest src/FHIRSERVER/python/tests/e2e/ -m e2e -v

Or point at any running server::

    FHIR_BASE_URL=http://localhost:8081/fhir pytest src/FHIRSERVER/python/tests/e2e/ -m e2e -v
"""

import os
import time
from typing import Any, Generator, Optional

import pytest
import requests

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
_DEFAULT_WEBGATEWAY_PORT = 8081
_DEFAULT_FHIR_BASE_URL = f"http://localhost:{_DEFAULT_WEBGATEWAY_PORT}/fhir"
_WEBGATEWAY_CONTAINER_NAME = "iris-fhir-facade-and-repo-template-webgateway-1"
_IRIS_CONTAINER_NAME = "iris-fhir-facade-and-repo-template-iris-1"
_RESTART_SCRIPT_PATH = "/irisdev/app/iris.script.restart.fhir"
_STARTUP_TIMEOUT_SECONDS = 120
_POST_RESTART_PROBE_TIMEOUT = 60
_AUTH = ("SuperUser", "SYS")
_ACCEPT_JSON = {"Accept": "application/fhir+json"}
_CONTENT_JSON = {
    "Content-Type": "application/fhir+json",
    "Accept": "application/fhir+json",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _probe_fhir(base_url: str, timeout: int = _STARTUP_TIMEOUT_SECONDS) -> bool:
    """Poll /metadata until it returns 200 or the timeout expires."""
    metadata_url = f"{base_url}/metadata"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(metadata_url, headers=_ACCEPT_JSON, auth=_AUTH, timeout=5)
            if r.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            # Covers ConnectionError, ReadTimeout, SSLError, etc.
            pass
        time.sleep(2)
    return False


def _find_iris_container(client: Any) -> Optional[Any]:
    """Return the running IRIS container for this project, or None."""
    for container in client.containers.list():
        if _IRIS_CONTAINER_NAME in container.name:
            return container
    return None


def _find_webgateway_port(client: Any) -> Optional[str]:
    """
    Find the host port mapped to this project's webgateway container port 80.
    Falls back to the direct IRIS port 52773 if webgateway is absent.
    """
    for container in client.containers.list():
        if container.name == _WEBGATEWAY_CONTAINER_NAME:
            ports = container.ports.get("80/tcp")
            if ports:
                return ports[0]["HostPort"]
    # Fall back: look for IRIS container exposing 52773 directly
    iris = _find_iris_container(client)
    if iris is not None:
        ports52 = iris.ports.get("52773/tcp")
        if ports52:
            return ports52[0]["HostPort"]
    return None


def _run_restart_script(container: Any) -> None:
    """
    Exec the FHIR reload script inside the running IRIS container so that
    Python source changes are picked up without restarting the container.

    Equivalent to running in the container::

        iris session iris < /irisdev/app/iris.script.restart.fhir
    """
    result = container.exec_run(
        ["/bin/sh", "-c", f"iris session iris < {_RESTART_SCRIPT_PATH}"],
        stdout=True,
        stderr=True,
        user="irisowner",
    )
    if result.exit_code != 0:
        raise RuntimeError(
            f"FHIR reload script failed (exit {result.exit_code}):\n"
            + result.output.decode("utf-8", errors="replace")
        )


# ---------------------------------------------------------------------------
# Session fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def fhir_base_url() -> Generator[str, None, None]:
    """
    Resolve the FHIR server base URL for the session and reload the Python
    customization module inside IRIS so local changes are applied.

    Priority:
    1. ``FHIR_BASE_URL`` environment variable (already includes /fhir path).
    2. Docker SDK — scan running containers for the webgateway port.
    3. Hard-coded default ``http://localhost:8081/fhir``.

    The fixture skips the entire test session if the endpoint is unreachable.
    """
    # 1. Explicit override
    base_url = os.environ.get("FHIR_BASE_URL")

    iris_container = None
    if base_url is None:
        # 2. Docker SDK auto-detect
        try:
            import docker  # type: ignore[import]
            client = docker.from_env()
            port = _find_webgateway_port(client)
            if port is not None:
                base_url = f"http://localhost:{port}/fhir"
            iris_container = _find_iris_container(client)
        except Exception:
            pass  # docker not available or container not found

    # 3. Default
    if base_url is None:
        base_url = _DEFAULT_FHIR_BASE_URL

    # Reload Python customizations inside the running IRIS container so that
    # any local source changes to custom_decorators.py are applied before the
    # test session begins.
    if iris_container is not None:
        try:
            _run_restart_script(iris_container)
        except Exception as exc:
            pytest.skip(f"Could not reload FHIR customizations: {exc}")
        # After killing CSP jobs IRIS needs time to respawn workers.
        probe_timeout = _POST_RESTART_PROBE_TIMEOUT
    else:
        probe_timeout = 10

    # Probe — skip if unreachable
    if not _probe_fhir(base_url, timeout=probe_timeout):
        pytest.skip(
            f"FHIR server not reachable at {base_url}/metadata — "
            "start the docker-compose stack or set FHIR_BASE_URL."
        )

    yield base_url
