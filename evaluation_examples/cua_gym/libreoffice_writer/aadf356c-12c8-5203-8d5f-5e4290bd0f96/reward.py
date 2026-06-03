"""
Reward Script: Accept all changes by 'External_Reviewer' but reject all changes by 'Intern_Jones'
Task ID: writer_rm_023
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): No tracked changes remain in the document
  Component 2 (0.30): External_Reviewer's 12 insertions are present as normal text (para.text)
  Component 3 (0.20): Intern_Jones's 10 insertions absent from full XML text (incl. tracked changes)
  Component 4 (0.25): Intern_Jones's 5 deleted phrases are restored in normal text (para.text)

Key insight: python-docx para.text EXCLUDES text inside <w:ins> tracked insertions.
  - On initial_env: External_Reviewer insertions are inside <w:ins> => NOT in para.text => Comp 2 FAILS
  - On golden_env: no tracked changes => all accepted text is normal => Comp 2 PASSES
  - For Comp 3: we must check the FULL XML text (including tracked changes). On initial,
    Intern_Jones insertions exist as <w:ins> nodes. On golden, they are completely removed.
  - For Comp 4: Intern_Jones deletions are <w:del> tags. On initial, the text inside is
    delText (not in para.text). On golden, the deletion was rejected so original text is restored.
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_023'


def persist_app_state(domain):
    """Save any unsaved LibreOffice Writer changes before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_writer", "libreoffice_calc", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def get_full_xml_text(doc):
    """Extract ALL text from the document XML, including text inside tracked changes.
    This includes <w:t> inside <w:ins> and <w:delText> inside <w:del>."""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = doc.element.body
    texts = []
    # Get all w:t elements (normal text + inserted text)
    for t in body.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
        if t.text:
            texts.append(t.text)
    # Also get w:delText elements (deleted text still tracked)
    for dt in body.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}delText'):
        if dt.text:
            texts.append(dt.text)
    return ' '.join(texts)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # para.text — normal text only (excludes tracked changes)
    normal_text = ' '.join(p.text for p in doc.paragraphs)
    # Full XML text — includes text inside tracked insertions and deletions
    full_xml_text = get_full_xml_text(doc)

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = doc.element.body

    # =========================================================================
    # Component 1: No tracked changes remain (0.25 points)
    # In the initial doc there are 39 tracked changes (22 ins + 17 del).
    # After accepting/rejecting all of them, zero should remain.
    # INITIAL: 39 changes => FAIL. GOLDEN: 0 changes => PASS.
    # =========================================================================
    try:
        inserts = body.findall('.//w:ins', ns)
        deletes = body.findall('.//w:del', ns)
        total_changes = len(inserts) + len(deletes)

        if total_changes == 0:
            print(f"PASS: Component 1 — No tracked changes remain (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — {total_changes} tracked changes still present (expected 0)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: External_Reviewer's insertions accepted (0.30 points)
    # These 12 phrases were inserted by External_Reviewer. Accepting them turns
    # them into normal text visible via para.text.
    # INITIAL: these are inside <w:ins> tags, so NOT in para.text => FAIL
    # GOLDEN: no tracked changes, text is normal => PASS
    # =========================================================================
    try:
        er_insertions = [
            'regulatory requirements',
            'shall comply with',
            'applicable statutes and regulations',
            'conduct periodic assessments of',
            'safeguard the confidentiality of',
            'compromised',
            'financial transaction processing',
            'gratuities, hospitality, or other inducements',
            'the Foreign Corrupt Practices Act (FCPA)',
            'report suspected violations through',
            'mandatory compliance education programs',
            'proportionate sanctions',
        ]

        er_present = 0
        for phrase in er_insertions:
            if phrase in normal_text:
                er_present += 1
            else:
                print(f"  DETAIL: External_Reviewer insertion MISSING from normal text: {repr(phrase)}")

        ratio = er_present / len(er_insertions)
        points = round(0.30 * ratio, 4)
        if er_present == len(er_insertions):
            print(f"PASS: Component 2 — All {len(er_insertions)} External_Reviewer insertions accepted ({points} pts)")
            total_score += points
        elif er_present > 0:
            print(f"PARTIAL: Component 2 — {er_present}/{len(er_insertions)} External_Reviewer insertions in normal text ({points} pts)")
            total_score += points
        else:
            print(f"FAIL: Component 2 — 0/{len(er_insertions)} External_Reviewer insertions found in normal text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: Intern_Jones's insertions rejected (0.20 points)
    # These 10 phrases were inserted by Intern_Jones. Rejecting them removes
    # them entirely from the document (not even as tracked changes).
    # We check full_xml_text which includes tracked change text.
    # INITIAL: these exist as <w:ins> nodes with <w:t> => present in full XML => FAIL
    # GOLDEN: these are completely gone (rejected) => absent from full XML => PASS
    # =========================================================================
    try:
        ij_insertions = [
            'getting in trouble',
            'This is pretty important stuff that everyone should pay attention to',
            'IT guy',
            'ways we deal with problems',
            'like free lunches or whatever',
            'people being mean to whistleblowers',
            'I think this is a lot of training lol',
            'really bad stuff',
        ]

        ij_absent = 0
        for phrase in ij_insertions:
            if phrase not in full_xml_text:
                ij_absent += 1
            else:
                print(f"  DETAIL: Intern_Jones insertion still in XML: {repr(phrase)}")

        ratio = ij_absent / len(ij_insertions)
        points = round(0.20 * ratio, 4)
        if ij_absent == len(ij_insertions):
            print(f"PASS: Component 3 — All {len(ij_insertions)} Intern_Jones insertions removed from document ({points} pts)")
            total_score += points
        elif ij_absent > 0:
            print(f"PARTIAL: Component 3 — {ij_absent}/{len(ij_insertions)} Intern_Jones insertions removed ({points} pts)")
            total_score += points
        else:
            print(f"FAIL: Component 3 — 0/{len(ij_insertions)} Intern_Jones insertions removed")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: Intern_Jones's deletions rejected — original text restored (0.25 points)
    # These 5 phrases were deleted by Intern_Jones. Rejecting those deletions
    # restores the original text as normal (non-tracked) content.
    # INITIAL: these exist only as <w:delText> inside <w:del> tags, NOT in para.text => FAIL
    # GOLDEN: deletion rejected, original text is normal => present in para.text => PASS
    # =========================================================================
    try:
        ij_deletions_restored = [
            'disciplinary review',
            'Chief Information Security Officer',
            'risk mitigation strategies',
            'retaliatory conduct',
            'criminal misconduct',
        ]

        ij_restored = 0
        for phrase in ij_deletions_restored:
            if phrase in normal_text:
                ij_restored += 1
            else:
                print(f"  DETAIL: Intern_Jones deleted text NOT restored: {repr(phrase)}")

        ratio = ij_restored / len(ij_deletions_restored)
        points = round(0.25 * ratio, 4)
        if ij_restored == len(ij_deletions_restored):
            print(f"PASS: Component 4 — All {len(ij_deletions_restored)} Intern_Jones deletions rejected, original text restored ({points} pts)")
            total_score += points
        elif ij_restored > 0:
            print(f"PARTIAL: Component 4 — {ij_restored}/{len(ij_deletions_restored)} Intern_Jones deleted phrases restored ({points} pts)")
            total_score += points
        else:
            print(f"FAIL: Component 4 — 0/{len(ij_deletions_restored)} Intern_Jones deleted phrases restored")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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
