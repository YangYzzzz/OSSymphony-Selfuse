"""
Reward Script: VSCode Node.js API project setup
Task ID: vscode_gf4_002
Domain: vscode
Scoring:
  - Component 1 (0.20): package.json exists and is valid JSON
  - Component 2 (0.20): express and dotenv in dependencies
  - Component 3 (0.15): nodemon in devDependencies
  - Component 4 (0.20): 'dev' script set to 'nodemon src/index.js'
  - Component 5 (0.15): .env file with PORT=4000 and NODE_ENV=development
  - Component 6 (0.10): node_modules contains express, dotenv, nodemon
"""

import os
import json

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'node-api')
TASK_ID = 'vscode_gf4_002'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    pkg_path = os.path.join(PROJECT_DIR, 'package.json')
    env_path = os.path.join(PROJECT_DIR, '.env')
    nm_path = os.path.join(PROJECT_DIR, 'node_modules')

    # Component 1: package.json exists and is valid JSON (0.20 points)
    pkg_data = None
    try:
        if os.path.isfile(pkg_path):
            with open(pkg_path, 'r') as f:
                pkg_data = json.load(f)
            if isinstance(pkg_data, dict):
                print(f"PASS: Component 1 — package.json exists and is valid JSON (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — package.json is not a JSON object, type: {type(pkg_data)}")
        else:
            print(f"FAIL: Component 1 — package.json does not exist at {pkg_path}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — package.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: express and dotenv in dependencies (0.20 points)
    try:
        if pkg_data and isinstance(pkg_data, dict):
            deps = pkg_data.get('dependencies', {})
            has_express = 'express' in deps
            has_dotenv = 'dotenv' in deps
            if has_express and has_dotenv:
                print(f"PASS: Component 2 — express and dotenv found in dependencies (0.20 pts)")
                total_score += 0.20
            else:
                missing = []
                if not has_express:
                    missing.append('express')
                if not has_dotenv:
                    missing.append('dotenv')
                print(f"FAIL: Component 2 — missing from dependencies: {missing}")
        else:
            print(f"FAIL: Component 2 — package.json not loaded, cannot check dependencies")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: nodemon in devDependencies (0.15 points)
    try:
        if pkg_data and isinstance(pkg_data, dict):
            dev_deps = pkg_data.get('devDependencies', {})
            if 'nodemon' in dev_deps:
                print(f"PASS: Component 3 — nodemon found in devDependencies (0.15 pts)")
                total_score += 0.15
            else:
                # Also check if it's mistakenly in regular dependencies
                deps = pkg_data.get('dependencies', {})
                if 'nodemon' in deps:
                    print(f"FAIL: Component 3 — nodemon found in dependencies but NOT in devDependencies")
                else:
                    print(f"FAIL: Component 3 — nodemon not found in devDependencies")
        else:
            print(f"FAIL: Component 3 — package.json not loaded")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'dev' script set to 'nodemon src/index.js' (0.20 points)
    try:
        if pkg_data and isinstance(pkg_data, dict):
            scripts = pkg_data.get('scripts', {})
            dev_script = scripts.get('dev', None)
            if dev_script is not None:
                # Normalize whitespace for comparison
                normalized = dev_script.strip()
                if normalized == 'nodemon src/index.js':
                    print(f"PASS: Component 4 — dev script is 'nodemon src/index.js' (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 4 — dev script is '{dev_script}', expected 'nodemon src/index.js'")
            else:
                print(f"FAIL: Component 4 — 'dev' script not found in scripts. Found scripts: {list(scripts.keys())}")
        else:
            print(f"FAIL: Component 4 — package.json not loaded")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: .env file with PORT=4000 and NODE_ENV=development (0.15 points)
    try:
        if os.path.isfile(env_path):
            with open(env_path, 'r') as f:
                env_content = f.read()
            # Parse .env lines into key-value pairs
            env_vars = {}
            for line in env_content.strip().split('\n'):
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, _, value = line.partition('=')
                    env_vars[key.strip()] = value.strip()

            has_port = env_vars.get('PORT') == '4000'
            has_node_env = env_vars.get('NODE_ENV') == 'development'

            if has_port and has_node_env:
                print(f"PASS: Component 5 — .env has PORT=4000 and NODE_ENV=development (0.15 pts)")
                total_score += 0.15
            else:
                if not has_port:
                    print(f"FAIL: Component 5 — PORT not set to 4000, found: {env_vars.get('PORT', '<missing>')}")
                if not has_node_env:
                    print(f"FAIL: Component 5 — NODE_ENV not set to development, found: {env_vars.get('NODE_ENV', '<missing>')}")
        else:
            print(f"FAIL: Component 5 — .env file does not exist at {env_path}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: node_modules contains express, dotenv, nodemon (0.10 points)
    try:
        if os.path.isdir(nm_path):
            installed = os.listdir(nm_path)
            has_express = 'express' in installed
            has_dotenv = 'dotenv' in installed
            has_nodemon = 'nodemon' in installed
            if has_express and has_dotenv and has_nodemon:
                print(f"PASS: Component 6 — node_modules contains express, dotenv, nodemon (0.10 pts)")
                total_score += 0.10
            else:
                missing = []
                if not has_express:
                    missing.append('express')
                if not has_dotenv:
                    missing.append('dotenv')
                if not has_nodemon:
                    missing.append('nodemon')
                print(f"FAIL: Component 6 — missing from node_modules: {missing}")
        else:
            print(f"FAIL: Component 6 — node_modules directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
