"""
Reward Script: gRPC UserService protobuf project setup
Task ID: vscode_gf4_059
Domain: vscode
Scoring:
  C1: user.proto defines UserService with 6 RPCs including streaming (0.20)
  C2: Generated Python protobuf files exist (0.10)
  C3: server.py implements UserServiceServicer with all RPCs (0.20)
  C4: client.py exists and demonstrates RPCs (0.10)
  C5: Tests use grpc.testing / grpc_testing (0.15)
  C6: .vscode/tasks.json has protoc and server tasks (0.10)
  C7: venv with required packages installed (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_059'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-protocol-buffer')


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # Component 1: user.proto defines UserService with 6 RPCs (0.20 points)
    try:
        proto_path = os.path.join(PROJECT, 'protos', 'user.proto')
        if not os.path.isfile(proto_path):
            print("FAIL: Component 1 -- protos/user.proto does not exist")
        else:
            with open(proto_path, 'r') as f:
                proto_content = f.read()

            # Check service definition exists
            has_service = 'service UserService' in proto_content
            if not has_service:
                print("FAIL: Component 1 -- No 'service UserService' found in user.proto")
            else:
                # Check for the 6 required RPCs
                required_rpcs = ['CreateUser', 'GetUser', 'ListUsers', 'UpdateUser', 'DeleteUser', 'SearchUsers']
                found_rpcs = []
                for rpc_name in required_rpcs:
                    # Match rpc <name> pattern
                    if re.search(r'rpc\s+' + rpc_name + r'\s*\(', proto_content):
                        found_rpcs.append(rpc_name)

                rpc_count = len(found_rpcs)
                missing = set(required_rpcs) - set(found_rpcs)

                # Check streaming types
                has_server_streaming = bool(re.search(r'rpc\s+ListUsers\s*\([^)]*\)\s*returns\s*\(\s*stream\b', proto_content))
                has_bidi_streaming = bool(
                    re.search(r'rpc\s+SearchUsers\s*\(\s*stream\b', proto_content)
                    and re.search(r'rpc\s+SearchUsers\s*\([^)]*\)\s*returns\s*\(\s*stream\b', proto_content)
                )

                sub_score = 0.0
                if rpc_count >= 6:
                    sub_score += 0.12
                elif rpc_count >= 4:
                    sub_score += 0.06
                if has_server_streaming:
                    sub_score += 0.04
                if has_bidi_streaming:
                    sub_score += 0.04

                if sub_score > 0:
                    total_score += sub_score
                    print(f"PASS: Component 1 -- user.proto has {rpc_count}/6 RPCs, server_streaming={has_server_streaming}, bidi_streaming={has_bidi_streaming} ({sub_score:.2f} pts)")
                    if missing:
                        print(f"  Missing RPCs: {missing}")
                else:
                    print(f"FAIL: Component 1 -- Only {rpc_count}/6 RPCs found, streaming checks failed")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Generated Python protobuf files exist (0.10 points)
    try:
        gen_dir = os.path.join(PROJECT, 'src', 'generated')
        pb2_path = os.path.join(gen_dir, 'user_pb2.py')
        pb2_grpc_path = os.path.join(gen_dir, 'user_pb2_grpc.py')

        has_pb2 = os.path.isfile(pb2_path)
        has_grpc = os.path.isfile(pb2_grpc_path)

        sub_score = 0.0
        if has_pb2:
            # Verify it's a real generated file, not empty
            with open(pb2_path, 'r') as f:
                content = f.read()
            if len(content) > 100 and ('DESCRIPTOR' in content or 'descriptor' in content or 'proto' in content.lower()):
                sub_score += 0.05
            else:
                print(f"FAIL: Component 2 -- user_pb2.py exists but appears empty or invalid (len={len(content)})")

        if has_grpc:
            with open(pb2_grpc_path, 'r') as f:
                content = f.read()
            if len(content) > 100 and 'UserService' in content:
                sub_score += 0.05
            else:
                print(f"FAIL: Component 2 -- user_pb2_grpc.py exists but appears invalid")

        if sub_score > 0:
            total_score += sub_score
            print(f"PASS: Component 2 -- Generated files: pb2={has_pb2}, pb2_grpc={has_grpc} ({sub_score:.2f} pts)")
        else:
            print(f"FAIL: Component 2 -- Generated files missing: pb2={has_pb2}, pb2_grpc={has_grpc}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: server.py implements UserServiceServicer with all RPCs (0.20 points)
    try:
        server_path = os.path.join(PROJECT, 'src', 'server.py')
        if not os.path.isfile(server_path):
            print("FAIL: Component 3 -- src/server.py does not exist")
        else:
            with open(server_path, 'r') as f:
                server_content = f.read()

            # Check for servicer class
            has_servicer_class = bool(re.search(r'class\s+\w*UserService\w*Servicer', server_content))

            # Check for RPC method implementations
            rpc_methods = ['CreateUser', 'GetUser', 'ListUsers', 'UpdateUser', 'DeleteUser', 'SearchUsers']
            implemented = []
            for method in rpc_methods:
                if re.search(r'def\s+' + method + r'\s*\(self', server_content):
                    implemented.append(method)

            # Check for in-memory storage (dict)
            has_dict_storage = bool(re.search(r'self\.\w+\s*=\s*\{\}', server_content) or 'dict()' in server_content)

            # Check for grpc import
            has_grpc_import = 'import grpc' in server_content

            sub_score = 0.0
            impl_count = len(implemented)
            if has_servicer_class and has_grpc_import:
                if impl_count >= 6:
                    sub_score = 0.14
                elif impl_count >= 4:
                    sub_score = 0.08
                elif impl_count >= 2:
                    sub_score = 0.04

                if has_dict_storage:
                    sub_score += 0.06
                else:
                    sub_score += 0.02  # partial credit if storage exists but different form

            if sub_score > 0:
                total_score += sub_score
                print(f"PASS: Component 3 -- server.py: servicer_class={has_servicer_class}, {impl_count}/6 RPCs, dict_storage={has_dict_storage} ({sub_score:.2f} pts)")
            else:
                print(f"FAIL: Component 3 -- server.py: servicer_class={has_servicer_class}, grpc={has_grpc_import}, {impl_count}/6 RPCs")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: client.py exists and demonstrates RPCs (0.10 points)
    try:
        client_path = os.path.join(PROJECT, 'src', 'client.py')
        if not os.path.isfile(client_path):
            print("FAIL: Component 4 -- src/client.py does not exist")
        else:
            with open(client_path, 'r') as f:
                client_content = f.read()

            has_grpc = 'import grpc' in client_content
            has_stub = 'UserServiceStub' in client_content

            # Check for usage of multiple RPCs
            rpc_calls = ['CreateUser', 'GetUser', 'ListUsers', 'UpdateUser', 'DeleteUser', 'SearchUsers']
            called = [r for r in rpc_calls if re.search(r'stub\.' + r + r'\s*\(', client_content) or re.search(r'\.' + r + r'\s*\(', client_content)]

            sub_score = 0.0
            if has_grpc and has_stub:
                if len(called) >= 4:
                    sub_score = 0.10
                elif len(called) >= 2:
                    sub_score = 0.05
                else:
                    sub_score = 0.02

            if sub_score > 0:
                total_score += sub_score
                print(f"PASS: Component 4 -- client.py: stub={has_stub}, {len(called)}/6 RPCs called ({sub_score:.2f} pts)")
            else:
                print(f"FAIL: Component 4 -- client.py: grpc={has_grpc}, stub={has_stub}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Tests use grpc.testing / grpc_testing (0.15 points)
    try:
        # Find test files
        tests_dir = os.path.join(PROJECT, 'tests')
        test_files = []
        if os.path.isdir(tests_dir):
            for fname in os.listdir(tests_dir):
                if fname.startswith('test') and fname.endswith('.py'):
                    test_files.append(os.path.join(tests_dir, fname))

        # Also check root for test files
        for fname in os.listdir(PROJECT):
            if fname.startswith('test') and fname.endswith('.py'):
                test_files.append(os.path.join(PROJECT, fname))

        if not test_files:
            print("FAIL: Component 5 -- No test files found")
        else:
            test_contents = []
            for tf in test_files:
                with open(tf, 'r') as f:
                    test_contents.append(f.read())

            any_grpc_testing = any('grpc_testing' in c or 'grpc.testing' in c for c in test_contents)
            any_test_class = any(re.search(r'class\s+\w*Test\w*', c) or 'def test_' in c for c in test_contents)

            sub_score = 0.0
            if any_grpc_testing and any_test_class:
                sub_score = 0.15
            elif any_test_class:
                sub_score = 0.05  # tests exist but don't use grpc_testing

            if sub_score > 0:
                total_score += sub_score
                print(f"PASS: Component 5 -- Tests: {len(test_files)} file(s), grpc_testing={any_grpc_testing}, test_class={any_test_class} ({sub_score:.2f} pts)")
            else:
                print(f"FAIL: Component 5 -- Tests exist but grpc_testing={any_grpc_testing}, test_class={any_test_class}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: .vscode/tasks.json with protoc and server tasks (0.10 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if not os.path.isfile(tasks_path):
            print("FAIL: Component 6 -- .vscode/tasks.json does not exist")
        else:
            with open(tasks_path, 'r') as f:
                # Handle JSONC (strip comments)
                content = f.read()
                content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                tasks_config = json.loads(content_clean)

            tasks_list = tasks_config.get('tasks', [])
            labels = [t.get('label', '').lower() for t in tasks_list]

            # Check for protoc compilation task
            has_protoc = any(
                'protoc' in (t.get('label', '').lower() + ' ' + str(t.get('command', '')).lower() + ' ' + ' '.join(str(a) for a in t.get('args', [])).lower())
                or 'proto' in (t.get('label', '').lower() + ' ' + str(t.get('command', '')).lower() + ' ' + ' '.join(str(a) for a in t.get('args', [])).lower())
                or 'grpc_tools.protoc' in (t.get('label', '').lower() + ' ' + str(t.get('command', '')).lower() + ' ' + ' '.join(str(a) for a in t.get('args', [])).lower())
                for t in tasks_list
            )

            # Check for server start task
            has_server = any(
                'server' in (t.get('label', '').lower() + ' ' + str(t.get('command', '')).lower() + ' ' + ' '.join(str(a) for a in t.get('args', [])).lower())
                for t in tasks_list
            )

            sub_score = 0.0
            if has_protoc:
                sub_score += 0.05
            if has_server:
                sub_score += 0.05

            if sub_score > 0:
                total_score += sub_score
                print(f"PASS: Component 6 -- tasks.json: protoc_task={has_protoc}, server_task={has_server}, {len(tasks_list)} task(s) ({sub_score:.2f} pts)")
            else:
                print(f"FAIL: Component 6 -- tasks.json: protoc_task={has_protoc}, server_task={has_server}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: venv with required packages (0.15 points)
    try:
        venv_dir = os.path.join(PROJECT, 'venv')
        if not os.path.isdir(venv_dir):
            print("FAIL: Component 7 -- venv/ directory does not exist")
        else:
            # Check for required packages by looking at site-packages dist-info dirs
            site_packages = None
            lib_dir = os.path.join(venv_dir, 'lib')
            if os.path.isdir(lib_dir):
                for d in os.listdir(lib_dir):
                    sp = os.path.join(lib_dir, d, 'site-packages')
                    if os.path.isdir(sp):
                        site_packages = sp
                        break

            if not site_packages:
                print("FAIL: Component 7 -- Cannot find site-packages in venv")
            else:
                installed = os.listdir(site_packages)
                installed_lower = [x.lower() for x in installed]

                required_pkgs = {
                    'grpcio': False,
                    'grpcio-tools': False,
                    'protobuf': False,
                    'pytest': False,
                    'grpcio-testing': False,
                }

                for pkg_name in required_pkgs:
                    # Look for dist-info with package name
                    normalized = pkg_name.replace('-', '_').replace('.', '_').lower()
                    alt_normalized = pkg_name.replace('_', '-').lower()
                    for item in installed_lower:
                        item_clean = item.replace('-', '_').replace('.', '_').lower()
                        if item_clean.startswith(normalized) and ('dist-info' in item.lower() or 'dist_info' in item.lower()):
                            required_pkgs[pkg_name] = True
                            break
                        if item.lower().startswith(alt_normalized) and ('dist-info' in item.lower()):
                            required_pkgs[pkg_name] = True
                            break

                found_count = sum(1 for v in required_pkgs.values() if v)
                missing_pkgs = [k for k, v in required_pkgs.items() if not v]

                sub_score = 0.0
                if found_count >= 5:
                    sub_score = 0.15
                elif found_count >= 3:
                    sub_score = 0.08
                elif found_count >= 1:
                    sub_score = 0.04

                if sub_score > 0:
                    total_score += sub_score
                    print(f"PASS: Component 7 -- venv: {found_count}/5 required packages installed ({sub_score:.2f} pts)")
                    if missing_pkgs:
                        print(f"  Missing: {missing_pkgs}")
                else:
                    print(f"FAIL: Component 7 -- venv: {found_count}/5 packages, missing: {missing_pkgs}")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
