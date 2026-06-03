"""
Reward Script: Insert footnote after citation 'Smith v. Jones, 456 U.S. 789 (2019)'
Task ID: writer_legal_008
Domain: libreoffice_writer
Scoring:
  Component 1: Footnote reference exists in body (0.3 pts)
  Component 2: Footnote ref is in paragraph containing the citation (0.3 pts)
  Component 3: Footnote text matches expected content (0.4 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_008'

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}

CITATION = 'Smith v. Jones, 456 U.S. 789 (2019)'
EXPECTED_FN_KEYWORDS = ['overruled in part', 'Williams v. State']


def get_paragraph_text(p_elem):
    """Extract full text from a w:p element."""
    texts = [t.text for t in p_elem.findall('.//w:t', NS) if t.text]
    return ' '.join(texts)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse document.xml for footnote references in body
    try:
        doc_xml = zf.read('word/document.xml').decode('utf-8')
        doc_root = ET.fromstring(doc_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse document.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all footnoteReference elements in the body
    fn_refs = doc_root.findall('.//' + f'{{{WNS}}}footnoteReference')

    # Component 1: Footnote reference exists in body (0.3 points)
    try:
        # Filter out separator/continuation refs (id=-1, id=0)
        real_refs = [r for r in fn_refs if r.get(f'{{{WNS}}}id') not in ('-1', '0', None)]
        if len(real_refs) >= 1:
            print(f"PASS: Component 1 -- Footnote reference found in body ({len(real_refs)} ref(s)) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- No footnote references found in document body")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Footnote ref is in paragraph containing the citation (0.3 points)
    try:
        comp2_awarded = 0.0
        # Find all paragraphs in document body
        body = doc_root.find(f'{{{WNS}}}body')
        if body is not None:
            for p_elem in body.iter(f'{{{WNS}}}p'):
                para_text = get_paragraph_text(p_elem)
                # Check if this paragraph contains both the citation and a footnote ref
                has_citation = CITATION in para_text
                has_fn_ref = any(
                    r.get(f'{{{WNS}}}id') not in ('-1', '0', None)
                    for r in p_elem.findall('.//' + f'{{{WNS}}}footnoteReference')
                )
                if has_citation and has_fn_ref:
                    comp2_awarded = 0.3
                    print(f"PASS: Component 2 -- Footnote ref found in paragraph containing '{CITATION}' (0.3 pts)")
                    total_score += comp2_awarded
                    break

        if comp2_awarded == 0.0:
            print(f"FAIL: Component 2 -- No footnote ref in paragraph containing '{CITATION}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Footnote text matches expected content (0.4 points)
    try:
        comp3_awarded = 0.0
        if 'word/footnotes.xml' in zf.namelist():
            fn_xml = zf.read('word/footnotes.xml').decode('utf-8')
            fn_root = ET.fromstring(fn_xml)
            for fn_elem in fn_root.findall('w:footnote', NS):
                fn_id = fn_elem.get(f'{{{WNS}}}id')
                if fn_id in ('-1', '0'):
                    continue  # skip separator/continuation
                fn_text = get_paragraph_text(fn_elem).strip()
                fn_text_lower = fn_text.lower()
                print(f"  Footnote id={fn_id} text: {repr(fn_text[:200])}")

                matches = sum(1 for kw in EXPECTED_FN_KEYWORDS if kw.lower() in fn_text_lower)
                if matches == len(EXPECTED_FN_KEYWORDS):
                    comp3_awarded = 0.4
                    break

        if comp3_awarded > 0:
            print(f"PASS: Component 3 -- Footnote text contains expected keywords: {EXPECTED_FN_KEYWORDS} (0.4 pts)")
            total_score += comp3_awarded
        else:
            print(f"FAIL: Component 3 -- Footnote text missing expected keywords {EXPECTED_FN_KEYWORDS}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    zf.close()

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
