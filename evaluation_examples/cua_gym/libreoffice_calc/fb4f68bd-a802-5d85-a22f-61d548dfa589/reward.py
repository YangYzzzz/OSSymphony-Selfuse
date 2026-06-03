"""
Reward Script: Configure VSCode for Terraform IaC editing
Task ID: osworld_multi_apps_vscode_ext_script_010
Domain: vs-code / os
Scoring:
  Component 1 (0.4): HashiCorp Terraform VSCode extension installed
  Component 2 (0.3): ~/Desktop/infra/main.tf file exists
  Component 3 (0.3): main.tf contains a valid aws_s3_bucket resource block named 'my-data-bucket'
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_ext_script_010'

EXTENSIONS_DIR = os.path.join(WORKDIR, '.vscode', 'extensions')
MAIN_TF_PATH = os.path.join(WORKDIR, 'Desktop', 'infra', 'main.tf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: HashiCorp Terraform extension is installed (0.4 points)
    # Check for a directory named 'hashicorp.terraform*' inside ~/.vscode/extensions/
    # This directory is created by VSCode when the extension is installed.
    # On initial_env, only an empty extensions.json exists — no extension directories.
    try:
        ext_dirs = []
        if os.path.isdir(EXTENSIONS_DIR):
            ext_dirs = [
                entry for entry in os.listdir(EXTENSIONS_DIR)
                if entry.lower().startswith('hashicorp.terraform')
                and os.path.isdir(os.path.join(EXTENSIONS_DIR, entry))
            ]
        ext_installed = len(ext_dirs) > 0
        if ext_installed:
            print(f"PASS: Component 1 — HashiCorp Terraform extension directory found: {ext_dirs[0]} (0.4 pts)")
        else:
            print(f"FAIL: Component 1 — No 'hashicorp.terraform*' extension directory found in {EXTENSIONS_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check extensions directory: {e}")
        ext_installed = False

    if ext_installed:
        total_score += 0.4

    # Component 2: ~/Desktop/infra/main.tf file exists (0.3 points)
    # On initial_env, ~/Desktop is empty and the infra/ directory does not exist.
    try:
        tf_exists = os.path.isfile(MAIN_TF_PATH)
        if tf_exists:
            print(f"PASS: Component 2 — main.tf file exists at {MAIN_TF_PATH} (0.3 pts)")
        else:
            print(f"FAIL: Component 2 — main.tf does not exist at {MAIN_TF_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check main.tf existence: {e}")
        tf_exists = False

    if tf_exists:
        total_score += 0.3

    # Component 3: main.tf contains a valid aws_s3_bucket resource block for 'my-data-bucket' (0.3 points)
    # The task requires a resource block: resource "aws_s3_bucket" "my-data-bucket" { ... }
    # On initial_env, the file does not exist so this check trivially fails.
    try:
        if tf_exists:
            with open(MAIN_TF_PATH, 'r') as f:
                content = f.read()

            # Check for resource block with aws_s3_bucket type and 'my-data-bucket' label
            # Pattern: resource "aws_s3_bucket" "my-data-bucket"
            resource_pattern = re.search(
                r'resource\s+"aws_s3_bucket"\s+"my-data-bucket"',
                content
            )

            if resource_pattern:
                print(f"PASS: Component 3 — main.tf contains resource \"aws_s3_bucket\" \"my-data-bucket\" block (0.3 pts)")
                total_score += 0.3
            else:
                # Check if the bucket name is referenced in any other form
                print(f"FAIL: Component 3 — main.tf does not contain a valid resource \"aws_s3_bucket\" \"my-data-bucket\" block")
                print(f"      File content:\n{content[:500]}")
        else:
            print(f"SKIP: Component 3 — main.tf does not exist, cannot check resource block")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not read main.tf: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
