"""
Reward Script: Insert page numbers in the header at the right side instead of the footer.
Task ID: writer_page_055
Domain: libreoffice_writer
Scoring:
  - Component 1: Header contains PAGE field code (instrText) — 0.5 pts
  - Component 2: Header paragraph with PAGE field is right-aligned — 0.3 pts
  - Component 3: Footer has no PAGE field code (footer cleared/emptied) — 0.2 pts
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_page_055'


def paragraphs_with_page_field(container):
    """Return list of paragraphs that contain a PAGE field code via instrText."""
    result = []
    for para in container.paragraphs:
        xml_str = para._element.xml
        if 'instrText' in xml_str:
            instrs = re.findall(r'<w:instrText[^>]*>(.*?)</w:instrText>', xml_str)
            for instr in instrs:
                if 'PAGE' in instr.upper():
                    result.append(para)
                    break
    return result


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Insert page numbers in the header at the right side instead of the footer.
    Initial state: Footer has centered PAGE field code; header is empty.
    Golden state: Header has right-aligned PAGE field code; footer is cleared (no PAGE).
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: at least one section exists
    try:
        section = doc.sections[0]
    except Exception as e:
        print(f"CRITICAL: Cannot access section: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Header contains a PAGE field code (0.5 points)
    # FAILS on initial (header paragraph has no instrText/PAGE field code)
    # PASSES on golden (header paragraph has instrText with PAGE)
    try:
        header = section.header
        header_page_paras = paragraphs_with_page_field(header)

        if len(header_page_paras) > 0:
            print(f"PASS: Component 1 — Header contains PAGE field code in {len(header_page_paras)} paragraph(s) (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 1 — Header does not contain any PAGE field code")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Header paragraph with PAGE field is right-aligned (0.3 points)
    # FAILS on initial (header has no PAGE para; even if checked, no jc="right")
    # PASSES on golden (header PAGE para has jc w:val="right")
    try:
        header = section.header
        header_page_paras = paragraphs_with_page_field(header)

        # Count paragraphs that are both page-field-containing and right-aligned
        right_aligned_count = sum(
            1 for para in header_page_paras
            if para.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.RIGHT
            or 'w:val="right"' in para._element.xml
        )

        if right_aligned_count > 0:
            print(f"PASS: Component 2 — Header PAGE field paragraph is right-aligned (0.3 pts)")
            total_score += 0.3
        else:
            if len(header_page_paras) == 0:
                print("FAIL: Component 2 — No PAGE field in header to check alignment")
            else:
                # Get actual alignment for debug
                alignments = [str(p.paragraph_format.alignment) for p in header_page_paras]
                print(f"FAIL: Component 2 — Header PAGE field paragraph not right-aligned; alignments: {alignments}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Footer has no PAGE field code (footer cleared/disabled) (0.2 points)
    # FAILS on initial (footer contains instrText PAGE with center alignment)
    # PASSES on golden (footer paragraph has no instrText)
    try:
        footer = section.footer
        footer_page_paras = paragraphs_with_page_field(footer)

        if len(footer_page_paras) == 0:
            print("PASS: Component 3 — Footer has no PAGE field code (footer cleared) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Footer still contains PAGE field code in {len(footer_page_paras)} paragraph(s); should be cleared")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/white_paper.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
