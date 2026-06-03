"""
Reward Script: Modify Corporate_Standard.otp template
Task ID: impress_fix_043
Domain: libreoffice_impress

Scoring:
  Component 1 (0.5): Footer text changed from '2024 Confidential' to '2025 Internal Use Only'
  Component 2 (0.5): Accent color changed from #cc0000 (red) to #008080 (teal)

The file is an ODP/OTP (OpenDocument) ZIP archive. We parse content.xml
to verify both footer text and color changes.
"""

import os
import re
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_043'
FILE_PATH = os.path.join(WORKDIR, 'Templates', 'Corporate_Standard.otp')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid ZIP (OTP is ZIP-based)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open OTP file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read content.xml - this is where slide content and styles live
    try:
        content_xml = zf.read('content.xml').decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot read content.xml from {file_path}: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    zf.close()

    # Component 1: Footer text changed to '2025 Internal Use Only' (0.5 points)
    # In the initial file, footer shapes named "Footer_Text" contain '2024 Confidential'.
    # In the golden file, they should contain '2025 Internal Use Only'.
    # We check: (a) new text present, (b) old text absent.
    try:
        new_footer_count = len(re.findall(r'2025 Internal Use Only', content_xml))
        old_footer_count = len(re.findall(r'2024 Confidential', content_xml))

        if new_footer_count > 0 and old_footer_count == 0:
            print(f"PASS: Component 1 — Footer text updated to '2025 Internal Use Only' "
                  f"({new_footer_count} occurrences, old text absent) (0.5 pts)")
            total_score += 0.5
        elif new_footer_count > 0 and old_footer_count > 0:
            # Partial: some footers updated but not all
            print(f"PARTIAL: Component 1 — New footer found ({new_footer_count}x) but "
                  f"old footer still present ({old_footer_count}x) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected '2025 Internal Use Only' in footer text. "
                  f"Found {new_footer_count} new, {old_footer_count} old.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Accent color changed from #cc0000 to #008080 (0.5 points)
    # In the initial file, there are 8 occurrences of #cc0000 in content.xml.
    # In the golden file, all should be replaced with #008080.
    # We check: (a) #008080 present, (b) #cc0000 absent.
    try:
        teal_count = len(re.findall(r'#008080', content_xml, re.IGNORECASE))
        red_count = len(re.findall(r'#cc0000', content_xml, re.IGNORECASE))

        if teal_count > 0 and red_count == 0:
            print(f"PASS: Component 2 — Accent color updated to #008080 "
                  f"({teal_count} occurrences, #cc0000 absent) (0.5 pts)")
            total_score += 0.5
        elif teal_count > 0 and red_count > 0:
            # Partial: some colors updated but not all
            ratio = teal_count / (teal_count + red_count)
            partial = round(0.5 * ratio, 2)
            print(f"PARTIAL: Component 2 — Teal found ({teal_count}x) but "
                  f"red still present ({red_count}x) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Expected #008080 accent color. "
                  f"Found {teal_count} teal, {red_count} red.")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
