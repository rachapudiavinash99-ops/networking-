import os

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

write_file('backend/app/main.py', '''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import api_router

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
''')

write_file('backend/app/core/config.py', '''
from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://netguardian:strongpassword123@localhost/netguardian_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    JWT_SECRET: str = "supersecretjwtkey_replace_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000", "http://localhost:5173"]
    MONITORING_INTERVAL: int = 60
    
    class Config:
        env_file = ".env"

settings = Settings()
''')

write_file('backend/app/db/session.py', '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''')

write_file('backend/app/db/base.py', '''
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
''')

write_file('backend/alembic.ini', '''
[alembic]
script_location = alembic
sqlalchemy.url = postgresql://netguardian:strongpassword123@localhost/netguardian_db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
''')

write_file('backend/app/api/endpoints/__init__.py', '''
from fastapi import APIRouter
from app.api.endpoints.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
''')

write_file('backend/app/api/endpoints/health.py', '''
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def check_health():
    return {"status": "ok", "service": "NetGuardian API"}
''')

print("Phase 3 generated successfully")
