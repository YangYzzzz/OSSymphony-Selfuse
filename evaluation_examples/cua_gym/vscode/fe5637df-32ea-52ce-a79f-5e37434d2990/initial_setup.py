"""
Initial Setup: Three untracked Python files in a git repository
Task ID: vscode_git_043
Domain: vs_code (git operations)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_043'
PROJECT_DIR = f'{WORKDIR}/project'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def run_cmd(cmd, cwd=None, check=True):
    """Run a shell command, returning stdout."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    if check and result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(f"  stdout: {result.stdout}")
        print(f"  stderr: {result.stderr}")
    return result


def create_initial():
    # ------------------------------------------------------------------ #
    # 1. Remove any existing project directory and recreate clean
    # ------------------------------------------------------------------ #
    run_cmd(f'rm -rf "{PROJECT_DIR}"', check=False)
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # ------------------------------------------------------------------ #
    # 2. Initialize git repository with user identity
    # ------------------------------------------------------------------ #
    run_cmd('git init', cwd=PROJECT_DIR)
    run_cmd('git config user.email "user@example.com"', cwd=PROJECT_DIR)
    run_cmd('git config user.name "User"', cwd=PROJECT_DIR)

    # ------------------------------------------------------------------ #
    # 3. Create initial commit with README so repo is not empty
    # ------------------------------------------------------------------ #
    readme_content = (
        "# Project\n\n"
        "This project demonstrates feature development with Git version control.\n\n"
        "## Structure\n\n"
        "- `feature_a.py` — Feature A implementation\n"
        "- `feature_b.py` — Feature B implementation\n"
        "- `feature_c.py` — Feature C implementation\n"
    )
    readme_path = os.path.join(PROJECT_DIR, 'README.md')
    with open(readme_path, 'w') as f:
        f.write(readme_content)

    run_cmd('git add README.md', cwd=PROJECT_DIR)
    run_cmd('git commit -m "Initial commit: add project README"', cwd=PROJECT_DIR)

    # ------------------------------------------------------------------ #
    # 4. Create three untracked feature files (NOT staged, NOT committed)
    # ------------------------------------------------------------------ #
    feature_a_content = '''\
"""
Feature A: Data validation utilities for user input processing.
"""


def validate_email(email: str) -> bool:
    """Validate that the given string is a properly formatted email address."""
    import re
    pattern = r"^[\\w.+-]+@[\\w-]+\\.[\\w.-]+$"
    return bool(re.match(pattern, email))


def validate_age(age) -> bool:
    """Return True if age is an integer between 0 and 150."""
    try:
        age = int(age)
        return 0 <= age <= 150
    except (ValueError, TypeError):
        return False


def sanitize_input(text: str, max_length: int = 255) -> str:
    """Strip whitespace and truncate input to max_length characters."""
    return text.strip()[:max_length]


if __name__ == "__main__":
    print("Feature A: Input validation utilities loaded.")
    print(f"  validate_email('alice@example.com') = {validate_email('alice@example.com')}")
    print(f"  validate_age(25) = {validate_age(25)}")
    print(f"  sanitize_input('  hello  ') = '{sanitize_input('  hello  ')}'")
'''

    feature_b_content = '''\
"""
Feature B: File processing utilities for batch operations.
"""

import os
import hashlib


def list_files(directory: str, extension: str = None):
    """Return a sorted list of files in directory, optionally filtered by extension."""
    entries = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            if extension is None or name.endswith(extension):
                entries.append(name)
    return sorted(entries)


def compute_checksum(filepath: str) -> str:
    """Compute the SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def count_lines(filepath: str) -> int:
    """Count the number of lines in a text file."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for _ in f)


if __name__ == "__main__":
    print("Feature B: File processing utilities loaded.")
    cwd = os.getcwd()
    files = list_files(cwd, ".py")
    print(f"  Python files in current directory: {files}")
'''

    feature_c_content = '''\
"""
Feature C: Report generation utilities for summarising project metrics.
"""

import datetime


def generate_header(project_name: str, author: str) -> str:
    """Generate a standard report header string."""
    date_str = datetime.date.today().isoformat()
    return (
        f"=" * 60 + "\\n"
        f"Project: {project_name}\\n"
        f"Author : {author}\\n"
        f"Date   : {date_str}\\n"
        f"=" * 60
    )


def summarise_stats(stats: dict) -> str:
    """Format a dictionary of statistics into a readable summary."""
    lines = ["Statistics Summary:", "-" * 40]
    for key, value in sorted(stats.items()):
        lines.append(f"  {key:<25}: {value}")
    lines.append("-" * 40)
    return "\\n".join(lines)


def save_report(content: str, filepath: str) -> None:
    """Write report content to the specified file."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Report saved to {filepath}")


if __name__ == "__main__":
    print("Feature C: Report generation utilities loaded.")
    header = generate_header("My Project", "Dev Team")
    print(header)
    stats = {"total_files": 3, "total_lines": 120, "features_implemented": 3}
    print(summarise_stats(stats))
'''

    for fname, content in [
        ('feature_a.py', feature_a_content),
        ('feature_b.py', feature_b_content),
        ('feature_c.py', feature_c_content),
    ]:
        path = os.path.join(PROJECT_DIR, fname)
        with open(path, 'w') as f:
            f.write(content)
        print(f"Created untracked file: {path}")

    # ------------------------------------------------------------------ #
    # 5. Verify git status shows three untracked files
    # ------------------------------------------------------------------ #
    result = run_cmd('git status', cwd=PROJECT_DIR)
    print(f"\nGit status:\n{result.stdout}")

    # ------------------------------------------------------------------ #
    # 6. GUI-ready startup: open VSCode with the project folder
    # ------------------------------------------------------------------ #
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')


create_initial()
