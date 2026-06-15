"""
Reward Script: Multi-stage Docker Compose deployment workflow with VSCode task
Task ID: vscode_gf3_063
Domain: vscode
Scoring:
  Component 1 (0.20): docker-compose.yml exists and has valid service definitions
  Component 2 (0.20): Production images use specific version tags + health checks present
  Component 3 (0.15): Traefik reverse proxy labels for HTTPS on webapp service
  Component 4 (0.20): docker-compose.override.yml with build context and debug port
  Component 5 (0.10): Override file has dev environment variable overrides
  Component 6 (0.15): VSCode tasks.json with 'Docker Compose Up (Dev)' task
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_063'

COMPOSE_PATH = os.path.join(WORKDIR, 'projects', 'webapp', 'docker-compose.yml')
OVERRIDE_PATH = os.path.join(WORKDIR, 'projects', 'webapp', 'docker-compose.override.yml')
TASKS_PATH = os.path.join(WORKDIR, 'projects', 'webapp', '.vscode', 'tasks.json')


def parse_yaml_basic(content):
    """
    Minimal YAML-like parser for docker-compose files.
    Returns a dict-like structure by parsing the raw text.
    We avoid importing yaml since it may not be available.
    """
    return content


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================================
    # Component 1: docker-compose.yml exists and has valid service definitions (0.20)
    # =========================================================================
    try:
        if not os.path.exists(COMPOSE_PATH):
            print(f"FAIL: Component 1 — docker-compose.yml not found at {COMPOSE_PATH}")
        else:
            with open(COMPOSE_PATH, 'r') as f:
                compose_content = f.read()

            # Check for services section and key service names
            has_services = bool(re.search(r'^services\s*:', compose_content, re.MULTILINE))
            has_webapp = bool(re.search(r'^\s+webapp\s*:', compose_content, re.MULTILINE))
            has_db = bool(re.search(r'^\s+db\s*:', compose_content, re.MULTILINE))
            has_redis = bool(re.search(r'^\s+redis\s*:', compose_content, re.MULTILINE))

            if has_services and has_webapp and has_db and has_redis:
                print(f"PASS: Component 1 — docker-compose.yml has services: webapp, db, redis (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — Missing required services. services={has_services}, webapp={has_webapp}, db={has_db}, redis={has_redis}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: Production images use specific version tags + health checks (0.20)
    # =========================================================================
    try:
        if not os.path.exists(COMPOSE_PATH):
            print(f"FAIL: Component 2 — docker-compose.yml not found")
        else:
            with open(COMPOSE_PATH, 'r') as f:
                compose_content = f.read()

            # Check for specific version tags on images (not 'latest', not bare image names)
            # Look for image lines with version tags like :2.4.1, :16.1-alpine, :7.2.3-alpine
            image_lines = re.findall(r'^\s+image:\s*(.+)$', compose_content, re.MULTILINE)
            has_versioned_images = False
            if image_lines:
                # Check that at least 2 images have specific version tags (not 'latest')
                versioned_count = 0
                for img in image_lines:
                    img = img.strip()
                    # Must have a colon with a version that is NOT 'latest'
                    if ':' in img:
                        tag = img.split(':')[-1].strip()
                        if tag and tag.lower() != 'latest':
                            versioned_count += 1
                has_versioned_images = versioned_count >= 2

            # Check for healthcheck definitions
            healthcheck_count = len(re.findall(r'^\s+healthcheck\s*:', compose_content, re.MULTILINE))
            has_healthchecks = healthcheck_count >= 2  # At least webapp and db should have health checks

            if has_versioned_images and has_healthchecks:
                print(f"PASS: Component 2 — Versioned images found, {healthcheck_count} healthchecks defined (0.20 pts)")
                total_score += 0.20
            elif has_versioned_images:
                print(f"PARTIAL: Component 2 — Versioned images OK but only {healthcheck_count} healthcheck(s) (0.10 pts)")
                total_score += 0.10
            elif has_healthchecks:
                print(f"PARTIAL: Component 2 — Healthchecks OK but images not properly versioned (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — No versioned images and no healthchecks")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: Traefik reverse proxy labels for HTTPS (0.15)
    # =========================================================================
    try:
        if not os.path.exists(COMPOSE_PATH):
            print(f"FAIL: Component 3 — docker-compose.yml not found")
        else:
            with open(COMPOSE_PATH, 'r') as f:
                compose_content = f.read()

            # Check for Traefik-related labels on the webapp service
            has_traefik_enable = bool(re.search(r'traefik\.enable\s*=\s*true', compose_content, re.IGNORECASE))
            has_traefik_router = bool(re.search(r'traefik\.http\.routers\.', compose_content))
            has_tls_or_https = bool(re.search(r'(tls|certresolver|letsencrypt|websecure)', compose_content, re.IGNORECASE))

            # Check for a traefik service definition
            has_traefik_service = bool(re.search(r'^\s+traefik\s*:', compose_content, re.MULTILINE))

            if has_traefik_enable and has_traefik_router and has_tls_or_https:
                print(f"PASS: Component 3 — Traefik labels with HTTPS/TLS config found (0.15 pts)")
                total_score += 0.15
            elif has_traefik_enable or has_traefik_service:
                print(f"PARTIAL: Component 3 — Some Traefik config but incomplete HTTPS setup (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 3 — No Traefik reverse proxy labels found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: docker-compose.override.yml with build context and debug port (0.20)
    # =========================================================================
    try:
        if not os.path.exists(OVERRIDE_PATH):
            print(f"FAIL: Component 4 — docker-compose.override.yml not found at {OVERRIDE_PATH}")
        else:
            with open(OVERRIDE_PATH, 'r') as f:
                override_content = f.read()

            # Check for build context (changes from pre-built image to local build)
            has_build = bool(re.search(r'^\s+build\s*:', override_content, re.MULTILINE))
            has_dockerfile_ref = bool(re.search(r'(dockerfile|Dockerfile|context)', override_content, re.IGNORECASE))

            # Check for debug port (typically 9229 for Node.js debugging)
            has_debug_port = bool(re.search(r'9229', override_content))

            if has_build and has_debug_port:
                print(f"PASS: Component 4 — Override has build context and debug port 9229 (0.20 pts)")
                total_score += 0.20
            elif has_build:
                print(f"PARTIAL: Component 4 — Override has build context but no debug port (0.10 pts)")
                total_score += 0.10
            elif has_debug_port:
                print(f"PARTIAL: Component 4 — Override has debug port but no build context (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — Override missing build context and debug port")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================================
    # Component 5: Override file has dev environment variable overrides (0.10)
    # =========================================================================
    try:
        if not os.path.exists(OVERRIDE_PATH):
            print(f"FAIL: Component 5 — docker-compose.override.yml not found")
        else:
            with open(OVERRIDE_PATH, 'r') as f:
                override_content = f.read()

            # Check for development-specific environment variables
            has_dev_env = bool(re.search(r'NODE_ENV\s*:\s*development', override_content, re.IGNORECASE))
            has_debug_or_log = bool(re.search(r'(LOG_LEVEL\s*:\s*debug|DEBUG\s*:)', override_content, re.IGNORECASE))

            if has_dev_env and has_debug_or_log:
                print(f"PASS: Component 5 — Dev environment overrides present (NODE_ENV=development, debug logging) (0.10 pts)")
                total_score += 0.10
            elif has_dev_env or has_debug_or_log:
                print(f"PARTIAL: Component 5 — Some dev env overrides (dev_env={has_dev_env}, debug_log={has_debug_or_log}) (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 5 — No development environment overrides found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # =========================================================================
    # Component 6: VSCode tasks.json with 'Docker Compose Up (Dev)' task (0.15)
    # =========================================================================
    try:
        if not os.path.exists(TASKS_PATH):
            print(f"FAIL: Component 6 — .vscode/tasks.json not found at {TASKS_PATH}")
        else:
            with open(TASKS_PATH, 'r') as f:
                # Handle possible JSONC (comments in JSON)
                content = f.read()
                # Strip single-line comments
                cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                tasks_config = json.loads(cleaned)

            tasks = tasks_config.get('tasks', [])

            # Find matching tasks using list comprehensions (no direct True assignments)
            matching_tasks = [
                t for t in tasks
                if 'Docker Compose Up (Dev)' in t.get('label', '')
            ]
            correct_cmd_tasks = [
                t for t in matching_tasks
                if 'docker compose up' in t.get('command', '') or 'docker-compose up' in t.get('command', '')
            ]

            if len(matching_tasks) > 0 and len(correct_cmd_tasks) > 0:
                print(f"PASS: Component 6 — VSCode task 'Docker Compose Up (Dev)' with correct command found (0.15 pts)")
                total_score += 0.15
            elif len(matching_tasks) > 0:
                print(f"PARTIAL: Component 6 — Task found but command incorrect (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 6 — No 'Docker Compose Up (Dev)' task found in tasks.json")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
