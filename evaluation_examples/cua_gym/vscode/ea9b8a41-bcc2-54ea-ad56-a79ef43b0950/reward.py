"""
Reward Script: Set up a complete tagging strategy with lightweight and annotated tags
Task ID: vscode_git_065
Domain: vs_code (git operations)
Scoring:
  Component 1: Lightweight tags dev-milestone-1, dev-milestone-2, dev-milestone-3 exist
               as lightweight tags pointing to correct commits (HEAD~8, HEAD~5, HEAD~2) — 0.40 points
  Component 2: Annotated tags v1.0.0, v1.1.0, v2.0.0 exist as annotated tag objects
               pointing to correct commits (HEAD~6, HEAD~3, HEAD) — 0.30 points
  Component 3: Annotated tag messages match expected values
               ("First stable release", "Feature update", "Major release") — 0.30 points
"""

import os
import zlib

REPO_PATH = '/home/user/project'
GIT_DIR = os.path.join(REPO_PATH, '.git')
TASK_ID = 'vscode_git_065'


def read_git_object(obj_hash):
    """Read and decompress a loose git object. Returns (obj_type, raw_content) or (None, None)."""
    obj_path = os.path.join(GIT_DIR, 'objects', obj_hash[:2], obj_hash[2:])
    if not os.path.exists(obj_path):
        return None, None
    with open(obj_path, 'rb') as f:
        data = zlib.decompress(f.read())
    null_idx = data.index(b'\x00')
    header = data[:null_idx].decode('utf-8')
    content = data[null_idx + 1:]
    obj_type = header.split(' ')[0]
    return obj_type, content


def read_ref(ref_path):
    """Read a git reference file, following symbolic refs if needed."""
    full_path = os.path.join(GIT_DIR, ref_path)
    if not os.path.exists(full_path):
        return None
    with open(full_path) as f:
        val = f.read().strip()
    if val.startswith('ref: '):
        # Symbolic ref — follow it
        return read_ref(val[5:])
    return val


def get_commit_hash_at_ref(ref_name):
    """Get the commit hash that a ref points to (dereferences tag objects)."""
    ref_hash = read_ref(os.path.join('refs', 'tags', ref_name)) or \
               read_ref(os.path.join('refs', 'heads', ref_name))
    if not ref_hash:
        return None
    # If it's a tag object, dereference to get the commit
    obj_type, content = read_git_object(ref_hash)
    if obj_type == 'tag':
        # Parse the 'object' line to get the underlying commit hash
        lines = content.decode('utf-8', errors='replace').split('\n')
        for line in lines:
            if line.startswith('object '):
                return line[7:].strip()
        return None
    elif obj_type == 'commit':
        return ref_hash
    return None


def get_commit_history(head_hash):
    """Walk the commit chain from HEAD and return list of commit hashes in order."""
    commits = []
    current = head_hash
    for _ in range(20):  # Safety limit
        if current is None:
            break
        obj_type, content = read_git_object(current)
        if obj_type != 'commit':
            break
        commits.append(current)
        # Find parent line
        lines = content.decode('utf-8', errors='replace').split('\n')
        parent = None
        for line in lines:
            if line.startswith('parent '):
                parent = line[7:].strip()
                break
        current = parent
    return commits


def get_tag_type(tag_name):
    """Return 'lightweight' or 'annotated' or None if tag doesn't exist."""
    ref_file = os.path.join(GIT_DIR, 'refs', 'tags', tag_name)
    if not os.path.exists(ref_file):
        return None
    with open(ref_file) as f:
        ref_hash = f.read().strip()
    obj_type, _ = read_git_object(ref_hash)
    if obj_type == 'commit':
        return 'lightweight'
    elif obj_type == 'tag':
        return 'annotated'
    return None


def get_tag_target_hash(tag_name):
    """Get the raw hash stored in the tag ref (NOT dereferenced)."""
    ref_file = os.path.join(GIT_DIR, 'refs', 'tags', tag_name)
    if not os.path.exists(ref_file):
        return None
    with open(ref_file) as f:
        return f.read().strip()


