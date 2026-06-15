"""
Reward Script: Configure ESLint in VSCode React project and fix linting errors
Task ID: vscode_gf5_012
Domain: vscode
Scoring:
  Component 1: ESLint extension installed (0.15)
  Component 2: .eslintrc.json exists with React plugin config (0.25)
  Component 3: package.json has eslint devDependencies (0.20)
  Component 4: App.js - unused import removed (0.15)
  Component 5: App.js - key prop added to list items (0.15)
  Component 6: App.js - console.log removed (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_012'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-app')


def verify_task():
    """
    Verify ESLint configuration and linting fixes.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ESLint extension installed (0.15 points)
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        if os.path.isdir(ext_dir):
            ext_entries = os.listdir(ext_dir)
            eslint_found = any('eslint' in e.lower() and e != 'extensions.json' for e in ext_entries)
            if eslint_found:
                print(f"PASS: Component 1 — ESLint extension found in {ext_dir} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — No ESLint extension in {ext_dir}, entries: {ext_entries}")
        else:
            print(f"FAIL: Component 1 — Extensions directory not found: {ext_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: .eslintrc.json exists with React plugin config (0.25 points)
    try:
        eslintrc_path = os.path.join(PROJECT_DIR, '.eslintrc.json')
        if os.path.exists(eslintrc_path):
            with open(eslintrc_path, 'r') as f:
                eslintrc = json.load(f)

            has_react_plugin = 'react' in eslintrc.get('plugins', [])
            extends_list = eslintrc.get('extends', [])
            has_react_extends = any('react' in ext for ext in extends_list)

            if has_react_plugin and has_react_extends:
                print(f"PASS: Component 2 — .eslintrc.json has React plugin and extends (0.25 pts)")
                total_score += 0.25
            elif has_react_plugin or has_react_extends:
                print(f"PARTIAL: Component 2 — React plugin: {has_react_plugin}, React extends: {has_react_extends} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — .eslintrc.json missing React plugin config. plugins={eslintrc.get('plugins')}, extends={extends_list}")
        else:
            print(f"FAIL: Component 2 — .eslintrc.json not found at {eslintrc_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: package.json has eslint devDependencies (0.20 points)
    try:
        pkg_path = os.path.join(PROJECT_DIR, 'package.json')
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)

        dev_deps = pkg.get('devDependencies', {})
        has_eslint = 'eslint' in dev_deps
        has_eslint_react = 'eslint-plugin-react' in dev_deps

        if has_eslint and has_eslint_react:
            print(f"PASS: Component 3 — devDependencies has eslint and eslint-plugin-react (0.20 pts)")
            total_score += 0.20
        elif has_eslint or has_eslint_react:
            print(f"PARTIAL: Component 3 — eslint: {has_eslint}, eslint-plugin-react: {has_eslint_react} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — devDependencies missing eslint packages. devDeps: {dev_deps}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Read App.js for components 4-6
    try:
        app_path = os.path.join(PROJECT_DIR, 'src', 'App.js')
        with open(app_path, 'r') as f:
            app_content = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read App.js: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    # Component 4: Unused import (useState) removed (0.15 points)
    # Initial has: import React, { useState } from 'react';
    # Golden has: import React from 'react';
    # Check that useState is NOT imported
    try:
        has_usestate_import = bool(re.search(r'\buseState\b', app_content.split('\n')[0] if app_content else ''))
        # More robust: check all import lines for useState
        import_lines = [l for l in app_content.split('\n') if l.strip().startswith('import')]
        has_usestate = any('useState' in l for l in import_lines)

        if not has_usestate:
            print(f"PASS: Component 4 — useState import removed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — useState still imported in: {[l for l in import_lines if 'useState' in l]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Key prop added to list items (0.15 points)
    # Initial: <li className="task-item">
    # Golden: <li key={task.id} className="task-item">
    try:
        # Check for key prop in li elements within map callback
        has_key_prop = bool(re.search(r'<li\s+key\s*=\s*\{', app_content))

        if has_key_prop:
            print(f"PASS: Component 5 — key prop found on list items (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — No key prop found on <li> elements in map")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: console.log removed (0.10 points)
    # Initial has: console.log('Rendering App component with tasks:', tasks.length);
    # Golden has it removed
    try:
        # Check that console.log is not present in the function body (not in comments)
        code_lines = [l for l in app_content.split('\n') if not l.strip().startswith('//')]
        has_console_log = any('console.log' in l for l in code_lines)

        if not has_console_log:
            print(f"PASS: Component 6 — console.log removed (0.10 pts)")
            total_score += 0.10
        else:
            matching = [l.strip() for l in code_lines if 'console.log' in l]
            print(f"FAIL: Component 6 — console.log still present: {matching}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
