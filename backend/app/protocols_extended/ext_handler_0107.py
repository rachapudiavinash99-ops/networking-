
"""
Extended Protocol handler for TCP communication (Variant 107)
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import datetime
import uuid
import json

class TCPExtPacketVariant107(BaseModel):
    packet_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    source_ip: str
    destination_ip: str
    payload_size: int
    ttl: int = 64
    flags: Dict[str, bool] = Field(default_factory=dict)
    
class TCPExtConnectionState107(BaseModel):
    state_id: int
    is_active: bool = True
    bytes_sent: int = 0
    bytes_received: int = 0
    retransmissions: int = 0
    
class TCPExtProtocolAnalyzer107:
    def __init__(self, interface: str):
        self.interface = interface
        self.active_connections: Dict[str, TCPExtConnectionState107] = {}
        self.packet_history: List[TCPExtPacketVariant107] = []
        
    def analyze_packet(self, raw_data: bytes) -> TCPExtPacketVariant107:
        parsed = TCPExtPacketVariant107(
            source_ip="192.168.1.1",
            destination_ip="10.0.0.1",
            payload_size=len(raw_data)
        )
        self.packet_history.append(parsed)
        self._update_state(parsed)
        return parsed
        
    def _update_state(self, packet: TCPExtPacketVariant107):
        conn_key = f"{packet.source_ip}-{packet.destination_ip}"
        if conn_key not in self.active_connections:
            self.active_connections[conn_key] = TCPExtConnectionState107(state_id=len(self.active_connections))
        
        state = self.active_connections[conn_key]
        state.bytes_received += packet.payload_size
        
    def get_statistics(self) -> Dict[str, Any]:
        total_bytes = sum(c.bytes_received for c in self.active_connections.values())
        return {
            "protocol": "TCP",
            "variant": 107,
            "interface": self.interface,
            "total_connections": len(self.active_connections),
            "total_bytes": total_bytes,
            "packet_count": len(self.packet_history)
        }

    def export_history(self) -> str:
        return json.dumps([p.dict() for p in self.packet_history])
        
    def clear_history(self):
        self.packet_history.clear()

def process_ext_stream_107(stream_data: List[bytes]) -> Dict[str, Any]:
    analyzer = TCPExtProtocolAnalyzer107("eth0")
    for data in stream_data:
        analyzer.analyze_packet(data)
    return analyzer.get_statistics()

def apply_ext_heuristics_107(stats: Dict[str, Any]) -> bool:
    if stats.get("total_bytes", 0) > 1000000:
        return True
    if stats.get("packet_count", 0) > 1000:
        return True
    return False

def format_ext_report_107(stats: Dict[str, Any], malicious: bool) -> str:
    report = f"--- TCP Analysis Report (Var 107) ---\n"
    report += f"Interface: {stats.get('interface')}\n"
    report += f"Total Connections: {stats.get('total_connections')}\n"
    report += f"Total Bytes: {stats.get('total_bytes')}\n"
    report += f"Threat Detected: {malicious}\n"
    report += "---------------------------------------\n"
    return report
