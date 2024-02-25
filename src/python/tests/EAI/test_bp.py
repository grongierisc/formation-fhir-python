from unittest.mock import MagicMock

from bp import MyBusinessProcess

import fixtures

import json

class TestMyBusinessProcess:

    def test_on_init(self):
        bp = MyBusinessProcess()
        bp.on_init()
        assert bp.target == 'HS.FHIRServer.Interop.HTTPOperation'

    def test_on_fhir_request(self):
        # initialize the business process
        bp = MyBusinessProcess()
        bp.on_init()
        # create a mock request
        request = MagicMock()
        # mock all the methods that are called on the request
        request.Request.AdditionalInfo.GetAt.return_value = "USER:OAuth Token"
        # create the expected response
        expected_rsp = MagicMock()
        # mock the send_request_sync method
        bp.send_request_sync = MagicMock(return_value=expected_rsp)
        # call the on_fhir_request method
        rsp = bp.on_fhir_request(request)
        assert rsp is not None

    def test_check_token_valid(self):
        bp = MyBusinessProcess()
        # scope is 'user/Patient.read VIP'
        token = fixtures.VALIDE_TOKEN
        result = bp.check_token(token)
        assert result is True

    def test_check_token_invalid(self):
        bp = MyBusinessProcess()
        # scope is 'user/Patient.read'
        token = fixtures.INVALID_TOKEN
        result = bp.check_token(token)
        assert result is False

    def test_quick_stream_to_string(self):
        bp = MyBusinessProcess()
        quick_stream_id = '12345'
        result = bp.quick_stream_to_string(quick_stream_id)
        assert isinstance(result, str)

    def test_string_to_quick_stream(self):
        bp = MyBusinessProcess()
        json_string = '{"name": "John Doe"}'
        result = bp.string_to_quick_stream(json_string)
        assert result is not None

    def test_filter_patient_resource(self):
        bp = MyBusinessProcess()
        patient_str = fixtures.FHIR_PATIENT
        result = bp.filter_patient_resource(patient_str)
        assert isinstance(result, str)
        dict_result = json.loads(result)
        # assert values are not present
        assert 'name' not in dict_result
        assert 'address' not in dict_result
        assert 'telecom' not in dict_result
        assert 'birthDate' not in dict_result
        

    def test_filter_resources_bundle(self):
        bp = MyBusinessProcess()
        resource_str = fixtures.FHIR_BUNDLE
        result = bp.filter_resources(resource_str)
        assert isinstance(result, str)
        dict_result = json.loads(result)
        # assert values are not present
        assert 'name' not in dict_result['entry'][0]['resource']
        assert 'address' not in dict_result['entry'][0]['resource']
        assert 'telecom' not in dict_result['entry'][0]['resource']
        assert 'birthDate' not in dict_result['entry'][0]['resource']

    def test_filter_resources_patient(self):
        bp = MyBusinessProcess()
        resource_str = fixtures.FHIR_PATIENT
        result = bp.filter_resources(resource_str)
        assert isinstance(result, str)
        dict_result = json.loads(result)
        # assert values are not present
        assert 'name' not in dict_result
        assert 'address' not in dict_result
        assert 'telecom' not in dict_result
        assert 'birthDate' not in dict_result