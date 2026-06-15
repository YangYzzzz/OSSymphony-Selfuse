"""
Reward Script: Verify footnote insertion in History_Essay.docx
Task ID: writer_pd_041
Domain: libreoffice_writer
Scoring:
  Component 1 (0.20): No placeholders remain in body text ([1]-[5] removed)
  Component 2 (0.20): Exactly 5 footnote references exist in document body
  Component 3 (0.60): Each footnote has the correct citation text (0.12 each)
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_pd_041'

# Expected footnote texts (in order)
EXPECTED_FOOTNOTES = [
    'Thompson, A History of Modern Europe, p. 142',
    'Archives of the British Museum, Collection 1847-B',
    'Cited in Parliamentary Records, Vol. 23',
    'As reported by The Times, March 15, 1923',
    'Private correspondence, Morrison Collection',
]

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


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

    # Component 1: Placeholders [1]-[5] are removed from body text (0.20 points)
    try:
        placeholders_found = []
        for para in doc.paragraphs:
            text = para.text
            for marker in ['[1]', '[2]', '[3]', '[4]', '[5]']:
                if marker in text:
                    placeholders_found.append(marker)

        if len(placeholders_found) == 0:
            print(f"PASS: Component 1 — No placeholders remain in body text (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Placeholders still present: {placeholders_found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Exactly 5 footnote references in document body (0.20 points)
    try:
        body = doc.element
        footnote_refs = body.findall('.//w:footnoteReference', NS)
        num_refs = len(footnote_refs)

        if num_refs == 5:
            print(f"PASS: Component 2 — Found exactly 5 footnote references (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected 5 footnote references, found {num_refs}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each footnote has correct citation text (0.12 points each, 0.60 total)
    try:
        # Extract footnotes from the footnotes part
        footnote_texts = {}
        for rel in doc.part.rels.values():
            if 'footnote' in str(rel.reltype).lower():
                ft_xml = rel.target_part.blob.decode('utf-8')
                root = etree.fromstring(ft_xml.encode('utf-8'))
                fns = root.findall(f'.//{{{WNS}}}footnote')
                for fn in fns:
                    fn_id = fn.get(f'{{{WNS}}}id')
                    fn_type = fn.get(f'{{{WNS}}}type', 'normal')
                    if fn_type != 'normal':
                        continue
                    # Get all text content
                    fn_text = ''.join(fn.itertext()).strip()
                    footnote_texts[fn_id] = fn_text

        # Sort by ID to get ordered footnotes
        sorted_ids = sorted(footnote_texts.keys(), key=lambda x: int(x))
        actual_texts = [footnote_texts[fid] for fid in sorted_ids]

        print(f"  Found {len(actual_texts)} normal footnotes")

        for i, expected in enumerate(EXPECTED_FOOTNOTES):
            if i < len(actual_texts):
                actual = actual_texts[i].strip()
                # Footnote text may have a leading footnote ref number; strip it
                # The actual text from itertext() includes the footnote ref mark
                # which is typically just a number. Check if text contains expected.
                if expected in actual or actual == expected:
                    print(f"PASS: Component 3.{i+1} — Footnote {i+1} text matches: '{expected}' (0.12 pts)")
                    total_score += 0.12
                else:
                    print(f"FAIL: Component 3.{i+1} — Footnote {i+1} expected '{expected}', found '{actual}'")
            else:
                print(f"FAIL: Component 3.{i+1} — Footnote {i+1} not found (only {len(actual_texts)} footnotes)")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
