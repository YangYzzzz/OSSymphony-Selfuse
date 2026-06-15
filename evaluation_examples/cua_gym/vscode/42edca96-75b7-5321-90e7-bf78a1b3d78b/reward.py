"""
Reward Script: Force push feature/rewrite branch to origin after rebase
Task ID: vscode_gs_044
Domain: vscode
Scoring:
  Component 1 (0.5): Local and remote feature/rewrite point to the same commit hash
  Component 2 (0.3): Current branch is feature/rewrite and local ref matches remote ref
  Component 3 (0.2): Remote origin/feature/rewrite contains the rebased commit
                      "Add logging utility module" (present in local rebased history
                      but absent from pre-rebase remote)
"""

import os
import zlib

WORKDIR = '/home/user'
TASK_ID = 'vscode_gs_044'
REPO_PATH = os.path.join(WORKDIR, 'projects', 'webapp')
GIT_DIR = os.path.join(REPO_PATH, '.git')


def read_ref(ref_path):
    """Read a git ref file and return the SHA hash."""
    full_path = os.path.join(GIT_DIR, ref_path)
    if not os.path.exists(full_path):
        return None
    with open(full_path) as f:
        return f.read().strip()


def read_git_object(sha):
    """Read a loose git object and return (type, content)."""
    obj_path = os.path.join(GIT_DIR, 'objects', sha[:2], sha[2:])
    if not os.path.exists(obj_path):
        return None
    with open(obj_path, 'rb') as f:
        data = zlib.decompress(f.read())
    null_idx = data.index(b'\x00')
    header = data[:null_idx].decode()
    content = data[null_idx + 1:]
    obj_type = header.split()[0]
    return obj_type, content


def get_commit_message(sha):
    """Extract the commit message from a commit object."""
    result = read_git_object(sha)
    if result is None:
        return None
    obj_type, content = result
    if obj_type != 'commit':
        return None
    text = content.decode('utf-8', errors='replace')
    blank_idx = text.index('\n\n')
    return text[blank_idx + 2:].strip()


def get_parent_sha(sha):
    """Get the first parent SHA from a commit object."""
    result = read_git_object(sha)
    if result is None:
        return None
    obj_type, content = result
    text = content.decode('utf-8', errors='replace')
    for line in text.split('\n'):
        if line.startswith('parent '):
            return line.split()[1]
        if line == '':
            break
    return None


def walk_commit_messages(start_sha, max_depth=20):
    """Walk commit history and return list of commit messages."""
    messages = []
    sha = start_sha
    for _ in range(max_depth):
        if sha is None:
            break
        msg = get_commit_message(sha)
        if msg is None:
            break
        messages.append(msg)
        sha = get_parent_sha(sha)
    return messages


def verify_task():
    """
    Verify that force push of feature/rewrite to origin was completed.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: repo exists
    if not os.path.isdir(GIT_DIR):
        print(f"CRITICAL: Git repo not found at {REPO_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: on feature/rewrite branch
    head_content = read_ref('HEAD')
    if head_content is None or head_content != 'ref: refs/heads/feature/rewrite':
        print(f"CRITICAL: Not on feature/rewrite branch (HEAD: {head_content})")
        print("REWARD: 0.0")
        return 0.0

    # Read local and remote refs
    local_sha = read_ref('refs/heads/feature/rewrite')
    remote_sha = read_ref('refs/remotes/origin/feature/rewrite')

    if local_sha is None:
        print("CRITICAL: Local feature/rewrite ref not found")
        print("REWARD: 0.0")
        return 0.0

    if remote_sha is None:
        print("CRITICAL: Remote origin/feature/rewrite ref not found")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Local and remote feature/rewrite point to same commit (0.5 points)
    # In initial_env: different hashes (diverged after rebase) -> FAIL
    # In golden_env: same hash (force push synced them) -> PASS
    try:
        if local_sha == remote_sha:
            print(f"PASS: Component 1 — local ({local_sha[:8]}) matches remote ({remote_sha[:8]}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — local ({local_sha[:8]}) != remote ({remote_sha[:8]})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The remote bare repo also has the updated ref (0.3 points)
    # Check the bare repo at /home/user/projects/webapp.git to confirm the push propagated
    # In initial_env: bare repo ref differs from local -> FAIL
    # In golden_env: bare repo ref matches local -> PASS
    try:
        bare_repo_ref = os.path.join(WORKDIR, 'projects', 'webapp.git', 'refs', 'heads', 'feature', 'rewrite')
        if os.path.exists(bare_repo_ref):
            with open(bare_repo_ref) as f:
                bare_sha = f.read().strip()
            if bare_sha == local_sha:
                print(f"PASS: Component 2 — bare repo ref ({bare_sha[:8]}) matches local ({local_sha[:8]}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — bare repo ref ({bare_sha[:8]}) != local ({local_sha[:8]})")
        else:
            # Try packed-refs in bare repo
            packed_path = os.path.join(WORKDIR, 'projects', 'webapp.git', 'packed-refs')
            if os.path.exists(packed_path):
                with open(packed_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.endswith('refs/heads/feature/rewrite'):
                            bare_sha = line.split()[0]
                            if bare_sha == local_sha:
                                print(f"PASS: Component 2 — bare repo packed ref matches local (0.3 pts)")
                                total_score += 0.3
                            else:
                                print(f"FAIL: Component 2 — bare repo packed ref ({bare_sha[:8]}) != local ({local_sha[:8]})")
                            break
                    else:
                        print("FAIL: Component 2 — feature/rewrite not found in bare repo packed-refs")
            else:
                print("FAIL: Component 2 — bare repo ref not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Remote origin/feature/rewrite contains "Add logging utility module" commit (0.2 points)
    # This commit is part of the rebased local history but was NOT in the pre-rebase remote.
    # In initial_env: remote doesn't have this commit -> FAIL
    # In golden_env: after force push, remote has it -> PASS
    try:
        remote_messages = walk_commit_messages(remote_sha, max_depth=20)
        if 'Add logging utility module' in remote_messages:
            print(f"PASS: Component 3 — remote contains rebased commit 'Add logging utility module' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — remote does not contain 'Add logging utility module' commit")
            print(f"  Remote commits: {remote_messages}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
