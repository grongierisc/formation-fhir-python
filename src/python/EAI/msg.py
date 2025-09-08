from iop import Message
from dataclasses import dataclass

@dataclass
class FhirConverterMessage(Message):
    input_filename: str
    input_data: str
    input_data_type: str
    root_template: str

@dataclass
class FhirConverterResponse(Message):
    status: int
    output_data: str
    output_filename: str


@dataclass
class FhirRequest(Message):
    url: str
    resource: str
    method: str
    data: str
    headers: dict

@dataclass
class FhirResponse(Message):
    status_code: int
    content: str
    headers: dict
    resource: str