"""
Reward Script: Kubernetes-like multi-container orchestration with Docker Compose
Task ID: os_adm_069
Domain: os (Docker/system administration)
Scoring:
  - Component 1: Resource limits on all 3 services (0.25 pts)
  - Component 2: Health checks on all 3 services (0.25 pts)
  - Component 3: Loki logging driver + Loki service (0.20 pts)
  - Component 4: Rolling update script exists and is executable (0.15 pts)
  - Component 5: Grafana service + Loki datasource provisioning (0.15 pts)
"""

import os
import stat
import yaml

WORKDIR = '/home/user'
TASK_ID = 'os_adm_069'
COMPOSE_PATH = f'{WORKDIR}/orchestration-project/docker-compose.yml'
ROLLING_SCRIPT = '/usr/local/bin/rolling_update.sh'
GRAFANA_LOKI_DS = f'{WORKDIR}/orchestration-project/grafana/provisioning/datasources/loki.yml'

# Expected resource limits per task context
EXPECTED_LIMITS = {
    'frontend': {'memory': '512M', 'cpus': '1.0'},
    'backend':  {'memory': '1G',   'cpus': '1.0'},
    'cache':    {'memory': '256M', 'cpus': '1.0'},
}

APP_SERVICES = ['frontend', 'backend', 'cache']


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load docker-compose.yml
    try:
        with open(COMPOSE_PATH, 'r') as f:
            compose = yaml.safe_load(f)
        services = compose.get('services', {})
        print(f"INFO: Loaded docker-compose.yml with services: {list(services.keys())}")
    except Exception as e:
        print(f"CRITICAL: Cannot load {COMPOSE_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check all 3 app services exist
    for svc in APP_SERVICES:
        if svc not in services:
            print(f"CRITICAL: Service '{svc}' not found in docker-compose.yml")
            print("REWARD: 0.0")
            return 0.0

    # Component 1: Resource limits on all 3 services (0.25 pts)
    # Task requires: frontend 512MB, backend 1GB, cache 256MB; each max 1.0 CPU
    try:
        limits_ok = 0
        for svc in APP_SERVICES:
            svc_cfg = services[svc]
            deploy = svc_cfg.get('deploy', {})
            resources = deploy.get('resources', {})
            limits = resources.get('limits', {})

            mem = str(limits.get('memory', '')).strip()
            cpus = str(limits.get('cpus', '')).strip()

            expected_mem = EXPECTED_LIMITS[svc]['memory']
            expected_cpus = EXPECTED_LIMITS[svc]['cpus']

            # Normalize memory comparisons (e.g., 512M vs 512m)
            mem_match = mem.upper() == expected_mem.upper()
            cpus_match = cpus == expected_cpus

            if mem_match and cpus_match:
                print(f"  PASS: {svc} limits: memory={mem}, cpus={cpus}")
                limits_ok += 1
            else:
                print(f"  FAIL: {svc} limits: memory={mem} (expected {expected_mem}), cpus={cpus} (expected {expected_cpus})")

        if limits_ok == 3:
            print(f"PASS: Component 1 - All 3 services have correct resource limits (0.25 pts)")
            total_score += 0.25
        elif limits_ok > 0:
            partial = round(0.25 * limits_ok / 3, 2)
            print(f"PARTIAL: Component 1 - {limits_ok}/3 services have correct limits ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No services have resource limits configured")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Health checks on all 3 services (0.25 pts)
    # Each service should have a healthcheck with test, interval, timeout, retries
    try:
        health_ok = 0
        for svc in APP_SERVICES:
            svc_cfg = services[svc]
            hc = svc_cfg.get('healthcheck', {})
            test = hc.get('test', None)

            if test is not None and len(test) > 0:
                # Verify healthcheck has required fields
                has_interval = 'interval' in hc
                has_timeout = 'timeout' in hc
                has_retries = 'retries' in hc
                if has_interval and has_timeout and has_retries:
                    print(f"  PASS: {svc} healthcheck configured: test={test}")
                    health_ok += 1
                else:
                    missing = []
                    if not has_interval: missing.append('interval')
                    if not has_timeout: missing.append('timeout')
                    if not has_retries: missing.append('retries')
                    print(f"  PARTIAL: {svc} healthcheck missing fields: {missing}")
            else:
                print(f"  FAIL: {svc} has no healthcheck configured")

        if health_ok == 3:
            print(f"PASS: Component 2 - All 3 services have health checks (0.25 pts)")
            total_score += 0.25
        elif health_ok > 0:
            partial = round(0.25 * health_ok / 3, 2)
            print(f"PARTIAL: Component 2 - {health_ok}/3 services have health checks ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No services have health checks configured")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Loki logging driver for app services + Loki service defined (0.20 pts)
    # All 3 app services should use loki log driver; a loki service must exist
    try:
        loki_logging_ok = 0
        for svc in APP_SERVICES:
            svc_cfg = services[svc]
            logging_cfg = svc_cfg.get('logging', {})
            driver = logging_cfg.get('driver', '')
            if driver == 'loki':
                print(f"  PASS: {svc} uses loki logging driver")
                loki_logging_ok += 1
            else:
                print(f"  FAIL: {svc} logging driver is '{driver}', expected 'loki'")

        loki_service_exists = 'loki' in services
        if loki_service_exists:
            print(f"  PASS: loki service defined in compose")
        else:
            print(f"  FAIL: loki service not defined in compose")

        # All 3 services with loki driver + loki service = full points
        if loki_logging_ok == 3 and loki_service_exists:
            print(f"PASS: Component 3 - Loki logging fully configured (0.20 pts)")
            total_score += 0.20
        elif loki_logging_ok > 0 or loki_service_exists:
            # Partial: loki service worth 0.05, each service driver worth 0.05
            partial = 0.0
            if loki_service_exists:
                partial += 0.05
            partial += round(0.05 * loki_logging_ok, 2)
            partial = min(partial, 0.20)
            print(f"PARTIAL: Component 3 - loki logging partially configured ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - No loki logging configured")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Rolling update script exists and is executable (0.15 pts)
    # Must be at /usr/local/bin/rolling_update.sh, executable, and contain relevant content
    try:
        if os.path.isfile(ROLLING_SCRIPT):
            mode = stat.S_IMODE(os.stat(ROLLING_SCRIPT).st_mode)
            is_executable = bool(mode & stat.S_IXUSR)

            with open(ROLLING_SCRIPT, 'r') as f:
                script_content = f.read()

            # Verify script contains key rolling update logic
            has_service_arg = 'SERVICE' in script_content.upper() or '$1' in script_content or '${1' in script_content
            has_health_wait = 'health' in script_content.lower()
            has_docker = 'docker' in script_content.lower()

            if is_executable and has_service_arg and has_health_wait and has_docker:
                print(f"PASS: Component 4 - Rolling update script exists, executable, with proper content (0.15 pts)")
                total_score += 0.15
            elif is_executable and has_docker:
                print(f"PARTIAL: Component 4 - Script exists and executable but incomplete logic (0.08 pts)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 4 - Script exists but not executable or missing content (exec={is_executable}, docker={has_docker}, health={has_health_wait})")
        else:
            print(f"FAIL: Component 4 - Rolling update script not found at {ROLLING_SCRIPT}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Grafana service + Loki datasource provisioning (0.15 pts)
    # Grafana service in compose + provisioning config for Loki datasource
    try:
        grafana_in_compose = 'grafana' in services
        loki_ds_exists = os.path.isfile(GRAFANA_LOKI_DS)

        loki_ds_valid = False
        if loki_ds_exists:
            with open(GRAFANA_LOKI_DS, 'r') as f:
                ds_config = yaml.safe_load(f)
            datasources = ds_config.get('datasources', [])
            for ds in datasources:
                if ds.get('type', '') == 'loki':
                    loki_ds_valid = True
                    break

        if grafana_in_compose and loki_ds_valid:
            print(f"PASS: Component 5 - Grafana service with Loki datasource provisioning (0.15 pts)")
            total_score += 0.15
        elif grafana_in_compose:
            print(f"PARTIAL: Component 5 - Grafana service exists but no valid Loki datasource (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 5 - Grafana service not in compose")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(COMPOSE_PATH):
    print(f"File not found: {COMPOSE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
