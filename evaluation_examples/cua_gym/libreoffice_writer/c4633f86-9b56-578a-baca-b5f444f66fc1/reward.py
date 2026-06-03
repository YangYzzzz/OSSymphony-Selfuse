"""
Reward Script: Insert arbitration clause text frame at bottom of signature page
Task ID: writer_legal_060
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Text frame (framePr) exists in the document
  Component 2 (0.30): Frame contains the correct arbitration clause text
  Component 3 (0.20): Frame has visible borders (all four sides, single style)
  Component 4 (0.15): Frame is anchored to the bottom of the page
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_060'

ARBITRATION_TEXT = (
    "Any dispute arising under this Agreement shall be resolved by "
    "binding arbitration in accordance with the rules of the "
    "American Arbitration Association."
)

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

    # Find all paragraphs that have a framePr element (text frame)
    frame_paras = []
    for para in doc.paragraphs:
        pPr = para._element.find('w:pPr', NS)
        if pPr is not None:
            framePr = pPr.find('w:framePr', NS)
            if framePr is not None:
                frame_paras.append(para)

    # Component 1: Text frame (framePr) exists (0.35 points)
    try:
        if len(frame_paras) > 0:
            print(f"PASS: Component 1 — framePr element found ({len(frame_paras)} text frame paragraph(s)) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — No framePr element found in any paragraph")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if not frame_paras:
        # No text frame found, remaining checks impossible
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Find the frame paragraph that contains arbitration text (or pick the first one)
    target_para = None
    for fp in frame_paras:
        if 'arbitration' in fp.text.lower() or 'dispute' in fp.text.lower():
            target_para = fp
            break
    if target_para is None:
        target_para = frame_paras[0]

    # Component 2: Frame contains arbitration clause text (0.30 points)
    try:
        para_text = target_para.text.strip()
        # Normalize whitespace for comparison
        norm_actual = ' '.join(para_text.split()).lower()
        norm_expected = ' '.join(ARBITRATION_TEXT.split()).lower()

        if norm_expected in norm_actual or norm_actual in norm_expected:
            print(f"PASS: Component 2 — Arbitration clause text found in frame (0.30 pts)")
            total_score += 0.30
        else:
            # Check for key phrases as partial match
            key_phrases = ['binding arbitration', 'american arbitration association', 'dispute arising']
            matches = sum(1 for kp in key_phrases if kp in norm_actual)
            if matches >= 2:
                print(f"PASS: Component 2 — Arbitration clause text found (partial match {matches}/3 key phrases) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — Expected arbitration clause text, found: '{para_text[:100]}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Frame has visible borders on all four sides (0.20 points)
    try:
        pPr = target_para._element.find('w:pPr', NS)
        pBdr = pPr.find('w:pBdr', NS) if pPr is not None else None

        if pBdr is not None:
            border_sides = ['top', 'left', 'bottom', 'right']
            borders_found = 0
            for side in border_sides:
                border_elem = pBdr.find(f'w:{side}', NS)
                if border_elem is not None:
                    val = border_elem.get(f'{{{WNS}}}val')
                    if val is not None and val != 'none' and val != 'nil':
                        borders_found += 1

            if borders_found == 4:
                print(f"PASS: Component 3 — All 4 borders present with visible style (0.20 pts)")
                total_score += 0.20
            elif borders_found > 0:
                partial = round(0.20 * borders_found / 4, 2)
                print(f"PARTIAL: Component 3 — {borders_found}/4 borders found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No visible borders found on frame paragraph")
        else:
            print(f"FAIL: Component 3 — No pBdr element found on frame paragraph")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Frame is anchored to bottom of page (0.15 points)
    try:
        pPr = target_para._element.find('w:pPr', NS)
        framePr = pPr.find('w:framePr', NS) if pPr is not None else None

        if framePr is not None:
            vAnchor = framePr.get(f'{{{WNS}}}vAnchor')
            yAlign = framePr.get(f'{{{WNS}}}yAlign')
            y_val = framePr.get(f'{{{WNS}}}y')

            # The frame should be positioned at the bottom of the page
            # yAlign="bottom" with vAnchor="page" is the ideal case
            # Also accept large y values indicating bottom positioning
            is_bottom = (yAlign == 'bottom') or (y_val is not None and int(y_val) > 12000)
            page_anchored = (vAnchor == 'page')

            if is_bottom and page_anchored:
                print(f"PASS: Component 4 — Frame anchored to bottom of page (vAnchor={vAnchor}, yAlign={yAlign}) (0.15 pts)")
                total_score += 0.15
            elif is_bottom:
                print(f"PARTIAL: Component 4 — Frame at bottom but vAnchor={vAnchor} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — Frame not at bottom (vAnchor={vAnchor}, yAlign={yAlign}, y={y_val})")
        else:
            print(f"FAIL: Component 4 — No framePr element found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
