"""
Initial Setup: Set up infrastructure-repo workspace for Terraform task
Task ID: vscode_td_036
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_036'
REPO_DIR = os.path.join(WORKDIR, 'infrastructure-repo')


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
    # Create directory structure
    os.makedirs(os.path.join(REPO_DIR, 'infra'), exist_ok=True)
    os.makedirs(os.path.join(REPO_DIR, 'environments'), exist_ok=True)

    # --- infra/main.tf ---
    main_tf = os.path.join(REPO_DIR, 'infra', 'main.tf')
    with open(main_tf, 'w') as f:
        f.write('''\
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "acme-terraform-state"
    key            = "staging/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = "acme-platform"
    }
  }
}

module "networking" {
  source = "./modules/networking"

  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  environment        = var.environment
}

module "compute" {
  source = "./modules/compute"

  instance_type    = var.instance_type
  min_size         = var.min_size
  max_size         = var.max_size
  desired_capacity = var.desired_capacity
  subnet_ids       = module.networking.private_subnet_ids
  vpc_id           = module.networking.vpc_id
  environment      = var.environment
}

module "database" {
  source = "./modules/database"

  db_instance_class    = var.db_instance_class
  db_name              = var.db_name
  db_engine_version    = var.db_engine_version
  subnet_ids           = module.networking.private_subnet_ids
  vpc_security_group_ids = [module.networking.db_security_group_id]
  environment          = var.environment
}

output "vpc_id" {
  value = module.networking.vpc_id
}

output "alb_dns_name" {
  value = module.compute.alb_dns_name
}

output "db_endpoint" {
  value     = module.database.endpoint
  sensitive = true
}
''')

    # --- infra/variables.tf ---
    variables_tf = os.path.join(REPO_DIR, 'infra', 'variables.tf')
    with open(variables_tf, 'w') as f:
        f.write('''\
variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b", "us-west-2c"]
}

variable "instance_type" {
  description = "EC2 instance type for compute nodes"
  type        = string
  default     = "t3.medium"
}

variable "min_size" {
  description = "Minimum number of instances in ASG"
  type        = number
  default     = 2
}

variable "max_size" {
  description = "Maximum number of instances in ASG"
  type        = number
  default     = 10
}

variable "desired_capacity" {
  description = "Desired number of instances in ASG"
  type        = number
  default     = 3
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.r6g.large"
}

variable "db_name" {
  description = "Name of the database"
  type        = string
  default     = "acme_platform"
}

variable "db_engine_version" {
  description = "PostgreSQL engine version"
  type        = string
  default     = "15.4"
}
''')

    # --- environments/staging.tfvars ---
    staging_tfvars = os.path.join(REPO_DIR, 'environments', 'staging.tfvars')
    with open(staging_tfvars, 'w') as f:
        f.write('''\
# Staging Environment Configuration
# Last updated: 2025-11-20 by DevOps team

environment = "staging"
aws_region  = "us-west-2"

# Networking
vpc_cidr           = "10.1.0.0/16"
availability_zones = ["us-west-2a", "us-west-2b"]

# Compute - smaller footprint for staging
instance_type    = "t3.small"
min_size         = 1
max_size         = 4
desired_capacity = 2

# Database - smaller instance for staging
db_instance_class = "db.t3.medium"
db_name           = "acme_platform_staging"
db_engine_version = "15.4"
''')

    # Ensure NO .vscode folder exists (task requirement)
    vscode_dir = os.path.join(REPO_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial workspace created: {REPO_DIR}')

    # GUI-ready startup: open VSCode with the workspace folder
    launch_gui(f'code "{REPO_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
