"""
Initial Setup: Git repo with deployment.yaml modified in last commit
Task ID: vscode_ops_051
Domain: vscode

Creates a git repository with a deployment.yaml. The last commit changed
replicas from 3 to 5 and updated the image tag. VSCode opens with this repo.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_051'
REPO_DIR = f'{WORKDIR}/{TASK_ID}'

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

def run(cmd, cwd=None):
    """Run a shell command."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
    return result

def create_initial():
    # Clean up if exists
    if os.path.exists(REPO_DIR):
        import shutil
        shutil.rmtree(REPO_DIR)

    os.makedirs(REPO_DIR, exist_ok=True)

    # --- First version of deployment.yaml (replicas=3, old image tag) ---
    deployment_v1 = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-frontend
  namespace: production
  labels:
    app: web-frontend
    team: platform-engineering
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-frontend
  template:
    metadata:
      labels:
        app: web-frontend
        version: v2.1.0
    spec:
      containers:
      - name: web-frontend
        image: registry.internal.io/web-frontend:v2.1.0
        ports:
        - containerPort: 8080
          protocol: TCP
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
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        env:
        - name: NODE_ENV
          value: "production"
        - name: LOG_LEVEL
          value: "info"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: connection-string
      imagePullSecrets:
      - name: registry-credentials
"""

    # --- Second version (replicas=5, updated image tag to v2.2.0) ---
    deployment_v2 = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-frontend
  namespace: production
  labels:
    app: web-frontend
    team: platform-engineering
spec:
  replicas: 5
  selector:
    matchLabels:
      app: web-frontend
  template:
    metadata:
      labels:
        app: web-frontend
        version: v2.2.0
    spec:
      containers:
      - name: web-frontend
        image: registry.internal.io/web-frontend:v2.2.0
        ports:
        - containerPort: 8080
          protocol: TCP
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
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
        env:
        - name: NODE_ENV
          value: "production"
        - name: LOG_LEVEL
          value: "info"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: connection-string
      imagePullSecrets:
      - name: registry-credentials
"""

    # Also add a README for realism
    readme_content = """\
# Web Frontend Deployment

Kubernetes deployment configuration for the web-frontend service.

## Overview

This repository contains the deployment manifests for the production
web-frontend application managed by the Platform Engineering team.

## Files

- `deployment.yaml` - Main deployment configuration
- `service.yaml` - Service configuration (planned)

## Deployment

```bash
kubectl apply -f deployment.yaml
```

## Change Log

- v2.2.0: Scale up replicas and update image tag
- v2.1.0: Initial production deployment
"""

    # Initialize git repo
    run('git init', cwd=REPO_DIR)
    run('git config user.email "developer@example.com"', cwd=REPO_DIR)
    run('git config user.name "Alex Rivera"', cwd=REPO_DIR)

    # Write first version and commit
    with open(os.path.join(REPO_DIR, 'deployment.yaml'), 'w') as f:
        f.write(deployment_v1)
    with open(os.path.join(REPO_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    run('git add -A', cwd=REPO_DIR)
    run('git commit -m "Initial deployment: web-frontend v2.1.0 with 3 replicas"', cwd=REPO_DIR)

    # Write second version and commit (changes replicas 3->5 and image tag v2.1.0->v2.2.0)
    with open(os.path.join(REPO_DIR, 'deployment.yaml'), 'w') as f:
        f.write(deployment_v2)

    run('git add -A', cwd=REPO_DIR)
    run('git commit -m "Scale up to 5 replicas and update image to v2.2.0"', cwd=REPO_DIR)

    print(f'Git repo created at: {REPO_DIR}')

    # Verify git log
    log_result = run('git log --oneline', cwd=REPO_DIR)
    print(f'Git log:\n{log_result.stdout}')

    diff_result = run('git diff HEAD~1 HEAD -- deployment.yaml', cwd=REPO_DIR)
    print(f'Diff of last commit:\n{diff_result.stdout}')

    # Launch VSCode with the repo folder
    launch_gui(f'code "{REPO_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
