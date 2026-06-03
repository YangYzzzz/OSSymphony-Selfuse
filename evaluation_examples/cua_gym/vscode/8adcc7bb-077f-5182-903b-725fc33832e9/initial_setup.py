"""
Initial Setup: Create a Kubernetes deployment.yaml with 5 YAML validation errors
Task ID: vscode_ops_090
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_090'
WORKSPACE_DIR = f'{WORKDIR}/k8s-project'
OUTPUT = f'{WORKSPACE_DIR}/deployment.yaml'

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


def create_initial():
    # Create workspace directory
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # ----- Create deployment.yaml with 5 intentional errors -----
    # Error 1: wrong apiVersion format ("apps/v1beta1" instead of "apps/v1")
    # Error 2: missing 'spec' under template (template has containers directly)
    # Error 3: incorrect indentation in containers section (indented too far)
    # Error 4: missing container name field
    # Error 5: invalid port format (string "eighty" instead of integer 80)
    broken_yaml = """\
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: webapp-deployment
  labels:
    app: webapp
    environment: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
        version: "1.2.0"
    containers:
            - image: nginx:1.25.3
              ports:
                - containerPort: "eighty"
              resources:
                limits:
                  cpu: "500m"
                  memory: "256Mi"
                requests:
                  cpu: "250m"
                  memory: "128Mi"
              env:
                - name: APP_ENV
                  value: "production"
                - name: LOG_LEVEL
                  value: "info"
              volumeMounts:
                - name: config-volume
                  mountPath: /etc/config
"""

    with open(OUTPUT, 'w') as f:
        f.write(broken_yaml)
    print(f'Initial file created: {OUTPUT}')

    # ----- Configure VSCode settings for YAML + Kubernetes validation -----
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)

    # Load existing settings or start fresh
    try:
        with open(SETTINGS_PATH, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Configure YAML extension and Kubernetes schema validation
    settings.update({
        "yaml.validate": True,
        "yaml.schemas": {
            "kubernetes": "deployment.yaml"
        },
        "yaml.schemaStore.enable": True,
        "editor.fontSize": 14,
        "editor.minimap.enabled": False,
        "workbench.colorTheme": "Default Dark Modern"
    })

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings configured at: {SETTINGS_PATH}')

    # ----- Install YAML extension -----
    try:
        subprocess.run(['code', '--install-extension', 'redhat.vscode-yaml', '--force'],
                       capture_output=True, text=True, timeout=60)
        print('YAML extension installed')
    except Exception as e:
        print(f'Extension install note: {e}')

    # ----- Launch VSCode with the deployment file -----
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
