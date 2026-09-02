from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import api_router

from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.models.device import Device
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NetGuardian API",
    description="Network Monitoring, Diagnostics & Management Platform API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}
