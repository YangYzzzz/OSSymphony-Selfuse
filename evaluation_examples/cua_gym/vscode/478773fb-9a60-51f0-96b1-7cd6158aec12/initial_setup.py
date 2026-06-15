"""
Initial Setup: Create k8s workspace with YAML extension configured, no ingress.yaml
Task ID: vscode_ops_080
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_080'
K8S_DIR = f'{WORKDIR}/k8s'

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

    # 2. Create some existing k8s resource files to make the workspace realistic
    # A deployment file
    deployment_yaml = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-service
  namespace: default
  labels:
    app: web-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-service
  template:
    metadata:
      labels:
        app: web-service
    spec:
      containers:
      - name: web
        image: nginx:1.25-alpine
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "250m"
            memory: "256Mi"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 15
"""
    with open(os.path.join(K8S_DIR, 'deployment.yaml'), 'w') as f:
        f.write(deployment_yaml)

    # A service file
    service_yaml = """apiVersion: v1
kind: Service
metadata:
  name: web-service
  namespace: default
  labels:
    app: web-service
spec:
  type: ClusterIP
  selector:
    app: web-service
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
"""
    with open(os.path.join(K8S_DIR, 'service.yaml'), 'w') as f:
        f.write(service_yaml)

    # A namespace file
    namespace_yaml = """apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
"""
    with open(os.path.join(K8S_DIR, 'namespace.yaml'), 'w') as f:
        f.write(namespace_yaml)

    # A configmap file
    configmap_yaml = """apiVersion: v1
kind: ConfigMap
metadata:
  name: web-config
  namespace: default
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"
  APP_NAME: "web-service"
"""
    with open(os.path.join(K8S_DIR, 'configmap.yaml'), 'w') as f:
        f.write(configmap_yaml)

    # A TLS secret placeholder (cert not real, just structure)
    secret_yaml = """apiVersion: v1
kind: Secret
metadata:
  name: app-tls-cert
  namespace: default
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTi...
  tls.key: LS0tLS1CRUdJTi...
"""
    with open(os.path.join(K8S_DIR, 'tls-secret.yaml'), 'w') as f:
        f.write(secret_yaml)

    # Make sure ingress.yaml does NOT exist
    ingress_path = os.path.join(K8S_DIR, 'ingress.yaml')
    if os.path.exists(ingress_path):
        os.remove(ingress_path)

    print(f'K8s workspace created at: {K8S_DIR}')
    print(f'Files: {os.listdir(K8S_DIR)}')

    # 3. Configure VSCode settings for YAML/Kubernetes
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
            "editor.tabSize": 2,
            "editor.insertSpaces": True,
            "editor.autoIndent": "keep"
        }
    })
    print('VSCode settings configured for YAML/Kubernetes')

    # 4. Launch VSCode with the k8s workspace
    launch_gui(f'code "{K8S_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with k8s workspace on DISPLAY=:0')


create_initial()
