"""
Reward Script: Verify Python log_parser.py script that parses nginx access log
Task ID: os_gf1_031
Domain: os (scripting)
Scoring:
  Component 1 (0.20): Script exists at /opt/scripts/log_parser.py and is executable
  Component 2 (0.25): Script runs without error on the access log
  Component 3 (0.35): Output contains correct status codes with correct counts
  Component 4 (0.20): Output is sorted by count in descending order
"""

import os
import re
import stat
from collections import Counter

SCRIPT_PATH = '/opt/scripts/log_parser.py'
LOG_PATH = '/var/log/nginx/access.log'


def compute_expected_counts():
    """Independently compute the expected status code counts from the access log."""
    counter = Counter()
    pattern = re.compile(r'"\S+\s+\S+\s+\S+" (\d{3})')
    try:
        with open(LOG_PATH, 'r') as f:
            for line in f:
                m = pattern.search(line)
                if m:
                    counter[m.group(1)] += 1
    except Exception:
        return {}
    return dict(counter)


def run_script():
    """Run the log_parser.py script and capture its stdout/stderr by exec'ing it."""
    import io
    import sys
    import contextlib

    try:
        with open(SCRIPT_PATH, 'r') as f:
            script_code = f.read()

        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        # Save original argv
        orig_argv = sys.argv
        sys.argv = [SCRIPT_PATH]

        try:
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                exec(compile(script_code, SCRIPT_PATH, 'exec'), {'__name__': '__main__', '__file__': SCRIPT_PATH})
            return stdout_capture.getvalue(), stderr_capture.getvalue(), 0
        except SystemExit as e:
            # Script called sys.exit() -- code 0 is OK, else failure
            code = e.code if e.code is not None else 0
            if code == 0:
                return stdout_capture.getvalue(), stderr_capture.getvalue(), 0
            else:
                return stdout_capture.getvalue(), stderr_capture.getvalue() + f"\nSystemExit({code})", code
        except Exception as e:
            return stdout_capture.getvalue(), str(e), 1
        finally:
            sys.argv = orig_argv
    except Exception as e:
        return '', str(e), -1


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Script exists and is executable (0.20 points)
    # This FAILS on initial_env (no script exists) and PASSES on golden_env
    try:
        if os.path.isfile(SCRIPT_PATH):
            mode = stat.S_IMODE(os.stat(SCRIPT_PATH).st_mode)
            # Check owner-executable bit at minimum
            if mode & stat.S_IXUSR:
                print(f"PASS: Component 1 — Script exists at {SCRIPT_PATH} with executable permission (mode={oct(mode)}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — Script exists but is not executable (mode={oct(mode)})")
        else:
            print(f"FAIL: Component 1 — Script not found at {SCRIPT_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If script doesn't exist, remaining checks are meaningless
    if not os.path.isfile(SCRIPT_PATH):
        print(f"\nScript not found — skipping remaining components.")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Script runs without error (0.25 points)
    # Runs the script with python3 and checks exit code == 0 and no stderr errors
    try:
        stdout, stderr, returncode = run_script()
        if returncode == 0 and stdout.strip():
            print(f"PASS: Component 2 — Script runs successfully (exit code 0, output has {len(stdout.strip().splitlines())} lines) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Script failed (exit code={returncode}, stdout_empty={not stdout.strip()}, stderr={stderr[:200]})")
            # If the script can't run, output checks will fail anyway
            stdout = ''
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")
        stdout = ''

    # Component 3: Output contains correct status codes with correct counts (0.35 points)
    # Parse script output and compare against independently computed counts
    try:
        expected = compute_expected_counts()
        if not expected:
            print(f"FAIL: Component 3 — Could not compute expected counts (log file issue)")
        else:
            # Parse output lines: expect format like "200: 1523" or "200 : 1523" or "200  1523"
            output_lines = stdout.strip().splitlines() if stdout else []
            parsed = {}
            for line in output_lines:
                line = line.strip()
                # Try "CODE: COUNT" or "CODE COUNT" patterns
                m = re.match(r'^(\d{3})\s*[:]\s*(\d+)$', line)
                if not m:
                    m = re.match(r'^(\d{3})\s+(\d+)$', line)
                if m:
                    parsed[m.group(1)] = int(m.group(2))

            if not parsed:
                print(f"FAIL: Component 3 — No status code lines parsed from output")
            else:
                # Check how many codes match exactly
                total_codes = len(expected)
                matching = 0
                for code, count in expected.items():
                    if code in parsed and parsed[code] == count:
                        matching += 1
                    else:
                        got = parsed.get(code, 'MISSING')
                        print(f"  INFO: Code {code}: expected {count}, got {got}")

                if matching == total_codes and len(parsed) == total_codes:
                    print(f"PASS: Component 3 — All {total_codes} status codes match exactly (0.35 pts)")
                    total_score += 0.35
                elif matching > 0:
                    partial = 0.35 * (matching / total_codes)
                    if partial > 0:
                        print(f"PARTIAL: Component 3 — {matching}/{total_codes} status codes match ({partial:.2f} pts)")
                        total_score += partial
                else:
                    print(f"FAIL: Component 3 — No status codes matched (parsed {len(parsed)} codes)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Output is sorted by count descending (0.20 points)
    try:
        output_lines = stdout.strip().splitlines() if stdout else []
        counts_in_order = []
        for line in output_lines:
            line = line.strip()
            m = re.match(r'^(\d{3})\s*[:]\s*(\d+)$', line)
            if not m:
                m = re.match(r'^(\d{3})\s+(\d+)$', line)
            if m:
                counts_in_order.append(int(m.group(2)))

        if len(counts_in_order) >= 2:
            is_sorted_desc = all(
                counts_in_order[i] >= counts_in_order[i + 1]
                for i in range(len(counts_in_order) - 1)
            )
            if is_sorted_desc:
                print(f"PASS: Component 4 — Output is sorted by count descending ({counts_in_order}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Output is NOT sorted descending: {counts_in_order}")
        else:
            print(f"FAIL: Component 4 — Not enough output lines to verify sorting ({len(counts_in_order)} lines)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
