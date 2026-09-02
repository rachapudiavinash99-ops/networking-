import os

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

write_file('docker-compose.yml', '''
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: netguardian
      POSTGRES_PASSWORD: strongpassword123
      POSTGRES_DB: netguardian_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U netguardian"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://netguardian:strongpassword123@db/netguardian_db
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
      - JWT_SECRET=supersecretjwtkey_replace_in_production
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.core.celery_app worker --loglevel=info
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://netguardian:strongpassword123@db/netguardian_db
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - redis
      - db

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  postgres_data:
''')

write_file('backend/Dockerfile', '''
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y iputils-ping dnsutils nmap && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
''')

write_file('frontend/Dockerfile', '''
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
''')

write_file('.env.example', '''
DATABASE_URL=postgresql://netguardian:strongpassword123@localhost/netguardian_db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=supersecretjwtkey_replace_in_production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
MONITORING_INTERVAL=60
LOG_LEVEL=INFO
''')

write_file('backend/requirements.txt', '''
fastapi==0.110.0
uvicorn==0.29.0
sqlalchemy==2.0.29
psycopg2-binary==2.9.9
alembic==1.13.1
pydantic==2.6.4
pydantic-settings==2.2.1
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.9
celery==5.3.6
redis==5.0.3
requests==2.31.0
websockets==12.0
pytest==8.1.1
httpx==0.27.0
''')

print("Phase 2 generated successfully")
