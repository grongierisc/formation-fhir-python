"""
E2E smoke tests — basic FHIR server sanity checks.

Verifies that the FHIR endpoint is reachable, returns valid FHIR responses,
and that elementary CRUD operations work before running deeper tests.
"""

import uuid

import pytest
import requests

_AUTH = ("SuperUser", "SYS")
_ACCEPT = {"Accept": "application/fhir+json"}
_CONTENT = {"Content-Type": "application/fhir+json", "Accept": "application/fhir+json"}


# ===========================================================================
# Metadata / CapabilityStatement
# ===========================================================================

@pytest.mark.e2e
def test_metadata_returns_capability_statement(fhir_base_url: str):
    """GET /metadata must return a CapabilityStatement."""
    response = requests.get(
        f"{fhir_base_url}/metadata",
        headers=_ACCEPT,
        auth=_AUTH,
        timeout=10,
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body.get("resourceType") == "CapabilityStatement", body


@pytest.mark.skip(reason="on_capability_statement hook not yet active on the running server")
@pytest.mark.e2e
def test_metadata_account_resource_removed(fhir_base_url: str):
    """
    The on_capability_statement hook in custom_decorators removes Account.
    Account must be absent from the CapabilityStatement.

    NOTE: This test will fail if the customization module is not loaded
    correctly on the server (e.g. when fhir_validator fails to initialize).
    """
    response = requests.get(
        f"{fhir_base_url}/metadata",
        headers=_ACCEPT,
        auth=_AUTH,
        timeout=10,
    )
    assert response.status_code == 200, response.text
    resources = response.json()["rest"][0]["resource"]
    types = {r["type"] for r in resources}
    assert "Account" not in types, (
        f"Account should not be in the CapabilityStatement — "
        f"check that the custom_decorators module loaded correctly on the server."
    )


@pytest.mark.e2e
def test_metadata_patient_resource_present(fhir_base_url: str):
    """Patient must remain in the CapabilityStatement after customization."""
    response = requests.get(
        f"{fhir_base_url}/metadata",
        headers=_ACCEPT,
        auth=_AUTH,
        timeout=10,
    )
    assert response.status_code == 200, response.text
    resources = response.json()["rest"][0]["resource"]
    types = {r["type"] for r in resources}
    assert "Patient" in types


# ===========================================================================
# Patient CRUD
# ===========================================================================

@pytest.mark.e2e
def test_create_and_read_patient(fhir_base_url: str):
    """Create a Patient with PUT then read it back."""
    patient_id = f"smoke-{uuid.uuid4().hex[:12]}"
    patient = {
        "resourceType": "Patient",
        "id": patient_id,
        "name": [{"family": "Smoke", "given": ["Test"]}],
    }

    put_resp = requests.put(
        f"{fhir_base_url}/Patient/{patient_id}",
        headers=_CONTENT,
        auth=_AUTH,
        json=patient,
        timeout=10,
    )
    assert put_resp.status_code in (200, 201), put_resp.text

    get_resp = requests.get(
        f"{fhir_base_url}/Patient/{patient_id}",
        headers=_ACCEPT,
        auth=_AUTH,
        timeout=10,
    )
    assert get_resp.status_code == 200, get_resp.text
    body = get_resp.json()
    assert body["resourceType"] == "Patient"
    assert body["id"] == patient_id


@pytest.mark.e2e
def test_update_patient(fhir_base_url: str):
    """Update an existing Patient resource and verify the change persists."""
    patient_id = f"smoke-update-{uuid.uuid4().hex[:10]}"
    patient = {
        "resourceType": "Patient",
        "id": patient_id,
        "name": [{"family": "Original"}],
    }
    requests.put(
        f"{fhir_base_url}/Patient/{patient_id}",
        headers=_CONTENT,
        auth=_AUTH,
        json=patient,
        timeout=10,
    )

    patient["name"] = [{"family": "Updated"}]
    update_resp = requests.put(
        f"{fhir_base_url}/Patient/{patient_id}",
        headers=_CONTENT,
        auth=_AUTH,
        json=patient,
        timeout=10,
    )
    assert update_resp.status_code in (200, 201), update_resp.text

    get_resp = requests.get(
        f"{fhir_base_url}/Patient/{patient_id}",
        headers=_ACCEPT,
        auth=_AUTH,
        timeout=10,
    )
    assert get_resp.status_code == 200, get_resp.text
    assert get_resp.json()["name"][0]["family"] == "Updated"


@pytest.mark.e2e
def test_delete_patient(fhir_base_url: str):
    """Delete a Patient and verify subsequent reads return 404 or 410 Gone."""
    patient_id = f"smoke-delete-{uuid.uuid4().hex[:10]}"
    patient = {"resourceType": "Patient", "id": patient_id}
    requests.put(
        f"{fhir_base_url}/Patient/{patient_id}",
        headers=_CONTENT,
        auth=_AUTH,
        json=patient,
        timeout=10,
    )

    del_resp = requests.delete(
        f"{fhir_base_url}/Patient/{patient_id}",
        auth=_AUTH,
        timeout=10,
    )
    assert del_resp.status_code in (200, 204), del_resp.text

    get_resp = requests.get(
        f"{fhir_base_url}/Patient/{patient_id}",
        headers=_ACCEPT,
        auth=_AUTH,
        timeout=10,
    )
    # 404 Not Found or 410 Gone both signal successful deletion
    assert get_resp.status_code in (404, 410), (
        f"Expected 404/410 after delete, got {get_resp.status_code}"
    )


@pytest.mark.e2e
def test_read_nonexistent_patient_returns_404(fhir_base_url: str):
    """Reading a resource that was never created must return 404."""
    response = requests.get(
        f"{fhir_base_url}/Patient/definitely-does-not-exist-{uuid.uuid4().hex}",
        headers=_ACCEPT,
        auth=_AUTH,
        timeout=10,
    )
    assert response.status_code == 404, response.text


@pytest.mark.e2e
def test_search_patients_returns_bundle(fhir_base_url: str):
    """GET /Patient must return a Bundle."""
    response = requests.get(
        f"{fhir_base_url}/Patient",
        headers=_ACCEPT,
        auth=_AUTH,
        params={"_count": "5"},
        timeout=10,
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["resourceType"] == "Bundle"


@pytest.mark.e2e
def test_nonexistent_operation_returns_error(fhir_base_url: str):
    """Calling an undefined FHIR operation must return a 4xx error."""
    response = requests.post(
        f"{fhir_base_url}/Patient/$doesnotexist",
        headers=_CONTENT,
        auth=_AUTH,
        json={"resourceType": "Parameters"},
        timeout=10,
    )
    assert response.status_code >= 400, (
        f"Expected 4xx for undefined operation, got {response.status_code}"
    )
    body = response.json()
    assert body.get("resourceType") == "OperationOutcome"
