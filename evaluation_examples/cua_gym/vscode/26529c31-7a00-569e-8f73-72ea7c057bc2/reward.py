"""
Reward Script: gRPC-Gateway setup for Go project in VSCode
Task ID: vscode_gf6_091
Domain: vscode
Scoring:
  C1: go.mod has grpc-gateway/v2 dependency (0.15)
  C2: proto/user.proto has google.api.http annotations for all 3 RPCs (0.20)
  C3: buf.gen.yaml exists with go, go-grpc, grpc-gateway plugins (0.15)
  C4: cmd/gateway/main.go exists with gRPC + HTTP gateway setup (0.20)
  C5: Makefile has proto-gen, run-grpc, run-gateway targets (0.15)
  C6: .vscode/tasks.json has 3 Makefile tasks (0.15)
"""

import os
import re
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-grpc-gateway')


def verify_task():
    total_score = 0.0

    # Component 1: go.mod has grpc-gateway/v2 dependency (0.15 points)
    try:
        go_mod_path = os.path.join(PROJECT, 'go.mod')
        with open(go_mod_path, 'r') as f:
            go_mod_content = f.read()
        if 'grpc-ecosystem/grpc-gateway/v2' in go_mod_content:
            print(f"PASS: Component 1 — go.mod contains grpc-gateway/v2 dependency (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — go.mod does not contain grpc-gateway/v2 dependency")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: proto/user.proto has google.api.http annotations for all 3 RPCs (0.20 points)
    try:
        proto_path = os.path.join(PROJECT, 'proto', 'user.proto')
        with open(proto_path, 'r') as f:
            proto_content = f.read()

        # Check for import of annotations.proto
        has_import = 'google/api/annotations.proto' in proto_content

        # Check for HTTP annotations on each RPC
        # GetUser -> GET /v1/users/{id}
        has_get_user = bool(re.search(r'rpc\s+GetUser\b.*?\{[^}]*get\s*:\s*"/v1/users/\{id\}"', proto_content, re.DOTALL))
        # ListUsers -> GET /v1/users
        has_list_users = bool(re.search(r'rpc\s+ListUsers\b.*?\{[^}]*get\s*:\s*"/v1/users"', proto_content, re.DOTALL))
        # CreateUser -> POST /v1/users
        has_create_user = bool(re.search(r'rpc\s+CreateUser\b.*?\{[^}]*post\s*:\s*"/v1/users"', proto_content, re.DOTALL))

        annotation_count = sum([has_get_user, has_list_users, has_create_user])

        if has_import and annotation_count == 3:
            print(f"PASS: Component 2 — proto has import + all 3 HTTP annotations (0.20 pts)")
            total_score += 0.20
        elif has_import and annotation_count >= 1:
            partial = round(0.05 + 0.05 * annotation_count, 2)
            print(f"PARTIAL: Component 2 — import present, {annotation_count}/3 annotations ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — import={has_import}, annotations={annotation_count}/3 (get_user={has_get_user}, list={has_list_users}, create={has_create_user})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: buf.gen.yaml exists with go, go-grpc, grpc-gateway plugins (0.15 points)
    try:
        buf_path = os.path.join(PROJECT, 'buf.gen.yaml')
        with open(buf_path, 'r') as f:
            buf_content = f.read()

        # Check for all 3 plugin types
        has_go_plugin = bool(re.search(r'plugin:\s*\bgo\b', buf_content))
        has_go_grpc_plugin = bool(re.search(r'plugin:\s*go-grpc', buf_content))
        has_gw_plugin = bool(re.search(r'plugin:\s*grpc-gateway', buf_content))

        if has_go_plugin and has_go_grpc_plugin and has_gw_plugin:
            print(f"PASS: Component 3 — buf.gen.yaml has all 3 plugins (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — go={has_go_plugin}, go-grpc={has_go_grpc_plugin}, grpc-gateway={has_gw_plugin}")
    except FileNotFoundError:
        print(f"FAIL: Component 3 — buf.gen.yaml not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: cmd/gateway/main.go exists with gRPC server + HTTP gateway (0.20 points)
    try:
        gw_path = os.path.join(PROJECT, 'cmd', 'gateway', 'main.go')
        with open(gw_path, 'r') as f:
            gw_content = f.read()

        checks = {
            'runtime.NewServeMux': 'runtime.NewServeMux()' in gw_content or 'runtime.NewServeMux(' in gw_content,
            'RegisterUserServiceHandler': 'RegisterUserServiceHandler' in gw_content,
            'grpc_server_9090': bool(re.search(r'["\']:?9090["\']?', gw_content)),
            'http_server_8080': bool(re.search(r'["\']:?8080["\']?', gw_content)),
            'net.Listen': 'net.Listen' in gw_content,
            'grpc.NewServer': 'grpc.NewServer()' in gw_content or 'grpc.NewServer(' in gw_content,
        }

        passed = sum(checks.values())
        total_checks = len(checks)

        if passed >= 5:
            print(f"PASS: Component 4 — gateway main.go has {passed}/{total_checks} key elements (0.20 pts)")
            total_score += 0.20
        elif passed >= 3:
            partial = round(0.10 * (passed / total_checks) * 2, 2)
            partial = min(partial, 0.15)
            print(f"PARTIAL: Component 4 — {passed}/{total_checks} checks passed ({partial} pts)")
            for k, v in checks.items():
                print(f"  {k}: {'PASS' if v else 'FAIL'}")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — only {passed}/{total_checks} checks passed")
            for k, v in checks.items():
                print(f"  {k}: {'PASS' if v else 'FAIL'}")
    except FileNotFoundError:
        print(f"FAIL: Component 4 — cmd/gateway/main.go not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Makefile has proto-gen, run-grpc, run-gateway targets (0.15 points)
    try:
        mk_path = os.path.join(PROJECT, 'Makefile')
        with open(mk_path, 'r') as f:
            mk_content = f.read()

        has_proto_gen = bool(re.search(r'^proto-gen\s*:', mk_content, re.MULTILINE))
        has_run_grpc = bool(re.search(r'^run-grpc\s*:', mk_content, re.MULTILINE))
        has_run_gateway = bool(re.search(r'^run-gateway\s*:', mk_content, re.MULTILINE))

        if has_proto_gen and has_run_grpc and has_run_gateway:
            print(f"PASS: Component 5 — Makefile has all 3 targets (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — proto-gen={has_proto_gen}, run-grpc={has_run_grpc}, run-gateway={has_run_gateway}")
    except FileNotFoundError:
        print(f"FAIL: Component 5 — Makefile not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/tasks.json has 3 Makefile tasks (0.15 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        with open(tasks_path, 'r') as f:
            tasks_data = json.load(f)

        tasks = tasks_data.get('tasks', [])
        task_labels = [t.get('label', '') for t in tasks]

        has_proto_gen_task = 'proto-gen' in task_labels
        has_run_grpc_task = 'run-grpc' in task_labels
        has_run_gateway_task = 'run-gateway' in task_labels

        if has_proto_gen_task and has_run_grpc_task and has_run_gateway_task:
            print(f"PASS: Component 6 — tasks.json has all 3 tasks (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — proto-gen={has_proto_gen_task}, run-grpc={has_run_grpc_task}, run-gateway={has_run_gateway_task}")
            print(f"  Found labels: {task_labels}")
    except FileNotFoundError:
        print(f"FAIL: Component 6 — .vscode/tasks.json not found")
    except json.JSONDecodeError as e:
        print(f"ERROR: Component 6 — invalid JSON in tasks.json: {e}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
