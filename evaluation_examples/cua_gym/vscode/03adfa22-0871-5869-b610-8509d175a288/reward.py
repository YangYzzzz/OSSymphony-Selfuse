"""
Reward Script: Set up a Go remote debugging configuration in launch.json
Task ID: vscode_lang_019
Domain: vs_code
Scoring:
  Component 1: "Attach to Remote" config exists (0.2 pts)
  Component 2: type=go, request=attach, mode=remote (0.3 pts)
  Component 3: host=127.0.0.1, port=2345 (0.3 pts)
  Component 4: remotePath and/or substitutePath configured (0.2 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_019'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, TASK_ID, '.vscode', 'launch.json')


def load_jsonc(file_path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def find_attach_remote_config(configurations):
    """Find a configuration named 'Attach to Remote' (case-insensitive match)."""
    for cfg in configurations:
        if isinstance(cfg, dict):
            name = cfg.get('name', '')
            if isinstance(name, str) and name.lower() == 'attach to remote':
                return cfg
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load launch.json
    try:
        data = load_jsonc(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    configurations = data.get('configurations', [])
    if not isinstance(configurations, list):
        print("FAIL: 'configurations' is not a list")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: "Attach to Remote" configuration exists (0.2 points)
    try:
        remote_cfg = find_attach_remote_config(configurations)
        if remote_cfg is not None:
            print(f"PASS: Component 1 — 'Attach to Remote' configuration found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — No configuration named 'Attach to Remote' found. Names: {[c.get('name') for c in configurations if isinstance(c, dict)]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: type=go, request=attach, mode=remote (0.3 points)
    try:
        if remote_cfg is not None:
            cfg_type = remote_cfg.get('type', '')
            cfg_request = remote_cfg.get('request', '')
            cfg_mode = remote_cfg.get('mode', '')

            checks_passed = 0
            if str(cfg_type).lower() == 'go':
                checks_passed += 1
            else:
                print(f"  DETAIL: type expected 'go', found '{cfg_type}'")
            if str(cfg_request).lower() == 'attach':
                checks_passed += 1
            else:
                print(f"  DETAIL: request expected 'attach', found '{cfg_request}'")
            if str(cfg_mode).lower() == 'remote':
                checks_passed += 1
            else:
                print(f"  DETAIL: mode expected 'remote', found '{cfg_mode}'")

            if checks_passed == 3:
                print(f"PASS: Component 2 — type=go, request=attach, mode=remote all correct (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Only {checks_passed}/3 sub-checks passed")
        else:
            print(f"FAIL: Component 2 — No 'Attach to Remote' config to check")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: host=127.0.0.1, port=2345 (0.3 points)
    try:
        if remote_cfg is not None:
            cfg_host = remote_cfg.get('host', '')
            cfg_port = remote_cfg.get('port', None)

            host_ok = str(cfg_host) in ('127.0.0.1', 'localhost')
            # Accept port as int or string
            port_ok = False
            if cfg_port is not None:
                try:
                    port_ok = int(cfg_port) == 2345
                except (ValueError, TypeError):
                    pass

            if host_ok and port_ok:
                print(f"PASS: Component 3 — host={cfg_host}, port={cfg_port} correct (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — host_ok={host_ok} (got '{cfg_host}'), port_ok={port_ok} (got '{cfg_port}')")
        else:
            print(f"FAIL: Component 3 — No 'Attach to Remote' config to check")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: remotePath and/or substitutePath configured (0.2 points)
    try:
        if remote_cfg is not None:
            has_remote_path = 'remotePath' in remote_cfg and remote_cfg['remotePath']
            has_substitute_path = 'substitutePath' in remote_cfg and remote_cfg['substitutePath']

            if has_remote_path or has_substitute_path:
                details = []
                if has_remote_path:
                    details.append(f"remotePath={remote_cfg['remotePath']}")
                if has_substitute_path:
                    details.append(f"substitutePath has {len(remote_cfg['substitutePath'])} entries")
                print(f"PASS: Component 4 — Path config present: {', '.join(details)} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — Neither remotePath nor substitutePath configured")
        else:
            print(f"FAIL: Component 4 — No 'Attach to Remote' config to check")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(LAUNCH_JSON_PATH)
