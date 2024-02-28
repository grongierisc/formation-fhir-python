from unittest.mock import MagicMock

import json
import unittest
from custom import CustomOperationHandler
from EAI import fixtures

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
        fhir_response = MagicMock()
        
        # Set up primary_resource and secondary_resource for testing
        primary_resource = {}  # Replace with actual primary resource
        secondary_resource = {}  # Replace with actual secondary resource
        fhir_service.interactions.Read.return_value = json.dumps(primary_resource)
        fhir_request.Json._ToJSON.return_value = json.dumps(secondary_resource)
        
        expected_result = {}  # Replace with expected result
        
        result = handler.process_operation(operation_name, operation_scope, {}, fhir_service, fhir_request, fhir_response)
        
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()