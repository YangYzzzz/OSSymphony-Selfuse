"""
Initial Setup: GitOps-style deployment with systemd path unit
Task ID: os_gff_051
Domain: os

Creates:
  - /opt/deploy/manifests/ directory with realistic K8s YAML files
  - A stub kubectl script so the service can reference it
  - Opens a terminal for the user to work in
"""

import os
import shlex
import subprocess
import time
from pathlib import Path


WORKDIR = '/home/user'
TASK_ID = 'os_gff_051'
SUDO_PASS = 'password'


def sudo_run(cmd, **kwargs):
    """Run a command with sudo, piping password via stdin."""
    if isinstance(cmd, str):
        full_cmd = f'echo {SUDO_PASS} | sudo -S bash -c {shlex.quote(cmd)}'
        return subprocess.run(full_cmd, shell=True, **kwargs)
    else:
        full_cmd = ['sudo', '-S'] + cmd
        return subprocess.run(full_cmd, input=f'{SUDO_PASS}\n', text=True, **kwargs)


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
    # 1. Create the manifests directory (needs sudo for /opt)
    manifests_dir = '/opt/deploy/manifests'
    sudo_run(['mkdir', '-p', manifests_dir])
    sudo_run(['chmod', '-R', '777', '/opt/deploy'])

    # 2. Create realistic Kubernetes YAML manifests
    nginx_deployment = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-frontend
  namespace: production
  labels:
    app: nginx-frontend
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx-frontend
  template:
    metadata:
      labels:
        app: nginx-frontend
        tier: frontend
    spec:
      containers:
      - name: nginx
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
    Path(f'{manifests_dir}/nginx-deployment.yml').write_text(nginx_deployment)

    redis_service = """\
apiVersion: v1
kind: Service
metadata:
  name: redis-cache
  namespace: production
  labels:
    app: redis-cache
    tier: backend
spec:
  type: ClusterIP
  ports:
  - port: 6379
    targetPort: 6379
    protocol: TCP
  selector:
    app: redis-cache
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-cache
  namespace: production
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis-cache
  template:
    metadata:
      labels:
        app: redis-cache
        tier: backend
    spec:
      containers:
      - name: redis
        image: redis:7.2-alpine
        ports:
        - containerPort: 6379
        resources:
          requests:
            cpu: "50m"
            memory: "64Mi"
          limits:
            cpu: "200m"
            memory: "128Mi"
"""
    Path(f'{manifests_dir}/redis-service.yml').write_text(redis_service)

    api_configmap = """\
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
  namespace: production
data:
  DATABASE_HOST: "postgres-primary.production.svc.cluster.local"
  DATABASE_PORT: "5432"
  REDIS_HOST: "redis-cache.production.svc.cluster.local"
  REDIS_PORT: "6379"
  LOG_LEVEL: "info"
  CORS_ORIGINS: "https://app.example.com,https://admin.example.com"
"""
    Path(f'{manifests_dir}/api-configmap.yml').write_text(api_configmap)

    # 3. Install a stub kubectl so the service unit can reference it
    kubectl_stub = '#!/bin/bash\necho "[$(date)] kubectl $@" >> /var/log/kubectl-apply.log\n'
    kubectl_path = '/usr/local/bin/kubectl'
    # Write via temp file and sudo mv
    tmp_path = '/tmp/kubectl_stub'
    Path(tmp_path).write_text(kubectl_stub)
    sudo_run(f'cp {tmp_path} {kubectl_path} && chmod 755 {kubectl_path}')
    print(f'Installed kubectl stub at {kubectl_path}')

    # 4. Ensure NO gitops systemd units exist (clean state)
    sudo_run('rm -f /etc/systemd/system/gitops-watch.path /etc/systemd/system/gitops-apply.service')
    sudo_run(['systemctl', 'daemon-reload'])

    print(f'Manifests directory created: {manifests_dir}')
    print(f'Files: {os.listdir(manifests_dir)}')

    # 5. GUI-ready: open a terminal for the user
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')


create_initial()
