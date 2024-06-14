from typing import List
from pydantic import BaseModel

class Record(BaseModel):
    key: str | dict | None = None
    value: str | dict | None = None

class Certificate(BaseModel):
    ca_location: str
    cert_location: str
    key_location: str
    password: str

class Request(BaseModel):
    topic: str
    brokers: List[str]
    schema_registry: str | None = None
    certificate: Certificate | None = None
    
    has_key_schema: bool = False
    has_value_schema: bool = False
    records: List[Record] | None = None
