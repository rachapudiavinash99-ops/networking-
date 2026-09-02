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
