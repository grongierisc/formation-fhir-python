from grongier.pex import BusinessProcess
import iris
import jwt
import json
from fhir.resources import patient, bundle

class MyBusinessProcess(BusinessProcess):

    def on_init(self):
        if not hasattr(self, 'target'):
            self.target = 'HS.FHIRServer.Interop.HTTPOperation'
            return

    def on_fhir_request(self, request:'iris.HS.FHIRServer.Interop.Request'):
        # Do something with the request
        self.log_info('Received a FHIR request')

        # pass it to the target
        rsp = self.send_request_sync(self.target, request)

        # Try to get the token from the request
        token = request.Request.AdditionalInfo.GetAt("USER:OAuthToken") or ""

        # Do something with the response
        if self.check_token(token):
            self.log_info('Filtering the response')
            # Filter the response
            payload_str = self.quick_stream_to_string(rsp.QuickStreamId)

            # if the payload is empty, return the response
            if payload_str == '':
                return rsp

            filtered_payload_string = self.filter_resources(payload_str)

            # write the json string to a quick stream
            quick_stream = self.string_to_quick_stream(filtered_payload_string)

            # return the response
            rsp.QuickStreamId = quick_stream._Id()

        return rsp
    
    def check_token(self, token:str) -> bool:

        # decode the token
        decoded_token= jwt.decode(token, options={"verify_signature": False})

        # check if the token is valid
        if 'VIP' in decoded_token['scope']:
            return True
        else:
            return False

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

    def filter_patient_resource(self, patient_str:str) -> str:
        # filter the patient
        p = patient.Patient(**json.loads(patient_str))
        # remove the name
        p.name = []
        # remove the address
        p.address = []
        # remove the telecom
        p.telecom = []
        # remove the birthdate
        p.birthDate = None

        return p.json()

    def filter_resources(self, resource_str:str) -> str:
        # parse the payload
        payload_dict = json.loads(resource_str)

        # what is the resource type?
        resource_type = payload_dict['resourceType'] if 'resourceType' in payload_dict else 'None'
        self.log_info('Resource type: ' + resource_type)

        # is it a bundle?
        if resource_type == 'Bundle':
            obj = bundle.Bundle(**payload_dict)
            # filter the bundle
            for entry in obj.entry:
                if entry.resource.resource_type == 'Patient':
                    self.log_info('Filtering a patient')
                    entry.resource = patient.Patient(**json.loads(self.filter_patient_resource(entry.resource.json())))

        elif resource_type == 'Patient':
            # filter the patient
            obj = patient.Patient(**json.loads(self.filter_patient_resource(resource_str)))

        return obj.json()
