from grongier.pex import BusinessProcess

import iris

import jwt
import json

from fhir.resources import patient, bundle, resource

class MyBusinessProcess(BusinessProcess):

    def on_init(self):
        if not hasattr(self, 'target'):
            self.target = 'HS.FHIRServer.Interop.HTTPOperation'
            return

    def on_fhir_request(self, request:'iris.HS.FHIRServer.Interop.Request'):
        # Do something with the request
        self.log_info('Received a FHIR request')

        # Try to get the token from the request
        token = request.Request.AdditionalInfo.GetAt("USER:OAuthToken") or ""

        decoded_jwt = None

        to_filter = True

        # Check if token is a jwt
        try:
            decoded_jwt = jwt.decode(token, verify=False)
        except jwt.exceptions.DecodeError:
            self.log_error('Token is not a jwt')

        # Check scopes
        if decoded_jwt and 'user/Patient.read' in decoded_jwt['scope']:
            self.log_info('Token has the right scope')
            to_filter = True
        else:
            self.log_error('Token does not have the right scope')

        # pass it to the target
        rsp = self.send_request_sync(self.target, request)

        # Do something with the response
        if to_filter:
            self.log_info('Filtering the response')
            # Filter the response
            # get the response body
            quick_stream_id = rsp.QuickStreamId
            quick_stream = iris.cls('HS.SDA3.QuickStream')._OpenId(quick_stream_id)
            json_payload = ''
            while quick_stream.AtEnd == 0:
                json_payload += quick_stream.Read()

            if json_payload == '':
                return rsp

            payload = json.loads(json_payload)

            # what is the resource type?
            resource_type = payload['resourceType'] if 'resourceType' in payload else None
            self.log_info('Resource type: ' + resource_type)

            # is it a bundle?
            if resource_type == 'Bundle':
                obj = bundle.Bundle(**payload)
                # filter the bundle
                for entry in obj.entry:
                    if entry.resource.resource_type == 'Patient':
                        self.log_info('Filtering a patient')
                        # filter the patient
                        p = patient.Patient(**entry.resource.dict())
                        # remove the name
                        p.name = []
                        # remove the address
                        p.address = []
                        # remove the telecom
                        p.telecom = []
                        # remove the birthdate
                        p.birthDate = None
                        # update the entry
                        entry.resource = p
            elif resource_type == 'Patient':
                # filter the patient
                obj = patient.Patient(**payload)
                # remove the name
                obj.name = []
                # remove the address
                obj.address = []
                # remove the telecom
                obj.telecom = []
                # remove the birthdate
                obj.birthDate = None

            # update the response body
            # clear the payload
            quick_stream = iris.cls('HS.SDA3.QuickStream')._New()

            # write the json string to the payload
            json_string = obj.json()
            n = 3000
            chunks = [json_string[i:i+n] for i in range(0, len(json_string), n)]
            for chunk in chunks:
                quick_stream.Write(chunk)

            rsp.QuickStreamId = quick_stream._Id()

        return rsp
