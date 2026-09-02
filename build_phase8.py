import os

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

write_file('backend/app/utils/network.py', '''
import subprocess
import socket
import ipaddress
import platform

def ping_host(host: str) -> dict:
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        return {"status": "SUCCESS", "output": output}
    except subprocess.CalledProcessError as e:
        return {"status": "FAILED", "output": e.output}

def check_tcp_port(host: str, port: int, timeout: int = 2) -> dict:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return {"status": "OPEN", "host": host, "port": port}
        else:
            return {"status": "CLOSED", "host": host, "port": port}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def resolve_dns(hostname: str) -> dict:
    try:
        ip = socket.gethostbyname(hostname)
        return {"hostname": hostname, "ip": ip, "status": "SUCCESS"}
    except Exception as e:
        return {"hostname": hostname, "status": "FAILED", "error": str(e)}

def calculate_subnet(cidr: str) -> dict:
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        return {
            "network_address": str(network.network_address),
            "broadcast_address": str(network.broadcast_address),
            "netmask": str(network.netmask),
            "num_addresses": network.num_addresses,
            "usable_hosts": max(0, network.num_addresses - 2),
            "version": network.version
        }
    except ValueError as e:
        return {"error": str(e)}
''')

write_file('backend/app/schemas/diagnostics.py', '''
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
''')

write_file('backend/app/api/endpoints/diagnostics.py', '''
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.diagnostics import PingRequest, TcpRequest, DnsRequest, SubnetRequest
from app.utils.network import ping_host, check_tcp_port, resolve_dns, calculate_subnet
from app.core.security import get_current_user

router = APIRouter()

@router.post("/ping")
def ping(request: PingRequest, current_user = Depends(get_current_user)):
    return ping_host(request.host)

@router.post("/tcp")
def tcp_check(request: TcpRequest, current_user = Depends(get_current_user)):
    return check_tcp_port(request.host, request.port)

@router.post("/dns")
def dns_lookup(request: DnsRequest, current_user = Depends(get_current_user)):
    return resolve_dns(request.hostname)

@router.post("/subnet")
def subnet_calc(request: SubnetRequest, current_user = Depends(get_current_user)):
    result = calculate_subnet(request.cidr)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
''')

write_file('backend/app/api/endpoints/__init__.py', '''
from fastapi import APIRouter
from app.api.endpoints.health import router as health_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.devices import router as devices_router
from app.api.endpoints.diagnostics import router as diagnostics_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(devices_router, prefix="/devices", tags=["devices"])
api_router.include_router(diagnostics_router, prefix="/diagnostics", tags=["diagnostics"])
''')

print("Phase 8 generated successfully")
