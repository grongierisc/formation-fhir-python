from obj import PermissionObj

FHIR_PATIENT = """{
    "resourceType": "Patient",
    "address": [
        {
            "city": "Lynnfield",
            "line": [
                "672 Bartoletti Arcade"
            ],
            "postalCode": "01940",
            "state": "Massachusetts"
        }
    ],
    "birthDate": "1994-08-02",
    "extension": [
        {
            "url": "http://intersystems.com/fhir/extn/sda3/lib/patient-entered-on",
            "valueDateTime": "2020-09-01T07:29:14+00:00"
        },
        {
            "url": "http://intersystems.com/fhir/extn/sda3/lib/patient-ethnic-group",
            "valueCodeableConcept": {
                "coding": [
                    {
                        "code": "2186-5",
                        "display": "non-hispanic",
                        "system": "urn:oid:2.16.840.1.113883.6.238"
                    }
                ]
            }
        },
        {
            "url": "http://intersystems.com/fhir/extn/sda3/lib/patient-races",
            "valueCodeableConcept": {
                "coding": [
                    {
                        "code": "2106-3",
                        "display": "white",
                        "system": "urn:oid:2.16.840.1.113883.6.238"
                    }
                ]
            }
        }
    ],
    "gender": "male",
    "identifier": [
        {
            "type": {
                "coding": [
                    {
                        "code": "MR",
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0203"
                    }
                ],
                "text": "MRN"
            },
            "value": "26504347-0230-8fa0-a625-db55483a3d2d"
        }
    ],
    "name": [
        {
            "family": "Gaylord",
            "given": [
                "Michal"
            ],
            "text": "Michal Gaylord",
            "use": "official"
        }
    ],
    "id": "1",
    "meta": {
        "lastUpdated": "2024-02-24T09:11:00Z",
        "versionId": "1"
    }
}"""

FHIR_BUNDLE_EMPTY = """{"resourceType":"Bundle","id":"93e46724-e9e1-11ee-a4d1-0242ac1e0002","type":"searchset","timestamp":"2024-03-24T13:22:35Z","total":0,"link":[{"relation":"self","url":"https://webgatewayfhir/fhir/r5/Patient"}]}"""

FHIR_BUNDLE = """{
    "resourceType": "Bundle",
    "id": "0880c8ac-d3ef-11ee-9bf3-0242ac170003",
    "type": "searchset",
    "timestamp": "2024-02-25T15:03:28Z",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "https://webgateway/fhir/r5/Patient"
        }
    ],
    "entry": [
        {
            "fullUrl": "https://webgateway/fhir/r5/Patient/1",
            "resource": {
                "resourceType": "Patient",
                "address": [
                    {
                        "city": "Lynnfield",
                        "line": [
                            "672 Bartoletti Arcade"
                        ],
                        "postalCode": "01940",
                        "state": "Massachusetts"
                    }
                ],
                "birthDate": "1994-08-02",
                "extension": [
                    {
                        "url": "http://intersystems.com/fhir/extn/sda3/lib/patient-entered-on",
                        "valueDateTime": "2020-09-01T07:29:14+00:00"
                    },
                    {
                        "url": "http://intersystems.com/fhir/extn/sda3/lib/patient-ethnic-group",
                        "valueCodeableConcept": {
                            "coding": [
                                {
                                    "code": "2186-5",
                                    "display": "non-hispanic",
                                    "system": "urn:oid:2.16.840.1.113883.6.238"
                                }
                            ]
                        }
                    },
                    {
                        "url": "http://intersystems.com/fhir/extn/sda3/lib/patient-races",
                        "valueCodeableConcept": {
                            "coding": [
                                {
                                    "code": "2106-3",
                                    "display": "white",
                                    "system": "urn:oid:2.16.840.1.113883.6.238"
                                }
                            ]
                        }
                    }
                ],
                "gender": "male",
                "identifier": [
                    {
                        "type": {
                            "coding": [
                                {
                                    "code": "MR",
                                    "system": "http://terminology.hl7.org/CodeSystem/v2-0203"
                                }
                            ],
                            "text": "MRN"
                        },
                        "value": "26504347-0230-8fa0-a625-db55483a3d2d"
                    }
                ],
                "name": [
                    {
                        "family": "Gaylord",
                        "given": [
                            "Michal"
                        ],
                        "text": "Michal Gaylord",
                        "use": "official"
                    }
                ],
                "id": "1",
                "meta": {
                    "lastUpdated": "2024-02-24T09:11:00Z",
                    "versionId": "1"
                }
            },
            "search": {
                "mode": "match"
            }
        }
    ]
}"""


