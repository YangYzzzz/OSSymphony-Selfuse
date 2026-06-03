"""
Reward Script: Fix source map configuration for webpack-bundled TypeScript project
Task ID: vscode_fix_071
Domain: vs_code
Scoring:
  Component 1 (0.4): webpack.config.js devtool changed from 'eval' to 'source-map'
  Component 2 (0.3): sourceMapPathOverrides has correct webpack:///./src/* mapping
  Component 3 (0.3): sourceMapPathOverrides has project-specific mapping (inventory-dashboard)
"""

import os
import re
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_071'
PROJECT_DIR = os.path.join(WORKDIR, 'webpack-ts-project')
WEBPACK_CONFIG = os.path.join(PROJECT_DIR, 'webpack.config.js')
LAUNCH_JSON = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def parse_jsonc(text):
    """Parse JSON with Comments (JSONC). Handles control characters and // comments outside strings."""
    # Rather than regex-stripping comments (which breaks URLs with //),
    # just use strict=False to handle control characters
    try:
        return json.loads(text, strict=False)
    except json.JSONDecodeError:
        # Fallback: strip single-line comments that start at beginning of line
        lines = text.split('\n')
        cleaned = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('//'):
                continue
            cleaned.append(line)
        return json.loads('\n'.join(cleaned), strict=False)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: webpack.config.js must exist
    if not os.path.exists(WEBPACK_CONFIG):
        print(f"CRITICAL: webpack.config.js not found at {WEBPACK_CONFIG}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: launch.json must exist
    if not os.path.exists(LAUNCH_JSON):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: webpack devtool set to 'source-map' (0.4 points)
    # Initial has 'eval', golden has 'source-map'
    try:
        with open(WEBPACK_CONFIG, 'r') as f:
            webpack_content = f.read()

        # Check that devtool is set to 'source-map' (not 'eval' or other values)
        # Match patterns like: devtool: 'source-map' or devtool: "source-map"
        source_map_match = re.search(r"devtool\s*:\s*['\"]source-map['\"]", webpack_content)
        eval_match = re.search(r"devtool\s*:\s*['\"]eval['\"]", webpack_content)

        if source_map_match and not eval_match:
            print(f"PASS: Component 1 -- webpack devtool is 'source-map' (0.4 pts)")
            total_score += 0.4
        elif eval_match:
            print(f"FAIL: Component 1 -- webpack devtool is still 'eval', expected 'source-map'")
        else:
            # Check for other devtool values
            devtool_match = re.search(r"devtool\s*:\s*['\"]([^'\"]+)['\"]", webpack_content)
            if devtool_match:
                print(f"FAIL: Component 1 -- webpack devtool is '{devtool_match.group(1)}', expected 'source-map'")
            else:
                print(f"FAIL: Component 1 -- devtool setting not found in webpack.config.js")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Load launch.json for Components 2 and 3
    try:
        with open(LAUNCH_JSON, 'r') as f:
            launch_content = f.read()
        launch_config = parse_jsonc(launch_content)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Find the Debug Webpack Bundle configuration
    debug_config = None
    for config in launch_config.get('configurations', []):
        if config.get('name') == 'Debug Webpack Bundle':
            debug_config = config
            break

    if not debug_config:
        print(f"FAIL: No 'Debug Webpack Bundle' configuration found in launch.json")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    overrides = debug_config.get('sourceMapPathOverrides', {})
    print(f"INFO: sourceMapPathOverrides found: {json.dumps(overrides, indent=2)}")

    # Component 2: sourceMapPathOverrides has correct webpack:///./src/* mapping (0.3 points)
    # Initial has "webpack:///./*" -> "${workspaceFolder}/src/*" (generic, incorrect)
    # Golden has "webpack:///./src/*" -> "${workspaceFolder}/src/*" (specific, correct)
    try:
        src_key = "webpack:///./src/*"
        old_generic_key = "webpack:///./*"

        if src_key in overrides:
            expected_value = "${workspaceFolder}/src/*"
            if overrides[src_key] == expected_value:
                # Also verify the old incorrect generic mapping is gone
                if old_generic_key not in overrides:
                    print(f"PASS: Component 2 -- sourceMapPathOverrides has '{src_key}' -> '{expected_value}' and old generic mapping removed (0.3 pts)")
                    total_score += 0.3
                else:
                    # Still has the old mapping, partial credit - the new correct one is there
                    print(f"PASS: Component 2 -- sourceMapPathOverrides has '{src_key}' -> '{expected_value}' (0.3 pts)")
                    total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- '{src_key}' maps to '{overrides[src_key]}', expected '{expected_value}'")
        else:
            print(f"FAIL: Component 2 -- sourceMapPathOverrides missing '{src_key}' key")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: sourceMapPathOverrides has project-specific mapping for inventory-dashboard (0.3 points)
    # Initial does NOT have this mapping. Golden adds:
    #   "webpack://inventory-dashboard/./src/*" -> "${workspaceFolder}/src/*"
    try:
        project_key = "webpack://inventory-dashboard/./src/*"
        if project_key in overrides:
            expected_value = "${workspaceFolder}/src/*"
            if overrides[project_key] == expected_value:
                print(f"PASS: Component 3 -- sourceMapPathOverrides has project-specific mapping '{project_key}' -> '{expected_value}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- '{project_key}' maps to '{overrides[project_key]}', expected '{expected_value}'")
        else:
            print(f"FAIL: Component 3 -- sourceMapPathOverrides missing project-specific mapping '{project_key}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
