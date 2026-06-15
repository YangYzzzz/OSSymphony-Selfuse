"""
Reward Script: Protect tracked changes with password 'Review2025'
Task ID: writer_lec_079
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): documentProtection element exists with edit="trackedChanges"
  Component 2 (0.3): enforcement="1" — protection is actually enforced
  Component 3 (0.3): Password hash present (hash + salt attributes) AND tracked changes preserved
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_079'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W_NS}


def verify_task(file_path):
    """
    Verify that tracked changes protection is enabled with a password.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            settings_xml = z.read('word/settings.xml')
            doc_xml = z.read('word/document.xml')
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    settings = etree.fromstring(settings_xml)
    doc_root = etree.fromstring(doc_xml)

    # Find documentProtection element
    protection_elements = settings.findall('.//w:documentProtection', NS)

    # Component 1: documentProtection exists with edit="trackedChanges" (0.4 points)
    # This element should NOT exist in the initial state; it is added by the task.
    try:
        if protection_elements:
            prot = protection_elements[0]
            edit_val = prot.get(f'{{{W_NS}}}edit')
            if edit_val == 'trackedChanges':
                print(f"PASS: Component 1 — documentProtection edit='trackedChanges' found (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — documentProtection exists but edit='{edit_val}', expected 'trackedChanges'")
        else:
            print("FAIL: Component 1 — No documentProtection element found in settings.xml")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: enforcement="1" — protection is actually enforced (0.3 points)
    try:
        if protection_elements:
            prot = protection_elements[0]
            enforcement_val = prot.get(f'{{{W_NS}}}enforcement')
            if enforcement_val == '1':
                print(f"PASS: Component 2 — enforcement='1', protection is enforced (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — enforcement='{enforcement_val}', expected '1'")
        else:
            print("FAIL: Component 2 — No documentProtection element (prerequisite missing)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Password hash is present AND tracked changes are preserved (0.3 points)
    # The hash/salt attributes confirm a password was set (not just empty protection).
    # Also verify tracked changes (inserts/deletes) still exist in the document.
    try:
        hash_ok = (
            len(protection_elements) > 0
            and protection_elements[0].get(f'{{{W_NS}}}hash', '') != ''
            and len(protection_elements[0].get(f'{{{W_NS}}}hash', '')) > 10
            and protection_elements[0].get(f'{{{W_NS}}}salt', '') != ''
            and len(protection_elements[0].get(f'{{{W_NS}}}salt', '')) > 5
        )

        if hash_ok:
            h = protection_elements[0].get(f'{{{W_NS}}}hash')
            s = protection_elements[0].get(f'{{{W_NS}}}salt')
            print(f"  CHECK: Password hash present (len={len(h)}), salt present (len={len(s)})")
        else:
            print(f"  CHECK: Missing or empty hash/salt in documentProtection")

        # Verify tracked changes still exist
        inserts = doc_root.findall('.//w:ins', NS)
        deletes = doc_root.findall('.//w:del', NS)
        total_changes = len(inserts) + len(deletes)
        changes_ok = total_changes > 0

        if changes_ok:
            print(f"  CHECK: {total_changes} tracked changes preserved ({len(inserts)} inserts, {len(deletes)} deletes)")
        else:
            print(f"  CHECK: No tracked changes found — they may have been accepted/rejected")

        if hash_ok and changes_ok:
            print(f"PASS: Component 3 — Password hash present AND tracked changes preserved (0.3 pts)")
            total_score += 0.3
        elif hash_ok:
            print(f"PARTIAL: Component 3 — Password hash present but tracked changes missing (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Password hash missing")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
