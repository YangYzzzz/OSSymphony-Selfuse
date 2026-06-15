"""
Reward Script: Docker health check configuration for webapp container
Task ID: os_adm_054
Domain: os (docker-compose configuration)
Scoring:
  Component 1 (0.20) - healthcheck section exists under webapp service
  Component 2 (0.25) - test command is correct (CMD curl -f http://localhost:8080/health)
  Component 3 (0.20) - interval is 30s
  Component 4 (0.15) - timeout is 10s
  Component 5 (0.10) - retries is 3
  Component 6 (0.10) - start_period is 40s
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'os_adm_054'
COMPOSE_FILE = '/opt/webapp/docker-compose.yml'


def normalize_duration(value):
    """Normalize a duration value to seconds for comparison.
    Handles strings like '30s', '10s', integers, etc.
    Returns integer seconds or None if unparsable.
    """
    if value is None:
        return None
    val = str(value).strip().lower()
    # Match patterns like '30s', '10s', '40s'
    m = re.match(r'^(\d+)\s*s?$', val)
    if m:
        return int(m.group(1))
    # Match patterns like '1m', '1m30s'
    m = re.match(r'^(\d+)\s*m(?:\s*(\d+)\s*s)?$', val)
    if m:
        return int(m.group(1)) * 60 + (int(m.group(2)) if m.group(2) else 0)
    return None


def verify_task():
    """
    Verify that docker-compose.yml has proper health check configuration.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load and parse the docker-compose.yml file
    try:
        import yaml
        with open(COMPOSE_FILE, 'r') as f:
            compose = yaml.safe_load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot load {COMPOSE_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Navigate to webapp service
    try:
        services = compose.get('services', {})
        webapp = services.get('webapp', None)
        if webapp is None:
            print("CRITICAL: No 'webapp' service found in docker-compose.yml")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot parse services: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: healthcheck section exists (0.20 points)
    try:
        healthcheck = webapp.get('healthcheck', None)
        if healthcheck is not None and isinstance(healthcheck, dict):
            print(f"PASS: Component 1 - healthcheck section exists (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - healthcheck section not found in webapp service")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: test command is correct (0.25 points)
    # Expected: ["CMD", "curl", "-f", "http://localhost:8080/health"] or equivalent
    try:
        if healthcheck is None:
            print("FAIL: Component 2 - no healthcheck section")
        else:
            test_cmd = healthcheck.get('test', None)
            if test_cmd is not None:
                # Normalize test command for comparison
                # YAML may parse it as a list or string
                if isinstance(test_cmd, list):
                    # Check for CMD-form: ["CMD", "curl", "-f", "http://localhost:8080/health"]
                    cmd_str = ' '.join(str(x) for x in test_cmd)
                elif isinstance(test_cmd, str):
                    cmd_str = test_cmd
                else:
                    cmd_str = str(test_cmd)

                # Check the essential parts: curl, -f flag, and /health endpoint
                has_cmd_prefix = (isinstance(test_cmd, list) and len(test_cmd) > 0
                                  and str(test_cmd[0]).upper() in ('CMD', 'CMD-SHELL'))
                has_curl = 'curl' in cmd_str.lower()
                has_fail_flag = '-f' in cmd_str
                has_health_endpoint = 'http://localhost:8080/health' in cmd_str

                if has_curl and has_fail_flag and has_health_endpoint:
                    print(f"PASS: Component 2 - test command correct: {test_cmd} (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 - test command incomplete. "
                          f"curl={has_curl}, -f={has_fail_flag}, endpoint={has_health_endpoint}. "
                          f"Found: {test_cmd}")
            else:
                print("FAIL: Component 2 - test field not found in healthcheck")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: interval is 30s (0.20 points)
    try:
        if healthcheck is None:
            print("FAIL: Component 3 - no healthcheck section")
        else:
            interval = healthcheck.get('interval', None)
            interval_secs = normalize_duration(interval)
            if interval_secs == 30:
                print(f"PASS: Component 3 - interval is 30s (raw: {interval}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 - expected interval 30s, found: {interval} ({interval_secs}s)")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: timeout is 10s (0.15 points)
    try:
        if healthcheck is None:
            print("FAIL: Component 4 - no healthcheck section")
        else:
            timeout = healthcheck.get('timeout', None)
            timeout_secs = normalize_duration(timeout)
            if timeout_secs == 10:
                print(f"PASS: Component 4 - timeout is 10s (raw: {timeout}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 - expected timeout 10s, found: {timeout} ({timeout_secs}s)")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: retries is 3 (0.10 points)
    try:
        if healthcheck is None:
            print("FAIL: Component 5 - no healthcheck section")
        else:
            retries = healthcheck.get('retries', None)
            if retries is not None and int(retries) == 3:
                print(f"PASS: Component 5 - retries is 3 (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 - expected retries 3, found: {retries}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: start_period is 40s (0.10 points)
    try:
        if healthcheck is None:
            print("FAIL: Component 6 - no healthcheck section")
        else:
            start_period = healthcheck.get('start_period', None)
            sp_secs = normalize_duration(start_period)
            if sp_secs == 40:
                print(f"PASS: Component 6 - start_period is 40s (raw: {start_period}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 - expected start_period 40s, found: {start_period} ({sp_secs}s)")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(COMPOSE_FILE):
    print(f"File not found: {COMPOSE_FILE}")
    print("REWARD: 0.0")
else:
    verify_task()
