"""
Reward Script: Environment-specific VSCode configuration
Task ID: vscode_wf_052
Domain: vscode
Scoring:
  C1 (0.25): Three .env files with environment-specific DATABASE_URL and API_KEY
  C2 (0.15): .env.example with placeholder values
  C3 (0.15): mikestead.dotenv extension installed
  C4 (0.25): launch.json has 3 configs each with correct envFile
  C5 (0.20): .gitignore has .env* and !.env.example
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_052'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---------------------------------------------------------------
    # Component 1: Three .env files with different DATABASE_URL and API_KEY (0.25 pts)
    # Each env file must exist and contain environment-specific values.
    # This FAILS on initial (no .env files) and PASSES on golden.
    # ---------------------------------------------------------------
    try:
        env_files = {
            'development': os.path.join(PROJECT, '.env.development'),
            'staging':     os.path.join(PROJECT, '.env.staging'),
            'production':  os.path.join(PROJECT, '.env.production'),
        }
        env_contents = {}
        missing_files = [name for name, path in env_files.items() if not os.path.isfile(path)]
        if missing_files:
            print(f"FAIL: C1 - Missing .env files for: {missing_files}")
        else:
            for env_name, path in env_files.items():
                with open(path, 'r') as f:
                    env_contents[env_name] = f.read()

            # Each file must have DATABASE_URL and API_KEY, and they must differ across envs
            db_urls = set()
            api_keys = set()
            missing_vars = []
            for env_name, content in env_contents.items():
                db_match = re.search(r'^DATABASE_URL=(.+)$', content, re.MULTILINE)
                ak_match = re.search(r'^API_KEY=(.+)$', content, re.MULTILINE)
                if not db_match or not ak_match:
                    missing_vars.append(env_name)
                else:
                    db_urls.add(db_match.group(1).strip())
                    api_keys.add(ak_match.group(1).strip())

            if missing_vars:
                print(f"FAIL: C1 - Missing DATABASE_URL or API_KEY in: {missing_vars}")
            elif len(db_urls) == 3 and len(api_keys) == 3:
                print(f"PASS: C1 - All 3 .env files have unique DATABASE_URL and API_KEY (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: C1 - DATABASE_URL unique count={len(db_urls)}, API_KEY unique count={len(api_keys)} (expected 3 each)")
    except Exception as e:
        print(f"ERROR: C1 - {e}")

    # ---------------------------------------------------------------
    # Component 2: .env.example with placeholder values (0.15 pts)
    # Must exist and contain placeholder-style values (not real secrets).
    # This FAILS on initial (no .env.example) and PASSES on golden.
    # ---------------------------------------------------------------
    try:
        example_path = os.path.join(PROJECT, '.env.example')
        if os.path.isfile(example_path):
            with open(example_path, 'r') as f:
                example_content = f.read()
            # Must have DATABASE_URL and API_KEY with placeholder-looking values
            has_db = re.search(r'^DATABASE_URL=', example_content, re.MULTILINE)
            has_ak = re.search(r'^API_KEY=', example_content, re.MULTILINE)
            if has_db and has_ak:
                # Ensure at least one placeholder indicator (e.g., "your-", "placeholder", "example", generic user/pass)
                placeholder_indicators = ['your-', 'placeholder', 'example', 'user:password', 'your_', 'change-me', 'xxx', 'here']
                content_lower = example_content.lower()
                has_placeholder = any(ind in content_lower for ind in placeholder_indicators)
                if has_placeholder:
                    print(f"PASS: C2 - .env.example exists with placeholder values (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: C2 - .env.example exists but values don't look like placeholders")
            else:
                print(f"FAIL: C2 - .env.example missing DATABASE_URL or API_KEY")
        else:
            print(f"FAIL: C2 - .env.example does not exist")
    except Exception as e:
        print(f"ERROR: C2 - {e}")

    # ---------------------------------------------------------------
    # Component 3: DotENV extension (mikestead.dotenv) installed (0.15 pts)
    # Check by scanning ~/.vscode/extensions/ directory for the extension folder.
    # This FAILS on initial (not installed) and PASSES on golden.
    # ---------------------------------------------------------------
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        if os.path.isdir(ext_dir):
            ext_folders = os.listdir(ext_dir)
            found = any('mikestead.dotenv' in folder.lower() for folder in ext_folders)
            if found:
                print(f"PASS: C3 - mikestead.dotenv extension is installed (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: C3 - mikestead.dotenv not found in extensions dir: {ext_folders}")
        else:
            print(f"FAIL: C3 - Extensions directory {ext_dir} does not exist")
    except Exception as e:
        print(f"ERROR: C3 - {e}")

    # ---------------------------------------------------------------
    # Component 4: launch.json has 3 configs with correct envFile (0.25 pts)
    # Each config must reference its respective .env file.
    # This FAILS on initial (no .vscode/launch.json) and PASSES on golden.
    # ---------------------------------------------------------------
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if os.path.isfile(launch_path):
            with open(launch_path, 'r') as f:
                raw = f.read()
            # Strip comments (JSONC support)
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            launch = json.loads(cleaned)

            configs = launch.get('configurations', [])
            if len(configs) >= 3:
                # Check that each of the 3 env files is referenced by at least one config
                expected_envs = {'.env.development', '.env.staging', '.env.production'}
                found_envs = set()
                for cfg in configs:
                    env_file = cfg.get('envFile', '')
                    for expected in expected_envs:
                        if expected in env_file:
                            found_envs.add(expected)

                if found_envs == expected_envs:
                    print(f"PASS: C4 - launch.json has 3+ configs referencing all 3 .env files (0.25 pts)")
                    total_score += 0.25
                else:
                    missing = expected_envs - found_envs
                    print(f"FAIL: C4 - launch.json missing envFile references for: {missing}")
            else:
                print(f"FAIL: C4 - launch.json has {len(configs)} configurations (expected >= 3)")
        else:
            print(f"FAIL: C4 - {launch_path} does not exist")
    except Exception as e:
        print(f"ERROR: C4 - {e}")

    # ---------------------------------------------------------------
    # Component 5: .gitignore has .env* and !.env.example (0.20 pts)
    # The gitignore must exclude .env* but allow .env.example.
    # This FAILS on initial (no .env* pattern) and PASSES on golden.
    # ---------------------------------------------------------------
    try:
        gitignore_path = os.path.join(PROJECT, '.gitignore')
        if os.path.isfile(gitignore_path):
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
            lines = [l.strip() for l in gitignore_content.splitlines()]

            has_env_star = any(l == '.env*' or l == '.env.*' for l in lines)
            has_example_exception = any(l == '!.env.example' for l in lines)

            if has_env_star and has_example_exception:
                print(f"PASS: C5 - .gitignore has .env* and !.env.example (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: C5 - .gitignore missing patterns: .env*={has_env_star}, !.env.example={has_example_exception}")
        else:
            print(f"FAIL: C5 - .gitignore does not exist")
    except Exception as e:
        print(f"ERROR: C5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
