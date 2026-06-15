"""
Reward Script: Restore database.py to correct version via VSCode Timeline
Task ID: vscode_rf_005
Domain: vscode
Scoring:
  Component 1 (0.30): DB_HOST is correct production host
  Component 2 (0.20): DB_PORT is correct PostgreSQL port (5432)
  Component 3 (0.25): DB_NAME is correct production database name
  Component 4 (0.25): DB_USER is correct service account
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_005'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'api', 'database.py')

# Expected values from the correct (pre-breakage) version
EXPECTED_DB_HOST = "db-prod-replica-01.internal.acme.io"
EXPECTED_DB_PORT = "5432"
EXPECTED_DB_NAME = "acme_api_production"
EXPECTED_DB_USER = "api_service"


def extract_env_default(content, var_name):
    """Extract the default value from os.getenv('VAR', 'default') pattern."""
    # Match patterns like: os.getenv("DB_HOST", "some_value")
    pattern = rf'{var_name}\s*=\s*.*?os\.getenv\(\s*["\'].*?["\']\s*,\s*["\']([^"\']*)["\']'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None


def verify_task(file_path):
    """
    Verify that database.py has been restored to the correct version
    with proper production connection configuration.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the file
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: DB_HOST is correct production host (0.30 points)
    try:
        db_host = extract_env_default(content, 'DB_HOST')
        if db_host == EXPECTED_DB_HOST:
            print(f"PASS: Component 1 - DB_HOST is '{db_host}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 - DB_HOST expected '{EXPECTED_DB_HOST}', found '{db_host}'")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: DB_PORT is correct PostgreSQL port (0.20 points)
    try:
        db_port = extract_env_default(content, 'DB_PORT')
        if db_port == EXPECTED_DB_PORT:
            print(f"PASS: Component 2 - DB_PORT is '{db_port}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 - DB_PORT expected '{EXPECTED_DB_PORT}', found '{db_port}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: DB_NAME is correct production database (0.25 points)
    try:
        db_name = extract_env_default(content, 'DB_NAME')
        if db_name == EXPECTED_DB_NAME:
            print(f"PASS: Component 3 - DB_NAME is '{db_name}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - DB_NAME expected '{EXPECTED_DB_NAME}', found '{db_name}'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: DB_USER is correct service account (0.25 points)
    try:
        db_user = extract_env_default(content, 'DB_USER')
        if db_user == EXPECTED_DB_USER:
            print(f"PASS: Component 4 - DB_USER is '{db_user}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 - DB_USER expected '{EXPECTED_DB_USER}', found '{db_user}'")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
