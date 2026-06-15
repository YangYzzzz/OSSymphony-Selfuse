"""
Reward Script: Handle stash, apply to different branch, resolve conflicts, clean up
Task ID: vscode_git_068
Domain: vs_code (git operations)
Scoring:
  Component 1: Current branch is 'develop'                       (0.2 pts)
  Component 2: Working tree is clean (working files match HEAD)  (0.2 pts)
  Component 3: No stash entries + 'Apply stash' commit on develop (0.2 pts)
  Component 4: routes.py has /api/search with @cache_response
               decorator AND /api/stats endpoint (committed)      (0.2 pts)
  Component 5: middleware.py has cache_response and cors_allow
               functions + MiddlewareStack (committed on develop)  (0.2 pts)
Total: 1.0
"""

import os
import zlib

PROJECT_DIR = '/home/user/project'
GIT_DIR = os.path.join(PROJECT_DIR, '.git')
TASK_ID = 'vscode_git_068'


def read_git_file(relative_path):
    """Read a text file from the .git directory. Returns content or None on error."""
    try:
        with open(os.path.join(GIT_DIR, relative_path), 'r') as f:
            return f.read().strip()
    except Exception:
        return None


def read_object(sha):
    """Read a git object by SHA using zlib decompression."""
    try:
        obj_path = os.path.join(GIT_DIR, 'objects', sha[:2], sha[2:])
        with open(obj_path, 'rb') as f:
            raw = f.read()
        data = zlib.decompress(raw)
        null_idx = data.index(b'\x00')
        header = data[:null_idx].decode('utf-8', errors='replace')
        content = data[null_idx + 1:]
        obj_type = header.split(' ')[0]
        return obj_type, content
    except Exception:
        return None, None


