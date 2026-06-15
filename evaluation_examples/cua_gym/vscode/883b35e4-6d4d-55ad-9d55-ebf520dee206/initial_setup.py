"""
Initial Setup: Create K8s YAML files workspace, some missing namespace field
Task ID: vscode_ops_049
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_049'
K8S_DIR = f'{WORKDIR}/k8s'


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


# --- YAML file contents ---
# Files WITH namespace: production (4 files)
# Files WITHOUT namespace (4 files) - these need the agent to add it

FILES_WITH_NAMESPACE = {
    "api-deployment.yaml": """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
  namespace: production
  labels:
    app: api-server
    tier: backend
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
        image: registry.internal.io/api-server:2.4.1
        ports:
        - containerPort: 8080
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
          requests:
            cpu: "250m"
            memory: "256Mi"
        env:
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: db-config
              key: host
""",
    "redis-service.yaml": """\
apiVersion: v1
kind: Service
metadata:
  name: redis-cache
  namespace: production
  labels:
    app: redis
    component: cache
spec:
  type: ClusterIP
  ports:
  - port: 6379
    targetPort: 6379
    protocol: TCP
  selector:
    app: redis
    component: cache
""",
    "monitoring-configmap.yaml": """\
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: production
  labels:
    app: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    scrape_configs:
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
""",
    "ingress.yaml": """\
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls-secret
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-server
            port:
              number: 8080
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 3000
""",
}

FILES_WITHOUT_NAMESPACE = {
    "worker-deployment.yaml": """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: background-worker
  labels:
    app: background-worker
    tier: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: background-worker
  template:
    metadata:
      labels:
        app: background-worker
    spec:
      containers:
      - name: worker
        image: registry.internal.io/bg-worker:1.8.3
        resources:
          limits:
            cpu: "1000m"
            memory: "1Gi"
          requests:
            cpu: "500m"
            memory: "512Mi"
        env:
        - name: QUEUE_URL
          valueFrom:
            secretKeyRef:
              name: queue-credentials
              key: url
""",
    "postgres-statefulset.yaml": """\
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-primary
  labels:
    app: postgres
    role: primary
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
      role: primary
  template:
    metadata:
      labels:
        app: postgres
        role: primary
    spec:
      containers:
      - name: postgres
        image: postgres:15.4
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
        env:
        - name: POSTGRES_DB
          value: "appdb"
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-credentials
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-credentials
              key: password
  volumeClaimTemplates:
  - metadata:
      name: postgres-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 50Gi
""",
    "frontend-service.yaml": """\
apiVersion: v1
kind: Service
metadata:
  name: frontend
  labels:
    app: frontend
    tier: web
spec:
  type: ClusterIP
  ports:
  - port: 3000
    targetPort: 3000
    protocol: TCP
    name: http
  selector:
    app: frontend
    tier: web
""",
    "cronjob-cleanup.yaml": """\
apiVersion: batch/v1
kind: CronJob
metadata:
  name: data-cleanup
  labels:
    app: maintenance
    schedule: nightly
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        metadata:
          labels:
            app: maintenance
        spec:
          containers:
          - name: cleanup
            image: registry.internal.io/cleanup-job:1.2.0
            args:
            - "--older-than=30d"
            - "--dry-run=false"
            env:
            - name: STORAGE_BUCKET
              value: "gs://app-data-archive"
          restartPolicy: OnFailure
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
""",
}


def create_initial():
    os.makedirs(K8S_DIR, exist_ok=True)

    # Write files that already have namespace
    for filename, content in FILES_WITH_NAMESPACE.items():
        filepath = os.path.join(K8S_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Created: {filepath}')

    # Write files missing namespace
    for filename, content in FILES_WITHOUT_NAMESPACE.items():
        filepath = os.path.join(K8S_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'Created: {filepath}')

    print(f'\nWorkspace created at {K8S_DIR} with 8 YAML files')
    print('Files WITH namespace: ' + ', '.join(FILES_WITH_NAMESPACE.keys()))
    print('Files WITHOUT namespace: ' + ', '.join(FILES_WITHOUT_NAMESPACE.keys()))

    # Open VSCode with the k8s workspace
    launch_gui(f'code "{K8S_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
