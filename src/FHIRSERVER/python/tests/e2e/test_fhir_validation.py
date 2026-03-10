"""
E2E tests for on_validate_resource hooks in custom_decorators.

Tests cover:
1. generic_resource_validation ("*") — raises ValueError when 'id' is absent.
2. validate_observation_resource — critical codes (critical-001 / critical-002)
   require a 'note' field; non-critical codes do not.
3. validate_resource_schema — FhirValidator is invoked on resource writes
   (valid resources must pass through without server errors).

Run these tests against a running IRIS FHIR server::

    pytest src/FHIRSERVER/python/tests/e2e/ -m e2e -v
"""

import uuid

import pytest
import requests

_AUTH = ("SuperUser", "SYS")
_CONTENT = {
    "Content-Type": "application/fhir+json",
    "Accept": "application/fhir+json",
}


def _make_observation(obs_id: str, coding_code: str, include_note: bool = False) -> dict:
    """
    Build a minimal R4-compliant Observation.

    Uses a coding code that maps to either a custom critical code or a
    standard LOINC placeholder for non-critical tests.
    """
    obs = {
        "resourceType": "Observation",
        "id": obs_id,
        "status": "final",
        "code": {
            "coding": [
                {
                    "system": "http://example.org/custom-codes",
                    "code": coding_code,
                    "display": f"Test code {coding_code}",
                }
            ],
            "text": coding_code,
        },
    }
    if include_note:
        obs["note"] = [{"text": "Required note for critical observation"}]
    return obs


# ===========================================================================
# generic_resource_validation — resource must have 'id'
# ===========================================================================

@pytest.mark.e2e
def test_create_resource_without_id_is_rejected(fhir_base_url: str):
    """
    generic_resource_validation raises ValueError('Resource must have an id
    field') when 'id' is absent. POSTing a Patient without 'id' must return
    an error (4xx).
    """
    patient_no_id = {
        "resourceType": "Patient",
        "active": True,
        "name": [{"family": "NoId"}],
        # Intentionally no 'id' field
    }

    resp = requests.post(
        f"{fhir_base_url}/Patient",
        headers=_CONTENT,
        auth=_AUTH,
        json=patient_no_id,
        timeout=10,
    )

    assert resp.status_code >= 400, (
        f"Expected 4xx when 'id' is absent, got {resp.status_code}: {resp.text}"
    )


@pytest.mark.e2e
def test_create_resource_with_id_succeeds(fhir_base_url: str):
    """
    A Patient with an 'id' field must pass generic_resource_validation.
    """
    patient_id = f"e2e-with-id-{uuid.uuid4().hex[:8]}"
    patient = {
        "resourceType": "Patient",
        "id": patient_id,
        "name": [{"family": "HasId"}],
    }

    resp = requests.put(
        f"{fhir_base_url}/Patient/{patient_id}",
        headers=_CONTENT,
        auth=_AUTH,
        json=patient,
        timeout=10,
    )
    assert resp.status_code in (200, 201), (
        f"Patient with 'id' should be accepted, got {resp.status_code}: {resp.text}"
    )


# ===========================================================================
# validate_observation_resource — critical codes
# ===========================================================================

@pytest.mark.e2e
def test_critical_observation_without_note_is_rejected(fhir_base_url: str):
    """
    Observation with code critical-001 and without 'note' must be rejected
    by validate_observation_resource (ValueError → 4xx).
    """
    obs_id = f"e2e-crit-{uuid.uuid4().hex[:8]}"
    obs = _make_observation(obs_id, "critical-001", include_note=False)

    resp = requests.put(
        f"{fhir_base_url}/Observation/{obs_id}",
        headers=_CONTENT,
        auth=_AUTH,
        json=obs,
        timeout=10,
    )

    assert resp.status_code >= 400, (
        f"Expected 4xx for critical obs without note, got {resp.status_code}: {resp.text}"
    )


@pytest.mark.e2e
def test_critical_observation_002_without_note_is_rejected(fhir_base_url: str):
    """
    Observation with code critical-002 and without 'note' must also be
    rejected.
    """
    obs_id = f"e2e-crit2-{uuid.uuid4().hex[:8]}"
    obs = _make_observation(obs_id, "critical-002", include_note=False)

    resp = requests.put(
        f"{fhir_base_url}/Observation/{obs_id}",
        headers=_CONTENT,
        auth=_AUTH,
        json=obs,
        timeout=10,
    )

    assert resp.status_code >= 400, (
        f"Expected 4xx for critical-002 obs without note, got {resp.status_code}: {resp.text}"
    )


