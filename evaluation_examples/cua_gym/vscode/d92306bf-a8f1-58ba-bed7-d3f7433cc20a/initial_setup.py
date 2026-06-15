"""
Initial Setup: Create workspace for Kubernetes deployment YAML task
Task ID: vscode_ops_041
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_041'
WORKSPACE_DIR = f'{WORKDIR}/k8s-manifests'

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

    # Create some existing K8s manifest files to make the workspace realistic
    # A service manifest
    service_yaml = """\
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: production
  labels:
    app: frontend
    tier: web
spec:
  type: ClusterIP
  selector:
    app: frontend
    tier: web
  ports:
    - name: http
      port: 80
      targetPort: 3000
      protocol: TCP
    - name: https
      port: 443
      targetPort: 3443
      protocol: TCP
"""
    with open(os.path.join(WORKSPACE_DIR, 'frontend-service.yaml'), 'w') as f:
        f.write(service_yaml)

    # A configmap manifest
    configmap_yaml = """\
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  DATABASE_HOST: "postgres.production.svc.cluster.local"
  DATABASE_PORT: "5432"
  REDIS_HOST: "redis.production.svc.cluster.local"
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"
  ENABLE_METRICS: "true"
"""
    with open(os.path.join(WORKSPACE_DIR, 'app-config.yaml'), 'w') as f:
        f.write(configmap_yaml)

    # A namespace manifest
    namespace_yaml = """\
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    team: platform-engineering
"""
    with open(os.path.join(WORKSPACE_DIR, 'namespace.yaml'), 'w') as f:
        f.write(namespace_yaml)

    # An ingress manifest
    ingress_yaml = """\
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: frontend-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: tls-secret
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
"""
    with open(os.path.join(WORKSPACE_DIR, 'ingress.yaml'), 'w') as f:
        f.write(ingress_yaml)

    # Ensure NO app-deployment.yaml exists (the task is to create it)
    deployment_path = os.path.join(WORKSPACE_DIR, 'app-deployment.yaml')
    if os.path.exists(deployment_path):
        os.remove(deployment_path)

    print(f'Workspace created: {WORKSPACE_DIR}')
    print(f'Files: {os.listdir(WORKSPACE_DIR)}')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
