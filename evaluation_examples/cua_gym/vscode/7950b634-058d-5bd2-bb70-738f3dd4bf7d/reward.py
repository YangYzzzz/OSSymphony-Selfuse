"""
Reward Script: VSCode launch.json compound config + email regex bug fix
Task ID: vscode_gf6_013
Domain: vscode
Scoring:
  Component 1 (0.15): .vscode/launch.json exists and is valid JSON with configurations array
  Component 2 (0.20): 'Launch Server' config with NODE_ENV=development env
  Component 3 (0.15): 'Debug Tests' config running jest --runInBand
  Component 4 (0.15): 'Attach to Process' config with request:attach and port:9229
  Component 5 (0.15): 'Full Stack Debug' compound referencing Launch Server and Debug Tests
  Component 6 (0.20): Email regex in validator.js fixed to accept plus-sign emails
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'node-debug')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')
VALIDATOR_PATH = os.path.join(PROJECT_DIR, 'src', 'middleware', 'validator.js')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def find_config_by_name(configurations, name):
    """Find a configuration object by its 'name' field (case-insensitive)."""
    for cfg in configurations:
        if isinstance(cfg, dict) and cfg.get('name', '').lower() == name.lower():
            return cfg
    return None


def verify_task():
    total_score = 0.0

    # =========================================================================
    # Component 1: launch.json exists and is valid JSON with configurations (0.15)
    # =========================================================================
    launch_data = None
    configurations = []
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 1 — launch.json not found at {LAUNCH_JSON_PATH}")
        else:
            launch_data = load_jsonc(LAUNCH_JSON_PATH)
            configurations = launch_data.get('configurations', [])
            if isinstance(configurations, list) and len(configurations) >= 3:
                print(f"PASS: Component 1 — launch.json valid with {len(configurations)} configurations (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Expected >= 3 configurations, found {len(configurations) if isinstance(configurations, list) else 'non-list'}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if launch_data is None:
        # Cannot proceed with launch.json checks if file failed to load
        print("FAIL: Components 2-5 skipped — launch.json not available")
    else:
        # =========================================================================
        # Component 2: 'Launch Server' with NODE_ENV=development (0.20)
        # =========================================================================
        try:
            cfg = find_config_by_name(configurations, 'Launch Server')
            if cfg is None:
                print("FAIL: Component 2 — 'Launch Server' configuration not found")
            else:
                env = cfg.get('env', {})
                node_env_val = env.get('NODE_ENV', None)
                if node_env_val == 'development':
                    print(f"PASS: Component 2 — 'Launch Server' has NODE_ENV=development (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 2 — 'Launch Server' NODE_ENV expected 'development', found '{node_env_val}'")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")

        # =========================================================================
        # Component 3: 'Debug Tests' running jest --runInBand (0.15)
        # =========================================================================
        try:
            cfg = find_config_by_name(configurations, 'Debug Tests')
            if cfg is None:
                print("FAIL: Component 3 — 'Debug Tests' configuration not found")
            else:
                # Check that jest and --runInBand are referenced somewhere in the config
                # Could be in program, runtimeExecutable, args, etc.
                cfg_str = json.dumps(cfg).lower()
                has_jest = 'jest' in cfg_str
                has_run_in_band = '--runinband' in cfg_str
                if has_jest and has_run_in_band:
                    print(f"PASS: Component 3 — 'Debug Tests' references jest with --runInBand (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 3 — 'Debug Tests' missing jest={has_jest}, --runInBand={has_run_in_band}")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")

        # =========================================================================
        # Component 4: 'Attach to Process' with request:attach, port:9229 (0.15)
        # =========================================================================
        try:
            cfg = find_config_by_name(configurations, 'Attach to Process')
            if cfg is None:
                print("FAIL: Component 4 — 'Attach to Process' configuration not found")
            else:
                req = cfg.get('request', '')
                port = cfg.get('port', None)
                if req == 'attach' and port == 9229:
                    print(f"PASS: Component 4 — 'Attach to Process' has request=attach, port=9229 (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — request='{req}' (expected 'attach'), port={port} (expected 9229)")
        except Exception as e:
            print(f"ERROR: Component 4 — {e}")

        # =========================================================================
        # Component 5: 'Full Stack Debug' compound (0.15)
        # =========================================================================
        try:
            compounds = launch_data.get('compounds', [])
            fsd = None
            for c in compounds:
                if isinstance(c, dict) and c.get('name', '').lower() == 'full stack debug':
                    fsd = c
                    break
            if fsd is None:
                print("FAIL: Component 5 — 'Full Stack Debug' compound not found")
            else:
                refs = [r.lower() if isinstance(r, str) else '' for r in fsd.get('configurations', [])]
                has_server = 'launch server' in refs
                has_tests = 'debug tests' in refs
                if has_server and has_tests:
                    print(f"PASS: Component 5 — 'Full Stack Debug' compound references Launch Server and Debug Tests (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 5 — compound configs={fsd.get('configurations', [])}, missing server={not has_server}, tests={not has_tests}")
        except Exception as e:
            print(f"ERROR: Component 5 — {e}")

    # =========================================================================
    # Component 6: Email regex fixed to accept plus signs (0.20)
    # =========================================================================
    try:
        if not os.path.exists(VALIDATOR_PATH):
            print(f"FAIL: Component 6 — validator.js not found at {VALIDATOR_PATH}")
        else:
            with open(VALIDATOR_PATH, 'r') as f:
                content = f.read()

            # Extract the email regex pattern from the file
            # Look for a regex that validates emails
            regex_match = re.search(r'const\s+emailRegex\s*=\s*/(.+?)/', content)
            if regex_match is None:
                # Try alternative patterns
                regex_match = re.search(r'emailRegex\s*=\s*/(.+?)/', content)

            if regex_match:
                regex_pattern = regex_match.group(1)
                # The fixed regex should include + in the character class before @
                # The buggy regex has [a-zA-Z0-9._%-] (no +), the fixed one has [a-zA-Z0-9._%+-] (with +)
                # Check if the character class before @ contains +
                char_class_match = re.search(r'\[([^\]]+)\]', regex_pattern)
                if char_class_match:
                    char_class = char_class_match.group(1)
                    if '+' in char_class:
                        # Double check: test the regex functionally
                        try:
                            full_pattern = regex_match.group(0).replace('/', '')
                            # Actually use the JS-compatible regex in Python
                            js_regex = re.compile(regex_pattern)
                            test_email = 'user+tag@example.com'
                            if js_regex.match(test_email):
                                print(f"PASS: Component 6 — Email regex accepts plus-sign emails (0.20 pts)")
                                total_score += 0.20
                            else:
                                print(f"FAIL: Component 6 — Regex has + in char class but doesn't match 'user+tag@example.com'")
                        except re.error:
                            # If Python can't parse the JS regex, just check char class
                            print(f"PASS: Component 6 — Email regex char class includes + (0.20 pts)")
                            total_score += 0.20
                    else:
                        print(f"FAIL: Component 6 — Email regex char class missing +: [{char_class}]")
                else:
                    print(f"FAIL: Component 6 — Could not find character class in regex: {regex_pattern}")
            else:
                print(f"FAIL: Component 6 — Could not extract emailRegex from validator.js")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    # Round to 2 decimal places to avoid float issues
    final_score = round(final_score, 2)
    print(f"\nScore: {round(total_score, 2)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
