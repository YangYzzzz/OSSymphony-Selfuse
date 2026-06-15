"""
Reward Script: Fix Python image batch processor to skip non-image files
Task ID: osworld_multi_apps_vscode_debug_crash_008
Domain: vs-code / os (Python file verification)
Scoring:
  Component 1 (0.4): processor.py catches UnidentifiedImageError and skips non-image files
  Component 2 (0.3): processor.py logs skipped files to ~/Desktop/skipped_files.log
  Component 3 (0.3): skipped_files.log exists and contains paths of non-image files
"""

import os
import re

WORKDIR = '/home/user'
PROCESSOR_PATH = '/home/user/Desktop/img_processor/processor.py'
SKIPPED_LOG_PATH = '/home/user/Desktop/skipped_files.log'
INPUT_DIR = '/home/user/Desktop/img_processor/input'

# Known non-image files from the input directory
NON_IMAGE_FILES = ['inventory.csv', 'metadata.txt', 'notes.txt']


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: processor.py must exist
    if not os.path.isfile(PROCESSOR_PATH):
        print(f"CRITICAL: processor.py not found at {PROCESSOR_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(PROCESSOR_PATH, 'r') as f:
            processor_code = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read processor.py: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: processor.py catches UnidentifiedImageError and skips non-image files (0.4 points)
    # This checks that the bug fix is present: the original code crashed on non-image files.
    # The fix must import UnidentifiedImageError and use it in an except clause.
    try:
        has_import = 'UnidentifiedImageError' in processor_code
        has_except = bool(re.search(r'except\s+UnidentifiedImageError', processor_code))
        # Also check that the except block does NOT re-raise (i.e., it skips/continues)
        # Look for a pattern where after catching UnidentifiedImageError, execution continues
        # (no bare raise, no sys.exit, etc.)
        except_blocks = re.findall(
            r'except\s+UnidentifiedImageError.*?(?=\nexcept|\ndef |\nclass |\Z)',
            processor_code,
            re.DOTALL
        )
        # A skip-behavior block is one that handles the error without re-raising it.
        # We check if any except block contains log/skip/continue/return without a bare raise.
        has_skip_behavior = any(
            ('raise' not in block.lower() or 'log' in block.lower()
             or 'skip' in block.lower() or 'continue' in block.lower()
             or 'return' in block.lower())
            for block in except_blocks
        )

        if has_import and has_except and has_skip_behavior:
            print(f"PASS: Component 1 — processor.py imports UnidentifiedImageError and catches it to skip non-image files (0.4 pts)")
            total_score += 0.4
        elif has_import and has_except:
            # Partial: has the import and except but uncertain about skip behavior
            print(f"PASS: Component 1 — processor.py has UnidentifiedImageError import and except clause (0.4 pts)")
            total_score += 0.4
        elif has_import:
            print(f"FAIL: Component 1 — processor.py imports UnidentifiedImageError but no except clause found")
        else:
            print(f"FAIL: Component 1 — processor.py does not import or handle UnidentifiedImageError (original bug not fixed)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: processor.py logs skipped files to ~/Desktop/skipped_files.log (0.3 points)
    # The fix must write skipped file paths to SKIPPED_LOG_PATH.
    try:
        skipped_log_ref = 'skipped_files.log' in processor_code
        # Check for a write/append operation to the log file in processor.py
        has_log_write = bool(re.search(
            r"open\s*\(.*skipped_files\.log.*['\"]a['\"]",
            processor_code
        )) or bool(re.search(
            r"SKIPPED_LOG\s*=.*skipped_files\.log",
            processor_code
        ))
        # Also accept if the log path variable is referenced and a write exists
        has_write_op = bool(re.search(r'\.write\s*\(', processor_code))

        if skipped_log_ref and (has_log_write or has_write_op):
            print(f"PASS: Component 2 — processor.py references skipped_files.log and has write operation (0.3 pts)")
            total_score += 0.3
        elif skipped_log_ref:
            print(f"PASS: Component 2 — processor.py references skipped_files.log (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — processor.py does not reference or write to skipped_files.log")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: skipped_files.log exists and contains paths of non-image files (0.3 points)
    # This is the runtime evidence that the fix works: the log file must exist on Desktop
    # and must contain entries for the non-image files from the input directory.
    try:
        if not os.path.isfile(SKIPPED_LOG_PATH):
            print(f"FAIL: Component 3 — skipped_files.log does not exist at {SKIPPED_LOG_PATH}")
        else:
            with open(SKIPPED_LOG_PATH, 'r') as f:
                log_content = f.read()

            if not log_content.strip():
                print(f"FAIL: Component 3 — skipped_files.log is empty")
            else:
                # Check that at least one of the known non-image files appears in the log
                found_entries = [fname for fname in NON_IMAGE_FILES if fname in log_content]
                if found_entries:
                    print(f"PASS: Component 3 — skipped_files.log exists and contains non-image file entries: {found_entries} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — skipped_files.log exists but does not contain expected non-image file entries. Content: {log_content[:200]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
