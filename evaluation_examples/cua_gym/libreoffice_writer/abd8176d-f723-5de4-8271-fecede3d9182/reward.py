"""
Reward Script: Create employee handbook 'Code of Conduct' section
Task ID: writer_wf_003
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Title 'Code of Conduct' with Heading 1 style
  Component 2 (0.35): All 5 subsections present with Heading 2 style
  Component 3 (0.25): Each subsection has >= 2 sentences of body text
  Component 4 (0.15): Table of Contents present at top of document
"""

import os
import re
from docx import Document
from docx.shared import Emu
from docx.enum.section import WD_ORIENT

WORKDIR = '/home/user'
TASK_ID = 'writer_wf_003'

EXPECTED_SUBSECTIONS = [
    'Professional Behavior',
    'Dress Code',
    'Use of Company Resources',
    'Conflict of Interest',
    'Disciplinary Procedures',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: portrait orientation and ~2.5cm margins
    # These are preconditions (already set in initial_env), so NOT scored.
    # But if the golden file somehow loses them, we note it.
    section = doc.sections[0]
    if section.orientation != WD_ORIENT.PORTRAIT:
        print("WARNING: Orientation is not portrait (precondition check)")

    paras = doc.paragraphs

    # Component 1: Title 'Code of Conduct' with Heading 1 style (0.25 points)
    # This FAILS on initial (blank doc) and PASSES on golden.
    try:
        heading1_found = False
        for para in paras:
            if para.style and para.style.name == 'Heading 1':
                if 'code of conduct' in para.text.lower():
                    heading1_found = True
                    break
        if heading1_found:
            print(f"PASS: Component 1 — 'Code of Conduct' title with Heading 1 found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — No 'Code of Conduct' paragraph with Heading 1 style found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 5 subsections present with Heading 2 style (0.35 points)
    # Award partial credit: 0.07 per subsection found.
    # This FAILS on initial (no headings) and PASSES on golden.
    try:
        heading2_texts = []
        for para in paras:
            if para.style and para.style.name == 'Heading 2':
                heading2_texts.append(para.text.strip())

        found_count = 0
        for expected in EXPECTED_SUBSECTIONS:
            matched = any(expected.lower() in h2.lower() for h2 in heading2_texts)
            if matched:
                found_count += 1
                print(f"  PASS: Subsection '{expected}' found with Heading 2")
            else:
                print(f"  FAIL: Subsection '{expected}' NOT found with Heading 2")

        sub_score = found_count * 0.07
        if found_count > 0:
            total_score += sub_score
        print(f"{'PASS' if found_count > 0 else 'FAIL'}: Component 2 — {found_count}/5 subsections found ({sub_score:.2f} pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each subsection has at least 2 sentences of body text (0.25 points)
    # We check that after each Heading 2, there are Normal paragraphs with text
    # containing at least 2 sentences (roughly: 2+ periods/exclamation/question marks).
    # Award 0.05 per subsection with adequate body text.
    # This FAILS on initial (no content) and PASSES on golden.
    try:
        subsection_body_count = 0
        for i, para in enumerate(paras):
            if para.style and para.style.name == 'Heading 2':
                # Collect body text after this heading until next heading or end
                body_text = ''
                for j in range(i + 1, len(paras)):
                    next_style = paras[j].style.name if paras[j].style else ''
                    if next_style.startswith('Heading'):
                        break
                    body_text += ' ' + paras[j].text.strip()

                # Count sentences (periods, exclamation marks, question marks)
                sentences = re.split(r'[.!?]+', body_text.strip())
                # Filter out empty strings
                sentences = [s.strip() for s in sentences if s.strip()]
                if len(sentences) >= 2:
                    subsection_body_count += 1
                    print(f"  PASS: '{para.text.strip()}' has {len(sentences)} sentences of body text")
                else:
                    print(f"  FAIL: '{para.text.strip()}' has only {len(sentences)} sentence(s) of body text")

        body_score = subsection_body_count * 0.05
        if subsection_body_count > 0:
            total_score += body_score
        print(f"{'PASS' if subsection_body_count > 0 else 'FAIL'}: Component 3 — {subsection_body_count}/5 subsections with adequate body text ({body_score:.2f} pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Table of Contents present at top of document (0.15 points)
    # Check for TOC-related content before the first Heading 1.
    # The golden file has a "Table of Contents" placeholder paragraph at index 0.
    # We also check for actual TOC field codes in the XML.
    # This FAILS on initial (blank doc) and PASSES on golden.
    try:
        toc_found = False

        # Method 1: Check for TOC-related text before first Heading 1
        for para in paras:
            if para.style and para.style.name.startswith('Heading'):
                break
            if 'table of contents' in para.text.lower() or 'contents' in para.text.lower():
                toc_found = True
                break

        # Method 2: Check for TOC field codes in the XML body
        if not toc_found:
            body_xml = doc.element.body.xml
            if 'TOC' in body_xml and ('\\o' in body_xml or 'HYPERLINK' in body_xml or 'instrText' in body_xml):
                toc_found = True

        # Method 3: Check for any SDT (structured document tag) TOC block
        if not toc_found:
            body_xml = doc.element.body.xml
            if 'w:sdt' in body_xml and ('TOC' in body_xml or 'Table of Contents' in body_xml):
                toc_found = True

        if toc_found:
            print(f"PASS: Component 4 — Table of Contents found at top of document (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — No Table of Contents found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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
