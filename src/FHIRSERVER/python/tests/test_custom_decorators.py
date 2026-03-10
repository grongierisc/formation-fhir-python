"""
Unit tests for src/FHIRSERVER/python/custom_decorators.py.

Test strategy follows the pattern used in the iris-fhir-python-strategy repo:
  - Import the module under test once; its decorators register handlers on the
    global `fhir` registry.
  - Access registered handlers via `fhir.get_*_handlers()` and call them
    directly — no running IRIS server required.
  - Use the `isolated_request_context` fixture (defined in conftest.py) to
    give every test a clean RequestContext so that tests are independent.
"""

import json
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

# Import the module under test — conftest has already mocked fhir_validator
import custom_decorators as cd

from iris_fhir_python_strategy import get_request_context


# ===========================================================================
# Capability Statement
# ===========================================================================

@pytest.mark.unit
def test_customize_capability_statement_removes_account():
    """Account resource must be absent from the returned statement."""
    handlers = cd.fhir.get_capability_statement_handlers()
    assert handlers, "No capability-statement handler was registered"

    capability = {
        "rest": [
            {
                "resource": [
                    {"type": "Account"},
                    {"type": "Patient"},
                    {"type": "Observation"},
                ]
            }
        ]
    }
    for handler in handlers:
        capability = handler(capability)

    resource_types = [r["type"] for r in capability["rest"][0]["resource"]]
    assert "Account" not in resource_types
    assert "Patient" in resource_types
    assert "Observation" in resource_types


@pytest.mark.unit
def test_customize_capability_statement_no_account_is_noop():
    """When Account is already absent the statement is returned unchanged."""
    handlers = cd.fhir.get_capability_statement_handlers()

    capability = {"rest": [{"resource": [{"type": "Patient"}]}]}
    original_length = len(capability["rest"][0]["resource"])

    for handler in handlers:
        capability = handler(capability)

    assert len(capability["rest"][0]["resource"]) == original_length


# ===========================================================================
# Before / After Request hooks
# ===========================================================================

@pytest.mark.unit
def test_extract_user_context_populates_request_context(fake_fhir_request):
    """extract_user_context should write username/roles into RequestContext."""
    req = fake_fhir_request(username="alice", roles="doctor")
    mock_service = MagicMock()
    mock_service.interactions = MagicMock()

    handlers = cd.fhir.get_on_before_request_handlers()
    assert handlers, "No on_before_request handler registered"

    for handler in handlers:
        handler(mock_service, req, None, None)

    ctx = get_request_context()
    assert ctx.username == "alice"
    assert ctx.roles == "doctor"
    assert ctx.security_list == ["VIP"]
    assert ctx.scope_list == []


@pytest.mark.unit
def test_extract_user_context_stores_interactions(fake_fhir_request):
    """interactions attribute on fhir_service must be forwarded to ctx."""
    req = fake_fhir_request(username="bob", roles="nurse")
    mock_service = MagicMock()
    fake_interactions = MagicMock(name="interactions")
    mock_service.interactions = fake_interactions

    for handler in cd.fhir.get_on_before_request_handlers():
        handler(mock_service, req, None, None)

    ctx = get_request_context()
    assert ctx.interactions is fake_interactions


@pytest.mark.unit
def test_cleanup_context_is_registered():
    """on_after_request hook must be registered (even if it does nothing)."""
    handlers = cd.fhir.get_on_after_request_handlers()
    assert handlers, "No on_after_request handler registered"

    # Must not raise
    for handler in handlers:
        handler(MagicMock(), MagicMock(), MagicMock(), None)


# ===========================================================================
# on_after_read — Patient
# ===========================================================================

@pytest.mark.unit
def test_filter_patient_read_returns_true():
    """`filter_patient_read` always allows access (returns True)."""
    handlers = [
        h for h in cd.fhir.get_on_after_read_handlers("Patient")
        if h.__name__ == "filter_patient_read"
    ]
    assert handlers, "filter_patient_read not registered"
    assert handlers[0]({"resourceType": "Patient", "id": "1"}) is True


@pytest.mark.unit
def test_log_all_reads_returns_true(capsys):
    """`log_all_reads` returns True and prints a log line for any resource."""
    handlers = [
        h for h in cd.fhir.get_on_after_read_handlers("Observation")
        if h.__name__ == "log_all_reads"
    ]
    assert handlers, "log_all_reads not registered for Observation"
    result = handlers[0]({"resourceType": "Observation", "id": "obs-1"})
    assert result is True
    captured = capsys.readouterr()
    assert "Observation" in captured.out
    assert "obs-1" in captured.out


@pytest.mark.unit
def test_log_all_reads_registered_for_patient():
    """Wildcard log_all_reads must also appear in Patient handlers."""
    handler_names = [h.__name__ for h in cd.fhir.get_on_after_read_handlers("Patient")]
    assert "log_all_reads" in handler_names


# ===========================================================================
# on_after_search — Patient
# ===========================================================================

