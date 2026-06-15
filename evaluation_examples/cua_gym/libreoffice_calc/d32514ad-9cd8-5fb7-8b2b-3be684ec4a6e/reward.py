"""
Reward Script: Create docker-compose.override.yml with debug ports, volumes, and NODE_ENV=development
Task ID: vscode_ops_085
Domain: vscode (file verification)
Scoring:
  - Component 1: Override file exists and is valid YAML (0.15 pts)
  - Component 2: Backend service has debug port mapping 9229 (0.30 pts)
  - Component 3: Backend service has volume mount for local source code (0.25 pts)
  - Component 4: Backend service has NODE_ENV=development (0.30 pts)
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_085'
OVERRIDE_PATH = os.path.join(WORKDIR, 'project', 'docker-compose.override.yml')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: override file must exist
    if not os.path.exists(OVERRIDE_PATH):
        print(f"CRITICAL: Override file not found at {OVERRIDE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File exists and is valid YAML (0.15 points)
    try:
        import yaml
    except ImportError:
        # Fallback: try to parse manually if PyYAML not available
        yaml = None

    override_data = None
    try:
        with open(OVERRIDE_PATH, 'r') as f:
            content = f.read()

        if yaml is not None:
            override_data = yaml.safe_load(content)
        else:
            # Simple fallback: check it's non-empty and has expected structure keywords
            # We'll try json-like parsing won't work for YAML, so check key strings
            if 'services' in content and 'backend' in content:
                # Build a minimal dict from text parsing for subsequent checks
                override_data = {'_raw': content}
            else:
                override_data = None

        if override_data is not None and override_data:
            print(f"PASS: Component 1 -- Override file is valid YAML (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Override file is empty or invalid YAML")
    except Exception as e:
        print(f"ERROR: Component 1 -- Could not parse override file: {e}")

    if override_data is None:
        print(f"REWARD: {total_score}")
        return total_score

    # For subsequent checks, we need the parsed data or raw content
    # If yaml was available, use structured data; otherwise parse raw text
    use_yaml = yaml is not None and '_raw' not in override_data

    # Component 2: Backend service has debug port mapping for 9229 (0.30 points)
    try:
        if use_yaml:
            services = override_data.get('services', {})
            backend = services.get('backend', {})
            ports = backend.get('ports', [])
            port_strs = [str(p) for p in ports]
            has_debug_port = any('9229' in p for p in port_strs)
        else:
            raw = override_data.get('_raw', content)
            has_debug_port = '9229' in raw and 'ports' in raw

        if has_debug_port:
            print(f"PASS: Component 2 -- Debug port 9229 mapping found (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 -- No debug port 9229 mapping found in backend service")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Backend service has volume mount for local source code (0.25 points)
    try:
        if use_yaml:
            services = override_data.get('services', {})
            backend = services.get('backend', {})
            volumes = backend.get('volumes', [])
            vol_strs = [str(v) for v in volumes]
            # Check for a volume mount that maps local backend directory
            # Expected patterns: ./backend:/app, ./backend:/usr/src/app, ./src:/app, etc.
            has_volume = any(
                (':' in v and ('backend' in v.split(':')[0] or 'src' in v.split(':')[0] or './' in v.split(':')[0]))
                for v in vol_strs
            )
        else:
            raw = override_data.get('_raw', content)
            has_volume = 'volumes' in raw and (':' in raw) and ('backend' in raw or './src' in raw)

        if has_volume:
            print(f"PASS: Component 3 -- Volume mount for local source code found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- No volume mount for local source code found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Backend service has NODE_ENV=development (0.30 points)
    try:
        if use_yaml:
            services = override_data.get('services', {})
            backend = services.get('backend', {})
            environment = backend.get('environment', [])
            # environment can be a list of strings or a dict
            if isinstance(environment, dict):
                has_dev_env = environment.get('NODE_ENV') == 'development'
            elif isinstance(environment, list):
                env_strs = [str(e) for e in environment]
                has_dev_env = any('NODE_ENV=development' in e for e in env_strs)
            else:
                has_dev_env = False
        else:
            raw = override_data.get('_raw', content)
            has_dev_env = 'NODE_ENV=development' in raw or 'NODE_ENV: development' in raw

        if has_dev_env:
            print(f"PASS: Component 4 -- NODE_ENV=development found in backend environment (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 4 -- NODE_ENV=development not found in backend environment")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
