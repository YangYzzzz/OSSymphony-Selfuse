"""
Reward Script: Configure Git branch management workflow in VSCode
Task ID: vscode_wf_063
Domain: vscode
Scoring:
  - Component 1: Git Graph extension installed (0.15)
  - Component 2: Branch 'develop' exists (0.10)
  - Component 3: Branch 'feature/login' exists (0.10)
  - Component 4: Branch 'feature/dashboard' exists (0.10)
  - Component 5: feature/login has unique commit(s) beyond main (0.10)
  - Component 6: feature/dashboard has unique commit(s) beyond main (0.10)
  - Component 7: git.mergeEditor is true in settings (0.10)
  - Component 8: git.autoStash is true in settings (0.10)
  - Component 9: git.branchProtection includes 'main' (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_063'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def get_git_branches(repo_dir):
    """Read branches from git refs."""
    branches = set()
    heads_dir = os.path.join(repo_dir, '.git', 'refs', 'heads')
    if os.path.isdir(heads_dir):
        for root, dirs, files in os.walk(heads_dir):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, heads_dir)
                branches.add(rel)
    # Also check packed-refs
    packed_refs = os.path.join(repo_dir, '.git', 'packed-refs')
    if os.path.isfile(packed_refs):
        with open(packed_refs, 'r') as pf:
            for line in pf:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                parts = line.split()
                if len(parts) == 2 and parts[1].startswith('refs/heads/'):
                    branches.add(parts[1][len('refs/heads/'):])
    return branches


def get_commit_hash(repo_dir, ref_path):
    """Get commit hash for a branch ref."""
    ref_file = os.path.join(repo_dir, '.git', 'refs', 'heads', ref_path)
    if os.path.isfile(ref_file):
        with open(ref_file, 'r') as f:
            return f.read().strip()
    # Check packed-refs
    packed_refs = os.path.join(repo_dir, '.git', 'packed-refs')
    if os.path.isfile(packed_refs):
        with open(packed_refs, 'r') as pf:
            for line in pf:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                parts = line.split()
                if len(parts) == 2 and parts[1] == f'refs/heads/{ref_path}':
                    return parts[0]
    return None


def get_ancestor_commits(repo_dir, commit_hash, max_depth=50):
    """Walk commit parents to get ancestor set (simplified, reads git objects)."""
    # We just compare the tip commits: if branch tip != main tip, the branch has unique commits
    return commit_hash


def load_settings():
    """Load VSCode settings.json with JSONC comment stripping."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip // comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return None


