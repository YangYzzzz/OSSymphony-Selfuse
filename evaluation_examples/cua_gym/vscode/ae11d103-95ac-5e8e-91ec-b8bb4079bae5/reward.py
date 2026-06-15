"""
Reward Script: Branch comparison workflow with feature branches
Task ID: vscode_git_063
Domain: vs_code (git)
Scoring:
  Component 1 (0.30): feature/approach-a branch exists with recursive Fibonacci commit
  Component 2 (0.30): feature/approach-b branch exists with iterative memoization Fibonacci commit
  Component 3 (0.20): Both branches diverge from same base commit on main
  Component 4 (0.20): Commit messages for each branch are meaningful (reference the approach)
"""

import os
import subprocess

WORKDIR = '/home/user/project'
TASK_ID = 'vscode_git_063'


def run_git(args, cwd=WORKDIR):
    """Run a git command and return stdout, or raise on error."""
    result = subprocess.run(
        ['git'] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: ensure project directory exists
    if not os.path.isdir(WORKDIR):
        print(f"CRITICAL: Project directory not found: {WORKDIR}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: ensure .git directory exists
    if not os.path.isdir(os.path.join(WORKDIR, '.git')):
        print(f"CRITICAL: Not a git repository: {WORKDIR}")
        print("REWARD: 0.0")
        return 0.0

    # Retrieve all local branch names
    branches_out, branches_err, branches_rc = run_git(['branch'])
    branch_list = [b.strip().lstrip('* ') for b in branches_out.splitlines() if b.strip()]
    print(f"INFO: Branches found: {branch_list}")

    # ------------------------------------------------------------------
    # Component 1: feature/approach-a branch exists with recursive
    #              Fibonacci implementation (0.30 points)
    # ------------------------------------------------------------------
    try:
        if 'feature/approach-a' not in branch_list:
            print("FAIL: Component 1 — branch 'feature/approach-a' does not exist")
        else:
            # Get algorithm.py content from feature/approach-a
            content_a, _, rc_a = run_git(['show', 'feature/approach-a:algorithm.py'])
            if rc_a != 0:
                print(f"FAIL: Component 1 — cannot read algorithm.py from feature/approach-a")
            else:
                # Check for recursive Fibonacci: must call itself (compute_fibonacci(n - 1) style)
                # and must NOT use a memoization dict or for-loop structure
                has_recursive_call = 'compute_fibonacci(n - 1)' in content_a or \
                                     'compute_fibonacci(n-1)' in content_a or \
                                     'compute_fibonacci(n - 1) + compute_fibonacci(n - 2)' in content_a
                has_iterative_memo = ('memo' in content_a and 'for i in range' in content_a) or \
                                     ('for i in range' in content_a and 'memo[i]' in content_a)

                if has_recursive_call and not has_iterative_memo:
                    print(f"PASS: Component 1 — feature/approach-a has recursive Fibonacci (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 1 — feature/approach-a compute_fibonacci is not recursive. "
                          f"has_recursive_call={has_recursive_call}, has_iterative_memo={has_iterative_memo}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: feature/approach-b branch exists with iterative
    #              memoization Fibonacci implementation (0.30 points)
    # ------------------------------------------------------------------
    try:
        if 'feature/approach-b' not in branch_list:
            print("FAIL: Component 2 — branch 'feature/approach-b' does not exist")
        else:
            content_b, _, rc_b = run_git(['show', 'feature/approach-b:algorithm.py'])
            if rc_b != 0:
                print(f"FAIL: Component 2 — cannot read algorithm.py from feature/approach-b")
            else:
                # Check for iterative memoization: dict with memo + for loop
                has_memo_dict = 'memo' in content_b and '{0: 0, 1: 1}' in content_b
                has_for_loop  = 'for i in range' in content_b
                # Must NOT use recursion (no self-call)
                has_recursive_call_b = 'compute_fibonacci(n - 1)' in content_b or \
                                       'compute_fibonacci(n-1)' in content_b

                if has_memo_dict and has_for_loop and not has_recursive_call_b:
                    print(f"PASS: Component 2 — feature/approach-b has iterative memoization Fibonacci (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 2 — feature/approach-b compute_fibonacci is not iterative with memoization. "
                          f"has_memo_dict={has_memo_dict}, has_for_loop={has_for_loop}, has_recursive_call_b={has_recursive_call_b}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: Both feature branches diverge from the same base
    #              commit (same parent commit that lives on main) (0.20 pts)
    # ------------------------------------------------------------------
    try:
        if 'feature/approach-a' not in branch_list or 'feature/approach-b' not in branch_list:
            print("FAIL: Component 3 — one or both branches missing, cannot check common base")
        else:
            # Merge base of the two feature branches
            merge_base_out, _, rc_mb = run_git(['merge-base', 'feature/approach-a', 'feature/approach-b'])
            if rc_mb != 0:
                print(f"FAIL: Component 3 — could not compute merge-base: {merge_base_out}")
            else:
                merge_base_sha = merge_base_out.strip()
                # The merge base must be a commit that exists on main
                main_commits_out, _, _ = run_git(['log', 'main', '--format=%H'])
                main_commits = [s.strip() for s in main_commits_out.splitlines() if s.strip()]
                if merge_base_sha in main_commits:
                    print(f"PASS: Component 3 — both feature branches share common base from main "
                          f"({merge_base_sha[:8]}) (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 3 — merge-base {merge_base_sha[:8]} is NOT on main. "
                          f"Branches may not both derive from main.")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------
    # Component 4: Commit messages on each branch mention the approach
    #              (0.20 points)
    # ------------------------------------------------------------------
    try:
        if 'feature/approach-a' not in branch_list or 'feature/approach-b' not in branch_list:
            print("FAIL: Component 4 — one or both branches missing, cannot check commit messages")
        else:
            # Get commit messages for each branch (only the tip commit, not the base)
            log_a_out, _, _ = run_git(['log', 'main..feature/approach-a', '--format=%s'])
            log_b_out, _, _ = run_git(['log', 'main..feature/approach-b', '--format=%s'])

            msgs_a = [m.strip().lower() for m in log_a_out.splitlines() if m.strip()]
            msgs_b = [m.strip().lower() for m in log_b_out.splitlines() if m.strip()]

            if not msgs_a:
                print("FAIL: Component 4 — feature/approach-a has no commits beyond main")
            elif not msgs_b:
                print("FAIL: Component 4 — feature/approach-b has no commits beyond main")
            else:
                # Check approach-a commit message references 'recursive'
                a_mentions_recursive = any('recursive' in m for m in msgs_a)
                # Check approach-b commit message references 'iterative' or 'memoization'
                b_mentions_iterative = any('iterative' in m or 'memoization' in m or 'memo' in m for m in msgs_b)

                if a_mentions_recursive and b_mentions_iterative:
                    print(f"PASS: Component 4 — both commit messages describe the implementation approach (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 4 — commit messages do not adequately describe approach. "
                          f"approach-a msgs={msgs_a} (recursive={a_mentions_recursive}), "
                          f"approach-b msgs={msgs_b} (iterative/memo={b_mentions_iterative})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.1f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if __name__ == '__main__':
    verify_task()
