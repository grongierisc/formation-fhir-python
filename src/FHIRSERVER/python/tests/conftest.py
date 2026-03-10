"""
Shared fixtures for FHIRSERVER unit tests.
"""

import sys
import os
from types import SimpleNamespace
from typing import Callable, Generator

import pytest

# ---------------------------------------------------------------------------
# 1. Ensure the FHIRSERVER python directory is on sys.path
# ---------------------------------------------------------------------------
_PYTHON_DIR = os.path.join(os.path.dirname(__file__), "..")
if _PYTHON_DIR not in sys.path:
    sys.path.insert(0, _PYTHON_DIR)

# ---------------------------------------------------------------------------
# 2. Request-context isolation
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def isolated_request_context() -> Generator[None, None, None]:
    """Each test runs inside a clean, isolated RequestContext."""
    from iris_fhir_python_strategy import request_context
    with request_context():
        yield


# ---------------------------------------------------------------------------
# 3. Fake FHIR request factory
# ---------------------------------------------------------------------------
@pytest.fixture
def fake_fhir_request() -> Callable[..., SimpleNamespace]:
    """
    Factory that builds a minimal FHIR request object.

    Usage::

        def test_something(fake_fhir_request):
            req = fake_fhir_request(username="alice", roles="doctor")
    """
    def _make(username: str = "testuser", roles: str = "user") -> SimpleNamespace:
        req = SimpleNamespace()
        req.Username = username
        req.Roles = roles
        return req

    return _make
