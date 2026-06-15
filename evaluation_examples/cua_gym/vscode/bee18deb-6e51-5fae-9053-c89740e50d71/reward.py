"""
Reward Script: Commit changes to three files in a specific order with three separate commits
Task ID: vscode_git_093
Domain: vs_code (git operations)
Scoring:
  Component 1: Commit with 'TASK-101: Update database connection pooling' touching database.py (0.35 pts)
  Component 2: Commit with 'TASK-102: Add rate limiting to API endpoints' touching api.py (0.35 pts)
  Component 3: Commit with 'TASK-103: Fix responsive layout issues' touching frontend.js,
               AND all 3 commits in correct chronological order (0.30 pts)
  Total: 1.0

Verification approach: Pure Python git object parsing (zlib + file I/O).
No subprocess used. Reads .git/objects/ and .git/logs/HEAD directly.
"""

import os
import zlib

WORKDIR = '/home/user/project'
TASK_ID = 'vscode_git_093'

# Expected commit messages and their associated file
EXPECTED_COMMITS = [
    ("TASK-101: Update database connection pooling", "database.py"),
    ("TASK-102: Add rate limiting to API endpoints", "api.py"),
    ("TASK-103: Fix responsive layout issues", "frontend.js"),
]


def read_git_object(repo_path, obj_hash):
    """Read a git loose object by hash. Returns (type, content_bytes) or (None, None)."""
    path = os.path.join(repo_path, '.git', 'objects', obj_hash[:2], obj_hash[2:])
    try:
        with open(path, 'rb') as f:
            raw = zlib.decompress(f.read())
        null_idx = raw.index(b'\x00')
        header = raw[:null_idx].decode('utf-8')
        obj_type, _ = header.split(' ', 1)
        content = raw[null_idx + 1:]
        return obj_type, content
    except FileNotFoundError:
        return None, None
    except Exception:
        return None, None


def get_tree_entries(repo_path, tree_hash):
    """Return list of {name, sha} for entries in a tree object."""
    obj_type, content = read_git_object(repo_path, tree_hash)
    if obj_type != 'tree' or content is None:
        return []
    entries = []
    i = 0
    while i < len(content):
        null_pos = content.index(b'\x00', i)
        mode_name = content[i:null_pos].decode('utf-8')
        parts = mode_name.split(' ', 1)
        name = parts[1] if len(parts) > 1 else ''
        sha = content[null_pos + 1:null_pos + 21].hex()
        entries.append({'name': name, 'sha': sha})
        i = null_pos + 21
    return entries


def get_files_changed_in_commit(repo_path, commit_hash):
    """Return list of filenames changed between a commit and its parent.
    Only handles top-level files (not subdirectory changes).
    """
    obj_type, content = read_git_object(repo_path, commit_hash)
    if obj_type != 'commit' or content is None:
        return []

    lines = content.decode('utf-8').split('\n')
    tree_hash = None
    parent_hash = None
    for line in lines:
        if line.startswith('tree '):
            tree_hash = line[5:].strip()
        elif line.startswith('parent '):
            parent_hash = line[7:].strip()

    if tree_hash is None:
        return []

    cur_entries = {e['name']: e['sha'] for e in get_tree_entries(repo_path, tree_hash)}

    if parent_hash:
        par_type, par_content = read_git_object(repo_path, parent_hash)
        if par_type == 'commit' and par_content is not None:
            par_lines = par_content.decode('utf-8').split('\n')
            par_tree_hash = None
            for line in par_lines:
                if line.startswith('tree '):
                    par_tree_hash = line[5:].strip()
                    break
            if par_tree_hash:
                par_entries = {e['name']: e['sha'] for e in get_tree_entries(repo_path, par_tree_hash)}
                # Files changed: those with different SHA or new in this commit
                changed = [
                    name for name, sha in cur_entries.items()
                    if par_entries.get(name) != sha
                ]
                return changed

    # Initial commit: all files are new
    return list(cur_entries.keys())


