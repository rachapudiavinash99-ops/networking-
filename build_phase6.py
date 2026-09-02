import os

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

write_file('backend/app/core/celery_app.py', '''
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.monitor_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "run-monitoring-every-minute": {
            "task": "app.tasks.monitor_tasks.run_all_monitoring",
            "schedule": 60.0,
        },
    }
)
''')

write_file('backend/app/tasks/monitor_tasks.py', '''
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
''')

print("Phase 6 generated successfully")
