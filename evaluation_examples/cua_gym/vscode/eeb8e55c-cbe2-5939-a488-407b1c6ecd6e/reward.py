"""
Reward Script: Stage all modified files and commit with specific message
Task ID: vscode_web_011
Domain: vscode
Scoring:
  Component 1 (0.3): New commit exists beyond initial commit
  Component 2 (0.4): HEAD commit message matches expected
  Component 3 (0.3): All 3 files in HEAD commit, working tree clean
"""

import os
import zlib

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_011'
REPO_PATH = os.path.join(WORKDIR, 'projects', 'webapp')
GIT_DIR = os.path.join(REPO_PATH, '.git')

EXPECTED_MESSAGE = 'feat: add responsive navigation component'
EXPECTED_FILES = {'src/App.jsx', 'src/components/Nav.jsx', 'src/styles/nav.css'}


def read_git_object(sha):
    """Read a git object by its SHA hash, return (type, content)."""
    obj_path = os.path.join(GIT_DIR, 'objects', sha[:2], sha[2:])
    with open(obj_path, 'rb') as f:
        raw = zlib.decompress(f.read())
    # Format: "<type> <size>\0<content>"
    header_end = raw.index(b'\x00')
    header = raw[:header_end].decode('ascii')
    obj_type, _ = header.split(' ', 1)
    content = raw[header_end + 1:]
    return obj_type, content


def resolve_ref(ref_path):
    """Resolve a git ref to a SHA hash."""
    full_path = os.path.join(GIT_DIR, ref_path)
    if os.path.exists(full_path):
        return open(full_path).read().strip()
    # Try packed-refs
    packed_refs = os.path.join(GIT_DIR, 'packed-refs')
    if os.path.exists(packed_refs):
        for line in open(packed_refs):
            line = line.strip()
            if line.startswith('#'):
                continue
            parts = line.split(' ', 1)
            if len(parts) == 2 and parts[1] == ref_path:
                return parts[0]
    return None


def get_head_sha():
    """Get the SHA of HEAD."""
    head_content = open(os.path.join(GIT_DIR, 'HEAD')).read().strip()
    if head_content.startswith('ref: '):
        ref = head_content[5:]
        return resolve_ref(ref)
    return head_content  # detached HEAD


def parse_commit(sha):
    """Parse a commit object, return dict with tree, parent(s), message."""
    obj_type, content = read_git_object(sha)
    if obj_type != 'commit':
        return None
    text = content.decode('utf-8', errors='replace')
    lines = text.split('\n')
    result = {'parents': []}
    i = 0
    while i < len(lines) and lines[i]:
        if lines[i].startswith('tree '):
            result['tree'] = lines[i][5:]
        elif lines[i].startswith('parent '):
            result['parents'].append(lines[i][7:])
        i += 1
    # Message is everything after the blank line
    result['message'] = '\n'.join(lines[i + 1:]).strip() if i < len(lines) else ''
    return result


def count_commits(sha, limit=20):
    """Count commits reachable from sha."""
    count = 0
    current = sha
    while current and count < limit:
        commit = parse_commit(current)
        if not commit:
            break
        count += 1
        current = commit['parents'][0] if commit['parents'] else None
    return count


def list_tree_files(tree_sha, prefix=''):
    """Recursively list files in a tree object."""
    _, content = read_git_object(tree_sha)
    files = []
    pos = 0
    while pos < len(content):
        # Format: "<mode> <name>\0<20-byte-sha>"
        null_pos = content.index(b'\x00', pos)
        entry = content[pos:null_pos].decode('ascii')
        mode, name = entry.split(' ', 1)
        sha_bytes = content[null_pos + 1:null_pos + 21]
        sha = sha_bytes.hex()
        pos = null_pos + 21
        full_name = f"{prefix}{name}" if not prefix else f"{prefix}/{name}"
        if mode.startswith('4'):  # directory (tree)
            files.extend(list_tree_files(sha, full_name))
        else:
            files.append(full_name)
    return files


def diff_trees(tree_sha1, tree_sha2):
    """Get files that differ between two trees (simple: compare file lists and shas)."""
    files1 = set(list_tree_files(tree_sha1))
    files2 = set(list_tree_files(tree_sha2))
    # Files only in tree2 or in both but different content
    return files2 - files1  # Simplified: new/changed files


