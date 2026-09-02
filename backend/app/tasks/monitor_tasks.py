from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.device import Device
import logging
import time

logger = logging.getLogger(__name__)

@celery_app.task
def check_device_health(device_id: int, ip_address: str):
    # Dummy placeholder for ping logic
    logger.info(f"Checking health for {ip_address}")
    db = SessionLocal()
    try:
        device = db.query(Device).filter(Device.id == device_id).first()
        if device:
            # Simulate a network check
            device.status = "ONLINE"
            device.latency = 5.2
            db.commit()
    finally:
        db.close()
    return {"status": "ONLINE", "ip": ip_address}

@celery_app.task
def run_all_monitoring():
    logger.info("Starting global monitoring run")
    db = SessionLocal()
    try:
        devices = db.query(Device).filter(Device.is_monitored == True).all()
        for device in devices:
            check_device_health.delay(device.id, device.ip_address)
    finally:
        db.close()
