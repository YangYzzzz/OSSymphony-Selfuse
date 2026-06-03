"""
Reward Script: Docker Swarm mode with replicated Nginx service
Task ID: os_adm_048
Domain: os (Docker)
Scoring:
  Component 1: Docker Swarm active (0.2)
  Component 2: Overlay network "app-overlay" exists (0.2)
  Component 3: Nginx service with 3 replicas, port 80:80, constraint node.role==manager (0.4)
  Component 4: curl localhost returns Nginx welcome page (0.2)
"""

import subprocess
import json
import re


def run_cmd(cmd: str) -> str:
    """Run a shell command with sudo and return stdout only."""
    full_cmd = f"echo 'password' | sudo -S {cmd} 2>/dev/null"
    result = subprocess.run(
        full_cmd, shell=True, capture_output=True, text=True, timeout=30
    )
    return result.stdout


def verify_task():
    total_score = 0.0

    # Component 1: Docker Swarm is active (0.2 points)
    try:
        info_output = run_cmd("docker info --format '{{.Swarm.LocalNodeState}}'")
        # The output may contain the sudo password prompt; look for 'active'
        if "active" in info_output and "inactive" not in info_output:
            print(f"PASS: Component 1 - Docker Swarm is active (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 - Docker Swarm not active. Output: {info_output.strip()}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Overlay network 'app-overlay' exists (0.2 points)
    try:
        net_output = run_cmd("docker network ls --format '{{.Name}} {{.Driver}}'")
        lines = net_output.strip().split("\n")
        found_overlay = False
        for line in lines:
            if "app-overlay" in line and "overlay" in line:
                found_overlay = True
                break
        if found_overlay:
            print(f"PASS: Component 2 - Overlay network 'app-overlay' exists (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 - 'app-overlay' overlay network not found. Networks: {net_output.strip()}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Nginx service with correct configuration (0.4 points)
    # Sub-checks: service exists (0.1), 3 replicas (0.1), port 80:80 (0.1), constraint (0.1)
    try:
        svc_output = run_cmd("docker service inspect nginx")
        # Strip sudo prompt lines
        json_start = svc_output.find("[")
        json_end = svc_output.rfind("]")
        if json_start == -1 or json_end == -1:
            print(f"FAIL: Component 3 - Nginx service not found. Output: {svc_output.strip()}")
        else:
            svc_json = json.loads(svc_output[json_start:json_end + 1])
            svc = svc_json[0]
            spec = svc["Spec"]

            # 3a: Service exists and named nginx
            svc_name = spec.get("Name", "")
            if svc_name == "nginx":
                print(f"PASS: Component 3a - Nginx service exists (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3a - Service name is '{svc_name}', expected 'nginx'")

            # 3b: 3 replicas
            replicas = spec.get("Mode", {}).get("Replicated", {}).get("Replicas", 0)
            if replicas == 3:
                print(f"PASS: Component 3b - Service has 3 replicas (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3b - Replicas={replicas}, expected 3")

            # 3c: Port 80 published
            ports = spec.get("EndpointSpec", {}).get("Ports", [])
            port_ok = False
            for p in ports:
                if p.get("PublishedPort") == 80 and p.get("TargetPort") == 80:
                    port_ok = True
                    break
            if port_ok:
                print(f"PASS: Component 3c - Port 80:80 published (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3c - Port 80:80 not found. Ports: {ports}")

            # 3d: Placement constraint node.role==manager
            constraints = spec.get("TaskTemplate", {}).get("Placement", {}).get("Constraints", [])
            constraint_ok = any("node.role==manager" in c for c in constraints)
            if constraint_ok:
                print(f"PASS: Component 3d - Constraint node.role==manager found (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3d - Constraint not found. Constraints: {constraints}")

    except json.JSONDecodeError as e:
        print(f"ERROR: Component 3 - Failed to parse service JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: curl localhost returns Nginx welcome page (0.2 points)
    try:
        curl_result = subprocess.run(
            ["curl", "-s", "--max-time", "5", "http://localhost"],
            capture_output=True, text=True, timeout=10
        )
        if "Welcome to nginx" in curl_result.stdout:
            print(f"PASS: Component 4 - curl localhost returns Nginx welcome page (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 - Nginx welcome page not found in curl output. Got: {curl_result.stdout[:200]}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
