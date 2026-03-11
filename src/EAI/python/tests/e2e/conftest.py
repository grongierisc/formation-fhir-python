"""
E2E test configuration for EAI interoperability tests.

Resolves the IOP REST API base URL from the running docker-compose stack
or from an explicit ``IOP_BASE_URL`` environment variable.

Run with the stack already up (``docker compose up -d``) then::

    pytest src/EAI/python/tests/e2e/ -m e2e -v

Or point at any running server::

    IOP_BASE_URL=http://localhost:8081 pytest src/EAI/python/tests/e2e/ -m e2e -v
"""

import os
import time
from typing import Optional

import pytest
import requests

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
_DEFAULT_WEBGATEWAY_PORT = 8081
_DEFAULT_IOP_BASE_URL = f"http://localhost:{_DEFAULT_WEBGATEWAY_PORT}"
_WEBGATEWAY_CONTAINER_NAME = "formation-fhir-python-webgateway-1"
_STARTUP_TIMEOUT_SECONDS = 30
_AUTH = ("SuperUser", "SYS")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _probe_iop(base_url: str, timeout: int = _STARTUP_TIMEOUT_SECONDS) -> bool:
    """Poll GET /api/iop/version until it returns 200 or the timeout expires."""
    version_url = f"{base_url}/api/iop/version"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(version_url, auth=_AUTH, timeout=5)
            if r.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(2)
    return False


def _find_webgateway_port(client) -> Optional[str]:
    """Return the host port mapped to the webgateway container's port 80."""
    for container in client.containers.list():
        if _WEBGATEWAY_CONTAINER_NAME in container.name:
            ports = container.ports.get("80/tcp")
            if ports:
                return ports[0]["HostPort"]
    return None


# ---------------------------------------------------------------------------
# Session fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def iop_base_url() -> str:
    """
    Resolve the IOP REST API base URL for the session.

    Priority:
    1. ``IOP_BASE_URL`` environment variable.
    2. Docker SDK — scan running containers for the webgateway port.
    3. Hard-coded default ``http://localhost:8081``.

    The fixture skips the entire test session if the IOP endpoint is unreachable.
    """
    base_url = os.environ.get("IOP_BASE_URL")

    if base_url is None:
        try:
            import docker  # type: ignore[import]
            client = docker.from_env()
            port = _find_webgateway_port(client)
            if port is not None:
                base_url = f"http://localhost:{port}"
        except Exception:
            pass

    if base_url is None:
        base_url = _DEFAULT_IOP_BASE_URL

    if not _probe_iop(base_url):
        pytest.skip(
            f"IOP REST API not reachable at {base_url}/api/iop/version — "
            "start the docker-compose stack or set IOP_BASE_URL."
        )

    return base_url
