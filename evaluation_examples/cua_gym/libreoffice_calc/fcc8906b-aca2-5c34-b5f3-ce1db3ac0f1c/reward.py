"""
Reward Script: Configure logrotate for /var/log/myapp/app.log
Task ID: os_gff_021
Domain: os
Scoring:
  - Component 1: 'daily' directive present (0.2)
  - Component 2: 'rotate 14' directive present (0.2)
  - Component 3: 'compress' directive present (0.2)
  - Component 4: postrotate script sends SIGHUP to myapp (0.25)
  - Component 5: config targets correct log path /var/log/myapp/app.log (0.15)
"""

import os
import re

CONFIG_PATH = '/etc/logrotate.d/myapp'


def strip_comments(line):
    """Remove inline comments from a logrotate config line."""
    return line.split('#')[0].strip()


def find_directive(lines, directive_regex):
    """Check if any non-comment line matches the given regex."""
    return any(re.match(directive_regex, strip_comments(line)) for line in lines)


def extract_postrotate(lines):
    """Extract content between postrotate and endscript directives."""
    content = []
    inside = 0  # 0 = outside, 1 = inside
    for line in lines:
        stripped = strip_comments(line)
        if stripped == 'postrotate':
            inside = 1
            continue
        if stripped == 'endscript':
            inside = 0
            continue
        if inside == 1:
            content.append(line)
    return content


def verify_task():
    """
    Verify logrotate configuration for /var/log/myapp/app.log.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: config file must exist
    if not os.path.isfile(CONFIG_PATH):
        print(f"CRITICAL: Config file not found: {CONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(CONFIG_PATH, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read config file: {e}")
        print("REWARD: 0.0")
        return 0.0

    lines = [line.strip() for line in content.split('\n')]

    # Component 1: 'daily' directive present (0.2 points)
    try:
        if find_directive(lines, r'^daily$'):
            print(f"PASS: Component 1 — 'daily' directive found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — 'daily' directive not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'rotate 14' directive present (0.2 points)
    try:
        if find_directive(lines, r'^rotate\s+14$'):
            print(f"PASS: Component 2 — 'rotate 14' directive found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — 'rotate 14' directive not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'compress' directive present (0.2 points)
    try:
        if find_directive(lines, r'^compress$'):
            print(f"PASS: Component 3 — 'compress' directive found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — 'compress' directive not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: postrotate script sends SIGHUP to myapp (0.25 points)
    try:
        postrotate_lines = extract_postrotate(lines)
        postrotate_text = ' '.join(postrotate_lines)

        # Check for SIGHUP signal to myapp process
        # Acceptable: kill -HUP $(pidof myapp), kill -1 $(pidof myapp),
        # killall -HUP myapp, pkill -HUP myapp, etc.
        sighup_patterns = [
            r'kill\s+(-HUP|-1|-s\s+HUP|-s\s+SIGHUP)\s+.*pidof\s+myapp',
            r'kill\s+(-HUP|-1|-s\s+HUP|-s\s+SIGHUP)\s+.*pgrep\s+myapp',
            r'killall\s+(-HUP|-1|-s\s+HUP)\s+myapp',
            r'pkill\s+(-HUP|-1)\s+myapp',
        ]
        sighup_found = any(re.search(p, postrotate_text) for p in sighup_patterns)

        if len(postrotate_lines) > 0 and sighup_found:
            print(f"PASS: Component 4 — postrotate with SIGHUP to myapp found (0.25 pts)")
            total_score += 0.25
        elif len(postrotate_lines) > 0:
            print(f"FAIL: Component 4 — postrotate block exists but no SIGHUP to myapp. Content: {postrotate_lines}")
        else:
            print(f"FAIL: Component 4 — no postrotate block found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: config targets correct log path /var/log/myapp/app.log (0.15 points)
    try:
        if '/var/log/myapp/app.log' in content:
            print(f"PASS: Component 5 — config targets /var/log/myapp/app.log (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — config does not reference /var/log/myapp/app.log")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
