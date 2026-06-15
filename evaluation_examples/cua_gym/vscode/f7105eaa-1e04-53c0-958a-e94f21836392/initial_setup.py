"""
Initial Setup: Configure YAML schema validation in VSCode workspace
Task ID: vscode_ops_050
Domain: vscode

Creates /home/user/infra workspace with docker-compose and k8s YAML files.
VSCode YAML extension installed but no .vscode/settings.json configured.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_050'
WORKSPACE = f'{WORKDIR}/infra'


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
    # Create workspace directory structure
    os.makedirs(WORKSPACE, exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE, 'k8s'), exist_ok=True)

    # Ensure NO .vscode/settings.json exists (task is to create it)
    vscode_dir = os.path.join(WORKSPACE, '.vscode')
    settings_path = os.path.join(vscode_dir, 'settings.json')
    if os.path.exists(settings_path):
        os.remove(settings_path)

    # --- docker-compose.yml ---
    docker_compose_content = """\
version: "3.8"

services:
  web:
    image: nginx:1.25-alpine
    container_name: infra-web
    ports:
      - "8080:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - static_assets:/usr/share/nginx/html
    depends_on:
      - api
      - redis
    networks:
      - frontend
      - backend
    restart: unless-stopped

  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: infra-api
    environment:
      DATABASE_URL: postgres://appuser:s3cret@db:5432/infradb
      REDIS_URL: redis://redis:6379/0
      LOG_LEVEL: info
      JWT_SECRET: change-me-in-production
    ports:
      - "3000:3000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - backend
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    container_name: infra-db
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: s3cret
      POSTGRES_DB: infradb
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d infradb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: infra-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - backend
    restart: unless-stopped

volumes:
  pgdata:
  redis_data:
  static_assets:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
"""
    with open(os.path.join(WORKSPACE, 'docker-compose.yml'), 'w') as f:
        f.write(docker_compose_content)

    # --- k8s/deployment.yaml ---
    k8s_deployment = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
  namespace: production
  labels:
    app: infra-api
    tier: backend
    version: v1.4.2
spec:
  replicas: 3
  selector:
    matchLabels:
      app: infra-api
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: infra-api
        tier: backend
    spec:
      containers:
        - name: api
          image: registry.internal.io/infra/api:1.4.2
          ports:
            - containerPort: 3000
              protocol: TCP
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: connection-string
            - name: LOG_LEVEL
              value: "info"
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 15
      restartPolicy: Always
"""
    with open(os.path.join(WORKSPACE, 'k8s', 'deployment.yaml'), 'w') as f:
        f.write(k8s_deployment)

    # --- k8s/service.yaml ---
    k8s_service = """\
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: production
  labels:
    app: infra-api
spec:
  type: ClusterIP
  selector:
    app: infra-api
  ports:
    - name: http
      port: 80
      targetPort: 3000
      protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  name: api-nodeport
  namespace: production
  labels:
    app: infra-api
spec:
  type: NodePort
  selector:
    app: infra-api
  ports:
    - name: http
      port: 80
      targetPort: 3000
      nodePort: 30080
      protocol: TCP
"""
    with open(os.path.join(WORKSPACE, 'k8s', 'service.yaml'), 'w') as f:
        f.write(k8s_service)

    print(f'Workspace created at: {WORKSPACE}')
    print(f'  docker-compose.yml')
    print(f'  k8s/deployment.yaml')
    print(f'  k8s/service.yaml')
    print(f'  .vscode/settings.json does NOT exist (task target)')

    # Install YAML extension if not already installed
    try:
        result = subprocess.run(['code', '--list-extensions'], capture_output=True, text=True, timeout=15)
        if 'redhat.vscode-yaml' not in result.stdout.lower():
            subprocess.run(['code', '--install-extension', 'redhat.vscode-yaml'], timeout=60)
            print('Installed redhat.vscode-yaml extension')
        else:
            print('YAML extension already installed')
    except Exception as e:
        print(f'Extension check/install note: {e}')

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with /home/user/infra workspace')


create_initial()
