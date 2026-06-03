"""
Reward Script: Terraform S3 Backend Configuration
Task ID: vscode_ops_078
Domain: vscode
Scoring:
  Component 1: backend.tf exists and contains backend "s3" block (0.2)
  Component 2: bucket = "my-terraform-state" (0.2)
  Component 3: key = "prod/terraform.tfstate" (0.2)
  Component 4: region = "us-east-1" (0.2)
  Component 5: dynamodb_table = "terraform-locks" (0.2)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_078'
BACKEND_FILE = os.path.join(WORKDIR, 'terraform-prod', 'backend.tf')


def parse_hcl_value(content, key):
    """Extract a quoted string value for a given HCL key from content."""
    # Match patterns like: key = "value" or key="value"
    pattern = rf'{re.escape(key)}\s*=\s*"([^"]*)"'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: backend.tf must exist
    if not os.path.exists(BACKEND_FILE):
        print(f"CRITICAL: backend.tf not found at {BACKEND_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(BACKEND_FILE, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {BACKEND_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File contains a backend "s3" block (0.2 points)
    # This checks that backend.tf has a proper S3 backend declaration
    try:
        # Match: backend "s3" { ... }
        has_s3_backend = bool(re.search(r'backend\s+"s3"\s*\{', content))
        if has_s3_backend:
            print(f"PASS: Component 1 -- backend \"s3\" block found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- no backend \"s3\" block found in backend.tf")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: bucket = "my-terraform-state" (0.2 points)
    try:
        bucket_val = parse_hcl_value(content, 'bucket')
        if bucket_val == 'my-terraform-state':
            print(f"PASS: Component 2 -- bucket = \"my-terraform-state\" (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- expected bucket=\"my-terraform-state\", found: {bucket_val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: key = "prod/terraform.tfstate" (0.2 points)
    try:
        key_val = parse_hcl_value(content, 'key')
        if key_val == 'prod/terraform.tfstate':
            print(f"PASS: Component 3 -- key = \"prod/terraform.tfstate\" (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- expected key=\"prod/terraform.tfstate\", found: {key_val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: region = "us-east-1" (0.2 points)
    # NOTE: We specifically check for region inside the backend "s3" block
    # to avoid false positives from provider region settings in other files.
    try:
        # Extract the backend "s3" { ... } block content first
        backend_block_match = re.search(r'backend\s+"s3"\s*\{([^}]*)\}', content, re.DOTALL)
        if backend_block_match:
            backend_block = backend_block_match.group(1)
            region_val = parse_hcl_value(backend_block, 'region')
            if region_val == 'us-east-1':
                print(f"PASS: Component 4 -- region = \"us-east-1\" in backend block (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 -- expected region=\"us-east-1\" in backend block, found: {region_val!r}")
        else:
            print(f"FAIL: Component 4 -- no backend \"s3\" block to check region in")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: dynamodb_table = "terraform-locks" (0.2 points)
    try:
        dynamo_val = parse_hcl_value(content, 'dynamodb_table')
        if dynamo_val == 'terraform-locks':
            print(f"PASS: Component 5 -- dynamodb_table = \"terraform-locks\" (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 -- expected dynamodb_table=\"terraform-locks\", found: {dynamo_val!r}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
