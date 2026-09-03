# NetGuardian - Network Monitoring Platform

## Dependencies
- Python 3.12+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose

## Installation
First, clone the repository and navigate to the directory:
```bash
git clone https://github.com/rachapudiavinash99-ops/networking-.git
cd networking-
```

## Build
To build the application using Docker:
```bash
docker-compose build
```
For local frontend build:
```bash
cd frontend
npm install
npm run build
```

## Run
To run the full stack via Docker Compose:
```bash
docker-compose up -d
`````
The application will be available at http://localhost:3000

## Usage
- Open http://localhost:3000 in your browser
- Register a new account or log in
- Navigate to the Dashboard to view network status
- Add devices and configure monitoring tasks
