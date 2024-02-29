from unittest.mock import MagicMock

import json
import unittest
from custom import CustomOperationHandler
import fixtures
import iris

class TestCustomOperationHandler(unittest.TestCase):
    
    def test_add_supported_operations(self):
        handler = CustomOperationHandler()
        map = {}
        result = handler.add_supported_operations(map)
        excepted_result = {'resource': 
                           {'Patient': 
                            [{'name': 'merge', 'definition': 'http://hl7.org/fhir/OperationDefinition/Patient-merge'}]
                            }
                        }
        self.assertEqual(result, excepted_result)
    
    def test_process_operation_merge(self):
        handler = CustomOperationHandler()
        operation_name = 'merge'
        operation_scope = 'Instance'

        fhir_service = MagicMock()
        fhir_request = MagicMock()
        fhir_request.RequestMethod = 'POST'
        fhir_response = MagicMock()
        
        # Set up primary_resource and secondary_resource for testing
        primary_resource = json.loads(fixtures.FHIR_PATIENT)
        secondary_resource = primary_resource.copy()
        secondary_resource['address'] = [{'city': 'Paris', 'line': ['Rue de la Paix']}]
        fhir_service.interactions.Read.return_value = iris.cls('%DynamicObject')._FromJSON(json.dumps(primary_resource))
        fhir_request.Json._ToJSON.return_value = json.dumps(secondary_resource)
        
        expected_result = '{"dictionary_item_removed": ["root[\'address\'][0][\'postalCode\']", "root[\'address\'][0][\'state\']"], "values_changed": {"root[\'address\'][0][\'city\']": {"new_value": "Paris", "old_value": "Lynnfield"}, "root[\'address\'][0][\'line\'][0]": {"new_value": "Rue de la Paix", "old_value": "672 Bartoletti Arcade"}}}'  # Replace with expected result
        
        result = handler.process_operation(operation_name, operation_scope, {}, fhir_service, fhir_request, fhir_response)
        
        self.assertEqual(json.loads(result.Json._ToJSON()), json.loads(expected_result))

if __name__ == '__main__':
    unittest.main()