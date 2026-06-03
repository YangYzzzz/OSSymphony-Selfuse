"""
Reward Script: Make three separate commits for three different files, then verify git log
Task ID: vscode_git_043
Domain: vs_code (git operations)
Scoring:
  Component 1 (0.4): Exactly 3 new commits exist beyond initial commit (one per feature file),
                     and all 3 feature files appear in HEAD commit tree (no uncommitted files)
  Component 2 (0.4): Each of the 3 new commits has the exact required commit message
  Component 3 (0.2): Each required commit contains exactly the right single file
                     (separate commits, not mixed)

Uses pure Python git object reading (zlib decompression) — no subprocess.
"""

import os
import zlib

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_043'
GIT_DIR = '/home/user/project/.git'
PROJECT_DIR = '/home/user/project'

# Required commit messages — exact text from task context
REQUIRED_MESSAGES = [
    'Add feature A implementation',
    'Add feature B implementation',
    'Add feature C implementation',
]

# Required file per commit (index matches REQUIRED_MESSAGES)
REQUIRED_FILES = [
    'feature_a.py',
    'feature_b.py',
    'feature_c.py',
]


# -----------------------------------------------------------------------
# Git object reader (pure Python, no subprocess)
# -----------------------------------------------------------------------

def read_git_object(obj_hash):
    """Read and decompress a git object by its SHA-1 hash."""
    obj_path = os.path.join(GIT_DIR, 'objects', obj_hash[:2], obj_hash[2:])
    with open(obj_path, 'rb') as f:
        raw = zlib.decompress(f.read())
    header_end = raw.index(b'\x00')
    header = raw[:header_end].decode('utf-8')
    obj_type, _ = header.split(' ', 1)
    data = raw[header_end + 1:]
    return obj_type, data


def parse_commit(data):
    """Parse a git commit object. Returns dict with tree, parent, message."""
    text = data.decode('utf-8')
    lines = text.split('\n')
    info = {}
    for i, line in enumerate(lines):
        if line == '':
            info['message'] = '\n'.join(lines[i + 1:]).strip()
            break
        key, _, val = line.partition(' ')
        if key in ('tree', 'author', 'committer', 'parent'):
            info[key] = val
    return info


def parse_tree(data):
    """Parse a git tree object. Returns list of (mode, name, sha_hex)."""
    files = []
    pos = 0
    while pos < len(data):
        null_pos = data.index(b'\x00', pos)
        mode_name = data[pos:null_pos].decode('utf-8')
        mode, name = mode_name.split(' ', 1)
        sha_bytes = data[null_pos + 1:null_pos + 21]
        sha_hex = sha_bytes.hex()
        files.append((mode, name, sha_hex))
        pos = null_pos + 21
    return files


def get_commit_chain():
    """Walk the commit chain from HEAD. Returns list of (hash, message, tree_hash, parent_hash)."""
    with open(os.path.join(GIT_DIR, 'HEAD')) as f:
        head_ref = f.read().strip()
    if head_ref.startswith('ref: '):
        ref_path = os.path.join(GIT_DIR, head_ref[5:])
        with open(ref_path) as f:
            current = f.read().strip()
    else:
        current = head_ref  # detached HEAD

    commits = []
    visited = set()
    while current and current not in visited:
        visited.add(current)
        obj_type, data = read_git_object(current)
        if obj_type != 'commit':
            break
        info = parse_commit(data)
        commits.append({
            'hash': current,
            'message': info.get('message', ''),
            'tree': info.get('tree', ''),
            'parent': info.get('parent', None),
        })
        current = info.get('parent', None)
    return commits


def get_files_changed_in_commit(commit):
    """Return list of filenames added or modified in this commit vs its parent."""
    _, tdata = read_git_object(commit['tree'])
    current_files = {name: sha for _, name, sha in parse_tree(tdata)}

    if commit['parent'] is None:
        # Root commit — all files are "added"
        return list(current_files.keys())

    _, parent_data = read_git_object(commit['parent'])
    parent_info = parse_commit(parent_data)
    _, ptdata = read_git_object(parent_info['tree'])
    parent_files = {name: sha for _, name, sha in parse_tree(ptdata)}

    changed = []
    for name, sha in current_files.items():
        if name not in parent_files or parent_files[name] != sha:
            changed.append(name)
    # Also detect deletions
    for name in parent_files:
        if name not in current_files:
            changed.append(name)  # deleted file
    return changed


