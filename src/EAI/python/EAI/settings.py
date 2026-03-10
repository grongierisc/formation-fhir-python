from bp import FhirMainProcess
from bo import FhirHttpOperation, RandomRestOperation


CLASSES = {
    'Python.EAI.bp.FhirMainProcess' : FhirMainProcess, 
    'Python.EAI.bo.FhirHttpOperation' : FhirHttpOperation,
    'Python.EAI.bo.RandomRestOperation' : RandomRestOperation
}

PRODUCTIONS = [
{
    "EAIPKG.FoundationProduction": {
        "@Name": "EAIPKG.FoundationProduction",
        "@LogGeneralTraceEvents": "false",
        "Description": "",
        "ActorPoolSize": "1",
        "Item": [
            {
                "@Name": "InteropService",
                "@Category": "",
                "@ClassName": "HS.FHIRServer.Interop.Service",
                "@PoolSize": "0",
                "@Enabled": "true",
                "@Foreground": "false",
                "@Comment": "",
                "@LogTraceEvents": "false",
                "@Schedule": "",
                "Setting": [
                    {
                        "@Target": "Host",
                        "@Name": "TargetConfigName",
                        "#text": "FHIR_MAIN"
                    },
                    {
                        "@Target": "Host",
                        "@Name": "TraceOperations",
                        "#text": "*FULL*"
                    }
                ]
            },
            {
                "@Name": "RANDOM_REST_HTTP",
                "@Category": "",
                "@ClassName": "Python.EAI.bo.RandomRestOperation",
                "@PoolSize": "1",
                "@Enabled": "true",
            },
            {
                "@Name": "FHIR_MAIN_HTTP",
                "@Category": "",
                "@ClassName": "HS.FHIRServer.Interop.HTTPOperation",
                "@PoolSize": "1",
                "@Enabled": "true",
                "@Foreground": "false",
                "@Comment": "",
                "@LogTraceEvents": "false",
                "@Schedule": "",
                "Setting": [
                    {
                        "@Target": "Host",
                        "@Name": "ServiceName",
                        "#text": "fhir"
                    },
                    {
                        "@Target": "Host",
                        "@Name": "TraceOperations",
                        "#text": "*FULL*"
                    }
                ]
            },
            {
                "@Name": "FHIR_MAIN",
                "@Category": "",
                "@ClassName": "Python.EAI.bp.FhirMainProcess",
                "@PoolSize": "1",
                "@Enabled": "true",
                "@Foreground": "false",
                "@Comment": "",
                "@LogTraceEvents": "false",
                "@Schedule": ""
            },
            {
                "@Name": "HS.Util.Trace.Operations",
                "@Category": "",
                "@ClassName": "HS.Util.Trace.Operations",
                "@PoolSize": "1",
                "@Enabled": "true",
                "@Foreground": "false",
                "@Comment": "",
                "@LogTraceEvents": "false",
                "@Schedule": ""
            },
            {
                "@Name": "FHIR_PYTHON_HTTP",
                "@Category": "",
                "@ClassName": "Python.EAI.bo.FhirHttpOperation",
                "@PoolSize": "1",
                "@Enabled": "true",
                "@Foreground": "false",
                "@Comment": "",
                "@LogTraceEvents": "false",
                "@Schedule": "",
                "Setting": {
                    "@Target": "Host",
                    "@Name": "%settings",
                    "#text": "url=https://webgateway/fhir/r4"
                }
            }
        ]
    }
}
]