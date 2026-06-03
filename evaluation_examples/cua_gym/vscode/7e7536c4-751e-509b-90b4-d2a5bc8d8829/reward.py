"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve just pulled the latest code and need to start tweaking the UI—could you help me open the /home/user/workspace/frontend folder in VS Code?
Generated: 2025-09-11 13:15:10
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import subprocess
import shlex
import re

"""
Reward Verification Script
Task: "Open the /home/user/workspace/frontend folder in VS Code"

Scoring (progressive):
    0.5 pts – A VS Code process is running
    0.5 pts – One of those VS Code processes was launched with the exact target folder
Returns a float in [0, 1].  Prints step-by-step diagnostics and the final
"REWARD: X.X" line required by the evaluation harness.
"""

def _normalize_path(path: str) -> str:
    """Return an absolute, normalised version of a filesystem path."""
    try:
        return os.path.abspath(os.path.realpath(os.path.expanduser(path.rstrip('/'))))
    except Exception:
        return path.rstrip('/')

def _get_code_processes():
    """Return a list of dicts {pid, args} for running VS Code processes."""
    try:
        ps_output = subprocess.check_output(['ps', '-eo', 'pid,args'], text=True, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"✗ Failed to enumerate processes: {e}")
        return []

    processes = []
    for line in ps_output.splitlines()[1:]:  # skip header
        line = line.strip()
        if not line:
            continue
        pid, *rest = line.split(maxsplit=1)
        args = rest[0] if rest else ''
        # look for the word "code" (covers code, code-oss, etc.) in the exec line
        if re.search(r'\bcode\b', args):
            processes.append({'pid': pid, 'args': args})
    return processes

def verify_task():
    target_path = '/home/user/workspace/frontend'
    norm_target = _normalize_path(target_path)

    total_score = 0.0

    # 1) Is VS Code running?
    code_procs = _get_code_processes()
    if code_procs:
        total_score += 0.5
        print(f"✓ VS Code process(es) found: {[p['pid'] for p in code_procs]} (0.5 points)")
    else:
        print("✗ No VS Code processes found – cannot be editing the folder")
        print("REWARD: 0.0")
        return 0.0  # Early exit – nothing else can succeed

    # 2) Was VS Code launched with the target folder?
    folder_open = False
    for proc in code_procs:
        args_line = proc['args']
        # Tokenise respecting quotes
        try:
            tokens = shlex.split(args_line)
        except ValueError:
            tokens = args_line.split()

        for token in tokens:
            if _normalize_path(token) == norm_target:
                folder_open = True
                print(f"✓ Target folder '{target_path}' open in process {proc['pid']} (0.5 points)")
                break
        if folder_open:
            break

    if folder_open:
        total_score += 0.5
    else:
        print(f"✗ Target folder '{target_path}' is NOT open in any VS Code process")

    final_score = min(total_score, 1.0)
    print(f"REWARD: {final_score}")
    return final_score

if __name__ == '__main__':
    verify_task()
