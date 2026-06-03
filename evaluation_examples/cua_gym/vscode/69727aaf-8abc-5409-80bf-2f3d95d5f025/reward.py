"""
Reward Script: Set up compound debug configuration in launch.json
Task ID: vscode_py_034
Domain: vscode
Scoring:
  Component 1: launch.json exists and is valid JSON with version field (0.1 pts)
  Component 2: FastAPI Server config with module=uvicorn and correct args (0.3 pts)
  Component 3: Celery Worker config with module=celery and correct args (0.3 pts)
  Component 4: Compound configuration referencing both configs (0.3 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_034'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, TASK_ID, '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load and parse
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json is valid JSON with version field (0.1 points)
    # This is a minimal structural check; the key task-introduced change is
    # that launch.json now EXISTS (it didn't before) with proper structure.
    try:
        if isinstance(data, dict) and "version" in data:
            print(f"PASS: Component 1 — launch.json is valid with version={data['version']} (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — launch.json missing 'version' field or not a dict")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    configurations = data.get("configurations", [])

    # Component 2: FastAPI Server configuration (0.3 points)
    try:
        fastapi_config = None
        for cfg in configurations:
            name = cfg.get("name", "").lower()
            if "fastapi" in name:
                fastapi_config = cfg
                break

        if fastapi_config is None:
            print("FAIL: Component 2 — No configuration with 'FastAPI' in name found")
        else:
            sub_score = 0.0
            module_val = fastapi_config.get("module", "")
            args_val = fastapi_config.get("args", [])

            # Check module is uvicorn
            if module_val == "uvicorn":
                sub_score += 0.15
                print(f"  PASS: FastAPI module = 'uvicorn'")
            else:
                print(f"  FAIL: FastAPI module expected 'uvicorn', found '{module_val}'")

            # Check args contain main:app and --reload
            has_main_app = "main:app" in args_val
            has_reload = "--reload" in args_val
            if has_main_app and has_reload:
                sub_score += 0.15
                print(f"  PASS: FastAPI args contain 'main:app' and '--reload'")
            else:
                print(f"  FAIL: FastAPI args expected ['main:app', '--reload'], found {args_val}")

            if sub_score > 0:
                print(f"PASS: Component 2 — FastAPI Server config verified ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 — FastAPI Server config incomplete")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Celery Worker configuration (0.3 points)
    try:
        celery_config = None
        for cfg in configurations:
            name = cfg.get("name", "").lower()
            if "celery" in name:
                celery_config = cfg
                break

        if celery_config is None:
            print("FAIL: Component 3 — No configuration with 'Celery' in name found")
        else:
            sub_score = 0.0
            module_val = celery_config.get("module", "")
            args_val = celery_config.get("args", [])

            # Check module is celery
            if module_val == "celery":
                sub_score += 0.15
                print(f"  PASS: Celery module = 'celery'")
            else:
                print(f"  FAIL: Celery module expected 'celery', found '{module_val}'")

            # Check args contain worker, -A, worker
            if "worker" in args_val and "-A" in args_val:
                # Verify -A is followed by worker
                try:
                    a_idx = args_val.index("-A")
                    if a_idx + 1 < len(args_val) and args_val[a_idx + 1] == "worker":
                        sub_score += 0.15
                        print(f"  PASS: Celery args contain 'worker -A worker'")
                    else:
                        print(f"  FAIL: Celery -A flag not followed by 'worker', found {args_val}")
                except (ValueError, IndexError):
                    print(f"  FAIL: Celery args structure incorrect: {args_val}")
            else:
                print(f"  FAIL: Celery args expected ['worker', '-A', 'worker'], found {args_val}")

            if sub_score > 0:
                print(f"PASS: Component 3 — Celery Worker config verified ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 3 — Celery Worker config incomplete")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Compound configuration (0.3 points)
    try:
        compounds = data.get("compounds", [])
        if not compounds:
            print("FAIL: Component 4 — No 'compounds' array found in launch.json")
        else:
            # Find a compound that references both FastAPI and Celery configs
            matching_compound = None
            for compound in compounds:
                compound_configs = compound.get("configurations", [])
                # Check that both individual config names are referenced
                config_names_lower = [c.lower() if isinstance(c, str) else "" for c in compound_configs]
                has_fastapi_ref = any("fastapi" in n for n in config_names_lower)
                has_celery_ref = any("celery" in n for n in config_names_lower)

                if has_fastapi_ref and has_celery_ref:
                    matching_compound = compound
                    break

            if matching_compound is not None:
                print(f"PASS: Component 4 — Compound config '{matching_compound.get('name', 'unnamed')}' references both FastAPI and Celery (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 4 — No compound config references both FastAPI and Celery configurations")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
