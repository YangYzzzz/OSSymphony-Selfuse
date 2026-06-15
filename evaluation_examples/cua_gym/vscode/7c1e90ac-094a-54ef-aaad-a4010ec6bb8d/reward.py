"""
Reward Script: Stash changes including untracked files, switch to main,
commit hotfix.txt, switch back to feature/dashboard and pop the stash.
Task ID: vscode_git_046
Domain: vs_code (git operations)

SCORING DESIGN:
The key distinguishing change between initial_env and golden_env is the
hotfix.txt commit on the main branch. All file-level changes (dashboard.py
modifications, chart_utils.py presence, current branch) exist in BOTH envs,
so only the hotfix commit provides genuine task-completion signal.

Progressive scoring uses the hotfix commit as the basis, with sub-checks
to award partial credit and ensure precise verification:

  Component 1: hotfix.txt exists on main branch (0.50 pts)
               [main has no extra commits on initial_env → FAILS on initial]
  Component 2: hotfix.txt content matches 'urgent fix' exactly (0.30 pts)
               [Content only present on golden_env → FAILS on initial]
  Component 3: Currently on feature/dashboard AND hotfix.txt absent from feature/dashboard (0.20 pts)
               [Confirms correct branch navigation (hotfix on main only, not feature/dashboard)]

  Total: 1.0

Note: dashboard.py and chart_utils.py restoration are preconditions
(true in both envs) — verified as precondition gates, not scoring components.
"""

import os
import subprocess

REPO_PATH = '/home/user/project'


def run_git(args, cwd=REPO_PATH):
    """Run a git command and return (stdout, returncode)."""
    result = subprocess.run(
        ['git'] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.stdout.strip(), result.returncode


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: repo must exist
    if not os.path.isdir(os.path.join(REPO_PATH, '.git')):
        print(f"CRITICAL: Git repo not found at {REPO_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: verify main branch exists
    main_exists, rc = run_git(['rev-parse', '--verify', 'main'])
    if rc != 0:
        print(f"CRITICAL: 'main' branch not found")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: confirm dashboard.py is modified (restored from stash or pre-existing)
    dashboard_path = os.path.join(REPO_PATH, 'dashboard.py')
    if not os.path.isfile(dashboard_path):
        print(f"WARN: dashboard.py not found at {dashboard_path}")
    else:
        diff_out, _ = run_git(['diff', 'dashboard.py'])
        if diff_out:
            print(f"INFO: dashboard.py has working-tree modifications (precondition met)")
        else:
            print(f"WARN: dashboard.py is not modified in working tree")

    # Precondition: confirm chart_utils.py is present
    chart_utils_path = os.path.join(REPO_PATH, 'chart_utils.py')
    if os.path.isfile(chart_utils_path):
        print(f"INFO: chart_utils.py is present (precondition met)")
    else:
        print(f"WARN: chart_utils.py not found")

    # Component 1: hotfix.txt exists on main branch (0.50 points)
    # On initial_env: main has only 'Initial commit' — no hotfix.txt → FAILS.
    # On golden_env: main has 'hotfix: urgent fix' commit with hotfix.txt → PASSES.
    try:
        hotfix_content, rc = run_git(['show', 'main:hotfix.txt'])
        if rc == 0 and hotfix_content != '':
            print(f"PASS: Component 1 — hotfix.txt exists on main branch (0.50 pts)")
            print(f"  Content: {repr(hotfix_content)}")
            total_score += 0.50
        else:
            print(f"FAIL: Component 1 — hotfix.txt does not exist on main branch (rc={rc})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: hotfix.txt content is 'urgent fix' (0.30 points)
    # On initial_env: hotfix.txt not on main at all → FAILS (hotfix_content is empty/error).
    # On golden_env: content is 'urgent fix' → PASSES.
    try:
        hotfix_content, rc = run_git(['show', 'main:hotfix.txt'])
        if rc == 0 and 'urgent fix' in hotfix_content:
            print(f"PASS: Component 2 — hotfix.txt content contains 'urgent fix' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — hotfix.txt content missing 'urgent fix'")
            print(f"  Actual content: {repr(hotfix_content)}, rc={rc}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Currently on feature/dashboard AND hotfix.txt on main (not on feature/dashboard) (0.20 points)
    # This is a compound check: the agent must be on feature/dashboard AND
    # the hotfix.txt commit must exist on main (differentiating condition).
    # On initial_env: main has no hotfix.txt → compound fails → FAILS on initial.
    # On golden_env: main has hotfix.txt AND we are on feature/dashboard → PASSES.
    try:
        current_branch, rc = run_git(['rev-parse', '--abbrev-ref', 'HEAD'])
        # Check main has hotfix.txt (already verified in C1, re-check for compound logic)
        main_hotfix, rc_main = run_git(['show', 'main:hotfix.txt'])
        main_has_hotfix = (rc_main == 0 and main_hotfix != '')

        if current_branch == 'feature/dashboard' and main_has_hotfix:
            # Verify hotfix.txt is not also committed on feature/dashboard (correct workflow)
            feat_hotfix, rc2 = run_git(['show', 'feature/dashboard:hotfix.txt'])
            hotfix_not_on_feature = (rc2 != 0)
            if hotfix_not_on_feature:
                print(f"PASS: Component 3 — On feature/dashboard, hotfix.txt on main only (correct workflow) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — hotfix.txt found on feature/dashboard too (incorrect — should be main only)")
                print(f"  feature/dashboard:hotfix.txt = {repr(feat_hotfix)}")
        elif current_branch != 'feature/dashboard':
            print(f"FAIL: Component 3 — Expected branch 'feature/dashboard', found '{current_branch}'")
        else:
            print(f"FAIL: Component 3 — main has no hotfix.txt (hotfix commit not found)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