# -----------------------------------------------------------------------
# Verification
# -----------------------------------------------------------------------

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: check the .git directory exists
    if not os.path.isdir(GIT_DIR):
        print(f"CRITICAL: Not a git repository: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Load full commit chain
    try:
        commits = get_commit_chain()
    except Exception as e:
        print(f"CRITICAL: Could not read git history: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not commits:
        print("CRITICAL: Git repository has no commits")
        print("REWARD: 0.0")
        return 0.0

    # Feature commits = all commits except the last one (the initial README commit)
    feature_commits = commits[:-1]

    # ----------------------------------------------------------------
    # Component 1: Exactly 3 new commits, and all 3 feature files are
    #              tracked in the HEAD commit tree (clean state) — 0.4 pts
    # ----------------------------------------------------------------
    try:
        num_feature_commits = len(feature_commits)

        # Check all 3 feature files are in HEAD commit tree
        head_commit = commits[0]
        _, tdata = read_git_object(head_commit['tree'])
        head_tree_files = {name for _, name, _ in parse_tree(tdata)}

        all_files_committed = all(f in head_tree_files for f in REQUIRED_FILES)
        missing_files = [f for f in REQUIRED_FILES if f not in head_tree_files]

        if num_feature_commits == 3 and all_files_committed:
            print(f"PASS: Component 1 — exactly 3 new commits found, all feature files in HEAD tree (0.4 pts)")
            total_score += 0.4
        elif num_feature_commits < 3:
            print(f"FAIL: Component 1 — expected 3 feature commits, found {num_feature_commits}")
        elif num_feature_commits > 3:
            print(f"FAIL: Component 1 — expected 3 feature commits, found {num_feature_commits} (too many)")
        elif missing_files:
            print(f"FAIL: Component 1 — feature files not committed: {missing_files}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: Each of the 3 required messages exists in the commit log — 0.4 pts
    #              Partial credit: 0.4 * (correct / 3)
    # ----------------------------------------------------------------
    try:
        all_messages = [c['message'] for c in commits]
        correct_messages = 0
        for required_msg in REQUIRED_MESSAGES:
            if required_msg in all_messages:
                print(f"  PASS: Found required commit message: '{required_msg}'")
                correct_messages += 1
            else:
                print(f"  FAIL: Missing required commit message: '{required_msg}'")

        if correct_messages == 3:
            print(f"PASS: Component 2 — all 3 required commit messages present (0.4 pts)")
            total_score += 0.4
        elif correct_messages > 0:
            partial = round(0.4 * correct_messages / 3, 4)
            print(f"PARTIAL: Component 2 — {correct_messages}/3 required messages found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no required commit messages found (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: Each required commit contains exactly the right single file — 0.2 pts
    #              Partial credit: 0.2 * (correct / 3)
    # ----------------------------------------------------------------
    try:
        # Build mapping from message -> commit
        msg_to_commit = {c['message']: c for c in commits}

        correct_files = 0
        for i, required_msg in enumerate(REQUIRED_MESSAGES):
            expected_file = REQUIRED_FILES[i]
            if required_msg not in msg_to_commit:
                print(f"  SKIP: Component 3 check for '{required_msg}' — commit not found")
                continue
            commit = msg_to_commit[required_msg]
            changed_files = get_files_changed_in_commit(commit)
            if len(changed_files) == 1 and changed_files[0] == expected_file:
                print(f"  PASS: Commit '{required_msg}' contains exactly '{expected_file}'")
                correct_files += 1
            elif expected_file in changed_files:
                print(f"  PARTIAL: Commit '{required_msg}' contains '{expected_file}' but also other files: {changed_files}")
            else:
                print(f"  FAIL: Commit '{required_msg}' expected '{expected_file}', found: {changed_files}")

        if correct_files == 3:
            print(f"PASS: Component 3 — all 3 commits contain exactly the right single file (0.2 pts)")
            total_score += 0.2
        elif correct_files > 0:
            partial = round(0.2 * correct_files / 3, 4)
            print(f"PARTIAL: Component 3 — {correct_files}/3 commits contain the right file ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no commits contain the correct single file (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
