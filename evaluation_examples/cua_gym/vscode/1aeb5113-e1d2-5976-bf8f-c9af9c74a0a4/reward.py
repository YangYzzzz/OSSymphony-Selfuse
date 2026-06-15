"""
Reward Script: Docker Compose dev file for microservices
Task ID: vscode_gf3_051
Domain: vscode
Scoring:
  Component 1: File exists and is valid YAML with services (0.1)
  Component 2: Redis service — image redis:7-alpine, port 6379 (0.2)
  Component 3: Postgres service — image postgres:15, port 5432, named volume (0.2)
  Component 4: Adminer service — image adminer:latest, port 8080 (0.15)
  Component 5: API service — build ./api, volume ./api:/app, depends_on redis+postgres (0.25)
  Component 6: Top-level named volume for postgres (0.1)
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_051'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'microservices', 'docker-compose.dev.yml')


def parse_yaml_minimal(content):
    """Parse YAML using PyYAML if available, else a basic fallback."""
    try:
        import yaml
        return yaml.safe_load(content)
    except ImportError:
        pass
    # Fallback: return None to signal we need text-based checks
    return None


def check_port_mapping(port_list, host_port, container_port=None):
    """Check if a port mapping like '6379:6379' exists in a ports list."""
    if container_port is None:
        container_port = host_port
    target = f"{host_port}:{container_port}"
    if not port_list:
        return False
    for p in port_list:
        p_str = str(p).strip().strip('"').strip("'")
        if p_str == target:
            return True
    return False


def check_volume_mapping(vol_list, expected):
    """Check if a volume mapping like './api:/app' exists in volumes list."""
    if not vol_list:
        return False
    for v in vol_list:
        v_str = str(v).strip().strip('"').strip("'")
        if v_str == expected:
            return True
    return False


def check_depends_on(depends, expected_services):
    """Check depends_on contains the expected services."""
    if not depends:
        return False
    if isinstance(depends, list):
        return all(svc in depends for svc in expected_services)
    if isinstance(depends, dict):
        return all(svc in depends for svc in expected_services)
    return False


def verify_task():
    """
    Verify docker-compose.dev.yml with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(FILE_PATH):
        print(f"CRITICAL: File not found at {FILE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(FILE_PATH, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {FILE_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Try to parse YAML
    data = parse_yaml_minimal(content)

    if data is None:
        print("CRITICAL: Could not parse YAML (no yaml library and no fallback)")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(data, dict):
        print(f"CRITICAL: YAML root is not a mapping, got {type(data)}")
        print("REWARD: 0.0")
        return 0.0

    services = data.get('services')
    if not services or not isinstance(services, dict):
        print("CRITICAL: No 'services' key found in YAML")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is valid YAML with a services section (0.1 points)
    # This component is anchored to the file existing at the new path — initial has no such file.
    try:
        if 'services' in data and len(services) >= 1:
            print(f"PASS: Component 1 — Valid YAML with {len(services)} service(s) (0.1 pts)")
            total_score += 0.1
        else:
            print("FAIL: Component 1 — No services defined")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Redis service — image redis:7-alpine, port 6379 (0.2 points)
    try:
        redis_svc = services.get('redis')
        if redis_svc and isinstance(redis_svc, dict):
            image_ok = str(redis_svc.get('image', '')).startswith('redis:7-alpine')
            ports = redis_svc.get('ports', [])
            port_ok = check_port_mapping(ports, '6379', '6379')

            if image_ok and port_ok:
                print(f"PASS: Component 2 — Redis: image={redis_svc.get('image')}, port 6379:6379 (0.2 pts)")
                total_score += 0.2
            elif image_ok:
                print(f"PARTIAL: Component 2 — Redis image correct but port 6379 mapping missing (0.1 pts)")
                total_score += 0.1
            elif port_ok:
                print(f"PARTIAL: Component 2 — Redis port correct but image wrong: {redis_svc.get('image')} (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 2 — Redis image={redis_svc.get('image')}, ports={ports}")
        else:
            print("FAIL: Component 2 — No 'redis' service found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Postgres service — image postgres:15, port 5432, named volume (0.2 points)
    try:
        pg_svc = services.get('postgres')
        if pg_svc and isinstance(pg_svc, dict):
            pg_image = str(pg_svc.get('image', ''))
            image_ok = pg_image.startswith('postgres:15')
            ports = pg_svc.get('ports', [])
            port_ok = check_port_mapping(ports, '5432', '5432')

            # Check for named volume (not a bind mount — should reference a top-level volume)
            volumes = pg_svc.get('volumes', [])
            named_vol = any(
                ':' in str(v).strip() and not str(v).strip().startswith('.') and not str(v).strip().startswith('/')
                for v in (volumes or [])
            )

            points = 0.0
            if image_ok:
                points += 0.07
            if port_ok:
                points += 0.07
            if named_vol:
                points += 0.06

            if image_ok and port_ok and named_vol:
                print(f"PASS: Component 3 — Postgres: image={pg_image}, port 5432, named volume (0.2 pts)")
                total_score += 0.2
            else:
                details = f"image={'OK' if image_ok else pg_image}, port={'OK' if port_ok else 'MISSING'}, named_vol={'OK' if named_vol else 'MISSING'}"
                print(f"PARTIAL: Component 3 — Postgres: {details} ({points:.2f} pts)")
                total_score += points
        else:
            print("FAIL: Component 3 — No 'postgres' service found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Adminer service — image adminer:latest, port 8080 (0.15 points)
    try:
        adminer_svc = services.get('adminer')
        if adminer_svc and isinstance(adminer_svc, dict):
            image_ok = str(adminer_svc.get('image', '')) == 'adminer:latest'
            ports = adminer_svc.get('ports', [])
            port_ok = check_port_mapping(ports, '8080', '8080')

            if image_ok and port_ok:
                print(f"PASS: Component 4 — Adminer: image=adminer:latest, port 8080 (0.15 pts)")
                total_score += 0.15
            elif image_ok:
                print(f"PARTIAL: Component 4 — Adminer image correct but port 8080 missing (0.07 pts)")
                total_score += 0.07
            elif port_ok:
                print(f"PARTIAL: Component 4 — Adminer port correct but image wrong: {adminer_svc.get('image')} (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 4 — Adminer image={adminer_svc.get('image')}, ports={ports}")
        else:
            print("FAIL: Component 4 — No 'adminer' service found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: API service — build from ./api, volume ./api:/app, depends_on redis+postgres (0.25 pts)
    try:
        api_svc = services.get('api')
        if api_svc and isinstance(api_svc, dict):
            # Check build context
            build = api_svc.get('build')
            build_ok = False
            if isinstance(build, str):
                build_ok = build.rstrip('/') == './api'
            elif isinstance(build, dict):
                ctx = str(build.get('context', '')).rstrip('/')
                build_ok = ctx == './api'

            # Check volume mount ./api:/app
            volumes = api_svc.get('volumes', [])
            vol_ok = check_volume_mapping(volumes, './api:/app')

            # Check depends_on includes redis and postgres
            depends = api_svc.get('depends_on')
            depends_ok = check_depends_on(depends, ['redis', 'postgres'])

            points = 0.0
            if build_ok:
                points += 0.09
            if vol_ok:
                points += 0.08
            if depends_ok:
                points += 0.08

            if build_ok and vol_ok and depends_ok:
                print(f"PASS: Component 5 — API: build=./api, vol=./api:/app, depends_on=[redis,postgres] (0.25 pts)")
                total_score += 0.25
            else:
                details = f"build={'OK' if build_ok else build}, vol={'OK' if vol_ok else 'MISSING'}, depends={'OK' if depends_ok else depends}"
                print(f"PARTIAL: Component 5 — API: {details} ({points:.2f} pts)")
                total_score += points
        else:
            print("FAIL: Component 5 — No 'api' service found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Top-level named volume for postgres data (0.1 pts)
    try:
        top_volumes = data.get('volumes')
        if top_volumes and isinstance(top_volumes, dict):
            # Check that at least one top-level volume is defined (for postgres)
            # The volume name used in postgres service should match a top-level volume
            pg_svc = services.get('postgres', {})
            pg_vols = pg_svc.get('volumes', []) if isinstance(pg_svc, dict) else []
            vol_name = None
            for v in pg_vols:
                v_str = str(v).strip()
                if ':' in v_str and not v_str.startswith('.') and not v_str.startswith('/'):
                    vol_name = v_str.split(':')[0]
                    break

            if vol_name and vol_name in top_volumes:
                print(f"PASS: Component 6 — Top-level named volume '{vol_name}' declared (0.1 pts)")
                total_score += 0.1
            elif len(top_volumes) > 0:
                # There's a top-level volumes section, give partial
                print(f"PARTIAL: Component 6 — Top-level volumes exist but don't match postgres vol name (0.05 pts)")
                total_score += 0.05
            else:
                print("FAIL: Component 6 — No top-level volumes defined")
        else:
            print("FAIL: Component 6 — No 'volumes' top-level key in compose file")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
