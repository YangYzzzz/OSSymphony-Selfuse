"""
Reward Script: Merge 'feature/refactor' into main with conflict resolution
Task ID: vscode_git_064
Domain: vs_code
Scoring:
  Component 1 (0.25): Merge commit exists on main (two-parent commit) - checked via .git/COMMIT_EDITMSG and parent count
  Component 2 (0.25): models.py resolved — no conflict markers, UserComment repr refactored, ProductManager class present
  Component 3 (0.25): views.py resolved — no conflict markers, index() has page param + paginate + featured_posts
  Component 4 (0.25): urls.py resolved — no conflict markers, all URL patterns present
Total: 1.0
"""

import os
import re

PROJECT_DIR = '/home/user/project'
GIT_DIR = os.path.join(PROJECT_DIR, '.git')
TASK_ID = 'vscode_git_064'


def read_git_file(relative_path):
    """Read a file within the .git directory. Returns content or None on failure."""
    full_path = os.path.join(GIT_DIR, relative_path)
    try:
        with open(full_path, 'r') as f:
            return f.read().strip()
    except Exception:
        return None


def resolve_ref(ref_name):
    """Resolve a git ref to its commit SHA by walking ref files and packed-refs."""
    # Direct ref file
    ref_path = os.path.join(GIT_DIR, ref_name)
    if os.path.exists(ref_path):
        with open(ref_path, 'r') as f:
            content = f.read().strip()
        if content.startswith('ref:'):
            # Symbolic ref — follow it
            return resolve_ref(content[len('ref: '):].strip())
        return content

    # Check packed-refs
    packed_refs_path = os.path.join(GIT_DIR, 'packed-refs')
    if os.path.exists(packed_refs_path):
        with open(packed_refs_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) == 2 and parts[1] == ref_name:
                    return parts[0]
    return None


def get_commit_parents(sha):
    """
    Return list of parent SHAs for a given commit SHA by reading object file.
    Git objects are stored as zlib-compressed data in .git/objects/<sha[:2]>/<sha[2:]>.
    """
    import zlib
    obj_path = os.path.join(GIT_DIR, 'objects', sha[:2], sha[2:])
    if not os.path.exists(obj_path):
        return None  # Could be in a pack file

    with open(obj_path, 'rb') as f:
        raw = f.read()

    try:
        decompressed = zlib.decompress(raw)
    except Exception:
        return None

    # Format: "<type> <size>\x00<content>"
    null_pos = decompressed.index(b'\x00')
    header = decompressed[:null_pos].decode('ascii', errors='replace')
    obj_type = header.split(' ')[0]

    if obj_type != 'commit':
        return None

    commit_content = decompressed[null_pos + 1:].decode('utf-8', errors='replace')
    parents = []
    for line in commit_content.split('\n'):
        if line.startswith('parent '):
            parents.append(line[len('parent '):].strip())
        elif line == '' and parents is not None:
            # End of header section
            break
    return parents


def get_head_sha():
    """Get the SHA that HEAD currently points to."""
    head_content = read_git_file('HEAD')
    if head_content is None:
        return None
    if head_content.startswith('ref:'):
        ref = head_content[len('ref: '):].strip()
        return resolve_ref(ref)
    # Detached HEAD
    return head_content


