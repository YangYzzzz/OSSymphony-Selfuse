"""
Reward Script: Capacity Planning Automation System
Task ID: os_adm_085
Domain: os (system administration)
Scoring:
  Component 1 (0.20): Script exists at /usr/local/bin/capacity_planner.py and is executable
  Component 2 (0.25): Script uses scipy linregress and reads metric CSV files
  Component 3 (0.15): Script has correct thresholds (CPU 85%, mem 90%, disk 95%) and 14-day alert horizon
  Component 4 (0.20): HTML report exists in /var/reports/ with required content
  Component 5 (0.10): Script uses Jinja2 template and references ops@example.com alert email
  Component 6 (0.10): Cron job configured for weekly Monday 8 AM
"""

import os
import stat
import glob
import re

SCRIPT_PATH = '/usr/local/bin/capacity_planner.py'
REPORTS_DIR = '/var/reports'
METRICS_DIR = '/var/lib/metrics'


def verify_task():
    """
    Verify capacity planning automation system.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Script exists at correct path and is executable (0.20 points)
    try:
        if os.path.isfile(SCRIPT_PATH):
            mode = os.stat(SCRIPT_PATH).st_mode
            is_executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
            if is_executable:
                print(f"PASS: Component 1 - Script exists at {SCRIPT_PATH} and is executable (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 - Script exists but is not executable (mode: {oct(mode)})")
        else:
            print(f"FAIL: Component 1 - Script not found at {SCRIPT_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Early exit if script doesn't exist (can't check content)
    if total_score < 0.1:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read script content for subsequent checks
    try:
        with open(SCRIPT_PATH, 'r') as f:
            script_content = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read script: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Script uses scipy linregress and reads metric CSVs (0.25 points)
    try:
        has_scipy = 'scipy' in script_content
        has_linregress = 'linregress' in script_content
        has_csv_reading = ('csv' in script_content.lower() and
                          ('/var/lib/metrics' in script_content or 'metrics' in script_content))

        sub_score = 0.0
        if has_scipy and has_linregress:
            sub_score += 0.15
            print(f"  - scipy.stats.linregress: FOUND")
        else:
            print(f"  - scipy.stats.linregress: MISSING (scipy={has_scipy}, linregress={has_linregress})")

        if has_csv_reading:
            sub_score += 0.10
            print(f"  - CSV metric reading: FOUND")
        else:
            print(f"  - CSV metric reading: MISSING")

        if sub_score > 0:
            print(f"PASS: Component 2 - Linear regression and CSV reading ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 2 - Missing scipy linregress and/or CSV reading")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Correct thresholds and alert horizon (0.15 points)
    try:
        # Check for threshold values: CPU 85%, mem 90%, disk 95%
        has_cpu_85 = bool(re.search(r'85', script_content))
        has_mem_90 = bool(re.search(r'90', script_content))
        has_disk_95 = bool(re.search(r'95', script_content))
        has_14_day = bool(re.search(r'14', script_content))

        threshold_count = sum([has_cpu_85, has_mem_90, has_disk_95, has_14_day])

        if threshold_count >= 3:
            print(f"PASS: Component 3 - Thresholds found (CPU85={has_cpu_85}, Mem90={has_mem_90}, Disk95={has_disk_95}, 14day={has_14_day}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - Missing thresholds (CPU85={has_cpu_85}, Mem90={has_mem_90}, Disk95={has_disk_95}, 14day={has_14_day})")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: HTML report exists with required content (0.20 points)
    try:
        # Find any capacity report HTML file
        report_files = glob.glob(os.path.join(REPORTS_DIR, 'capacity_report_*.html'))
        if report_files:
            report_path = report_files[0]  # Take the most recent/any
            with open(report_path, 'r') as f:
                html_content = f.read()

            sub_score = 0.0
            checks = {
                'CPU content': 'CPU' in html_content,
                'Memory content': ('Memory' in html_content or 'Mem' in html_content),
                'Disk content': 'Disk' in html_content,
                'Trend/slope': ('trend' in html_content.lower() or 'slope' in html_content.lower()),
                'Confidence interval': ('confidence' in html_content.lower() or 'ci_' in html_content.lower()),
            }

            passed = sum(1 for v in checks.values() if v)
            for name, result in checks.items():
                print(f"  - {name}: {'FOUND' if result else 'MISSING'}")

            if passed >= 4:
                sub_score = 0.20
            elif passed >= 3:
                sub_score = 0.15
            elif passed >= 2:
                sub_score = 0.10

            if sub_score > 0:
                print(f"PASS: Component 4 - HTML report at {report_path} ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 4 - HTML report missing key content ({passed}/5 checks)")
        else:
            print(f"FAIL: Component 4 - No HTML report found in {REPORTS_DIR}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Jinja2 template and alert email (0.10 points)
    try:
        has_jinja2 = ('jinja2' in script_content.lower() or
                      'Template' in script_content or
                      'Jinja2' in script_content)
        has_email = 'ops@example.com' in script_content

        if has_jinja2 and has_email:
            print(f"PASS: Component 5 - Jinja2 template and ops@example.com alert email (0.10 pts)")
            total_score += 0.10
        elif has_jinja2:
            print(f"PARTIAL: Component 5 - Jinja2 found but alert email missing (0.05 pts)")
            total_score += 0.05
        elif has_email:
            print(f"PARTIAL: Component 5 - Alert email found but Jinja2 missing (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 - Neither Jinja2 template nor alert email found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Cron job for weekly Monday 8 AM (0.10 points)
    try:
        # Read crontab
        cron_content = ''
        try:
            import io
            cron_paths = ['/var/spool/cron/crontabs/root', '/var/spool/cron/crontabs/user']
            for cp in cron_paths:
                if os.path.isfile(cp):
                    with open(cp, 'r') as f:
                        cron_content += f.read()
        except PermissionError:
            pass

        if not cron_content:
            # Try reading via os.popen
            try:
                cron_content = os.popen('crontab -l 2>/dev/null').read()
            except Exception:
                pass

        if not cron_content:
            try:
                cron_content = os.popen('crontab -l -u root 2>/dev/null').read()
            except Exception:
                pass

        if not cron_content:
            try:
                cron_content = os.popen('crontab -l -u user 2>/dev/null').read()
            except Exception:
                pass

        cron_match_count = 0
        if cron_content:
            # Check for Monday (day 1) at 8 AM with capacity_planner
            # Expected: 0 8 * * 1 ...capacity_planner...
            for line in cron_content.strip().split('\n'):
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                if 'capacity_planner' in line:
                    # Parse cron fields
                    parts = line.split()
                    if len(parts) >= 5:
                        minute, hour, dom, month, dow = parts[0:5]
                        if minute == '0' and hour == '8' and dow == '1':
                            cron_match_count += 1
                            print(f"  - Cron schedule: {minute} {hour} {dom} {month} {dow} (Monday 8AM)")

        if cron_match_count > 0:
            print(f"PASS: Component 6 - Cron job configured for weekly Monday 8 AM (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 - Cron job not found or incorrect schedule (cron content: '{cron_content[:200]}')")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
