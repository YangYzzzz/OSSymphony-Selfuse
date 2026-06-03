"""
Initial Setup: Branch comparison workflow - create base project with git repo
Task ID: vscode_git_063
Domain: vs_code

Creates /home/user/project as a git repo on main branch with algorithm.py (base implementation).
No feature branches are created - the agent must create them.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_063'
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
    """Run a shell command, optionally in a given directory."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    if check and result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        raise RuntimeError(f"Command failed with exit code {result.returncode}")
    return result


def create_initial():
    # Clean up any existing project
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)

    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- Create algorithm.py with realistic base implementation ---
    algorithm_py = '''\
"""
Algorithm module for data processing utilities.
Provides functions for searching and sorting operations.
"""


def binary_search(arr, target):
    """
    Search for target in a sorted array.
    Returns the index of target if found, otherwise -1.
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def compute_fibonacci(n):
    """
    Compute the nth Fibonacci number.
    Base implementation using a simple loop.
    n must be a non-negative integer.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def flatten_list(nested):
    """
    Flatten a nested list structure into a single list.
    Base implementation.
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


if __name__ == "__main__":
    # Quick smoke tests
    arr = [1, 3, 5, 7, 9, 11, 13]
    print(f"binary_search([1..13], 7) = {binary_search(arr, 7)}")
    print(f"compute_fibonacci(10) = {compute_fibonacci(10)}")
    print(f"flatten_list([[1,2],[3,[4,5]]]) = {flatten_list([[1, 2], [3, [4, 5]]])}")
'''

    # --- Create README.md ---
    readme_md = '''\
# Project: Algorithm Utilities

A collection of algorithm implementations for data processing tasks.

## Modules

### algorithm.py
- `binary_search(arr, target)`: Efficient search in sorted arrays
- `compute_fibonacci(n)`: Compute nth Fibonacci number
- `flatten_list(nested)`: Flatten nested list structures

## Usage

```python
from algorithm import binary_search, compute_fibonacci, flatten_list

result = binary_search([1, 3, 5, 7, 9], 5)  # returns 2
fib = compute_fibonacci(10)                   # returns 55
flat = flatten_list([[1, 2], [3, [4, 5]]])   # returns [1, 2, 3, 4, 5]
```

## Development

Branch naming convention:
- `feature/approach-a`: Alternative implementation A
- `feature/approach-b`: Alternative implementation B
'''

    # --- Create tests/test_algorithm.py ---
    test_py = '''\
"""
Unit tests for algorithm.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithm import binary_search, compute_fibonacci, flatten_list


def test_binary_search():
    arr = [1, 3, 5, 7, 9, 11, 13]
    assert binary_search(arr, 7) == 3
    assert binary_search(arr, 1) == 0
    assert binary_search(arr, 13) == 6
    assert binary_search(arr, 6) == -1
    print("binary_search tests passed")


def test_fibonacci():
    assert compute_fibonacci(0) == 0
    assert compute_fibonacci(1) == 1
    assert compute_fibonacci(10) == 55
    assert compute_fibonacci(15) == 610
    print("fibonacci tests passed")


def test_flatten():
    assert flatten_list([[1, 2], [3, [4, 5]]]) == [1, 2, 3, 4, 5]
    assert flatten_list([]) == []
    assert flatten_list([[1], [2], [3]]) == [1, 2, 3]
    print("flatten tests passed")


if __name__ == "__main__":
    test_binary_search()
    test_fibonacci()
    test_flatten()
    print("All tests passed!")
'''

    # Write files to project directory
    with open(os.path.join(PROJECT_DIR, 'algorithm.py'), 'w') as f:
        f.write(algorithm_py)
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_md)

    tests_dir = os.path.join(PROJECT_DIR, 'tests')
    os.makedirs(tests_dir, exist_ok=True)
    with open(os.path.join(tests_dir, 'test_algorithm.py'), 'w') as f:
        f.write(test_py)

    # Create an empty __init__.py for tests package
    with open(os.path.join(tests_dir, '__init__.py'), 'w') as f:
        f.write('')

    print(f'Project files created in {PROJECT_DIR}')

    # --- Initialize git repository ---
    run_cmd('git init', cwd=PROJECT_DIR)
    run_cmd('git config user.email "dev@example.com"', cwd=PROJECT_DIR)
    run_cmd('git config user.name "Dev User"', cwd=PROJECT_DIR)
    run_cmd('git add .', cwd=PROJECT_DIR)
    run_cmd('git commit -m "Initial commit: add algorithm utilities"', cwd=PROJECT_DIR)

    # Ensure we're on main branch
    result = run_cmd('git branch --show-current', cwd=PROJECT_DIR, check=False)
    current_branch = result.stdout.strip()
    if current_branch != 'main':
        run_cmd('git branch -M main', cwd=PROJECT_DIR)

    print('Git repository initialized with initial commit on main branch')

    # Verify no feature branches exist
    result = run_cmd('git branch', cwd=PROJECT_DIR)
    print(f'Branches in repo: {result.stdout.strip()}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')


create_initial()
