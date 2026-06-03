"""
Initial Setup: Configure YAML extension Kubernetes schema association
Task ID: vscode_ops_016
Domain: vscode (settings configuration)

Creates:
- Empty VSCode settings.json (no yaml.schemas)
- A realistic k8s-deployment.yaml file
- Installs Red Hat YAML extension
- Opens VSCode with the yaml file
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_016'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
YAML_FILE = os.path.join(WORKDIR, 'k8s-deployment.yaml')


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
    # 1. Ensure VSCode user config directory exists
    os.makedirs(VSCODE_USER, exist_ok=True)

    # 2. Write empty settings.json (no yaml.schemas)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump({}, f, indent=4)
    print(f'Settings file created: {SETTINGS_PATH}')

    # 3. Create a realistic Kubernetes deployment YAML file
    k8s_content = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-api
  namespace: production
  labels:
    app: ecommerce-api
    tier: backend
    version: v2.4.1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ecommerce-api
      tier: backend
  template:
    metadata:
      labels:
        app: ecommerce-api
        tier: backend
        version: v2.4.1
    spec:
      containers:
        - name: api-server
          image: registry.internal.acme.io/ecommerce-api:2.4.1
          ports:
            - containerPort: 8080
              protocol: TCP
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: connection-string
            - name: REDIS_HOST
              value: "redis-cluster.production.svc.cluster.local"
            - name: LOG_LEVEL
              value: "info"
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
      imagePullSecrets:
        - name: registry-credentials
"""
    with open(YAML_FILE, 'w') as f:
        f.write(k8s_content)
    print(f'Kubernetes YAML file created: {YAML_FILE}')

    # 4. Install Red Hat YAML extension if not already installed
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=30
        )
        if 'redhat.vscode-yaml' not in result.stdout.lower():
            subprocess.run(
                ['code', '--install-extension', 'redhat.vscode-yaml', '--force'],
                capture_output=True, text=True, timeout=120
            )
            print('Installed redhat.vscode-yaml extension')
        else:
            print('redhat.vscode-yaml extension already installed')
    except Exception as e:
        print(f'Extension install note: {e}')

    # 5. Launch VSCode with the YAML file open
    launch_gui(f'code "{YAML_FILE}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with k8s-deployment.yaml on DISPLAY=:0')


create_initial()
