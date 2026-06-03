"""
Reward Script: Archive Thunderbird sent emails as .eml files and log backup count
Task ID: osworld_multi_apps_email_file_convert_004
Domain: multi_apps (OS file operations + email export)
Scoring:
  - Component 1: sent_backup/ directory contains exactly 12 .eml files (0.6 pts)
  - Component 2: backup_log.txt contains a timestamped count line in correct format (0.4 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_file_convert_004'

SENT_BACKUP_DIR = os.path.join(WORKDIR, 'sent_backup')
BACKUP_LOG_FILE = os.path.join(WORKDIR, 'backup_log.txt')

EXPECTED_EML_COUNT = 12

# Pattern for the log line:
# e.g., "2024-01-15 14:30:00 - Sent: 12 emails backed up"
# We accept any valid datetime prefix (the agent may choose a different timestamp)
LOG_LINE_PATTERN = re.compile(
    r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s+-\s+Sent:\s+12\s+emails\s+backed\s+up\s*$'
)


def count_eml_files(directory):
    """Return count of .eml files in directory, or -1 if directory doesn't exist."""
    if not os.path.isdir(directory):
        return -1
    return len([f for f in os.listdir(directory) if f.lower().endswith('.eml')])


def find_matching_log_line(log_path, pattern):
    """Return the first matching line from the log file, or None if not found."""
    if not os.path.isfile(log_path):
        return None
    with open(log_path, 'r') as f:
        for line in f:
            stripped = line.rstrip('\n').rstrip()
            if pattern.match(stripped):
                return stripped
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: sent_backup/ directory contains exactly 12 .eml files (0.6 points)
    # This FAILS on initial_env (directory does not exist) and PASSES on golden_env (12 .eml files present)
    try:
        eml_count = count_eml_files(SENT_BACKUP_DIR)
        if eml_count == -1:
            print(f"FAIL: Component 1 — sent_backup/ directory does not exist at {SENT_BACKUP_DIR}")
        elif eml_count == EXPECTED_EML_COUNT:
            print(f"PASS: Component 1 — sent_backup/ contains exactly {eml_count} .eml files (0.6 pts)")
            total_score += 0.6
        elif eml_count > 0:
            # Partial credit: some .eml files present but not the expected count
            partial = round(0.6 * (eml_count / EXPECTED_EML_COUNT), 2)
            print(f"PARTIAL: Component 1 — sent_backup/ contains {eml_count}/{EXPECTED_EML_COUNT} .eml files (partial: {partial} pts)")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 1 — sent_backup/ exists but contains 0 .eml files")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: backup_log.txt exists with at least one line matching the format:
    # "<YYYY-MM-DD HH:MM:SS> - Sent: 12 emails backed up"
    # This FAILS on initial_env (file does not exist) and PASSES on golden_env (correct line present)
    try:
        matching_line = find_matching_log_line(BACKUP_LOG_FILE, LOG_LINE_PATTERN)
        if matching_line is None and not os.path.isfile(BACKUP_LOG_FILE):
            print(f"FAIL: Component 2 — backup_log.txt does not exist at {BACKUP_LOG_FILE}")
        elif matching_line is not None:
            print(f"PASS: Component 2 — backup_log.txt contains valid timestamped log line: '{matching_line}' (0.4 pts)")
            total_score += 0.4
        else:
            # File exists but no matching line
            with open(BACKUP_LOG_FILE, 'r') as f:
                actual_lines = [l.rstrip() for l in f.readlines()]
            print(f"FAIL: Component 2 — backup_log.txt exists but no valid line matches expected format.")
            print(f"  Expected pattern: 'YYYY-MM-DD HH:MM:SS - Sent: 12 emails backed up'")
            print(f"  Actual lines: {actual_lines}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
