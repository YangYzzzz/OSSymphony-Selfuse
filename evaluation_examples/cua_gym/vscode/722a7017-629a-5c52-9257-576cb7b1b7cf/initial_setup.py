"""
Initial Setup: Write a Kubernetes ConfigMap YAML file with nginx.conf multi-line string
Task ID: vscode_ops_062
Domain: vscode

Creates /home/user/k8s/ workspace directory with some existing K8s manifests
(but NO configmap.yaml). Configures VSCode YAML extension settings.
Opens VSCode on the workspace.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_062'
K8S_DIR = f'{WORKDIR}/k8s'

VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    # Create the k8s workspace directory
    os.makedirs(K8S_DIR, exist_ok=True)

    # Create some existing K8s manifests to make the workspace realistic
    # 1. A deployment manifest
    deployment_yaml = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25.3
        ports:
        - containerPort: 80
        volumeMounts:
        - name: config-volume
          mountPath: /etc/nginx/nginx.conf
          subPath: nginx.conf
      volumes:
      - name: config-volume
        configMap:
          name: nginx-config
"""
    with open(os.path.join(K8S_DIR, 'deployment.yaml'), 'w') as f:
        f.write(deployment_yaml)

    # 2. A service manifest
    service_yaml = """apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  labels:
    app: nginx
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
  selector:
    app: nginx
"""
    with open(os.path.join(K8S_DIR, 'service.yaml'), 'w') as f:
        f.write(service_yaml)

    # 3. A namespace manifest
    namespace_yaml = """apiVersion: v1
kind: Namespace
metadata:
  name: web-platform
  labels:
    environment: production
    team: platform-engineering
"""
    with open(os.path.join(K8S_DIR, 'namespace.yaml'), 'w') as f:
        f.write(namespace_yaml)

    # Do NOT create configmap.yaml - that is the task for the agent

    print(f'Workspace created: {K8S_DIR}')
    print(f'Files: deployment.yaml, service.yaml, namespace.yaml')
    print(f'configmap.yaml does NOT exist (task target)')

    # Configure VSCode settings for YAML support
    update_settings({
        "yaml.validate": True,
        "yaml.format.enable": True,
        "editor.tabSize": 2,
        "files.associations": {
            "*.yaml": "yaml",
            "*.yml": "yaml"
        },
        "[yaml]": {
            "editor.insertSpaces": True,
            "editor.tabSize": 2,
            "editor.autoIndent": "keep"
        }
    })
    print(f'VSCode YAML settings configured at {SETTINGS_PATH}')

    # Open VSCode on the k8s workspace
    launch_gui(f'code "{K8S_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
