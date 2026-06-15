"""
Reward Script: Save email attachment onboarding_checklist.odt to /home/user/documents/
Task ID: osworld_multi_apps_email_file_convert_002
Domain: multi_apps (Thunderbird + OS file management)
Scoring:
  - Component 1: onboarding_checklist.odt exists at /home/user/documents/ (0.5 pts)
  - Component 2: File is a valid ODT (ZIP-based) format with expected structure (0.3 pts)
  - Component 3: ODT content.xml contains expected document heading (0.2 pts)
  Total: 1.0
"""

import os
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_file_convert_002'

TARGET_PATH = '/home/user/documents/onboarding_checklist.odt'
EXPECTED_HEADING = 'New Employee Onboarding Checklist'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    The task requires saving onboarding_checklist.odt from a Thunderbird email
    attachment to /home/user/documents/. We verify:
    1. The file was saved to the correct location
    2. The file is a valid ODT (OpenDocument Text) format
    3. The file content matches the expected onboarding checklist document

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File saved to correct location (0.5 points)
    # This FAILS on initial_env (empty documents dir) and PASSES on golden_env
    try:
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            if file_size > 0:
                print(f"PASS: Component 1 — onboarding_checklist.odt exists at {file_path} "
                      f"(size: {file_size} bytes) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — file exists but is empty at {file_path}")
        else:
            print(f"FAIL: Component 1 — file not found at {file_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: File is a valid ODT format (0.3 points)
    # ODT files are ZIP archives; check for required ODT structure entries
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env (valid ODT)
    try:
        if os.path.isfile(file_path):
            with zipfile.ZipFile(file_path, 'r') as z:
                names = z.namelist()
                required_entries = ['mimetype', 'content.xml', 'META-INF/manifest.xml']
                missing = [e for e in required_entries if e not in names]
                if not missing:
                    print(f"PASS: Component 2 — Valid ODT structure with required entries: {required_entries} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Missing ODT entries: {missing}")
        else:
            print(f"FAIL: Component 2 — Cannot validate ODT structure, file not found")
    except zipfile.BadZipFile:
        print(f"FAIL: Component 2 — File is not a valid ZIP/ODT archive")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ODT content matches expected onboarding checklist document (0.2 points)
    # Verify the specific document heading exists in content.xml
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env
    try:
        if os.path.isfile(file_path):
            with zipfile.ZipFile(file_path, 'r') as z:
                content_xml = z.read('content.xml').decode('utf-8')
                if EXPECTED_HEADING in content_xml:
                    print(f"PASS: Component 3 — ODT contains expected heading '{EXPECTED_HEADING}' (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — ODT does not contain expected heading '{EXPECTED_HEADING}'")
                    print(f"      This may be a different document than the expected onboarding checklist")
        else:
            print(f"FAIL: Component 3 — Cannot verify content, file not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the canonical artifact path
if not os.path.isdir('/home/user/documents'):
    print(f"CRITICAL: Target directory /home/user/documents does not exist")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_PATH)
