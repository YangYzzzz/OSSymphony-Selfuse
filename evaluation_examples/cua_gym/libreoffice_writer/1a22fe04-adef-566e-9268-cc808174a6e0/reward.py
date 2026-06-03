"""
Reward Script: Apply 'Keep with next paragraph' to all figure captions
Task ID: writer_tech_086
Domain: libreoffice_writer
Scoring:
  Component 1 (0.2 each x 5 captions = 1.0): Each figure caption paragraph
  has keepNext enabled (not disabled with val="0").

The document has 5 figure captions (paragraphs starting with "Figure N:").
In the initial state, all have <w:keepNext w:val="0"/> (explicitly disabled).
In the golden state, all have <w:keepNext/> (enabled).

We check at the XML level because python-docx's paragraph_format.keep_with_next
returns True even when the element has val="0" (it only checks element presence).
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_086'


def is_keep_next_enabled(para):
    """
    Check if keepNext is truly enabled on a paragraph.
    In OOXML, <w:keepNext/> (no val) or <w:keepNext w:val="1"/>
    or <w:keepNext w:val="true"/> means enabled.
    <w:keepNext w:val="0"/> or <w:keepNext w:val="false"/> means disabled.
    No <w:keepNext> element at all means inherited (usually off).
    """
    pPr = para._element.find(qn('w:pPr'))
    if pPr is None:
        return False
    kn = pPr.find(qn('w:keepNext'))
    if kn is None:
        return False
    val = kn.get(qn('w:val'))
    # No val attribute means true (OOXML default for boolean toggle)
    if val is None:
        return True
    # Explicit values
    return val.lower() in ('1', 'true')


def find_caption_paragraphs(doc):
    """
    Find all paragraphs that are figure captions (start with 'Figure').
    Returns list of (index, paragraph) tuples.
    """
    captions = []
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if text.startswith('Figure') and ':' in text[:20]:
            captions.append((i, para))
    return captions


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

    # Find all caption paragraphs
    captions = find_caption_paragraphs(doc)
    expected_count = 5
    print(f"Found {len(captions)} caption paragraphs (expected {expected_count})")

    if len(captions) == 0:
        print("FAIL: No caption paragraphs found — cannot verify task")
        print("REWARD: 0.0")
        return 0.0

    # Score each caption: 0.2 points per caption with keepNext enabled
    points_per_caption = 1.0 / max(len(captions), expected_count)

    for idx, (para_idx, para) in enumerate(captions):
        caption_num = idx + 1
        caption_text = para.text.strip()[:60]

        # Component N: Figure caption N has keepNext enabled
        try:
            if is_keep_next_enabled(para):
                print(f"PASS: Caption {caption_num} (para {para_idx}) — keepNext enabled ({points_per_caption:.2f} pts) — '{caption_text}'")
                total_score += points_per_caption
            else:
                print(f"FAIL: Caption {caption_num} (para {para_idx}) — keepNext NOT enabled — '{caption_text}'")
        except Exception as e:
            print(f"ERROR: Caption {caption_num} (para {para_idx}) — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
