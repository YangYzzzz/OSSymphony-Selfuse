"""
Reward Script: Format poem for literary journal submission
Task ID: writer_creative_060
Domain: libreoffice_writer
Scoring:
  - Component 1: Contact block added at top (0.30 pts)
  - Component 2: Title reformatted (centered, Liberation Sans, 14pt, bold, space_before=36pt) (0.30 pts)
  - Component 3: Byline centered (0.10 pts)
  - Component 4: Poem body double-spaced (0.30 pts)
  Total: 1.0
"""

import os
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user/Desktop'
TASK_ID = 'poem_submission'

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

    paras = doc.paragraphs
    if len(paras) == 0:
        print("CRITICAL: Document has no paragraphs")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: Contact block at the top of the document (0.30 points)
    # The initial file has NO contact info. The golden file adds:
    #   Para[0]: 'Amara Johnson'
    #   Para[1]: '1520 Birch Street'
    #   Para[2]: 'Minneapolis, MN 55403'
    #   Para[3]: 'amara.johnson@email.com'
    # All single-spaced and left-aligned.
    # -------------------------------------------------------------------------
    try:
        contact_lines_expected = [
            'Amara Johnson',
            '1520 Birch Street',
            'Minneapolis, MN 55403',
            'amara.johnson@email.com',
        ]
        # Find all paragraphs matching the expected contact block content
        found_contact_lines = 0
        for expected_line in contact_lines_expected:
            for para in paras:
                if para.text.strip() == expected_line:
                    found_contact_lines += 1
                    break

        if found_contact_lines == 4:
            # Verify they appear as the first 4 paragraphs (top-left contact block)
            first_four_texts = [p.text.strip() for p in paras[:4]]
            if first_four_texts == contact_lines_expected:
                print(f"PASS: Component 1 — Full contact block present at top of document (0.30 pts)")
                total_score += 0.30
            else:
                # Partial: contact lines exist somewhere in document but not at top
                print(f"FAIL: Component 1 — Contact lines found but not at top of document. First 4 paras: {first_four_texts}")
        else:
            print(f"FAIL: Component 1 — Contact block incomplete. Found {found_contact_lines}/4 expected lines")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Title reformatted (0.30 points)
    # In initial: 'The Weight of Winter' is left-aligned, Times New Roman, 12pt, not bold
    # In golden:  centered, Liberation Sans, 14pt, bold=True, space_before≈36pt
    # We check for all 4 sub-requirements (centered, Liberation Sans, 14pt, bold).
    # space_before=36pt is also checked for a strict pass.
    # -------------------------------------------------------------------------
    try:
        title_para = None
        for para in paras:
            if 'The Weight of Winter' in para.text:
                title_para = para
                break

        if title_para is None:
            print(f"FAIL: Component 2 — Title paragraph 'The Weight of Winter' not found")
        else:
            title_checks = {}

            # Check alignment == CENTER
            title_checks['centered'] = (title_para.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER)

            # Check font properties from runs
            title_font_name = None
            title_font_size_pt = None
            title_font_bold = None
            for run in title_para.runs:
                if run.text.strip():
                    if run.font.name:
                        title_font_name = run.font.name
                    if run.font.size:
                        title_font_size_pt = run.font.size.pt
                    if run.font.bold is not None:
                        title_font_bold = run.font.bold

            # Liberation Sans (case-insensitive check for flexibility)
            title_checks['liberation_sans'] = (
                title_font_name is not None and
                'liberation sans' in title_font_name.lower()
            )
            # 14pt
            title_checks['14pt'] = (title_font_size_pt is not None and abs(title_font_size_pt - 14.0) < 0.5)
            # bold
            title_checks['bold'] = (title_font_bold is True)

            # space_before ~36pt (457200 EMU = 36pt)
            sb = title_para.paragraph_format.space_before
            if sb is not None:
                sb_pt = sb.pt if hasattr(sb, 'pt') else (sb / 12700.0)
                title_checks['space_before_36pt'] = abs(sb_pt - 36.0) < 2.0
            else:
                title_checks['space_before_36pt'] = False

            passed_checks = sum(1 for v in title_checks.values() if v)
            total_checks = len(title_checks)

            if passed_checks == total_checks:
                print(f"PASS: Component 2 — Title fully reformatted: centered, Liberation Sans, 14pt, bold, space_before=36pt (0.30 pts)")
                total_score += 0.30
            elif passed_checks >= 3:
                print(f"PARTIAL: Component 2 — Title mostly reformatted ({passed_checks}/{total_checks} checks). Details: {title_checks}")
                # Award partial credit for 3+ of 5 checks
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Title not properly reformatted ({passed_checks}/{total_checks} checks). Details: {title_checks}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Byline 'by Amara Johnson' is centered (0.10 points)
    # In initial: left-aligned. In golden: centered.
    # -------------------------------------------------------------------------
    try:
        byline_para = None
        for para in paras:
            if para.text.strip() == 'by Amara Johnson':
                byline_para = para
                break

        if byline_para is None:
            print(f"FAIL: Component 3 — Byline 'by Amara Johnson' not found")
        else:
            byline_alignment = byline_para.paragraph_format.alignment
            if byline_alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
                print(f"PASS: Component 3 — Byline is centered (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — Byline alignment is {byline_alignment}, expected CENTER")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Poem body is double-spaced (0.30 points)
    # In initial: all poem lines have line_spacing=1.0 (single).
    # In golden: all poem lines AND blank stanza separators have line_spacing=2.0.
    # Check that non-empty poem body paragraphs (not title, not byline, not contact)
    # have line_spacing=2.0.
    # -------------------------------------------------------------------------
    try:
        # Poem lines are lines from stanzas (non-empty, not title, not byline, not contact info)
        contact_texts = {
            'Amara Johnson', '1520 Birch Street',
            'Minneapolis, MN 55403', 'amara.johnson@email.com',
        }
        poem_paras = []
        for para in paras:
            txt = para.text.strip()
            if txt in contact_texts:
                continue
            if txt in ('The Weight of Winter', 'by Amara Johnson'):
                continue
            poem_paras.append(para)

        if len(poem_paras) == 0:
            print(f"FAIL: Component 4 — No poem body paragraphs found")
        else:
            double_spaced_count = 0
            total_poem_paras = len(poem_paras)
            for para in poem_paras:
                ls = para.paragraph_format.line_spacing
                # line_spacing=2.0 means double
                if ls is not None and abs(float(ls) - 2.0) < 0.1:
                    double_spaced_count += 1

            ratio = double_spaced_count / total_poem_paras if total_poem_paras > 0 else 0.0
            if ratio >= 0.9:
                print(f"PASS: Component 4 — Poem body is double-spaced ({double_spaced_count}/{total_poem_paras} paragraphs at 2.0) (0.30 pts)")
                total_score += 0.30
            elif ratio >= 0.5:
                print(f"PARTIAL: Component 4 — Poem body partially double-spaced ({double_spaced_count}/{total_poem_paras} at 2.0)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Poem body not double-spaced ({double_spaced_count}/{total_poem_paras} at 2.0, ratio={ratio:.2f})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
