"""
Reward Script: Fix ESLint missing peer dependencies for airbnb config
Task ID: vscode_fix_059
Domain: vs_code
Scoring:
  - Component 1 (0.25): eslint-plugin-import installed in node_modules
  - Component 2 (0.25): eslint-plugin-jsx-a11y installed in node_modules
  - Component 3 (0.25): eslint-plugin-react installed in node_modules
  - Component 4 (0.25): eslint-plugin-react-hooks installed in node_modules
"""

import os
import json

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'react-project')
TASK_ID = 'vscode_fix_059'

# The four missing peer dependencies that must be installed
REQUIRED_PLUGINS = [
    'eslint-plugin-import',
    'eslint-plugin-jsx-a11y',
    'eslint-plugin-react',
    'eslint-plugin-react-hooks',
]

WEIGHT_PER_PLUGIN = 0.25


def verify_task():
    """
    Verify that all four missing ESLint peer dependencies have been installed.
    Each plugin is checked in node_modules (actual installation) AND in package.json
    devDependencies (persistent record). Both must be present for full credit per plugin.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Load package.json to check devDependencies
    package_json_path = os.path.join(PROJECT_DIR, 'package.json')
    pkg_data = None
    try:
        with open(package_json_path, 'r') as f:
            pkg_data = json.load(f)
    except Exception as e:
        print(f"WARNING: Could not load package.json: {e}")

    dev_deps = {}
    if pkg_data:
        dev_deps = pkg_data.get('devDependencies', {})

    for plugin in REQUIRED_PLUGINS:
        component_label = f"Plugin '{plugin}'"
        try:
            # Check 1: plugin directory exists in node_modules
            plugin_dir = os.path.join(PROJECT_DIR, 'node_modules', plugin)
            dir_exists = os.path.isdir(plugin_dir)

            # Check 2: plugin listed in devDependencies
            in_dev_deps = plugin in dev_deps

            if dir_exists and in_dev_deps:
                print(f"PASS: {component_label} -- installed in node_modules AND listed in devDependencies ({WEIGHT_PER_PLUGIN} pts)")
                total_score += WEIGHT_PER_PLUGIN
            elif dir_exists and not in_dev_deps:
                # Installed but not in package.json -- partial credit (half)
                partial = WEIGHT_PER_PLUGIN * 0.5
                print(f"PARTIAL: {component_label} -- in node_modules but NOT in devDependencies ({partial} pts)")
                total_score += partial
            elif not dir_exists and in_dev_deps:
                # In package.json but not actually installed -- no credit
                print(f"FAIL: {component_label} -- listed in devDependencies but NOT found in node_modules")
            else:
                print(f"FAIL: {component_label} -- not installed and not in devDependencies")
        except Exception as e:
            print(f"ERROR: {component_label} -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
