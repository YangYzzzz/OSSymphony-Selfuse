"""
Reward Script: Git Cherry-Pick Security Fixes Backport
Task ID: vscode_gf6_019
Domain: vscode
Scoring:
  - Component 1 (0.30): 3 cherry-picked [SECURITY] commits exist on release/v2.0
  - Component 2 (0.25): Cherry-pick provenance — each has "(cherry picked from commit ...)"
  - Component 3 (0.20): CHANGELOG.md has a NEW section documenting backported security fixes
  - Component 4 (0.15): release/v2.0 has >= 12 commits (9 original + 3 cherry-picks + changelog)
  - Component 5 (0.10): No unresolved merge conflicts AND release/v2.0 is checked out
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_019'
REPO_DIR = os.path.join(WORKDIR, 'projects', 'git-cherry-pick')


def run_git(args):
    """Run a git command in the repo directory and return stdout."""
    import subprocess
    result = subprocess.run(
        ['git'] + args,
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        timeout=10
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repo exists
    if not os.path.isdir(REPO_DIR):
        print(f"CRITICAL: Repository not found at {REPO_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: release/v2.0 branch exists
    stdout, stderr, rc = run_git(['branch', '--list', 'release/v2.0'])
    if not stdout.strip():
        print("CRITICAL: release/v2.0 branch does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 3 cherry-picked [SECURITY] commits on release/v2.0 (0.30 points)
    # On initial_env, release/v2.0 has NO [SECURITY] commits. On golden, it has 3.
    # IMPORTANT: Use --fixed-strings so [SECURITY] is literal, not regex char class
    try:
        stdout, stderr, rc = run_git([
            'log', 'release/v2.0', '--oneline',
            '--fixed-strings', '--grep=[SECURITY]'
        ])
        security_commits = [line for line in stdout.split('\n') if line.strip()] if stdout else []
        num_security = len(security_commits)

        if num_security >= 3:
            print(f"PASS: Component 1 — Found {num_security} [SECURITY] commits on release/v2.0 (0.30 pts)")
            total_score += 0.30
        elif num_security > 0:
            partial = 0.10 * num_security
            print(f"PARTIAL: Component 1 — Found {num_security}/3 [SECURITY] commits on release/v2.0 ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No [SECURITY] commits found on release/v2.0")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Cherry-pick provenance (0.25 points)
    # Each cherry-picked commit should contain "(cherry picked from commit <sha>)"
    try:
        stdout, stderr, rc = run_git([
            'log', 'release/v2.0',
            '--fixed-strings', '--grep=[SECURITY]',
            '--format=%H'
        ])
        cherry_shas = [line.strip() for line in stdout.split('\n') if line.strip()] if stdout else []

        provenance_count = 0
        for sha in cherry_shas:
            msg_stdout, _, _ = run_git(['log', '-1', '--format=%B', sha])
            if '(cherry picked from commit' in msg_stdout:
                provenance_count += 1

        if len(cherry_shas) >= 3 and provenance_count >= 3:
            print(f"PASS: Component 2 — All {provenance_count} cherry-pick commits have provenance markers (0.25 pts)")
            total_score += 0.25
        elif provenance_count > 0:
            partial = round(0.25 * (provenance_count / 3), 2)
            print(f"PARTIAL: Component 2 — {provenance_count}/3 commits have provenance ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No cherry-pick provenance markers found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: CHANGELOG.md has a NEW section for backported security fixes (0.20 points)
    # Initial CHANGELOG.md has [2.0.0] and [1.0.0] sections only.
    # Golden CHANGELOG.md adds a [2.0.1] section with "Security" or "Backported" entries.
    # We check for content that does NOT exist in the initial CHANGELOG:
    #   - A version section newer than [2.0.0] (e.g., [2.0.1])
    #   - OR a "Security" subsection with backport-related keywords
    # The initial [2.0.0] section mentions "Authentication module with password hashing" but
    # does NOT mention "bcrypt", "SQL injection", "HTTPS redirect", or "backport".
    try:
        run_git(['checkout', 'release/v2.0'])
        changelog_path = os.path.join(REPO_DIR, 'CHANGELOG.md')

        if not os.path.exists(changelog_path):
            print(f"FAIL: Component 3 — CHANGELOG.md not found on release/v2.0")
        else:
            with open(changelog_path, 'r') as f:
                changelog_content = f.read()
            cl_lower = changelog_content.lower()

            # These keywords are NOT in the initial CHANGELOG and indicate the security backport
            backport_indicators = [
                'bcrypt',           # password hashing upgrade to bcrypt
                'sql injection',    # SQL injection fix
                'https redirect',   # HTTPS redirect enforcement
                'backport',         # explicit backport mention
            ]

            indicators_found = sum(1 for kw in backport_indicators if kw in cl_lower)

            # Check for a new version section (anything beyond [2.0.0])
            has_new_version = bool(re.search(r'\[2\.0\.[1-9]\]|\[2\.[1-9]', cl_lower))

            if indicators_found >= 3 or (indicators_found >= 2 and has_new_version):
                print(f"PASS: Component 3 — CHANGELOG.md has new security backport entries ({indicators_found} indicators, new_version={has_new_version}) (0.20 pts)")
                total_score += 0.20
            elif indicators_found >= 1:
                partial = round(0.20 * (indicators_found / 3), 2)
                print(f"PARTIAL: Component 3 — CHANGELOG has {indicators_found}/3 backport indicators ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — CHANGELOG.md has no security backport entries")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: release/v2.0 has >= 12 commits (0.15 points)
    # Initial: 9 commits. Golden: 13 (9 + 3 cherry-picks + 1 changelog commit).
    # We check for > 9 to detect that cherry-picks were added.
    try:
        stdout, stderr, rc = run_git(['rev-list', '--count', 'release/v2.0'])
        commit_count = int(stdout.strip())

        if commit_count >= 12:
            print(f"PASS: Component 4 — release/v2.0 has {commit_count} commits (>= 12) (0.15 pts)")
            total_score += 0.15
        elif commit_count >= 11:
            print(f"PARTIAL: Component 4 — release/v2.0 has {commit_count} commits (0.10 pts)")
            total_score += 0.10
        elif commit_count >= 10:
            print(f"PARTIAL: Component 4 — release/v2.0 has {commit_count} commits (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 — release/v2.0 has only {commit_count} commits (expected >= 12)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Working tree clean on release/v2.0 AND cherry-pick commits reference
    # the correct original main SHAs (0.10 points)
    # This checks that the cherry-picks reference real main-branch [SECURITY] commits
    try:
        run_git(['checkout', 'release/v2.0'])
        stdout, stderr, rc = run_git(['status', '--porcelain'])
        tree_clean = not stdout.strip()

        if not tree_clean:
            print(f"FAIL: Component 5 — Working tree has uncommitted changes or conflicts")
        else:
            # Check that cherry-pick provenance references valid main commits
            stdout, stderr, rc = run_git([
                'log', 'release/v2.0',
                '--fixed-strings', '--grep=[SECURITY]',
                '--format=%B'
            ])
            # Extract referenced SHAs from "(cherry picked from commit <sha>)"
            referenced_shas = re.findall(r'\(cherry picked from commit ([0-9a-f]+)\)', stdout)

            # Verify each referenced SHA exists on main
            valid_refs = 0
            for sha in referenced_shas:
                check_stdout, _, check_rc = run_git(['branch', '--contains', sha, '--list', 'main'])
                if 'main' in check_stdout:
                    valid_refs += 1

            if valid_refs >= 3:
                print(f"PASS: Component 5 — Clean tree + {valid_refs} cherry-picks reference valid main commits (0.10 pts)")
                total_score += 0.10
            elif valid_refs >= 1:
                partial = round(0.10 * (valid_refs / 3), 2)
                print(f"PARTIAL: Component 5 — Clean tree + {valid_refs}/3 valid references ({partial} pts)")
                total_score += partial
            else:
                # Tree clean but no cherry-pick refs found — this is the initial state, no points
                print(f"FAIL: Component 5 — No cherry-pick SHA references found on release/v2.0")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
