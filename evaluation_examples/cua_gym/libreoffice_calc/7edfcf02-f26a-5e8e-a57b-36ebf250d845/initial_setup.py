"""
Initial Setup: Create workspace for Kubernetes Secret YAML task
Task ID: vscode_ops_089
Domain: libreoffice_calc (VSCode ops)
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_089'
K8S_DIR = f'{WORKDIR}/k8s'

# VSCode config paths
HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_initial():
    # 1. Create the k8s workspace directory
    os.makedirs(K8S_DIR, exist_ok=True)
    print(f'Created workspace directory: {K8S_DIR}')

    # 2. Add some existing k8s files so workspace is not empty (realistic)
    # A deployment.yaml to give context
    deployment_content = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-api
  namespace: production
  labels:
    app: backend-api
    tier: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend-api
  template:
    metadata:
      labels:
        app: backend-api
        tier: backend
    spec:
      containers:
      - name: backend-api
        image: registry.internal.io/backend-api:v2.4.1
        ports:
        - containerPort: 8080
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: DB_HOST
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: DB_USER
        - name: DB_PASS
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: DB_PASS
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
"""
    with open(os.path.join(K8S_DIR, 'deployment.yaml'), 'w') as f:
        f.write(deployment_content)
    print('Created deployment.yaml')

    # A service.yaml
    service_content = """apiVersion: v1
kind: Service
metadata:
  name: backend-api-svc
  namespace: production
spec:
  selector:
    app: backend-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
"""
    with open(os.path.join(K8S_DIR, 'service.yaml'), 'w') as f:
        f.write(service_content)
    print('Created service.yaml')

    # A namespace.yaml
    namespace_content = """apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    team: platform-engineering
"""
    with open(os.path.join(K8S_DIR, 'namespace.yaml'), 'w') as f:
        f.write(namespace_content)
    print('Created namespace.yaml')

    # NO secret.yaml - that is what the agent must create

    # 3. Configure VSCode with YAML extension settings
    update_settings({
        "yaml.schemas": {
            "kubernetes": "*.yaml"
        },
        "editor.tabSize": 2,
        "editor.insertSpaces": True,
        "files.associations": {
            "*.yaml": "yaml",
            "*.yml": "yaml"
        },
        "[yaml]": {
            "editor.autoIndent": "keep",
            "editor.tabSize": 2
        }
    })
    print('Configured VSCode YAML settings')

    # 4. Install YAML extension (best effort)
    try:
        subprocess.run(
            ["code", "--install-extension", "redhat.vscode-yaml", "--force"],
            capture_output=True, text=True, timeout=30
        )
        print('Installed YAML extension')
    except Exception as e:
        print(f'YAML extension install skipped: {e}')

    # 5. Launch VSCode with the k8s workspace
    launch_gui(f'code "{K8S_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with /home/user/k8s workspace on DISPLAY=:0')


create_initial()