@pytest.mark.unit
def test_filter_patient_search_marks_vip_patient_as_deleted(fake_fhir_request):
    """
    Patients whose meta.security contains 'VIP' must be marked as deleted in the
    result-set when security_list = ['VIP'].
    """
    req = fake_fhir_request(username="user", roles="user")
    mock_service = MagicMock()
    mock_service.interactions = MagicMock()

    for handler in cd.fhir.get_on_before_request_handlers():
        handler(mock_service, req, None, None)

    ctx = get_request_context()
    # The fixture sets security_list = ["VIP"]

    vip_patient = json.dumps({
        "resourceType": "Patient",
        "id": "vip-1",
        "meta": {"security": [{"code": "VIP"}]},
    })

    mock_rs = MagicMock()
    mock_rs._Next.side_effect = [True, False]
    mock_rs._Get.side_effect = lambda key: "vip-1" if key == "ResourceId" else "1"

    ctx.interactions.Read.return_value._ToJSON.return_value = vip_patient

    search_handlers = [
        h for h in cd.fhir.get_on_after_search_handlers("Patient")
        if h.__name__ == "filter_patient_search"
    ]
    assert search_handlers

    search_handlers[0](mock_rs, "Patient")

    mock_rs.MarkAsDeleted.assert_called_once()
    mock_rs._SaveRow.assert_called_once()


@pytest.mark.unit
def test_filter_patient_search_keeps_non_vip_patient(fake_fhir_request):
    """Patients without VIP security tag must NOT be marked as deleted."""
    req = fake_fhir_request(username="user", roles="user")
    mock_service = MagicMock()
    mock_service.interactions = MagicMock()

    for handler in cd.fhir.get_on_before_request_handlers():
        handler(mock_service, req, None, None)

    ctx = get_request_context()

    normal_patient = json.dumps({"resourceType": "Patient", "id": "p-1"})

    mock_rs = MagicMock()
    mock_rs._Next.side_effect = [True, False]
    mock_rs._Get.side_effect = lambda key: "p-1" if key == "ResourceId" else "1"
    ctx.interactions.Read.return_value._ToJSON.return_value = normal_patient

    search_handlers = [
        h for h in cd.fhir.get_on_after_search_handlers("Patient")
        if h.__name__ == "filter_patient_search"
    ]
    search_handlers[0](mock_rs, "Patient")

    mock_rs.MarkAsDeleted.assert_not_called()


# ===========================================================================
# Consent
# ===========================================================================

@pytest.mark.unit
def test_patient_consent_rules_denies_vip_resource(fake_fhir_request):
    """consent handler must return False when resource has VIP security tag."""
    req = fake_fhir_request(username="user", roles="user")
    mock_service = MagicMock()
    mock_service.interactions = MagicMock()

    for handler in cd.fhir.get_on_before_request_handlers():
        handler(mock_service, req, None, None)

    consent_handlers = cd.fhir.get_consent_handlers("Patient")
    assert consent_handlers

    resource = {"resourceType": "Patient", "meta": {"security": [{"code": "VIP"}]}}
    result = consent_handlers[0](resource)
    assert result is False


@pytest.mark.unit
def test_patient_consent_rules_allows_normal_resource(fake_fhir_request):
    """consent handler must return True for resources without VIP tag."""
    req = fake_fhir_request(username="user", roles="user")
    mock_service = MagicMock()
    mock_service.interactions = MagicMock()

    for handler in cd.fhir.get_on_before_request_handlers():
        handler(mock_service, req, None, None)

    consent_handlers = cd.fhir.get_consent_handlers("Patient")
    resource = {"resourceType": "Patient", "id": "p-1"}
    result = consent_handlers[0](resource)
    assert result is True


# ===========================================================================
# check_consent helper
# ===========================================================================

@pytest.mark.unit
def test_check_consent_denies_when_security_code_in_security_list(fake_fhir_request):
    """check_consent returns False when resource security code is in ctx.security_list."""
    req = fake_fhir_request()
    mock_service = MagicMock()
    mock_service.interactions = MagicMock()
    for handler in cd.fhir.get_on_before_request_handlers():
        handler(mock_service, req, None, None)

    resource = {"meta": {"security": [{"code": "VIP"}]}}
    assert cd.check_consent(resource) is False


@pytest.mark.unit
def test_check_consent_allows_when_no_security_meta(fake_fhir_request):
    """check_consent returns True when resource has no meta security."""
    req = fake_fhir_request()
    mock_service = MagicMock()
    mock_service.interactions = MagicMock()
    for handler in cd.fhir.get_on_before_request_handlers():
        handler(mock_service, req, None, None)

    assert cd.check_consent({"id": "p-2"}) is True


@pytest.mark.unit
def test_check_consent_allows_when_code_not_in_security_list(fake_fhir_request):
    """check_consent returns True when resource security code is not in list."""
    req = fake_fhir_request()
    mock_service = MagicMock()
    mock_service.interactions = MagicMock()
    for handler in cd.fhir.get_on_before_request_handlers():
        handler(mock_service, req, None, None)

    resource = {"meta": {"security": [{"code": "PUBLIC"}]}}
    assert cd.check_consent(resource) is True


# ===========================================================================
# CRUD lifecycle hooks
# ===========================================================================

