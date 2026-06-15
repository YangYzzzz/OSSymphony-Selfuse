"""
Initial Setup: Multi-stage Docker Compose deployment workflow
Task ID: vscode_gf3_063
Domain: vscode

Creates the project directory with a basic Dockerfile and source files
so the agent has a realistic workspace to work with. Does NOT create
docker-compose.yml, docker-compose.override.yml, or .vscode/tasks.json.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_063'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'


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
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/nginx', exist_ok=True)

    # Create a realistic Dockerfile for the webapp
    dockerfile_content = """\
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY src/ ./src/
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
EXPOSE 3000
CMD ["node", "dist/server.js"]
"""
    with open(f'{PROJECT_DIR}/Dockerfile', 'w') as f:
        f.write(dockerfile_content)

    # Create a basic package.json
    package_json = """\
{
  "name": "webapp",
  "version": "2.4.1",
  "description": "Production web application with API and frontend",
  "main": "dist/server.js",
  "scripts": {
    "start": "node dist/server.js",
    "dev": "nodemon src/server.js",
    "build": "tsc -p tsconfig.json",
    "test": "jest --coverage",
    "lint": "eslint src/"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "helmet": "^7.1.0",
    "morgan": "^1.10.0",
    "pg": "^8.11.3",
    "redis": "^4.6.10"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "nodemon": "^3.0.2",
    "jest": "^29.7.0",
    "@types/express": "^4.17.21"
  }
}
"""
    with open(f'{PROJECT_DIR}/package.json', 'w') as f:
        f.write(package_json)

    # Create a basic server source file
    server_js = """\
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.get('/api/v1/status', (req, res) => {
  res.json({
    service: 'webapp',
    version: '2.4.1',
    environment: process.env.NODE_ENV || 'development',
    uptime: process.uptime()
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
"""
    with open(f'{PROJECT_DIR}/src/server.js', 'w') as f:
        f.write(server_js)

    # Create nginx config for reference
    nginx_conf = """\
server {
    listen 80;
    server_name webapp.example.com;

    location / {
        proxy_pass http://webapp:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
    with open(f'{PROJECT_DIR}/nginx/default.conf', 'w') as f:
        f.write(nginx_conf)

    # Create a .env.example for reference
    env_example = """\
# Database
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=webapp_prod
POSTGRES_USER=webapp
POSTGRES_PASSWORD=changeme

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Application
NODE_ENV=production
PORT=3000
LOG_LEVEL=info
"""
    with open(f'{PROJECT_DIR}/.env.example', 'w') as f:
        f.write(env_example)

    print(f'Initial project structure created at: {PROJECT_DIR}')

    # Open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
