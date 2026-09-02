from fastapi import APIRouter, Depends, HTTPException
from app.schemas.diagnostics import PingRequest, TcpRequest, DnsRequest, SubnetRequest
from app.utils.network import ping_host, check_tcp_port, resolve_dns, calculate_subnet
from app.core.security import get_current_user

router = APIRouter()

@router.post("/ping")
def ping(request: PingRequest, current_user = None):
    return ping_host(request.host)

@router.post("/tcp")
def tcp_check(request: TcpRequest, current_user = None):
    return check_tcp_port(request.host, request.port)

@router.post("/dns")
def dns_lookup(request: DnsRequest, current_user = None):
    return resolve_dns(request.hostname)

@router.post("/subnet")
def subnet_calc(request: SubnetRequest, current_user = None):
    result = calculate_subnet(request.cidr)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
