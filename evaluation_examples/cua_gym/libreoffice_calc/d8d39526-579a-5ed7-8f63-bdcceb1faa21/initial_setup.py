"""
Initial Setup: Configure a Kubernetes Ingress resource for api-server
Task ID: os_gf2_040
Domain: os (Kubernetes manifest creation)
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'os_gf2_040'

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
    # Create a project directory structure for Kubernetes work
    k8s_dir = os.path.join(WORKDIR, 'k8s-manifests', 'production')
    os.makedirs(k8s_dir, exist_ok=True)

    # Create an existing service manifest to provide context
    # (The api-server service already exists in the cluster)
    service_yaml = """apiVersion: v1
kind: Service
metadata:
  name: api-server
  namespace: production
  labels:
    app: api-server
    tier: backend
spec:
  type: ClusterIP
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
      name: http
  selector:
    app: api-server
"""
    Path(os.path.join(k8s_dir, 'api-server-service.yaml')).write_text(service_yaml)

    # Create a deployment manifest for context
    deployment_yaml = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
  namespace: production
  labels:
    app: api-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-server
  template:
    metadata:
      labels:
        app: api-server
    spec:
      containers:
        - name: api-server
          image: company-registry.io/api-server:v2.4.1
          ports:
            - containerPort: 8080
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          env:
            - name: DB_HOST
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: host
            - name: LOG_LEVEL
              value: "info"
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
"""
    Path(os.path.join(k8s_dir, 'api-server-deployment.yaml')).write_text(deployment_yaml)

    # Create a namespace manifest
    namespace_yaml = """apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    team: platform
"""
    Path(os.path.join(k8s_dir, 'namespace.yaml')).write_text(namespace_yaml)

    # Create a TLS secret reference (just the manifest, not actual cert data)
    tls_secret_yaml = """apiVersion: v1
kind: Secret
metadata:
  name: api-tls-secret
  namespace: production
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTi... # base64-encoded certificate
  tls.key: LS0tLS1CRUdJTi... # base64-encoded private key
"""
    Path(os.path.join(k8s_dir, 'api-tls-secret.yaml')).write_text(tls_secret_yaml)

    # Create a README for the project
    readme = """# Production Kubernetes Manifests

This directory contains Kubernetes manifests for the production namespace.

## Services
- **api-server**: Main API backend service (port 8080)

## Secrets
- **api-tls-secret**: TLS certificate for api.company.com

## TODO
- [ ] Create Ingress resource for api-server with TLS and rate limiting
- [ ] Set up monitoring with Prometheus ServiceMonitor
"""
    Path(os.path.join(k8s_dir, 'README.md')).write_text(readme)

    # NO ingress manifest exists yet - the agent must create it
    print(f'Initial k8s project structure created at: {k8s_dir}')

    # Open a terminal and file manager for the user
    launch_gui('gnome-terminal --working-directory=/home/user/k8s-manifests/production', delay_sec=2.0)
    launch_gui('nautilus "/home/user/k8s-manifests/production"', delay_sec=1.5)
    print('GUI_READY: launched terminal and file manager with DISPLAY=:0')

create_initial()