def verify_task():
    """
    Verify task completion: merging 'feature/refactor' into main
    with conflict resolution across models.py, views.py, and urls.py.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: it is a git repo
    if not os.path.isdir(GIT_DIR):
        print(f"CRITICAL: {PROJECT_DIR} is not a git repository")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: A merge commit exists on main (HEAD has two parents)
    # This fails on initial_env (merge in progress, no commit yet)
    # and passes on golden_env (merge commit created)
    # -----------------------------------------------------------------------
    try:
        head_sha = get_head_sha()
        if head_sha is None:
            print(f"FAIL: Component 1 — Could not resolve HEAD SHA")
        else:
            parents = get_commit_parents(head_sha)
            if parents is None:
                # Fallback: check COMMIT_EDITMSG for merge message and MERGE_HEAD absence
                merge_head_path = os.path.join(GIT_DIR, 'MERGE_HEAD')
                commit_msg = read_git_file('COMMIT_EDITMSG') or ''
                if not os.path.exists(merge_head_path) and 'Merge branch' in commit_msg:
                    print(f"PASS: Component 1 — Merge commit detected via COMMIT_EDITMSG (pack file, cannot verify parent count)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 1 — Could not read commit object (may be packed). MERGE_HEAD exists: {os.path.exists(merge_head_path)}")
            elif len(parents) == 2:
                print(f"PASS: Component 1 — Merge commit found on HEAD with two parents")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — HEAD has {len(parents)} parent(s), expected 2 for a merge commit")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: models.py resolved correctly
    #   - No conflict markers present
    #   - UserComment __repr__ uses 'UserComment(text=...')  (feature refactor kept)
    #   - ProductManager class present (main's new model kept)
    # -----------------------------------------------------------------------
    try:
        models_path = os.path.join(PROJECT_DIR, 'models.py')
        with open(models_path, 'r') as f:
            models_content = f.read()

        has_conflict_markers = bool(re.search(r'^(<{7}|={7}|>{7})', models_content, re.MULTILINE))
        has_user_comment_repr = 'UserComment(text=' in models_content
        has_product_manager = 'class ProductManager' in models_content

        if has_conflict_markers:
            print(f"FAIL: Component 2 — models.py still contains conflict markers")
        elif not has_user_comment_repr:
            print(f"FAIL: Component 2 — models.py missing refactored UserComment repr (UserComment(text=...))")
        elif not has_product_manager:
            print(f"FAIL: Component 2 — models.py missing ProductManager class (main's new model)")
        else:
            print(f"PASS: Component 2 — models.py resolved: no conflict markers, UserComment refactored repr, ProductManager class present")
            total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: views.py resolved correctly
    #   - No conflict markers present
    #   - index() has 'page=1' parameter (from feature/refactor)
    #   - index() uses 'paginate' (from feature/refactor)
    #   - index() includes 'featured_posts' (from main)
    # -----------------------------------------------------------------------
    try:
        views_path = os.path.join(PROJECT_DIR, 'views.py')
        with open(views_path, 'r') as f:
            views_content = f.read()

        has_conflict_markers = bool(re.search(r'^(<{7}|={7}|>{7})', views_content, re.MULTILINE))
        has_page_param = bool(re.search(r'def index\s*\(.*page\s*=\s*1', views_content))
        has_paginate = 'paginate' in views_content
        has_featured_posts = 'featured_posts' in views_content

        if has_conflict_markers:
            print(f"FAIL: Component 3 — views.py still contains conflict markers")
        elif not has_page_param:
            print(f"FAIL: Component 3 — views.py: index() missing 'page=1' parameter (feature's pagination)")
        elif not has_paginate:
            print(f"FAIL: Component 3 — views.py: index() missing 'paginate' call (feature's pagination)")
        elif not has_featured_posts:
            print(f"FAIL: Component 3 — views.py: index() missing 'featured_posts' variable (main's featured posts)")
        else:
            print(f"PASS: Component 3 — views.py resolved: no conflict markers, page=1 param, paginate call, featured_posts all present")
            total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: urls.py resolved correctly
    #   - No conflict markers present
    #   - All URL patterns present from both branches:
    #     index, about (feature), index-paged (feature), post-detail,
    #     product-list (main), product-detail (main), user-profile
    # -----------------------------------------------------------------------
    try:
        urls_path = os.path.join(PROJECT_DIR, 'urls.py')
        with open(urls_path, 'r') as f:
            urls_content = f.read()

        has_conflict_markers = bool(re.search(r'^(<{7}|={7}|>{7})', urls_content, re.MULTILINE))

        # All required URL pattern names from both branches
        required_names = [
            'name="index"',
            'name="about"',
            'name="index-paged"',
            'name="post-detail"',
            'name="product-list"',
            'name="product-detail"',
            'name="user-profile"',
        ]
        missing_names = [n for n in required_names if n not in urls_content]

        if has_conflict_markers:
            print(f"FAIL: Component 4 — urls.py still contains conflict markers")
        elif missing_names:
            print(f"FAIL: Component 4 — urls.py missing URL patterns: {missing_names}")
        else:
            print(f"PASS: Component 4 — urls.py resolved: no conflict markers, all 7 URL patterns present")
            total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
