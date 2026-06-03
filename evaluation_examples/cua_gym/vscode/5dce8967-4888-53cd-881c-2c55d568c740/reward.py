"""
Reward Script: Configure multi-language debugging workflow in VSCode
Task ID: vscode_wf_078
Domain: vscode
Scoring:
  Component 1 (0.10): launch.json exists and is valid JSON with version 0.2.0
  Component 2 (0.20): Debug Backend config (debugpy, Python)
  Component 3 (0.20): Debug Frontend config (node, TypeScript, sourceMaps, outFiles)
  Component 4 (0.20): Debug Native config (cppdbg, GDB, miDebuggerPath)
  Component 5 (0.20): Compound 'Debug Full Stack' with backend + frontend
  Component 6 (0.10): Each individual config has correct cwd
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_078'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'project', '.vscode', 'launch.json')


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
    """Find a configuration entry by its name field."""
    for cfg in configurations:
        if cfg.get('name') == name:
            return cfg
    return None


def find_compound_by_name(compounds, name):
    """Find a compound entry by its name field."""
    for comp in compounds:
        if comp.get('name') == name:
            return comp
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
            print(f"FAIL: Component 1 -- launch.json not found at {LAUNCH_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0

        data = load_jsonc(LAUNCH_JSON_PATH)
        version = data.get('version', '')
        configs = data.get('configurations', [])
        if isinstance(configs, list) and len(configs) >= 3 and version == '0.2.0':
            print(f"PASS: Component 1 -- launch.json valid, version={version}, {len(configs)} configs (0.10 pts)")
            total_score += 0.10
        elif isinstance(configs, list) and len(configs) >= 3:
            print(f"PARTIAL: Component 1 -- launch.json valid, version={version} (expected 0.2.0), {len(configs)} configs (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 1 -- expected >= 3 configs, found {len(configs) if isinstance(configs, list) else 'N/A'}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Debug Backend config (0.20 points)
    try:
        backend_cfg = find_config_by_name(configs, 'Debug Backend')
        if backend_cfg is None:
            print("FAIL: Component 2 -- No 'Debug Backend' configuration found")
        else:
            pts = 0.0
            cfg_type = backend_cfg.get('type', '')
            # Accept debugpy or python as valid Python debug types
            if cfg_type in ('debugpy', 'python'):
                pts += 0.10
            else:
                print(f"  FAIL: Backend type={cfg_type}, expected debugpy or python")

            request = backend_cfg.get('request', '')
            program = backend_cfg.get('program', '')
            if request == 'launch' and 'backend' in program.lower() and 'app.py' in program.lower():
                pts += 0.10
            else:
                print(f"  FAIL: Backend request={request}, program={program}")

            if pts > 0:
                print(f"PASS: Component 2 -- Debug Backend: type={cfg_type}, program={program} ({pts:.2f} pts)")
            total_score += pts
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Debug Frontend config (0.20 points)
    try:
        frontend_cfg = find_config_by_name(configs, 'Debug Frontend')
        if frontend_cfg is None:
            print("FAIL: Component 3 -- No 'Debug Frontend' configuration found")
        else:
            pts = 0.0
            cfg_type = frontend_cfg.get('type', '')
            if cfg_type in ('node', 'pwa-node'):
                pts += 0.05
            else:
                print(f"  FAIL: Frontend type={cfg_type}, expected node")

            # Check sourceMaps
            if frontend_cfg.get('sourceMaps') is True:
                pts += 0.05
            else:
                print(f"  FAIL: Frontend sourceMaps={frontend_cfg.get('sourceMaps')}, expected true")

            # Check outFiles
            out_files = frontend_cfg.get('outFiles', [])
            if isinstance(out_files, list) and len(out_files) > 0:
                pts += 0.05
            else:
                print(f"  FAIL: Frontend outFiles missing or empty")

            # Check program references TypeScript or frontend
            program = frontend_cfg.get('program', '')
            if 'frontend' in program.lower() and ('index.ts' in program.lower() or 'index.js' in program.lower()):
                pts += 0.05
            else:
                print(f"  FAIL: Frontend program={program}")

            if pts > 0:
                print(f"PASS: Component 3 -- Debug Frontend: type={cfg_type}, sourceMaps={frontend_cfg.get('sourceMaps')}, outFiles={len(out_files)} ({pts:.2f} pts)")
            total_score += pts
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Debug Native config (0.20 points)
    try:
        native_cfg = find_config_by_name(configs, 'Debug Native')
        if native_cfg is None:
            print("FAIL: Component 4 -- No 'Debug Native' configuration found")
        else:
            pts = 0.0
            cfg_type = native_cfg.get('type', '')
            if cfg_type == 'cppdbg':
                pts += 0.05
            else:
                print(f"  FAIL: Native type={cfg_type}, expected cppdbg")

            mi_mode = native_cfg.get('MIMode', '')
            if mi_mode == 'gdb':
                pts += 0.05
            else:
                print(f"  FAIL: Native MIMode={mi_mode}, expected gdb")

            mi_path = native_cfg.get('miDebuggerPath', '')
            if 'gdb' in mi_path.lower():
                pts += 0.05
            else:
                print(f"  FAIL: Native miDebuggerPath={mi_path}, expected path containing gdb")

            program = native_cfg.get('program', '')
            if 'native' in program.lower() and 'lib' in program.lower():
                pts += 0.05
            else:
                print(f"  FAIL: Native program={program}")

            if pts > 0:
                print(f"PASS: Component 4 -- Debug Native: type={cfg_type}, MIMode={mi_mode}, miDebuggerPath={mi_path} ({pts:.2f} pts)")
            total_score += pts
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Compound 'Debug Full Stack' (0.20 points)
    try:
        compounds = data.get('compounds', [])
        full_stack = find_compound_by_name(compounds, 'Debug Full Stack')
        if full_stack is None:
            print("FAIL: Component 5 -- No 'Debug Full Stack' compound found")
        else:
            compound_configs = full_stack.get('configurations', [])
            has_backend = 'Debug Backend' in compound_configs
            has_frontend = 'Debug Frontend' in compound_configs

            if has_backend and has_frontend:
                print(f"PASS: Component 5 -- Debug Full Stack compound includes Backend + Frontend (0.20 pts)")
                total_score += 0.20
            elif has_backend or has_frontend:
                print(f"PARTIAL: Component 5 -- Debug Full Stack compound only has {'Backend' if has_backend else 'Frontend'} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 -- Debug Full Stack compound configs: {compound_configs}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Each config has correct cwd (0.10 points)
    try:
        pts = 0.0
        checks = [
            ('Debug Backend', 'backend'),
            ('Debug Frontend', 'frontend'),
            ('Debug Native', 'native'),
        ]
        per_check = 0.10 / 3.0

        for cfg_name, subdir in checks:
            cfg = find_config_by_name(configs, cfg_name)
            if cfg is not None:
                cwd = cfg.get('cwd', '')
                if subdir in cwd.lower():
                    pts += per_check
                else:
                    print(f"  FAIL: {cfg_name} cwd={cwd}, expected to contain '{subdir}'")
            else:
                print(f"  FAIL: {cfg_name} not found for cwd check")

        if pts > 0.09:
            print(f"PASS: Component 6 -- All configs have correct cwd ({pts:.2f} pts)")
            total_score += pts
        elif pts > 0:
            print(f"PARTIAL: Component 6 -- Some configs have correct cwd ({pts:.2f} pts)")
            total_score += pts
        else:
            print("FAIL: Component 6 -- No configs have correct cwd")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
