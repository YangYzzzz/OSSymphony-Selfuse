"""
Reward Script: Git rebase feature/pagination onto origin/main
Task ID: vscode_gf2_031
Domain: vscode
Scoring:
  Component 1 (0.5): Rebase completed — feature/pagination is based on origin/main tip
  Component 2 (0.25): origin/main commits are ancestors of feature/pagination
  Component 3 (0.25): Feature commits preserved on top of origin/main with correct messages
"""

import os
import zlib
import struct

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_031'
REPO_PATH = os.path.join(WORKDIR, 'projects', 'api')
GIT_DIR = os.path.join(REPO_PATH, '.git')


def resolve_ref(ref_name):
    """Resolve a git ref (branch name, remote ref) to a commit hash."""
    # Try packed-refs first for remote tracking branches
    ref_paths = []
    if '/' in ref_name and not ref_name.startswith('refs/'):
        # e.g. "origin/main" -> "refs/remotes/origin/main"
        ref_paths.append(os.path.join(GIT_DIR, 'refs', 'remotes', ref_name))
        # Also try as a local branch
        ref_paths.append(os.path.join(GIT_DIR, 'refs', 'heads', ref_name))
    else:
        ref_paths.append(os.path.join(GIT_DIR, 'refs', 'heads', ref_name))
        ref_paths.append(os.path.join(GIT_DIR, 'refs', 'remotes', ref_name))

    # Try direct file refs
    for ref_path in ref_paths:
        if os.path.isfile(ref_path):
            content = open(ref_path, 'r').read().strip()
            # Handle symbolic refs
            if content.startswith('ref: '):
                return resolve_ref_by_path(content[5:])
            return content

    # Try packed-refs
    packed_refs_path = os.path.join(GIT_DIR, 'packed-refs')
    if os.path.isfile(packed_refs_path):
        with open(packed_refs_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or line.startswith('^'):
                    continue
                parts = line.split()
                if len(parts) == 2:
                    sha, ref = parts
                    for rp in ref_paths:
                        # Convert file path to ref path for comparison
                        expected_ref = rp.replace(GIT_DIR + '/', '')
                        if ref == expected_ref:
                            return sha
    return None


def resolve_ref_by_path(ref_path):
    """Resolve a full ref path like refs/heads/main."""
    full_path = os.path.join(GIT_DIR, ref_path)
    if os.path.isfile(full_path):
        content = open(full_path, 'r').read().strip()
        if content.startswith('ref: '):
            return resolve_ref_by_path(content[5:])
        return content

    # Try packed-refs
    packed_refs_path = os.path.join(GIT_DIR, 'packed-refs')
    if os.path.isfile(packed_refs_path):
        with open(packed_refs_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or line.startswith('^'):
                    continue
                parts = line.split()
                if len(parts) == 2 and parts[1] == ref_path:
                    return parts[0]
    return None


def read_git_object(sha):
    """Read a git object and return (type, data)."""
    # Try loose object
    obj_path = os.path.join(GIT_DIR, 'objects', sha[:2], sha[2:])
    if os.path.isfile(obj_path):
        with open(obj_path, 'rb') as f:
            raw = zlib.decompress(f.read())
        header, _, data = raw.partition(b'\x00')
        obj_type = header.split(b' ')[0].decode()
        return obj_type, data

    # Try pack files
    pack_dir = os.path.join(GIT_DIR, 'objects', 'pack')
    if os.path.isdir(pack_dir):
        for fname in os.listdir(pack_dir):
            if fname.endswith('.idx'):
                pack_name = fname[:-4]
                result = read_from_pack(pack_dir, pack_name, sha)
                if result:
                    return result

    return None, None


def read_from_pack(pack_dir, pack_name, target_sha):
    """Read an object from a pack file. Returns (type, data) or None."""
    idx_path = os.path.join(pack_dir, pack_name + '.idx')
    pack_path = os.path.join(pack_dir, pack_name + '.pack')

    if not os.path.isfile(idx_path) or not os.path.isfile(pack_path):
        return None

    target_bytes = bytes.fromhex(target_sha)

    with open(idx_path, 'rb') as f:
        # Check magic number
        magic = f.read(4)
        if magic != b'\xfftOc':
            return None
        version = struct.unpack('>I', f.read(4))[0]
        if version != 2:
            return None

        # Read fanout table (256 entries, 4 bytes each)
        fanout = []
        for _ in range(256):
            fanout.append(struct.unpack('>I', f.read(4))[0])

        total_objects = fanout[255]

        # Binary search in the SHA section
        first_byte = target_bytes[0]
        start = fanout[first_byte - 1] if first_byte > 0 else 0
        end = fanout[first_byte]

        # SHA table starts at current position
        sha_table_offset = f.tell()

        found_index = None
        for i in range(start, end):
            f.seek(sha_table_offset + i * 20)
            sha = f.read(20)
            if sha == target_bytes:
                found_index = i
                break

        if found_index is None:
            return None

        # Skip CRC table
        crc_offset = sha_table_offset + total_objects * 20
        # 4-byte offset table
        offset_table_start = crc_offset + total_objects * 4

        f.seek(offset_table_start + found_index * 4)
        pack_offset = struct.unpack('>I', f.read(4))[0]

        # Check for 8-byte offset (MSB set)
        if pack_offset & 0x80000000:
            large_offset_table = offset_table_start + total_objects * 4
            large_idx = pack_offset & 0x7FFFFFFF
            f.seek(large_offset_table + large_idx * 8)
            pack_offset = struct.unpack('>Q', f.read(8))[0]

    # Read from pack file
    with open(pack_path, 'rb') as f:
        f.seek(pack_offset)
        byte = f.read(1)[0]
        obj_type_num = (byte >> 4) & 0x07
        size = byte & 0x0F
        shift = 4
        while byte & 0x80:
            byte = f.read(1)[0]
            size |= (byte & 0x7F) << shift
            shift += 7

        type_map = {1: 'commit', 2: 'tree', 3: 'blob', 4: 'tag'}

        if obj_type_num in type_map:
            # Non-delta object
            remaining = f.read()
            try:
                data = zlib.decompress(remaining)
                return type_map[obj_type_num], data
            except zlib.error:
                # Try with limited buffer
                d = zlib.decompressobj()
                data = d.decompress(remaining, size + 512)
                return type_map[obj_type_num], data[:size]

    return None


def get_commit_parents(sha):
    """Get parent commit hashes from a commit object."""
    obj_type, data = read_git_object(sha)
    if obj_type != 'commit' or data is None:
        return []
    parents = []
    for line in data.decode('utf-8', errors='replace').split('\n'):
        if line.startswith('parent '):
            parents.append(line.split()[1])
        elif line == '':
            break
    return parents


def get_commit_message(sha):
    """Get the first line of a commit message."""
    obj_type, data = read_git_object(sha)
    if obj_type != 'commit' or data is None:
        return ''
    text = data.decode('utf-8', errors='replace')
    # Message starts after the first blank line
    parts = text.split('\n\n', 1)
    if len(parts) > 1:
        return parts[1].strip().split('\n')[0]
    return ''


def is_ancestor(ancestor_sha, descendant_sha, max_depth=50):
    """Check if ancestor_sha is an ancestor of descendant_sha by walking the parent chain."""
    visited = set()
    queue = [descendant_sha]
    depth = 0
    while queue and depth < max_depth:
        current = queue.pop(0)
        if current == ancestor_sha:
            return True
        if current in visited:
            continue
        visited.add(current)
        parents = get_commit_parents(current)
        queue.extend(parents)
        depth += 1
    return False


def get_commits_between(base_sha, tip_sha, max_depth=50):
    """Get commits reachable from tip_sha but not from base_sha (base_sha..tip_sha)."""
    # Walk from tip back to base, collecting commits
    commits = []
    visited = set()
    queue = [tip_sha]
    while queue:
        current = queue.pop(0)
        if current == base_sha or current in visited:
            continue
        visited.add(current)
        commits.append(current)
        parents = get_commit_parents(current)
        queue.extend(parents)
        if len(visited) > max_depth:
            break
    return commits


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repo exists
    if not os.path.isdir(GIT_DIR):
        print(f"CRITICAL: Git repo not found at {REPO_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Resolve refs
    feature_sha = resolve_ref('feature/pagination')
    origin_main_sha = resolve_ref('origin/main')

    if not feature_sha:
        print("CRITICAL: Cannot resolve feature/pagination ref")
        print("REWARD: 0.0")
        return 0.0

    if not origin_main_sha:
        print("CRITICAL: Cannot resolve origin/main ref")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: feature/pagination -> {feature_sha[:8]}")
    print(f"INFO: origin/main -> {origin_main_sha[:8]}")

    # Component 1: Rebase completed — merge-base equals origin/main tip (0.5 points)
    # After rebase, the common ancestor of feature/pagination and origin/main
    # should be origin/main itself (feature branch is on top of it).
    # We check this by verifying origin/main IS an ancestor of feature/pagination
    # AND the first divergence point walking back from feature/pagination hits origin/main.
    try:
        # Walk back from feature/pagination following first-parent chain to find origin/main
        current = feature_sha
        origin_main_in_ancestry = (current == origin_main_sha)
        steps = 0
        while not origin_main_in_ancestry and current and steps < 50:
            parents = get_commit_parents(current)
            if not parents:
                break
            current = parents[0]  # Follow first parent
            origin_main_in_ancestry = (current == origin_main_sha)
            steps += 1

        if origin_main_in_ancestry:
            print(f"PASS: Component 1 — feature/pagination is rebased on origin/main ({origin_main_sha[:8]}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — feature/pagination does not have origin/main in its direct ancestry")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: origin/main is a direct ancestor of feature/pagination (0.25 points)
    # Before rebase: origin/main and feature/pagination diverge, origin/main is NOT ancestor
    # After rebase: origin/main IS a direct ancestor
    try:
        if is_ancestor(origin_main_sha, feature_sha):
            print(f"PASS: Component 2 — origin/main is an ancestor of feature/pagination (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — origin/main is NOT an ancestor of feature/pagination")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Feature commits preserved with correct messages (0.25 points)
    # After rebase, between origin/main and feature/pagination there should be exactly 3 commits
    # with the original feature commit messages, AND origin/main must be ancestor (gate).
    expected_messages = [
        "Add pagination utility with PaginatedResponse dataclass",
        "Integrate pagination into products list endpoint",
        "Add unit tests for pagination utility",
    ]
    try:
        if not is_ancestor(origin_main_sha, feature_sha):
            print(f"FAIL: Component 3 — Cannot verify: origin/main not ancestor of feature/pagination")
        else:
            commits_between = get_commits_between(origin_main_sha, feature_sha)
            actual_messages = []
            for sha in commits_between:
                msg = get_commit_message(sha)
                if msg:
                    actual_messages.append(msg)

            found_count = 0
            for expected in expected_messages:
                if any(expected in m for m in actual_messages):
                    found_count += 1
                else:
                    print(f"  MISS: '{expected}'")

            if found_count == len(expected_messages) and len(commits_between) == len(expected_messages):
                print(f"PASS: Component 3 — All {found_count} feature commit messages preserved (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — {found_count}/{len(expected_messages)} messages found, {len(commits_between)} commits between refs")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
