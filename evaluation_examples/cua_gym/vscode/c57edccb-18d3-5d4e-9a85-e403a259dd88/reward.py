"""
Reward Script: Initialize git repo with branching model (main, develop, feature branches),
               commits on each branch, merge feature/auth into develop, visualize topology.
Task ID: vscode_git_076
Domain: vs_code (git)

Scoring Rubric:
  Component 1: Git repo initialized in /home/user/new-project                      (0.20)
  Component 2: All 4 required branches exist (main, develop, feature/auth, feature/api) (0.25)
  Component 3: Each branch has the expected number of commits                      (0.20)
  Component 4: feature/auth merged into develop (merge commit present)             (0.20)
  Component 5: feature/api has at least 1 unique commit branched from develop      (0.15)
  Total: 1.00

Note: Git repository inspection has no viable pure-Python library on this VM
(gitpython/pygit2/dulwich not available). We use the git CLI via subprocess
ONLY for read-only git inspection commands — no write operations, no shell
expansion. All git commands are passed as lists to avoid shell injection.
"""

import os
import subprocess

WORKDIR = '/home/user/new-project'
TASK_ID = 'vscode_git_076'


def git(args, cwd=WORKDIR):
    """
    Run a read-only git command and return (returncode, stdout, stderr).
    Args must be a list of strings (no shell=True to avoid injection).
    """
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True, text=True, cwd=cwd
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except FileNotFoundError:
        return 1, '', 'git not found'
    except Exception as e:
        return 1, '', str(e)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Precondition gate: project directory must exist
    if not os.path.isdir(WORKDIR):
        print(f"CRITICAL: Project directory not found: {WORKDIR}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: Git repository initialized (0.20 points)
    # The .git directory must exist and git must recognize it as a valid repo.
    # This FAILS on initial_env (no .git dir), PASSES on golden_env.
    # -----------------------------------------------------------------------
    try:
        git_dir = os.path.join(WORKDIR, '.git')
        if os.path.isdir(git_dir):
            rc, out, err = git(['rev-parse', '--is-inside-work-tree'])
            if rc == 0 and out == 'true':
                print("PASS: Component 1 — Git repo initialized at /home/user/new-project (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — .git dir exists but repo is invalid: {err}")
        else:
            print(f"FAIL: Component 1 — No .git directory at {WORKDIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: All 4 required branches exist (0.25 points)
    # Branches: main, develop, feature/auth, feature/api
    # This FAILS on initial_env (no repo), PASSES on golden_env (all 4 present).
    # Each branch contributes 0.0625 pts; full credit only if all 4 present.
    # -----------------------------------------------------------------------
    try:
        rc, out, err = git(['branch', '--list'])
        if rc != 0:
            print(f"FAIL: Component 2 — Cannot list branches: {err}")
        else:
            branches = set(b.strip().lstrip('* ').strip() for b in out.splitlines() if b.strip())
            required = ['main', 'develop', 'feature/auth', 'feature/api']
            present = [b for b in required if b in branches]
            missing = [b for b in required if b not in branches]

            if len(present) == 4:
                print(f"PASS: Component 2 — All 4 required branches exist: {present} (0.25 pts)")
                total_score += 0.25
            elif len(present) > 0:
                partial = round(0.0625 * len(present), 4)
                print(f"PARTIAL: Component 2 — {len(present)}/4 branches present: {present}, "
                      f"missing: {missing} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — No required branches found (branches: {branches})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Each branch has expected number of commits (0.20 points)
    # - main: >= 1 commit (initial commit)
    # - develop: >= 3 commits (initial + 2 develop commits, merges count too)
    # - feature/auth: >= 2 commits beyond main (2 develop + 2 feature/auth = 4 total beyond main)
    #   NOTE: We use ^main (not ^develop) because after merging feature/auth into develop,
    #   `feature/auth ^develop` = 0. Using ^main correctly shows 4 non-initial commits.
    # - feature/api: >= 1 unique commit beyond develop (branched from develop, 1 feature commit)
    # This FAILS on initial_env (no repo), PASSES on golden_env.
    # -----------------------------------------------------------------------
    try:
        # Count commits on each branch using rev-list
        rc_main, main_count, _ = git(['rev-list', '--count', 'main'])
        rc_dev, dev_count, _ = git(['rev-list', '--count', 'develop'])
        # For feature/auth: count commits beyond main (since it was merged into develop,
        # comparing against develop gives 0; comparing against main gives 4)
        rc_fauth, fauth_beyond_main, _ = git(['rev-list', '--count', 'feature/auth', '^main'])
        # For feature/api: count commits beyond develop (1 unique feature commit)
        rc_fapi, fapi_unique, _ = git(['rev-list', '--count', 'feature/api', '^develop'])

        branch_checks = {}
        # main: at least 1 commit (initial commit)
        branch_checks['main'] = (rc_main == 0 and int(main_count or 0) >= 1)
        # develop: at least 3 commits (1 initial + 2 develop commits + possible merge)
        branch_checks['develop'] = (rc_dev == 0 and int(dev_count or 0) >= 3)
        # feature/auth: at least 2 commits beyond main (develop work + feature work)
        branch_checks['feature/auth'] = (rc_fauth == 0 and int(fauth_beyond_main or 0) >= 2)
        # feature/api: at least 1 unique commit beyond develop
        branch_checks['feature/api'] = (rc_fapi == 0 and int(fapi_unique or 0) >= 1)

        passing = [k for k, v in branch_checks.items() if v]
        failing = [k for k, v in branch_checks.items() if not v]

        if len(passing) == 4:
            print(f"PASS: Component 3 — All 4 branches have expected commits "
                  f"(main:{main_count}, develop:{dev_count}, "
                  f"feature/auth beyond main:{fauth_beyond_main}, "
                  f"feature/api unique:{fapi_unique}) (0.20 pts)")
            total_score += 0.20
        elif len(passing) >= 2:
            partial = round(0.05 * len(passing), 4)
            print(f"PARTIAL: Component 3 — {len(passing)}/4 branches have expected commits: "
                  f"passing={passing}, failing={failing} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Insufficient commits on branches: "
                  f"main:{main_count}, develop:{dev_count}, "
                  f"feature/auth beyond main:{fauth_beyond_main}, feature/api unique:{fapi_unique}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: feature/auth merged into develop (0.20 points)
    # A merge commit must exist on develop's history where feature/auth was merged.
    # This FAILS on initial_env (no repo), PASSES on golden_env.
    # -----------------------------------------------------------------------
    try:
        # Check for merge commits on develop
        rc_merge, merge_out, _ = git(['log', '--merges', '--oneline', 'develop'])
        if rc_merge != 0:
            print(f"FAIL: Component 4 — Cannot check merge history: {merge_out}")
        else:
            merge_commits = [l for l in merge_out.splitlines() if l.strip()]
            if merge_commits:
                # Verify feature/auth is an ancestor of develop (was merged)
                rc_anc, anc_out, anc_err = git(
                    ['merge-base', '--is-ancestor', 'feature/auth', 'develop']
                )
                if rc_anc == 0:
                    print(f"PASS: Component 4 — feature/auth merged into develop "
                          f"(merge commit: '{merge_commits[0]}') (0.20 pts)")
                    total_score += 0.20
                else:
                    # Merge commits exist but feature/auth is not confirmed as merged
                    auth_in_merge = any('auth' in m.lower() for m in merge_commits)
                    if auth_in_merge:
                        print(f"PASS: Component 4 — Merge commit referencing auth found: "
                              f"{merge_commits} (0.20 pts)")
                        total_score += 0.20
                    else:
                        print(f"PARTIAL: Component 4 — Merge commits exist but feature/auth "
                              f"not confirmed merged: {merge_commits} (0.10 pts)")
                        total_score += 0.10
            else:
                # No explicit merge — check if feature/auth tip is ancestor of develop
                rc_anc, _, _ = git(
                    ['merge-base', '--is-ancestor', 'feature/auth', 'develop']
                )
                if rc_anc == 0:
                    print(f"PASS: Component 4 — feature/auth is ancestor of develop "
                          f"(fast-forward or squash merge) (0.15 pts)")
                    total_score += 0.15
                else:
                    print("FAIL: Component 4 — feature/auth was NOT merged into develop")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: feature/api has at least 1 unique commit branched from develop (0.15 points)
    # feature/api must have commits that are NOT on develop (unique feature work).
    # This FAILS on initial_env (no repo), PASSES on golden_env.
    # -----------------------------------------------------------------------
    try:
        # Count commits on feature/api that are NOT on develop
        rc, unique_count, err = git(['rev-list', '--count', 'feature/api', '^develop'])
        if rc == 0:
            n = int(unique_count or 0)
            if n >= 1:
                print(f"PASS: Component 5 — feature/api has {n} unique commit(s) "
                      f"not on develop (0.15 pts)")
                total_score += 0.15
            else:
                # feature/api might have been merged into develop or has no unique commits
                # Check if feature/api was branched from develop at least
                rc2, base_out, _ = git(['merge-base', 'feature/api', 'develop'])
                rc3, dev_tip, _ = git(['rev-parse', 'develop'])
                if rc2 == 0 and rc3 == 0:
                    print(f"PARTIAL: Component 5 — feature/api exists and shares base with develop "
                          f"but has no unique commits (0.05 pts)")
                    total_score += 0.05
                else:
                    print(f"FAIL: Component 5 — feature/api has no unique commits beyond develop")
        else:
            # Branch may not exist
            rc2, _, _ = git(['rev-parse', 'feature/api'])
            if rc2 == 0:
                print(f"PARTIAL: Component 5 — feature/api exists but comparison failed: {err} (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 5 — feature/api branch does not exist or has no commits")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
