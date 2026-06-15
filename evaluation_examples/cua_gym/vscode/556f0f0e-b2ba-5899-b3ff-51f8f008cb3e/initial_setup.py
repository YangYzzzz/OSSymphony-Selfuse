"""
Initial Setup: Configure VSCode terminal profile K8s-Prod
Task ID: vscode_ops_058
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_058'
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


def create_initial():
    # 1. Create /home/user/.kube/prod.config (realistic kubeconfig)
    kube_dir = os.path.join(WORKDIR, '.kube')
    os.makedirs(kube_dir, exist_ok=True)

    kubeconfig_content = """apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTi...BASE64DATA...LS0tLS0K
    server: https://k8s-prod-api.company.internal:6443
  name: prod-cluster
contexts:
- context:
    cluster: prod-cluster
    namespace: default
    user: prod-admin
  name: prod-context
current-context: prod-context
preferences: {}
users:
- name: prod-admin
  user:
    client-certificate-data: LS0tLS1CRUdJTi...BASE64CERT...LS0tLS0K
    client-key-data: LS0tLS1CRUdJTi...BASE64KEY...LS0tLS0K
"""
    with open(os.path.join(kube_dir, 'prod.config'), 'w') as f:
        f.write(kubeconfig_content)
    print(f'Created {kube_dir}/prod.config')

    # 2. Create /home/user/k8s/ directory with realistic manifests
    k8s_dir = os.path.join(WORKDIR, 'k8s')
    os.makedirs(k8s_dir, exist_ok=True)

    deployment_yaml = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  namespace: production
  labels:
    app: payment-service
    tier: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-service
  template:
    metadata:
      labels:
        app: payment-service
        tier: backend
    spec:
      containers:
      - name: payment-service
        image: registry.company.internal/payment-service:2.4.1
        ports:
        - containerPort: 8080
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: payment-db-creds
              key: host
        - name: REDIS_URL
          value: "redis://cache-cluster.production.svc:6379"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
"""
    with open(os.path.join(k8s_dir, 'deployment.yaml'), 'w') as f:
        f.write(deployment_yaml)

    service_yaml = """apiVersion: v1
kind: Service
metadata:
  name: payment-service
  namespace: production
spec:
  selector:
    app: payment-service
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
"""
    with open(os.path.join(k8s_dir, 'service.yaml'), 'w') as f:
        f.write(service_yaml)

    ingress_yaml = """apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: payment-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: api.company.internal
    http:
      paths:
      - path: /payments
        pathType: Prefix
        backend:
          service:
            name: payment-service
            port:
              number: 80
"""
    with open(os.path.join(k8s_dir, 'ingress.yaml'), 'w') as f:
        f.write(ingress_yaml)
    print(f'Created k8s manifests in {k8s_dir}')

    # 3. Set up VSCode settings with default config but NO terminal profiles
    os.makedirs(VSCODE_USER, exist_ok=True)

    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Add some default settings but explicitly NO terminal profiles
    settings.update({
        "editor.fontSize": 14,
        "editor.tabSize": 2,
        "editor.wordWrap": "on",
        "workbench.colorTheme": "Default Dark Modern",
        "terminal.integrated.defaultProfile.linux": "bash",
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
    })

    # Ensure no terminal profiles exist in initial state
    if "terminal.integrated.profiles.linux" in settings:
        del settings["terminal.integrated.profiles.linux"]

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'Created VSCode settings at {SETTINGS_PATH}')

    # 4. Launch VSCode with the k8s directory
    launch_gui(f'code "{k8s_dir}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
