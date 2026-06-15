"""
Reward Script: Create git branch 'feature-login', switch to it, add comment to app.py line 1, commit
Task ID: vscode_stu_055
Domain: vscode (git operations)
Scoring:
  Component 1 (0.25): Branch 'feature-login' exists
  Component 2 (0.25): Currently on 'feature-login' branch
  Component 3 (0.25): app.py first line is a comment
  Component 4 (0.25): The comment in app.py is committed on feature-login
"""

import os
import configparser

WORKDIR = '/home/user/workspace'
TASK_ID = 'vscode_stu_055'


def read_git_head(git_dir):
    """Read the current HEAD reference to determine active branch."""
    head_path = os.path.join(git_dir, 'HEAD')
    try:
        with open(head_path, 'r') as f:
            content = f.read().strip()
        if content.startswith('ref: refs/heads/'):
            return content[len('ref: refs/heads/'):]
        return None  # detached HEAD
    except Exception:
        return None


def list_branches(git_dir):
    """List all local branch names by scanning refs/heads/."""
    heads_dir = os.path.join(git_dir, 'refs', 'heads')
    branches = []
    try:
        for root, dirs, files in os.walk(heads_dir):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, heads_dir)
                branches.append(rel)
    except Exception:
        pass
    # Also check packed-refs for branches not yet unpacked
    packed_refs = os.path.join(git_dir, 'packed-refs')
    if os.path.exists(packed_refs):
        try:
            with open(packed_refs, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    parts = line.split()
                    if len(parts) >= 2:
                        ref = parts[1]
                        if ref.startswith('refs/heads/'):
                            branch = ref[len('refs/heads/'):]
                            if branch not in branches:
                                branches.append(branch)
        except Exception:
            pass
    return branches


def get_commit_tree_blob(git_dir, commit_hash):
    """
    Read a commit object to get its tree hash, then read the tree to find
    the blob hash for app.py. Returns the blob content as bytes, or None.
    This uses pure Python to read loose git objects.
    """
    import zlib
    import struct

    def read_object(git_dir, sha):
        """Read a git object (loose or packed). Returns (type, data)."""
        # Try loose object first
        obj_path = os.path.join(git_dir, 'objects', sha[:2], sha[2:])
        if os.path.exists(obj_path):
            with open(obj_path, 'rb') as f:
                raw = zlib.decompress(f.read())
            # Format: "<type> <size>\0<data>"
            null_idx = raw.index(b'\x00')
            header = raw[:null_idx].decode('ascii')
            obj_type = header.split(' ')[0]
            data = raw[null_idx + 1:]
            return obj_type, data
        return None, None

    def parse_tree(data):
        """Parse a tree object, yielding (mode, name, sha_hex) tuples."""
        i = 0
        while i < len(data):
            # Format: "<mode> <name>\0<20-byte sha>"
            space_idx = data.index(b' ', i)
            mode = data[i:space_idx].decode('ascii')
            null_idx = data.index(b'\x00', space_idx)
            name = data[space_idx + 1:null_idx].decode('utf-8')
            sha_bytes = data[null_idx + 1:null_idx + 21]
            sha_hex = sha_bytes.hex()
            yield mode, name, sha_hex
            i = null_idx + 21

    try:
        # Read commit to get tree hash
        obj_type, commit_data = read_object(git_dir, commit_hash)
        if obj_type != 'commit':
            return None
        # Parse tree line from commit
        tree_hash = None
        for line in commit_data.decode('utf-8', errors='replace').split('\n'):
            if line.startswith('tree '):
                tree_hash = line.split(' ')[1].strip()
                break
        if not tree_hash:
            return None
        # Read tree to find app.py blob
        obj_type, tree_data = read_object(git_dir, tree_hash)
        if obj_type != 'tree':
            return None
        for mode, name, sha_hex in parse_tree(tree_data):
            if name == 'app.py':
                # Read blob
                obj_type, blob_data = read_object(git_dir, sha_hex)
                if obj_type == 'blob':
                    return blob_data.decode('utf-8', errors='replace')
        return None
    except Exception:
        return None


def get_branch_head_commit(git_dir, branch_name):
    """Get the commit hash that a branch points to."""
    ref_path = os.path.join(git_dir, 'refs', 'heads', branch_name)
    if os.path.exists(ref_path):
        with open(ref_path, 'r') as f:
            return f.read().strip()
    # Check packed-refs
    packed_refs = os.path.join(git_dir, 'packed-refs')
    if os.path.exists(packed_refs):
        with open(packed_refs, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                parts = line.split()
                if len(parts) >= 2 and parts[1] == f'refs/heads/{branch_name}':
                    return parts[0]
    return None


def verify_task(repo_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    git_dir = os.path.join(repo_path, '.git')

    if not os.path.isdir(git_dir):
        print(f"CRITICAL: Not a git repository: {repo_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Branch 'feature-login' exists (0.25 points)
    try:
        branches = list_branches(git_dir)
        if 'feature-login' in branches:
            print(f"PASS: Component 1 — 'feature-login' branch exists (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — 'feature-login' branch not found. Branches: {branches}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Currently checked out on 'feature-login' (0.25 points)
    try:
        current_branch = read_git_head(git_dir)
        if current_branch == 'feature-login':
            print(f"PASS: Component 2 — Currently on 'feature-login' branch (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected branch 'feature-login', found: '{current_branch}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: app.py first line is a comment (0.25 points)
    # This checks the working tree file
    try:
        app_path = os.path.join(repo_path, 'app.py')
        if not os.path.exists(app_path):
            print(f"FAIL: Component 3 — app.py not found")
        else:
            with open(app_path, 'r') as f:
                first_line = f.readline().strip()
            if first_line.startswith('#'):
                print(f"PASS: Component 3 — app.py line 1 is a comment: '{first_line}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — app.py line 1 is not a comment: '{first_line}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: The comment is committed on feature-login branch (0.25 points)
    # Read the committed version of app.py from feature-login's HEAD
    try:
        fl_commit = get_branch_head_commit(git_dir, 'feature-login')
        if not fl_commit:
            print(f"FAIL: Component 4 — Cannot resolve feature-login HEAD commit")
        else:
            # Also get main's HEAD to ensure the commit differs
            main_commit = get_branch_head_commit(git_dir, 'main')
            if fl_commit == main_commit:
                print(f"FAIL: Component 4 — feature-login points to same commit as main (no new commit)")
            else:
                committed_content = get_commit_tree_blob(git_dir, fl_commit)
                if committed_content is None:
                    print(f"FAIL: Component 4 — Cannot read app.py from feature-login commit {fl_commit[:8]}")
                else:
                    committed_first_line = committed_content.split('\n')[0].strip()
                    if committed_first_line.startswith('#'):
                        print(f"PASS: Component 4 — Committed app.py on feature-login has comment at line 1: '{committed_first_line}' (0.25 pts)")
                        total_score += 0.25
                    else:
                        print(f"FAIL: Component 4 — Committed app.py first line is not a comment: '{committed_first_line}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
repo_path = WORKDIR
if not os.path.isdir(repo_path):
    print(f"Repository not found: {repo_path}")
    print("REWARD: 0.0")
else:
    verify_task(repo_path)
