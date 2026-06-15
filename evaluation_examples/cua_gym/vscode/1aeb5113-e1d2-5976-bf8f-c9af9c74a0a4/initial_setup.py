"""
Initial Setup: Create microservices project directory with API service scaffold
Task ID: vscode_gf3_051
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_051'
PROJECT_DIR = f'{WORKDIR}/projects/microservices'
API_DIR = f'{PROJECT_DIR}/api'

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
    # Create directory structure
    os.makedirs(API_DIR, exist_ok=True)

    # --- api/Dockerfile ---
    with open(f'{API_DIR}/Dockerfile', 'w') as f:
        f.write("""FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
""")

    # --- api/package.json ---
    with open(f'{API_DIR}/package.json', 'w') as f:
        f.write("""{
  "name": "microservices-api",
  "version": "1.0.0",
  "description": "REST API for microservices platform",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "jest --coverage"
  },
  "dependencies": {
    "express": "^4.18.2",
    "ioredis": "^5.3.2",
    "pg": "^8.11.3",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.2",
    "jest": "^29.7.0"
  }
}
""")

    # --- api/server.js ---
    with open(f'{API_DIR}/server.js', 'w') as f:
        f.write("""const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');
const Redis = require('ioredis');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// PostgreSQL connection
const pool = new Pool({
  host: process.env.POSTGRES_HOST || 'localhost',
  port: process.env.POSTGRES_PORT || 5432,
  user: process.env.POSTGRES_USER || 'devuser',
  password: process.env.POSTGRES_PASSWORD || 'devpassword',
  database: process.env.POSTGRES_DB || 'appdb',
});

// Redis connection
const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: process.env.REDIS_PORT || 6379,
});

app.get('/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    await redis.ping();
    res.json({ status: 'healthy', services: { postgres: 'connected', redis: 'connected' } });
  } catch (err) {
    res.status(503).json({ status: 'unhealthy', error: err.message });
  }
});

app.get('/api/products', async (req, res) => {
  const cacheKey = 'products:all';
  const cached = await redis.get(cacheKey);
  if (cached) {
    return res.json(JSON.parse(cached));
  }
  const result = await pool.query('SELECT * FROM products ORDER BY created_at DESC');
  await redis.setex(cacheKey, 300, JSON.stringify(result.rows));
  res.json(result.rows);
});

app.listen(port, () => {
  console.log(`API server running on port ${port}`);
});
""")

    # --- api/.env.example ---
    with open(f'{API_DIR}/.env.example', 'w') as f:
        f.write("""POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=devuser
POSTGRES_PASSWORD=devpassword
POSTGRES_DB=appdb
REDIS_HOST=redis
REDIS_PORT=6379
PORT=3000
""")

    # --- Production docker-compose.yml (for context, NOT the dev file) ---
    with open(f'{PROJECT_DIR}/docker-compose.yml', 'w') as f:
        f.write("""version: "3.8"

services:
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - POSTGRES_HOST=postgres
      - REDIS_HOST=redis
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: produser
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: appdb
    volumes:
      - pg_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  pg_data:
""")

    # --- README.md for context ---
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# Microservices Platform

A containerized microservices architecture with a Node.js API backed by PostgreSQL and Redis.

## Project Structure

```
microservices/
├── api/                    # REST API service
│   ├── Dockerfile
│   ├── package.json
│   ├── server.js
│   └── .env.example
├── docker-compose.yml      # Production configuration
└── README.md
```

## Getting Started

### Production
```bash
docker-compose up -d
```

### Development
Create a `docker-compose.dev.yml` for local development with hot-reload,
database admin tools, and exposed ports for debugging.
""")

    print(f'Initial project structure created at: {PROJECT_DIR}')

    # Open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
