"""
Reward Script: Resolve merge conflicts in shared_utils.py
Task ID: vscode_rf_048
Domain: vscode
Scoring:
  - Component 1 (0.25): No conflict markers remain
  - Component 2 (0.30): First conflict resolved by keeping both functions
  - Component 3 (0.25): Second conflict resolved by keeping only incoming change
  - Component 4 (0.20): File is valid Python syntax
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_048'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'collaboration', 'shared_utils.py')


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

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: No conflict markers remain (0.25 points)
    # This checks that ALL conflict markers have been removed from the file.
    try:
        conflict_markers = ['<<<<<<<', '=======', '>>>>>>>']
        markers_found = []
        for marker in conflict_markers:
            if marker in content:
                markers_found.append(marker)

        if len(markers_found) == 0:
            print(f"PASS: Component 1 — No conflict markers found in file (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Conflict markers still present: {markers_found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: First conflict resolved by keeping both functions (0.30 points)
    # The first conflict had extract_emails (HEAD) and normalize_whitespace (incoming).
    # Both should be present after accepting both changes.
    # IMPORTANT: Both function defs exist in the unresolved file inside conflict markers,
    # so we must also require NO conflict markers to confirm actual resolution.
    try:
        has_extract_emails = 'def extract_emails(' in content
        has_normalize_whitespace = 'def normalize_whitespace(' in content
        no_markers = not any(m in content for m in ['<<<<<<<', '=======', '>>>>>>>'])

        if has_extract_emails and has_normalize_whitespace and no_markers:
            print(f"PASS: Component 2 — Both extract_emails and normalize_whitespace functions present, no conflict markers (0.30 pts)")
            total_score += 0.30
        elif not no_markers:
            print(f"FAIL: Component 2 — Conflict markers still present, first conflict not resolved")
        else:
            missing = []
            if not has_extract_emails:
                missing.append('extract_emails')
            if not has_normalize_whitespace:
                missing.append('normalize_whitespace')
            print(f"FAIL: Component 2 — Missing functions from first conflict resolution: {missing}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Second conflict resolved by keeping only incoming change (0.25 points)
    # The second conflict had calculate_date_range (HEAD) and parse_relative_date (incoming).
    # Only parse_relative_date should remain (incoming change accepted).
    # Must also require no conflict markers to confirm actual resolution.
    try:
        has_calculate_date_range = 'def calculate_date_range(' in content
        has_parse_relative_date = 'def parse_relative_date(' in content
        no_markers = not any(m in content for m in ['<<<<<<<', '=======', '>>>>>>>'])

        if has_parse_relative_date and not has_calculate_date_range and no_markers:
            print(f"PASS: Component 3 — parse_relative_date present, calculate_date_range removed, no markers (0.25 pts)")
            total_score += 0.25
        elif not no_markers:
            print(f"FAIL: Component 3 — Conflict markers still present, second conflict not resolved")
        elif has_parse_relative_date and has_calculate_date_range:
            print(f"FAIL: Component 3 — calculate_date_range should have been removed (only incoming change for second conflict)")
        elif not has_parse_relative_date and not has_calculate_date_range:
            print(f"FAIL: Component 3 — parse_relative_date missing (incoming change should have been kept)")
        else:
            print(f"FAIL: Component 3 — parse_relative_date missing, calculate_date_range present (wrong resolution)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Valid Python syntax (0.20 points)
    # The resolved file should be valid Python that can be compiled.
    try:
        syntax_error = None
        try:
            compile(content, file_path, 'exec')
        except SyntaxError as se:
            syntax_error = str(se)

        if syntax_error is None:
            print(f"PASS: Component 4 — File compiles as valid Python (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Python syntax error: {syntax_error}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
