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


VALIDE_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6MX0.eyJqdGkiOiJodHRwczovL3dlYmdhdGV3YXkvb2F1dGgyLlZobnBzRF9udC1Xb3dwT0ZIekQ4M00wVmc2TSIsImlzcyI6Imh0dHBzOi8vd2ViZ2F0ZXdheS9vYXV0aDIiLCJzdWIiOiJNM0pBMHBOM3dJenNncWVwQnR2aVBXMEhYeEZSZEN3RHBVSERGd2NTM0xvIiwiZXhwIjoxNzA4ODU2Mjc0LCJhdWQiOiJodHRwczovL3dlYmdhdGV3YXkvZmhpci9yNSIsInNjb3BlIjoiVklQIHVzZXIvUGF0aWVudC5yZWFkIiwiaWF0IjoxNzA4ODUyNjc0fQ.R5aVZlKyfhHxNAt4gjiGt5Vtp3W4wQSMWQ-fzpjR1w1aKTbOY0cy6Xa435RzNnyAIQdyxaA7FivgrvxrwWGhgTX4SjEvbimcspsnH4OQPiw0LRgzLC8jSnYaxQNb371SCvXQUJpxlpCfuJAHi5kjx-BBAklbuKIiYFj1OFCv8CNOOyzWBGNXEVrC3BxmDvcFtYEXU7EpVnBDXqvM-PjAWdeOSSw1aO2Pkd5UUVX3j4pdY-F9O2mC6Hb6mlpJZEtJFSAQUiqBZTIrvh9DWrPS9rLW_WRHApTNFAkzkvwPfOZMl59AOAwLcx9UCZa41RJg518vagXfepRUrmEb4tSssA'
INVALID_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6MX0.eyJqdGkiOiJodHRwczovL3dlYmdhdGV3YXkvb2F1dGgyLjdLQkkzYmFhNHJkOURWLTVPNkgxemhGQnE0byIsImlzcyI6Imh0dHBzOi8vd2ViZ2F0ZXdheS9vYXV0aDIiLCJzdWIiOiJNM0pBMHBOM3dJenNncWVwQnR2aVBXMEhYeEZSZEN3RHBVSERGd2NTM0xvIiwiZXhwIjoxNzA4ODc1OTU2LCJhdWQiOiJodHRwczovL3dlYmdhdGV3YXkvZmhpci9yNSIsInNjb3BlIjoidXNlci9QYXRpZW50LnJlYWQiLCJpYXQiOjE3MDg4NzIzNTZ9.ajn_0hbhlJWeN9hNA74E6q9rPFNNvtW0zoKF07RnriNjyUyss7aD4mpFzaO19Mz2T5OI7uG9_XqUj8UHlRGN4oMuL3R7H9rJW036kIK-tL5MPomZDcTvrsNVaEca4C6fuUMmVu2Gqoa1vxMoG7HxGzAOKwqTppVy2ilm3L7ewnb0qCkT3S89ldaas7QycERWyF81qjl_Vz5BcjMZXJ5hTq8rPpvBCR81NCmwAdWHBHsMqFqmg1FSqq3xNiQBuxLYP5A1fdK06XIBcdTqk0EKlp5O0q1HMGrn8pgaPByyDtpBgtkjDA5mi_kenxCCkqRkqEkZYRcFG6OrVUKKsnBBUA'