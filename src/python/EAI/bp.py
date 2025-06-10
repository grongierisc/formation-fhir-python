from iop import BusinessProcess
import iris
import jwt
import json
from fhir.resources import patient, bundle

class MyBusinessProcess(BusinessProcess):

    def on_init(self):
        if not hasattr(self, 'target'):
            self.target = 'HS.FHIRServer.Interop.HTTPOperation'
            return
        
    def to_request(self, request):
        self.log_info('Received a request')

    def on_fhir_request(self, request:'iris.HS.FHIRServer.Interop.Request'):
        # Do something with the request
        self.log_info('Received a FHIR request')

        self.logger.debug(f'Request: {request}')

        token_id = request.Request.AdditionalInfo.GetAt("USER:TokenId")

        token = self.get_token_string(token_id)

        # pass it to the target
        rsp = self.send_request_sync(self.target, request)

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
        raise NotImplementedError('You must implement the check_token method')

    def filter_patient_resource(self, patient_str:str) -> str:
        raise NotImplementedError('You must implement the filter_patient_resource method')

    def filter_resources(self, resource_str:str) -> str:
        raise NotImplementedError('You must implement the filter_resources method')

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