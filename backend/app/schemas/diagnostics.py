from pydantic import BaseModel

class PingRequest(BaseModel):
    host: str

class TcpRequest(BaseModel):
    host: str
    port: int
    
class DnsRequest(BaseModel):
    hostname: str
    
class SubnetRequest(BaseModel):
    cidr: str
