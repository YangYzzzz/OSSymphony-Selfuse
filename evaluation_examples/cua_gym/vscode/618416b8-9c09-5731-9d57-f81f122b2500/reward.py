"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve separated my project into two folders—/home/user/src for the code and /home/user/tests for the test suite. Could you add both of these directories to my current VS Code workspace?
Generated: 2025-09-11 12:59:22
Status: success
Model: azure-o3
Total Steps: 16
"""

import os
import json
import glob

SRC_DIR = '/home/user/src'
TESTS_DIR = '/home/user/tests'


def _canonicalize(path: str, workspace_file: str) -> str:
    """Convert a folder entry from a VS Code workspace file to an absolute,
    normalised path so comparisons are reliable.
    1. Expands '~'
    2. Resolves relative paths against the workspace file location
    3. Normalises the result (removes .., symlinks, etc.)
    """
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(workspace_file), path)
    return os.path.normpath(os.path.abspath(path))


def _read_workspace_folders(workspace_file: str):
    """Return a list of canonical folder paths declared in the workspace file.
    If the file cannot be parsed or has no valid `folders` section, returns
    None so the caller can skip it.
    """
    try:
        with open(workspace_file, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
    except Exception as exc:
        print(f"  ✗ Could not parse {workspace_file}: {exc}")
        return None

    if not isinstance(data, dict):
        print(f"  ✗ Unexpected structure in {workspace_file}")
        return None

    folders_field = data.get('folders', [])
    canonical_paths = []
    for entry in folders_field:
        if isinstance(entry, dict) and 'path' in entry:
            canonical_paths.append(_canonicalize(entry['path'], workspace_file))
    return canonical_paths


def verify_task() -> float:
    """Verify that the VS Code workspace under /home/user includes BOTH
    /home/user/src and /home/user/tests. Progressive scoring:
      • 0.5 for each directory that EXISTS on disk AND is referenced by at
        least one *.code-workspace file.
      • Returns a float in [0.0, 1.0].
    The function outputs detailed diagnostic information and finally prints
    `REWARD: X.X` where X.X is the computed score.
    """
    print('=== VS Code Workspace Verification ===')

    # Locate workspace files (common root location in these tasks)
    workspace_files = sorted(
        set(glob.glob('/home/user/**/*.code-workspace', recursive=True) +
            glob.glob('/home/user/*.code-workspace'))
    )

    if not workspace_files:
        print('✗ No *.code-workspace files found under /home/user')
    else:
        print(f'Found {len(workspace_files)} workspace file(s):')
        for wf in workspace_files:
            print(f' • {wf}')

    src_in_workspace = False
    tests_in_workspace = False

    for wf in workspace_files:
        folders = _read_workspace_folders(wf)
        if folders is None:
            continue
        print(f'  -> Workspace "{wf}" lists {len(folders)} folder(s):')
        for folder in folders:
            print(f'     - {folder}')
        if SRC_DIR in folders:
            src_in_workspace = True
        if TESTS_DIR in folders:
            tests_in_workspace = True

    # Progressive scoring ----------------------------------------------
    score = 0.0

    # Condition 1: /home/user/src exists AND is referenced
    if os.path.isdir(SRC_DIR) and src_in_workspace:
        print('✓ /home/user/src directory exists and is included (+0.5)')
        score += 0.5
    elif not os.path.isdir(SRC_DIR):
        print('✗ /home/user/src directory does NOT exist')
    else:
        print('✗ /home/user/src is NOT referenced by any workspace file')

    # Condition 2: /home/user/tests exists AND is referenced
    if os.path.isdir(TESTS_DIR) and tests_in_workspace:
        print('✓ /home/user/tests directory exists and is included (+0.5)')
        score += 0.5
    elif not os.path.isdir(TESTS_DIR):
        print('✗ /home/user/tests directory does NOT exist')
    else:
        print('✗ /home/user/tests is NOT referenced by any workspace file')

    final_score = round(min(score, 1.0), 2)
    print(f'Computed score: {final_score}')
    return final_score


if __name__ == '__main__':
    reward = verify_task()
    print(f'REWARD: {reward}')