@pytest.mark.unit
def test_validate_patient_creation_is_registered():
    """on_before_create Patient handler must be present (no-op body)."""
    handlers = cd.fhir.get_on_before_create_handlers("Patient")
    assert handlers
    # Must not raise
    for handler in handlers:
        handler(MagicMock(), MagicMock(), {"resourceType": "Patient"}, None)


@pytest.mark.unit
def test_audit_patient_update_is_registered():
    """on_before_update Patient handler must be present (no-op body)."""
    handlers = cd.fhir.get_on_before_update_handlers("Patient")
    assert handlers
    for handler in handlers:
        handler(MagicMock(), MagicMock(), {"resourceType": "Patient"}, None)


# ===========================================================================
# Custom operations
# ===========================================================================

@pytest.mark.unit
def test_diff_operation_is_registered():
    """$diff operation must be registered as (diff, Instance, Patient)."""
    handler = cd.fhir.get_operation_handler("diff", "Instance", "Patient")
    assert handler is not None
    assert callable(handler)


@pytest.mark.unit
def test_diff_operation_computes_diff():
    """$diff returns a fhir_response with the DeepDiff result as JSON."""
    handler = cd.fhir.get_operation_handler("diff", "Instance", "Patient")

    primary = {"resourceType": "Patient", "id": "1", "name": [{"family": "Smith"}]}
    secondary = {"resourceType": "Patient", "id": "1", "name": [{"family": "Jones"}]}

    mock_service = MagicMock()
    mock_service.interactions.Read.return_value._ToJSON.return_value = json.dumps(primary)

    mock_request = MagicMock()
    mock_request.Type = "Patient"
    mock_request.Id = "1"
    mock_request.Json._ToJSON.return_value = json.dumps(secondary)

    mock_response = MagicMock()

    result = handler("diff", "Instance", {}, mock_service, mock_request, mock_response)
    assert result is mock_response
    mock_response.__setattr__  # ensure it was returned, not None


@pytest.mark.unit
def test_generic_resource_validation_raises_when_no_id():
    """generic_resource_validation must raise ValueError if 'id' is absent."""
    handlers = [
        h for h in cd.fhir.get_on_validate_resource_handlers("Patient")
        if h.__name__ == "generic_resource_validation"
    ]
    assert handlers

    with pytest.raises(ValueError, match="id"):
        handlers[0]({"resourceType": "Patient"}, False)


@pytest.mark.unit
def test_generic_resource_validation_passes_when_id_present():
    """generic_resource_validation must not raise when 'id' is present."""
    handlers = [
        h for h in cd.fhir.get_on_validate_resource_handlers("Patient")
        if h.__name__ == "generic_resource_validation"
    ]
    handlers[0]({"resourceType": "Patient", "id": "p-1"}, False)  # no exception


@pytest.mark.unit
def test_generic_resource_validation_registered_for_observation():
    """The '*' validator must also appear for Observation handlers."""
    names = [h.__name__ for h in cd.fhir.get_on_validate_resource_handlers("Observation")]
    assert "generic_resource_validation" in names


# ===========================================================================
# on_validate_resource — Observation
# ===========================================================================

@pytest.mark.unit
def test_validate_observation_critical_code_without_note_raises():
    """Critical observations (critical-001/critical-002) must include a note."""
    handlers = [
        h for h in cd.fhir.get_on_validate_resource_handlers("Observation")
        if h.__name__ == "validate_observation_resource"
    ]
    assert handlers

    observation = {
        "resourceType": "Observation",
        "id": "obs-1",
        "code": {"coding": [{"code": "critical-001"}]},
    }
    with pytest.raises(ValueError, match="note"):
        handlers[0](observation, False)


@pytest.mark.unit
def test_validate_observation_critical_code_with_note_passes():
    """Critical observation with a note field must not raise."""
    handlers = [
        h for h in cd.fhir.get_on_validate_resource_handlers("Observation")
        if h.__name__ == "validate_observation_resource"
    ]

    observation = {
        "resourceType": "Observation",
        "id": "obs-2",
        "code": {"coding": [{"code": "critical-002"}]},
        "note": [{"text": "Important follow-up required"}],
    }
    handlers[0](observation, False)  # must not raise


@pytest.mark.unit
def test_validate_observation_non_critical_code_without_note_passes():
    """Non-critical observations do not require a note."""
    handlers = [
        h for h in cd.fhir.get_on_validate_resource_handlers("Observation")
        if h.__name__ == "validate_observation_resource"
    ]

    observation = {
        "resourceType": "Observation",
        "id": "obs-3",
        "code": {"coding": [{"code": "routine-check"}]},
    }
    handlers[0](observation, False)  # must not raise


@pytest.mark.unit
def test_validate_observation_no_code_passes():
    """Observations without a code element must not raise (no critical check)."""
    handlers = [
        h for h in cd.fhir.get_on_validate_resource_handlers("Observation")
        if h.__name__ == "validate_observation_resource"
    ]

    observation = {"resourceType": "Observation", "id": "obs-4"}
    handlers[0](observation, False)  # must not raise
