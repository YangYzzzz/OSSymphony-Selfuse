"""
Reward Script: Protobuf/gRPC VSCode Workflow Setup
Task ID: vscode_wf_085
Domain: vscode
Scoring:
  Component 1 (0.15): Extension zxh404.vscode-proto3 installed
  Component 2 (0.25): proto/service.proto with syntax=proto3, messages, service
  Component 3 (0.20): .vscode/settings.json with proto3-related settings
  Component 4 (0.20): .vscode/tasks.json with proto-compile, proto-lint, proto-format
  Component 5 (0.10): .vscode/launch.json with Python debug config for gRPC server
  Component 6 (0.10): Generated Python stubs path in settings
"""

import os
import json
import re
import glob as glob_mod

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_085'


def load_json_file(path):
    """Load a JSON file, stripping JSONC comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip // comments (JSONC support)
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task():
    """
    Verify protobuf/gRPC workflow setup with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extension zxh404.vscode-proto3 is installed (0.15 points)
    # Check by looking at the extensions directory on disk
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        ext_installed = False
        if os.path.isdir(ext_dir):
            for entry in os.listdir(ext_dir):
                if entry.lower().startswith('zxh404.vscode-proto3'):
                    ext_installed = True
                    break
        if ext_installed:
            print(f"PASS: Component 1 — zxh404.vscode-proto3 extension installed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — zxh404.vscode-proto3 extension not found in {ext_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: proto/service.proto with syntax=proto3, message and service defs (0.25 points)
    try:
        proto_path = os.path.join(PROJECT, 'proto', 'service.proto')
        if not os.path.isfile(proto_path):
            print(f"FAIL: Component 2 — {proto_path} does not exist")
        else:
            with open(proto_path, 'r') as f:
                proto_content = f.read()

            comp2_score = 0.0

            # Check syntax = "proto3"
            if re.search(r'syntax\s*=\s*"proto3"', proto_content):
                comp2_score += 0.08
                print(f"  PASS: Component 2a — syntax = proto3 found")
            else:
                print(f"  FAIL: Component 2a — syntax = proto3 not found")

            # Check for message definitions (at least 2)
            messages = re.findall(r'\bmessage\s+\w+\s*\{', proto_content)
            if len(messages) >= 2:
                comp2_score += 0.09
                print(f"  PASS: Component 2b — {len(messages)} message definitions found")
            else:
                print(f"  FAIL: Component 2b — expected >=2 message definitions, found {len(messages)}")

            # Check for service definition with rpc methods
            services = re.findall(r'\bservice\s+\w+\s*\{', proto_content)
            rpcs = re.findall(r'\brpc\s+\w+\s*\(', proto_content)
            if len(services) >= 1 and len(rpcs) >= 1:
                comp2_score += 0.08
                print(f"  PASS: Component 2c — {len(services)} service(s) with {len(rpcs)} rpc method(s)")
            else:
                print(f"  FAIL: Component 2c — expected service+rpc, found {len(services)} services, {len(rpcs)} rpcs")

            total_score += comp2_score
            print(f"PASS: Component 2 — proto/service.proto verified ({comp2_score:.2f} pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: .vscode/settings.json with proto3-related settings (0.20 points)
    try:
        settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
        if not os.path.isfile(settings_path):
            print(f"FAIL: Component 3 — {settings_path} does not exist")
        else:
            settings = load_json_file(settings_path)
            comp3_score = 0.0

            # Check proto3-related settings: [proto3] section or proto3 file association
            has_proto3_section = "[proto3]" in settings
            has_proto_assoc = False
            fa = settings.get("files.associations", {})
            if isinstance(fa, dict) and fa.get("*.proto", "").lower() == "proto3":
                has_proto_assoc = True

            if has_proto3_section or has_proto_assoc:
                comp3_score += 0.10
                print(f"  PASS: Component 3a — proto3 language/formatting settings found")
            else:
                print(f"  FAIL: Component 3a — no proto3 language section or file association")

            # Check protoc path or compile settings
            has_protoc = False
            if "protoc" in settings or "proto3.path.protoc" in settings:
                has_protoc = True
            if has_protoc:
                comp3_score += 0.10
                print(f"  PASS: Component 3b — protoc configuration found in settings")
            else:
                print(f"  FAIL: Component 3b — no protoc configuration in settings")

            total_score += comp3_score
            print(f"PASS: Component 3 — settings.json verified ({comp3_score:.2f} pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: .vscode/tasks.json with proto-compile, proto-lint, proto-format (0.20 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if not os.path.isfile(tasks_path):
            print(f"FAIL: Component 4 — {tasks_path} does not exist")
        else:
            tasks_data = load_json_file(tasks_path)
            tasks_list = tasks_data.get("tasks", [])
            task_labels = [t.get("label", "").lower() for t in tasks_list]

            comp4_score = 0.0
            required_tasks = ["proto-compile", "proto-lint", "proto-format"]
            per_task_pts = round(0.20 / len(required_tasks), 4)

            for req_task in required_tasks:
                if any(req_task in label for label in task_labels):
                    comp4_score += per_task_pts
                    print(f"  PASS: Component 4 — task '{req_task}' found")
                else:
                    print(f"  FAIL: Component 4 — task '{req_task}' not found in labels: {task_labels}")

            total_score += comp4_score
            print(f"PASS: Component 4 — tasks.json verified ({comp4_score:.4f} pts)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: .vscode/launch.json with Python debug config for gRPC server (0.10 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if not os.path.isfile(launch_path):
            print(f"FAIL: Component 5 — {launch_path} does not exist")
        else:
            launch_data = load_json_file(launch_path)
            configs = launch_data.get("configurations", [])
            comp5_score = 0.0

            # Look for a Python debug config that references gRPC or server
            for cfg in configs:
                cfg_type = str(cfg.get("type", "")).lower()
                cfg_request = str(cfg.get("request", "")).lower()
                cfg_program = str(cfg.get("program", "")).lower()
                cfg_name = str(cfg.get("name", "")).lower()

                is_python = cfg_type in ("python", "debugpy")
                is_launch = cfg_request == "launch"
                refs_server = "server" in cfg_program or "grpc" in cfg_name or "server" in cfg_name

                if is_python and is_launch and refs_server:
                    comp5_score = 0.10
                    print(f"  PASS: Component 5 — Python debug config for gRPC server found: '{cfg.get('name')}'")
                    break

            if comp5_score == 0.0:
                print(f"  FAIL: Component 5 — no Python launch config referencing gRPC/server found")

            total_score += comp5_score
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Generated Python stubs path configured in settings (0.10 points)
    try:
        settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
        if not os.path.isfile(settings_path):
            print(f"FAIL: Component 6 — settings.json does not exist")
        else:
            settings = load_json_file(settings_path)
            comp6_score = 0.0

            # Check python.analysis.extraPaths or python.autoComplete.extraPaths
            # or protoc options referencing generated output path
            extra_paths = settings.get("python.analysis.extraPaths", [])
            autocomplete_paths = settings.get("python.autoComplete.extraPaths", [])
            protoc_cfg = settings.get("protoc", {})
            protoc_options = protoc_cfg.get("options", []) if isinstance(protoc_cfg, dict) else []

            has_generated_path = False
            # Check if any path references a generated stubs directory
            for p in extra_paths + autocomplete_paths:
                if "generated" in str(p).lower() or "stubs" in str(p).lower() or "proto" in str(p).lower():
                    has_generated_path = True
                    break

            # Also check protoc options for python_out
            if not has_generated_path:
                for opt in protoc_options:
                    if "--python_out" in str(opt) or "--grpc_python_out" in str(opt):
                        has_generated_path = True
                        break

            if has_generated_path:
                comp6_score = 0.10
                print(f"  PASS: Component 6 — generated Python stubs path configured")
            else:
                print(f"  FAIL: Component 6 — no generated stubs path found in settings")

            total_score += comp6_score
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
