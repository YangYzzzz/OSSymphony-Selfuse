"""
Initial Setup: VSCode Timeline - Restore Terraform main.tf from local history
Task ID: vscode_ops_071
Domain: vscode
"""

import json
import os
import random
import shlex
import string
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_071'
PROJECT_DIR = f'{WORKDIR}/terraform-project'
OUTPUT = f'{PROJECT_DIR}/main.tf'

HOME = os.path.expanduser('~')
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
HISTORY_DIR = os.path.join(VSCODE_USER, 'History')


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


def random_id(length=4):
    """Generate a random alphanumeric ID like VSCode uses."""
    return ''.join(random.choices(string.ascii_letters, k=length))


# ---------- Terraform file versions ----------

# Version 1: Initial commit (~4 hours ago) - basic provider and VPC
VERSION_4H_AGO = '''\
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "production-vpc"
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-west-2a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-a"
    Type = "public"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-west-2b"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-b"
    Type = "public"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "public-rt"
  }
}
'''

# Version 2: Added security group (~2 hours ago) - THE TARGET RESTORE POINT
VERSION_2H_AGO = VERSION_4H_AGO + '''
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTPS"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-security-group"
  }
}
'''

# Version 3: Added EC2 instance (~1 hour ago)
VERSION_1H_AGO = VERSION_2H_AGO + '''
resource "aws_instance" "web_server" {
  ami                    = "ami-0c55b159cbfafe1f0"
  instance_type          = "t3.medium"
  subnet_id              = aws_subnet.public_a.id
  vpc_security_group_ids = [aws_security_group.web.id]

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
  }

  tags = {
    Name        = "web-server-01"
    Environment = "production"
  }
}
'''

# Version 4: Current - Added broken/experimental ALB config (~20 min ago)
VERSION_CURRENT = VERSION_1H_AGO + '''
resource "aws_lb" "web_alb" {
  name               = "web-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web.id]
  subnets            = [aws_subnet.public_a.id, aws_subnet.public_b.id]

  enable_deletion_protection = true

  tags = {
    Name = "web-alb"
  }
}

resource "aws_lb_target_group" "web_tg" {
  name     = "web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 10
    timeout             = 60
    interval            = 300
    matcher             = "200,301,302"
  }
}

resource "aws_lb_listener" "web_http" {
  load_balancer_arn = aws_lb.web_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_tg.arn
  }
}
'''


def create_initial():
    # Create Terraform project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Write current version of main.tf
    with open(OUTPUT, 'w') as f:
        f.write(VERSION_CURRENT)
    print(f'Created: {OUTPUT}')

    # Create additional project files for realism
    with open(os.path.join(PROJECT_DIR, 'variables.tf'), 'w') as f:
        f.write('''\
variable "region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}
''')

    with open(os.path.join(PROJECT_DIR, 'outputs.tf'), 'w') as f:
        f.write('''\
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}
''')

    with open(os.path.join(PROJECT_DIR, 'terraform.tfvars'), 'w') as f:
        f.write('''\
region      = "us-west-2"
environment = "production"
vpc_cidr    = "10.0.0.0/16"
''')

    # Create VSCode local history for main.tf
    # VSCode uses a hash-based directory name for the file path
    # We'll create a unique history directory
    now_ms = int(time.time() * 1000)
    h4_ago = now_ms - (4 * 3600 * 1000)  # 4 hours ago
    h2_ago = now_ms - (2 * 3600 * 1000)  # 2 hours ago
    h1_ago = now_ms - (1 * 3600 * 1000)  # 1 hour ago
    m20_ago = now_ms - (20 * 60 * 1000)   # 20 minutes ago

    # Create a history directory with a hash-like name
    history_hash = '-' + ''.join(random.choices(string.hexdigits[:16], k=8))
    hist_dir = os.path.join(HISTORY_DIR, history_hash)
    os.makedirs(hist_dir, exist_ok=True)

    # Generate entry IDs
    id1 = random_id() + '.tf'
    id2 = random_id() + '.tf'
    id3 = random_id() + '.tf'
    id4 = random_id() + '.tf'

    # Write history entry files
    with open(os.path.join(hist_dir, id1), 'w') as f:
        f.write(VERSION_4H_AGO)

    with open(os.path.join(hist_dir, id2), 'w') as f:
        f.write(VERSION_2H_AGO)

    with open(os.path.join(hist_dir, id3), 'w') as f:
        f.write(VERSION_1H_AGO)

    with open(os.path.join(hist_dir, id4), 'w') as f:
        f.write(VERSION_CURRENT)

    # Write entries.json
    entries = {
        "version": 1,
        "resource": f"file://{OUTPUT}",
        "entries": [
            {"id": id1, "timestamp": h4_ago},
            {"id": id2, "timestamp": h2_ago},
            {"id": id3, "timestamp": h1_ago},
            {"id": id4, "timestamp": m20_ago},
        ]
    }
    with open(os.path.join(hist_dir, 'entries.json'), 'w') as f:
        json.dump(entries, f, indent=2)

    print(f'Created local history in: {hist_dir}')
    print(f'History entries: {len(entries["entries"])} versions')

    # Update VSCode settings to ensure Timeline view is enabled
    settings_path = os.path.join(VSCODE_USER, 'settings.json')
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    settings.update({
        "workbench.localHistory.enabled": True,
        "workbench.localHistory.maxFileEntries": 50,
        "security.workspace.trust.enabled": False,
        "security.workspace.trust.startupPrompt": "never",
        "security.workspace.trust.emptyWindow": False,
    })

    os.makedirs(os.path.dirname(settings_path), exist_ok=True)
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)

    print('Updated VSCode settings')

    # Launch VSCode with the project folder and main.tf open
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