VALIDE_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6MX0.eyJqdGkiOiJodHRwczovL3dlYmdhdGV3YXllYWkvb2F1dGgyLlFYNWJUcGJsQVVGNHYtTkVzazg3cWl1UWZIbyIsImlzcyI6Imh0dHBzOi8vd2ViZ2F0ZXdheWVhaS9vYXV0aDIiLCJzdWIiOiJtTlRjWDhLaEFwaVUyWWdYZ2FBcEJJQmxyZDZQRWFaU2ZUZDhuME9OV1ZjIiwiZXhwIjoxNzExMjgyMzM5LCJhdWQiOiJodHRwczovL3dlYmdhdGV3YXlmaGlyL2ZoaXIvcjUiLCJzY29wZSI6InN1cGVyUmVhZCB1c2VyLyouKiIsImlhdCI6MTcxMTI3ODczOX0.qQh03RoG2PJYEpdkkMOt4zK4aMjKHafnXir4wPVAbCsvZlUvvFQE43V-VsJ-Dr1D10Pe5SL0HkJGYsBWWoFk1EafW6LKwOqZJ3XlUN2wsTlRMWIbaApAMTr2if2dprpPOsaTIMsOfXJYjX8GpkJabCba4TEXqIG4Fs7uJTf1ok_p3s8jmQLWy68OVV6KgRByj9F7aN8f2t7ypd9K7rB0Uh0z3MLrhNy9c0Vt51NU5v9Rq7eYVeq1hHpb85w0ooh6MA2ttulJ28EP4IQ7nuqKpOY6yIWmqUnSNmHFd3yEWp6RP_LVVW0xK_5bUYRUPq7gAFSGr4bTwIoGYj35_NTuRg'
INVALID_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6MX0.eyJqdGkiOiJodHRwczovL3dlYmdhdGV3YXkvb2F1dGgyLjdLQkkzYmFhNHJkOURWLTVPNkgxemhGQnE0byIsImlzcyI6Imh0dHBzOi8vd2ViZ2F0ZXdheS9vYXV0aDIiLCJzdWIiOiJNM0pBMHBOM3dJenNncWVwQnR2aVBXMEhYeEZSZEN3RHBVSERGd2NTM0xvIiwiZXhwIjoxNzA4ODc1OTU2LCJhdWQiOiJodHRwczovL3dlYmdhdGV3YXkvZmhpci9yNSIsInNjb3BlIjoidXNlci9QYXRpZW50LnJlYWQiLCJpYXQiOjE3MDg4NzIzNTZ9.ajn_0hbhlJWeN9hNA74E6q9rPFNNvtW0zoKF07RnriNjyUyss7aD4mpFzaO19Mz2T5OI7uG9_XqUj8UHlRGN4oMuL3R7H9rJW036kIK-tL5MPomZDcTvrsNVaEca4C6fuUMmVu2Gqoa1vxMoG7HxGzAOKwqTppVy2ilm3L7ewnb0qCkT3S89ldaas7QycERWyF81qjl_Vz5BcjMZXJ5hTq8rPpvBCR81NCmwAdWHBHsMqFqmg1FSqq3xNiQBuxLYP5A1fdK06XIBcdTqk0EKlp5O0q1HMGrn8pgaPByyDtpBgtkjDA5mi_kenxCCkqRkqEkZYRcFG6OrVUKKsnBBUA'

PERMISSIONS = [ PermissionObj(resource_type="Patient", json_path="$.name")]

