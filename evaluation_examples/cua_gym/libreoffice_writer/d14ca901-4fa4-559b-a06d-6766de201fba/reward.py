"""
Reward Script: Disable the AutoCorrect replacement that changes '(c)' to the copyright symbol '©'.
Task ID: writer_edit_068
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): User-level acor_en-US.dat file exists (LibreOffice AutoCorrect override file)
  Component 2 (0.5): The '(c)'/'.*(C)' -> '©' entry is absent from the user-level AutoCorrect file
"""

import os
import zipfile
import io
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_edit_068'

# Path to the user-level AutoCorrect override file
USER_AUTOCORR_PATH = '/home/user/.config/libreoffice/4/user/autocorr/acor_en-US.dat'

# Known abbreviation forms for the (c) -> copyright replacement in LibreOffice
# The system default uses '.*(C)' as the abbreviated-name (regex form)
COPYRIGHT_ABBREV_FORMS = ['.*(C)', '(c)', '(C)']
COPYRIGHT_UNICODE = '\u00a9'  # ©
COPYRIGHT_XML_ENTITY = '&#xA9;'  # &#xA9; is © in XML


def load_doclist_entries(dat_path):
    """Load DocumentList.xml entries from an acor_en-US.dat (zip) file.
    Returns dict: {abbreviated_name: replacement_name}
    """
    with open(dat_path, 'rb') as f:
        data = f.read()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        content = z.read('DocumentList.xml').decode('utf-8')
    entries = {}
    for block in re.findall(r'<block-list:block[^/]*/>', content):
        abname = re.search(r'abbreviated-name="([^"]*)"', block)
        name_match = re.search(r'block-list:name="([^"]*)"', block)
        if abname and name_match:
            entries[abname.group(1)] = name_match.group(1)
    return entries


def verify_task():
    """
    Verify that the (c) -> © AutoCorrect entry has been removed or disabled.

    The task requires:
    1. A user-level AutoCorrect file exists to override the system default.
    2. The .*(C) / (c) -> © replacement entry is NOT present in that file.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: User-level acor_en-US.dat file exists (0.5 points)
    # When a user modifies AutoCorrect settings, LibreOffice creates a user-level
    # override file at ~/.config/libreoffice/4/user/autocorr/acor_en-US.dat.
    # Without this file, the system default (which includes (c) -> ©) is used.
    try:
        if os.path.exists(USER_AUTOCORR_PATH):
            print(f"PASS: Component 1 — user-level acor_en-US.dat exists at {USER_AUTOCORR_PATH} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — user-level acor_en-US.dat NOT found at {USER_AUTOCORR_PATH}")
            print("      Without this file, system defaults (including (c)->©) remain active.")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: The (c) -> © entry is absent from the user-level AutoCorrect file (0.5 points)
    # The system default uses '.*(C)' as abbreviated-name which matches (c) and (C).
    # After the task is complete, this entry should be removed from the user-level file.
    try:
        entries = load_doclist_entries(USER_AUTOCORR_PATH)
        print(f"INFO: Loaded {len(entries)} entries from user-level acor_en-US.dat")

        # Check if any copyright-abbreviation form exists in the user file
        found_copyright_entry = None
        for abbrev_form in COPYRIGHT_ABBREV_FORMS:
            if abbrev_form in entries:
                found_copyright_entry = abbrev_form
                break

        # Also check by value: any entry whose replacement is © (unicode or XML)
        # This catches alternate abbreviated-name forms
        for abbrev, replacement in entries.items():
            if replacement == COPYRIGHT_UNICODE or replacement == COPYRIGHT_XML_ENTITY:
                # '(c)' family check - only flag if it looks like the (c) entry
                if '(c)' in abbrev.lower() or '(C)' in abbrev or abbrev == '.*(C)':
                    found_copyright_entry = abbrev
                    break

        if found_copyright_entry is None:
            print(f"PASS: Component 2 — (c)->© AutoCorrect entry is ABSENT from user-level file (0.5 pts)")
            print(f"      Checked abbreviation forms: {COPYRIGHT_ABBREV_FORMS}")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — (c)->© entry still present in user-level file")
            print(f"      Found entry: '{found_copyright_entry}' -> '{entries[found_copyright_entry]}'")
    except Exception as e:
        print(f"ERROR: Component 2 — could not load/parse user acor_en-US.dat: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
