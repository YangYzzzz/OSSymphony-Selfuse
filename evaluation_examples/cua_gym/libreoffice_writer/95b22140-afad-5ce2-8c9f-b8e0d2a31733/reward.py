"""
Reward Script: Protect the section named 'Confidential Terms' so its content cannot be edited.
Task ID: writer_struct_020
Domain: libreoffice_writer
Scoring:
  Component 1: 'Confidential Terms' SDT section has w:lock=sdtContentLocked (0.6 pts)
  Component 2: Section protection is active AND content paragraphs are intact (0.4 pts)
  Total: 1.0

Note: Component 2 is gated on the lock being active from Component 1,
ensuring it only awards points in the golden state (not the initial state).
"""

import os
from docx import Document
import lxml.etree as etree

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_020'

# XML namespace for OOXML
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W = '{' + W_NS + '}'

# Expected content in the 'Confidential Terms' section (two paragraphs)
EXPECTED_PARA_SUBSTRINGS = [
    'parties acknowledge that all information exchanged under this Agreement constitutes highly sensitive',
    'breach of the confidentiality obligations set forth in this section shall entitle the Disclosing Party',
]

PROTECTED_LOCK_VALUES = ('sdtContentLocked', 'sdtLocked')


def find_confidential_terms_sdt(doc):
    """
    Find the SDT (Structured Document Tag / content control) representing
    the 'Confidential Terms' section by its alias or tag attribute.
    Returns (sdtPr, sdtContent) or (None, None) if not found.
    """
    body = doc.element.body
    for sdt in body.iter(W + 'sdt'):
        sdtPr = sdt.find(W + 'sdtPr')
        if sdtPr is not None:
            alias = sdtPr.find(W + 'alias')
            tag = sdtPr.find(W + 'tag')
            alias_val = alias.get(W + 'val') if alias is not None else None
            tag_val = tag.get(W + 'val') if tag is not None else None
            if alias_val == 'Confidential Terms' or tag_val == 'Confidential Terms':
                sdtContent = sdt.find(W + 'sdtContent')
                return sdtPr, sdtContent
    return None, None


def get_lock_value(sdtPr):
    """
    Read the w:lock/@w:val from an sdtPr element.
    Returns the string value, or None if not present.
    """
    lock = sdtPr.find(W + 'lock')
    if lock is None:
        return None
    return lock.get(W + 'val')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the 'Confidential Terms' section SDT
    try:
        sdtPr, sdtContent = find_confidential_terms_sdt(doc)
    except Exception as e:
        print(f"CRITICAL: Error searching for 'Confidential Terms' section: {e}")
        print("REWARD: 0.0")
        return 0.0

    if sdtPr is None:
        print("FAIL: 'Confidential Terms' SDT section not found in document — section may have been deleted")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'Confidential Terms' SDT section has w:lock = sdtContentLocked (0.6 points)
    # The task asks to make the section read-only (protected). In OOXML, this is achieved by
    # setting w:lock/@w:val to 'sdtContentLocked' on the SDT's sdtPr element.
    # Initial state: no w:lock element (lock_val = None) → FAILS
    # Golden state: w:lock val='sdtContentLocked' → PASSES
    try:
        lock_val = get_lock_value(sdtPr)
        if lock_val in PROTECTED_LOCK_VALUES:
            print(f"PASS: Component 1 — 'Confidential Terms' section has protection lock={lock_val!r} (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — 'Confidential Terms' section lock={lock_val!r}, expected one of {PROTECTED_LOCK_VALUES}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Content paragraphs are intact GIVEN protection lock is active (0.4 points)
    # Gated on lock_val (not the initial state) so this component cannot pass in initial_env.
    # In initial state: lock_val is None → gate condition fails → 0 pts
    # In golden state: lock_val is 'sdtContentLocked' AND content is intact → PASSES (0.4 pts)
    try:
        lock_val = get_lock_value(sdtPr)
        if lock_val not in PROTECTED_LOCK_VALUES:
            print("SKIP: Component 2 — Skipped because section protection (Component 1) is not active")
        elif sdtContent is None:
            print("FAIL: Component 2 — No sdtContent found inside 'Confidential Terms' section")
        else:
            # Extract all paragraph texts from the section content
            para_texts = []
            for para in sdtContent.iter(W + 'p'):
                texts = []
                for t in para.iter(W + 't'):
                    texts.append(t.text or '')
                para_texts.append(''.join(texts))

            # Verify the two expected NDA obligation paragraphs are present
            found_count = 0
            for expected_substr in EXPECTED_PARA_SUBSTRINGS:
                matched = any(expected_substr.lower() in pt.lower() for pt in para_texts)
                if matched:
                    found_count += 1
                else:
                    print(f"FAIL: Component 2 — Expected paragraph '{expected_substr[:60]}...' not found in section")

            if found_count == len(EXPECTED_PARA_SUBSTRINGS):
                print(f"PASS: Component 2 — All {found_count} content paragraphs intact under active protection (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — Only {found_count}/{len(EXPECTED_PARA_SUBSTRINGS)} expected paragraphs found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/nda_template.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
