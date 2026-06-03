"""
Reward Script: Verify footnotes in employment contract
Task ID: writer_hr_045
Domain: libreoffice_writer
Scoring:
  Component 1 (0.20): footnotes.xml exists with exactly 3 normal footnotes
  Component 2 (0.30): 3 footnote references in body, each in the correct paragraph
  Component 3 (0.20): Footnote near 'at-will employment' mentions at-will doctrine
  Component 4 (0.20): Footnote near 'non-compete clause' mentions state law
  Component 5 (0.10): Footnote near 'arbitration agreement' mentions arbitration process
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_045'

WML_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WML_NS}


def _get_text(element):
    """Extract all w:t text from an XML element."""
    parts = []
    for t in element.iter(f'{{{WML_NS}}}t'):
        if t.text:
            parts.append(t.text)
    return ''.join(parts)


def _get_para_text_and_refs(para_elem):
    """Return (full_text, list_of_footnoteRef_ids) for a w:p element."""
    text = _get_text(para_elem)
    refs = para_elem.findall(f'.//{{{WML_NS}}}footnoteReference')
    ref_ids = [r.get(f'{{{WML_NS}}}id') for r in refs]
    return text, ref_ids


def verify_task(file_path):
    """Verify footnote insertion with progressive scoring. Returns 0.0-1.0."""
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------
    # Component 1: footnotes.xml exists with exactly 3 normal footnotes (0.20)
    # ---------------------------------------------------------------
    normal_footnotes = {}  # id -> text
    try:
        if 'word/footnotes.xml' not in zf.namelist():
            print("FAIL: Component 1 — word/footnotes.xml not found in archive")
        else:
            fn_xml = zf.read('word/footnotes.xml')
            fn_root = etree.fromstring(fn_xml)
            for fn in fn_root.findall(f'{{{WML_NS}}}footnote'):
                fn_id = fn.get(f'{{{WML_NS}}}id')
                fn_type = fn.get(f'{{{WML_NS}}}type', 'normal')
                if fn_type == 'normal':
                    normal_footnotes[fn_id] = _get_text(fn)

            count = len(normal_footnotes)
            if count == 3:
                print(f"PASS: Component 1 — 3 normal footnotes found (ids: {list(normal_footnotes.keys())}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — expected 3 normal footnotes, found {count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: 3 footnote references in body, in correct paragraphs (0.30)
    # ---------------------------------------------------------------
    # Map: phrase keyword -> footnote id found in that paragraph
    phrase_to_fn_id = {}
    keywords = {
        'at-will': 'at-will employment',
        'non-compete': 'non-compete clause',
        'arbitration': 'arbitration agreement',
    }
    try:
        doc_xml = zf.read('word/document.xml')
        doc_root = etree.fromstring(doc_xml)
        body = doc_root.find(f'.//{{{WML_NS}}}body')

        for para in body.findall(f'.//{{{WML_NS}}}p'):
            text, ref_ids = _get_para_text_and_refs(para)
            text_lower = text.lower()
            for key, phrase in keywords.items():
                if phrase.lower() in text_lower and ref_ids:
                    # Take the first ref id found for this phrase
                    phrase_to_fn_id[key] = ref_ids[0]

        matched = len(phrase_to_fn_id)
        if matched == 3:
            print(f"PASS: Component 2 — all 3 footnote references found in correct paragraphs (0.30 pts)")
            total_score += 0.30
        elif matched > 0:
            partial = round(0.30 * matched / 3, 2)
            print(f"PARTIAL: Component 2 — {matched}/3 references found in correct paragraphs ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no footnote references found in target paragraphs")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: Footnote for 'at-will employment' has relevant content (0.20)
    # ---------------------------------------------------------------
    try:
        fn_id = phrase_to_fn_id.get('at-will')
        if fn_id and fn_id in normal_footnotes:
            fn_text = normal_footnotes[fn_id].lower()
            # Should mention at-will doctrine concepts
            has_relevant = any(kw in fn_text for kw in [
                'at-will', 'at will', 'terminate', 'termination',
                'employer', 'resign', 'doctrine', 'without cause',
            ])
            if has_relevant:
                print(f"PASS: Component 3 — at-will footnote contains relevant explanatory text (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — at-will footnote text does not mention at-will doctrine")
        else:
            print(f"FAIL: Component 3 — no footnote found for 'at-will employment' paragraph")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: Footnote for 'non-compete clause' has relevant content (0.20)
    # ---------------------------------------------------------------
    try:
        fn_id = phrase_to_fn_id.get('non-compete')
        if fn_id and fn_id in normal_footnotes:
            fn_text = normal_footnotes[fn_id].lower()
            # Should reference state law limitations
            has_relevant = any(kw in fn_text for kw in [
                'state law', 'state', 'enforce', 'enforceability',
                'restrict', 'limitation', 'california', 'jurisdiction',
                'prohibit', 'legislation',
            ])
            if has_relevant:
                print(f"PASS: Component 4 — non-compete footnote references state law limitations (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — non-compete footnote does not reference state law")
        else:
            print(f"FAIL: Component 4 — no footnote found for 'non-compete clause' paragraph")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---------------------------------------------------------------
    # Component 5: Footnote for 'arbitration agreement' has relevant content (0.10)
    # ---------------------------------------------------------------
    try:
        fn_id = phrase_to_fn_id.get('arbitration')
        if fn_id and fn_id in normal_footnotes:
            fn_text = normal_footnotes[fn_id].lower()
            # Should mention arbitration process
            has_relevant = any(kw in fn_text for kw in [
                'arbitration', 'arbitrator', 'dispute', 'resolution',
                'binding', 'hearing', 'alternative', 'neutral',
            ])
            if has_relevant:
                print(f"PASS: Component 5 — arbitration footnote describes the process (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — arbitration footnote does not describe the process")
        else:
            print(f"FAIL: Component 5 — no footnote found for 'arbitration agreement' paragraph")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    zf.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
