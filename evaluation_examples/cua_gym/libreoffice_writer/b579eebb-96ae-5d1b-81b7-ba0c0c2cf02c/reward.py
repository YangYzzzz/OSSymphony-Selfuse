"""
Reward Script: Convert footnote 2 on page 3 into an endnote
Task ID: writer_struct_031
Domain: libreoffice_writer
Scoring:
  Component 1: Footnote 2 (Thompson reference) removed from footnotes (0.3 pts)
  Component 2: Endnote created with exact Thompson reference text (0.5 pts)
  Component 3: Remaining footnotes (1 and 3) are preserved intact (0.2 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_struct_031'

# Ground truth from task context
THOMPSON_TEXT = 'Thompson, E.P., The Making of the English Working Class, 1963, p. 214.'
FOOTNOTE1_TEXT = 'Mokyr, Joel, The Enlightened Economy: An Economic History of Britain 1700-1850, Yale University Press, 2009, p. 47.'
FOOTNOTE3_TEXT = 'Berg, Maxine, The Age of Manufactures, 1700-1820: Industry, Innovation and Work in Britain, Routledge, 1994, p. 312.'

NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def get_note_texts(docx_path, part_name):
    """Extract text from a footnotes.xml or endnotes.xml part inside the docx."""
    result = {}
    with zipfile.ZipFile(docx_path) as z:
        if part_name not in z.namelist():
            return result
        content = z.read(part_name).decode('utf-8')
    root = ET.fromstring(content)
    tag = '{' + NS + '}footnote' if 'footnote' in part_name else '{' + NS + '}endnote'
    for note in root.findall(tag):
        note_id = note.attrib.get('{' + NS + '}id')
        text = ''.join(t.text or '' for t in note.iter('{' + NS + '}t'))
        result[note_id] = text
    return result


def get_body_references(docx_path, ref_tag):
    """Count body references to footnotes or endnotes in the document body."""
    with zipfile.ZipFile(docx_path) as z:
        if 'word/document.xml' not in z.namelist():
            return []
        content = z.read('word/document.xml').decode('utf-8')
    root = ET.fromstring(content)
    full_tag = '{' + NS + '}' + ref_tag
    refs = root.findall('.//' + full_tag)
    return [r.attrib.get('{' + NS + '}id') for r in refs]


def verify_task(file_path):
    """
    Verify task: footnote 2 converted to endnote with same text.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must be loadable as a valid docx (zip)
    try:
        with zipfile.ZipFile(file_path) as z:
            names = z.namelist()
        if 'word/document.xml' not in names or 'word/footnotes.xml' not in names:
            print(f"CRITICAL: Not a valid docx or missing footnotes.xml: {names}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read footnote and endnote data
    try:
        footnotes = get_note_texts(file_path, 'word/footnotes.xml')
        endnotes = get_note_texts(file_path, 'word/endnotes.xml')
        fn_body_refs = get_body_references(file_path, 'footnoteReference')
        en_body_refs = get_body_references(file_path, 'endnoteReference')
    except Exception as e:
        print(f"CRITICAL: Cannot parse note XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Footnote 2 (Thompson reference) has been removed from footnotes (0.3 pts)
    # This FAILS on initial (footnote 2 with Thompson text exists) → PASSES on golden (no footnote 2)
    try:
        # Check both: no footnote with id='2' in footnotes.xml AND no body reference to footnote 2
        fn2_in_xml = '2' in footnotes
        fn2_text = footnotes.get('2', '')
        fn2_is_thompson = THOMPSON_TEXT in fn2_text

        fn2_body_ref = '2' in fn_body_refs

        if (not fn2_is_thompson) and (not fn2_body_ref):
            print(f"PASS: Component 1 — Footnote 2 (Thompson reference) removed from footnotes (0.3 pts)")
            total_score += 0.3
        else:
            if fn2_is_thompson:
                print(f"FAIL: Component 1 — Thompson text still found as footnote id=2: '{fn2_text[:60]}...'")
            elif fn2_body_ref:
                print(f"FAIL: Component 1 — Body still references footnote id=2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: An endnote exists containing the exact Thompson reference text (0.5 pts)
    # This FAILS on initial (no endnotes.xml) → PASSES on golden (endnote with Thompson text exists)
    try:
        # Find endnotes with Thompson text (skip separator ids -1 and 0)
        matching_endnotes = [
            en_id for en_id, en_text in endnotes.items()
            if en_id not in ('-1', '0') and THOMPSON_TEXT in en_text
        ]
        if len(matching_endnotes) >= 1:
            print(f"PASS: Component 2 — Endnote id={matching_endnotes[0]} contains exact Thompson text (0.5 pts)")
            total_score += 0.5
        else:
            has_en_body_ref = any(r not in ('-1', '0') for r in en_body_refs if r is not None)
            if not has_en_body_ref:
                print(f"FAIL: Component 2 — No endnote with Thompson text found. Endnotes: {endnotes}")
            else:
                print(f"FAIL: Component 2 — Endnote body reference exists but text does not match '{THOMPSON_TEXT[:40]}...'")
                print(f"  Found endnotes: {endnotes}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Remaining footnotes (1 and 3) are preserved with correct text (0.2 pts)
    # This FAILS on initial ONLY if footnotes 1 or 3 are also missing/changed (they exist in initial)
    # BUT combined with Component 1 (footnote 2 must be gone), this component tests the preservation
    # We combine: footnotes 1 and 3 exist AND footnote 2 is gone
    # Since initial has fn 1, 2, 3 (fn2 present), and golden has fn 1, 3 (fn2 absent),
    # the "right configuration" of exactly fn1 and fn3 only fails on initial (which also has fn2).
    try:
        fn1_text = footnotes.get('1', '')
        fn3_text = footnotes.get('3', '')
        fn1_ok = FOOTNOTE1_TEXT in fn1_text
        fn3_ok = FOOTNOTE3_TEXT in fn3_text
        # Also require that footnote 2 is NOT present (to ensure this doesn't score on initial)
        fn2_gone = '2' not in footnotes or (THOMPSON_TEXT not in footnotes.get('2', ''))

        if fn1_ok and fn3_ok and fn2_gone:
            print(f"PASS: Component 3 — Footnotes 1 and 3 preserved, footnote 2 absent from footnotes (0.2 pts)")
            total_score += 0.2
        else:
            if not fn1_ok:
                print(f"FAIL: Component 3 — Footnote 1 text mismatch. Found: '{fn1_text[:60]}'")
            if not fn3_ok:
                print(f"FAIL: Component 3 — Footnote 3 text mismatch. Found: '{fn3_text[:60]}'")
            if not fn2_gone:
                print(f"FAIL: Component 3 — Footnote 2 (Thompson) still present in footnotes")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/history_essay.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
