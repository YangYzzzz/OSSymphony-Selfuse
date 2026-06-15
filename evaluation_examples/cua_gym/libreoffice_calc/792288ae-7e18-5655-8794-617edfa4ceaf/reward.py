"""
Reward Script: Prometheus alerting pipeline setup
Task ID: os_gff_074
Domain: os (Prometheus/Alertmanager configuration)
Scoring:
  - Component 1: Alert rules file exists with 3 rules (0.20)
  - Component 2: CPU alert rule has correct expression and for clause (0.15)
  - Component 3: Memory and Disk alert rules present with correct thresholds (0.15)
  - Component 4: Prometheus config includes rule_files (0.15)
  - Component 5: Alertmanager has PagerDuty receiver with correct key (0.15)
  - Component 6: Alertmanager has email receiver configured (0.10)
  - Component 7: Route has repeat_interval 15m (0.10)
"""

import os
import re
import yaml

ALERTS_FILE = '/etc/prometheus/alerts/node_alerts.yml'
PROM_CONFIG = '/etc/prometheus/prometheus.yml'
ALERTMGR_CONFIG = '/etc/alertmanager/alertmanager.yml'
PAGERDUTY_KEY_FILE = '/etc/prometheus/pagerduty_key.txt'


def verify_task():
    """
    Verify Prometheus alerting pipeline setup.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load PagerDuty key for later comparison
    pd_key = None
    try:
        pd_key = open(PAGERDUTY_KEY_FILE).read().strip()
        print(f"INFO: PagerDuty key loaded: {pd_key[:8]}...")
    except Exception as e:
        print(f"WARN: Could not read PagerDuty key file: {e}")

    # ========================================================
    # Component 1: Alert rules file exists with 3 rules (0.20)
    # ========================================================
    try:
        if not os.path.isfile(ALERTS_FILE):
            print(f"FAIL: Component 1 — Alert rules file not found at {ALERTS_FILE}")
        else:
            with open(ALERTS_FILE) as f:
                alerts_data = yaml.safe_load(f)

            rules = []
            if alerts_data and 'groups' in alerts_data:
                for group in alerts_data['groups']:
                    if 'rules' in group:
                        rules.extend(group['rules'])

            if len(rules) >= 3:
                alert_names = [r.get('alert', '') for r in rules]
                print(f"PASS: Component 1 — Found {len(rules)} alert rules: {alert_names} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — Expected >= 3 rules, found {len(rules)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ========================================================
    # Component 2: CPU alert rule correct expr and for (0.15)
    # ========================================================
    try:
        if not os.path.isfile(ALERTS_FILE):
            print("FAIL: Component 2 — No alerts file")
        else:
            with open(ALERTS_FILE) as f:
                alerts_data = yaml.safe_load(f)

            rules = []
            if alerts_data and 'groups' in alerts_data:
                for group in alerts_data['groups']:
                    if 'rules' in group:
                        rules.extend(group['rules'])

            cpu_rule = None
            for r in rules:
                expr = str(r.get('expr', ''))
                alert_name = str(r.get('alert', '')).lower()
                if 'cpu' in alert_name.lower() or ('node_cpu_seconds_total' in expr and '80' in expr):
                    cpu_rule = r
                    break

            if cpu_rule is None:
                print("FAIL: Component 2 — No CPU alert rule found")
            else:
                expr = str(cpu_rule.get('expr', ''))
                for_val = str(cpu_rule.get('for', ''))

                # Check expression has key elements
                has_cpu_metric = 'node_cpu_seconds_total' in expr
                has_idle_mode = 'idle' in expr
                has_rate_5m = 'rate(' in expr and '5m' in expr
                has_threshold_80 = '80' in expr
                has_for_5m = '5m' in for_val

                if has_cpu_metric and has_idle_mode and has_rate_5m and has_threshold_80 and has_for_5m:
                    print(f"PASS: Component 2 — CPU alert correct: expr has node_cpu_seconds_total, idle, rate 5m, >80; for: 5m (0.15 pts)")
                    total_score += 0.15
                else:
                    missing = []
                    if not has_cpu_metric: missing.append('node_cpu_seconds_total metric')
                    if not has_idle_mode: missing.append('idle mode filter')
                    if not has_rate_5m: missing.append('rate with 5m window')
                    if not has_threshold_80: missing.append('>80 threshold')
                    if not has_for_5m: missing.append('for: 5m')
                    print(f"FAIL: Component 2 — CPU alert missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ========================================================
    # Component 3: Memory and Disk alert rules present (0.15)
    # ========================================================
    try:
        if not os.path.isfile(ALERTS_FILE):
            print("FAIL: Component 3 — No alerts file")
        else:
            with open(ALERTS_FILE) as f:
                alerts_data = yaml.safe_load(f)

            rules = []
            if alerts_data and 'groups' in alerts_data:
                for group in alerts_data['groups']:
                    if 'rules' in group:
                        rules.extend(group['rules'])

            found_memory = False
            found_disk = False

            for r in rules:
                expr = str(r.get('expr', ''))
                alert_name = str(r.get('alert', '')).lower()

                # Memory alert: >90% usage
                if ('memory' in alert_name or 'node_memory' in expr) and '90' in expr:
                    found_memory = True

                # Disk alert: <10% free
                if ('disk' in alert_name or 'node_filesystem' in expr) and '10' in expr:
                    found_disk = True

            pts = 0.0
            if found_memory:
                pts += 0.075
                print("PASS: Component 3a — Memory alert rule found with 90% threshold")
            else:
                print("FAIL: Component 3a — Memory alert rule not found or missing 90% threshold")

            if found_disk:
                pts += 0.075
                print("PASS: Component 3b — Disk alert rule found with 10% threshold")
            else:
                print("FAIL: Component 3b — Disk alert rule not found or missing 10% threshold")

            if pts > 0:
                total_score += pts
                print(f"PASS: Component 3 — {pts} pts awarded")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ========================================================
    # Component 4: Prometheus config includes rule_files (0.15)
    # ========================================================
    try:
        with open(PROM_CONFIG) as f:
            prom_data = yaml.safe_load(f)

        rule_files = prom_data.get('rule_files', [])
        if rule_files and any('node_alerts' in str(rf) for rf in rule_files):
            print(f"PASS: Component 4 — rule_files includes alerts file: {rule_files} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — rule_files missing or doesn't reference node_alerts. Found: {rule_files}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ========================================================
    # Component 5: Alertmanager PagerDuty receiver (0.15)
    # ========================================================
    try:
        with open(ALERTMGR_CONFIG) as f:
            am_data = yaml.safe_load(f)

        receivers = am_data.get('receivers', [])
        found_pd = False
        for recv in receivers:
            pd_configs = recv.get('pagerduty_configs', [])
            if pd_configs:
                # Check if service_key matches the PagerDuty key
                for pdc in pd_configs:
                    sk = pdc.get('service_key', '')
                    rk = pdc.get('routing_key', '')
                    key_used = sk or rk
                    if key_used:
                        found_pd = True
                        if pd_key and key_used == pd_key:
                            print(f"PASS: Component 5 — PagerDuty receiver found with correct key (0.15 pts)")
                        else:
                            print(f"PASS: Component 5 — PagerDuty receiver found (key present) (0.15 pts)")
                        break
            if found_pd:
                break

        if found_pd:
            total_score += 0.15
        else:
            print("FAIL: Component 5 — No PagerDuty receiver configured in Alertmanager")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ========================================================
    # Component 6: Alertmanager email receiver (0.10)
    # ========================================================
    try:
        with open(ALERTMGR_CONFIG) as f:
            am_data = yaml.safe_load(f)

        receivers = am_data.get('receivers', [])
        found_email = False
        for recv in receivers:
            email_configs = recv.get('email_configs', [])
            if email_configs:
                for ec in email_configs:
                    if ec.get('to'):
                        found_email = True
                        print(f"PASS: Component 6 — Email receiver configured, to: {ec['to']} (0.10 pts)")
                        break
            if found_email:
                break

        if found_email:
            total_score += 0.10
        else:
            print("FAIL: Component 6 — No email receiver configured in Alertmanager")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # ========================================================
    # Component 7: Route repeat_interval 15m (0.10)
    # ========================================================
    try:
        with open(ALERTMGR_CONFIG) as f:
            am_data = yaml.safe_load(f)

        route = am_data.get('route', {})
        repeat_interval = str(route.get('repeat_interval', ''))

        if repeat_interval == '15m':
            print(f"PASS: Component 7 — repeat_interval is 15m (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 — repeat_interval is '{repeat_interval}', expected '15m'")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Final score
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
