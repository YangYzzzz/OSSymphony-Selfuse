"""
Reward Script: Insert alphabetical index of key terms in technical proposal
Task ID: writer_biz_070
Domain: libreoffice_writer
Scoring:
  Component 1 (0.50): XE index entries exist for all 5 required terms
  Component 2 (0.25): INDEX field code exists in the document
  Component 3 (0.25): Index heading/section exists at end of document
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_070'

# The 5 terms that must be marked for indexing
REQUIRED_TERMS = [
    'SLA',
    'API Integration',
    'Data Migration',
    'Cloud Infrastructure',
    'Disaster Recovery',
]


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

    # Parse all instrText fields from the document XML
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = doc.element.body
    all_instr = body.findall('.//w:instrText', ns)
    instr_texts = [f.text.strip() for f in all_instr if f.text]

    # Collect XE entries and check for INDEX field
    xe_entries = []
    has_index_field = False
    for txt in instr_texts:
        # XE fields look like: XE "Term Name"
        xe_match = re.match(r'XE\s+"(.+?)"', txt)
        if xe_match:
            xe_entries.append(xe_match.group(1))
        # INDEX field
        if txt.upper().startswith('INDEX'):
            has_index_field = True

    xe_unique_terms = set(xe_entries)
    print(f"DEBUG: Found {len(xe_entries)} XE entries for terms: {xe_unique_terms}")
    print(f"DEBUG: INDEX field present: {has_index_field}")

    # Component 1: XE index entries exist for all 5 required terms (0.50 points)
    # Each term is worth 0.10 points
    try:
        terms_found = 0
        for term in REQUIRED_TERMS:
            if term in xe_unique_terms:
                print(f"PASS: XE entry found for '{term}' (0.10 pts)")
                terms_found += 1
                total_score += 0.10
            else:
                print(f"FAIL: No XE entry found for '{term}'")
        print(f"Component 1 summary: {terms_found}/5 terms marked ({terms_found * 0.10:.2f}/0.50 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: INDEX field code exists in the document (0.25 points)
    # This is the field that generates the actual alphabetical index
    try:
        if has_index_field:
            print(f"PASS: Component 2 — INDEX field code found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — No INDEX field code found in document")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Index heading/section exists at end of document (0.25 points)
    # The golden file has an "Index" heading near the end of the document
    try:
        # Check the last few paragraphs for an index heading
        paragraphs = doc.paragraphs
        found_index_heading = False
        # Look in the last 10 paragraphs for a heading containing "Index"
        search_range = paragraphs[-10:] if len(paragraphs) >= 10 else paragraphs
        for para in search_range:
            style_name = para.style.name if para.style else ''
            text = para.text.strip().lower()
            if 'index' in text and ('Heading' in style_name or 'heading' in style_name):
                found_index_heading = True
                print(f"PASS: Component 3 — Index heading found: '{para.text}' (style: {style_name}) (0.25 pts)")
                break

        if not found_index_heading:
            # Fallback: check for any paragraph near the end with "index" in text
            # even if not a heading style (might use different formatting)
            for para in search_range:
                text = para.text.strip().lower()
                if text == 'index' or text == 'alphabetical index':
                    found_index_heading = True
                    print(f"PASS: Component 3 — Index section found: '{para.text}' (0.25 pts)")
                    break

        if found_index_heading:
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — No Index heading/section found at end of document")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
