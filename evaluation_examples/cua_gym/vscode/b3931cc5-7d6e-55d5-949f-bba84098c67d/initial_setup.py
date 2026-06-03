"""
Initial Setup: Create Kubernetes workspace with web-app deployment for HPA task
Task ID: vscode_ops_074
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_074'
K8S_DIR = f'{WORKDIR}/k8s'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'


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
    # --- Create k8s directory ---
    os.makedirs(K8S_DIR, exist_ok=True)

    # --- Create deployment.yaml (the existing web-app deployment) ---
    deployment_yaml = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: default
  labels:
    app: web-app
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
        tier: frontend
    spec:
      containers:
      - name: web-app
        image: nginx:1.25-alpine
        ports:
        - containerPort: 80
          name: http
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "256Mi"
        readinessProbe:
          httpGet:
            path: /healthz
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /healthz
            port: 80
          initialDelaySeconds: 15
          periodSeconds: 20
"""
    with open(f'{K8S_DIR}/deployment.yaml', 'w') as f:
        f.write(deployment_yaml)

    # --- Create service.yaml (companion service for the deployment) ---
    service_yaml = """\
apiVersion: v1
kind: Service
metadata:
  name: web-app-svc
  namespace: default
  labels:
    app: web-app
spec:
  type: ClusterIP
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
"""
    with open(f'{K8S_DIR}/service.yaml', 'w') as f:
        f.write(service_yaml)

    # --- Create namespace.yaml ---
    namespace_yaml = """\
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    team: platform-engineering
"""
    with open(f'{K8S_DIR}/namespace.yaml', 'w') as f:
        f.write(namespace_yaml)

    # --- Create configmap.yaml ---
    configmap_yaml = """\
apiVersion: v1
kind: ConfigMap
metadata:
  name: web-app-config
  namespace: default
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"
  CACHE_TTL: "3600"
"""
    with open(f'{K8S_DIR}/configmap.yaml', 'w') as f:
        f.write(configmap_yaml)

    # --- Configure VSCode settings with YAML/Kubernetes schema support ---
    os.makedirs(VSCODE_USER, exist_ok=True)
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    settings.update({
        "yaml.schemas": {
            "kubernetes": "*.yaml"
        },
        "editor.tabSize": 2,
        "editor.insertSpaces": True,
        "files.associations": {
            "*.yaml": "yaml",
            "*.yml": "yaml"
        },
        "yaml.format.enable": True,
        "editor.fontSize": 14,
        "workbench.colorTheme": "Visual Studio Dark"
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Initial k8s workspace created at: {K8S_DIR}')
    print(f'Files: deployment.yaml, service.yaml, namespace.yaml, configmap.yaml')
    print(f'VSCode settings configured with YAML/Kubernetes schema')

    # --- GUI-ready startup: open VSCode with the k8s workspace ---
    launch_gui(f'code "{K8S_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
