"""
Reward Script: Markdown linting configuration and fix in VSCode
Task ID: vscode_gf5_043
Domain: vscode
Scoring:
  Component 1 (0.30): markdownlint extension is installed
  Component 2 (0.30): .markdownlint.json exists with MD013: false and MD041: false
  Component 3 (0.20): MD022 fix — blank line before headings in README.md
  Component 4 (0.20): MD032 fix — blank line before lists in README.md
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_043'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'documentation')


def check_extension_installed():
    """Check if markdownlint extension is installed by scanning extension directories."""
    ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
    try:
        if not os.path.isdir(ext_dir):
            return False
        for entry in os.listdir(ext_dir):
            if 'markdownlint' in entry.lower():
                return os.path.isdir(os.path.join(ext_dir, entry))
        return False
    except Exception:
        return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: markdownlint extension is installed (0.30 points)
    try:
        ext_installed = check_extension_installed()
        if ext_installed:
            print(f"PASS: Component 1 — markdownlint extension is installed (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — markdownlint extension is NOT installed")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: .markdownlint.json exists with correct config (0.30 points)
    lint_config_path = os.path.join(PROJECT_DIR, '.markdownlint.json')
    try:
        if not os.path.exists(lint_config_path):
            print(f"FAIL: Component 2 — .markdownlint.json does not exist at {lint_config_path}")
        else:
            with open(lint_config_path, 'r') as f:
                config = json.load(f)

            md013_disabled = config.get('MD013') is False
            md041_disabled = config.get('MD041') is False

            if md013_disabled and md041_disabled:
                print(f"PASS: Component 2 — .markdownlint.json has MD013: false and MD041: false (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — MD013={config.get('MD013')}, MD041={config.get('MD041')}; expected both false")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 2 — .markdownlint.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: MD022 fix — blank line before headings (0.20 points)
    # In the initial README.md, the first line of text is immediately followed
    # by "## Architecture Overview" with no blank line. The fix adds a blank line.
    readme_path = os.path.join(PROJECT_DIR, 'README.md')
    try:
        if not os.path.exists(readme_path):
            print(f"FAIL: Component 3 — README.md not found")
        else:
            with open(readme_path, 'r') as f:
                content = f.read()
            lines = content.split('\n')

            # Check MD022: every heading (##) must be preceded by a blank line
            # (except if it's the first line of the file)
            # Find all headings that violate MD022
            md022_violations = [
                i for i, line in enumerate(lines)
                if i > 0
                and re.match(r'^#{1,6}\s', line)
                and lines[i - 1].strip() != ''
            ]

            if len(md022_violations) == 0:
                print(f"PASS: Component 3 — MD022 fixed: blank lines before all headings (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — MD022 not fixed: {len(md022_violations)} heading(s) missing preceding blank line")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: MD032 fix — blank line before lists (0.20 points)
    # In the initial README.md, "The required dependencies are:" is immediately
    # followed by "- Docker Desktop..." with no blank line. The fix adds a blank line.
    try:
        if not os.path.exists(readme_path):
            print(f"FAIL: Component 4 — README.md not found")
        else:
            with open(readme_path, 'r') as f:
                content = f.read()
            lines = content.split('\n')

            # Check MD032: lists must be surrounded by blank lines
            # Specifically check that any line starting with "- " that is preceded
            # by a non-blank, non-list line has a blank line before it.
            md032_violations = [
                i for i, line in enumerate(lines)
                if i > 0
                and re.match(r'^[-*+]\s', line.strip())
                and lines[i - 1].strip() != ''
                and not re.match(r'^[-*+]\s', lines[i - 1].strip())
            ]

            if len(md032_violations) == 0:
                print(f"PASS: Component 4 — MD032 fixed: blank lines before lists (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — MD032 not fixed: {len(md032_violations)} list(s) missing preceding blank line")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
