"""
Reward Script: Docker Compose three-service stack verification
Task ID: os_gf2_007
Domain: os (Docker Compose file creation)
Scoring:
  - Component 1: File exists and is valid YAML (0.1)
  - Component 2: Exactly 3 services defined: db, cache, web (0.2)
  - Component 3: db service correct (postgres:15, env, volume) (0.2)
  - Component 4: cache service correct (redis:7-alpine) (0.1)
  - Component 5: web service correct (build, ports, depends_on, env) (0.2)
  - Component 6: appnet network declared as bridge (0.1)
  - Component 7: db_data volume declared at top level (0.1)
"""

import os
import yaml

COMPOSE_PATH = '/opt/webapp/docker-compose.yml'


def verify_task():
    """
    Verify Docker Compose file creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File exists and is valid YAML (0.1 points)
    try:
        if not os.path.isfile(COMPOSE_PATH):
            print(f"FAIL: Component 1 — {COMPOSE_PATH} does not exist")
            print("REWARD: 0.0")
            return 0.0

        with open(COMPOSE_PATH, 'r') as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            print(f"FAIL: Component 1 — YAML parsed but is not a dict (type: {type(data)})")
            print("REWARD: 0.0")
            return 0.0

        if isinstance(data, dict):
            print(f"PASS: Component 1 — file exists and is valid YAML (0.1 pts)")
            total_score += 0.1
    except yaml.YAMLError as e:
        print(f"FAIL: Component 1 — invalid YAML: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Exactly 3 services: db, cache, web (0.2 points)
    try:
        services = data.get('services', {})
        if not isinstance(services, dict):
            print(f"FAIL: Component 2 — 'services' key missing or not a dict")
        else:
            service_names = set(services.keys())
            expected_names = {'db', 'cache', 'web'}
            if service_names == expected_names:
                print(f"PASS: Component 2 — exactly 3 services: {sorted(service_names)} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — expected services {sorted(expected_names)}, found {sorted(service_names)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: db service — postgres:15 image, env vars, volume (0.2 points)
    try:
        db = services.get('db', {})
        if not isinstance(db, dict):
            print(f"FAIL: Component 3 — 'db' service not found or not a dict")
        else:
            sub_score = 0.0
            sub_checks = []

            # Check image
            img = str(db.get('image', ''))
            if img.startswith('postgres:15'):
                sub_score += 0.06
                sub_checks.append(f"image={img}")
            else:
                sub_checks.append(f"MISS image: expected postgres:15*, got {img}")

            # Check environment vars
            env = db.get('environment', {})
            if isinstance(env, dict):
                env_dict = env
            elif isinstance(env, list):
                env_dict = {}
                for item in env:
                    if '=' in str(item):
                        k, v = str(item).split('=', 1)
                        env_dict[k] = v
            else:
                env_dict = {}

            required_env = {
                'POSTGRES_DB': 'appdb',
                'POSTGRES_USER': 'app',
                'POSTGRES_PASSWORD': 'secret',
            }
            env_misses = [k for k, v in required_env.items()
                          if str(env_dict.get(k, '')).strip() != v]
            if len(env_misses) == 0:
                sub_score += 0.08
                sub_checks.append("env vars correct")
            else:
                for k in env_misses:
                    sub_checks.append(f"MISS env {k}={required_env[k]}, got {env_dict.get(k)}")

            # Check volume
            volumes = db.get('volumes', [])
            vol_ok = any('db_data:/var/lib/postgresql/data' in str(v) for v in volumes)
            if vol_ok:
                sub_score += 0.06
                sub_checks.append("volume db_data mapped")
            else:
                sub_checks.append(f"MISS volume db_data:/var/lib/postgresql/data, got {volumes}")

            if sub_score >= 0.19:  # all 3 sub-checks pass
                print(f"PASS: Component 3 — db service correct ({sub_score:.2f} pts) [{', '.join(sub_checks)}]")
                total_score += sub_score
            elif sub_score > 0:
                print(f"PARTIAL: Component 3 — db service ({sub_score:.2f} pts) [{', '.join(sub_checks)}]")
                total_score += sub_score
            else:
                print(f"FAIL: Component 3 — db service ({sub_score:.2f} pts) [{', '.join(sub_checks)}]")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: cache service — redis:7-alpine image (0.1 points)
    try:
        cache = services.get('cache', {})
        if not isinstance(cache, dict):
            print(f"FAIL: Component 4 — 'cache' service not found or not a dict")
        else:
            img = str(cache.get('image', ''))
            if img.startswith('redis:7'):
                print(f"PASS: Component 4 — cache service image={img} (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 4 — expected redis:7*, got {img}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: web service — build, ports, depends_on, env (0.2 points)
    try:
        web = services.get('web', {})
        if not isinstance(web, dict):
            print(f"FAIL: Component 5 — 'web' service not found or not a dict")
        else:
            sub_score = 0.0
            sub_checks = []

            # Check build context (. or /opt/webapp or similar)
            build = web.get('build', None)
            if build is not None:
                build_str = str(build) if not isinstance(build, dict) else str(build.get('context', ''))
                if build_str in ['.', './']:
                    sub_score += 0.04
                    sub_checks.append(f"build={build_str}")
                elif build_str:
                    sub_score += 0.02  # partial — build is specified but not '.'
                    sub_checks.append(f"build context is '{build_str}', expected '.'")
                else:
                    sub_checks.append("MISS build context value")
            else:
                sub_checks.append("MISS build context")

            # Check ports mapping 8080:5000
            ports = web.get('ports', [])
            port_ok = any('8080:5000' in str(p) for p in ports)
            if port_ok:
                sub_score += 0.04
                sub_checks.append("ports 8080:5000")
            else:
                sub_checks.append(f"MISS port 8080:5000, got {ports}")

            # Check depends_on includes db and cache
            depends = web.get('depends_on', [])
            if isinstance(depends, dict):
                dep_names = set(depends.keys())
            elif isinstance(depends, list):
                dep_names = set(depends)
            else:
                dep_names = set()
            if 'db' in dep_names and 'cache' in dep_names:
                sub_score += 0.06
                sub_checks.append("depends_on [db, cache]")
            else:
                sub_checks.append(f"MISS depends_on [db, cache], got {dep_names}")

            # Check environment has DATABASE_URL and REDIS_URL
            env = web.get('environment', {})
            if isinstance(env, dict):
                env_dict = env
            elif isinstance(env, list):
                env_dict = {}
                for item in env:
                    if '=' in str(item):
                        k, v = str(item).split('=', 1)
                        env_dict[k] = v
            else:
                env_dict = {}

            has_db_url = 'DATABASE_URL' in env_dict and 'db' in str(env_dict.get('DATABASE_URL', ''))
            has_redis_url = 'REDIS_URL' in env_dict and 'cache' in str(env_dict.get('REDIS_URL', ''))
            if has_db_url and has_redis_url:
                sub_score += 0.06
                sub_checks.append("env DATABASE_URL and REDIS_URL present and reference service names")
            else:
                if not has_db_url:
                    sub_checks.append(f"MISS DATABASE_URL pointing to db, got {env_dict.get('DATABASE_URL')}")
                if not has_redis_url:
                    sub_checks.append(f"MISS REDIS_URL pointing to cache, got {env_dict.get('REDIS_URL')}")

            if sub_score >= 0.19:
                print(f"PASS: Component 5 — web service correct ({sub_score:.2f} pts) [{', '.join(sub_checks)}]")
                total_score += sub_score
            elif sub_score > 0:
                print(f"PARTIAL: Component 5 — web service ({sub_score:.2f} pts) [{', '.join(sub_checks)}]")
                total_score += sub_score
            else:
                print(f"FAIL: Component 5 — web service ({sub_score:.2f} pts) [{', '.join(sub_checks)}]")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: appnet network declared as bridge (0.1 points)
    try:
        networks = data.get('networks', {})
        if not isinstance(networks, dict):
            print(f"FAIL: Component 6 — 'networks' key missing or not a dict")
        elif 'appnet' not in networks:
            print(f"FAIL: Component 6 — 'appnet' network not declared, found {list(networks.keys())}")
        else:
            appnet = networks.get('appnet', {})
            # Check driver is bridge (or default which is bridge)
            driver = appnet.get('driver', 'bridge') if isinstance(appnet, dict) else 'bridge'
            if driver == 'bridge':
                print(f"PASS: Component 6 — appnet network declared with bridge driver (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 6 — appnet driver is '{driver}', expected 'bridge'")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: db_data volume declared at top level (0.1 points)
    try:
        volumes = data.get('volumes', {})
        if not isinstance(volumes, dict):
            print(f"FAIL: Component 7 — 'volumes' key missing or not a dict")
        elif 'db_data' not in volumes:
            print(f"FAIL: Component 7 — 'db_data' volume not declared, found {list(volumes.keys()) if isinstance(volumes, dict) else volumes}")
        else:
            print(f"PASS: Component 7 — db_data volume declared at top level (0.1 pts)")
            total_score += 0.1
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
