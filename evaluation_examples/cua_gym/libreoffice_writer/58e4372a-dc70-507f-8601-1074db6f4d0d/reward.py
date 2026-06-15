"""
Reward Script: Protect sections 1-3 of contract, leave section 4 editable
Task ID: writer_biz_072
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): Document protection enabled (readOnly + enforcement)
  Component 2 (0.35): Editable range (permStart) at Section 4 with edGrp=everyone
  Component 3 (0.25): Editable range properly closed (permEnd with matching id)
"""

import os
import re
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_072'

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def persist_app_state(domain):
    """Save any unsaved LibreOffice changes before verification."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        import time
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for %s" % domain)
    except Exception as e:
        print("PERSIST_WARN: save hook failed: %s" % e)


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
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Document protection enabled (0.40 points)
    # Task requires sections 1-3 to be protected from editing.
    # In OOXML this is done via documentProtection in settings.
    # Must have edit="readOnly" (or "forms"/"sections") and enforcement="1".
    try:
        settings_el = doc.settings.element
        doc_prot = settings_el.find('.//w:documentProtection', NS)
        if doc_prot is not None:
            w_ns = NS['w']
            edit_val = doc_prot.get('{%s}edit' % w_ns)
            enforce_val = doc_prot.get('{%s}enforcement' % w_ns)
            # Accept readOnly or forms or sections as valid protection types
            valid_edits = ('readOnly', 'forms', 'sections', 'comments', 'trackedChanges')
            if edit_val in valid_edits and enforce_val in ('1', 'true'):
                print("PASS: Component 1 — documentProtection found: edit=%s, enforcement=%s (0.40 pts)" % (edit_val, enforce_val))
                total_score += 0.40
            else:
                print("FAIL: Component 1 — documentProtection has unexpected values: edit=%s, enforcement=%s" % (edit_val, enforce_val))
        else:
            print("FAIL: Component 1 — no documentProtection element found in settings")
    except Exception as e:
        print("ERROR: Component 1 — %s" % e)

    # Component 2: Editable range at Section 4 (0.35 points)
    # There must be a permStart element with edGrp="everyone" located at/near
    # the "Section 4: Amendments" heading, making that section editable.
    try:
        body = doc.element.body
        perm_starts = body.findall('.//w:permStart', NS)
        if len(perm_starts) > 0:
            w_ns = NS['w']
            # Check that at least one permStart has edGrp="everyone" near Section 4
            everyone_perm_ids = []
            section4_perm_ids = []
            for ps in perm_starts:
                ed_grp = ps.get('{%s}edGrp' % w_ns)
                ps_id = ps.get('{%s}id' % w_ns)
                if ed_grp == 'everyone':
                    everyone_perm_ids.append(ps_id)
                    # Check location: should be in a paragraph containing "Section 4" or "Amendments"
                    parent = ps.getparent()
                    while parent is not None and parent.tag != '{%s}p' % w_ns:
                        parent = parent.getparent()
                    if parent is not None:
                        para_text = ''.join(t.text or '' for t in parent.findall('.//w:t', NS))
                        if 'section 4' in para_text.lower() or 'amendment' in para_text.lower():
                            section4_perm_ids.append(ps_id)

            if len(section4_perm_ids) > 0:
                perm_id = section4_perm_ids[0]
                print("PASS: Component 2 — permStart with edGrp=everyone found at Section 4 (id=%s) (0.35 pts)" % perm_id)
                total_score += 0.35
            elif len(everyone_perm_ids) > 0:
                # Partial: editable range exists but not clearly at Section 4
                perm_id = everyone_perm_ids[0]
                if len(everyone_perm_ids) > 0:
                    print("PARTIAL: Component 2 — permStart with edGrp=everyone found but not clearly at Section 4 (0.20 pts)")
                    total_score += 0.20
            else:
                perm_id = None
                all_grps = [ps.get('{%s}edGrp' % w_ns) for ps in perm_starts]
                print("FAIL: Component 2 — permStart found but edGrp values are: %s (expected 'everyone')" % all_grps)
        else:
            print("FAIL: Component 2 — no permStart elements found in document body")
    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    # Component 3: Editable range properly closed (0.25 points)
    # There must be a permEnd element with matching id, ensuring the editable
    # range for Section 4 is properly bounded.
    try:
        body_xml = etree.tostring(body).decode()
        perm_ends = body.findall('.//w:permEnd', NS)
        if len(perm_ends) > 0:
            w_ns = NS['w']
            # Check for a matching permEnd id
            if perm_id is not None:
                end_ids = [pe.get('{%s}id' % w_ns) for pe in perm_ends]
                if perm_id in end_ids:
                    print("PASS: Component 3 — permEnd with matching id=%s found (0.25 pts)" % perm_id)
                    total_score += 0.25
                else:
                    print("FAIL: Component 3 — permEnd found but ids=%s don't match permStart id=%s" % (end_ids, perm_id))
            else:
                # No perm_id from component 2, but permEnd exists
                print("FAIL: Component 3 — permEnd exists but no matching permStart was validated")
        else:
            print("FAIL: Component 3 — no permEnd elements found in document body")
    except Exception as e:
        print("ERROR: Component 3 — %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = '%s/%s.docx' % (WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
