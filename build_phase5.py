import os

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

write_file('backend/app/models/device.py', '''
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.db.base import Base

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, index=True, nullable=False)
    ip_address = Column(String, nullable=False)
    mac_address = Column(String)
    device_type = Column(String)  # Router, Switch, Server, etc.
    os_version = Column(String)
    location = Column(String)
    description = Column(String)
    
    is_monitored = Column(Boolean, default=True)
    monitoring_interval = Column(Integer, default=60)  # seconds
    
    status = Column(String, default="UNKNOWN")  # ONLINE, OFFLINE, WARNING, CRITICAL
    last_seen = Column(DateTime(timezone=True))
    latency = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
''')

write_file('backend/app/schemas/device.py', '''
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
''')

write_file('backend/app/api/endpoints/devices.py', '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse
from app.core.security import get_current_user
from typing import List, Any

router = APIRouter()

@router.get("/", response_model=List[DeviceResponse])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    devices = db.query(Device).offset(skip).limit(limit).all()
    return devices

@router.post("/", response_model=DeviceResponse)
def create_device(device_in: DeviceCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ["admin", "operator"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    device = Device(**device_in.dict())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device

@router.get("/{device_id}", response_model=DeviceResponse)
def read_device(device_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(device_id: int, device_in: DeviceUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in ["admin", "operator"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
        
    update_data = device_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(device, key, value)
        
    db.commit()
    db.refresh(device)
    return device

@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
        
    db.delete(device)
    db.commit()
    return {"ok": True}
''')

write_file('backend/app/api/endpoints/__init__.py', '''
from fastapi import APIRouter
from app.api.endpoints.health import router as health_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.devices import router as devices_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(devices_router, prefix="/devices", tags=["devices"])
''')

print("Phase 5 generated successfully")
