FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y iputils-ping dnsutils nmap && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
