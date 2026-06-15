"""
Reward Script: Docker Swarm cluster setup with stack deployment
Task ID: os_gff_064
Domain: os (Docker Swarm)
Scoring:
  - Component 1: Swarm mode active, node is manager (0.15)
  - Component 2: /opt/swarm/stack.yml exists with correct structure (0.20)
  - Component 3: Stack 'myapp' deployed with 2 services (0.15)
  - Component 4: Web service has 3 running replicas (0.15)
  - Component 5: Web service rolling update config (parallelism=1, delay=30s) (0.15)
  - Component 6: Redis service has placement constraint (node.role==manager) (0.10)
  - Component 7: Overlay network connecting services (0.10)
"""

import subprocess
import os
import re


def run_cmd(cmd):
    """Run a shell command and return stdout, stderr, returncode."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def verify_task():
    total_score = 0.0

    # Component 1: Swarm mode active, node is manager (0.15 pts)
    # This FAILS on initial (not in swarm mode) and PASSES on golden
    try:
        stdout, stderr, rc = run_cmd("docker info --format '{{.Swarm.LocalNodeState}}'")
        if rc == 0 and 'active' in stdout:
            # Also check this node is a manager
            stdout2, _, rc2 = run_cmd("docker node ls --format '{{.ManagerStatus}}' 2>/dev/null | head -1")
            if rc2 == 0 and 'Leader' in stdout2:
                print(f"PASS: Component 1 — Swarm active, node is Leader (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Swarm active but node not Leader. Got: {stdout2}")
        else:
            print(f"FAIL: Component 1 — Swarm not active. State: {stdout} {stderr}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: /opt/swarm/stack.yml exists with correct structure (0.20 pts)
    # This FAILS on initial (file does not exist) and PASSES on golden
    try:
        stack_path = '/opt/swarm/stack.yml'
        if os.path.isfile(stack_path):
            with open(stack_path, 'r') as f:
                content = f.read()

            checks_passed = 0
            total_checks = 5

            # Check version 3.8
            if re.search(r"version:\s*['\"]3\.8['\"]", content):
                checks_passed += 1
            else:
                print(f"  DETAIL: stack.yml missing version '3.8'")

            # Check web service with nginx:alpine
            if re.search(r'web:', content) and re.search(r'image:\s*nginx:alpine', content):
                checks_passed += 1
            else:
                print(f"  DETAIL: stack.yml missing web service with nginx:alpine")

            # Check redis service with redis:7-alpine
            if re.search(r'redis:', content) and re.search(r'image:\s*redis:7-alpine', content):
                checks_passed += 1
            else:
                print(f"  DETAIL: stack.yml missing redis service with redis:7-alpine")

            # Check overlay network
            if re.search(r'driver:\s*overlay', content):
                checks_passed += 1
            else:
                print(f"  DETAIL: stack.yml missing overlay network")

            # Check deploy section exists
            if re.search(r'deploy:', content):
                checks_passed += 1
            else:
                print(f"  DETAIL: stack.yml missing deploy section")

            if checks_passed == total_checks:
                print(f"PASS: Component 2 — stack.yml has all required structure ({checks_passed}/{total_checks}) (0.20 pts)")
                total_score += 0.20
            elif checks_passed >= 3:
                partial = round(0.20 * checks_passed / total_checks, 2)
                print(f"PARTIAL: Component 2 — stack.yml has {checks_passed}/{total_checks} elements ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — stack.yml incomplete ({checks_passed}/{total_checks})")
        else:
            print(f"FAIL: Component 2 — /opt/swarm/stack.yml does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Stack 'myapp' deployed with 2 services (0.15 pts)
    # This FAILS on initial (no stack) and PASSES on golden
    try:
        stdout, stderr, rc = run_cmd("docker stack ls --format '{{.Name}}:{{.Services}}' 2>/dev/null")
        if rc == 0 and 'myapp:2' in stdout:
            print(f"PASS: Component 3 — Stack 'myapp' deployed with 2 services (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Expected 'myapp:2' in stack list. Got: {stdout} {stderr}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Web service has 3 running replicas (0.15 pts)
    # This FAILS on initial (service doesn't exist) and PASSES on golden
    try:
        stdout, stderr, rc = run_cmd("docker service ls --filter 'name=myapp_web' --format '{{.Replicas}}' 2>/dev/null")
        if rc == 0 and '3/3' in stdout:
            print(f"PASS: Component 4 — Web service has 3/3 replicas running (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Expected 3/3 replicas. Got: {stdout} {stderr}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Web service rolling update config (parallelism=1, delay=30s) (0.15 pts)
    # This FAILS on initial (service doesn't exist) and PASSES on golden
    try:
        stdout, stderr, rc = run_cmd("docker service inspect myapp_web --format '{{.Spec.UpdateConfig.Parallelism}},{{.Spec.UpdateConfig.Delay}}' 2>/dev/null")
        if rc == 0:
            parts = stdout.strip()
            # Delay is in nanoseconds in API: 30s = 30000000000
            parallelism_ok = parts.startswith('1,')
            delay_val = parts.split(',')[1] if ',' in parts else ''
            # Docker returns delay in ns: 30000000000 = 30s
            delay_ok = delay_val == '30000000000' or delay_val == '30s'
            if parallelism_ok and delay_ok:
                print(f"PASS: Component 5 — Update config parallelism=1, delay=30s (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — Update config mismatch. Got: {parts}")
        else:
            print(f"FAIL: Component 5 — Cannot inspect myapp_web: {stderr}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Redis service has placement constraint (node.role==manager) (0.10 pts)
    # This FAILS on initial (service doesn't exist) and PASSES on golden
    try:
        stdout, stderr, rc = run_cmd("docker service inspect myapp_redis --format '{{.Spec.TaskTemplate.Placement.Constraints}}' 2>/dev/null")
        if rc == 0 and 'node.role' in stdout and 'manager' in stdout:
            print(f"PASS: Component 6 — Redis has placement constraint node.role==manager (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — Redis constraint missing. Got: {stdout} {stderr}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Overlay network connecting services (0.10 pts)
    # This FAILS on initial (no swarm networks) and PASSES on golden
    try:
        stdout, stderr, rc = run_cmd("docker network ls --filter 'scope=swarm' --filter 'driver=overlay' --format '{{.Name}}' 2>/dev/null")
        if rc == 0 and 'myapp_app_network' in stdout:
            print(f"PASS: Component 7 — Overlay network 'myapp_app_network' exists (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 — Expected 'myapp_app_network' overlay. Got: {stdout} {stderr}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
