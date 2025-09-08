import iris

import os

iris.system.Process.SetNamespace('EAI')

from bp import MyBusinessProcess, FhirConverterProcess
from bo import FhirConverterOperation, FhirHttpOperation

CLASSES = {
    'Python.MyBusinessProcess' : MyBusinessProcess,
    'Python.FhirConverterProcess' : FhirConverterProcess,
    'Python.FhirConverterOperation' : FhirConverterOperation,
    'Python.FhirHttpOperation' : FhirHttpOperation
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
                        "#text": "Python.MyBusinessProcess"
                    },
                    {
                        "@Target": "Host",
                        "@Name": "TraceOperations",
                        "#text": "*FULL*"
                    }
                ]
            },
            {
                "@Name": "HS.FHIRServer.Interop.HTTPOperation",
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
                "@Name": "Python.MyBusinessProcess",
                "@Category": "",
                "@ClassName": "Python.MyBusinessProcess",
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
                "@Name": "Python.FhirHttpOperation",
                "@Category": "",
                "@ClassName": "Python.FhirHttpOperation",
                "@PoolSize": "4",
                "@Enabled": "true",
                "@Foreground": "false",
                "@Comment": "",
                "@LogTraceEvents": "false",
                "@Schedule": "",
                "Setting": {
                    "@Target": "Host",
                    "@Name": "%settings",
                    "#text": "url=https://default/fhir/r4"
                }
            },
            {
                "@Name": "Python.FhirConverterProcess",
                "@Category": "",
                "@ClassName": "Python.FhirConverterProcess",
                "@PoolSize": "1", 
                "@Enabled": "true",
                "@Foreground": "false",
                "@Comment": "",
                "@LogTraceEvents": "false",
                "@Schedule": ""
            },
            {
                "@Name": "Python.FhirConverterOperation",
                "@Category": "",
                "@ClassName": "Python.FhirConverterOperation",
                "@PoolSize": "4",
                "@Enabled": "true",
                "@Foreground": "false",
                "@Comment": "",
                "@LogTraceEvents": "false",
                "@Schedule": "",
                "Setting": {
                    "@Target": "Host",
                    "@Name": "%settings",
                    "#text": f"template_path={os.getenv('TEMPLATE_PATH', '/irisdev/app/templates')}"
                }
            },
            {
                "@Name": "IRIS.Hl7v2FileService",
                "@Category": "",
                "@ClassName": "EnsLib.HL7.Service.FileService",
                "@PoolSize": "1",
                "@Enabled": "true",
                "@Foreground": "false",
                "@Comment": "",
                "@LogTraceEvents": "false",
                "@Schedule": "",
                "Setting": [
                    {
                        "@Target": "Host",
                        "@Name": "MessageSchemaCategory",
                        "#text": "2.8"
                    },
                    {
                        "@Target": "Host",
                        "@Name": "TargetConfigNames",
                        "#text": "Python.FhirConverterProcess"
                    },
                    {
                        "@Target": "Adapter",
                        "@Name": "FilePath",
                        "#text": "/irisdev/app/misc/data/input/"
                    },
                    {
                        "@Target": "Adapter",
                        "@Name": "ArchivePath",
                        "#text": "/irisdev/app/misc/data/archive"
                    },
                    {
                        "@Target": "Adapter",
                        "@Name": "FileSpec",
                        "#text": "*.hl7"
                    }
                ]
            }
        ]
    }
}
]