def resolve_ref(ref_name):
    """Resolve a git ref to a SHA, checking packed-refs and loose ref files."""
    # Try packed-refs first
    packed_refs_path = os.path.join(GIT_DIR, 'packed-refs')
    try:
        with open(packed_refs_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.endswith(ref_name) and not line.startswith('#') and not line.startswith('^'):
                    parts = line.split()
                    if len(parts) >= 1:
                        return parts[0]
    except Exception:
        pass
    # Try loose ref file
    ref_file = os.path.join(GIT_DIR, ref_name)
    if os.path.exists(ref_file):
        try:
            with open(ref_file, 'r') as f:
                return f.read().strip()
        except Exception:
            pass
    return None


def get_current_branch():
    """Get the current git branch name."""
    head_content = read_git_file('HEAD')
    if head_content and head_content.startswith('ref: refs/heads/'):
        return head_content[len('ref: refs/heads/'):]
    return None


def get_head_sha():
    """Resolve HEAD to a commit SHA."""
    head_content = read_git_file('HEAD')
    if head_content and head_content.startswith('ref: '):
        ref_path = head_content[5:]  # e.g., refs/heads/develop
        sha = read_git_file(ref_path)
        if not sha:
            sha = resolve_ref(ref_path)
        return sha
    # Detached HEAD
    return head_content


def get_tree_files(commit_sha):
    """
    Get a dict of {filename: blob_sha} from a commit's tree.
    Only returns top-level files (not recursive into subdirectories).
    """
    obj_type, content = read_object(commit_sha)
    if obj_type != 'commit':
        return {}

    tree_sha = None
    for line in content.decode('utf-8', errors='replace').split('\n'):
        if line.startswith('tree '):
            tree_sha = line.split(' ', 1)[1].strip()
            break

    if not tree_sha:
        return {}

    obj_type, tree_content = read_object(tree_sha)
    if obj_type != 'tree':
        return {}

    files = {}
    pos = 0
    while pos < len(tree_content):
        null_idx = tree_content.index(b'\x00', pos)
        entry_header = tree_content[pos:null_idx].decode('utf-8', errors='replace')
        sha1_bin = tree_content[null_idx + 1:null_idx + 21]
        sha1_hex = sha1_bin.hex()
        pos = null_idx + 21
        parts = entry_header.split(' ', 1)
        if len(parts) == 2:
            files[parts[1]] = sha1_hex
    return files


def get_committed_file_content(branch, filename):
    """Read the content of a file from a branch's latest commit."""
    branch_sha = resolve_ref(f'refs/heads/{branch}')
    if not branch_sha:
        return None
    tree_files = get_tree_files(branch_sha)
    blob_sha = tree_files.get(filename)
    if not blob_sha:
        return None
    obj_type, blob_content = read_object(blob_sha)
    if obj_type != 'blob':
        return None
    return blob_content.decode('utf-8', errors='replace')


def check_working_tree_clean():
    """
    Check if the working tree matches HEAD (no staged or unstaged changes).
    Compares actual file content against the committed blob content in HEAD.
    Returns (is_clean, list_of_modified_files)
    """
    head_sha = get_head_sha()
    if not head_sha:
        return False, ["Cannot resolve HEAD"]

    tree_files = get_tree_files(head_sha)
    if not tree_files:
        return False, ["Cannot read HEAD tree"]

    modified = []
    for filename, blob_sha in tree_files.items():
        obj_type, committed_content = read_object(blob_sha)
        if obj_type != 'blob':
            continue
        file_path = os.path.join(PROJECT_DIR, filename)
        if not os.path.exists(file_path):
            modified.append(f"{filename} (deleted)")
            continue
        with open(file_path, 'rb') as f:
            actual_content = f.read()
        if actual_content != committed_content:
            modified.append(filename)

    return len(modified) == 0, modified


def get_stash_list():
    """Check if there are stash entries."""
    stash_ref = resolve_ref('refs/stash')
    if stash_ref:
        return True, stash_ref
    # Also check stash log
    stash_log_path = os.path.join(GIT_DIR, 'logs', 'refs', 'stash')
    if os.path.exists(stash_log_path):
        try:
            with open(stash_log_path, 'r') as f:
                content = f.read().strip()
            if content:
                return True, "stash log has entries"
        except Exception:
            pass
    return False, ""


def get_recent_commit_messages(n=5):
    """Get recent commit messages walking from HEAD."""
    messages = []
    current_sha = get_head_sha()

    for _ in range(n):
        if not current_sha:
            break
        obj_type, content = read_object(current_sha)
        if obj_type != 'commit':
            break
        text = content.decode('utf-8', errors='replace')
        lines = text.split('\n')
        parent_sha = None
        message_lines = []
        in_message = False
        for line in lines:
            if line.startswith('parent '):
                parent_sha = line.split(' ', 1)[1].strip()
            elif line == '' and not in_message:
                in_message = True
            elif in_message:
                message_lines.append(line)
        messages.append('\n'.join(message_lines).strip())
        current_sha = parent_sha

    return messages


def verify_task():
    """
    Verify task completion with progressive scoring.

    The task requires:
    1. Stash changes from feature/api branch
    2. Switch to develop branch
    3. Apply the stash (routes.py clean, middleware.py needed conflict resolution)
    4. Drop the stash after successful application

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory must exist
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory {PROJECT_DIR} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be a git repo
    if not os.path.isdir(GIT_DIR):
        print(f"CRITICAL: {PROJECT_DIR} is not a git repository")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Current branch is 'develop' (0.2 points)
    # Initial state: on 'feature/api' branch
    # Golden state: on 'develop' branch
    try:
        current_branch = get_current_branch()
        if current_branch == 'develop':
            print(f"PASS: Component 1 — Current branch is 'develop' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected branch 'develop', found '{current_branch}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Working tree is clean (0.2 points)
    # Check by comparing working file content against HEAD-committed blob content.
    # Initial state: middleware.py and routes.py differ from HEAD (staged modifications)
    # Golden state: all files match HEAD (stash applied and committed, no pending changes)
    try:
        is_clean, modified_files = check_working_tree_clean()
        if is_clean:
            print(f"PASS: Component 2 — Working tree is clean, all files match HEAD commit (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Files differ from HEAD: {modified_files}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No stash entries + 'Apply stash' commit in history (0.2 points)
    # Initial state: no stash AND no 'Apply stash' commit on feature/api log
    # Golden state: no stash AND 'Apply stash' commit exists in develop log
    try:
        has_stash, stash_info = get_stash_list()
        if has_stash:
            print(f"FAIL: Component 3 — Stash is not empty: {stash_info}")
        else:
            recent_messages = get_recent_commit_messages(5)
            apply_stash_found = any(
                'Apply stash' in msg or 'apply stash' in msg.lower()
                for msg in recent_messages
            )
            if apply_stash_found:
                print(f"PASS: Component 3 — No stash entries and 'Apply stash' commit found (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — No stash but no 'Apply stash' commit in history. Recent: {recent_messages[:2]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: routes.py committed on develop has /api/search with @cache_response
    #              AND /api/stats endpoint (0.2 points)
    # Initial state: develop branch HEAD routes.py lacks /api/search, /api/stats,
    #                and cache_response (the initial feature/api staged changes haven't
    #                been applied to develop yet)
    # Golden state: develop HEAD routes.py has both endpoints with cache_response
    try:
        committed_routes = get_committed_file_content('develop', 'routes.py')
        if committed_routes:
            has_search = "'/api/search'" in committed_routes or '"/api/search"' in committed_routes
            has_stats = "'/api/stats'" in committed_routes or '"/api/stats"' in committed_routes
            has_cache_decorator = '@cache_response' in committed_routes
            has_cache_import = 'cache_response' in committed_routes

            if has_search and has_stats and has_cache_decorator and has_cache_import:
                print(f"PASS: Component 4 — develop HEAD routes.py has /api/search with @cache_response AND /api/stats (0.2 pts)")
                total_score += 0.2
            else:
                missing = []
                if not has_search:
                    missing.append('/api/search route')
                if not has_stats:
                    missing.append('/api/stats route')
                if not has_cache_decorator:
                    missing.append('@cache_response decorator')
                if not has_cache_import:
                    missing.append('cache_response import')
                print(f"FAIL: Component 4 — develop HEAD routes.py missing: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 4 — Could not read routes.py from develop HEAD")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: middleware.py committed on develop has cache_response, cors_allow,
    #              AND MiddlewareStack (adapted for develop branch) (0.2 points)
    # Initial state: develop HEAD middleware.py lacks cache_response and cors_allow
    # Golden state: develop HEAD middleware.py has all three (middleware adapted from stash)
    try:
        committed_mw = get_committed_file_content('develop', 'middleware.py')
        if committed_mw:
            has_cache_fn = 'def cache_response' in committed_mw
            has_cors_fn = 'def cors_allow' in committed_mw
            has_stack = 'class MiddlewareStack' in committed_mw or 'MiddlewareStack' in committed_mw

            if has_cache_fn and has_cors_fn and has_stack:
                print(f"PASS: Component 5 — develop HEAD middleware.py has cache_response + cors_allow + MiddlewareStack (0.2 pts)")
                total_score += 0.2
            else:
                missing = []
                if not has_cache_fn:
                    missing.append('def cache_response')
                if not has_cors_fn:
                    missing.append('def cors_allow')
                if not has_stack:
                    missing.append('MiddlewareStack')
                print(f"FAIL: Component 5 — develop HEAD middleware.py missing: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 5 — Could not read middleware.py from develop HEAD")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
