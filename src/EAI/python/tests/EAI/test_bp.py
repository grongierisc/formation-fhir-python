import json
from unittest.mock import MagicMock

import jwt
import pytest

from bp import FhirMainProcess
import fixtures


# ===========================================================================
# Fixtures
# ===========================================================================

@pytest.fixture
def bp():
    return FhirMainProcess()


def _make_token(scope: str) -> str:
    """Build an unsigned JWT with the given scope claim."""
    return jwt.encode({"scope": scope}, key="", algorithm="none")


# ===========================================================================
# FhirMainProcess — token helpers
# ===========================================================================

@pytest.mark.unit
def test_check_token_returns_false_when_no_vip():
    bp = FhirMainProcess()
    assert bp.check_token(fixtures.VALIDE_TOKEN) is False


@pytest.mark.unit
def test_check_token_returns_true_when_vip_in_scope():
    bp = FhirMainProcess()
    token = _make_token("read VIP write")
    assert bp.check_token(token) is True


@pytest.mark.unit
def test_check_token_returns_false_on_invalid_token():
    bp = FhirMainProcess()
    assert bp.check_token("not-a-jwt") is False


# ===========================================================================
# FhirMainProcess — filter_patient_resource
# ===========================================================================

@pytest.mark.unit
def test_filter_patient_resource_removes_pii(bp):
    patient = json.loads(fixtures.FHIR_PATIENT)
    result = bp.filter_patient_resource(patient)
    assert "name" not in result
    assert result["address"] is None
    assert result["telecom"] == []
    assert result["birthDate"] is None


@pytest.mark.unit
def test_filter_patient_resource_returns_dict(bp):
    patient = json.loads(fixtures.FHIR_PATIENT)
    result = bp.filter_patient_resource(patient)
    assert isinstance(result, dict)


# ===========================================================================
# FhirMainProcess — filter_resources
# ===========================================================================

@pytest.mark.unit
def test_filter_resources_patient_bundle(bp):
    bundle = json.loads(fixtures.FHIR_BUNDLE_PERMISSION)
    result = bp.filter_resources(bundle)
    for entry in result.get("entry", []):
        resource = entry["resource"]
        if resource.get("resourceType") == "Patient":
            assert "name" not in resource


@pytest.mark.unit
def test_filter_resources_single_patient(bp):
    patient = json.loads(fixtures.FHIR_PATIENT)
    result = bp.filter_resources(patient)
    assert "name" not in result


@pytest.mark.unit
def test_filter_resources_unsupported_type_returned_unchanged(bp):
    observation = {"resourceType": "Observation", "id": "obs-1", "status": "final"}
    result = bp.filter_resources(observation)
    assert result == observation


# ===========================================================================
# FhirMainProcess — on_fhir_request (mocked I/O)
# ===========================================================================

@pytest.mark.unit
def test_on_fhir_request(bp):
    request = MagicMock()
    request.Request.AdditionalInfo.GetAt.return_value = "token-id-123"
    expected_rsp = MagicMock()
    bp.get_token_string = MagicMock(return_value=fixtures.VALIDE_TOKEN)
    bp.send_request_sync = MagicMock(return_value=expected_rsp)
    rsp = bp.on_fhir_request(request)
    assert rsp is not None

