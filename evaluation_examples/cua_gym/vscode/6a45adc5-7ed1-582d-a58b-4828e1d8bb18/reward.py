"""
Reward Script: Set up local bare repository as remote, push main branch, create tracking branch
Task ID: vscode_git_059
Domain: vs_code (git operations)
Scoring:
  Component 1: /tmp/shared-repo.git exists as a bare repository (0.2 pts)
  Component 2: Remote 'origin' configured in /home/user/project pointing to /tmp/shared-repo.git (0.2 pts)
  Component 3: main branch pushed to remote with all 5 original commits (0.3 pts)
  Component 4: develop branch exists on remote and is tracked locally (0.3 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_059'
PROJECT_DIR = '/home/user/project'
BARE_REPO_PATH = '/tmp/shared-repo.git'
EXPECTED_REMOTE_NAME = 'origin'
EXPECTED_MAIN_COMMITS = 5


def count_commits_in_bare_repo(bare_repo_path, branch_name):
    """
    Count commits reachable from a branch in a bare git repository
    by traversing the commit chain via git object files.
    Uses only file I/O — no external processes.
    """
    try:
        ref_path = os.path.join(bare_repo_path, 'refs', 'heads', branch_name)
        if not os.path.isfile(ref_path):
            return -1, f"ref file not found: {ref_path}"

        with open(ref_path, 'r') as f:
            current_sha = f.read().strip()

        visited = set()
        count = 0
        max_depth = 200  # safety cap

        while current_sha and current_sha not in visited and count < max_depth:
            visited.add(current_sha)
            obj_dir = os.path.join(bare_repo_path, 'objects', current_sha[:2])
            obj_file = os.path.join(obj_dir, current_sha[2:])

            if not os.path.isfile(obj_file):
                # Try packed-objects — check packed-refs approach
                # If the object is in a pack file, we can't easily traverse it
                # Fall back to counting refs via packed-refs
                return _count_commits_via_packed(bare_repo_path, branch_name)

            # Read the raw (zlib-compressed) git object
            import zlib
            with open(obj_file, 'rb') as f:
                raw = zlib.decompress(f.read())

            # Format: "commit <size>\x00<content>"
            null_pos = raw.index(b'\x00')
            header = raw[:null_pos].decode('utf-8', errors='replace')
            if not header.startswith('commit'):
                break  # unexpected object type

            count += 1
            content = raw[null_pos + 1:]

            # Parse parent SHA(s) from commit content
            parent_sha = None
            for line in content.decode('utf-8', errors='replace').split('\n'):
                if line.startswith('parent '):
                    parent_sha = line.split(' ', 1)[1].strip()
                    break  # follow first parent only (linear history)
                elif line == '':
                    break  # empty line = end of headers

            current_sha = parent_sha

        return count, None
    except Exception as e:
        return -1, str(e)


def _count_commits_via_packed(bare_repo_path, branch_name):
    """
    Fallback: use git pack index to count commits.
    Counts commits by scanning pack-*.idx files for commit objects.
    This is a best-effort approximation for repos with packed objects.
    Returns tuple (count_or_estimate, error_or_None).
    """
    try:
        pack_dir = os.path.join(bare_repo_path, 'objects', 'pack')
        if not os.path.isdir(pack_dir):
            return -1, "No pack directory found"

        # For simplicity, read the pack data file to count commit objects
        import zlib
        import struct

        pack_files = [f for f in os.listdir(pack_dir) if f.endswith('.pack')]
        if not pack_files:
            return -1, "No pack files found"

        # Use the idx file to count commit-type objects
        idx_files = [f for f in os.listdir(pack_dir) if f.endswith('.idx')]
        if not idx_files:
            return -1, "No idx files found"

        # Parse v2 pack index to get SHA list, then read pack file for types
        idx_path = os.path.join(pack_dir, idx_files[0])
        pack_path = os.path.join(pack_dir, pack_files[0])

        with open(idx_path, 'rb') as f:
            magic = f.read(4)
            version = struct.unpack('>I', f.read(4))[0]
            if magic != b'\xff\x74\x4f\x63' or version != 2:
                return -1, "Unsupported pack index format"

            # Fan-out table: 256 entries of 4 bytes
            fan_out = struct.unpack('>256I', f.read(256 * 4))
            total_objects = fan_out[255]

            # Read all SHA1s
            shas = []
            for _ in range(total_objects):
                shas.append(f.read(20).hex())

        # Read pack file to get object types for each SHA
        commit_count = 0
        with open(pack_path, 'rb') as f:
            magic = f.read(4)
            version = struct.unpack('>I', f.read(4))[0]
            num_objects = struct.unpack('>I', f.read(4))[0]

            # Read objects sequentially
            for _ in range(num_objects):
                # Read the size+type byte(s)
                byte = ord(f.read(1))
                obj_type = (byte >> 4) & 0x7
                size = byte & 0xf
                shift = 4
                while byte & 0x80:
                    byte = ord(f.read(1))
                    size |= (byte & 0x7f) << shift
                    shift += 7

                if obj_type == 1:  # commit
                    commit_count += 1

                # Skip the compressed data
                start = f.tell()
                d = zlib.decompressobj()
                compressed = f.read(size + 64)  # read more than needed
                try:
                    decompressed = d.decompress(compressed)
                    unused = len(d.unused_data)
                    f.seek(start + len(compressed) - unused)
                except Exception:
                    break

        return commit_count, None

    except Exception as e:
        return -1, str(e)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: /tmp/shared-repo.git exists as a bare repository (0.2 points)
    # This FAILS on initial (no bare repo) → PASSES on golden ✅
    try:
        bare_repo_exists = os.path.isdir(BARE_REPO_PATH)
        if not bare_repo_exists:
            print(f"FAIL: Component 1 — {BARE_REPO_PATH} does not exist as a directory")
        else:
            head_file = os.path.join(BARE_REPO_PATH, 'HEAD')
            objects_dir = os.path.join(BARE_REPO_PATH, 'objects')
            config_file = os.path.join(BARE_REPO_PATH, 'config')
            is_bare_structure = (
                os.path.isfile(head_file) and
                os.path.isdir(objects_dir) and
                os.path.isfile(config_file)
            )
            if is_bare_structure:
                with open(config_file, 'r') as f:
                    config_content = f.read()
                if 'bare = true' in config_content:
                    print(f"PASS: Component 1 — {BARE_REPO_PATH} exists as bare git repo (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 1 — {BARE_REPO_PATH} exists but 'bare = true' not found in config")
            else:
                print(f"FAIL: Component 1 — {BARE_REPO_PATH} is not a valid bare git repo (missing HEAD/objects/config)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Remote 'origin' configured pointing to /tmp/shared-repo.git (0.2 points)
    # This FAILS on initial (no remote) → PASSES on golden ✅
    try:
        git_config_path = os.path.join(PROJECT_DIR, '.git', 'config')
        if not os.path.isfile(git_config_path):
            print(f"FAIL: Component 2 — {PROJECT_DIR}/.git/config not found")
        else:
            with open(git_config_path, 'r') as f:
                git_config = f.read()
            has_origin_remote = f'[remote "{EXPECTED_REMOTE_NAME}"]' in git_config
            has_correct_url = f'url = {BARE_REPO_PATH}' in git_config
            if has_origin_remote and has_correct_url:
                print(f"PASS: Component 2 — Remote '{EXPECTED_REMOTE_NAME}' configured with url={BARE_REPO_PATH} (0.2 pts)")
                total_score += 0.2
            elif has_origin_remote:
                print(f"FAIL: Component 2 — Remote '{EXPECTED_REMOTE_NAME}' exists but url is not {BARE_REPO_PATH}")
            else:
                print(f"FAIL: Component 2 — Remote '{EXPECTED_REMOTE_NAME}' not configured in {git_config_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: main branch pushed to remote with all 5 original commits (0.3 points)
    # This FAILS on initial (no bare repo, no pushes) → PASSES on golden ✅
    try:
        main_ref_path = os.path.join(BARE_REPO_PATH, 'refs', 'heads', 'main')
        if not os.path.isfile(main_ref_path):
            print(f"FAIL: Component 3 — 'main' branch not found in bare repository refs")
        else:
            commit_count, err = count_commits_in_bare_repo(BARE_REPO_PATH, 'main')
            if err:
                print(f"FAIL: Component 3 — Could not count commits in remote main: {err}")
            elif commit_count >= EXPECTED_MAIN_COMMITS:
                print(f"PASS: Component 3 — Remote 'main' has {commit_count} commits (expected >= {EXPECTED_MAIN_COMMITS}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Remote 'main' has {commit_count} commits, expected >= {EXPECTED_MAIN_COMMITS}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: develop branch exists on remote AND is tracked locally (0.3 points)
    # This FAILS on initial (no develop branch, no bare repo) → PASSES on golden ✅
    try:
        develop_ref_path = os.path.join(BARE_REPO_PATH, 'refs', 'heads', 'develop')
        remote_develop_exists = os.path.isfile(develop_ref_path)

        if not remote_develop_exists:
            print(f"FAIL: Component 4 — 'develop' branch not found in remote bare repository")
        else:
            git_config_path = os.path.join(PROJECT_DIR, '.git', 'config')
            with open(git_config_path, 'r') as f:
                git_config = f.read()

            has_branch_develop_section = '[branch "develop"]' in git_config
            has_tracking_remote = 'remote = origin' in git_config
            has_tracking_merge = 'merge = refs/heads/develop' in git_config

            if has_branch_develop_section and has_tracking_remote and has_tracking_merge:
                print(f"PASS: Component 4 — 'develop' branch on remote with local tracking configured (0.3 pts)")
                total_score += 0.3
            elif not has_branch_develop_section:
                print(f"FAIL: Component 4 — 'develop' on remote but no [branch \"develop\"] section in .git/config")
            else:
                print(f"FAIL: Component 4 — 'develop' on remote but tracking config incomplete (remote={has_tracking_remote}, merge={has_tracking_merge})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
