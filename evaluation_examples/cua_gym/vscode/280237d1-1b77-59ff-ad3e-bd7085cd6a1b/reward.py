"""
Reward Script: Change all values in the [production] section to 'REDACTED'
Task ID: vscode_edit_066
Domain: vs_code
Scoring:
  - Component 1: production[database_url] == 'REDACTED' AND dev/test sections intact (0.25 pts)
  - Component 2: production[api_key] == 'REDACTED' AND dev/test sections intact (0.25 pts)
  - Component 3: production[debug_mode] == 'REDACTED' AND dev/test sections intact (0.25 pts)
  - Component 4: production[log_level] == 'REDACTED' AND dev/test sections intact (0.25 pts)
  Total: 1.0

  NOTE: dev/test preservation is a COMPOUND requirement bundled with each production key check.
  On initial_env, none of the production values are 'REDACTED', so all components fail → score 0.0.
  On golden_env, all production values are 'REDACTED' and dev/test are intact → score 1.0.
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_066'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'settings.ini')

# Expected values for sections that must NOT change
EXPECTED_DEVELOPMENT = {
    'database_url': 'postgres://dev-db.internal:5432/appdb_dev',
    'api_key': 'dev_api_key_a3f82bc91d4e',
    'debug_mode': 'true',
    'log_level': 'DEBUG',
}

EXPECTED_TESTING = {
    'database_url': 'postgres://test-db.internal:5432/appdb_test',
    'api_key': 'test_api_key_7c6d2ef04a91',
    'debug_mode': 'true',
    'log_level': 'INFO',
}

# Production keys that must all become REDACTED
PRODUCTION_KEYS = ['database_url', 'api_key', 'debug_mode', 'log_level']


def parse_ini_preserve_case(file_path):
    """
    Parse INI file while preserving key case and handling semicolon comments.
    Returns a dict of {section: {key: value}} for key-value lines only.
    """
    sections = {}
    current_section = None

    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        stripped = line.strip()
        # Skip empty lines and comment lines (semicolons and hash used in this file)
        if not stripped or stripped.startswith(';') or stripped.startswith('#'):
            continue
        # Section header
        if stripped.startswith('[') and stripped.endswith(']'):
            current_section = stripped[1:-1]
            sections[current_section] = {}
            continue
        # Key-value pair
        if '=' in stripped and current_section is not None:
            key, _, value = stripped.partition('=')
            sections[current_section][key.strip()] = value.strip()

    return sections


def check_sections_preserved(sections):
    """
    Check that [development] and [testing] sections retain their original values.
    Returns (bool, list_of_issues)
    """
    issues = []

    dev_section = sections.get('development', {})
    for key, expected_val in EXPECTED_DEVELOPMENT.items():
        actual_val = dev_section.get(key, None)
        # Case-insensitive compare for values like 'true'/'True', 'DEBUG'/'debug'
        if actual_val is None or actual_val.lower() != expected_val.lower():
            issues.append(f"development[{key}]: expected {repr(expected_val)}, found {repr(actual_val)}")

    test_section = sections.get('testing', {})
    for key, expected_val in EXPECTED_TESTING.items():
        actual_val = test_section.get(key, None)
        if actual_val is None or actual_val.lower() != expected_val.lower():
            issues.append(f"testing[{key}]: expected {repr(expected_val)}, found {repr(actual_val)}")

    return len(issues) == 0, issues


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the INI file
    try:
        sections = parse_ini_preserve_case(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: all three sections must exist
    for section_name in ['development', 'testing', 'production']:
        if section_name not in sections:
            print(f"CRITICAL: Missing section [{section_name}] — file may be corrupted")
            print("REWARD: 0.0")
            return 0.0

    # Check that dev/test sections are preserved — used as a compound guard
    try:
        preserved, preservation_issues = check_sections_preserved(sections)
        if not preserved:
            print("FAIL: [development] or [testing] sections have been modified:")
            for issue in preservation_issues:
                print(f"  - {issue}")
            print("NOTE: Points are only awarded when production values are REDACTED AND dev/test are preserved")
            # Don't return early — still report production check results below, but score will be 0.0
    except Exception as e:
        preserved = False
        print(f"ERROR: Could not verify dev/test preservation: {e}")

    # Components 1-4: Each production key value must be 'REDACTED'
    # Points are only awarded when the key is REDACTED AND dev/test sections are preserved.
    # This compound design ensures initial_env (where production is not REDACTED) scores 0.0.
    prod_section = sections.get('production', {})

    for key in PRODUCTION_KEYS:
        try:
            actual_value = prod_section.get(key, None)
            production_key_ok = (actual_value == 'REDACTED')

            if production_key_ok and preserved:
                print(f"PASS: production[{key}] == 'REDACTED' AND dev/test preserved (+0.25 pts)")
                total_score += 0.25
            elif production_key_ok and not preserved:
                print(f"PARTIAL: production[{key}] == 'REDACTED' but dev/test sections were modified (0 pts)")
            else:
                print(f"FAIL: production[{key}] expected 'REDACTED', found: {repr(actual_value)}")
        except Exception as e:
            print(f"ERROR: Checking production[{key}]: {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
