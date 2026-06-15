"""
Reward Script: Create a launch.json for debugging a Node.js Express server
Task ID: vscode_web_021
Domain: vscode
Scoring:
  - Component 1: launch.json exists with valid structure (0.15)
  - Component 2: Configuration name and type correct (0.20)
  - Component 3: ts-node configured via runtimeArgs or runtimeExecutable (0.20)
  - Component 4: program points to src/server.ts (0.20)
  - Component 5: Port 3000 configured (0.15)
  - Component 6: sourceMaps enabled (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_021'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'api-server', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load JSON or JSONC (with comments) from a file."""
    with open(path, 'r') as f:
        content = f.read()
    # Try plain JSON first (avoids corrupting strings with // in them)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Fallback: strip comments outside of strings
    # Remove single-line comments (only outside strings - simplified approach)
    lines = content.split('\n')
    cleaned = []
    for line in lines:
        # Only strip // comments that are NOT inside a string value
        # Simple heuristic: if the line has an even number of unescaped quotes before //, strip it
        idx = line.find('//')
        if idx >= 0:
            before = line[:idx]
            quote_count = before.count('"') - before.count('\\"')
            if quote_count % 2 == 0:
                line = before
        cleaned.append(line)
    content = '\n'.join(cleaned)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
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

    # Load and parse launch.json
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid structure with version and configurations array (0.15 points)
    try:
        has_version = data.get("version") == "0.2.0"
        has_configs = isinstance(data.get("configurations"), list) and len(data.get("configurations", [])) > 0
        if has_version and has_configs:
            print(f"PASS: Component 1 — Valid launch.json structure with version 0.2.0 and {len(data['configurations'])} config(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — version={data.get('version')}, configs={type(data.get('configurations'))}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Get the first configuration (or find the one named 'Debug Express Server')
    config = None
    configs = data.get("configurations", [])
    for c in configs:
        if isinstance(c, dict) and "Debug Express Server" in c.get("name", ""):
            config = c
            break
    if config is None and len(configs) > 0:
        config = configs[0]  # Fallback to first config

    if config is None:
        print("FAIL: No configuration found in launch.json")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Configuration name is 'Debug Express Server' and type is 'node' (0.20 points)
    try:
        name_ok = config.get("name") == "Debug Express Server"
        type_ok = config.get("type") == "node"
        if name_ok and type_ok:
            print(f"PASS: Component 2 — name='Debug Express Server', type='node' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — name='{config.get('name')}', type='{config.get('type')}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ts-node configured via runtimeArgs or runtimeExecutable (0.20 points)
    try:
        runtime_args = config.get("runtimeArgs", [])
        runtime_exec = config.get("runtimeExecutable", "")
        # Check runtimeArgs for ts-node/register pattern
        args_str = " ".join(str(a) for a in runtime_args) if isinstance(runtime_args, list) else str(runtime_args)
        has_tsnode_args = "ts-node/register" in args_str or "ts-node" in args_str
        # Check runtimeExecutable for ts-node
        has_tsnode_exec = "ts-node" in str(runtime_exec)
        if has_tsnode_args or has_tsnode_exec:
            print(f"PASS: Component 3 — ts-node configured (runtimeArgs: {has_tsnode_args}, runtimeExecutable: {has_tsnode_exec}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — ts-node not found in runtimeArgs={runtime_args} or runtimeExecutable={runtime_exec}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: program points to src/server.ts (0.20 points)
    try:
        program = config.get("program", "")
        # Accept various forms: ${workspaceFolder}/src/server.ts, ./src/server.ts, src/server.ts
        program_ok = ("src/server.ts" in program)
        if program_ok:
            print(f"PASS: Component 4 — program='{program}' points to src/server.ts (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — program='{program}' does not point to src/server.ts")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Port 3000 configured (env, args, or port field) (0.15 points)
    try:
        env_vars = config.get("env", {})
        args = config.get("args", [])
        port_field = config.get("port", None)
        config_str = json.dumps(config)

        # Check env.PORT = "3000" or "3000" in args or port=3000
        port_in_env = isinstance(env_vars, dict) and str(env_vars.get("PORT", "")) == "3000"
        port_in_args = isinstance(args, list) and any("3000" in str(a) for a in args)
        port_in_field = str(port_field) == "3000" if port_field is not None else False
        port_in_config = "3000" in config_str

        if port_in_env or port_in_args or port_in_field or port_in_config:
            print(f"PASS: Component 5 — Port 3000 configured (env:{port_in_env}, args:{port_in_args}, field:{port_in_field}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Port 3000 not found in configuration")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: sourceMaps enabled (0.10 points)
    try:
        source_maps = config.get("sourceMaps", None)
        if source_maps is True:
            print(f"PASS: Component 6 — sourceMaps=true (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — sourceMaps={source_maps}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
