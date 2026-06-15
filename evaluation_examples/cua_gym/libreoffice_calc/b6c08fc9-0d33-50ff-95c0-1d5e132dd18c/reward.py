"""
Reward Script: Set up VSCode C++ development environment for /home/user/projects/cpp_game/
Task ID: osworld_multi_apps_code_vscode_config_007
Domain: vs-code / os
Scoring:
  - Component 1: C/C++ extension (ms-vscode.cpptools) installed via filesystem check  0.20 pts
  - Component 2: .vscode/tasks.json with g++ build task                               0.25 pts
  - Component 3: .vscode/launch.json with gdb debug configuration                     0.25 pts
  - Component 4: .vscode/c_cpp_properties.json with system include paths              0.15 pts
  - Component 5: game binary compiled and present as valid ELF executable             0.15 pts
  Total: 1.0
"""

import os
import json

PROJECT_DIR = '/home/user/projects/cpp_game'
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
EXTENSIONS_DIR = os.path.expanduser('~/.vscode/extensions')

TASKS_JSON = os.path.join(VSCODE_DIR, 'tasks.json')
LAUNCH_JSON = os.path.join(VSCODE_DIR, 'launch.json')
CPP_PROPS_JSON = os.path.join(VSCODE_DIR, 'c_cpp_properties.json')
GAME_BINARY = os.path.join(PROJECT_DIR, 'game')


def _is_subset(expected, actual) -> bool:
    """Recursively check that expected is a subset of actual."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def verify_task():
    """
    Verify VSCode C++ development environment setup.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: project directory must exist
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: C/C++ extension (ms-vscode.cpptools) installed (0.20 points)
    # Checks the ~/.vscode/extensions/ directory for an ms-vscode.cpptools entry.
    # FAILS on initial (no extension directory) and PASSES on golden (extension installed).
    try:
        extension_found = False
        if os.path.isdir(EXTENSIONS_DIR):
            for entry in os.listdir(EXTENSIONS_DIR):
                if entry.lower().startswith('ms-vscode.cpptools'):
                    extension_found = True
                    break

        if extension_found:
            print(f"PASS: Component 1 — ms-vscode.cpptools extension found in {EXTENSIONS_DIR} (0.20 pts)")
            total_score += 0.20
        else:
            listing = os.listdir(EXTENSIONS_DIR) if os.path.isdir(EXTENSIONS_DIR) else 'dir not found'
            print(f"FAIL: Component 1 — ms-vscode.cpptools NOT found in extensions dir. Contents: {listing}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check extensions directory: {e}")

    # Component 2: .vscode/tasks.json with valid g++ build task (0.25 points)
    # Checks: file exists, has at least one task with g++ command and 'game'/'main.cpp' args,
    # with group.kind == 'build'.
    # FAILS on initial (.vscode dir absent) and PASSES on golden.
    try:
        if not os.path.isfile(TASKS_JSON):
            print(f"FAIL: Component 2 — tasks.json not found at {TASKS_JSON}")
        else:
            with open(TASKS_JSON, 'r') as f:
                tasks_data = json.load(f)

            tasks = tasks_data.get('tasks', [])
            build_task_found = False
            for task in tasks:
                cmd = task.get('command', '')
                args = task.get('args', [])
                args_str = ' '.join(str(a) for a in args)
                group = task.get('group', {})
                group_kind = group.get('kind', '') if isinstance(group, dict) else str(group)

                uses_gpp = ('g++' in cmd) or ('g++' in args_str)
                outputs_game = '-o' in args and 'game' in args
                references_main = 'main.cpp' in args
                is_build_group = group_kind == 'build'

                if uses_gpp and outputs_game and references_main and is_build_group:
                    build_task_found = True
                    break

            if build_task_found:
                print(f"PASS: Component 2 — tasks.json has valid g++ build task for game from main.cpp (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — tasks.json present but no valid g++ build task found. Tasks: {tasks}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 2 — tasks.json is invalid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: .vscode/launch.json with valid gdb debug configuration (0.25 points)
    # Checks: file exists, has a configuration with type=cppdbg, MIMode=gdb,
    # program pointing to game binary, and request=launch.
    # FAILS on initial (.vscode dir absent) and PASSES on golden.
    try:
        if not os.path.isfile(LAUNCH_JSON):
            print(f"FAIL: Component 3 — launch.json not found at {LAUNCH_JSON}")
        else:
            with open(LAUNCH_JSON, 'r') as f:
                launch_data = json.load(f)

            configurations = launch_data.get('configurations', [])
            gdb_config_found = False
            for config in configurations:
                cfg_type = config.get('type', '')
                mi_mode = config.get('MIMode', '')
                program = config.get('program', '')
                request = config.get('request', '')

                is_cppdbg = cfg_type == 'cppdbg'
                uses_gdb = mi_mode == 'gdb'
                targets_game = 'game' in program
                is_launch = request == 'launch'

                if is_cppdbg and uses_gdb and targets_game and is_launch:
                    gdb_config_found = True
                    break

            if gdb_config_found:
                print(f"PASS: Component 3 — launch.json has valid cppdbg/gdb configuration targeting game binary (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — launch.json present but no valid cppdbg/gdb config. Configs: {configurations}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 3 — launch.json is invalid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: .vscode/c_cpp_properties.json with system include paths (0.15 points)
    # Checks: file exists, has a configuration with system /usr/include entries and
    # a compilerPath pointing to g++.
    # FAILS on initial (.vscode dir absent) and PASSES on golden.
    try:
        if not os.path.isfile(CPP_PROPS_JSON):
            print(f"FAIL: Component 4 — c_cpp_properties.json not found at {CPP_PROPS_JSON}")
        else:
            with open(CPP_PROPS_JSON, 'r') as f:
                props_data = json.load(f)

            configurations = props_data.get('configurations', [])
            props_config_found = False
            for config in configurations:
                include_path = config.get('includePath', [])
                compiler_path = config.get('compilerPath', '')

                has_system_includes = any('/usr/include' in p or '/usr/lib/gcc' in p for p in include_path)
                has_gpp_compiler = bool(compiler_path) and 'g++' in compiler_path

                if has_system_includes and has_gpp_compiler:
                    props_config_found = True
                    break

            if props_config_found:
                print(f"PASS: Component 4 — c_cpp_properties.json has system include paths and g++ compiler path (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — c_cpp_properties.json present but missing include paths or g++ compiler. Configs: {configurations}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 4 — c_cpp_properties.json is invalid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: game binary compiled and present as valid ELF executable (0.15 points)
    # Checks: binary file exists at expected path AND starts with ELF magic bytes AND is executable.
    # FAILS on initial (no game file in project dir) and PASSES on golden (game built by g++).
    try:
        if not os.path.isfile(GAME_BINARY):
            print(f"FAIL: Component 5 — game binary not found at {GAME_BINARY}")
        else:
            with open(GAME_BINARY, 'rb') as f:
                magic = f.read(4)
            is_elf = magic == b'\x7fELF'
            is_executable = os.access(GAME_BINARY, os.X_OK)

            if is_elf and is_executable:
                print(f"PASS: Component 5 — game binary exists and is a valid ELF executable (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — game file exists but is not a valid ELF executable. "
                      f"ELF={is_elf}, executable={is_executable}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
