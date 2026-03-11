"""
E2E tests for the RandomRestOperation component.

Uses the IOP REST API (POST /api/iop/test) to invoke the ``RANDOM_REST_HTTP``
component in the running IRIS EAI production and verify the FhirResponse
returned by the operation.

The component makes a GET request to a public mock endpoint and wraps the
result in a FhirResponse message.  All tests share one HTTP round-trip via
the ``random_rest_iop_response`` module-scoped fixture.
"""

import json

import pytest
import requests

_AUTH = ("SuperUser", "SYS")
_IOP_TEST_PATH = "/api/iop/test"
_TARGET = "RANDOM_REST_HTTP"
_NAMESPACE = "EAI"
_MESSAGE_CLASSNAME = "msg.FhirRequest"

# Minimal FhirRequest payload — RandomRestOperation ignores the message body
# and always fetches its own configured URL.
_FHIR_REQUEST_BODY = json.dumps(
    {
        "url": "",
        "resource": "random",
        "method": "GET",
        "data": "",
        "headers": {},
    }
)


# ---------------------------------------------------------------------------
# Module-scoped fixture — one IOP call for the whole module
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def random_rest_iop_response(iop_base_url: str) -> dict:
    """
    Invoke the RANDOM_REST_HTTP operation via POST /api/iop/test and return
    the parsed JSON response body.

    Fails fast with a clear message if the IOP call itself returns a non-200
    status, so individual tests can focus on the response content.
    """
    resp = requests.post(
        f"{iop_base_url}{_IOP_TEST_PATH}",
        auth=_AUTH,
        json={
            "target": _TARGET,
            "classname": _MESSAGE_CLASSNAME,
            "body": _FHIR_REQUEST_BODY,
            "namespace": _NAMESPACE,
        },
        timeout=30,
    )
    assert resp.status_code == 200, (
        f"IOP test endpoint returned HTTP {resp.status_code}:\n{resp.text}"
    )
    return resp.json()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.e2e
def test_iop_response_has_body(random_rest_iop_response: dict):
    """The IOP response must include a non-empty 'body' key."""
    assert "body" in random_rest_iop_response
    assert random_rest_iop_response["body"]


@pytest.mark.e2e
def test_iop_response_is_not_truncated(random_rest_iop_response: dict):
    """The response body must not be truncated by the IOP API."""
    assert random_rest_iop_response.get("truncated") is 0

@pytest.mark.e2e
def test_fhir_response_upstream_status_code_is_200(random_rest_iop_response: dict):
    """The mock endpoint must have answered with HTTP 200."""
    body = json.loads(random_rest_iop_response["body"])
    assert body["status_code"] == 200


@pytest.mark.e2e
def test_fhir_response_resource_is_random(random_rest_iop_response: dict):
    """The 'resource' field must be set to 'random' as returned by the operation."""
    body = json.loads(random_rest_iop_response["body"])
    assert body.get("resource") == "random"


@pytest.mark.e2e
def test_fhir_response_content_is_not_empty(random_rest_iop_response: dict):
    """The operation must return non-empty content from the upstream endpoint."""
    body = json.loads(random_rest_iop_response["body"])
    assert body.get("content")


@pytest.mark.e2e
def test_fhir_response_headers_present(random_rest_iop_response: dict):
    """The upstream response headers must be forwarded in the FhirResponse."""
    body = json.loads(random_rest_iop_response["body"])
    assert isinstance(body.get("headers"), dict)
    assert body["headers"]
