"""
Reward Script: Convert single-quoted strings to double-quoted strings in JavaScript file
Task ID: vscode_gs_074
Domain: vscode
Scoring:
  Component 1 (0.5): Simple variable declarations use double quotes
  Component 2 (0.3): Object property values use double quotes
  Component 3 (0.2): Strings with apostrophes converted correctly
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gs_074'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'webapp', 'src', 'config.js')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Simple variable declarations use double quotes (0.5 points)
    # Check that the 10 simple string variable assignments use double quotes
    # These are: environment, hostname, apiBase, secretKey, dbHost, logLevel,
    #            appName, region, cacheDriver, sessionTimeout
    try:
        simple_vars = [
            ('environment', 'production'),
            ('hostname', 'localhost'),
            ('apiBase', '/api/v1'),
            ('secretKey', 'sk-92xJ4mNpQrT8vWzY'),
            ('dbHost', 'db.internal.mycompany.io'),
            ('logLevel', 'warning'),
            ('appName', 'WebApp Dashboard'),
            ('region', 'us-east-1'),
            ('cacheDriver', 'redis'),
            ('sessionTimeout', '3600'),
        ]
        converted_count = 0
        for var_name, expected_value in simple_vars:
            # Look for the line with this variable assignment
            pattern = re.compile(
                r'const\s+' + re.escape(var_name) + r'\s*=\s*"' + re.escape(expected_value) + r'"'
            )
            found_double = any(pattern.search(line) for line in lines)
            if found_double:
                converted_count += 1
            else:
                print(f"  DETAIL: {var_name} not using double quotes with expected value")

        if converted_count == len(simple_vars):
            print(f"PASS: Component 1 - All {converted_count}/{len(simple_vars)} simple vars use double quotes (0.5 pts)")
            total_score += 0.5
        elif converted_count > 0:
            partial = 0.5 * (converted_count / len(simple_vars))
            print(f"PARTIAL: Component 1 - {converted_count}/{len(simple_vars)} simple vars converted ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No simple vars converted to double quotes")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Object property values use double quotes (0.3 points)
    # Check dbConfig and routes object values
    try:
        obj_values = [
            ('host', 'db.internal.mycompany.io'),
            ('name', 'webapp_prod'),
            ('home', '/dashboard'),
            ('login', '/auth/login'),
            ('api', '/api/v1/resources'),
            ('health', '/status/health'),
        ]
        obj_converted = 0
        for prop_name, expected_value in obj_values:
            # Match object property: key: "value"
            pattern = re.compile(
                r'\b' + re.escape(prop_name) + r'\s*:\s*"' + re.escape(expected_value) + r'"'
            )
            found_double = any(pattern.search(line) for line in lines)
            if found_double:
                obj_converted += 1
            else:
                print(f"  DETAIL: Object prop '{prop_name}' not using double quotes")

        if obj_converted == len(obj_values):
            print(f"PASS: Component 2 - All {obj_converted}/{len(obj_values)} object props use double quotes (0.3 pts)")
            total_score += 0.3
        elif obj_converted > 0:
            partial = 0.3 * (obj_converted / len(obj_values))
            print(f"PARTIAL: Component 2 - {obj_converted}/{len(obj_values)} object props converted ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No object property values converted to double quotes")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Strings with apostrophes handled correctly (0.2 points)
    # welcomeMsg should be "it's working" and errorMsg should be "something's not right"
    # With double quotes, the apostrophe doesn't need escaping
    try:
        apostrophe_checks = [
            ('welcomeMsg', "it's working"),
            ('errorMsg', "something's not right"),
        ]
        apos_converted = 0
        for var_name, expected_value in apostrophe_checks:
            # Check for double-quoted version with unescaped apostrophe
            # The line should contain: "it's working" (not 'it\'s working')
            pattern = re.compile(
                r'const\s+' + re.escape(var_name) + r'\s*=\s*"' + re.escape(expected_value) + r'"'
            )
            found_double = any(pattern.search(line) for line in lines)
            if found_double:
                apos_converted += 1
            else:
                print(f"  DETAIL: {var_name} with apostrophe not correctly converted")

        if apos_converted == len(apostrophe_checks):
            print(f"PASS: Component 3 - Both apostrophe strings correctly converted (0.2 pts)")
            total_score += 0.2
        elif apos_converted > 0:
            partial = 0.2 * (apos_converted / len(apostrophe_checks))
            print(f"PARTIAL: Component 3 - {apos_converted}/{len(apostrophe_checks)} apostrophe strings converted ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - Apostrophe strings not converted to double quotes")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point - test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
