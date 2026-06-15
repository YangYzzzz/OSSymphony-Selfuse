"""
Reward Script: Manage multiple stashes
Task ID: vscode_git_062
Domain: vs_code (git stash management)
Scoring:
  Component 1: Exactly 1 stash remaining (0.30 pts)
  Component 2: Remaining stash is 'WIP: file A' (0.20 pts)
  Component 3: file_b.py contains get_user_by_email function (0.25 pts)
  Component 4: file_c.py contains format_response function (0.25 pts)
  Total: 1.00

Strategy:
  - Components 1 & 2: Read git internal files directly:
      .git/refs/stash     — existence means at least one stash exists
      .git/logs/refs/stash — each line is one stash entry; count lines for stash count
                             each line ends with 'On master: <stash_message>'
  - Components 3 & 4: Read working-tree Python files directly.

Initial state (before task): 3 stashes (C, B, A), clean working tree
Golden state (after task):   1 stash ('WIP: file A'), file_b.py and file_c.py modified
"""

import os

WORKDIR = '/home/user/project'
TASK_ID = 'vscode_git_062'


def read_stash_log(project_dir):
    """
    Read the git stash reflog to get a list of stash messages.
    Returns a list of stash message strings (e.g., ['On master: WIP: file A']).
    Returns empty list if no stashes exist.
    """
    stash_log_path = os.path.join(project_dir, '.git', 'logs', 'refs', 'stash')
    if not os.path.exists(stash_log_path):
        return []
    try:
        with open(stash_log_path, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        # Parse the stash log to get active stash entries
        # Each line format: <old_hash> <new_hash> <author> <timestamp> <tz>\t<message>
        # Count unique active stashes from refs/stash (packed/loose objects)
        return lines
    except Exception:
        return []


def count_active_stashes(project_dir):
    """
    Count the number of active stashes by reading the stash reflog.

    The stash reflog contains one line per stash push. When a stash is dropped/popped,
    a new "drop" entry is NOT written to this log — instead the stash ref is updated.
    The actual count of active stashes corresponds to how many entries exist in the
    stash reflog where the new hash is not the all-zeros hash from the previous entry.

    Simplest reliable approach: count lines in the reflog where the old hash is not zeros
    (i.e., non-initial entries) plus 1 for the first entry.
    Actually: count ALL non-empty lines in the log, which matches stash push count,
    then subtract drops.

    Better: check refs/stash for the tip hash and walk the stash chain.
    The stash chain: stash@{0} -> stash@{1} -> stash@{2} via parent commits.
    We count by following the parent chain in .git/refs/stash.

    Simplest correct approach: count non-empty lines in stash reflog IF no drops
    occurred, but that fails after drops. Instead, walk the parent chain.
    """
    stash_ref_path = os.path.join(project_dir, '.git', 'refs', 'stash')
    if not os.path.exists(stash_ref_path):
        return 0, []

    try:
        with open(stash_ref_path, 'r') as f:
            tip_hash = f.read().strip()
        if not tip_hash:
            return 0, []
    except Exception:
        return 0, []

    # Walk the commit chain to count stashes and collect their messages
    git_dir = os.path.join(project_dir, '.git')
    stash_messages = []
    current_hash = tip_hash

    for _ in range(20):  # Safety limit — max 20 stashes
        commit_data = read_git_object(git_dir, current_hash)
        if commit_data is None:
            break

        # Extract commit message from the commit object
        if '\n\n' in commit_data:
            msg = commit_data.split('\n\n', 1)[1].strip()
            stash_messages.append(msg)

        # Find the 'parent' lines — for stash commits the first parent is the
        # stash@{n-1} in the chain (the previous stash on the stash stack)
        parents = []
        for line in commit_data.split('\n'):
            if line.startswith('parent '):
                parents.append(line[7:].strip())

        # Stash commits have 2 or 3 parents (index tree, working tree, untracked).
        # The FIRST parent is the base commit (the branch tip), not the stash chain.
        # The stash chain is followed by looking at the SECOND parent only if
        # stash@{n+1} shares the same base. Actually stash is a DAG not a chain.
        #
        # Reliable approach: count by reading the stash reflog after all.
        break  # Fall back to reflog-based counting

    # Fall back to reflog: count lines where old_hash is not zeros
    # (each push adds a line; drops remove entries but also rewrite the log)
    # After a drop, the log is rewritten with one fewer line.
    stash_log_path = os.path.join(project_dir, '.git', 'logs', 'refs', 'stash')
    if not os.path.exists(stash_log_path):
        return 1, stash_messages  # ref exists but no log = 1 stash

    try:
        with open(stash_log_path, 'r') as f:
            log_lines = [l.strip() for l in f.readlines() if l.strip()]
    except Exception:
        return 1, stash_messages

    # Each line in the reflog is one stash. After drops/pops, the reflog
    # is rewritten and only contains the remaining stashes.
    # Parse each line to extract message after the tab character.
    active_messages = []
    for line in log_lines:
        if '\t' in line:
            msg = line.split('\t', 1)[1].strip()
            active_messages.append(msg)

    return len(log_lines), active_messages


def read_git_object(git_dir, obj_hash):
    """
    Read a loose git object by hash. Returns decoded text or None.
    Uses zlib decompression since git objects are zlib-compressed.
    """
    try:
        import zlib
        obj_path = os.path.join(git_dir, 'objects', obj_hash[:2], obj_hash[2:])
        if not os.path.exists(obj_path):
            return None
        with open(obj_path, 'rb') as f:
            compressed = f.read()
        raw = zlib.decompress(compressed)
        # Format: "<type> <size>\0<content>"
        null_idx = raw.index(b'\0')
        content = raw[null_idx + 1:]
        return content.decode('utf-8', errors='replace')
    except Exception:
        return None


def verify_task(project_dir):
    """
    Verify git stash management task completion.

    Expected final state:
    - Exactly 1 stash remaining: 'WIP: file A'
    - file_b.py contains the get_user_by_email function (applied from stash@{1})
    - file_c.py contains the format_response function (popped from stash@{0}='WIP: file C')
    - file_a.py is unmodified (stash 'WIP: file A' was not applied, only preserved)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory must exist and be a git repo
    if not os.path.isdir(project_dir):
        print(f"CRITICAL: Project directory not found: {project_dir}")
        print("REWARD: 0.0")
        return 0.0

    git_dir = os.path.join(project_dir, '.git')
    if not os.path.isdir(git_dir):
        print(f"CRITICAL: Not a git repository: {project_dir}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Exactly 1 stash remaining (0.30 points)
    # In the initial_env: 3 stashes exist. After the task:
    # stash@{1} ('WIP: file B') was applied and then dropped,
    # stash@{0} ('WIP: file C') was popped (applied + dropped),
    # only stash 'WIP: file A' should remain.
    try:
        stash_count, stash_msgs = count_active_stashes(project_dir)
        if stash_count == 1:
            print(f"PASS: Component 1 — Exactly 1 stash remaining (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected 1 stash, found {stash_count}. Messages: {stash_msgs}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check stash count: {e}")
        stash_count, stash_msgs = 0, []

    # Component 2: Remaining stash is 'WIP: file A' (0.20 points)
    # After dropping WIP: file B and popping WIP: file C,
    # only the first-created stash 'WIP: file A' should remain.
    try:
        stash_count, stash_msgs = count_active_stashes(project_dir)
        if stash_count == 1 and any('WIP: file A' in msg for msg in stash_msgs):
            print(f"PASS: Component 2 — Remaining stash is 'WIP: file A' (msgs: {stash_msgs}) (0.20 pts)")
            total_score += 0.20
        elif stash_count == 1:
            print(f"FAIL: Component 2 — Expected 'WIP: file A' stash, found: {stash_msgs}")
        else:
            print(f"FAIL: Component 2 — Cannot verify stash name, stash count is {stash_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check stash name: {e}")

    # Component 3: file_b.py contains get_user_by_email function (0.25 points)
    # stash@{1} was 'WIP: file B' which adds get_user_by_email.
    # After applying stash@{1}, this function should be present in the working tree.
    try:
        file_b_path = os.path.join(project_dir, 'file_b.py')
        with open(file_b_path, 'r') as f:
            content_b = f.read()
        if 'def get_user_by_email' in content_b:
            print(f"PASS: Component 3 — file_b.py contains get_user_by_email function (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — file_b.py does not contain get_user_by_email function")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not read file_b.py: {e}")

    # Component 4: file_c.py contains format_response function (0.25 points)
    # stash@{0} was 'WIP: file C' which adds format_response.
    # After popping stash@{0}, this function should be present in the working tree.
    try:
        file_c_path = os.path.join(project_dir, 'file_c.py')
        with open(file_c_path, 'r') as f:
            content_c = f.read()
        if 'def format_response' in content_c:
            print(f"PASS: Component 4 — file_c.py contains format_response function (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — file_c.py does not contain format_response function")
    except Exception as e:
        print(f"ERROR: Component 4 — Could not read file_c.py: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Run verification
if not os.path.isdir(WORKDIR):
    print(f"Project directory not found: {WORKDIR}")
    print("REWARD: 0.0")
else:
    verify_task(WORKDIR)