FHIR_N_BUNDLE = """{"resourceType":"Bundle","id":"3c26ad1e-eda6-11ee-ac13-0242ac120003","type":"searchset","timestamp":"2024-03-29T08:27:52Z","total":7,"link":[{"relation":"self","url":"https://webgatewayfhir/fhir/r5/Patient"}],"entry":[{"fullUrl":"https://webgatewayfhir/fhir/r5/Patient/1","resource":{"resourceType":"Patient","id":"1","extension":[{"url":"http://example.org/StructureDefinition/birthsex-extension","valueCode":"F"}],"name":[{"given":["Janette"],"family":"Smith"}],"maritalStatus":{"coding":[{"code":"M","system":"http://terminology.hl7.org/CodeSystem/v3-MaritalStatus","display":"Married"}]},"meta":{"lastUpdated":"2024-03-24T14:45:44Z","versionId":"1"}},"search":{"mode":"match"}},{"fullUrl":"https://webgatewayfhir/fhir/r5/Patient/2","resource":{"resourceType":"Patient","id":"2","meta":{"profile":["http://example.org/StructureDefinition/MyPatient"],"lastUpdated":"2024-03-25T11:03:15Z","versionId":"1"},"extension":[{"url":"http://example.org/StructureDefinition/birthsex-extension","valueCode":"F"}],"name":[{"given":["Janette"],"family":"Smith"}],"maritalStatus":{"coding":[{"code":"M","system":"http://terminology.hl7.org/CodeSystem/v3-MaritalStatus","display":"Married"}]}},"search":{"mode":"match"}},{"fullUrl":"https://webgatewayfhir/fhir/r5/Patient/3","resource":{"resourceType":"Patient","id":"3","meta":{"profile":["http://example.org/StructureDefinition/MyPatient"],"lastUpdated":"2024-03-25T11:03:37Z","versionId":"1"},"extension":[{"url":"http://example.org/StructureDefinition/birthsex-extension","valueCode":"F"}],"name":[{"given":["Janette"],"family":"Smith"}],"maritalStatus":{"coding":[{"code":"M","system":"http://terminology.hl7.org/CodeSystem/v3-MaritalStatus","display":"Married"}]}},"search":{"mode":"match"}},{"fullUrl":"https://webgatewayfhir/fhir/r5/Patient/4","resource":{"resourceType":"Patient","id":"4","meta":{"profile":["http://example.org/StructureDefinition/MyPatient"],"lastUpdated":"2024-03-25T11:22:08Z","versionId":"1"},"extension":[{"url":"http://example.org/StructureDefinition/birthsex-extension","valueCode":"F"}],"name":[{"given":["Janette"],"family":"Smith"}],"maritalStatus":{"coding":[{"code":"M","system":"http://terminology.hl7.org/CodeSystem/v3-MaritalStatus","display":"Married"}]}},"search":{"mode":"match"}},{"fullUrl":"https://webgatewayfhir/fhir/r5/Patient/5","resource":{"resourceType":"Patient","id":"5","meta":{"profile":["http://example.org/StructureDefinition/MyPatient"],"lastUpdated":"2024-03-25T11:22:08Z","versionId":"1"},"extension":[{"url":"http://example.org/StructureDefinition/birthsex-extension","valueCode":"F"}],"name":[{"given":["Janette"],"family":"Smith"}],"maritalStatus":{"coding":[{"code":"M","system":"http://terminology.hl7.org/CodeSystem/v3-MaritalStatus","display":"Married"}]}},"search":{"mode":"match"}},{"fullUrl":"https://webgatewayfhir/fhir/r5/Patient/6","resource":{"resourceType":"Patient","id":"6","meta":{"profile":["http://example.org/StructureDefinition/MyPatient"],"lastUpdated":"2024-03-25T11:22:17Z","versionId":"1"},"extension":[{"url":"http://example.org/StructureDefinition/birthsex-extension","valueCode":"F"}],"name":[{"given":["Janette"],"family":"Smith"}],"maritalStatus":{"coding":[{"code":"M","system":"http://terminology.hl7.org/CodeSystem/v3-MaritalStatus","display":"Married"}]}},"search":{"mode":"match"}},{"fullUrl":"https://webgatewayfhir/fhir/r5/Patient/7","resource":{"resourceType":"Patient","id":"7","extension":[{"url":"http://example.org/StructureDefinition/birthsex-extension","valueCode":"F"}],"name":[{"given":["Janette"],"family":"Smith"}],"maritalStatus":{"coding":[{"code":"M","system":"http://terminology.hl7.org/CodeSystem/v3-MaritalStatus","display":"Married"}]},"meta":{"lastUpdated":"2024-03-25T11:22:44Z","versionId":"1"}},"search":{"mode":"match"}}]}"""

FHIR_BUNDLE_PERMISSION = """{"resourceType":"Bundle","id":"f125ce56-f196-11ee-ac13-0242ac120003","type":"searchset","timestamp":"2024-04-03T08:48:28Z","total":2,"link":[{"relation":"self","url":"https://webgatewayfhir/fhir/r5/Permission"}],"entry":[{"fullUrl":"https://webgatewayfhir/fhir/r5/Permission/BOT","resource":{"resourceType":"Permission","id":"BOT","status":"active","combining":"permit-unless-deny","rule":[{"type":"deny","data":[{"security":[{"code":"VIP"}]},{"resource":[{"meaning":"instance","reference":{"display":"Patient"}}],"expression":{"language":"text/jsonpath","expression":"$.name"}},{"resource":[{"meaning":"instance","reference":{"display":"Patient"}}],"expression":{"language":"text/jsonpath","expression":"$.maritalStatus"}}]}],"meta":{"lastUpdated":"2024-03-29T12:49:28Z","versionId":"8"}},"search":{"mode":"match"}},{"fullUrl":"https://webgatewayfhir/fhir/r5/Permission/superRead","resource":{"resourceType":"Permission","id":"superRead","status":"active","date":["2018-12-24"],"combining":"permit-unless-deny","meta":{"lastUpdated":"2024-03-28T13:34:33Z","versionId":"2"}},"search":{"mode":"match"}}]}"""

FHIR_PERMISSION = """{"resourceType":"Permission","id":"BOT","status":"active","combining":"permit-unless-deny","rule":[{"type":"deny","data":[{"resource":[{"meaning":"instance","reference":{"display":"Patient"}}],"expression":{"language":"text/jsonpath","expression":"$.name"}}]}],"meta":{"lastUpdated":"2024-03-28T16:27:30Z","versionId":"6"}}"""