"""
Reward Script: Multi-container debugging launch.json setup
Task ID: vscode_gf2_048
Domain: vscode
Scoring:
  Component 1 (0.10): launch.json exists and is valid JSON with version field
  Component 2 (0.25): Python debugpy attach config on port 5678 with pathMappings
  Component 3 (0.20): Node.js attach config on port 9229
  Component 4 (0.20): Chrome launch config on port 3000
  Component 5 (0.25): Compound "Debug Microservices" referencing all 3 configs with stopAll: true
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_048'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'microservices', '.vscode', 'launch.json')


def load_jsonc(file_path):
    """Load a JSONC file (JSON with comments). Try direct parse first, then strip comments."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Try direct JSON parse first (handles most cases)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Fallback: strip comments carefully (avoid stripping // inside strings)
    # Remove single-line comments only outside strings
    cleaned = re.sub(r'(?<!["\w:])//.*$', '', content, flags=re.MULTILINE)
    # Remove multi-line comments
    cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
    return json.loads(cleaned)


def find_config_by_criteria(configurations, criteria_fn):
    """Find a configuration matching given criteria function."""
    for cfg in configurations:
        if criteria_fn(cfg):
            return cfg
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: launch.json exists and is valid JSON with version (0.10 points)
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 1 — launch.json not found at {LAUNCH_JSON_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        data = load_jsonc(LAUNCH_JSON_PATH)
        if isinstance(data, dict) and "version" in data:
            print(f"PASS: Component 1 — launch.json exists and is valid JSON with version '{data['version']}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — launch.json missing 'version' field")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    configurations = data.get("configurations", [])
    compounds = data.get("compounds", [])

    # Component 2: Python debugpy attach config on port 5678 with pathMappings (0.25 points)
    try:
        def is_python_config(cfg):
            cfg_type = str(cfg.get("type", "")).lower()
            cfg_request = str(cfg.get("request", "")).lower()
            # Check type is debugpy or python
            if cfg_type not in ("debugpy", "python"):
                return False
            if cfg_request != "attach":
                return False
            # Check port 5678
            connect = cfg.get("connect", {})
            port = cfg.get("port", connect.get("port", None))
            if port != 5678:
                return False
            return True

        python_cfg = find_config_by_criteria(configurations, is_python_config)
        if python_cfg is None:
            print(f"FAIL: Component 2 — No Python debugpy attach config on port 5678 found")
        else:
            # Check pathMappings
            path_mappings = python_cfg.get("pathMappings", [])
            if isinstance(path_mappings, list) and len(path_mappings) > 0:
                print(f"PASS: Component 2 — Python debugpy attach on port 5678 with {len(path_mappings)} pathMapping(s) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Python config found but missing pathMappings (has: {path_mappings})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Node.js attach config on port 9229 (0.20 points)
    try:
        def is_node_config(cfg):
            cfg_type = str(cfg.get("type", "")).lower()
            cfg_request = str(cfg.get("request", "")).lower()
            if cfg_type not in ("node", "pwa-node"):
                return False
            if cfg_request != "attach":
                return False
            # Check port 9229 - can be at top level or in connect
            connect = cfg.get("connect", {})
            port = cfg.get("port", connect.get("port", None))
            if port != 9229:
                return False
            return True

        node_cfg = find_config_by_criteria(configurations, is_node_config)
        if node_cfg is None:
            print(f"FAIL: Component 3 — No Node.js attach config on port 9229 found")
        else:
            print(f"PASS: Component 3 — Node.js attach on port 9229 found (0.20 pts)")
            total_score += 0.20
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Chrome launch config for port 3000 (0.20 points)
    try:
        def is_chrome_config(cfg):
            cfg_type = str(cfg.get("type", "")).lower()
            # Accept chrome, pwa-chrome, or msedge
            if cfg_type not in ("chrome", "pwa-chrome"):
                return False
            cfg_request = str(cfg.get("request", "")).lower()
            if cfg_request != "launch":
                return False
            # Check URL contains port 3000
            url = str(cfg.get("url", ""))
            if "3000" not in url:
                return False
            return True

        chrome_cfg = find_config_by_criteria(configurations, is_chrome_config)
        if chrome_cfg is None:
            print(f"FAIL: Component 4 — No Chrome launch config for port 3000 found")
        else:
            print(f"PASS: Component 4 — Chrome launch for port 3000 found (0.20 pts)")
            total_score += 0.20
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Compound "Debug Microservices" with stopAll: true, referencing all 3 (0.25 points)
    try:
        compound = None
        for c in compounds:
            name = str(c.get("name", "")).lower()
            if "debug microservices" in name:
                compound = c
                break

        if compound is None:
            print(f"FAIL: Component 5 — No compound config named 'Debug Microservices' found")
        else:
            comp_configs = compound.get("configurations", [])
            stop_all = compound.get("stopAll", False)

            # Verify stopAll is true
            if stop_all is not True:
                print(f"FAIL: Component 5 — Compound found but stopAll is {stop_all}, expected true")
            # Verify it references at least 3 configurations
            elif len(comp_configs) < 3:
                print(f"FAIL: Component 5 — Compound found but only references {len(comp_configs)} configs, need at least 3")
            else:
                # Verify the compound references match actual config names
                config_names = [cfg.get("name", "") for cfg in configurations]
                all_referenced = all(ref in config_names for ref in comp_configs)
                if all_referenced:
                    print(f"PASS: Component 5 — Compound 'Debug Microservices' with {len(comp_configs)} configs and stopAll=true (0.25 pts)")
                    total_score += 0.25
                else:
                    missing = [ref for ref in comp_configs if ref not in config_names]
                    print(f"FAIL: Component 5 — Compound references non-existent configs: {missing}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