def get_changed_files_in_commit(sha):
    """Get list of files changed in a commit by comparing to parent tree."""
    commit = parse_commit(sha)
    if not commit:
        return set()

    head_tree = commit['tree']
    head_files = set(list_tree_files(head_tree))

    if not commit['parents']:
        # Root commit: all files are new
        return head_files

    parent = parse_commit(commit['parents'][0])
    if not parent:
        return head_files

    parent_tree = parent['tree']
    parent_files_list = list_tree_files(parent_tree)
    parent_files = set(parent_files_list)

    # Files added or potentially changed
    # For a proper diff we'd compare blob SHAs, but for this task
    # we just need to know which files are in the commit
    # Since all 3 files existed before and were modified, they should appear
    # in the tree of both commits. We need to check blob SHA differences.
    return get_changed_blobs(parent_tree, head_tree)


def get_tree_entries(tree_sha, prefix=''):
    """Get {path: blob_sha} for all files in a tree."""
    _, content = read_git_object(tree_sha)
    entries = {}
    pos = 0
    while pos < len(content):
        null_pos = content.index(b'\x00', pos)
        entry = content[pos:null_pos].decode('ascii')
        mode, name = entry.split(' ', 1)
        sha_bytes = content[null_pos + 1:null_pos + 21]
        sha = sha_bytes.hex()
        pos = null_pos + 21
        full_name = f"{prefix}{name}" if not prefix else f"{prefix}/{name}"
        if mode.startswith('4'):
            entries.update(get_tree_entries(sha, full_name))
        else:
            entries[full_name] = sha
    return entries


def get_changed_blobs(parent_tree_sha, head_tree_sha):
    """Compare two trees and return set of files with different blob SHAs."""
    parent_entries = get_tree_entries(parent_tree_sha)
    head_entries = get_tree_entries(head_tree_sha)
    changed = set()
    for path, blob_sha in head_entries.items():
        if path not in parent_entries or parent_entries[path] != blob_sha:
            changed.add(path)
    for path in parent_entries:
        if path not in head_entries:
            changed.add(path)
    return changed


def check_working_tree_clean():
    """Check if working tree is clean by comparing HEAD tree to working directory."""
    head_sha = get_head_sha()
    if not head_sha:
        return False
    commit = parse_commit(head_sha)
    if not commit:
        return False

    # Check index: if .git/index mtime > last commit, there might be staged changes
    # Simpler approach: check if the 3 expected files match their blob content
    tree_entries = get_tree_entries(commit['tree'])

    for fpath, blob_sha in tree_entries.items():
        full_path = os.path.join(REPO_PATH, fpath)
        if not os.path.exists(full_path):
            return False  # File missing
        # Read working copy
        with open(full_path, 'rb') as f:
            working_content = f.read()
        # Read blob content
        _, blob_content = read_git_object(blob_sha)
        if working_content != blob_content:
            return False  # Modified in working tree

    # Also check no untracked files that are relevant (simplified)
    return True


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repo exists
    if not os.path.isdir(GIT_DIR):
        print(f"CRITICAL: Not a git repo: {REPO_PATH}")
        print("REWARD: 0.0")
        return 0.0

    head_sha = get_head_sha()
    if not head_sha:
        print("CRITICAL: Cannot resolve HEAD")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: New commit exists beyond initial (0.3 points)
    # Initial state has exactly 1 commit. Golden should have >= 2.
    try:
        commit_count = count_commits(head_sha)
        if commit_count >= 2:
            print(f"PASS: Component 1 — commit count is {commit_count} (>= 2) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — commit count is {commit_count}, expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: HEAD commit message matches expected (0.4 points)
    try:
        commit = parse_commit(head_sha)
        if commit:
            head_message = commit['message'].split('\n')[0].strip()
            if head_message == EXPECTED_MESSAGE:
                print(f"PASS: Component 2 — HEAD message matches: '{head_message}' (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — HEAD message: '{head_message}', expected: '{EXPECTED_MESSAGE}'")
        else:
            print("FAIL: Component 2 — Could not parse HEAD commit")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 3 files in HEAD commit AND working tree is clean (0.3 points)
    try:
        changed_files = get_changed_files_in_commit(head_sha)
        files_present = EXPECTED_FILES.issubset(changed_files)
        wt_clean = check_working_tree_clean()

        if files_present and wt_clean:
            print(f"PASS: Component 3 — All 3 files committed, working tree clean (0.3 pts)")
            total_score += 0.3
        else:
            if not files_present:
                missing = EXPECTED_FILES - changed_files
                print(f"FAIL: Component 3 — Missing files in HEAD commit: {missing} (found: {changed_files})")
            if not wt_clean:
                print(f"FAIL: Component 3 — Working tree not clean")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