def get_annotated_tag_message(tag_name):
    """Get the message body of an annotated tag. Returns None if not annotated."""
    ref_hash = get_tag_target_hash(tag_name)
    if ref_hash is None:
        return None
    obj_type, content = read_git_object(ref_hash)
    if obj_type != 'tag':
        return None
    lines = content.decode('utf-8', errors='replace').split('\n')
    # Tag format: header lines, blank line, then message
    for i, line in enumerate(lines):
        if line == '':
            # Message starts after the blank line
            return lines[i + 1].strip() if i + 1 < len(lines) else ''
    return ''


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: verify the repo and .git directory exists
    if not os.path.isdir(GIT_DIR):
        print(f"CRITICAL: No .git directory found at {GIT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Get HEAD hash for computing relative commit positions
    head_hash = read_ref('HEAD')
    if not head_hash:
        print("CRITICAL: Cannot read HEAD ref")
        print("REWARD: 0.0")
        return 0.0

    # Build commit history (HEAD, HEAD~1, HEAD~2, ...)
    commits = get_commit_history(head_hash)
    if len(commits) < 9:
        print(f"CRITICAL: Expected at least 9 commits, found {len(commits)}")
        print("REWARD: 0.0")
        return 0.0

    # Map relative refs to actual commit hashes using index into history list
    # commits[0] = HEAD, commits[1] = HEAD~1, ..., commits[N] = HEAD~N
    head_at = {
        'HEAD': commits[0],
        'HEAD~2': commits[2],
        'HEAD~3': commits[3],
        'HEAD~5': commits[5],
        'HEAD~6': commits[6],
        'HEAD~8': commits[8],
    }

    # Component 1: Lightweight tags exist and point to correct commits (0.40 points)
    # dev-milestone-1 -> HEAD~8, dev-milestone-2 -> HEAD~5, dev-milestone-3 -> HEAD~2
    try:
        expected_lightweight = {
            'dev-milestone-1': 'HEAD~8',
            'dev-milestone-2': 'HEAD~5',
            'dev-milestone-3': 'HEAD~2',
        }

        all_lightweight_ok = True
        for tag_name, rel_ref in expected_lightweight.items():
            expected_commit = head_at[rel_ref]
            tag_type = get_tag_type(tag_name)

            if tag_type is None:
                print(f"FAIL: Component 1 — tag '{tag_name}' does not exist")
                all_lightweight_ok = False
                continue

            if tag_type != 'lightweight':
                print(f"FAIL: Component 1 — tag '{tag_name}' is {tag_type}, expected lightweight")
                all_lightweight_ok = False
                continue

            # For lightweight tags, the ref hash IS the commit hash
            actual_commit = get_tag_target_hash(tag_name)
            if actual_commit == expected_commit:
                print(f"PASS: Component 1 — lightweight tag '{tag_name}' "
                      f"-> {expected_commit[:8]} ({rel_ref})")
            else:
                print(f"FAIL: Component 1 — '{tag_name}' points to {actual_commit[:8] if actual_commit else 'None'}, "
                      f"expected {expected_commit[:8]} ({rel_ref})")
                all_lightweight_ok = False

        if all_lightweight_ok:
            print("PASS: Component 1 — all 3 lightweight milestone tags are correct (0.40 pts)")
            total_score += 0.40
        else:
            print("FAIL: Component 1 — one or more lightweight tags are missing or incorrect")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Annotated tags exist as tag objects pointing to correct commits (0.30 points)
    # v1.0.0 -> HEAD~6, v1.1.0 -> HEAD~3, v2.0.0 -> HEAD
    try:
        expected_annotated = {
            'v1.0.0': 'HEAD~6',
            'v1.1.0': 'HEAD~3',
            'v2.0.0': 'HEAD',
        }

        all_annotated_ok = True
        for tag_name, rel_ref in expected_annotated.items():
            expected_commit = head_at[rel_ref]
            tag_type = get_tag_type(tag_name)

            if tag_type is None:
                print(f"FAIL: Component 2 — tag '{tag_name}' does not exist")
                all_annotated_ok = False
                continue

            if tag_type != 'annotated':
                print(f"FAIL: Component 2 — tag '{tag_name}' is {tag_type}, expected annotated")
                all_annotated_ok = False
                continue

            # For annotated tags, dereference the tag object to get the commit
            actual_commit = get_commit_hash_at_ref(tag_name)
            if actual_commit == expected_commit:
                print(f"PASS: Component 2 — annotated tag '{tag_name}' "
                      f"-> {expected_commit[:8]} ({rel_ref})")
            else:
                actual_short = actual_commit[:8] if actual_commit else 'None'
                print(f"FAIL: Component 2 — '{tag_name}' points to commit {actual_short}, "
                      f"expected {expected_commit[:8]} ({rel_ref})")
                all_annotated_ok = False

        if all_annotated_ok:
            print("PASS: Component 2 — all 3 annotated version tags are correct (0.30 pts)")
            total_score += 0.30
        else:
            print("FAIL: Component 2 — one or more annotated tags are missing or incorrect")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Annotated tag messages are correct (0.30 points)
    # v1.0.0 -> "First stable release", v1.1.0 -> "Feature update", v2.0.0 -> "Major release"
    try:
        expected_messages = {
            'v1.0.0': 'First stable release',
            'v1.1.0': 'Feature update',
            'v2.0.0': 'Major release',
        }

        all_messages_ok = True
        for tag_name, expected_msg in expected_messages.items():
            actual_msg = get_annotated_tag_message(tag_name)
            if actual_msg is None:
                print(f"FAIL: Component 3 — cannot get message for tag '{tag_name}' "
                      f"(not annotated or missing)")
                all_messages_ok = False
                continue

            if actual_msg == expected_msg:
                print(f"PASS: Component 3 — tag '{tag_name}' message: '{actual_msg}'")
            else:
                print(f"FAIL: Component 3 — tag '{tag_name}': "
                      f"expected '{expected_msg}', found '{actual_msg}'")
                all_messages_ok = False

        if all_messages_ok:
            print("PASS: Component 3 — all annotated tag messages are correct (0.30 pts)")
            total_score += 0.30
        else:
            print("FAIL: Component 3 — one or more tag messages are incorrect")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the git repo
if not os.path.isdir(REPO_PATH):
    print(f"CRITICAL: Project directory not found: {REPO_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
