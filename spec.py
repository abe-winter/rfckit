"spec.py -- pydantic parser for spec yaml files"

from typing import Literal, Union, List, Dict, Tuple, Optional
from pydantic import BaseModel

class Meta(BaseModel):
    ""
    format: Literal['rfckit']
    version: str

class RefBlock(BaseModel):
    ""
    url: Optional[str]
    section: Optional[str]
    desc: Optional[str]

# todo: hydrate raw strings parse as RefBlock
Ref = Union[str, RefBlock]

class Header(BaseModel):
    "title, source and other core properties of the app"
    title: str
    roles: List[str] # order for protocol diagram
    ref: Optional[Ref]

class Role(BaseModel):
    ""
    aka: Optional[List[str]] # 'also known as', aliases
    ref: Optional[Ref]
    icon: Optional[str] # unicode emoji or image URL

class RoutePayload(BaseModel):
    "describe what's in a request or response"
    kind: Optional[str]
    contents: Optional[List[str]]
    optional: Optional[List[str]]

class Request(BaseModel):
    ref: Optional[Ref]
    auth: Optional[str] # pointer to auth
    payload: Optional[List[RoutePayload]]
    label: Optional[str]

class Response(BaseModel):
    ref: Optional[Ref]
    payload: Optional[List[RoutePayload]]
    redirect: Optional[str]
    label: Optional[str]

class Endpoint(BaseModel):
    abbrev: Optional[str]
    ref: Optional[Ref]
    request: Optional[Request]
    checks: Optional[List[str]] # list of conditions server asserts
    response: Optional[Response]

class Payload(BaseModel):
    "describe an individual payload content"
    icon: Optional[str]
    ref: Optional[Ref]

class Auth(BaseModel):
    ref: Optional[Ref]

class FlowStep(BaseModel):
    ""
    roles: Tuple[str, str]
    ref: Optional[Ref]
    endpoint: Optional[str]
    request: bool = True
    response: bool = True
    label: Optional[str]

class Spec(BaseModel):
    "root document"
    meta: Meta
    header: Header
    roles: Dict[str, Role]
    endpoints: Dict[str, Endpoint]
    payloads: Dict[str, Payload]
    auth: Dict[str, Auth]
    flow: List[FlowStep]
