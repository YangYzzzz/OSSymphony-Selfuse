"""
Reward Script: Branch-based code review workflow in VSCode
Task ID: vscode_wf_045
Domain: vscode
Scoring:
  - Component 1: Branch 'feature/add-auth' exists (0.2 pts)
  - Component 2: Branch 'feature/add-auth' is checked out (0.1 pts)
  - Component 3: auth.js exists with authentication middleware code (0.3 pts)
  - Component 4: Commit on feature/add-auth is ahead of main with auth.js (0.25 pts)
  - Component 5: auth.js is tracked in feature/add-auth but not in main (0.15 pts)
"""

import os
import re
import zlib
import struct

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
GIT_DIR = os.path.join(PROJECT_DIR, '.git')
TASK_ID = 'vscode_wf_045'


def resolve_ref(ref_path):
    """Resolve a git ref to a commit hash by reading .git files directly."""
    full_path = os.path.join(GIT_DIR, ref_path)
    if os.path.isfile(full_path):
        return open(full_path, 'r').read().strip()
    # Check packed-refs
    packed_refs_path = os.path.join(GIT_DIR, 'packed-refs')
    if os.path.isfile(packed_refs_path):
        with open(packed_refs_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                parts = line.split()
                if len(parts) == 2 and parts[1] == ref_path:
                    return parts[0]
    return None


def read_git_object(sha):
    """Read and decompress a git object, return (type, content_bytes)."""
    obj_path = os.path.join(GIT_DIR, 'objects', sha[:2], sha[2:])
    if not os.path.isfile(obj_path):
        return None, None
    with open(obj_path, 'rb') as f:
        raw = zlib.decompress(f.read())
    # Format: "<type> <size>\0<content>"
    null_idx = raw.index(b'\x00')
    header = raw[:null_idx].decode('ascii')
    obj_type = header.split(' ')[0]
    content = raw[null_idx + 1:]
    return obj_type, content


def parse_tree(tree_content):
    """Parse a git tree object into list of (mode, name, sha)."""
    entries = []
    i = 0
    while i < len(tree_content):
        # Format: "<mode> <name>\0<20-byte SHA>"
        space_idx = tree_content.index(b' ', i)
        null_idx = tree_content.index(b'\x00', space_idx)
        mode = tree_content[i:space_idx].decode('ascii')
        name = tree_content[space_idx + 1:null_idx].decode('ascii')
        sha_bytes = tree_content[null_idx + 1:null_idx + 21]
        sha = sha_bytes.hex()
        entries.append((mode, name, sha))
        i = null_idx + 21
    return entries


def get_commit_tree(commit_sha):
    """Get the tree SHA from a commit object."""
    obj_type, content = read_git_object(commit_sha)
    if obj_type != 'commit':
        return None
    # First line: "tree <sha>"
    first_line = content.split(b'\n')[0].decode('ascii')
    if first_line.startswith('tree '):
        return first_line[5:]
    return None


def get_commit_parent(commit_sha):
    """Get the parent SHA(s) from a commit object."""
    obj_type, content = read_git_object(commit_sha)
    if obj_type != 'commit':
        return []
    parents = []
    for line in content.split(b'\n'):
        decoded = line.decode('ascii', errors='replace')
        if decoded.startswith('parent '):
            parents.append(decoded[7:].strip())
        elif decoded == '' or not decoded.startswith(('tree ', 'parent ', 'author ', 'committer ')):
            break
    return parents


def tree_has_file(tree_sha, path_parts):
    """Check if a file exists in a git tree, following nested directories."""
    if not path_parts:
        return False
    obj_type, content = read_git_object(tree_sha)
    if obj_type != 'tree':
        return False
    entries = parse_tree(content)
    target = path_parts[0]
    for mode, name, sha in entries:
        if name == target:
            if len(path_parts) == 1:
                # Found the file
                return True
            else:
                # Need to go deeper into subdirectory
                return tree_has_file(sha, path_parts[1:])
    return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory {PROJECT_DIR} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: it's a git repo
    if not os.path.isdir(GIT_DIR):
        print(f"CRITICAL: {PROJECT_DIR} is not a git repository")
        print("REWARD: 0.0")
        return 0.0

    # Resolve branch refs
    feature_sha = resolve_ref('refs/heads/feature/add-auth')
    main_sha = resolve_ref('refs/heads/main')

    # Component 1: Branch 'feature/add-auth' exists (0.2 points)
    try:
        if feature_sha:
            print(f"PASS: Component 1 -- Branch 'feature/add-auth' exists (sha: {feature_sha[:8]}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Branch 'feature/add-auth' not found in refs")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Branch 'feature/add-auth' is checked out (0.1 points)
    try:
        head_path = os.path.join(GIT_DIR, 'HEAD')
        head_content = open(head_path, 'r').read().strip()
        if head_content == 'ref: refs/heads/feature/add-auth':
            print(f"PASS: Component 2 -- Branch 'feature/add-auth' is checked out (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 -- HEAD points to '{head_content}', expected 'ref: refs/heads/feature/add-auth'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: auth.js exists with authentication middleware code (0.3 points)
    auth_js_path = os.path.join(PROJECT_DIR, 'src', 'middleware', 'auth.js')
    try:
        if os.path.isfile(auth_js_path):
            with open(auth_js_path, 'r') as f:
                content = f.read()
            # Check for meaningful authentication middleware content
            has_auth_function = bool(re.search(r'function\s+\w*auth\w*|const\s+\w*auth\w*\s*=|module\.exports', content, re.IGNORECASE))
            has_middleware_pattern = bool(re.search(r'(req|request)\s*,\s*(res|response)\s*,\s*(next|callback)', content))
            has_auth_logic = bool(re.search(r'(token|jwt|authorization|authenticate|401|403|Bearer)', content, re.IGNORECASE))

            if has_auth_function and has_middleware_pattern and has_auth_logic:
                print(f"PASS: Component 3 -- auth.js exists with valid authentication middleware ({len(content)} bytes) (0.3 pts)")
                total_score += 0.3
            elif has_auth_logic:
                # Partial: has auth-related code but missing middleware pattern
                print(f"PARTIAL: Component 3 -- auth.js has auth logic but incomplete middleware pattern (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- auth.js exists but lacks authentication middleware code")
        else:
            print(f"FAIL: Component 3 -- auth.js does not exist at {auth_js_path}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Commit on feature/add-auth is ahead of main (0.25 points)
    # feature/add-auth must have commit(s) that main does not
    try:
        if feature_sha and main_sha and feature_sha != main_sha:
            # Check that main_sha is an ancestor of feature_sha
            # Walk parent chain from feature_sha
            current = feature_sha
            ancestor_check = 0  # 0 = not found, 1 = found
            commits_ahead = 0
            for _ in range(50):  # limit traversal
                parents = get_commit_parent(current)
                commits_ahead += 1
                if main_sha in parents:
                    ancestor_check = 1
                    break
                if not parents:
                    break
                current = parents[0]

            if ancestor_check == 1 and commits_ahead > 0:
                # Verify the commit tree includes auth.js
                feature_tree = get_commit_tree(feature_sha)
                main_tree = get_commit_tree(main_sha)
                auth_in_feature = tree_has_file(feature_tree, ['src', 'middleware', 'auth.js']) if feature_tree else False
                auth_in_main = tree_has_file(main_tree, ['src', 'middleware', 'auth.js']) if main_tree else False

                if auth_in_feature and not auth_in_main:
                    print(f"PASS: Component 4 -- feature/add-auth is {commits_ahead} commit(s) ahead of main, adding auth.js (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 4 -- auth.js in feature: {auth_in_feature}, in main: {auth_in_main}")
            else:
                print(f"FAIL: Component 4 -- feature/add-auth is not ahead of main (ancestor_check={ancestor_check}, ahead={commits_ahead})")
        elif feature_sha and not main_sha:
            print(f"FAIL: Component 4 -- main branch ref not found")
        elif not feature_sha:
            print(f"FAIL: Component 4 -- feature/add-auth branch does not exist")
        else:
            print(f"FAIL: Component 4 -- feature/add-auth and main point to same commit")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: auth.js is tracked in feature/add-auth tree but NOT in main tree (0.15 points)
    # This verifies the diff between branches includes auth.js
    try:
        if feature_sha and main_sha:
            feature_tree = get_commit_tree(feature_sha)
            main_tree = get_commit_tree(main_sha)
            auth_in_feature = tree_has_file(feature_tree, ['src', 'middleware', 'auth.js']) if feature_tree else False
            auth_in_main = tree_has_file(main_tree, ['src', 'middleware', 'auth.js']) if main_tree else False

            if auth_in_feature and not auth_in_main:
                print(f"PASS: Component 5 -- auth.js exists in feature/add-auth tree but not in main tree (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 -- auth.js in feature tree: {auth_in_feature}, in main tree: {auth_in_main}")
        else:
            print(f"FAIL: Component 5 -- Cannot compare branches (feature={feature_sha is not None}, main={main_sha is not None})")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
