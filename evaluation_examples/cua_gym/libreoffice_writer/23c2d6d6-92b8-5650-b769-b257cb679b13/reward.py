"""
Reward Script: Legal memorandum footnote insertion verification
Task ID: writer_legal_051
Domain: libreoffice_writer
Scoring:
  Component 1 (0.20): Exactly 5 footnotes exist in the document
  Component 2 (0.16): Footnote after 'due process rights' cites Amendment XIV
  Component 3 (0.16): Footnote after 'equal protection' cites Brown v. Board, 347 U.S. 483
  Component 4 (0.16): Footnote after 'strict scrutiny' cites Grutter v. Bollinger, 539 U.S. 306
  Component 5 (0.16): Footnote after 'rational basis' cites Williamson v. Lee Optical, 348 U.S. 483
  Component 6 (0.16): Footnote after 'compelling interest' cites Burson v. Freeman, 504 U.S. 191
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_051'
WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def extract_footnotes_and_refs(file_path):
    """
    Parse the docx ZIP to extract:
    1. footnote_texts: dict mapping footnote ID -> full text content
    2. ref_contexts: dict mapping footnote ID -> text preceding the reference in the body
    Returns (footnote_texts, ref_contexts, normal_footnote_count)
    """
    footnote_texts = {}
    ref_contexts = {}
    normal_count = 0

    with zipfile.ZipFile(file_path) as z:
        # Parse footnotes.xml (may not exist if no footnotes)
        if 'word/footnotes.xml' not in z.namelist():
            return {}, {}, 0

        fn_xml = z.read('word/footnotes.xml')
        fn_root = ET.fromstring(fn_xml)

        for fn in fn_root.findall(f'{{{WNS}}}footnote'):
            fn_id = fn.attrib.get(f'{{{WNS}}}id', '')
            fn_type = fn.attrib.get(f'{{{WNS}}}type', 'normal')
            if fn_type != 'normal':
                continue
            normal_count += 1
            text_parts = []
            for t in fn.iter(f'{{{WNS}}}t'):
                if t.text:
                    text_parts.append(t.text)
            footnote_texts[fn_id] = ''.join(text_parts).strip()

        # Parse document.xml to find footnote references and preceding text
        doc_xml = z.read('word/document.xml')
        doc_root = ET.fromstring(doc_xml)

        for para in doc_root.iter(f'{{{WNS}}}p'):
            refs = list(para.iter(f'{{{WNS}}}footnoteReference'))
            if not refs:
                continue

            # Walk elements in order to capture text preceding each ref
            collected_text = []
            for elem in para.iter():
                if elem.tag == f'{{{WNS}}}t' and elem.text:
                    collected_text.append(elem.text)
                elif elem.tag == f'{{{WNS}}}footnoteReference':
                    ref_id = elem.attrib.get(f'{{{WNS}}}id', '')
                    ref_contexts[ref_id] = ''.join(collected_text).lower()
                    collected_text = []

    return footnote_texts, ref_contexts, normal_count


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        footnote_texts, ref_contexts, normal_count = extract_footnotes_and_refs(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Exactly 5 normal footnotes exist (0.20 points)
    try:
        if normal_count == 5 and len(ref_contexts) == 5:
            print(f"PASS: Component 1 -- 5 footnotes found ({normal_count} texts, {len(ref_contexts)} refs) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- expected 5 footnotes, found {normal_count} texts and {len(ref_contexts)} refs")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Build a mapping: anchor_phrase -> footnote_text by matching ref context
    # Each anchor phrase and its required citation keywords
    checks = [
        {
            "component": 2,
            "anchor": "due process rights",
            "citation_keywords": ["amendment xiv"],
            "description": "Amendment XIV",
            "points": 0.16,
        },
        {
            "component": 3,
            "anchor": "equal protection",
            "citation_keywords": ["brown v. board", "347 u.s. 483"],
            "description": "Brown v. Board, 347 U.S. 483",
            "points": 0.16,
        },
        {
            "component": 4,
            "anchor": "strict scrutiny",
            "citation_keywords": ["grutter v. bollinger", "539 u.s. 306"],
            "description": "Grutter v. Bollinger, 539 U.S. 306",
            "points": 0.16,
        },
        {
            "component": 5,
            "anchor": "rational basis",
            "citation_keywords": ["williamson v. lee optical", "348 u.s. 483"],
            "description": "Williamson v. Lee Optical, 348 U.S. 483",
            "points": 0.16,
        },
        {
            "component": 6,
            "anchor": "compelling interest",
            "citation_keywords": ["burson v. freeman", "504 u.s. 191"],
            "description": "Burson v. Freeman, 504 U.S. 191",
            "points": 0.16,
        },
    ]

    for check in checks:
        comp = check["component"]
        anchor = check["anchor"]
        keywords = check["citation_keywords"]
        desc = check["description"]
        pts = check["points"]

        try:
            # Find which footnote ref is preceded by text containing the anchor phrase
            matched_fn_id = None
            for ref_id, context in ref_contexts.items():
                if anchor in context:
                    matched_fn_id = ref_id
                    break

            if matched_fn_id is None:
                print(f"FAIL: Component {comp} -- no footnote ref found after '{anchor}'")
                continue

            fn_text = footnote_texts.get(matched_fn_id, "")
            fn_text_lower = fn_text.lower()

            # Check all required keywords are present in the footnote text
            all_found = all(kw in fn_text_lower for kw in keywords)

            if all_found:
                print(f"PASS: Component {comp} -- footnote after '{anchor}' correctly cites {desc}: [{fn_text}] ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component {comp} -- footnote after '{anchor}' expected {desc}, found: [{fn_text}]")
        except Exception as e:
            print(f"ERROR: Component {comp} -- {e}")

    final_score = round(min(total_score, 1.0), 2)
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
