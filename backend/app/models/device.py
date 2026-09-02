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
