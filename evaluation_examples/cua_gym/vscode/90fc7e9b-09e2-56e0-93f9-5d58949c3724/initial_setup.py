"""
Initial Setup: Create Helm chart workspace with default values.yaml for reference.
Task ID: vscode_ops_094
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_094'
PROJECT_DIR = f'{WORKDIR}/helm-deploy'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a default values.yaml (typical Helm chart default values for reference)
    default_values = """\
# Default values for myapp chart
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

replicaCount: 1

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "1.25.3"

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}

podSecurityContext: {}

securityContext: {}

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: "nginx"
  annotations: {}
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []

resources: {}
  # limits:
  #   cpu: 100m
  #   memory: 128Mi
  # requests:
  #   cpu: 100m
  #   memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}
"""
    values_path = os.path.join(PROJECT_DIR, 'values.yaml')
    with open(values_path, 'w') as f:
        f.write(default_values)
    print(f'Default values.yaml created: {values_path}')

    # Create a Chart.yaml for context
    chart_yaml = """\
apiVersion: v2
name: myapp
description: A Helm chart for deploying the company application
type: application
version: 0.1.0
appVersion: "1.25.3"
"""
    chart_path = os.path.join(PROJECT_DIR, 'Chart.yaml')
    with open(chart_path, 'w') as f:
        f.write(chart_yaml)
    print(f'Chart.yaml created: {chart_path}')

    # Create templates directory with a basic deployment template for realism
    templates_dir = os.path.join(PROJECT_DIR, 'templates')
    os.makedirs(templates_dir, exist_ok=True)

    deployment_tpl = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
"""
    with open(os.path.join(templates_dir, 'deployment.yaml'), 'w') as f:
        f.write(deployment_tpl)

    ingress_tpl = """\
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "myapp.fullname" . }}
  annotations:
    {{- toYaml .Values.ingress.annotations | nindent 4 }}
spec:
  ingressClassName: {{ .Values.ingress.className }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- toYaml .Values.ingress.tls | nindent 4 }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ include "myapp.fullname" $ }}
                port:
                  number: {{ $.Values.service.port }}
          {{- end }}
    {{- end }}
{{- end }}
"""
    with open(os.path.join(templates_dir, 'ingress.yaml'), 'w') as f:
        f.write(ingress_tpl)

    print(f'Templates created in: {templates_dir}')

    # Install YAML extension for VSCode
    try:
        subprocess.run(['code', '--install-extension', 'redhat.vscode-yaml'],
                       capture_output=True, text=True, timeout=30)
        print('YAML extension installed')
    except Exception as e:
        print(f'Extension install note: {e}')

    # Ensure no custom-values.yaml exists (initial state must NOT have the answer)
    custom_path = os.path.join(PROJECT_DIR, 'custom-values.yaml')
    if os.path.exists(custom_path):
        os.remove(custom_path)

    # Launch VSCode with the workspace
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
