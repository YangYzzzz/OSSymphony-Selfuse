"""
Reward Script: Git repository initialization with .gitignore
Task ID: vscode_wf_016
Domain: vscode (os/git operations)
Scoring:
  Component 1: .git directory exists (0.2 pts)
  Component 2: .gitignore contains node_modules/, .env, dist/ (0.3 pts)
  Component 3: Git log has one commit with message 'Initial commit' (0.3 pts)
  Component 4: node_modules and .env are NOT tracked by git (0.2 pts)
"""

import os

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .git directory exists — git repository initialized (0.2 points)
    try:
        git_dir = os.path.join(PROJECT_DIR, '.git')
        if os.path.isdir(git_dir):
            # Verify it's a real git repo by checking for HEAD file
            head_file = os.path.join(git_dir, 'HEAD')
            if os.path.isfile(head_file):
                print(f"PASS: Component 1 — .git directory exists with HEAD file (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — .git directory exists but no HEAD file")
        else:
            print(f"FAIL: Component 1 — .git directory does not exist at {git_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: .gitignore contains node_modules/, .env, and dist/ (0.3 points)
    try:
        gitignore_path = os.path.join(PROJECT_DIR, '.gitignore')
        if os.path.isfile(gitignore_path):
            with open(gitignore_path, 'r') as f:
                content = f.read()
            lines = [line.strip() for line in content.strip().splitlines() if line.strip()]

            required_entries = ['node_modules/', '.env', 'dist/']
            found_count = 0
            for entry in required_entries:
                # Check for exact match or match without trailing slash
                entry_base = entry.rstrip('/')
                if entry in lines or entry_base in lines:
                    found_count += 1
                    print(f"  FOUND: '{entry}' in .gitignore")
                else:
                    print(f"  MISSING: '{entry}' in .gitignore")

            if found_count == len(required_entries):
                print(f"PASS: Component 2 — .gitignore contains all 3 required entries (0.3 pts)")
                total_score += 0.3
            elif found_count > 0:
                partial = round(0.3 * found_count / len(required_entries), 2)
                print(f"PARTIAL: Component 2 — {found_count}/{len(required_entries)} entries found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — .gitignore exists but contains none of the required entries")
        else:
            print(f"FAIL: Component 2 — .gitignore file does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Git log shows one commit with message 'Initial commit' (0.3 points)
    try:
        # Read git log by parsing git objects directly
        # We need to check the commit message from the git repository
        git_dir = os.path.join(PROJECT_DIR, '.git')
        if not os.path.isdir(git_dir):
            print(f"FAIL: Component 3 — No .git directory, cannot check git log")
        else:
            # Read HEAD to find the current ref
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
                commit_hash = head_content

            if commit_hash:
                # Read the commit object using zlib
                import zlib
                obj_path = os.path.join(git_dir, 'objects', commit_hash[:2], commit_hash[2:])
                if os.path.isfile(obj_path):
                    with open(obj_path, 'rb') as f:
                        raw = zlib.decompress(f.read())
                    # Parse commit object: header\0content
                    null_idx = raw.index(b'\x00')
                    commit_data = raw[null_idx + 1:].decode('utf-8', errors='replace')

                    # Extract commit message (after blank line)
                    parts = commit_data.split('\n\n', 1)
                    if len(parts) >= 2:
                        message = parts[1].strip()
                    else:
                        message = ''

                    # Check parent field to ensure this is the only commit
                    header_part = parts[0] if parts else ''
                    has_parent = 'parent ' in header_part

                    if message == 'Initial commit' and not has_parent:
                        print(f"PASS: Component 3 — Single commit with message 'Initial commit' (0.3 pts)")
                        total_score += 0.3
                    elif message == 'Initial commit':
                        print(f"PARTIAL: Component 3 — Commit message matches but there are parent commits (0.15 pts)")
                        total_score += 0.15
                    else:
                        print(f"FAIL: Component 3 — Commit message is '{message}', expected 'Initial commit'")
                else:
                    # Might be a packed object, try pack files
                    # Fall back to checking COMMIT_EDITMSG as a hint
                    cem_path = os.path.join(git_dir, 'COMMIT_EDITMSG')
                    if os.path.isfile(cem_path):
                        with open(cem_path, 'r') as f:
                            cem = f.read().strip()
                        if cem == 'Initial commit':
                            print(f"PASS: Component 3 — COMMIT_EDITMSG confirms 'Initial commit' (0.3 pts)")
                            total_score += 0.3
                        else:
                            print(f"FAIL: Component 3 — COMMIT_EDITMSG is '{cem}', expected 'Initial commit'")
                    else:
                        print(f"FAIL: Component 3 — Could not read commit object or COMMIT_EDITMSG")
            else:
                print(f"FAIL: Component 3 — No commit hash found in HEAD")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: node_modules and .env are NOT tracked by git (0.2 points)
    try:
        git_dir = os.path.join(PROJECT_DIR, '.git')
        if not os.path.isdir(git_dir):
            print(f"FAIL: Component 4 — No .git directory, cannot check tracked files")
        else:
            # Read the git index to find tracked files
            index_path = os.path.join(git_dir, 'index')
            if os.path.isfile(index_path):
                with open(index_path, 'rb') as f:
                    index_data = f.read()

                # Parse git index: find all file paths
                # Git index format: 4-byte sig, 4-byte version, 4-byte num entries, then entries
                import struct
                sig = index_data[:4]
                if sig == b'DIRC':
                    version = struct.unpack('>I', index_data[4:8])[0]
                    num_entries = struct.unpack('>I', index_data[8:12])[0]

                    tracked_files = []
                    offset = 12
                    for _ in range(num_entries):
                        # Each entry: 40 bytes of stat info + 20 bytes SHA + 2 bytes flags
                        # flags contain name length (lower 12 bits)
                        if offset + 62 > len(index_data):
                            break
                        flags = struct.unpack('>H', index_data[offset + 60:offset + 62])[0]
                        name_len = flags & 0xFFF
                        name_start = offset + 62
                        if name_len > 0 and name_start + name_len <= len(index_data):
                            name = index_data[name_start:name_start + name_len].decode('utf-8', errors='replace')
                        else:
                            # Name length might be 0xFFF meaning name is longer, read until null
                            null_pos = index_data.index(b'\x00', name_start)
                            name = index_data[name_start:null_pos].decode('utf-8', errors='replace')

                        tracked_files.append(name)

                        # Entry is padded to multiple of 8 bytes
                        entry_len = 62 + len(name.encode('utf-8')) + 1  # +1 for null terminator
                        entry_len = (entry_len + 7) & ~7  # round up to 8
                        offset += entry_len

                    print(f"  Tracked files: {tracked_files}")

                    # Check that no tracked file starts with node_modules/ or is .env
                    node_modules_tracked = any(f.startswith('node_modules/') or f == 'node_modules' for f in tracked_files)
                    env_tracked = any(f == '.env' or f.startswith('.env/') for f in tracked_files)

                    if not node_modules_tracked and not env_tracked:
                        print(f"PASS: Component 4 — node_modules and .env are not tracked (0.2 pts)")
                        total_score += 0.2
                    else:
                        if node_modules_tracked:
                            print(f"FAIL: Component 4 — node_modules is tracked in git")
                        if env_tracked:
                            print(f"FAIL: Component 4 — .env is tracked in git")
                else:
                    print(f"FAIL: Component 4 — Invalid git index file")
            else:
                print(f"FAIL: Component 4 — No git index file found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
