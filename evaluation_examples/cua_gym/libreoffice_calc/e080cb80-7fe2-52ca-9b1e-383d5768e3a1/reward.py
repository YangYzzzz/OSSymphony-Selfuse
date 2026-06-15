"""
Reward Script: backup_and_report.sh creation and execution
Task ID: osworld_multi_apps_code_batch_terminal_011
Domain: multi_apps / os / terminal
Scoring:
  - Component 1: Shell script exists at /home/user/scripts/backup_and_report.sh and is executable (0.2)
  - Component 2: Script contains required logic (sha256sum, cp -r, timestamp, checksums.txt, HTML report) (0.3)
  - Component 3: At least one timestamped backup directory with 18 copied files and 18 checksum entries (0.3)
  - Component 4: HTML report at /home/user/Desktop/backup_report.html showing file count of 18 (0.2)
Total: 1.0
"""

import os
import re
import glob
import stat

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_batch_terminal_011'

SCRIPT_PATH = '/home/user/scripts/backup_and_report.sh'
BACKUPS_BASE = '/home/user/backups'
HTML_REPORT = '/home/user/Desktop/backup_report.html'
EXPECTED_FILE_COUNT = 18


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Script exists and is executable (0.2 points)
    # This FAILS on initial (script does not exist) and PASSES on golden (script exists and is executable)
    try:
        script_exists = os.path.isfile(SCRIPT_PATH)
        if not script_exists:
            print(f"FAIL: Component 1 — script not found at {SCRIPT_PATH}")
        else:
            # Check executable permission
            file_stat = os.stat(SCRIPT_PATH)
            is_executable = bool(file_stat.st_mode & stat.S_IXUSR) or bool(file_stat.st_mode & stat.S_IXGRP) or bool(file_stat.st_mode & stat.S_IXOTH)
            if is_executable:
                print(f"PASS: Component 1 — script exists at {SCRIPT_PATH} and is executable (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — script exists but is NOT executable (permissions: {oct(file_stat.st_mode)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Script contains required logic (0.3 points)
    # Checks for sha256sum, cp -r, timestamped directory logic, checksums.txt, HTML report path
    # This FAILS on initial (script doesn't exist) and PASSES on golden
    try:
        if not os.path.isfile(SCRIPT_PATH):
            print("FAIL: Component 2 — script does not exist, cannot check content")
        else:
            with open(SCRIPT_PATH, 'r') as f:
                script_content = f.read()

            checks = {
                'sha256sum (checksum computation)': 'sha256sum' in script_content,
                'cp -r (recursive copy)': 'cp -r' in script_content,
                'timestamped backup dir (date +%Y%m%d_%H%M%S or similar)': bool(
                    re.search(r'date\s+\+.*%Y', script_content) or
                    re.search(r'TIMESTAMP', script_content)
                ),
                'checksums.txt reference': 'checksums.txt' in script_content,
                'HTML report generation': 'backup_report.html' in script_content or '.html' in script_content,
                '/home/user/documents/important source dir': '/home/user/documents/important' in script_content or 'documents/important' in script_content,
            }

            passed = [k for k, v in checks.items() if v]
            failed = [k for k, v in checks.items() if not v]

            # Full credit: all 6 elements present
            if len(passed) == len(checks):
                print(f"PASS: Component 2 — all {len(checks)} required script elements present (0.3 pts)")
                print(f"  Verified: {', '.join(passed)}")
                total_score += 0.3
            # Partial credit: at least 4 of 6 elements present
            elif len(passed) >= 4:
                print(f"PARTIAL: Component 2 — {len(passed)}/{len(checks)} elements present (0.15 pts)")
                total_score += 0.15
            # No credit: fewer than 4 elements present
            else:
                print(f"FAIL: Component 2 — only {len(passed)}/{len(checks)} required elements present")
                print(f"  Present: {passed}")
                print(f"  Missing: {failed}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Timestamped backup directory with 18 files and 18 checksum entries (0.3 points)
    # This FAILS on initial (no backups directory) and PASSES on golden (backup dirs exist)
    try:
        if not os.path.isdir(BACKUPS_BASE):
            print(f"FAIL: Component 3 — backups base directory not found: {BACKUPS_BASE}")
        else:
            # Find all timestamped backup dirs matching YYYYMMDD_HHMMSS
            backup_dirs = [
                d for d in glob.glob(os.path.join(BACKUPS_BASE, '*'))
                if os.path.isdir(d) and re.match(r'^\d{8}_\d{6}$', os.path.basename(d))
            ]

            if not backup_dirs:
                print(f"FAIL: Component 3 — no timestamped backup directories found in {BACKUPS_BASE}")
            else:
                # Check the most recent backup dir for completeness
                backup_dirs_sorted = sorted(backup_dirs)
                valid_backup = None
                for d in backup_dirs_sorted:
                    # Count files excluding checksums.txt
                    file_count = 0
                    for root, dirs, files in os.walk(d):
                        for fn in files:
                            if fn != 'checksums.txt':
                                file_count += 1

                    # Count checksum entries
                    cksum_path = os.path.join(d, 'checksums.txt')
                    cksum_count = 0
                    if os.path.isfile(cksum_path):
                        with open(cksum_path, 'r') as f:
                            cksum_count = len([line for line in f.readlines() if line.strip()])

                    if file_count == EXPECTED_FILE_COUNT and cksum_count == EXPECTED_FILE_COUNT:
                        valid_backup = d
                        break

                if valid_backup:
                    print(f"PASS: Component 3 — valid backup at {valid_backup} with {EXPECTED_FILE_COUNT} files and {EXPECTED_FILE_COUNT} checksum entries (0.3 pts)")
                    total_score += 0.3
                else:
                    # Check if any backup has files and checksums (partial)
                    best_dir = None
                    best_files = 0
                    best_cksum = 0
                    for d in backup_dirs_sorted:
                        file_count = 0
                        for root, dirs, files in os.walk(d):
                            for fn in files:
                                if fn != 'checksums.txt':
                                    file_count += 1
                        cksum_path = os.path.join(d, 'checksums.txt')
                        cksum_count = 0
                        if os.path.isfile(cksum_path):
                            with open(cksum_path, 'r') as f:
                                cksum_count = len([line for line in f.readlines() if line.strip()])
                        if file_count > best_files:
                            best_files = file_count
                            best_cksum = cksum_count
                            best_dir = d

                    if best_files > 0:
                        print(f"PARTIAL: Component 3 — backup dir {best_dir} has {best_files} files (expected {EXPECTED_FILE_COUNT}) and {best_cksum} checksum entries (0.1 pts)")
                        total_score += 0.1
                    else:
                        print(f"FAIL: Component 3 — backup directories found ({len(backup_dirs)}) but none have correct file count ({EXPECTED_FILE_COUNT})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: HTML report at /home/user/Desktop/backup_report.html with file count 18 (0.2 points)
    # This FAILS on initial (no HTML report) and PASSES on golden (HTML report with 18 files)
    try:
        if not os.path.isfile(HTML_REPORT):
            print(f"FAIL: Component 4 — HTML report not found at {HTML_REPORT}")
        else:
            with open(HTML_REPORT, 'r') as f:
                html_content = f.read()

            # Check for required elements
            has_file_count_18 = '18' in html_content
            has_backup_stats = ('Total Files' in html_content or 'files backed' in html_content.lower() or
                                'Files Backed Up' in html_content)
            has_backup_path = 'backups' in html_content
            has_html_structure = '<html' in html_content.lower() or '<!DOCTYPE' in html_content

            print(f"  HTML report checks: file_count_18={has_file_count_18}, backup_stats={has_backup_stats}, "
                  f"backup_path={has_backup_path}, html_structure={has_html_structure}")

            if has_file_count_18 and has_backup_stats and has_backup_path and has_html_structure:
                print(f"PASS: Component 4 — HTML report exists at {HTML_REPORT} with file count (18) and backup statistics (0.2 pts)")
                total_score += 0.2
            elif has_html_structure and has_backup_path:
                print(f"PARTIAL: Component 4 — HTML report exists but missing file count 18 or stats details (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 4 — HTML report exists but missing required content")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
