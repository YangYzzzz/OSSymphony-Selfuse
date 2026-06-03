"""
Reward Script: Remove document protection on Quarterly_Report.docx
Task ID: writer_rm_041
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): Document protection is removed (no documentProtection element or enforcement off)
  Component 2 (0.4): Tracked changes are preserved (14 tracked changes: 9 insertions + 5 deletions)
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_041'

WML_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WML_NS}


def persist_app_state(domain: str):
    """Best-effort save if LibreOffice is open."""
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


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Document protection is removed (0.6 points)
    # In the initial env, there is a <w:documentProtection w:enforcement="1" w:edit="trackedChanges"> element.
    # In the golden env, this element should be absent or have enforcement="0"/not enforced.
    try:
        settings_elem = doc.settings.element
        prot_elements = settings_elem.findall('.//w:documentProtection', NS)

        if len(prot_elements) == 0:
            # No protection element at all — protection fully removed
            print("PASS: Component 1 — No documentProtection element found; protection removed (0.6 pts)")
            total_score += 0.6
        else:
            # Check if enforcement is off
            prot = prot_elements[0]
            enforcement = prot.get(f'{{{WML_NS}}}enforcement')
            if enforcement in ('0', 'false', None):
                print(f"PASS: Component 1 — documentProtection exists but enforcement={enforcement}; protection disabled (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 1 — documentProtection enforcement={enforcement}; protection still active")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Protection removed AND tracked changes preserved (0.4 points)
    # This is a compound check: only awards points if protection is already removed (Component 1 passed)
    # AND the 14 tracked changes (9 insertions + 5 deletions) are still present.
    # This ensures that removing protection didn't accidentally accept/reject/delete tracked changes.
    try:
        body_xml = etree.tostring(doc.element.body, pretty_print=True).decode()
        ins_count = body_xml.count('<w:ins ')
        del_count = body_xml.count('<w:del ')
        rpr_count = body_xml.count('<w:rPrChange ')
        ppr_count = body_xml.count('<w:pPrChange ')
        total_tracked = ins_count + del_count + rpr_count + ppr_count

        print(f"  Tracked changes found: {total_tracked} (ins={ins_count}, del={del_count}, rPr={rpr_count}, pPr={ppr_count})")

        # Only award points if protection was actually removed (anchored to the task change)
        protection_removed = (total_score >= 0.6)  # Component 1 must have passed

        if protection_removed and total_tracked >= 14:
            print(f"PASS: Component 2 — Protection removed AND all 14 tracked changes preserved (0.4 pts)")
            total_score += 0.4
        elif protection_removed and total_tracked >= 7:
            print(f"PARTIAL: Component 2 — Protection removed but only {total_tracked}/14 tracked changes remain (0.2 pts)")
            total_score += 0.2
        elif protection_removed and total_tracked > 0:
            print(f"PARTIAL: Component 2 — Protection removed but only {total_tracked}/14 tracked changes remain (0.1 pts)")
            total_score += 0.1
        elif not protection_removed:
            print(f"FAIL: Component 2 — Protection not yet removed; cannot award tracked-changes preservation points")
        else:
            print(f"FAIL: Component 2 — No tracked changes found; expected 14")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
