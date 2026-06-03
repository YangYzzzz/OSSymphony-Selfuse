"""
Initial Setup: Create workspace with docker-compose files containing ':latest' image tags
Task ID: vscode_ops_059
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_059'
WORKSPACE = f'{WORKDIR}/workspace'

def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)

def create_initial():
    os.makedirs(WORKSPACE, exist_ok=True)

    # --- docker-compose.yml (main) ---
    docker_compose_main = """\
version: '3.8'

services:
  web:
    image: myregistry/web-frontend:latest
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - API_URL=http://api:8080
    depends_on:
      - api
      - redis
    networks:
      - app-network
    restart: unless-stopped

  api:
    image: myregistry/api-server:latest
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://dbuser:dbpass@postgres:5432/appdb
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=supersecretkey
    depends_on:
      - postgres
      - redis
    networks:
      - app-network
    restart: unless-stopped

  postgres:
    image: postgres:latest
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=dbuser
      - POSTGRES_PASSWORD=dbpass
    networks:
      - app-network
    restart: unless-stopped

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    networks:
      - app-network
    restart: unless-stopped

  nginx:
    image: myregistry/nginx-proxy:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./certs:/etc/nginx/certs
    depends_on:
      - web
      - api
    networks:
      - app-network
    restart: unless-stopped

volumes:
  pgdata:

networks:
  app-network:
    driver: bridge
"""

    # --- docker-compose.staging.yml ---
    docker_compose_staging = """\
version: '3.8'

services:
  web:
    image: myregistry/web-frontend:latest
    ports:
      - "3001:3000"
    environment:
      - NODE_ENV=staging
      - API_URL=http://api:8080
      - DEBUG=true
    depends_on:
      - api

  api:
    image: myregistry/api-server:latest
    ports:
      - "8081:8080"
    environment:
      - DATABASE_URL=postgres://dbuser:stagingpass@postgres:5432/staging_db
      - REDIS_URL=redis://redis:6379
      - LOG_LEVEL=debug
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:latest
    environment:
      - POSTGRES_DB=staging_db
      - POSTGRES_USER=dbuser
      - POSTGRES_PASSWORD=stagingpass

  redis:
    image: redis:latest

  worker:
    image: myregistry/task-worker:latest
    environment:
      - QUEUE_NAME=staging-jobs
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
"""

    # --- docker-compose.prod.yml ---
    docker_compose_prod = """\
version: '3.8'

services:
  web:
    image: myregistry/web-frontend:latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - API_URL=http://api:8080

  api:
    image: myregistry/api-server:latest
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1.0'
          memory: 1024M
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://produser:prodpass@postgres:5432/prod_db
      - REDIS_URL=redis://redis:6379

  postgres:
    image: postgres:latest
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2048M
    volumes:
      - prod-pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=prod_db
      - POSTGRES_USER=produser
      - POSTGRES_PASSWORD=prodpass

  redis:
    image: redis:latest
    deploy:
      resources:
        limits:
          memory: 256M

  nginx:
    image: myregistry/nginx-proxy:latest
    ports:
      - "80:80"
      - "443:443"

  monitoring:
    image: myregistry/metrics-collector:latest
    ports:
      - "9090:9090"
    environment:
      - SCRAPE_INTERVAL=15s

volumes:
  prod-pgdata:
"""

    # --- Other files that should NOT be modified ---
    dockerfile_content = """\
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

EXPOSE 3000
CMD ["node", "server.js"]
"""

    readme_content = """\
# Microservices Platform

## Overview
This project contains the Docker Compose configurations for our
microservices deployment platform.

## Environments
- **Development**: `docker-compose.yml`
- **Staging**: `docker-compose.staging.yml`
- **Production**: `docker-compose.prod.yml`

## Services
- **web**: React frontend application
- **api**: Node.js REST API server
- **postgres**: PostgreSQL database
- **redis**: Redis cache and message broker
- **nginx**: Reverse proxy and load balancer
- **worker**: Background task processor
- **monitoring**: Metrics collection service

## Getting Started
```bash
docker-compose up -d
```
"""

    env_content = """\
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=appdb
DB_USER=dbuser
DB_PASSWORD=dbpass

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Application Settings
APP_PORT=3000
API_PORT=8080
NODE_ENV=development
"""

    # Write all files
    files = {
        'docker-compose.yml': docker_compose_main,
        'docker-compose.staging.yml': docker_compose_staging,
        'docker-compose.prod.yml': docker_compose_prod,
        'Dockerfile': dockerfile_content,
        'README.md': readme_content,
        '.env': env_content,
    }

    for filename, content in files.items():
        filepath = os.path.join(WORKSPACE, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Created: {filepath}')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
