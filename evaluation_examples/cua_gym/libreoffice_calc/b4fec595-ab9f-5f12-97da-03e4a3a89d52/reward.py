"""
Reward Script: Export Thunderbird 'Projects' emails to .eml files and find deadline emails
Task ID: osworld_multi_apps_email_file_convert_005
Domain: os (multi-apps: Thunderbird + terminal)
Scoring:
  Component 1 (0.40): projects_email_backup/ directory exists with exactly 9 .eml files
  Component 2 (0.35): deadline_emails.txt exists and lists exactly the 4 correct filenames (basenames only)
  Component 3 (0.25): Each file listed in deadline_emails.txt actually contains 'deadline' in its content
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_file_convert_005'

BACKUP_DIR = '/home/user/projects_email_backup'
DEADLINE_FILE = '/home/user/deadline_emails.txt'
EXPECTED_EML_COUNT = 9
EXPECTED_DEADLINE_FILENAMES = {
    'proj001_Q3_Project_Deadline_Reminder.eml',
    'proj002_Website_Redesign_Status_Update.eml',
    'proj003_Budget_Approval_Required.eml',
    'proj004_Code_Review_Assignments.eml',
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: projects_email_backup directory exists with exactly 9 .eml files (0.40 points)
    # This check FAILS on initial_env (directory doesn't exist) and PASSES on golden_env
    try:
        if not os.path.isdir(BACKUP_DIR):
            print(f"FAIL: Component 1 — backup directory not found at {BACKUP_DIR}")
        else:
            eml_files = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.eml')]
            actual_count = len(eml_files)
            if actual_count == EXPECTED_EML_COUNT:
                print(f"PASS: Component 1 — {BACKUP_DIR} exists with exactly {EXPECTED_EML_COUNT} .eml files (0.4 pts)")
                total_score += 0.40
            else:
                print(f"FAIL: Component 1 — expected {EXPECTED_EML_COUNT} .eml files, found {actual_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: deadline_emails.txt exists and lists the 4 correct filenames (0.35 points)
    # This check FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        if not os.path.isfile(DEADLINE_FILE):
            print(f"FAIL: Component 2 — deadline_emails.txt not found at {DEADLINE_FILE}")
        else:
            with open(DEADLINE_FILE, 'r') as f:
                raw_content = f.read()
            # Parse lines, strip whitespace, ignore empty lines, and strip full paths to get basenames only
            lines = [line.strip() for line in raw_content.splitlines() if line.strip()]
            # Allow both full-path and filename-only entries — normalize to basename
            actual_filenames = set(os.path.basename(line) for line in lines)

            if actual_filenames == EXPECTED_DEADLINE_FILENAMES:
                print(f"PASS: Component 2 — deadline_emails.txt lists exactly the 4 expected filenames (0.35 pts)")
                print(f"  Listed filenames: {sorted(actual_filenames)}")
                total_score += 0.35
            else:
                missing = EXPECTED_DEADLINE_FILENAMES - actual_filenames
                extra = actual_filenames - EXPECTED_DEADLINE_FILENAMES
                print(f"FAIL: Component 2 — deadline_emails.txt content mismatch")
                if missing:
                    print(f"  Missing: {sorted(missing)}")
                if extra:
                    print(f"  Extra (unexpected): {sorted(extra)}")
                print(f"  Actual entries: {sorted(actual_filenames)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each file listed in deadline_emails.txt actually contains 'deadline' in its content (0.25 points)
    # This check FAILS on initial_env (backup dir and deadline_emails.txt don't exist)
    try:
        if not os.path.isfile(DEADLINE_FILE) or not os.path.isdir(BACKUP_DIR):
            print(f"FAIL: Component 3 — prerequisites not met (backup dir or deadline file missing)")
        else:
            with open(DEADLINE_FILE, 'r') as f:
                lines = [line.strip() for line in f.read().splitlines() if line.strip()]

            verified_count = 0
            problem_files = []

            for entry in lines:
                # The file may be listed as basename or full path; resolve to backup dir
                filename = os.path.basename(entry)
                eml_path = os.path.join(BACKUP_DIR, filename)

                if not os.path.isfile(eml_path):
                    problem_files.append(f"{filename}: file not found in backup dir")
                    continue

                try:
                    with open(eml_path, 'r', errors='replace') as ef:
                        content = ef.read()
                    # Use case-sensitive search for 'deadline' consistent with grep -l 'deadline'
                    if 'deadline' in content:
                        verified_count += 1
                    else:
                        problem_files.append(f"{filename}: does not contain 'deadline'")
                except Exception as fe:
                    problem_files.append(f"{filename}: read error — {fe}")

            if len(problem_files) == 0 and verified_count == len(lines) and len(lines) > 0:
                print(f"PASS: Component 3 — all {verified_count} listed files contain 'deadline' in content (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — content verification issues:")
                for p in problem_files:
                    print(f"  - {p}")
                print(f"  Verified {verified_count}/{len(lines)} files")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


verify_task()
