"""
Reward Script: Restore main.tf to a previous version from ~2 hours ago using VSCode Timeline
Task ID: vscode_ops_071
Domain: vscode
Scoring:
  Component 1 (0.4): aws_instance resource block removed from main.tf
  Component 2 (0.3): aws_lb / aws_lb_target_group / aws_lb_listener resource blocks removed
  Component 3 (0.3): Exact content match with the historical (~2h ago) version
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_071'
MAIN_TF = os.path.join(WORKDIR, 'terraform-project', 'main.tf')

# The expected content of main.tf after restoring to the ~2-hour-ago version.
# This version ends after the aws_security_group "web" resource and does NOT
# contain aws_instance, aws_lb, aws_lb_target_group, or aws_lb_listener.
EXPECTED_CONTENT = r'''terraform {
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


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: aws_instance resource block is removed (0.4 points)
    # In the initial state, main.tf contains 'resource "aws_instance"'.
    # After restoring to the 2h-ago version, it should be gone.
    try:
        has_instance = bool(re.search(r'resource\s+"aws_instance"', content))
        if not has_instance:
            print(f"PASS: Component 1 -- aws_instance resource not present (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- aws_instance resource still present in main.tf")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: aws_lb, aws_lb_target_group, aws_lb_listener removed (0.3 points)
    # These three resources were added after the 2h-ago version. All must be absent.
    try:
        has_lb = bool(re.search(r'resource\s+"aws_lb"\s+"web_alb"', content))
        has_tg = bool(re.search(r'resource\s+"aws_lb_target_group"', content))
        has_listener = bool(re.search(r'resource\s+"aws_lb_listener"', content))

        removed_count = sum([not has_lb, not has_tg, not has_listener])
        if removed_count == 3:
            print(f"PASS: Component 2 -- all 3 LB-related resources removed (0.3 pts)")
            total_score += 0.3
        else:
            still_present = []
            if has_lb:
                still_present.append("aws_lb")
            if has_tg:
                still_present.append("aws_lb_target_group")
            if has_listener:
                still_present.append("aws_lb_listener")
            print(f"FAIL: Component 2 -- {len(still_present)} LB resources still present: {still_present}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Exact content match with historical version (0.3 points)
    # The restored file should match the ~2h-ago version character-for-character
    # (after normalizing trailing whitespace/newlines).
    try:
        normalized_actual = content.strip()
        normalized_expected = EXPECTED_CONTENT.strip()
        if normalized_actual == normalized_expected:
            print(f"PASS: Component 3 -- exact content match with historical version (0.3 pts)")
            total_score += 0.3
        else:
            # Give partial credit if core resources are intact but minor whitespace diffs
            actual_lines = [l.rstrip() for l in normalized_actual.splitlines()]
            expected_lines = [l.rstrip() for l in normalized_expected.splitlines()]
            if actual_lines == expected_lines:
                print(f"PASS: Component 3 -- content matches after trailing-whitespace normalization (0.3 pts)")
                total_score += 0.3
            else:
                # Check how many lines match
                matching = sum(1 for a, e in zip(actual_lines, expected_lines) if a == e)
                total_lines = max(len(actual_lines), len(expected_lines))
                match_pct = matching / total_lines if total_lines > 0 else 0
                print(f"FAIL: Component 3 -- content mismatch. {matching}/{total_lines} lines match ({match_pct:.0%})")
                print(f"  Actual length: {len(normalized_actual)} chars, Expected: {len(normalized_expected)} chars")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(MAIN_TF):
    print(f"File not found: {MAIN_TF}")
    print("REWARD: 0.0")
else:
    verify_task(MAIN_TF)