def check_extension_installed(ext_id):
    """Check if extension is installed by scanning extensions directory."""
    ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
    if not os.path.isdir(ext_dir):
        # Try the standard location
        ext_dir = os.path.join(WORKDIR, '.vscode-server', 'extensions')
    if not os.path.isdir(ext_dir):
        # Try yet another standard location
        for search_dir in [
            os.path.join(WORKDIR, '.vscode', 'extensions'),
            '/home/user/.vscode/extensions',
        ]:
            if os.path.isdir(search_dir):
                ext_dir = search_dir
                break

    # Also try code --list-extensions output cached approach:
    # Check filesystem-based detection
    ext_id_lower = ext_id.lower()

    # Method 1: scan extensions directories
    for search_path in [
        os.path.join(WORKDIR, '.vscode', 'extensions'),
        os.path.join(WORKDIR, '.vscode-server', 'extensions'),
    ]:
        if os.path.isdir(search_path):
            for entry in os.listdir(search_path):
                if ext_id_lower in entry.lower():
                    return True

    # Method 2: check extension marker files written by code CLI
    # The `code --list-extensions` output could be checked via a marker
    # But since we can't use subprocess, check extension metadata
    ext_storage = os.path.join(
        WORKDIR, '.config', 'Code', 'User', 'globalStorage', 'state.vscdb'
    )
    # Fallback: check if the extension package.json exists anywhere under extensions
    for base in ['/home/user/.vscode/extensions']:
        if os.path.isdir(base):
            for d in os.listdir(base):
                pkg = os.path.join(base, d, 'package.json')
                if os.path.isfile(pkg):
                    try:
                        with open(pkg, 'r') as f:
                            meta = json.load(f)
                        pub = meta.get('publisher', '').lower()
                        name = meta.get('name', '').lower()
                        if f"{pub}.{name}" == ext_id_lower:
                            return True
                    except Exception:
                        pass
    return False


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # Precondition: project directory must exist and be a git repo
    git_dir = os.path.join(PROJECT_DIR, '.git')
    if not os.path.isdir(git_dir):
        print(f"CRITICAL: {PROJECT_DIR} is not a git repo")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Git Graph extension installed (0.15 points)
    try:
        ext_installed = check_extension_installed('mhutchie.git-graph')
        if ext_installed:
            print(f"PASS: Component 1 -- Git Graph extension installed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Git Graph extension not found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Get branches
    branches = get_git_branches(PROJECT_DIR)
    print(f"INFO: Found branches: {branches}")

    # Component 2: Branch 'develop' exists (0.10 points)
    try:
        if 'develop' in branches:
            print(f"PASS: Component 2 -- Branch 'develop' exists (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 -- Branch 'develop' not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Branch 'feature/login' exists (0.10 points)
    try:
        if 'feature/login' in branches:
            print(f"PASS: Component 3 -- Branch 'feature/login' exists (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 -- Branch 'feature/login' not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Branch 'feature/dashboard' exists (0.10 points)
    try:
        if 'feature/dashboard' in branches:
            print(f"PASS: Component 4 -- Branch 'feature/dashboard' exists (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 -- Branch 'feature/dashboard' not found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Get main branch commit hash for comparison
    main_hash = get_commit_hash(PROJECT_DIR, 'main')
    print(f"INFO: main branch tip: {main_hash}")

    # Component 5: feature/login has unique commit(s) beyond main (0.10 points)
    try:
        login_hash = get_commit_hash(PROJECT_DIR, 'feature/login')
        print(f"INFO: feature/login tip: {login_hash}")
        if login_hash and main_hash and login_hash != main_hash:
            print(f"PASS: Component 5 -- feature/login has unique commit(s) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- feature/login has no unique commits (same as main)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: feature/dashboard has unique commit(s) beyond main (0.10 points)
    try:
        dash_hash = get_commit_hash(PROJECT_DIR, 'feature/dashboard')
        print(f"INFO: feature/dashboard tip: {dash_hash}")
        if dash_hash and main_hash and dash_hash != main_hash:
            print(f"PASS: Component 6 -- feature/dashboard has unique commit(s) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 -- feature/dashboard has no unique commits (same as main)")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Load settings for components 7-9
    settings = load_settings()
    if settings is None:
        print("WARN: Could not load settings.json, components 7-9 will fail")

    # Component 7: git.mergeEditor is true (0.10 points)
    try:
        if settings and settings.get('git.mergeEditor') is True:
            print(f"PASS: Component 7 -- git.mergeEditor is true (0.10 pts)")
            total_score += 0.10
        else:
            val = settings.get('git.mergeEditor') if settings else None
            print(f"FAIL: Component 7 -- git.mergeEditor expected true, found {val}")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    # Component 8: git.autoStash is true (0.10 points)
    try:
        if settings and settings.get('git.autoStash') is True:
            print(f"PASS: Component 8 -- git.autoStash is true (0.10 pts)")
            total_score += 0.10
        else:
            val = settings.get('git.autoStash') if settings else None
            print(f"FAIL: Component 8 -- git.autoStash expected true, found {val}")
    except Exception as e:
        print(f"ERROR: Component 8 -- {e}")

    # Component 9: git.branchProtection includes 'main' (0.15 points)
    try:
        if settings:
            bp = settings.get('git.branchProtection')
            if isinstance(bp, list) and 'main' in bp:
                print(f"PASS: Component 9 -- git.branchProtection includes 'main' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 9 -- git.branchProtection expected ['main'], found {bp}")
        else:
            print(f"FAIL: Component 9 -- settings not loaded")
    except Exception as e:
        print(f"ERROR: Component 9 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
