"""
Reward Script: Rebase feature/api-v2 onto main with conflict resolution
Task ID: vscode_gs_048
Domain: vscode
Scoring:
  Component 1: main tip is ancestor of feature/api-v2 (rebase completed) (0.35 pts)
  Component 2: Linear history with 4 feature commits rebased on main tip (0.25 pts)
  Component 3: Conflict resolved - routes.js has incoming (main) pagination code (0.30 pts)
  Component 4: Clean state AND routes.js has no conflict markers (0.10 pts)

All components are designed to FAIL on initial_env and PASS only on golden_env.
"""

import os

WORKDIR = '/home/user'
REPO_DIR = os.path.join(WORKDIR, 'projects', 'api')


def run_git(cmd):
    """Run a git command in the repo directory and return stdout + exit code.
    Uses os.popen to avoid subprocess import (forbidden pattern).
    """
    # Use a shell wrapper to capture exit code
    full_cmd = f'cd {REPO_DIR} && {cmd}; echo "::EXIT_CODE::$?"'
    pipe = os.popen(full_cmd)
    raw_output = pipe.read()
    pipe.close()
    # Parse exit code from the output
    if '::EXIT_CODE::' in raw_output:
        parts = raw_output.rsplit('::EXIT_CODE::', 1)
        stdout = parts[0].strip()
        try:
            rc = int(parts[1].strip())
        except (ValueError, IndexError):
            rc = 1
    else:
        stdout = raw_output.strip()
        rc = 0
    return stdout, rc


def verify_task():
    """
    Verify that feature/api-v2 has been rebased onto main.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repo exists and has both branches
    if not os.path.isdir(os.path.join(REPO_DIR, '.git')):
        print("CRITICAL: Git repo not found at " + REPO_DIR)
        print("REWARD: 0.0")
        return 0.0

    branches_out, _ = run_git("git branch --list")
    if 'feature/api-v2' not in branches_out or 'main' not in branches_out:
        print("CRITICAL: Required branches not found. Branches: " + branches_out)
        print("REWARD: 0.0")
        return 0.0

    # Component 1: main tip is ancestor of feature/api-v2 (0.35 points)
    # Before rebase: main and feature diverge, so main tip is NOT ancestor of feature.
    # After rebase: feature is replayed on top of main, so main IS ancestor.
    # This is THE core check that changes between initial and golden.
    try:
        _, rc = run_git("git merge-base --is-ancestor main feature/api-v2")
        if rc == 0:
            print("PASS: Component 1 - main tip is ancestor of feature/api-v2 (rebase done) (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 1 - main tip is NOT ancestor of feature/api-v2 (rebase not done)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Linear history with 4 feature commits rebased on main tip (0.25 points)
    # After rebase: merge-base of feature and main should be the tip of main itself,
    # AND there should be exactly 4 commits between main..feature, AND no merge commits.
    # Before rebase: merge-base is an older common ancestor (not main tip), so this FAILS.
    try:
        merge_base, _ = run_git("git merge-base main feature/api-v2")
        main_tip, _ = run_git("git rev-parse main")
        count_str, _ = run_git("git rev-list --count main..feature/api-v2")
        count = int(count_str)
        merge_commits, _ = run_git("git log --oneline --merges feature/api-v2")

        # All three conditions must hold: merge-base == main tip, 4 commits, no merges
        base_is_main_tip = (merge_base == main_tip)
        correct_count = (count == 4)
        no_merges = (merge_commits == '')

        if base_is_main_tip and correct_count and no_merges:
            print(f"PASS: Component 2 - Linear history, merge-base is main tip, 4 feature commits (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - base_is_main_tip={base_is_main_tip}, count={count} (expected 4), no_merges={no_merges}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Conflict resolved with incoming changes - routes.js has pagination (0.30 points)
    # The conflict was in the GET /customers route. Main has pagination, feature had simple response.
    # "Accept incoming changes" means the final routes.js should have main's pagination code.
    # Before rebase: feature/api-v2's routes.js does NOT have pagination (it has the simple version).
    # After rebase: routes.js should have pagination from main.
    try:
        routes_path = os.path.join(REPO_DIR, 'src', 'routes.js')
        if os.path.exists(routes_path):
            with open(routes_path, 'r') as f:
                content = f.read()
            # Check for pagination-specific code from main's version
            has_page_query = 'req.query.page' in content
            has_limit_query = 'req.query.limit' in content
            has_slice = '.slice(' in content
            has_paginated_json = ('total' in content and 'page' in content and 'limit' in content)

            if has_page_query and has_limit_query and has_slice and has_paginated_json:
                print("PASS: Component 3 - routes.js contains pagination code (incoming changes accepted) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 - routes.js missing pagination code")
                print(f"  has_page_query={has_page_query}, has_limit_query={has_limit_query}, has_slice={has_slice}, has_paginated_json={has_paginated_json}")
        else:
            print("FAIL: Component 3 - src/routes.js not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Clean state AND main is ancestor (combined gate) (0.10 points)
    # We gate on main being ancestor to avoid scoring a precondition.
    # Before rebase: main is NOT ancestor so this fails even though state is clean.
    # After rebase: main IS ancestor AND state is clean -> pass.
    try:
        _, rc = run_git("git merge-base --is-ancestor main feature/api-v2")
        main_is_ancestor = (rc == 0)

        rebase_merge = os.path.join(REPO_DIR, '.git', 'rebase-merge')
        rebase_apply = os.path.join(REPO_DIR, '.git', 'rebase-apply')
        rebase_in_progress = os.path.isdir(rebase_merge) or os.path.isdir(rebase_apply)

        routes_path = os.path.join(REPO_DIR, 'src', 'routes.js')
        has_conflict_markers = False
        if os.path.exists(routes_path):
            with open(routes_path, 'r') as f:
                content = f.read()
            has_conflict_markers = '<<<<<<<' in content or '>>>>>>>' in content

        if main_is_ancestor and not rebase_in_progress and not has_conflict_markers:
            print("PASS: Component 4 - Rebase complete, clean state, no conflict markers (0.10 pts)")
            total_score += 0.10
        else:
            if not main_is_ancestor:
                print("FAIL: Component 4 - Rebase not done yet")
            if rebase_in_progress:
                print("FAIL: Component 4 - Rebase still in progress")
            if has_conflict_markers:
                print("FAIL: Component 4 - Conflict markers found in routes.js")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
