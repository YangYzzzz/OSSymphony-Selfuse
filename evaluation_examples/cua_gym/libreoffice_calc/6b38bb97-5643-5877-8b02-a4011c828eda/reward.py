"""
Reward Script: Zero-downtime deployment pipeline for Node.js with Nginx upstream switching
Task ID: os_adm_061
Domain: os (system administration)
Scoring:
  Component 1: Deploy script exists and is executable           — 0.20 pts
  Component 2: Deploy script contains key deployment logic      — 0.25 pts
  Component 3: Nginx upstream points to port 3001 only          — 0.20 pts
  Component 4: PM2 has app-v2 running on port 3001              — 0.20 pts
  Component 5: PM2 does NOT have app-v1 running                 — 0.15 pts
  Total: 1.0
"""

import os
import stat
import json
import re

DEPLOY_SCRIPT = '/usr/local/bin/deploy_nodejs.sh'
NGINX_CONF = '/etc/nginx/sites-available/nodejs-app'
PM2_HOME = os.path.expanduser('~/.pm2')


def get_pm2_processes():
    """Read PM2 process list via pm2 jlist (live status) or dump file (fallback).
    Returns list of normalized dicts with keys: name, status, port.
    """
    processes = []

    # Prefer pm2 jlist for live status
    try:
        stream = os.popen('pm2 jlist 2>/dev/null')
        raw = stream.read()
        stream.close()
        data = json.loads(raw)
        for proc in data:
            name = proc.get('name', '')
            pm2_env = proc.get('pm2_env', {})
            status = pm2_env.get('status', 'unknown')
            port = str(pm2_env.get('env', {}).get('PORT', pm2_env.get('PORT', '')))
            processes.append({'name': name, 'status': status, 'port': port})
        if processes:
            return processes
    except Exception:
        pass

    # Fallback: dump file (flat structure, no live status)
    dump_path = os.path.join(PM2_HOME, 'dump.pm2')
    try:
        with open(dump_path, 'r') as f:
            data = json.load(f)
        for proc in data:
            name = proc.get('name', '')
            # Dump uses flat structure: PORT and status at top level
            port = str(proc.get('PORT', proc.get('env', {}).get('PORT', '')))
            # In dump, status may be missing; if process is in dump, consider it was running
            status = proc.get('status', 'online')
            processes.append({'name': name, 'status': status, 'port': port})
        return processes
    except Exception:
        pass

    return []


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================
    # Component 1: Deploy script exists and is executable (0.20)
    # =========================================================
    # INITIAL: script does NOT exist -> FAIL (correct)
    # GOLDEN: script exists with 755 perms -> PASS
    try:
        if os.path.isfile(DEPLOY_SCRIPT):
            mode = stat.S_IMODE(os.stat(DEPLOY_SCRIPT).st_mode)
            # Check at least owner-execute bit is set
            if mode & stat.S_IXUSR:
                print(f"PASS: Component 1 — deploy script exists and is executable (mode={oct(mode)}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — deploy script exists but not executable (mode={oct(mode)})")
        else:
            print(f"FAIL: Component 1 — deploy script not found at {DEPLOY_SCRIPT}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================
    # Component 2: Deploy script contains key deployment logic (0.25)
    # =========================================================
    # Checks for: health check, nginx upstream switching, PM2 start v2,
    # rollback logic, and stop of old version.
    # INITIAL: no script -> FAIL
    # GOLDEN: script with all logic -> PASS
    try:
        if os.path.isfile(DEPLOY_SCRIPT):
            with open(DEPLOY_SCRIPT, 'r') as f:
                script_content = f.read()

            sub_score = 0.0
            checks = {
                'health_check': bool(re.search(r'(health|curl.*localhost.*3001|curl.*127\.0\.0\.1.*3001)', script_content, re.IGNORECASE)),
                'pm2_start_v2': bool(re.search(r'pm2\s+start.*app-v2|pm2\s+start.*/opt/app-v2', script_content)),
                'nginx_reload': bool(re.search(r'nginx\s+(-s\s+reload|-t|reload)', script_content)),
                'upstream_switch': bool(re.search(r'(upstream|3001)', script_content) and re.search(r'(tee|sed|cat).*nginx', script_content, re.IGNORECASE)),
                'rollback': bool(re.search(r'(rollback|ROLLBACK|revert|backup)', script_content, re.IGNORECASE)),
            }

            passed = sum(1 for v in checks.values() if v)
            sub_score = 0.25 * (passed / len(checks))

            for name, result in checks.items():
                status = "found" if result else "MISSING"
                print(f"  Component 2 sub-check '{name}': {status}")

            if sub_score > 0:
                print(f"PASS: Component 2 — deploy script logic ({passed}/{len(checks)} checks) ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 — deploy script missing all key logic patterns")
        else:
            print(f"FAIL: Component 2 — no deploy script to analyze")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================
    # Component 3: Nginx upstream points to port 3001 only (0.20)
    # =========================================================
    # INITIAL: upstream points to 3000 -> FAIL
    # GOLDEN: upstream points to 3001 only -> PASS
    try:
        if os.path.isfile(NGINX_CONF):
            with open(NGINX_CONF, 'r') as f:
                nginx_content = f.read()

            # Extract upstream block
            upstream_match = re.search(r'upstream\s+\w+\s*\{([^}]+)\}', nginx_content)
            if upstream_match:
                upstream_block = upstream_match.group(1)
                has_3001 = bool(re.search(r'server\s+127\.0\.0\.1:3001', upstream_block))
                has_3000 = bool(re.search(r'server\s+127\.0\.0\.1:3000', upstream_block))

                if has_3001 and not has_3000:
                    print(f"PASS: Component 3 — Nginx upstream points to port 3001 only (0.20 pts)")
                    total_score += 0.20
                elif has_3001 and has_3000:
                    print(f"FAIL: Component 3 — Nginx upstream still has both 3000 and 3001")
                else:
                    print(f"FAIL: Component 3 — Nginx upstream does not point to port 3001")
            else:
                print(f"FAIL: Component 3 — no upstream block found in Nginx config")
        else:
            print(f"FAIL: Component 3 — Nginx config not found at {NGINX_CONF}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================
    # Component 4: PM2 has app-v2 running on port 3001 (0.20)
    # =========================================================
    # INITIAL: only app-v1 on port 3000 -> FAIL
    # GOLDEN: app-v2 on port 3001, online -> PASS
    try:
        processes = get_pm2_processes()
        v2_found = False
        for proc in processes:
            if proc['name'] == 'app-v2' and proc['status'] == 'online' and proc['port'] == '3001':
                v2_found = True
                break

        if v2_found:
            print(f"PASS: Component 4 — app-v2 running on port 3001 via PM2 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — app-v2 not found running on port 3001 in PM2 (processes: {processes})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================
    # Component 5: PM2 does NOT have app-v1 running (0.15)
    # =========================================================
    # INITIAL: app-v1 is online -> FAIL (this check awards points when v1 is absent)
    # GOLDEN: app-v1 is stopped/deleted -> PASS
    try:
        processes = get_pm2_processes()
        v1_running = False
        for proc in processes:
            if proc['name'] == 'app-v1' and proc['status'] == 'online':
                v1_running = True
                break

        if not v1_running:
            print(f"PASS: Component 5 — app-v1 is not running in PM2 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — app-v1 is still running in PM2")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
