"""
Reward Script: Verify AutoCorrect entry 'dept' -> 'Department' in LibreOffice Writer
Task ID: writer_frd_061
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): acor_en-US.dat file exists in user profile
  Component 2 (0.6): DocumentList.xml contains dept -> Department mapping
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_061'

# Possible paths for the autocorrect dat file across LibreOffice versions
ACOR_PATHS = [
    os.path.join(WORKDIR, '.config/libreoffice/4/user/autocorr/acor_en-US.dat'),
    os.path.join(WORKDIR, '.config/libreoffice/4/user/autocorr/acor_en-us.dat'),
]


def persist_app_state(domain: str):
    """Attempt to save any open LibreOffice documents before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def find_acor_file():
    """Find the autocorrect dat file."""
    for path in ACOR_PATHS:
        if os.path.exists(path):
            return path
    # Broader search
    autocorr_dir = os.path.join(WORKDIR, '.config/libreoffice/4/user/autocorr')
    if os.path.isdir(autocorr_dir):
        for f in os.listdir(autocorr_dir):
            if f.lower().startswith('acor_en') and f.lower().endswith('.dat'):
                return os.path.join(autocorr_dir, f)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: acor_en-US.dat file exists (0.4 points)
    # This checks that the autocorrect file has been created/modified in the user profile.
    # On initial_env, this file does not exist (empty autocorr dir).
    try:
        acor_path = find_acor_file()
        if acor_path is not None:
            file_size = os.path.getsize(acor_path)
            if file_size > 0:
                print(f"PASS: Component 1 — acor dat file exists at {acor_path} (size: {file_size}) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — acor dat file exists but is empty")
        else:
            print(f"FAIL: Component 1 — No acor_en-US.dat found in LibreOffice user profile")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: DocumentList.xml contains 'dept' -> 'Department' mapping (0.6 points)
    # This verifies the specific autocorrect entry the task requires.
    # On initial_env, no acor file exists so this will fail.
    try:
        if acor_path is None:
            print(f"FAIL: Component 2 — No acor file to check for dept mapping")
        else:
            with zipfile.ZipFile(acor_path, 'r') as z:
                if 'DocumentList.xml' not in z.namelist():
                    print(f"FAIL: Component 2 — DocumentList.xml not found in acor dat file")
                else:
                    content = z.read('DocumentList.xml').decode('utf-8')
                    # Look for the dept -> Department block entry
                    # The XML format is:
                    # <block-list:block block-list:abbreviated-name="dept" block-list:name="Department"/>
                    pattern = r'<block-list:block\s+block-list:abbreviated-name="dept"\s+block-list:name="Department"\s*/>'
                    match = re.search(pattern, content)
                    if match:
                        print(f"PASS: Component 2 — Found dept -> Department mapping in DocumentList.xml (0.6 pts)")
                        total_score += 0.6
                    else:
                        # Also check case-insensitive match for "department"
                        pattern_ci = r'block-list:abbreviated-name="dept"[^/]*block-list:name="[Dd]epartment"'
                        match_ci = re.search(pattern_ci, content)
                        if match_ci:
                            print(f"PASS: Component 2 — Found dept -> Department mapping (case variant) (0.6 pts)")
                            total_score += 0.6
                        else:
                            # Check if dept entry exists with wrong value
                            dept_pattern = r'block-list:abbreviated-name="dept"\s+block-list:name="([^"]*)"'
                            dept_match = re.search(dept_pattern, content)
                            if dept_match:
                                print(f"FAIL: Component 2 — dept maps to '{dept_match.group(1)}' instead of 'Department'")
                            else:
                                print(f"FAIL: Component 2 — No 'dept' entry found in DocumentList.xml")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")
verify_task()
