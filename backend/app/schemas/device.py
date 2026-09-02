from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    hostname: str
    ip_address: str
    mac_address: Optional[str] = None
    device_type: Optional[str] = "Server"
    os_version: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    is_monitored: bool = True
    monitoring_interval: int = 60

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(DeviceBase):
    hostname: Optional[str] = None
    ip_address: Optional[str] = None

class DeviceResponse(DeviceBase):
    id: int
    status: str
    last_seen: Optional[datetime] = None
    latency: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
