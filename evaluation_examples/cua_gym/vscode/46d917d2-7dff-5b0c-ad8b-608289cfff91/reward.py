"""
Reward Script: Git hooks workflow with Husky for pre-commit (ESLint) and commit-msg (Conventional Commits)
Task ID: vscode_gf5_032
Domain: vscode
Scoring:
  Component 1: husky in devDependencies (0.15)
  Component 2: .husky/ directory exists with husky.sh (0.15)
  Component 3: pre-commit hook runs eslint (0.25)
  Component 4: commit-msg hook validates Conventional Commits (0.25)
  Component 5: git hooksPath configured to .husky (0.20)
"""

import os
import json
import re
import configparser
import io

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'team-project')
TASK_ID = 'vscode_gf5_032'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: husky is in devDependencies (0.15 points)
    try:
        pkg_path = os.path.join(PROJECT_DIR, 'package.json')
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)
        dev_deps = pkg.get('devDependencies', {})
        if 'husky' in dev_deps:
            print(f"PASS: Component 1 — husky found in devDependencies: {dev_deps['husky']} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — husky not found in devDependencies. Keys: {list(dev_deps.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: .husky/ directory exists with husky.sh bootstrap (0.15 points)
    try:
        husky_dir = os.path.join(PROJECT_DIR, '.husky')
        husky_sh = os.path.join(husky_dir, '_', 'husky.sh')
        if os.path.isdir(husky_dir) and os.path.isfile(husky_sh):
            with open(husky_sh, 'r') as f:
                content = f.read()
            if 'husky' in content.lower():
                print(f"PASS: Component 2 — .husky/ dir and _/husky.sh exist with husky content (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — .husky/_/husky.sh exists but doesn't contain husky references")
        else:
            missing = []
            if not os.path.isdir(husky_dir):
                missing.append('.husky/ directory')
            if not os.path.isfile(husky_sh):
                missing.append('.husky/_/husky.sh')
            print(f"FAIL: Component 2 — missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: pre-commit hook runs eslint on src/ (0.25 points)
    try:
        pre_commit_path = os.path.join(PROJECT_DIR, '.husky', 'pre-commit')
        if os.path.isfile(pre_commit_path):
            with open(pre_commit_path, 'r') as f:
                content = f.read()
            # Check that the hook invokes eslint on src/
            has_eslint = bool(re.search(r'eslint\s+src', content, re.IGNORECASE))
            if has_eslint:
                print(f"PASS: Component 3 — pre-commit hook runs eslint on src/ (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — pre-commit hook exists but does not run eslint on src/. Content: {content[:200]}")
        else:
            print(f"FAIL: Component 3 — .husky/pre-commit file does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: commit-msg hook validates Conventional Commits format (0.25 points)
    try:
        commit_msg_path = os.path.join(PROJECT_DIR, '.husky', 'commit-msg')
        if os.path.isfile(commit_msg_path):
            with open(commit_msg_path, 'r') as f:
                content = f.read()
            # The hook should validate conventional commits - check for key type keywords
            # and either commitlint usage or a regex pattern
            has_type_check = bool(re.search(r'(feat|fix|docs|refactor|chore)', content))
            has_validation = bool(
                re.search(r'commitlint', content, re.IGNORECASE)
                or re.search(r'grep.*-[qeE]', content)
                or re.search(r'pattern\s*=', content)
                or re.search(r're\.match|re\.search|regex', content, re.IGNORECASE)
            )
            has_reject = bool(re.search(r'exit\s+1', content))

            if has_type_check and has_validation and has_reject:
                print(f"PASS: Component 4 — commit-msg hook validates Conventional Commits with rejection (0.25 pts)")
                total_score += 0.25
            elif has_type_check and (has_validation or has_reject):
                print(f"PARTIAL: Component 4 — commit-msg hook has type check but incomplete validation (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — commit-msg hook does not validate Conventional Commits. "
                      f"type_check={has_type_check}, validation={has_validation}, reject={has_reject}. "
                      f"Content preview: {content[:300]}")
        else:
            print(f"FAIL: Component 4 — .husky/commit-msg file does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: git hooksPath configured to .husky (0.20 points)
    try:
        git_config_path = os.path.join(PROJECT_DIR, '.git', 'config')
        with open(git_config_path, 'r') as f:
            git_config_content = f.read()
        # Check for hooksPath pointing to .husky
        if re.search(r'hooksPath\s*=\s*\.husky', git_config_content):
            print(f"PASS: Component 5 — git core.hooksPath set to .husky (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — git core.hooksPath not set to .husky. Config content: {git_config_content[:300]}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
