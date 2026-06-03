"""
Reward Script: Nginx Load Balancer Configuration
Task ID: os_adm_037
Domain: os (nginx configuration)
Scoring:
  Component 1: upstream block with least_conn (0.20)
  Component 2: three servers with correct IPs, max_fails, fail_timeout (0.30)
  Component 3: proxy_pass to upstream group in server/location block (0.15)
  Component 4: proxy_connect_timeout and proxy_read_timeout set (0.15)
  Component 5: sites-enabled symlink exists for loadbalancer (0.20)
"""

import os
import re

CONFIG_PATH = '/etc/nginx/sites-available/loadbalancer'
SYMLINK_PATH = '/etc/nginx/sites-enabled/loadbalancer'

def verify_task():
    """
    Verify Nginx load balancer configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: config file must exist
    if not os.path.isfile(CONFIG_PATH):
        print(f"CRITICAL: Config file not found at {CONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(CONFIG_PATH, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read config file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Normalize whitespace for easier matching
    # but keep original for detailed checks
    content_stripped = content.strip()

    # Component 1: upstream block with least_conn directive (0.20 points)
    try:
        has_upstream = bool(re.search(r'upstream\s+\w+\s*\{', content))
        has_least_conn = bool(re.search(r'least_conn\s*;', content))
        if has_upstream and has_least_conn:
            print(f"PASS: Component 1 — upstream block with least_conn found (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not has_upstream:
                missing.append("upstream block")
            if not has_least_conn:
                missing.append("least_conn directive")
            print(f"FAIL: Component 1 — missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Three upstream servers with correct IPs/ports and health check params (0.30 points)
    try:
        expected_servers = [
            ('10.0.1.10', '8080'),
            ('10.0.1.11', '8080'),
            ('10.0.1.12', '8080'),
        ]
        # Match server lines within upstream block
        server_pattern = r'server\s+([\d.]+):(\d+)\s+.*?max_fails\s*=\s*(\d+)\s+.*?fail_timeout\s*=\s*(\d+)s'
        server_matches = re.findall(server_pattern, content)

        servers_found = [(m[0], m[1]) for m in server_matches]
        all_servers_present = all(
            (ip, port) in servers_found for ip, port in expected_servers
        )
        all_health_correct = all(
            m[2] == '3' and m[3] == '30' for m in server_matches
        )

        if len(server_matches) >= 3 and all_servers_present and all_health_correct:
            print(f"PASS: Component 2 — all 3 servers with max_fails=3 fail_timeout=30s (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — found {len(server_matches)} valid server entries: {server_matches}")
            if not all_servers_present:
                print(f"  Missing servers: expected {expected_servers}, found {servers_found}")
            if not all_health_correct:
                print(f"  Health check params incorrect for some servers")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: proxy_pass to the upstream group (0.15 points)
    try:
        # proxy_pass should reference an upstream name defined in the upstream block
        upstream_name_match = re.search(r'upstream\s+(\w+)\s*\{', content)
        proxy_pass_match = re.search(r'proxy_pass\s+https?://(\w+)\s*;', content)

        if upstream_name_match and proxy_pass_match:
            upstream_name = upstream_name_match.group(1)
            proxy_target = proxy_pass_match.group(1)
            if upstream_name == proxy_target:
                print(f"PASS: Component 3 — proxy_pass http://{proxy_target} matches upstream {upstream_name} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — proxy_pass targets '{proxy_target}' but upstream is '{upstream_name}'")
        else:
            print(f"FAIL: Component 3 — upstream name or proxy_pass not found")
            if not upstream_name_match:
                print(f"  No upstream block found")
            if not proxy_pass_match:
                print(f"  No proxy_pass directive found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: proxy_connect_timeout and proxy_read_timeout configured (0.15 points)
    try:
        has_connect_timeout = bool(re.search(r'proxy_connect_timeout\s+\d+', content))
        has_read_timeout = bool(re.search(r'proxy_read_timeout\s+\d+', content))

        if has_connect_timeout and has_read_timeout:
            connect_val = re.search(r'proxy_connect_timeout\s+(\d+)', content).group(1)
            read_val = re.search(r'proxy_read_timeout\s+(\d+)', content).group(1)
            print(f"PASS: Component 4 — proxy_connect_timeout={connect_val}s, proxy_read_timeout={read_val}s (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_connect_timeout:
                missing.append("proxy_connect_timeout")
            if not has_read_timeout:
                missing.append("proxy_read_timeout")
            print(f"FAIL: Component 4 — missing timeout directives: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: sites-enabled symlink for loadbalancer (0.20 points)
    try:
        if os.path.islink(SYMLINK_PATH) or os.path.isfile(SYMLINK_PATH):
            # Verify it points to the correct target
            if os.path.islink(SYMLINK_PATH):
                target = os.readlink(SYMLINK_PATH)
                if 'loadbalancer' in target:
                    print(f"PASS: Component 5 — sites-enabled symlink -> {target} (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 5 — symlink points to {target}, not loadbalancer")
            else:
                # It's a regular file copy, also acceptable
                print(f"PASS: Component 5 — loadbalancer present in sites-enabled (0.20 pts)")
                total_score += 0.20
        else:
            print(f"FAIL: Component 5 — no loadbalancer in sites-enabled")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
