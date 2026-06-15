"""
Reward Script: Undo last commit (soft reset), modify commit message, add api_docs.md, recommit.
Task ID: vscode_git_049
Domain: vs_code (git operations)
Scoring:
  Component 1: Latest commit message is "Update API and documentation" (0.4 pts)
  Component 2: Latest commit tree includes both api.py and api_docs.md (0.4 pts)
  Component 3: Working tree is clean — api_docs.md is tracked (no untracked py/md files) (0.2 pts)
  Total: 1.0

Verification strategy: Reads git object files directly using zlib decompression.
No subprocess usage — pure Python file I/O with the standard library.
"""

import os
import zlib

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_049'
PROJECT_DIR = '/home/user/project'
GIT_DIR = '/home/user/project/.git'

EXPECTED_COMMIT_MSG = 'Update API and documentation'
EXPECTED_FILES_IN_COMMIT = {'api.py', 'api_docs.md'}


def read_git_object(git_dir, sha):
    """Read and decompress a git loose object by its SHA. Returns (type_str, content_bytes)."""
    path = os.path.join(git_dir, 'objects', sha[:2], sha[2:])
    with open(path, 'rb') as f:
        raw = f.read()
    data = zlib.decompress(raw)
    header_end = data.index(b'\x00')
    header = data[:header_end].decode()
    content = data[header_end + 1:]
    obj_type = header.split()[0]
    return obj_type, content


def parse_tree_names(tree_content):
    """Extract file names from a git tree object binary content."""
    names = []
    i = 0
    while i < len(tree_content):
        null_idx = tree_content.index(b'\x00', i)
        mode_name = tree_content[i:null_idx].decode()
        # Skip 20-byte SHA bytes after null
        i = null_idx + 1 + 20
        # mode_name is "<mode> <name>"
        parts = mode_name.split(' ', 1)
        if len(parts) == 2:
            names.append(parts[1])
    return names


def get_head_sha(git_dir):
    """Resolve HEAD to a concrete SHA (supports both direct SHA and symref)."""
    head_path = os.path.join(git_dir, 'HEAD')
    with open(head_path) as f:
        head_content = f.read().strip()
    if head_content.startswith('ref: '):
        ref_path = head_content[5:]  # e.g. refs/heads/master
        ref_file = os.path.join(git_dir, ref_path)
        with open(ref_file) as f:
            return f.read().strip()
    else:
        # Detached HEAD — content is the SHA directly
        return head_content


def verify_task(project_dir, git_dir):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: project directory and .git dir must exist
    if not os.path.isdir(project_dir):
        print(f"CRITICAL: Project directory not found: {project_dir}")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.isdir(git_dir):
        print(f"CRITICAL: Not a git repository (missing .git): {project_dir}")
        print("REWARD: 0.0")
        return 0.0

    # --- Resolve HEAD commit SHA ---
    try:
        head_sha = get_head_sha(git_dir)
    except Exception as e:
        print(f"CRITICAL: Cannot resolve HEAD: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --- Read HEAD commit object ---
    try:
        obj_type, commit_content = read_git_object(git_dir, head_sha)
        if obj_type != 'commit':
            print(f"CRITICAL: HEAD object is not a commit (type={obj_type})")
            print("REWARD: 0.0")
            return 0.0
        commit_text = commit_content.decode('utf-8', errors='replace')
    except Exception as e:
        print(f"CRITICAL: Cannot read HEAD commit object ({head_sha}): {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract commit message (after the blank line separator)
    try:
        msg_separator = '\n\n'
        sep_pos = commit_text.index(msg_separator)
        commit_msg = commit_text[sep_pos + 2:].strip()
    except ValueError:
        commit_msg = ''

    # Extract tree SHA from commit
    try:
        tree_sha = None
        for line in commit_text.split('\n'):
            if line.startswith('tree '):
                tree_sha = line.split()[1]
                break
    except Exception as e:
        tree_sha = None

    # --- Component 1: Commit message is "Update API and documentation" (0.4 pts) ---
    # FAILS on initial ("Update API") — PASSES on golden ("Update API and documentation")
    try:
        if commit_msg == EXPECTED_COMMIT_MSG:
            print(f"PASS: Component 1 — commit message is '{commit_msg}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected '{EXPECTED_COMMIT_MSG}', found '{commit_msg}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: HEAD commit tree includes both api.py and api_docs.md (0.4 pts) ---
    # FAILS on initial (only api.py in latest commit) — PASSES on golden
    try:
        if tree_sha is None:
            print("FAIL: Component 2 — could not parse tree SHA from commit")
        else:
            obj_type, tree_content = read_git_object(git_dir, tree_sha)
            committed_files = set(parse_tree_names(tree_content))
            if EXPECTED_FILES_IN_COMMIT.issubset(committed_files):
                print(f"PASS: Component 2 — HEAD commit contains {sorted(EXPECTED_FILES_IN_COMMIT)} (0.4 pts)")
                print(f"      Full commit tree: {sorted(committed_files)}")
                total_score += 0.4
            else:
                missing = EXPECTED_FILES_IN_COMMIT - committed_files
                print(f"FAIL: Component 2 — HEAD commit missing files: {missing}")
                print(f"      Files found in HEAD commit: {sorted(committed_files)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: Working tree is clean — api_docs.md is tracked, no untracked project files (0.2 pts) ---
    # FAILS on initial (api_docs.md exists in working dir but is untracked/not in HEAD commit tree)
    # PASSES on golden (api_docs.md is committed, working dir matches HEAD tree)
    try:
        # Get files in project working directory (excluding .git)
        working_files = set(
            f for f in os.listdir(project_dir)
            if not f.startswith('.') and os.path.isfile(os.path.join(project_dir, f))
        )

        # Get files in HEAD commit tree
        if tree_sha is not None:
            obj_type, tree_content = read_git_object(git_dir, tree_sha)
            committed_files_set = set(parse_tree_names(tree_content))
        else:
            committed_files_set = set()

        # Untracked = files in working dir that are NOT in the committed tree
        untracked = working_files - committed_files_set
        if not untracked:
            print(f"PASS: Component 3 — all working tree files are tracked in HEAD commit (0.2 pts)")
            print(f"      Working files: {sorted(working_files)}")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — untracked files present: {sorted(untracked)}")
            print(f"      Working files: {sorted(working_files)}")
            print(f"      Tracked in HEAD: {sorted(committed_files_set)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task(PROJECT_DIR, GIT_DIR)
