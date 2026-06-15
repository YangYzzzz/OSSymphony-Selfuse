"""
Reward Script: Create a Kubernetes Secret YAML with base64-encoded database credentials
Task ID: vscode_ops_089
Domain: vscode (k8s YAML creation)
Scoring:
  Component 1 (0.15): File exists and is valid YAML
  Component 2 (0.15): apiVersion: v1, kind: Secret
  Component 3 (0.15): type: Opaque
  Component 4 (0.15): data section has DB_HOST, DB_USER, DB_PASS keys
  Component 5 (0.15): DB_HOST decodes to db.internal.svc
  Component 6 (0.10): DB_USER decodes to admin
  Component 7 (0.15): DB_PASS decodes to s3cur3P@ss
"""

import os
import base64

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_089'
SECRET_PATH = os.path.join(WORKDIR, 'k8s', 'secret.yaml')


def parse_yaml_simple(content):
    """
    Minimal YAML parser for flat/one-level-nested k8s manifests.
    Returns a dict. Handles simple key: value and one-level nested mappings.
    """
    result = {}
    current_key = None
    current_dict = None

    for line in content.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        # Check indentation level
        indent = len(line) - len(line.lstrip())

        if indent == 0:
            # Top-level key
            if ':' in stripped:
                key, _, value = stripped.partition(':')
                key = key.strip()
                value = value.strip()
                if value:
                    result[key] = value
                else:
                    # Start of a nested block
                    current_key = key
                    current_dict = {}
                    result[current_key] = current_dict
        elif indent > 0 and current_dict is not None:
            # Nested key under current_key
            if ':' in stripped:
                key, _, value = stripped.partition(':')
                key = key.strip()
                value = value.strip()
                current_dict[key] = value

    return result


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File exists and is valid YAML (0.15 points)
    try:
        if not os.path.isfile(file_path):
            print(f"FAIL: Component 1 -- secret.yaml does not exist at {file_path}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with open(file_path, 'r') as f:
            content = f.read()

        if not content.strip():
            print("FAIL: Component 1 -- secret.yaml is empty")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        parsed = parse_yaml_simple(content)
        if not parsed:
            print("FAIL: Component 1 -- Could not parse YAML content")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        if parsed and content.strip():
            print(f"PASS: Component 1 -- secret.yaml exists and is parseable (0.15 pts)")
            total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: apiVersion: v1 and kind: Secret (0.15 points)
    try:
        api_ok = parsed.get('apiVersion') == 'v1'
        kind_ok = parsed.get('kind') == 'Secret'
        if api_ok and kind_ok:
            print(f"PASS: Component 2 -- apiVersion=v1, kind=Secret (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- apiVersion={parsed.get('apiVersion')}, kind={parsed.get('kind')}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: type: Opaque (0.15 points)
    try:
        secret_type = parsed.get('type', '')
        if secret_type == 'Opaque':
            print(f"PASS: Component 3 -- type=Opaque (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- expected type=Opaque, found type={secret_type}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: data section has DB_HOST, DB_USER, DB_PASS keys (0.15 points)
    try:
        data_section = parsed.get('data', {})
        if not isinstance(data_section, dict):
            print(f"FAIL: Component 4 -- 'data' section is not a dict")
        else:
            required_keys = {'DB_HOST', 'DB_USER', 'DB_PASS'}
            present_keys = set(data_section.keys()) & required_keys
            if present_keys == required_keys:
                print(f"PASS: Component 4 -- data has DB_HOST, DB_USER, DB_PASS (0.15 pts)")
                total_score += 0.15
            else:
                missing = required_keys - present_keys
                print(f"FAIL: Component 4 -- missing keys in data: {missing}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: DB_HOST decodes to db.internal.svc (0.15 points)
    try:
        db_host_b64 = data_section.get('DB_HOST', '')
        if db_host_b64:
            decoded = base64.b64decode(db_host_b64).decode('utf-8')
            if decoded == 'db.internal.svc':
                print(f"PASS: Component 5 -- DB_HOST decodes to 'db.internal.svc' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 -- DB_HOST decodes to '{decoded}', expected 'db.internal.svc'")
        else:
            print(f"FAIL: Component 5 -- DB_HOST not found or empty in data section")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: DB_USER decodes to admin (0.10 points)
    try:
        db_user_b64 = data_section.get('DB_USER', '')
        if db_user_b64:
            decoded = base64.b64decode(db_user_b64).decode('utf-8')
            if decoded == 'admin':
                print(f"PASS: Component 6 -- DB_USER decodes to 'admin' (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 -- DB_USER decodes to '{decoded}', expected 'admin'")
        else:
            print(f"FAIL: Component 6 -- DB_USER not found or empty in data section")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: DB_PASS decodes to s3cur3P@ss (0.15 points)
    try:
        db_pass_b64 = data_section.get('DB_PASS', '')
        if db_pass_b64:
            decoded = base64.b64decode(db_pass_b64).decode('utf-8')
            if decoded == 's3cur3P@ss':
                print(f"PASS: Component 7 -- DB_PASS decodes to 's3cur3P@ss' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 7 -- DB_PASS decodes to '{decoded}', expected 's3cur3P@ss'")
        else:
            print(f"FAIL: Component 7 -- DB_PASS not found or empty in data section")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SECRET_PATH):
    print(f"File not found: {SECRET_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(SECRET_PATH)
