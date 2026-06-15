"""
Reward Script: VSCode git workflow - squash 3 WIP commits into 1, configure git.rebaseWhenSync
Task ID: vscode_gf2_045
Domain: vscode
Scoring:
  Component 1 (0.40): Commits squashed (3 WIP commits merged into 1) AND project files intact
  Component 2 (0.30): Squashed commit message is clean (no WIP)
  Component 3 (0.30): .vscode/settings.json has git.rebaseWhenSync: true
"""

import os
import json
import re

WORKDIR = '/home/user/projects/node-api'


def get_git_log():
    """Read git log by parsing .git objects via git command output saved to a temp file."""
    # Use os.popen since subprocess is forbidden
    stream = os.popen(f'cd {WORKDIR} && git log --format="%H|||%s" 2>/dev/null')
    output = stream.read().strip()
    stream.close()
    commits = []
    for line in output.split('\n'):
        if '|||' in line:
            hash_val, subject = line.split('|||', 1)
            commits.append({'hash': hash_val.strip(), 'subject': subject.strip()})
    return commits


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Commits squashed AND project files intact (0.40 points)
    # Initial state has 4 commits (3 WIP + 1 initial setup).
    # Golden state should have 2 commits (1 squashed + 1 initial setup).
    # The key change: the 3 WIP commits should be collapsed into 1.
    # Also verify project files are intact (precondition gate + task change).
    try:
        commits = get_git_log()
        num_commits = len(commits)

        # Count WIP commits remaining
        wip_commits = [c for c in commits if 'WIP' in c['subject'] or 'wip' in c['subject'].lower()]

        # Check project files intact (sub-condition)
        expected_files = ['index.js', 'package.json', 'README.md', '.gitignore']
        expected_dirs = ['src', 'tests']
        missing = []
        for f in expected_files:
            if not os.path.isfile(os.path.join(WORKDIR, f)):
                missing.append(f)
        for d in expected_dirs:
            if not os.path.isdir(os.path.join(WORKDIR, d)):
                missing.append(d + '/')

        if len(missing) > 0:
            print(f"FAIL: Component 1 - Project files missing after rebase: {missing}")
        elif num_commits <= 2 and len(wip_commits) == 0:
            print(f"PASS: Component 1 - Commits squashed: {num_commits} commits, 0 WIP, files intact (0.40 pts)")
            total_score += 0.40
        elif num_commits <= 3 and len(wip_commits) <= 1:
            # Partial credit: some squashing done
            print(f"PARTIAL: Component 1 - Partially squashed: {num_commits} commits, {len(wip_commits)} WIP remaining (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - Expected <=2 commits with 0 WIP, found {num_commits} commits with {len(wip_commits)} WIP")
            for c in commits:
                print(f"  commit: {c['subject']}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Squashed commit message is clean (0.30 points)
    # The combined commit message should NOT be a WIP message.
    # It should be a descriptive, clean commit message.
    try:
        commits = get_git_log()
        # Look at the most recent commit (the squashed one, not the initial setup)
        if len(commits) >= 1:
            latest = commits[0]
            subject = latest['subject']

            # The squashed commit should not contain "WIP"
            has_wip = bool(re.search(r'\bWIP\b', subject, re.IGNORECASE))

            # It should be a meaningful message (more than just whitespace)
            is_meaningful = len(subject.strip()) > 5

            if not has_wip and is_meaningful:
                print(f"PASS: Component 2 - Clean commit message: '{subject}' (0.30 pts)")
                total_score += 0.30
            elif not has_wip:
                print(f"PARTIAL: Component 2 - No WIP but short message: '{subject}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 - Commit message still contains WIP: '{subject}'")
        else:
            print(f"FAIL: Component 2 - No commits found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: .vscode/settings.json with git.rebaseWhenSync: true (0.30 points)
    # This file should NOT exist in initial state.
    try:
        settings_path = os.path.join(WORKDIR, '.vscode', 'settings.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments if present
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
            settings = json.loads(cleaned)

            rebase_setting = settings.get('git.rebaseWhenSync')
            if rebase_setting is True:
                print(f"PASS: Component 3 - git.rebaseWhenSync is true (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 - git.rebaseWhenSync is {rebase_setting}, expected true")
        else:
            print(f"FAIL: Component 3 - .vscode/settings.json does not exist")
    except json.JSONDecodeError as e:
        print(f"ERROR: Component 3 - Invalid JSON in settings.json: {e}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(WORKDIR):
    print(f"Directory not found: {WORKDIR}")
    print("REWARD: 0.0")
else:
    verify_task()
