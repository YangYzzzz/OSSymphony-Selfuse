"""
Reward Script: Git initialization in VSCode web project
Task ID: vscode_gf5_003
Domain: vscode
Scoring:
  Component 1: .git directory exists (0.20)
  Component 2: .gitignore has node_modules/ (0.15)
  Component 3: .gitignore has .env (0.15)
  Component 4: Git log contains 'Initial commit' (0.25)
  Component 5: All project files tracked (0.15)
  Component 6: Clean working tree (0.10)
"""

import os
import configparser

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_003'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'web-project')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .git directory exists (0.20 points)
    # This verifies git init was run. Fails on initial_env (no .git), passes on golden_env.
    try:
        git_dir = os.path.join(PROJECT_DIR, '.git')
        if os.path.isdir(git_dir):
            # Further verify it's a valid git repo by checking HEAD exists
            head_file = os.path.join(git_dir, 'HEAD')
            if os.path.isfile(head_file):
                print(f"PASS: Component 1 — .git directory exists with HEAD (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — .git dir exists but no HEAD file")
        else:
            print(f"FAIL: Component 1 — .git directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: .gitignore contains node_modules/ (0.15 points)
    # Task requires .gitignore with node_modules entry. Fails on initial_env (no .gitignore).
    try:
        gitignore_path = os.path.join(PROJECT_DIR, '.gitignore')
        if os.path.isfile(gitignore_path):
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
            # Check for node_modules entry (with or without trailing slash)
            lines = [line.strip() for line in gitignore_content.splitlines()]
            if any(line in ('node_modules', 'node_modules/') for line in lines):
                print(f"PASS: Component 2 — .gitignore contains node_modules entry (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — .gitignore exists but no node_modules entry. Lines: {lines}")
        else:
            print(f"FAIL: Component 2 — .gitignore file does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: .gitignore contains .env (0.15 points)
    # Task requires .gitignore with .env entry. Fails on initial_env (no .gitignore).
    try:
        gitignore_path = os.path.join(PROJECT_DIR, '.gitignore')
        if os.path.isfile(gitignore_path):
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
            lines = [line.strip() for line in gitignore_content.splitlines()]
            if any(line in ('.env', '.env/') for line in lines):
                print(f"PASS: Component 3 — .gitignore contains .env entry (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — .gitignore exists but no .env entry. Lines: {lines}")
        else:
            print(f"FAIL: Component 3 — .gitignore file does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Git log contains commit with message 'Initial commit' (0.25 points)
    # This is the core task action. Fails on initial_env (no git repo / no commits).
    try:
        git_dir = os.path.join(PROJECT_DIR, '.git')
        if not os.path.isdir(git_dir):
            print(f"FAIL: Component 4 — no .git directory, cannot check log")
        else:
            # Read the commit message from the HEAD commit
            # Parse HEAD to find the current branch ref
            head_path = os.path.join(git_dir, 'HEAD')
            with open(head_path, 'r') as f:
                head_content = f.read().strip()

            commit_hash = None
            if head_content.startswith('ref: '):
                ref_path = os.path.join(git_dir, head_content[5:])
                if os.path.isfile(ref_path):
                    with open(ref_path, 'r') as f:
                        commit_hash = f.read().strip()
            else:
                # Detached HEAD - direct commit hash
                commit_hash = head_content

            if commit_hash:
                # Read the commit object to find the message
                # Git objects are stored in .git/objects/xx/yyyy...
                obj_dir = os.path.join(git_dir, 'objects', commit_hash[:2])
                obj_file = os.path.join(obj_dir, commit_hash[2:])

                if os.path.isfile(obj_file):
                    # Decompress the git object
                    import zlib
                    with open(obj_file, 'rb') as f:
                        raw = zlib.decompress(f.read())
                    # Git commit object format: "commit <size>\0<content>"
                    content = raw.split(b'\x00', 1)[1].decode('utf-8', errors='replace')
                    # The commit message is after the blank line
                    parts = content.split('\n\n', 1)
                    if len(parts) > 1:
                        message = parts[1].strip()
                        if message == 'Initial commit':
                            print(f"PASS: Component 4 — commit message is 'Initial commit' (0.25 pts)")
                            total_score += 0.25
                        else:
                            print(f"FAIL: Component 4 — commit message is '{message}', expected 'Initial commit'")
                    else:
                        print(f"FAIL: Component 4 — could not parse commit message from object")
                else:
                    # Object might be in a pack file; try reading COMMIT_EDITMSG as fallback
                    commit_editmsg = os.path.join(git_dir, 'COMMIT_EDITMSG')
                    if os.path.isfile(commit_editmsg):
                        with open(commit_editmsg, 'r') as f:
                            msg = f.read().strip()
                        if msg == 'Initial commit':
                            print(f"PASS: Component 4 — COMMIT_EDITMSG is 'Initial commit' (0.25 pts)")
                            total_score += 0.25
                        else:
                            print(f"FAIL: Component 4 — COMMIT_EDITMSG is '{msg}', expected 'Initial commit'")
                    else:
                        print(f"FAIL: Component 4 — cannot read commit object (may be packed)")
            else:
                print(f"FAIL: Component 4 — no commit found at HEAD")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: All project files are tracked (index.html, style.css, .gitignore) (0.15 points)
    # Fails on initial_env (no git repo). Passes on golden_env where files are committed.
    try:
        git_dir = os.path.join(PROJECT_DIR, '.git')
        if not os.path.isdir(git_dir):
            print(f"FAIL: Component 5 — no .git directory, cannot check tracked files")
        else:
            # Read the git index file to find tracked files
            index_path = os.path.join(git_dir, 'index')
            if os.path.isfile(index_path):
                with open(index_path, 'rb') as f:
                    index_data = f.read()
                # The index file contains file names as null-terminated strings
                # We can search for our expected filenames
                expected_files = ['index.html', 'style.css', '.gitignore']
                tracked = []
                for fname in expected_files:
                    if fname.encode('utf-8') in index_data:
                        tracked.append(fname)

                if set(expected_files) == set(tracked):
                    print(f"PASS: Component 5 — all files tracked: {tracked} (0.15 pts)")
                    total_score += 0.15
                else:
                    missing = set(expected_files) - set(tracked)
                    print(f"FAIL: Component 5 — missing tracked files: {missing}")
            else:
                print(f"FAIL: Component 5 — git index file not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Clean working tree (no uncommitted changes) (0.10 points)
    # Fails on initial_env (no git repo). Passes on golden_env (all committed).
    try:
        git_dir = os.path.join(PROJECT_DIR, '.git')
        if not os.path.isdir(git_dir):
            print(f"FAIL: Component 6 — no .git directory, cannot check working tree")
        else:
            # Check if there are any modified/untracked files by comparing
            # the working directory files with what's tracked
            # A clean tree means: all files in project dir are tracked AND
            # no modifications since last commit
            # Simple heuristic: list files in project dir, compare to tracked
            all_files = []
            for item in os.listdir(PROJECT_DIR):
                if item == '.git':
                    continue
                all_files.append(item)

            expected_files = ['index.html', 'style.css', '.gitignore']
            # Check no extra untracked files exist
            extra = set(all_files) - set(expected_files)
            if len(extra) == 0:
                # All files in directory are expected ones; if they're all tracked (component 5),
                # working tree should be clean
                print(f"PASS: Component 6 — working tree appears clean, no extra files (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — extra files found in working directory: {extra}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
