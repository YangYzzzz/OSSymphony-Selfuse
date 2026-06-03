"""
Reward Script: PDF Form Validation Engine
Task ID: pdf_gf3_042
Domain: pdf
Scoring:
  Component 1 (0.15): form_validator.py exists at /home/user/scripts/form_validator.py
  Component 2 (0.15): Script executes without errors (exit code 0)
  Component 3 (0.15): Script reads PDF form fields (output mentions known field names)
  Component 4 (0.15): Script validates fields with PASS/FAIL lines for each rule
  Component 5 (0.20): Output format correct: 'PASS: <field>' or 'FAIL: <field> - <msg>'
  Component 6 (0.20): Summary line: 'Total fields: 12, Passed: X, Failed: Y'
"""

import os
import re
import sys

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_042'

SCRIPT_PATH = os.path.join(WORKDIR, 'scripts', 'form_validator.py')
PDF_PATH = os.path.join(WORKDIR, 'forms', 'filled_application.pdf')
RULES_PATH = os.path.join(WORKDIR, 'rules', 'form_rules.json')

# The 12 field names from form_rules.json
EXPECTED_FIELDS = [
    'first_name', 'last_name', 'email', 'phone',
    'date_of_birth', 'application_date', 'years_experience',
    'desired_salary', 'department', 'education_level',
    'agree_terms', 'cover_letter'
]


def run_script():
    """Run the form_validator.py script and capture output + exit code."""
    import io
    import importlib.util

    # Run as a subprocess-like execution by capturing stdout
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    captured_out = io.StringIO()
    captured_err = io.StringIO()
    sys.stdout = captured_out
    sys.stderr = captured_err
    exit_code = 0

    try:
        # Read and exec the script in an isolated namespace
        with open(SCRIPT_PATH, 'r') as f:
            script_code = f.read()
        exec_namespace = {'__name__': '__main__', '__file__': SCRIPT_PATH}
        exec(compile(script_code, SCRIPT_PATH, 'exec'), exec_namespace)
    except SystemExit as e:
        exit_code = e.code if e.code is not None else 0
    except Exception as e:
        exit_code = 1
        captured_err.write(str(e))
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    return captured_out.getvalue(), captured_err.getvalue(), exit_code


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: form_validator.py exists (0.15 points)
    try:
        if os.path.isfile(SCRIPT_PATH):
            # Check it's not an empty file
            file_size = os.path.getsize(SCRIPT_PATH)
            if file_size > 50:
                print(f"PASS: Component 1 -- form_validator.py exists ({file_size} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- form_validator.py exists but too small ({file_size} bytes)")
        else:
            print(f"FAIL: Component 1 -- form_validator.py not found at {SCRIPT_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # If the script doesn't exist, we can't test further
    if total_score < 0.1:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Run the script to get output
    try:
        stdout_text, stderr_text, exit_code = run_script()
        output_lines = stdout_text.strip().split('\n') if stdout_text.strip() else []
        print(f"DEBUG: Script produced {len(output_lines)} output lines, exit_code={exit_code}")
        if stderr_text.strip():
            print(f"DEBUG: stderr: {stderr_text.strip()[:200]}")
    except Exception as e:
        print(f"ERROR: Could not run script: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Script runs without errors (0.15 points)
    try:
        if exit_code == 0 and len(output_lines) > 0:
            print(f"PASS: Component 2 -- Script executed successfully, exit code 0 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Script exit_code={exit_code}, output_lines={len(output_lines)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Script reads PDF form fields (0.15 points)
    # Verify the output references at least 8 of the 12 known field names
    try:
        fields_mentioned = 0
        for field in EXPECTED_FIELDS:
            for line in output_lines:
                if field in line:
                    fields_mentioned += 1
                    break
        if fields_mentioned >= 8:
            print(f"PASS: Component 3 -- {fields_mentioned}/12 expected fields found in output (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- Only {fields_mentioned}/12 expected fields found in output")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Script validates fields with PASS/FAIL lines (0.15 points)
    # Each field should have a PASS: or FAIL: line
    try:
        pass_fail_lines = [l for l in output_lines if l.strip().startswith('PASS:') or l.strip().startswith('FAIL:')]
        # We expect at least 10 PASS/FAIL lines (out of 12 fields)
        if len(pass_fail_lines) >= 10:
            print(f"PASS: Component 4 -- {len(pass_fail_lines)} PASS/FAIL validation lines found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- Only {len(pass_fail_lines)} PASS/FAIL lines (expected >= 10)")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Output format correct (0.20 points)
    # 'PASS: field_name' or 'FAIL: field_name - error message'
    try:
        correct_format_count = 0
        pass_pattern = re.compile(r'^PASS:\s+\w+$')
        fail_pattern = re.compile(r'^FAIL:\s+\w+\s*-\s*.+$')
        for line in output_lines:
            stripped = line.strip()
            if pass_pattern.match(stripped) or fail_pattern.match(stripped):
                correct_format_count += 1

        # At least 10 lines should match the expected format
        if correct_format_count >= 10:
            print(f"PASS: Component 5 -- {correct_format_count} lines match expected format (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 -- Only {correct_format_count} lines match format 'PASS: name' or 'FAIL: name - msg'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Summary line format (0.20 points)
    # 'Total fields: 12, Passed: X, Failed: Y'
    try:
        summary_pattern = re.compile(r'Total fields:\s*12,\s*Passed:\s*\d+,\s*Failed:\s*\d+')
        summary_found = False
        for line in output_lines:
            if summary_pattern.search(line.strip()):
                # Also verify Passed + Failed == 12
                m = re.search(r'Passed:\s*(\d+),\s*Failed:\s*(\d+)', line)
                if m:
                    passed_val = int(m.group(1))
                    failed_val = int(m.group(2))
                    if passed_val + failed_val == 12:
                        summary_found = True
                        print(f"PASS: Component 6 -- Summary line correct: Passed={passed_val}, Failed={failed_val} (0.20 pts)")
                        total_score += 0.20
                    else:
                        print(f"FAIL: Component 6 -- Summary counts don't add to 12: {passed_val}+{failed_val}={passed_val+failed_val}")
                break
        if not summary_found:
            # Check for a partial match
            partial_pattern = re.compile(r'Total fields.*Passed.*Failed', re.IGNORECASE)
            partial_match = False
            for line in output_lines:
                if partial_pattern.search(line):
                    partial_match = True
                    break
            if partial_match:
                print(f"FAIL: Component 6 -- Summary line found but does not match exact format")
            else:
                print(f"FAIL: Component 6 -- No summary line found")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
