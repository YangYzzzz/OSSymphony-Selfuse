"""
Reward Script: Install Terraform binary and ensure it persists across shell sessions
Task ID: osworld_multi_apps_cli_path_fix_011
Domain: os (CLI/PATH management)
Scoring:
  - Component 1: Terraform binary exists at /usr/local/bin or ~/bin (0.4 pts)
  - Component 2: Terraform binary is executable and 'terraform version' succeeds (0.3 pts)
  - Component 3: PATH is updated in ~/.bashrc to persist terraform across sessions (0.3 pts)
"""

import os
import stat

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_cli_path_fix_011'

# Candidate install locations per task spec
TERRAFORM_CANDIDATES = [
    '/usr/local/bin/terraform',
    '/home/user/bin/terraform',
    os.path.expanduser('~/bin/terraform'),
]

BASHRC_PATH = '/home/user/.bashrc'


def run_command(cmd):
    """Run a shell command and return (returncode, stdout, stderr)."""
    import shlex
    try:
        # Use os.popen-style execution without subprocess module
        read_fd, write_fd = os.pipe()
        err_read_fd, err_write_fd = os.pipe()
        pid = os.fork()
        if pid == 0:
            # Child process
            os.close(read_fd)
            os.close(err_read_fd)
            os.dup2(write_fd, 1)
            os.dup2(err_write_fd, 2)
            os.close(write_fd)
            os.close(err_write_fd)
            args = shlex.split(cmd)
            os.execvp(args[0], args)
            os._exit(127)
        else:
            # Parent process
            os.close(write_fd)
            os.close(err_write_fd)
            stdout_data = b''
            stderr_data = b''
            while True:
                chunk = os.read(read_fd, 4096)
                if not chunk:
                    break
                stdout_data += chunk
            os.close(read_fd)
            while True:
                chunk = os.read(err_read_fd, 4096)
                if not chunk:
                    break
                stderr_data += chunk
            os.close(err_read_fd)
            _, status = os.waitpid(pid, 0)
            returncode = os.WEXITSTATUS(status)
            return returncode, stdout_data.decode('utf-8', errors='replace'), stderr_data.decode('utf-8', errors='replace')
    except Exception as e:
        return -1, '', str(e)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    terraform_path = None

    # Component 1: Terraform binary exists at /usr/local/bin or ~/bin (0.4 points)
    # This FAILS on initial_env (no binary) and PASSES on golden_env (binary present)
    try:
        found_path = None
        for candidate in TERRAFORM_CANDIDATES:
            if os.path.isfile(candidate):
                found_path = candidate
                break

        if found_path:
            terraform_path = found_path
            print(f"PASS: Component 1 — terraform binary found at {found_path} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — terraform binary not found in any expected location: {TERRAFORM_CANDIDATES}")
    except Exception as e:
        print(f"ERROR: Component 1 — could not check binary existence: {e}")

    # Component 2: Binary is executable and 'terraform version' succeeds (0.3 points)
    # This FAILS on initial_env (no binary) and PASSES on golden_env (binary present and executable)
    try:
        if terraform_path is None:
            print("FAIL: Component 2 — skipped, no binary found in Component 1")
        else:
            # Check executable bit
            file_stat = os.stat(terraform_path)
            is_executable = bool(stat.S_IMODE(file_stat.st_mode) & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))

            if not is_executable:
                print(f"FAIL: Component 2 — terraform at {terraform_path} is not executable (mode: {oct(stat.S_IMODE(file_stat.st_mode))})")
            else:
                # Run terraform version to verify it executes successfully (using os-level fork/exec)
                rc, stdout, stderr = run_command(f"{terraform_path} version")
                output = stdout + stderr
                if rc == 0 and 'Terraform' in output:
                    version_line = output.strip().splitlines()[0] if output.strip() else '(no output)'
                    print(f"PASS: Component 2 — terraform version succeeded: {version_line} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — terraform version failed (rc={rc}), output: {output[:200]}")
    except Exception as e:
        print(f"ERROR: Component 2 — could not verify terraform execution: {e}")

    # Component 3: PATH updated in ~/.bashrc for persistence across shell sessions (0.3 points)
    # This FAILS on initial_env (no PATH line) and PASSES on golden_env (PATH line present)
    try:
        if not os.path.isfile(BASHRC_PATH):
            print(f"FAIL: Component 3 — {BASHRC_PATH} does not exist")
        else:
            with open(BASHRC_PATH, 'r') as f:
                bashrc_content = f.read()

            # Check that bashrc exports a PATH that includes a directory where terraform lives
            # Look for export PATH patterns that add /usr/local/bin or ~/bin or /home/user/bin
            path_patterns = [
                '/usr/local/bin',
                '/home/user/bin',
                '~/bin',
                '$HOME/bin',
            ]

            # Find any line with 'export PATH' that also contains a valid terraform directory
            matching_pattern = next(
                (
                    line.strip()
                    for line in bashrc_content.splitlines()
                    if 'export PATH' in line and any(pat in line for pat in path_patterns)
                ),
                None,
            )

            if matching_pattern is not None:
                print(f"PASS: Component 3 — PATH export found in .bashrc: '{matching_pattern}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — no PATH export for terraform directory found in .bashrc")
                print(f"  Searched for patterns: {path_patterns}")
                # Show relevant lines for debugging
                path_lines = [l for l in bashrc_content.splitlines() if 'PATH' in l or 'terraform' in l.lower()]
                if path_lines:
                    print(f"  PATH-related lines in .bashrc: {path_lines}")
    except Exception as e:
        print(f"ERROR: Component 3 — could not verify .bashrc PATH: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
