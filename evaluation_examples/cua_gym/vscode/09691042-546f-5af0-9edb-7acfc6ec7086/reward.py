"""
Reward Script: Git rebase --onto verification
Task ID: vscode_gf6_063
Domain: vscode (git operations)
Scoring:
  Component 1: feature/dependent has exactly 4 commits above main (0.35)
  Component 2: feature/dependent is rebased onto main's tip (0.2)
  Component 3: No merge conflict markers in tracked files (0.1)
  Component 4: pytest passes all tests (0.15)
  Component 5: rebase_notes.txt exists with meaningful content (0.2)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_063'
REPO_DIR = os.path.join(WORKDIR, 'projects', 'git-rebase-onto')


def run_git(args):
    """Run a git command in the repo directory and return stdout."""
    import os as _os
    original_dir = _os.getcwd()
    try:
        _os.chdir(REPO_DIR)
        # Use os.popen since subprocess is forbidden
        cmd = 'git ' + args
        result = _os.popen(cmd).read()
        return result.strip()
    finally:
        _os.chdir(original_dir)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repo directory exists
    if not os.path.isdir(REPO_DIR):
        print(f"CRITICAL: Repository directory not found: {REPO_DIR}")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.isdir(os.path.join(REPO_DIR, '.git')):
        print(f"CRITICAL: Not a git repository: {REPO_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: feature/dependent branch must exist
    branches = run_git('branch')
    if 'feature/dependent' not in branches or 'main' not in branches:
        print("CRITICAL: Required branches (main, feature/dependent) missing")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: feature/dependent has exactly 4 commits above main (0.35 points)
    # In initial state, this shows 7 commits (includes feature/base's 3).
    # After rebase --onto, only 4 (feature/dependent's own) should remain.
    try:
        dep_only_commits = run_git('log --oneline feature/dependent ^main')
        lines = [l for l in dep_only_commits.split('\n') if l.strip()] if dep_only_commits else []
        commit_count = len(lines)
        if commit_count == 4:
            print(f"PASS: Component 1 — feature/dependent has exactly 4 commits above main (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — expected 4 commits above main, found {commit_count}")
            for line in lines:
                print(f"  commit: {line}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: feature/dependent is rebased onto main's tip (0.2 points)
    # The merge-base of main and feature/dependent should be main's tip commit.
    # In initial state, merge-base is commit 5 (not main tip).
    try:
        merge_base = run_git('merge-base main feature/dependent')
        main_tip = run_git('rev-parse main')
        if merge_base == main_tip:
            print(f"PASS: Component 2 — merge-base is main's tip ({main_tip[:8]}), rebase onto main confirmed (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — merge-base is {merge_base[:8]}, expected main tip {main_tip[:8]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No merge conflict markers in tracked files (0.1 points)
    # Gated on Components 1+2 (rebase must have happened first)
    try:
        if total_score >= 0.5:  # Components 1+2 passed, rebase happened
            tracked_files = run_git('ls-files')
            conflict_files = []
            for f in tracked_files.split('\n'):
                f = f.strip()
                if not f:
                    continue
                fpath = os.path.join(REPO_DIR, f)
                if os.path.isfile(fpath):
                    try:
                        with open(fpath, 'r', errors='ignore') as fh:
                            content = fh.read()
                        if '<<<<<<<' in content or '>>>>>>>' in content:
                            conflict_files.append(f)
                    except Exception:
                        pass
            if len(conflict_files) == 0:
                print(f"PASS: Component 3 — No merge conflict markers in tracked files (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3 — Merge conflict markers found in: {', '.join(conflict_files)}")
        else:
            print(f"SKIP: Component 3 — Gated on Components 1+2 (rebase not confirmed)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: pytest passes all tests (0.15 points)
    # Gated on rebase having happened (Components 1+2)
    try:
        if total_score >= 0.5:  # Rebase confirmed
            pytest_output = os.popen('cd /home/user/projects/git-rebase-onto && python3 -m pytest --tb=short 2>&1').read()
            if 'passed' in pytest_output and 'failed' not in pytest_output and 'error' not in pytest_output.lower().split('passed')[0]:
                print(f"PASS: Component 4 — All tests pass after rebase (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Tests did not all pass after rebase")
                for line in pytest_output.strip().split('\n')[-5:]:
                    print(f"  {line}")
        else:
            print(f"SKIP: Component 4 — Gated on Components 1+2 (rebase not confirmed)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: rebase_notes.txt exists with meaningful documentation (0.2 points)
    # This file should NOT exist in the initial state. Only created after the task.
    try:
        notes_path = os.path.join(REPO_DIR, 'rebase_notes.txt')
        if os.path.isfile(notes_path):
            with open(notes_path, 'r') as f:
                content = f.read()
            content_lower = content.lower()
            has_before = 'before' in content_lower
            has_after = 'after' in content_lower
            has_rebase = 'rebase' in content_lower
            has_onto = 'onto' in content_lower or '--onto' in content_lower
            matching_terms = sum([has_before, has_after, has_rebase, has_onto])
            if matching_terms >= 3 and len(content) > 100:
                print(f"PASS: Component 5 — rebase_notes.txt exists with meaningful content ({len(content)} chars, {matching_terms}/4 key terms) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 5 — rebase_notes.txt exists but content insufficient (len={len(content)}, terms={matching_terms}/4)")
        else:
            print(f"FAIL: Component 5 — rebase_notes.txt not found at {notes_path}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
