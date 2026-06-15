"""
Reward Script: Create comprehensive Git tag management workflow
Task ID: vscode_git_079
Domain: vs_code
Scoring:
  - Component 1: v1.0.0 annotated tag exists at commit 3 (Release 1.0.0) on main — 0.3 pts
  - Component 2: v1.0.0-dev lightweight tag exists at commit 5 (Add configuration module) — 0.2 pts
  - Component 3: v2.0.0-rc2 annotated tag exists at HEAD of release/v2 — 0.3 pts
  - Component 4: v2.0.0-rc1 does NOT exist (was deleted) — 0.1 pts
  - Component 5: Exactly the expected tags present (v1.0.0, v1.0.0-dev, v2.0.0-rc2) — 0.1 pts
Total: 1.0
"""

import os
import sys

PROJECT_DIR = '/home/user/project'

# Expected commit subjects for identifying tagged commits
V100_COMMIT_MSG = "Release 1.0.0: add core package structure"   # commit 3 on main
V100DEV_COMMIT_MSG = "Add configuration module with defaults"    # commit 5 on main
EXPECTED_TAGS = {"v1.0.0", "v1.0.0-dev", "v2.0.0-rc2"}
DELETED_TAG = "v2.0.0-rc1"


def run_git(args, cwd=PROJECT_DIR):
    """Run a git command and return (returncode, stdout, stderr)."""
    import subprocess as _sp
    result = _sp.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def verify_task():
    """
    Verify task completion: Git tag management workflow.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Pre-check: ensure git repo exists
    if not os.path.isdir(os.path.join(PROJECT_DIR, '.git')):
        print(f"CRITICAL: {PROJECT_DIR} is not a git repository")
        print("REWARD: 0.0")
        return 0.0

    # Get all tags
    rc, tag_list_output, err = run_git(["tag", "--list"])
    if rc != 0:
        print(f"CRITICAL: git tag --list failed: {err}")
        print("REWARD: 0.0")
        return 0.0

    existing_tags = set(tag_list_output.splitlines()) if tag_list_output else set()
    print(f"INFO: Current tags: {sorted(existing_tags)}")

    # -------------------------------------------------------------------
    # Component 1: v1.0.0 is an annotated tag pointing to commit with
    #              message "Release 1.0.0: add core package structure" (0.3 points)
    # -------------------------------------------------------------------
    try:
        if "v1.0.0" in existing_tags:
            # Check it is annotated (type == 'tag' object, not 'commit')
            rc_type, tag_type, _ = run_git(["cat-file", "-t", "v1.0.0"])
            is_annotated = (rc_type == 0 and tag_type == "tag")

            if is_annotated:
                # Verify it points to the correct commit
                rc_commit, commit_sha, _ = run_git(["rev-parse", "v1.0.0^{}"])
                rc_msg, commit_msg, _ = run_git(["log", "-1", "--format=%s", commit_sha.strip()])
                correct_commit = (rc_msg == 0 and V100_COMMIT_MSG in commit_msg)

                if correct_commit:
                    print(f"PASS: Component 1 — v1.0.0 is annotated tag at correct commit (0.3 pts)")
                    print(f"      Commit msg: '{commit_msg}'")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 1 — v1.0.0 is annotated but points to wrong commit")
                    print(f"      Commit msg found: '{commit_msg}', expected: '{V100_COMMIT_MSG}'")
            else:
                print(f"FAIL: Component 1 — v1.0.0 exists but is not annotated (type: {tag_type})")
        else:
            print(f"FAIL: Component 1 — v1.0.0 tag does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------
    # Component 2: v1.0.0-dev is a lightweight tag pointing to commit with
    #              message "Add configuration module with defaults" (0.2 points)
    # -------------------------------------------------------------------
    try:
        if "v1.0.0-dev" in existing_tags:
            # Check it is lightweight (type == 'commit' directly, not 'tag' object)
            rc_type, tag_type, _ = run_git(["cat-file", "-t", "v1.0.0-dev"])
            is_lightweight = (rc_type == 0 and tag_type == "commit")

            if is_lightweight:
                # Verify it points to the correct commit
                rc_commit, commit_sha, _ = run_git(["rev-parse", "v1.0.0-dev"])
                rc_msg, commit_msg, _ = run_git(["log", "-1", "--format=%s", commit_sha.strip()])
                correct_commit = (rc_msg == 0 and V100DEV_COMMIT_MSG in commit_msg)

                if correct_commit:
                    print(f"PASS: Component 2 — v1.0.0-dev is lightweight tag at correct commit (0.2 pts)")
                    print(f"      Commit msg: '{commit_msg}'")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 2 — v1.0.0-dev is lightweight but points to wrong commit")
                    print(f"      Commit msg found: '{commit_msg}', expected: '{V100DEV_COMMIT_MSG}'")
            else:
                print(f"FAIL: Component 2 — v1.0.0-dev exists but is not lightweight (type: {tag_type})")
        else:
            print(f"FAIL: Component 2 — v1.0.0-dev tag does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------
    # Component 3: v2.0.0-rc2 is an annotated tag at HEAD of release/v2 (0.3 points)
    # -------------------------------------------------------------------
    try:
        if "v2.0.0-rc2" in existing_tags:
            # Check it is annotated
            rc_type, tag_type, _ = run_git(["cat-file", "-t", "v2.0.0-rc2"])
            is_annotated = (rc_type == 0 and tag_type == "tag")

            if is_annotated:
                # Verify it points to the HEAD of release/v2 branch
                rc_tag_commit, tag_commit, _ = run_git(["rev-parse", "v2.0.0-rc2^{}"])
                rc_branch_head, branch_head, _ = run_git(["rev-parse", "release/v2"])

                correct_position = (
                    rc_tag_commit == 0 and rc_branch_head == 0 and
                    tag_commit.strip() == branch_head.strip()
                )

                if correct_position:
                    print(f"PASS: Component 3 — v2.0.0-rc2 is annotated tag at HEAD of release/v2 (0.3 pts)")
                    print(f"      Tag commit: {tag_commit.strip()}, branch HEAD: {branch_head.strip()}")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — v2.0.0-rc2 is annotated but not at HEAD of release/v2")
                    print(f"      Tag commit: {tag_commit.strip()}, branch HEAD: {branch_head.strip()}")
            else:
                print(f"FAIL: Component 3 — v2.0.0-rc2 exists but is not annotated (type: {tag_type})")
        else:
            print(f"FAIL: Component 3 — v2.0.0-rc2 tag does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------
    # Component 4: v2.0.0-rc1 does NOT exist (was deleted as superseded) AND
    #              v2.0.0-rc2 exists (meaning rc1 was created then intentionally deleted,
    #              not just never created) (0.1 points)
    # This compound check ensures we score the intentional deletion action, not absence-by-default.
    # -------------------------------------------------------------------
    try:
        rc1_absent = DELETED_TAG not in existing_tags
        rc2_present = "v2.0.0-rc2" in existing_tags

        if rc1_absent and rc2_present:
            print(f"PASS: Component 4 — v2.0.0-rc1 is absent and v2.0.0-rc2 exists (correct deletion workflow) (0.1 pts)")
            total_score += 0.1
        elif not rc1_absent:
            print(f"FAIL: Component 4 — v2.0.0-rc1 still exists but should have been deleted")
        else:
            # rc2 is also absent - the deletion workflow hasn't been done at all
            print(f"FAIL: Component 4 — v2.0.0-rc2 is also absent; rc1 deletion workflow not completed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -------------------------------------------------------------------
    # Component 5: Exactly the expected set of tags present (0.1 points)
    # -------------------------------------------------------------------
    try:
        if existing_tags == EXPECTED_TAGS:
            print(f"PASS: Component 5 — Exactly expected tags present: {sorted(EXPECTED_TAGS)} (0.1 pts)")
            total_score += 0.1
        else:
            extra = existing_tags - EXPECTED_TAGS
            missing = EXPECTED_TAGS - existing_tags
            print(f"FAIL: Component 5 — Tag set mismatch")
            if extra:
                print(f"      Extra (unexpected) tags: {sorted(extra)}")
            if missing:
                print(f"      Missing tags: {sorted(missing)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()
