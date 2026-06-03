"""
Reward Script: Configure comprehensive devcontainer with custom Docker build
Task ID: vscode_gf3_084
Domain: vscode
Scoring:
  - Dockerfile: base image (0.1), gcc/system deps (0.15), requirements (0.1), awscli (0.1), pgcli (0.1)
  - devcontainer.json: build config (0.1), runArgs env-file (0.1), SSH mount (0.1), Python ext (0.075), Jupyter ext (0.075)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_084'

DEVCONTAINER_DIR = os.path.join(WORKDIR, 'projects', 'data-pipeline', '.devcontainer')
DOCKERFILE_PATH = os.path.join(DEVCONTAINER_DIR, 'Dockerfile')
DEVCONTAINER_JSON_PATH = os.path.join(DEVCONTAINER_DIR, 'devcontainer.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ── DOCKERFILE CHECKS ──

    # Precondition: Dockerfile must exist
    if not os.path.exists(DOCKERFILE_PATH):
        print(f"CRITICAL: Dockerfile not found at {DOCKERFILE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(DOCKERFILE_PATH, 'r') as f:
            dockerfile_content = f.read()
        dockerfile_upper = dockerfile_content.upper()
    except Exception as e:
        print(f"CRITICAL: Cannot read Dockerfile: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Base image is python:3.11-slim (0.1 points)
    try:
        # Check for FROM python:3.11-slim (case-insensitive for FROM keyword)
        if re.search(r'(?i)^FROM\s+python:3\.11-slim', dockerfile_content, re.MULTILINE):
            print(f"PASS: Component 1 — Base image is python:3.11-slim (0.1 pts)")
            total_score += 0.1
        else:
            # Check for any python:3.11 variant
            from_match = re.search(r'(?i)^FROM\s+(\S+)', dockerfile_content, re.MULTILINE)
            found = from_match.group(1) if from_match else "none"
            print(f"FAIL: Component 1 — Expected base image python:3.11-slim, found: {found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Installs gcc and system dependencies for psycopg2 (0.15 points)
    try:
        has_gcc = bool(re.search(r'\bgcc\b', dockerfile_content))
        has_libpq = bool(re.search(r'\blibpq-dev\b', dockerfile_content))
        # Check for apt-get install
        has_apt_install = bool(re.search(r'apt-get\s+install', dockerfile_content))

        if has_gcc and has_apt_install:
            if has_libpq:
                print(f"PASS: Component 2 — gcc and libpq-dev installed via apt-get (0.15 pts)")
                total_score += 0.15
            else:
                # Partial: gcc present but no libpq-dev (give partial)
                print(f"PARTIAL: Component 2 — gcc installed but libpq-dev missing (0.1 pts)")
                total_score += 0.1
        else:
            print(f"FAIL: Component 2 — gcc={has_gcc}, apt-get install={has_apt_install}, libpq-dev={has_libpq}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Installs Python requirements from requirements.txt (0.1 points)
    try:
        # Look for pip install ... requirements.txt or COPY requirements.txt + pip install
        has_req_copy = bool(re.search(r'COPY.*requirements\.txt', dockerfile_content, re.IGNORECASE))
        has_pip_req = bool(re.search(r'pip\s+install.*requirements', dockerfile_content, re.IGNORECASE))

        if has_pip_req:
            print(f"PASS: Component 3 — Python requirements installed (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 — No pip install of requirements.txt found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Installs AWS CLI (0.1 points)
    try:
        has_awscli = bool(re.search(r'(?i)(awscli|aws-cli|aws\s+cli)', dockerfile_content))
        # Also check for 'pip install awscli' pattern
        has_pip_aws = bool(re.search(r'pip\s+install.*awscli', dockerfile_content, re.IGNORECASE))
        # Or apt-get install awscli
        has_apt_aws = bool(re.search(r'apt-get\s+install.*awscli', dockerfile_content, re.IGNORECASE))
        # Or curl-based install
        has_curl_aws = bool(re.search(r'curl.*aws', dockerfile_content, re.IGNORECASE))

        if has_awscli or has_pip_aws or has_apt_aws or has_curl_aws:
            print(f"PASS: Component 4 — AWS CLI installation found (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — No AWS CLI installation found in Dockerfile")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Installs pgcli (0.1 points)
    try:
        has_pgcli = bool(re.search(r'\bpgcli\b', dockerfile_content))
        if has_pgcli:
            print(f"PASS: Component 5 — pgcli installation found (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 5 — No pgcli installation found in Dockerfile")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ── DEVCONTAINER.JSON CHECKS ──

    # Precondition: devcontainer.json must exist
    if not os.path.exists(DEVCONTAINER_JSON_PATH):
        print(f"CRITICAL: devcontainer.json not found at {DEVCONTAINER_JSON_PATH}")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    try:
        with open(DEVCONTAINER_JSON_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content_clean = re.sub(r'/\*.*?\*/', '', content_clean, flags=re.DOTALL)
        dc = json.loads(content_clean)
    except Exception as e:
        print(f"CRITICAL: Cannot parse devcontainer.json: {e}")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 6: Build config references Dockerfile (0.1 points)
    try:
        build = dc.get('build', {})
        dockerfile_ref = build.get('dockerfile', dc.get('dockerFile', ''))
        # Accept "Dockerfile" or "./Dockerfile" or path containing "Dockerfile"
        if 'dockerfile' in str(dockerfile_ref).lower():
            print(f"PASS: Component 6 — Build references Dockerfile: '{dockerfile_ref}' (0.1 pts)")
            total_score += 0.1
        else:
            # Also check top-level dockerFile key
            top_dockerfile = dc.get('dockerFile', '')
            if 'dockerfile' in str(top_dockerfile).lower():
                print(f"PASS: Component 6 — dockerFile references Dockerfile: '{top_dockerfile}' (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 6 — No Dockerfile reference found in build config. build={build}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: runArgs with --env-file pointing to .env (0.1 points)
    try:
        run_args = dc.get('runArgs', [])
        run_args_str = ' '.join(str(a) for a in run_args)
        has_env_file_flag = '--env-file' in run_args_str
        has_env_ref = '.env' in run_args_str

        if has_env_file_flag and has_env_ref:
            print(f"PASS: Component 7 — runArgs has --env-file with .env (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 7 — runArgs missing --env-file .env. runArgs={run_args}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: SSH agent socket mount (0.1 points)
    try:
        mounts = dc.get('mounts', [])
        mounts_str = json.dumps(mounts).lower()
        has_ssh_mount = 'ssh-agent' in mounts_str or 'ssh_auth_sock' in mounts_str

        # Also check containerEnv for SSH_AUTH_SOCK
        container_env = dc.get('containerEnv', {})
        has_ssh_env = 'SSH_AUTH_SOCK' in container_env or 'ssh_auth_sock' in str(container_env).lower()

        # Primary check: mount exists with ssh-agent reference
        if has_ssh_mount:
            print(f"PASS: Component 8 — SSH agent socket mount found (0.1 pts)")
            total_score += 0.1
        elif has_ssh_env:
            # Accept if SSH_AUTH_SOCK env is set even without explicit mount string matching
            print(f"PASS: Component 8 — SSH_AUTH_SOCK configured in containerEnv (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 8 — No SSH agent socket mount found. mounts={mounts}")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    # Component 9: Python extension (0.075 points)
    try:
        extensions = []
        customizations = dc.get('customizations', {})
        vscode_custom = customizations.get('vscode', {})
        extensions = vscode_custom.get('extensions', [])
        # Also check top-level extensions key
        if not extensions:
            extensions = dc.get('extensions', [])

        extensions_lower = [e.lower() for e in extensions]
        has_python = any('python' in e and 'ms-python' in e for e in extensions_lower)
        # Also accept just "ms-python.python"
        if not has_python:
            has_python = any('ms-python.python' in e for e in extensions_lower)
        # Also accept broader python extension
        if not has_python:
            has_python = any('python' in e for e in extensions_lower)

        if has_python:
            print(f"PASS: Component 9 — Python extension found (0.075 pts)")
            total_score += 0.075
        else:
            print(f"FAIL: Component 9 — No Python extension found. extensions={extensions}")
    except Exception as e:
        print(f"ERROR: Component 9 — {e}")

    # Component 10: Jupyter extension (0.075 points)
    try:
        extensions = []
        customizations = dc.get('customizations', {})
        vscode_custom = customizations.get('vscode', {})
        extensions = vscode_custom.get('extensions', [])
        if not extensions:
            extensions = dc.get('extensions', [])

        extensions_lower = [e.lower() for e in extensions]
        has_jupyter = any('jupyter' in e for e in extensions_lower)

        if has_jupyter:
            print(f"PASS: Component 10 — Jupyter extension found (0.075 pts)")
            total_score += 0.075
        else:
            print(f"FAIL: Component 10 — No Jupyter extension found. extensions={extensions}")
    except Exception as e:
        print(f"ERROR: Component 10 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
