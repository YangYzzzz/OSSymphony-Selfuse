"""
Reward Script: Set line spacing of abstract paragraph to exactly 18pt,
               and body paragraphs to proportional 120%.
Task ID: wrpara_013
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Abstract paragraph has EXACTLY line spacing at 18pt
  Component 2 (0.5): All 4 body paragraphs have MULTIPLE (proportional) line spacing at 120% (1.2)
"""

import os

from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'wrpara_013'


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

    paragraphs = doc.paragraphs

    # Identify document structure:
    # Para 0: Title
    # Para 1: "Abstract" heading
    # Para 2: Abstract paragraph (the one to check)
    # Para 3: "Introduction" heading
    # Paras 4-7: Body paragraphs (4 of them)

    if len(paragraphs) < 8:
        print(f"FAIL: Expected at least 8 paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    # Find the abstract paragraph: first Normal paragraph after "Abstract" heading
    abstract_para = None
    body_paras = []
    found_abstract_heading = False
    found_intro_heading = False

    for para in paragraphs:
        text = para.text.strip()
        style = para.style.name if para.style else ''

        if 'Abstract' in text and 'Heading' in style:
            found_abstract_heading = True
            continue
        if 'Introduction' in text and 'Heading' in style:
            found_intro_heading = True
            continue

        if found_abstract_heading and not found_intro_heading and 'Heading' not in style and text:
            if abstract_para is None:
                abstract_para = para
        elif found_intro_heading and 'Heading' not in style and text:
            body_paras.append(para)

    if abstract_para is None:
        print("FAIL: Could not identify the abstract paragraph")
        print("REWARD: 0.0")
        return 0.0

    if len(body_paras) < 4:
        print(f"FAIL: Expected 4 body paragraphs, found {len(body_paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Abstract paragraph has EXACTLY line spacing at 18pt (0.5 points)
    # 18pt = 228600 EMU. Rule should be EXACTLY (4).
    try:
        pf = abstract_para.paragraph_format
        ls = pf.line_spacing
        lsr = pf.line_spacing_rule

        # line_spacing_rule EXACTLY has value 4 in python-docx
        # When set to EXACTLY, line_spacing is in EMU (228600 for 18pt)
        is_exactly = (lsr is not None and lsr == 4)  # WD_LINE_SPACING.EXACTLY = 4
        is_18pt = False
        if ls is not None:
            # ls could be EMU (int) for fixed spacing
            if isinstance(ls, int):
                # Convert EMU to pt: 1pt = 12700 EMU
                pt_val = ls / 12700.0
                is_18pt = abs(pt_val - 18.0) < 0.5
            elif hasattr(ls, 'pt'):
                is_18pt = abs(ls.pt - 18.0) < 0.5

        if is_exactly and is_18pt:
            print(f"PASS: Component 1 - Abstract paragraph has EXACTLY 18pt line spacing (ls={ls}, rule={lsr}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - Abstract paragraph line spacing: ls={ls}, rule={lsr} (expected EXACTLY/18pt)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All 4 body paragraphs have MULTIPLE (proportional) line spacing at 120% (0.5 points)
    # Proportional 120% = line_spacing=1.2, rule=MULTIPLE (5)
    try:
        body_pass_count = 0
        for idx, bp in enumerate(body_paras[:4]):
            pf = bp.paragraph_format
            ls = pf.line_spacing
            lsr = pf.line_spacing_rule

            # MULTIPLE rule has value 5
            is_multiple = (lsr is not None and lsr == 5)
            is_120 = False
            if ls is not None:
                if isinstance(ls, (int, float)):
                    is_120 = abs(float(ls) - 1.2) < 0.05
                elif hasattr(ls, 'pt'):
                    # Shouldn't be Pt for proportional, but handle gracefully
                    pass

            if is_multiple and is_120:
                print(f"  Body para {idx+1}: PASS (ls={ls}, rule={lsr})")
                body_pass_count += 1
            else:
                print(f"  Body para {idx+1}: FAIL (ls={ls}, rule={lsr}, expected MULTIPLE/1.2)")

        if body_pass_count == 4:
            print(f"PASS: Component 2 - All 4 body paragraphs have proportional 120% line spacing (0.5 pts)")
            total_score += 0.5
        elif body_pass_count > 0:
            partial = 0.5 * (body_pass_count / 4.0)
            print(f"PARTIAL: Component 2 - {body_pass_count}/4 body paragraphs correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No body paragraphs have correct line spacing")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
