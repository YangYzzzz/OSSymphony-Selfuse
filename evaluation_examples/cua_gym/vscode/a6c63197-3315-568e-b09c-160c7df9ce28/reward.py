"""
Reward Script: Release preparation workflow in VSCode tasks.json
Task ID: vscode_wf_081
Domain: vscode
Scoring:
  C1 (0.20) - tasks.json exists with all 6 required task labels
  C2 (0.10) - version-bump task handles patch/minor/major via npm version
  C3 (0.10) - changelog task runs changelog script
  C4 (0.10) - build-release does clean build for production
  C5 (0.10) - tag-release creates git tag
  C6 (0.15) - release compound task runs all in sequence (dependsOrder: sequence)
  C7 (0.10) - pre-release-check verifies clean git status and passing tests
  C8 (0.05) - version-bump depends on pre-release-check
  C9 (0.10) - scripts/changelog.sh exists and generates CHANGELOG.md from git log
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
TASKS_PATH = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
CHANGELOG_SCRIPT = os.path.join(PROJECT_DIR, 'scripts', 'changelog.sh')
TASK_ID = 'vscode_wf_081'

REQUIRED_LABELS = {'version-bump', 'changelog', 'build-release', 'tag-release', 'pre-release-check', 'release'}


def load_tasks_json(path):
    """Load tasks.json, stripping JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def get_task_by_label(tasks_list, label):
    """Find a task object by its label."""
    for t in tasks_list:
        if t.get('label', '').lower() == label.lower():
            return t
    return None


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # ---------- Pre-check: tasks.json must exist ----------
    if not os.path.exists(TASKS_PATH):
        print(f"CRITICAL: tasks.json not found at {TASKS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        data = load_tasks_json(TASKS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks_list = data.get('tasks', [])
    labels = {t.get('label', '').lower() for t in tasks_list}

    # ---- Component 1: All 6 required task labels present (0.20) ----
    try:
        missing = {l for l in REQUIRED_LABELS if l.lower() not in labels}
        if not missing:
            print(f"PASS: Component 1 — All 6 required task labels found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Missing task labels: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---- Component 2: version-bump handles patch/minor/major (0.10) ----
    try:
        vb = get_task_by_label(tasks_list, 'version-bump')
        if vb:
            cmd = str(vb.get('command', ''))
            # Should reference npm version and patch/minor/major
            if 'npm version' in cmd.lower() and ('patch' in cmd.lower() or 'minor' in cmd.lower() or 'major' in cmd.lower() or 'versiontype' in cmd.lower() or 'input:' in cmd.lower()):
                print(f"PASS: Component 2 — version-bump uses npm version with patch/minor/major (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — version-bump command doesn't reference npm version patch/minor/major: {cmd}")
        else:
            print(f"FAIL: Component 2 — version-bump task not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: changelog task runs changelog script (0.10) ----
    try:
        cl = get_task_by_label(tasks_list, 'changelog')
        if cl:
            cmd = str(cl.get('command', ''))
            if 'changelog' in cmd.lower():
                print(f"PASS: Component 3 — changelog task runs changelog script (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — changelog command doesn't reference changelog script: {cmd}")
        else:
            print(f"FAIL: Component 3 — changelog task not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---- Component 4: build-release does clean build (0.10) ----
    try:
        br = get_task_by_label(tasks_list, 'build-release')
        if br:
            cmd = str(br.get('command', ''))
            has_clean = 'rm ' in cmd.lower() or 'clean' in cmd.lower() or 'rm -rf' in cmd.lower()
            has_build = 'build' in cmd.lower()
            if has_clean and has_build:
                print(f"PASS: Component 4 — build-release cleans and builds (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — build-release missing clean ({has_clean}) or build ({has_build}): {cmd}")
        else:
            print(f"FAIL: Component 4 — build-release task not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---- Component 5: tag-release creates git tag (0.10) ----
    try:
        tr = get_task_by_label(tasks_list, 'tag-release')
        if tr:
            cmd = str(tr.get('command', ''))
            if 'git tag' in cmd.lower() or 'git' in cmd.lower() and 'tag' in cmd.lower():
                print(f"PASS: Component 5 — tag-release creates git tag (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — tag-release command doesn't create git tag: {cmd}")
        else:
            print(f"FAIL: Component 5 — tag-release task not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ---- Component 6: release compound task with sequence (0.15) ----
    try:
        rel = get_task_by_label(tasks_list, 'release')
        if rel:
            depends_on = [d.lower() if isinstance(d, str) else str(d).lower() for d in rel.get('dependsOn', [])]
            depends_order = str(rel.get('dependsOrder', '')).lower()

            # Must have all sub-tasks and use sequence ordering
            required_deps = {'version-bump', 'changelog', 'build-release', 'tag-release'}
            has_all_deps = required_deps.issubset(set(depends_on))
            has_sequence = depends_order == 'sequence'

            if has_all_deps and has_sequence:
                print(f"PASS: Component 6 — release compound task has all deps in sequence (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — release task: has_all_deps={has_all_deps}, has_sequence={has_sequence}, dependsOn={depends_on}")
        else:
            print(f"FAIL: Component 6 — release task not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # ---- Component 7: pre-release-check verifies git status and tests (0.10) ----
    try:
        prc = get_task_by_label(tasks_list, 'pre-release-check')
        if prc:
            cmd = str(prc.get('command', ''))
            has_git_check = 'git diff' in cmd.lower() or 'git status' in cmd.lower()
            has_test_check = 'npm test' in cmd.lower() or 'jest' in cmd.lower() or 'test' in cmd.lower()

            if has_git_check and has_test_check:
                print(f"PASS: Component 7 — pre-release-check verifies git status and tests (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — pre-release-check missing git check ({has_git_check}) or test check ({has_test_check}): {cmd}")
        else:
            print(f"FAIL: Component 7 — pre-release-check task not found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # ---- Component 8: version-bump depends on pre-release-check (0.05) ----
    try:
        vb = get_task_by_label(tasks_list, 'version-bump')
        if vb:
            depends_on = [d.lower() if isinstance(d, str) else str(d).lower() for d in vb.get('dependsOn', [])]
            if 'pre-release-check' in depends_on:
                print(f"PASS: Component 8 — version-bump depends on pre-release-check (0.05 pts)")
                total_score += 0.05
            else:
                # Also check if release task has pre-release-check before version-bump in sequence
                rel = get_task_by_label(tasks_list, 'release')
                if rel:
                    rel_deps = [d.lower() if isinstance(d, str) else str(d).lower() for d in rel.get('dependsOn', [])]
                    if 'pre-release-check' in rel_deps and 'version-bump' in rel_deps:
                        prc_idx = rel_deps.index('pre-release-check')
                        vb_idx = rel_deps.index('version-bump')
                        if prc_idx < vb_idx:
                            print(f"PASS: Component 8 — pre-release-check runs before version-bump in release sequence (0.05 pts)")
                            total_score += 0.05
                        else:
                            print(f"FAIL: Component 8 — pre-release-check at index {prc_idx} is not before version-bump at index {vb_idx}")
                    else:
                        print(f"FAIL: Component 8 — version-bump doesn't depend on pre-release-check")
                else:
                    print(f"FAIL: Component 8 — version-bump doesn't depend on pre-release-check")
        else:
            print(f"FAIL: Component 8 — version-bump task not found")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    # ---- Component 9: scripts/changelog.sh exists and generates CHANGELOG from git log (0.10) ----
    try:
        if os.path.exists(CHANGELOG_SCRIPT):
            with open(CHANGELOG_SCRIPT, 'r') as f:
                content = f.read()
            has_git_log = 'git log' in content.lower()
            has_changelog = 'changelog' in content.lower()
            if has_git_log and has_changelog:
                print(f"PASS: Component 9 — changelog.sh exists and uses git log to generate CHANGELOG (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 9 — changelog.sh missing git log ({has_git_log}) or changelog ref ({has_changelog})")
        else:
            print(f"FAIL: Component 9 — scripts/changelog.sh not found")
    except Exception as e:
        print(f"ERROR: Component 9 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
