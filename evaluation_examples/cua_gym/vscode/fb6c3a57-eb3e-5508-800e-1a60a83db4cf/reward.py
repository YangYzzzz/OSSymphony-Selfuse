"""
Reward Script: Project scaffolding with directories and config files
Task ID: vscode_lp_082
Domain: vscode
Scoring:
  Component 1 (0.30): All 4 directories exist (src/, tests/, docs/, configs/)
  Component 2 (0.25): setup.py exists with setuptools configuration
  Component 3 (0.15): requirements.txt exists with content
  Component 4 (0.30): .gitignore exists with Python-specific patterns
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_082'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'newlib')


def verify_task(project_dir):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: All 4 required directories exist (0.30 points)
    # Each directory is worth 0.075 points for partial credit
    try:
        required_dirs = ['src', 'tests', 'docs', 'configs']
        dirs_found = 0
        for d in required_dirs:
            dir_path = os.path.join(project_dir, d)
            if os.path.isdir(dir_path):
                dirs_found += 1
                print(f"PASS: Directory '{d}/' exists")
            else:
                print(f"FAIL: Directory '{d}/' not found")

        if dirs_found == len(required_dirs):
            print(f"PASS: Component 1 -- All {len(required_dirs)} directories exist (0.30 pts)")
            total_score += 0.30
        elif dirs_found > 0:
            partial = round(0.30 * dirs_found / len(required_dirs), 2)
            print(f"PARTIAL: Component 1 -- {dirs_found}/{len(required_dirs)} directories exist ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No required directories found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: setup.py exists with setuptools configuration (0.25 points)
    try:
        setup_path = os.path.join(project_dir, 'setup.py')
        if os.path.isfile(setup_path):
            with open(setup_path, 'r') as f:
                content = f.read()

            has_setuptools_import = 'setuptools' in content or 'from setuptools' in content
            has_setup_call = 'setup(' in content
            has_name = 'name=' in content or 'name =' in content

            if has_setuptools_import and has_setup_call and has_name:
                print(f"PASS: Component 2 -- setup.py has setuptools config (0.25 pts)")
                total_score += 0.25
            elif has_setup_call:
                # Has a setup() call but missing some elements
                print(f"PARTIAL: Component 2 -- setup.py has setup() but incomplete config (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- setup.py exists but lacks setuptools configuration")
        else:
            print(f"FAIL: Component 2 -- setup.py not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: requirements.txt exists (0.15 points)
    try:
        req_path = os.path.join(project_dir, 'requirements.txt')
        if os.path.isfile(req_path):
            with open(req_path, 'r') as f:
                content = f.read().strip()
            # File exists -- task says "can be empty or have common packages listed"
            # Award full points if file exists (content is optional per task spec)
            if len(content) > 0:
                print(f"PASS: Component 3 -- requirements.txt exists with content (0.15 pts)")
                total_score += 0.15
            elif len(content) == 0:
                print(f"PASS: Component 3 -- requirements.txt exists (empty, allowed by task) (0.15 pts)")
                total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- requirements.txt not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: .gitignore exists with Python-specific patterns (0.30 points)
    # Required patterns: __pycache__, *.pyc, .env, venv/
    try:
        gitignore_path = os.path.join(project_dir, '.gitignore')
        if os.path.isfile(gitignore_path):
            with open(gitignore_path, 'r') as f:
                content = f.read()

            required_patterns = {
                '__pycache__': '__pycache__' in content,
                '*.pyc': '*.pyc' in content or '*.py[cod]' in content,
                '.env': '.env' in content,
                'venv/': 'venv' in content,
            }

            patterns_found = sum(1 for v in required_patterns.values() if v)
            total_patterns = len(required_patterns)

            for pattern, found in required_patterns.items():
                if found:
                    print(f"  PASS: .gitignore contains pattern for '{pattern}'")
                else:
                    print(f"  FAIL: .gitignore missing pattern for '{pattern}'")

            if patterns_found == total_patterns:
                print(f"PASS: Component 4 -- .gitignore has all Python patterns (0.30 pts)")
                total_score += 0.30
            elif patterns_found > 0:
                partial = round(0.30 * patterns_found / total_patterns, 2)
                print(f"PARTIAL: Component 4 -- .gitignore has {patterns_found}/{total_patterns} patterns ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 -- .gitignore exists but has no Python patterns")
        else:
            print(f"FAIL: Component 4 -- .gitignore not found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical project path
if not os.path.isdir(PROJECT_DIR):
    print(f"Project directory not found: {PROJECT_DIR}")
    print("REWARD: 0.0")
else:
    verify_task(PROJECT_DIR)
