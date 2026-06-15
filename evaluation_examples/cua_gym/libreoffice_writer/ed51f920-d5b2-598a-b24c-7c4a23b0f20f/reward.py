"""
Reward Script: Insert a horizontal line separator after the third paragraph on page 1.
Task ID: writer_obj_009
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): The third body paragraph (Para index 3) has a bottom border (horizontal line)
  Component 2 (0.4): The bottom border is on the correct paragraph (3rd body paragraph, between
                     paragraphs 3 and 4), and no other body paragraphs have unexpected bottom borders
Total: 1.0

The document 'report_draft.docx' has 6 paragraphs:
  [0] Heading 1 — "Quarterly Business Performance Report"
  [1] Normal    — First body paragraph (overview)
  [2] Normal    — Second body paragraph (sales)
  [3] Normal    — Third body paragraph (operations) ← horizontal line separator goes here (bottom border)
  [4] Normal    — Fourth body paragraph (HR)
  [5] Normal    — Fifth body paragraph (looking ahead)

A horizontal line separator is implemented as a paragraph bottom border (w:pBdr/w:bottom) in .docx format.
"""

import os

from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_009'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'report_draft.docx')


def get_bottom_border(para):
    """Return the <w:bottom> element from paragraph's pBdr, or None if not present."""
    pPr = para._element.find(qn('w:pPr'))
    if pPr is None:
        return None
    pBdr = pPr.find(qn('w:pBdr'))
    if pBdr is None:
        return None
    bottom = pBdr.find('{%s}bottom' % W_NS)
    return bottom


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Precondition: verify document has expected structure (at least 5 body paragraphs)
    # Paragraphs: index 0 is heading, indices 1-5 are body paragraphs
    paragraphs = doc.paragraphs
    if len(paragraphs) < 4:
        print("CRITICAL: Document has fewer paragraphs than expected (%d). Cannot verify." % len(paragraphs))
        print("REWARD: 0.0")
        return 0.0

    # The "third paragraph" refers to the 3rd body paragraph after the heading.
    # Paragraph indices: [0]=Heading, [1]=1st body, [2]=2nd body, [3]=3rd body
    # A horizontal line separator after the 3rd body paragraph is implemented as
    # a bottom border (w:pBdr/w:bottom) on the 3rd body paragraph (index 3).
    THIRD_PARA_IDX = 3  # 0-indexed: heading=0, body1=1, body2=2, body3=3

    # Component 1: The third body paragraph (Para index 3) has a bottom border (0.6 points)
    # This is the primary task requirement: a horizontal line after the 3rd paragraph.
    try:
        third_para = paragraphs[THIRD_PARA_IDX]
        bottom_border = get_bottom_border(third_para)
        if bottom_border is not None:
            border_val = bottom_border.get('{%s}val' % W_NS, 'none')
            border_sz = bottom_border.get('{%s}sz' % W_NS, 'none')
            print("PASS: Component 1 — Para[3] has bottom border (val=%s, sz=%s) (0.6 pts)" % (border_val, border_sz))
            total_score += 0.6
        else:
            print("FAIL: Component 1 — Para[3] '%s...' has no bottom border (horizontal line missing)" % third_para.text[:40])
    except IndexError:
        print("ERROR: Component 1 — Para[3] does not exist in document")
    except Exception as e:
        print("ERROR: Component 1 — %s" % e)

    # Component 2: The bottom border is on the correct paragraph and is a valid separator style (0.4 points)
    # This verifies: the border is on the right paragraph (3rd body para, not heading or other paras),
    # AND no other unexpected body paragraphs (4 and 5) have bottom borders that would indicate
    # the change was applied to the wrong paragraph.
    try:
        third_para = paragraphs[THIRD_PARA_IDX]
        bottom_border = get_bottom_border(third_para)

        if bottom_border is None:
            print("FAIL: Component 2 — Para[3] has no bottom border; cannot confirm correct placement")
        else:
            # Check that the border value is a valid line style (not 'nil' or 'none')
            border_val = bottom_border.get('{%s}val' % W_NS, 'none')
            is_valid_style = border_val not in ('nil', 'none', '')

            if not is_valid_style:
                print("FAIL: Component 2 — Para[3] bottom border has invalid/empty val='%s'" % border_val)
            else:
                # Confirm the heading (Para[0]) does NOT have an unexpected bottom border from this task
                # (it may have style-driven borders, but not task-added pBdr borders)
                heading_para = paragraphs[0]
                heading_has_pbdr_bottom = get_bottom_border(heading_para) is not None

                # Check that Para[4] and Para[5] (4th and 5th body paras) do not have bottom borders
                # which would indicate misplacement
                misplaced_borders = []
                for idx in [1, 2, 4, 5]:
                    if idx < len(paragraphs):
                        p = paragraphs[idx]
                        if get_bottom_border(p) is not None:
                            misplaced_borders.append(idx)

                if misplaced_borders:
                    print("FAIL: Component 2 — Unexpected bottom borders found on paras %s (misplaced separator)" % misplaced_borders)
                else:
                    print("PASS: Component 2 — Border is correctly placed on Para[3] only, no misplaced borders (0.4 pts)")
                    total_score += 0.4

    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.1f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


if not os.path.exists(FILE_PATH):
    print("File not found: %s" % FILE_PATH)
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
