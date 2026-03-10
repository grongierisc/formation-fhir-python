from iop import BusinessProcess
import iris
import jwt
import json

from msg import FhirRequest

class FhirMainProcess(BusinessProcess):

    target = 'FHIR_MAIN_HTTP'

    def on_fhir_request(self, request:'iris.HS.FHIRServer.Interop.Request'):
        # Do something with the request
        self.log_info('Received a FHIR request')

        self.logger.debug(f'Request: {request}')

        token_id = request.Request.AdditionalInfo.GetAt("USER:TokenId")

        token = self.get_token_string(token_id)

        # before sending the request, check to a random rest api call
        random_rest_response = self.send_request_sync('RANDOM_REST_HTTP', FhirRequest(
            url=None,
            resource=None,
            method='GET',
            data='',
            headers={}
        ))

        self.log_info(f'Response from random rest api: {random_rest_response}')

        # pass it to the target
        rsp = self.send_request_sync(self.target, request)

        # Do something with the response
        if self.check_token(token):
            self.log_info('Filtering the response')
            # Filter the response
            payload_str = self.quick_stream_to_string(rsp.QuickStreamId)

            # if the payload is empty, return the response
            if payload_str == '':
                return rsp

            filtered_payload_string = self.filter_resources(json.loads(payload_str))

            # write the json string to a quick stream
            quick_stream = self.string_to_quick_stream(json.dumps(filtered_payload_string))

            rsp = rsp._ConstructClone(1)
            # return the response
            rsp.QuickStreamId = quick_stream._Id()

        return rsp
    
    def get_token_string(self, token_id:str) -> str:
        """
        Returns the token string from the JWT token.
        """
        ## ##class(HS.HC.Util.InfoCache).GetTokenInfoItem(tokenCacheId, "token_string")
        token_info = iris.cls('HS.HC.Util.InfoCache').GetTokenInfoItem(token_id, 'token_string')
        if not token_info:
            raise ValueError(f'Token with ID {token_id} not found in the cache.')
        return token_info

    def check_token(self, token:str) -> bool:

        # decode the token
        try:
            decoded_token= jwt.decode(token, options={"verify_signature": False})
        except jwt.exceptions.DecodeError:
            return False

        # check if the token is valid
        if 'VIP' in decoded_token['scope']:
            return True
        else:
            return False

    def filter_patient_resource(self, patient_dict:dict) -> dict:
        # filter the patient
        # remove the name
        del patient_dict['name']
        # remove the address
        patient_dict['address'] = None
        # remove the telecom
        patient_dict['telecom'] = []
        # remove the birthdate
        patient_dict['birthDate'] = None

        return patient_dict

    def filter_resources(self, resource_dict:dict) -> dict:
        # what is the resource type?
        resource_type = resource_dict['resourceType'] if 'resourceType' in resource_dict else 'None'
        self.log_info('Resource type: ' + resource_type)

        # is it a bundle?
        if resource_type == 'Bundle':
            # filter the bundle
            for entry in resource_dict['entry']:
                if entry['resource']['resourceType'] == 'Patient':
                    self.log_info('Filtering a patient')
                    entry['resource'] = self.filter_patient_resource(entry['resource'])

        elif resource_type == 'Patient':
            # filter the patient
            payload_dict = self.filter_patient_resource(resource_dict)
        else:
            self.log_info('Resource type is not supported for filtering: ' + resource_type)
            return resource_dict

        return resource_dict

    def quick_stream_to_string(self, quick_stream_id) -> str:
        quick_stream = iris.cls('HS.SDA3.QuickStream')._OpenId(quick_stream_id)
        json_payload = ''
        while quick_stream.AtEnd == 0:
            json_payload += quick_stream.Read()

        return json_payload
    
    def string_to_quick_stream(self, json_string:str):
        quick_stream = iris.cls('HS.SDA3.QuickStream')._New()

        # write the json string to the payload
        n = 3000
        chunks = [json_string[i:i+n] for i in range(0, len(json_string), n)]
        for chunk in chunks:
            quick_stream.Write(chunk)

        return quick_stream