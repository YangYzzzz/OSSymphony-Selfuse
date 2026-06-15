"""
Reward Script: Fix YAML validation errors in Kubernetes deployment file
Task ID: vscode_ops_090
Domain: vscode
Scoring:
  Component 1: apiVersion corrected to apps/v1 (0.2 pts)
  Component 2: spec key added under template (0.25 pts)
  Component 3: containers indentation fixed (0.2 pts)
  Component 4: container name field added (0.2 pts)
  Component 5: containerPort is numeric integer 80 (0.15 pts)
"""

import os
import yaml  # PyYAML is available on VM

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_090'
DEPLOY_PATH = os.path.join(WORKDIR, 'k8s-project', 'deployment.yaml')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the YAML file
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        doc = yaml.safe_load(content)
        if not isinstance(doc, dict):
            print(f"CRITICAL: YAML did not parse to a dict, got {type(doc)}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load YAML file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: apiVersion corrected to apps/v1 (0.2 points)
    # Initial has "apps/v1beta1", golden has "apps/v1"
    try:
        api_version = doc.get('apiVersion', '')
        if api_version == 'apps/v1':
            print(f"PASS: Component 1 — apiVersion is 'apps/v1' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — expected apiVersion 'apps/v1', found '{api_version}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: spec key exists under template (0.25 points)
    # Initial has template.containers directly (no spec key); golden has template.spec.containers
    try:
        template = doc.get('spec', {}).get('template', {})
        if isinstance(template, dict) and 'spec' in template:
            template_spec = template['spec']
            if isinstance(template_spec, dict) and 'containers' in template_spec:
                print(f"PASS: Component 2 — template.spec.containers structure present (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — template.spec exists but 'containers' not found inside")
        else:
            print(f"FAIL: Component 2 — 'spec' key missing under template (keys: {list(template.keys()) if isinstance(template, dict) else 'N/A'})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: containers indentation is correct (0.2 points)
    # In the initial file, containers list is over-indented (8 extra spaces).
    # After fixing, the '- name:' or '- image:' lines under containers should be at 8 spaces indent.
    # We check the raw text for proper indentation of the first container item.
    try:
        lines = content.split('\n')
        # Find the "containers:" line and then the first list item after it
        containers_line_idx = None
        containers_indent = None
        for i, line in enumerate(lines):
            stripped = line.lstrip()
            if stripped.startswith('containers:'):
                containers_line_idx = i
                containers_indent = len(line) - len(stripped)
                break

        container_item_indent = None
        if containers_line_idx is not None:
            # Find the first list item (starts with '- ') after the containers: line
            for line in lines[containers_line_idx + 1:]:
                stripped = line.lstrip()
                if stripped.startswith('- '):
                    container_item_indent = len(line) - len(stripped)
                    break
                elif stripped and not stripped.startswith('#'):
                    break  # non-list, non-comment line means containers section ended

        # In a properly structured k8s deployment with 2-space indent:
        #   containers: is at indent N, items should be at indent N+2
        # Golden: containers: at 6 spaces, items at 8 spaces (diff = 2)
        # Initial: containers: at some level, items at 12 spaces (diff much larger = over-indented)
        if container_item_indent is not None and containers_indent is not None:
            indent_diff = container_item_indent - containers_indent
            if indent_diff <= 4:
                # Properly indented: item is 2-4 spaces deeper than containers key
                print(f"PASS: Component 3 — container items indented {indent_diff} spaces beyond 'containers:' (proper) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — container items indented {indent_diff} spaces beyond 'containers:' (over-indented, expected 2-4)")
        else:
            print(f"FAIL: Component 3 — could not find containers section or list items")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: container name field exists (0.2 points)
    # Initial file has no 'name' in the container; golden has 'name: webapp-container'
    try:
        containers = None
        template = doc.get('spec', {}).get('template', {})
        # Try template.spec.containers (golden structure)
        if isinstance(template, dict) and 'spec' in template:
            containers = template['spec'].get('containers', [])
        # Fallback: template.containers (initial structure, but with name added)
        if not containers and isinstance(template, dict) and 'containers' in template:
            containers = template.get('containers', [])

        if containers and isinstance(containers, list) and len(containers) > 0:
            first_container = containers[0]
            if isinstance(first_container, dict) and 'name' in first_container:
                name_val = first_container['name']
                if isinstance(name_val, str) and len(name_val) > 0:
                    print(f"PASS: Component 4 — container has name field: '{name_val}' (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 4 — container name is empty or invalid: {name_val}")
            else:
                print(f"FAIL: Component 4 — container missing 'name' field (keys: {list(first_container.keys()) if isinstance(first_container, dict) else 'N/A'})")
        else:
            print(f"FAIL: Component 4 — no containers found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: containerPort is numeric integer 80 (0.15 points)
    # Initial has containerPort: "eighty" (string); golden has containerPort: 80 (int)
    try:
        containers = None
        template = doc.get('spec', {}).get('template', {})
        if isinstance(template, dict) and 'spec' in template:
            containers = template['spec'].get('containers', [])
        if not containers and isinstance(template, dict) and 'containers' in template:
            containers = template.get('containers', [])

        if containers and isinstance(containers, list) and len(containers) > 0:
            first_container = containers[0]
            ports = first_container.get('ports', [])
            if ports and isinstance(ports, list) and len(ports) > 0:
                port_val = ports[0].get('containerPort')
                if isinstance(port_val, int) and port_val == 80:
                    print(f"PASS: Component 5 — containerPort is 80 (integer) (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 5 — expected containerPort=80 (int), found '{port_val}' ({type(port_val).__name__})")
            else:
                print(f"FAIL: Component 5 — no ports found in container")
        else:
            print(f"FAIL: Component 5 — no containers found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
if not os.path.exists(DEPLOY_PATH):
    print(f"File not found: {DEPLOY_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(DEPLOY_PATH)
