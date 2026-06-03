"""
Initial Setup: Create workspace with config files containing IP addresses for regex search task
Task ID: vscode_ops_034
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_034'
WORKSPACE_DIR = f'{WORKDIR}/workspace'


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


def create_workspace():
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Write VSCode settings to disable workspace trust and search exclusions
    vscode_settings_dir = os.path.expanduser('~/.config/Code/User')
    os.makedirs(vscode_settings_dir, exist_ok=True)
    import json
    settings_path = os.path.join(vscode_settings_dir, 'settings.json')
    settings = {
        "security.workspace.trust.enabled": False,
        "search.exclude": {},
        "files.exclude": {},
        "search.useIgnoreFiles": False,
        "search.followSymlinks": True
    }
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)

    # --- nginx.conf ---
    create_file(f'{WORKSPACE_DIR}/nginx.conf', """\
# Nginx reverse proxy configuration
# Last updated: 2025-11-20

upstream backend_servers {
    server 10.0.1.15:8080 weight=3;
    server 10.0.1.16:8080 weight=2;
    server 10.0.1.17:8080 backup;
}

server {
    listen 80;
    server_name app.meridian-analytics.com;

    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api {
        proxy_pass http://10.0.2.50:3000;
        proxy_read_timeout 90s;
    }

    # Static assets served from CDN origin
    location /static {
        proxy_pass http://192.168.100.5:9000;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    access_log /var/log/nginx/meridian_access.log;
    error_log /var/log/nginx/meridian_error.log warn;
}
""")

    # --- database.yaml ---
    create_file(f'{WORKSPACE_DIR}/database.yaml', """\
# Database cluster configuration
# Meridian Analytics - Production Environment

postgresql:
  primary:
    host: 172.16.0.10
    port: 5432
    database: meridian_prod
    max_connections: 200
    ssl_mode: require
  replicas:
    - host: 172.16.0.11
      port: 5432
      role: read_replica
      max_connections: 100
    - host: 172.16.0.12
      port: 5432
      role: read_replica
      max_connections: 100

redis:
  sentinel:
    hosts:
      - 172.16.1.20:26379
      - 172.16.1.21:26379
      - 172.16.1.22:26379
    master_name: meridian-cache
    password: "${REDIS_SENTINEL_PASSWORD}"
  cluster:
    nodes:
      - 172.16.1.30:6379
      - 172.16.1.31:6379
      - 172.16.1.32:6379

elasticsearch:
  hosts:
    - 172.16.2.40:9200
    - 172.16.2.41:9200
    - 172.16.2.42:9200
  index_prefix: meridian
  shards: 5
  replicas: 1
""")

    # --- app.env ---
    create_file(f'{WORKSPACE_DIR}/app.env', """\
# Application Environment Variables
# Meridian Analytics Platform

APP_NAME=meridian-analytics
APP_ENV=production
APP_DEBUG=false
APP_PORT=8080

# Database
DATABASE_URL=postgresql://app_user:${DB_PASSWORD}@172.16.0.10:5432/meridian_prod
DATABASE_POOL_SIZE=25
DATABASE_READ_REPLICA=172.16.0.11

# Cache
REDIS_URL=redis://:${REDIS_PASSWORD}@172.16.1.30:6379/0
REDIS_CACHE_TTL=3600

# External Services
PAYMENT_GATEWAY_HOST=10.5.0.100
PAYMENT_GATEWAY_PORT=443
EMAIL_SMTP_HOST=10.5.0.101
EMAIL_SMTP_PORT=587

# Monitoring
PROMETHEUS_PUSHGATEWAY=10.10.0.50:9091
GRAFANA_HOST=10.10.0.51
JAEGER_AGENT_HOST=10.10.0.52
JAEGER_AGENT_PORT=6831

# API Keys (rotate quarterly)
STRIPE_WEBHOOK_SECRET=${STRIPE_SECRET}
SENDGRID_API_KEY=${SENDGRID_KEY}

# Logging
LOG_LEVEL=info
SYSLOG_SERVER=10.10.0.55:514
""")

    # --- infrastructure.tf ---
    create_file(f'{WORKSPACE_DIR}/infrastructure.tf', """\
# Terraform configuration for Meridian Analytics
# Cloud infrastructure provisioning

provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "meridian-vpc"
    Environment = "production"
  }
}

resource "aws_subnet" "public_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-west-2a"

  tags = {
    Name = "meridian-public-a"
  }
}

resource "aws_subnet" "private_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.10.0/24"
  availability_zone = "us-west-2a"

  tags = {
    Name = "meridian-private-a"
  }
}

resource "aws_security_group" "web" {
  name        = "meridian-web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
    description = "SSH from VPC only"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "bastion" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public_a.id
  private_ip    = "10.0.1.100"

  tags = {
    Name = "meridian-bastion"
    Role = "jumpbox"
  }
}

resource "aws_lb" "main" {
  name               = "meridian-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = [aws_subnet.public_a.id]

  tags = {
    Name = "meridian-alb"
  }
}

# DNS records
resource "aws_route53_record" "api" {
  zone_id = var.hosted_zone_id
  name    = "api.meridian-analytics.com"
  type    = "A"

  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}

# VPN gateway for office connectivity
resource "aws_vpn_gateway" "office" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "meridian-vpn-gw"
  }
}

resource "aws_customer_gateway" "office" {
  bgp_asn    = 65000
  ip_address = "203.0.113.25"
  type       = "ipsec.1"

  tags = {
    Name = "meridian-office-gw"
  }
}
""")

    # --- monitoring.conf ---
    create_file(f'{WORKSPACE_DIR}/monitoring.conf', """\
# Prometheus & Alertmanager Configuration
# Meridian Analytics Monitoring Stack

[global]
scrape_interval = 15s
evaluation_interval = 15s

[alertmanager]
targets = 10.10.0.60:9093

[scrape_configs]

# Application metrics
job_name = meridian-app
static_configs_targets = 10.0.1.15:9090,10.0.1.16:9090,10.0.1.17:9090
metrics_path = /metrics
scrape_interval = 10s

# Database exporters
job_name = postgres-exporter
static_configs_targets = 172.16.0.10:9187,172.16.0.11:9187,172.16.0.12:9187
scrape_interval = 30s

# Redis exporter
job_name = redis-exporter
static_configs_targets = 172.16.1.30:9121
scrape_interval = 15s

# Node exporters (all hosts)
job_name = node-exporter
static_configs_targets = 10.0.1.15:9100,10.0.1.16:9100,10.0.1.17:9100,172.16.0.10:9100,172.16.0.11:9100,172.16.0.12:9100,10.10.0.50:9100

# Blackbox exporter for endpoint probing
job_name = blackbox
static_configs_targets = 10.10.0.53:9115
modules = http_2xx
relabel_target = 203.0.113.25:443
""")

    print(f'Workspace created at: {WORKSPACE_DIR}')
    print(f'Files: nginx.conf, database.yaml, app.env, infrastructure.tf, monitoring.conf')


def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def main():
    create_workspace()

    # Open VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with workspace folder with DISPLAY=:0')


main()
