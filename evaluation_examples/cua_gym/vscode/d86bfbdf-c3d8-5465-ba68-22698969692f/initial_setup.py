"""
Initial Setup: Create Terraform workspace with main.tf but no backend.tf
Task ID: vscode_ops_078
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_078'
PROJECT_DIR = f'{WORKDIR}/terraform-prod'

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
    # Create the terraform-prod workspace directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create main.tf with an empty terraform block (no backend)
    main_tf_content = """\
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "prod-vpc"
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "prod-public-subnet-a"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "prod-public-subnet-b"
  }
}

resource "aws_security_group" "web" {
  name        = "prod-web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "prod-web-sg"
  }
}
"""

    main_tf_path = os.path.join(PROJECT_DIR, 'main.tf')
    with open(main_tf_path, 'w') as f:
        f.write(main_tf_content)
    print(f'Created: {main_tf_path}')

    # Create a variables.tf for added realism
    variables_tf_content = """\
variable "environment" {
  description = "The deployment environment"
  type        = string
  default     = "production"
}

variable "instance_type" {
  description = "EC2 instance type for web servers"
  type        = string
  default     = "t3.medium"
}

variable "min_capacity" {
  description = "Minimum number of instances in ASG"
  type        = number
  default     = 2
}

variable "max_capacity" {
  description = "Maximum number of instances in ASG"
  type        = number
  default     = 6
}
"""

    variables_tf_path = os.path.join(PROJECT_DIR, 'variables.tf')
    with open(variables_tf_path, 'w') as f:
        f.write(variables_tf_content)
    print(f'Created: {variables_tf_path}')

    # Create outputs.tf for realism
    outputs_tf_content = """\
output "vpc_id" {
  description = "The ID of the production VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

output "web_sg_id" {
  description = "Security group ID for web servers"
  value       = aws_security_group.web.id
}
"""

    outputs_tf_path = os.path.join(PROJECT_DIR, 'outputs.tf')
    with open(outputs_tf_path, 'w') as f:
        f.write(outputs_tf_content)
    print(f'Created: {outputs_tf_path}')

    # Ensure NO backend.tf exists
    backend_tf_path = os.path.join(PROJECT_DIR, 'backend.tf')
    if os.path.exists(backend_tf_path):
        os.remove(backend_tf_path)
        print(f'Removed existing: {backend_tf_path}')

    print(f'Workspace created at: {PROJECT_DIR}')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
