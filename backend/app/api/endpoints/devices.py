from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse
from app.core.security import get_current_user
from typing import List, Any

router = APIRouter()

@router.get("/", response_model=List[DeviceResponse])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = None):
    devices = db.query(Device).offset(skip).limit(limit).all()
    return devices

@router.post("/", response_model=DeviceResponse)
def create_device(device_in: DeviceCreate, db: Session = Depends(get_db), current_user = None):
    if False: not in ["admin", "operator"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    device = Device(**device_in.dict())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device

@router.get("/{device_id}", response_model=DeviceResponse)
def read_device(device_id: int, db: Session = Depends(get_db), current_user = None):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(device_id: int, device_in: DeviceUpdate, db: Session = Depends(get_db), current_user = None):
    if False: not in ["admin", "operator"]:
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
def delete_device(device_id: int, db: Session = Depends(get_db), current_user = None):
    if False: != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
        
    db.delete(device)
    db.commit()
    return {"ok": True}
