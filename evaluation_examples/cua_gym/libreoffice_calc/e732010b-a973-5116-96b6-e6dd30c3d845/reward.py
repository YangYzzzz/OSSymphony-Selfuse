"""
Reward Script: Set up a complete development workspace from scratch.
Task ID: osworld_multi_apps_sys_config_008
Domain: os (system configuration)
Scoring:
  Component 1: Directory structure created (src, tests, docs, scripts) — 0.20 pts
  Component 2: Git repo initialized with user config (Developer / dev@example.com) — 0.20 pts
  Component 3: Python 3.10 venv at .venv/ — 0.20 pts
  Component 4: pytest, black, flake8 installed in venv — 0.20 pts
  Component 5: activate.sh is executable and prints 'Workspace ready' — 0.10 pts
  Component 6: README.txt contains 'MyProject' — 0.10 pts
  Total: 1.0
"""

import os
import stat
import configparser

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_sys_config_008'
PROJECT_DIR = '/home/user/workspace/myproject'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: workspace directory must exist
    if not os.path.isdir('/home/user/workspace'):
        print("CRITICAL: /home/user/workspace does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Directory structure created (0.20 points)
    # Task requires: /home/user/workspace/myproject/{src,tests,docs,scripts}
    try:
        required_dirs = ['src', 'tests', 'docs', 'scripts']
        missing_dirs = []
        for d in required_dirs:
            path = os.path.join(PROJECT_DIR, d)
            if not os.path.isdir(path):
                missing_dirs.append(d)
        if not missing_dirs:
            print(f"PASS: Component 1 — all required directories exist: {required_dirs} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — missing directories in myproject: {missing_dirs}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Git repo initialized with user config (0.20 points)
    # Task requires: git init in /home/user/workspace/myproject/
    # and git config user.name='Developer', user.email='dev@example.com'
    try:
        git_dir = os.path.join(PROJECT_DIR, '.git')
        git_config_path = os.path.join(git_dir, 'config')
        if not os.path.isdir(git_dir):
            print("FAIL: Component 2 — .git directory not found (git not initialized)")
        elif not os.path.isfile(git_config_path):
            print("FAIL: Component 2 — .git/config not found")
        else:
            cfg = configparser.ConfigParser()
            cfg.read(git_config_path)
            name = cfg.get('user', 'name', fallback=None)
            email = cfg.get('user', 'email', fallback=None)
            if name == 'Developer' and email == 'dev@example.com':
                print(f"PASS: Component 2 — git repo initialized with user.name='{name}' user.email='{email}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — git user config mismatch: name='{name}' email='{email}' (expected Developer / dev@example.com)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Python 3.10 venv at .venv/ (0.20 points)
    # Task requires: virtual environment using Python 3.10 at /home/user/workspace/myproject/.venv/
    try:
        venv_dir = os.path.join(PROJECT_DIR, '.venv')
        pyvenv_cfg = os.path.join(venv_dir, 'pyvenv.cfg')
        venv_python = os.path.join(venv_dir, 'bin', 'python3')
        if not os.path.isdir(venv_dir):
            print("FAIL: Component 3 — .venv directory not found")
        elif not os.path.isfile(pyvenv_cfg):
            print("FAIL: Component 3 — pyvenv.cfg not found in .venv/")
        else:
            # Read the pyvenv.cfg to check Python version
            with open(pyvenv_cfg, 'r') as f:
                cfg_content = f.read()
            # Check for 3.10 in the version or version_info lines
            version_ok = any(
                (line.startswith('version') and '3.10' in line)
                for line in cfg_content.splitlines()
            )
            if version_ok and os.path.isfile(venv_python):
                print(f"PASS: Component 3 — Python 3.10 venv found at .venv/ (0.20 pts)")
                total_score += 0.20
            elif not version_ok:
                print(f"FAIL: Component 3 — .venv exists but not Python 3.10 (pyvenv.cfg: {cfg_content.strip()})")
            else:
                print(f"FAIL: Component 3 — .venv/bin/python3 not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: pytest, black, flake8 installed in venv (0.20 points)
    # Task requires: all 3 packages installed into the venv
    try:
        venv_dir = os.path.join(PROJECT_DIR, '.venv')
        site_packages = os.path.join(venv_dir, 'lib', 'python3.10', 'site-packages')
        if not os.path.isdir(site_packages):
            print(f"FAIL: Component 4 — site-packages directory not found at {site_packages}")
        else:
            packages = os.listdir(site_packages)
            has_pytest = any(p.startswith('pytest') or p == '_pytest' for p in packages)
            has_black = any(p.startswith('black') and not p.startswith('blackd') for p in packages)
            has_flake8 = any(p.startswith('flake8') for p in packages)

            missing = []
            if not has_pytest:
                missing.append('pytest')
            if not has_black:
                missing.append('black')
            if not has_flake8:
                missing.append('flake8')

            if not missing:
                print(f"PASS: Component 4 — pytest, black, flake8 all installed in venv (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — missing packages in venv: {missing}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: activate.sh is executable and contains 'Workspace ready' echo (0.10 points)
    # Task requires: activate.sh at project root, executable, prints "Workspace ready"
    try:
        activate_path = os.path.join(PROJECT_DIR, 'activate.sh')
        if not os.path.isfile(activate_path):
            print(f"FAIL: Component 5 — activate.sh not found at {activate_path}")
        else:
            file_stat = os.stat(activate_path)
            is_executable = bool(stat.S_IMODE(file_stat.st_mode) & 0o111)
            if not is_executable:
                print(f"FAIL: Component 5 — activate.sh is not executable (mode: {oct(stat.S_IMODE(file_stat.st_mode))})")
            else:
                # Check that activate.sh content includes the 'Workspace ready' echo
                with open(activate_path, 'r') as f:
                    content = f.read()
                if 'Workspace ready' in content:
                    print(f"PASS: Component 5 — activate.sh is executable and contains 'Workspace ready' (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 5 — activate.sh is executable but does not contain 'Workspace ready': {repr(content)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: README.txt contains 'MyProject' (0.10 points)
    # Task requires: README.txt with project name 'MyProject'
    try:
        readme_path = os.path.join(PROJECT_DIR, 'README.txt')
        if not os.path.isfile(readme_path):
            print(f"FAIL: Component 6 — README.txt not found at {readme_path}")
        else:
            with open(readme_path, 'r') as f:
                content = f.read()
            if 'MyProject' in content:
                print(f"PASS: Component 6 — README.txt contains 'MyProject' (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — README.txt does not contain 'MyProject' (content: {repr(content)})")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
