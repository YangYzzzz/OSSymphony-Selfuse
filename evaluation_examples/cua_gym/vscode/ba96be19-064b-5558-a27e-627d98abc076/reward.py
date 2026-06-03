"""
Reward Script: Node.js project scaffolding in VSCode
Task ID: vscode_gf6_002
Domain: vscode
Scoring:
  Component 1: Project file structure (0.25)
  Component 2: package.json dependencies (0.25)
  Component 3: package.json scripts (0.15)
  Component 4: .env.example entries (0.10)
  Component 5: .gitignore entries (0.10)
  Component 6: .vscode/launch.json config (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_002'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'node-scaffold')


def verify_task(project_dir):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Project file structure exists (0.25 points)
    # All required source files must exist
    try:
        required_files = [
            'src/index.js',
            'src/routes/api.js',
            'src/middleware/auth.js',
            'src/utils/logger.js',
            'test/api.test.js',
        ]
        existing = 0
        for f in required_files:
            fpath = os.path.join(project_dir, f)
            if os.path.isfile(fpath):
                existing += 1
                print(f"  FOUND: {f}")
            else:
                print(f"  MISSING: {f}")

        if existing == len(required_files):
            print(f"PASS: Component 1 — All {len(required_files)} source files exist (0.25 pts)")
            total_score += 0.25
        elif existing > 0:
            partial = round(0.25 * existing / len(required_files), 3)
            print(f"PARTIAL: Component 1 — {existing}/{len(required_files)} source files exist ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No source files found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: package.json dependencies (0.25 points)
    # express, dotenv, winston in dependencies; jest, supertest in devDependencies
    try:
        pkg_path = os.path.join(project_dir, 'package.json')
        if not os.path.isfile(pkg_path):
            print("FAIL: Component 2 — package.json not found")
        else:
            with open(pkg_path, 'r') as f:
                pkg = json.load(f)

            deps = pkg.get('dependencies', {})
            dev_deps = pkg.get('devDependencies', {})

            required_deps = ['express', 'dotenv', 'winston']
            required_dev_deps = ['jest', 'supertest']

            deps_found = sum(1 for d in required_deps if d in deps)
            dev_deps_found = sum(1 for d in required_dev_deps if d in dev_deps)

            total_dep_checks = len(required_deps) + len(required_dev_deps)
            found_total = deps_found + dev_deps_found

            for d in required_deps:
                status = "present" if d in deps else "MISSING"
                print(f"  dependencies.{d}: {status}")
            for d in required_dev_deps:
                status = "present" if d in dev_deps else "MISSING"
                print(f"  devDependencies.{d}: {status}")

            if found_total == total_dep_checks:
                print(f"PASS: Component 2 — All dependencies correct (0.25 pts)")
                total_score += 0.25
            elif found_total > 0:
                partial = round(0.25 * found_total / total_dep_checks, 3)
                print(f"PARTIAL: Component 2 — {found_total}/{total_dep_checks} deps found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — No expected dependencies found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: package.json scripts (0.15 points)
    # start: 'node src/index.js', test: 'jest', dev: 'nodemon src/index.js'
    try:
        pkg_path = os.path.join(project_dir, 'package.json')
        if not os.path.isfile(pkg_path):
            print("FAIL: Component 3 — package.json not found")
        else:
            with open(pkg_path, 'r') as f:
                pkg = json.load(f)

            scripts = pkg.get('scripts', {})
            expected_scripts = {
                'start': 'node src/index.js',
                'test': 'jest',
                'dev': 'nodemon src/index.js',
            }

            matched = 0
            for name, expected_val in expected_scripts.items():
                actual_val = scripts.get(name, '')
                if actual_val == expected_val:
                    matched += 1
                    print(f"  scripts.{name}: '{actual_val}' == '{expected_val}'")
                else:
                    print(f"  scripts.{name}: '{actual_val}' != expected '{expected_val}'")

            if matched == len(expected_scripts):
                print(f"PASS: Component 3 — All scripts correct (0.15 pts)")
                total_score += 0.15
            elif matched > 0:
                partial = round(0.15 * matched / len(expected_scripts), 3)
                print(f"PARTIAL: Component 3 — {matched}/{len(expected_scripts)} scripts correct ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No expected scripts found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: .env.example entries (0.10 points)
    # Must contain PORT=3000, NODE_ENV=development, JWT_SECRET=changeme
    try:
        env_path = os.path.join(project_dir, '.env.example')
        if not os.path.isfile(env_path):
            print("FAIL: Component 4 — .env.example not found")
        else:
            with open(env_path, 'r') as f:
                env_content = f.read()

            required_entries = {
                'PORT': '3000',
                'NODE_ENV': 'development',
                'JWT_SECRET': 'changeme',
            }

            found_entries = 0
            for key, val in required_entries.items():
                # Match KEY=VALUE pattern, allowing spaces around =
                pattern = rf'^{re.escape(key)}\s*=\s*{re.escape(val)}\s*$'
                if re.search(pattern, env_content, re.MULTILINE):
                    found_entries += 1
                    print(f"  {key}={val}: found")
                else:
                    print(f"  {key}={val}: MISSING")

            if found_entries == len(required_entries):
                print(f"PASS: Component 4 — .env.example correct (0.10 pts)")
                total_score += 0.10
            elif found_entries > 0:
                partial = round(0.10 * found_entries / len(required_entries), 3)
                print(f"PARTIAL: Component 4 — {found_entries}/{len(required_entries)} entries found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — No expected entries found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: .gitignore entries (0.10 points)
    # Must contain node_modules and .env
    try:
        gi_path = os.path.join(project_dir, '.gitignore')
        if not os.path.isfile(gi_path):
            print("FAIL: Component 5 — .gitignore not found")
        else:
            with open(gi_path, 'r') as f:
                gi_content = f.read()

            # Check for node_modules and .env lines
            gi_lines = [line.strip() for line in gi_content.splitlines()]

            has_node_modules = any('node_modules' in line for line in gi_lines)
            has_dot_env = any(line == '.env' or line.startswith('.env') for line in gi_lines)

            print(f"  node_modules in .gitignore: {has_node_modules}")
            print(f"  .env in .gitignore: {has_dot_env}")

            if has_node_modules and has_dot_env:
                print(f"PASS: Component 5 — .gitignore correct (0.10 pts)")
                total_score += 0.10
            elif has_node_modules or has_dot_env:
                print(f"PARTIAL: Component 5 — 1/2 entries found (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 5 — .gitignore missing required entries")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/launch.json with Node.js debug config (0.15 points)
    # Must have type: 'node', and program pointing to src/index.js
    try:
        launch_path = os.path.join(project_dir, '.vscode', 'launch.json')
        if not os.path.isfile(launch_path):
            print("FAIL: Component 6 — .vscode/launch.json not found")
        else:
            with open(launch_path, 'r') as f:
                content = f.read()
            # Handle JSONC (strip comments)
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            launch = json.loads(cleaned)

            configs = launch.get('configurations', [])
            node_config_found = False
            points_to_index = False

            for cfg in configs:
                if cfg.get('type') == 'node':
                    node_config_found = True
                    program = cfg.get('program', '')
                    # Check if program points to src/index.js
                    if 'src/index.js' in program:
                        points_to_index = True
                    print(f"  Node config found, program: '{program}'")

            if node_config_found and points_to_index:
                print(f"PASS: Component 6 — launch.json correct (0.15 pts)")
                total_score += 0.15
            elif node_config_found:
                print(f"PARTIAL: Component 6 — Node config found but program doesn't target src/index.js (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 6 — No Node.js launch configuration found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(PROJECT_DIR):
    print(f"Project directory not found: {PROJECT_DIR}")
    print("REWARD: 0.0")
else:
    verify_task(PROJECT_DIR)