def parse_commit_history(repo_path):
    """Walk the commit chain from HEAD and return commits in newest-first order.
    Returns list of {hash, subject} dicts.
    Uses the reflog to identify commit hashes and subjects.
    """
    reflog_path = os.path.join(repo_path, '.git', 'logs', 'HEAD')
    commits = []
    try:
        with open(reflog_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []

    # Parse reflog (oldest to newest order in file)
    for line in lines:
        parts = line.strip().split('\t', 1)
        if len(parts) < 2:
            continue
        hash_parts = parts[0].split()
        if len(hash_parts) < 2:
            continue
        new_hash = hash_parts[1]
        action_msg = parts[1]
        # Extract commit message from action string (e.g. "commit: TASK-101: ...")
        if '\tcommit: ' in '\t' + action_msg:
            if 'commit (initial): ' in action_msg:
                subject = action_msg.split('commit (initial): ', 1)[1].strip()
            elif 'commit: ' in action_msg:
                subject = action_msg.split('commit: ', 1)[1].strip()
            else:
                subject = action_msg.strip()
        else:
            subject = action_msg.strip()
        commits.append({'hash': new_hash, 'subject': subject})

    # Return newest-first (last entries in reflog are most recent)
    commits.reverse()
    return commits


def verify_task(repo_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: git repo must exist
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        print(f"CRITICAL: No git repository found at {repo_path}")
        print("REWARD: 0.0")
        return 0.0

    # Get commit history (newest first)
    commits = parse_commit_history(repo_path)
    if not commits:
        print("CRITICAL: No commits found in repository")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(commits)} entries in reflog (newest first)")
    for c in commits[:5]:
        print(f"  {c['hash'][:10]} | {c['subject']}")

    # Build a lookup: message -> first (most recent) commit with that message
    # The task requires the 3 commits to exist - we find the most recent occurrence
    commit_map = {}  # subject -> (hash, reflog_position)
    for idx, commit in enumerate(commits):
        subj = commit['subject']
        if subj not in commit_map:
            commit_map[subj] = (commit['hash'], idx)

    # Component 1: Commit with TASK-101 message touching database.py (0.35 points)
    try:
        msg1 = "TASK-101: Update database connection pooling"
        expected_file1 = "database.py"
        if msg1 in commit_map:
            h1, idx1 = commit_map[msg1]
            changed1 = get_files_changed_in_commit(repo_path, h1)
            if expected_file1 in changed1:
                print(f"PASS: Component 1 — '{msg1}' found touching {expected_file1} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — '{msg1}' commit exists but changed {changed1}, not {expected_file1}")
        else:
            print(f"FAIL: Component 1 — No commit with message '{msg1}' found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Commit with TASK-102 message touching api.py (0.35 points)
    try:
        msg2 = "TASK-102: Add rate limiting to API endpoints"
        expected_file2 = "api.py"
        if msg2 in commit_map:
            h2, idx2 = commit_map[msg2]
            changed2 = get_files_changed_in_commit(repo_path, h2)
            if expected_file2 in changed2:
                print(f"PASS: Component 2 — '{msg2}' found touching {expected_file2} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — '{msg2}' commit exists but changed {changed2}, not {expected_file2}")
        else:
            print(f"FAIL: Component 2 — No commit with message '{msg2}' found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Commit with TASK-103 message touching frontend.js
    # AND all 3 commits in correct order: TASK-101 oldest, TASK-103 newest (0.30 points)
    try:
        msg3 = "TASK-103: Fix responsive layout issues"
        expected_file3 = "frontend.js"
        msg1 = "TASK-101: Update database connection pooling"
        msg2 = "TASK-102: Add rate limiting to API endpoints"

        comp3_score = 0.0
        if msg3 in commit_map:
            h3, idx3 = commit_map[msg3]
            changed3 = get_files_changed_in_commit(repo_path, h3)
            if expected_file3 in changed3:
                print(f"PASS: Component 3a — '{msg3}' found touching {expected_file3}")
                comp3_score += 0.20

                # Check ordering: in newest-first order, idx3 < idx2 < idx1
                # means TASK-103 is most recent, TASK-101 is oldest
                if msg1 in commit_map and msg2 in commit_map:
                    _, idx1 = commit_map[msg1]
                    _, idx2 = commit_map[msg2]
                    if idx3 < idx2 < idx1:
                        print(f"PASS: Component 3b — Correct commit order: "
                              f"TASK-101 (pos {idx1}) → TASK-102 (pos {idx2}) → TASK-103 (pos {idx3}) (0.10 pts)")
                        comp3_score += 0.10
                    else:
                        print(f"FAIL: Component 3b — Commit order incorrect: "
                              f"TASK-101 pos={idx1}, TASK-102 pos={idx2}, TASK-103 pos={idx3}. "
                              f"Expected pos3 < pos2 < pos1 (newest-first ordering)")
                else:
                    print("INFO: Component 3b — Cannot verify ordering (not all 3 commit messages found)")
                    # Don't penalize for ordering if other commits are missing
                    comp3_score += 0.10

                if comp3_score > 0:
                    print(f"PASS: Component 3 total: {comp3_score} pts")
                    total_score += comp3_score
            else:
                print(f"FAIL: Component 3 — '{msg3}' commit exists but changed {changed3}, not {expected_file3}")
        else:
            print(f"FAIL: Component 3 — No commit with message '{msg3}' found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.isdir(WORKDIR):
    print(f"Repository not found: {WORKDIR}")
    print("REWARD: 0.0")
else:
    verify_task(WORKDIR)