@pytest.mark.e2e
def test_critical_observation_with_note_is_accepted(fhir_base_url: str):
    """
    Observation with code critical-001 AND a 'note' field must pass
    validate_observation_resource.
    """
    obs_id = f"e2e-crit-note-{uuid.uuid4().hex[:8]}"
    obs = _make_observation(obs_id, "critical-001", include_note=True)

    resp = requests.put(
        f"{fhir_base_url}/Observation/{obs_id}",
        headers=_CONTENT,
        auth=_AUTH,
        json=obs,
        timeout=10,
    )

    assert resp.status_code in (200, 201), (
        f"Critical obs WITH note should be accepted, got {resp.status_code}: {resp.text}"
    )


@pytest.mark.e2e
def test_non_critical_observation_without_note_is_accepted(fhir_base_url: str):
    """
    Observations with non-critical codes do not require a 'note'.
    A routine observation without 'note' must be accepted (200/201).
    """
    obs_id = f"e2e-routine-{uuid.uuid4().hex[:8]}"
    obs = _make_observation(obs_id, "routine-check", include_note=False)

    resp = requests.put(
        f"{fhir_base_url}/Observation/{obs_id}",
        headers=_CONTENT,
        auth=_AUTH,
        json=obs,
        timeout=10,
    )

    assert resp.status_code in (200, 201), (
        f"Non-critical obs without note should be accepted, got {resp.status_code}: {resp.text}"
    )


@pytest.mark.e2e
def test_critical_observation_error_message_mentions_note(fhir_base_url: str):
    """
    The error response for a critical observation without a note must contain
    a meaningful error message referencing 'note'.
    """
    obs_id = f"e2e-crit-msg-{uuid.uuid4().hex[:8]}"
    obs = _make_observation(obs_id, "critical-001", include_note=False)

    resp = requests.put(
        f"{fhir_base_url}/Observation/{obs_id}",
        headers=_CONTENT,
        auth=_AUTH,
        json=obs,
        timeout=10,
    )

    assert resp.status_code >= 400, resp.text
    # The error should mention "note" per the ValueError message
    assert "note" in resp.text.lower() or "Critical" in resp.text, (
        f"Error message should reference 'note', got: {resp.text[:200]}"
    )


# ===========================================================================
# validate_resource_schema — FhirValidator is invoked
# ===========================================================================

@pytest.mark.e2e
def test_schema_validator_invoked_for_patient(fhir_base_url: str):
    """
    validate_resource_schema calls FhirValidator.validate on every Patient
    write. A well-formed Patient must be accepted (200/201).
    """
    patient_id = f"e2e-schema-{uuid.uuid4().hex[:8]}"
    patient = {
        "resourceType": "Patient",
        "id": patient_id,
        "name": [{"family": "SchemaTest", "given": ["Valid"]}],
        "birthDate": "1990-01-01",
    }

    resp = requests.put(
        f"{fhir_base_url}/Patient/{patient_id}",
        headers=_CONTENT,
        auth=_AUTH,
        json=patient,
        timeout=15,
    )

    assert resp.status_code in (200, 201), (
        f"Well-formed Patient should pass schema validation, got "
        f"{resp.status_code}: {resp.text}"
    )


@pytest.mark.e2e
def test_schema_validator_invoked_for_observation(fhir_base_url: str):
    """
    validate_resource_schema is a wildcard hook that fires for Observation
    as well. A minimal valid Observation must not trigger a server error.
    """
    obs_id = f"e2e-schema-obs-{uuid.uuid4().hex[:8]}"
    obs = {
        "resourceType": "Observation",
        "id": obs_id,
        "status": "final",
        "code": {"text": "Schema test observation"},
        "note": [{"text": "Included to satisfy any critical-code check"}],
    }

    resp = requests.put(
        f"{fhir_base_url}/Observation/{obs_id}",
        headers=_CONTENT,
        auth=_AUTH,
        json=obs,
        timeout=15,
    )

    # The FhirValidator may return warnings but should NOT hard-fail a minimal R4 Observation
    assert resp.status_code not in (500,), (
        f"Server error on valid Observation: {resp.status_code}: {resp.text}"
    )
