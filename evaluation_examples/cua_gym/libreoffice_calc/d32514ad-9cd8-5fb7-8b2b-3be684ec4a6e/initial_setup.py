"""
Initial Setup: Create docker-compose project workspace for VSCode
Task ID: vscode_ops_085
Domain: vscode_ops (OS/VSCode)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_085'
PROJECT_DIR = f'{WORKDIR}/project'

DOCKER_COMPOSE_YML = """\
version: "3.8"

services:
  backend:
    image: node:18-alpine
    container_name: myapp-backend
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://dbuser:dbpass@db:5432/myapp
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    networks:
      - app-network
    restart: unless-stopped

  frontend:
    image: node:18-alpine
    container_name: myapp-frontend
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "8080:80"
    environment:
      - REACT_APP_API_URL=http://backend:3000
    depends_on:
      - backend
    networks:
      - app-network
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: myapp-db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=dbuser
      - POSTGRES_PASSWORD=dbpass
      - POSTGRES_DB=myapp
    ports:
      - "5432:5432"
    networks:
      - app-network
    restart: unless-stopped

  cache:
    image: redis:7-alpine
    container_name: myapp-cache
    ports:
      - "6379:6379"
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
"""

# Backend service source files
BACKEND_INDEX_JS = """\
const express = require('express');
const { Pool } = require('pg');
const redis = require('redis');

const app = express();
const port = process.env.PORT || 3000;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

const redisClient = redis.createClient({
  url: process.env.REDIS_URL,
});

app.use(express.json());

app.get('/api/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ status: 'healthy', environment: process.env.NODE_ENV });
  } catch (err) {
    res.status(500).json({ status: 'unhealthy', error: err.message });
  }
});

app.get('/api/users', async (req, res) => {
  const cached = await redisClient.get('users');
  if (cached) {
    return res.json(JSON.parse(cached));
  }
  const result = await pool.query('SELECT * FROM users ORDER BY created_at DESC');
  await redisClient.setEx('users', 300, JSON.stringify(result.rows));
  res.json(result.rows);
});

app.post('/api/users', async (req, res) => {
  const { name, email, role } = req.body;
  const result = await pool.query(
    'INSERT INTO users (name, email, role) VALUES ($1, $2, $3) RETURNING *',
    [name, email, role]
  );
  await redisClient.del('users');
  res.status(201).json(result.rows[0]);
});

app.listen(port, () => {
  console.log(`Backend server running on port ${port}`);
});
"""

BACKEND_PACKAGE_JSON = """\
{
  "name": "myapp-backend",
  "version": "1.0.0",
  "description": "MyApp backend service",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon --inspect=0.0.0.0:9229 index.js",
    "test": "jest --coverage"
  },
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.3",
    "redis": "^4.6.10"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "nodemon": "^3.0.2"
  }
}
"""

BACKEND_DOCKERFILE = """\
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
"""

FRONTEND_DOCKERFILE = """\
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""

FRONTEND_PACKAGE_JSON = """\
{
  "name": "myapp-frontend",
  "version": "1.0.0",
  "description": "MyApp frontend application",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "axios": "^1.6.2"
  }
}
"""

README_MD = """\
# MyApp - Full Stack Application

A containerized full-stack application with Node.js backend, React frontend,
PostgreSQL database, and Redis caching.

## Services

| Service  | Port | Description            |
|----------|------|------------------------|
| backend  | 3000 | Express.js API server  |
| frontend | 8080 | React SPA (via Nginx)  |
| db       | 5432 | PostgreSQL 15          |
| cache    | 6379 | Redis 7                |

## Getting Started

```bash
docker-compose up -d
```

## Development

For local development with hot-reload and debugging:

```bash
docker-compose -f docker-compose.yml -f docker-compose.override.yml up
```
"""


def create_initial():
    # Create project directory structure
    os.makedirs(f'{PROJECT_DIR}/backend', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/frontend', exist_ok=True)

    # Write docker-compose.yml
    with open(f'{PROJECT_DIR}/docker-compose.yml', 'w') as f:
        f.write(DOCKER_COMPOSE_YML)

    # Write backend files
    with open(f'{PROJECT_DIR}/backend/index.js', 'w') as f:
        f.write(BACKEND_INDEX_JS)

    with open(f'{PROJECT_DIR}/backend/package.json', 'w') as f:
        f.write(BACKEND_PACKAGE_JSON)

    with open(f'{PROJECT_DIR}/backend/Dockerfile', 'w') as f:
        f.write(BACKEND_DOCKERFILE)

    # Write frontend files
    with open(f'{PROJECT_DIR}/frontend/Dockerfile', 'w') as f:
        f.write(FRONTEND_DOCKERFILE)

    with open(f'{PROJECT_DIR}/frontend/package.json', 'w') as f:
        f.write(FRONTEND_PACKAGE_JSON)

    # Write README
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(README_MD)

    print(f'Project workspace created at: {PROJECT_DIR}')
    print(f'docker-compose.yml created at: {PROJECT_DIR}/docker-compose.yml')
    print(f'NO docker-compose.override.yml exists (task requires agent to create it)')


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


create_initial()

# Open VSCode with the project workspace
launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
print('GUI_READY: launched VSCode with DISPLAY=:0')
