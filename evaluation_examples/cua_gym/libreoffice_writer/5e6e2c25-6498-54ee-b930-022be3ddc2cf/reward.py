"""
Reward Script: Set body text paragraphs to 1.5 line spacing, keep headings at single spacing
Task ID: osworld_writer_line_spacing_per_paragraph_004
Domain: libreoffice_writer
Scoring:
  Component 1: All 3 Normal/body paragraphs have 1.5 line spacing  — 0.6 points
  Component 2: All 2 Heading 1 paragraphs remain at single spacing — 0.4 points
  Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_line_spacing_per_paragraph_004'


def persist_app_state():
    """Send Ctrl+S to save any open LibreOffice Writer document."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.2)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def para_line_spacing_rule(para):
    """Return the line_spacing_rule integer value (0=SINGLE, 1=ONE_POINT_FIVE, 2=DOUBLE)."""
    lsr = para.paragraph_format.line_spacing_rule
    if lsr is not None:
        return int(lsr)
    return None


def para_line_spacing_float(para):
    """Return the line_spacing as float, or None."""
    ls = para.paragraph_format.line_spacing
    if ls is not None:
        try:
            return float(ls)
        except (TypeError, ValueError):
            pass
    return None


def check_para_is_1_5(para):
    """Return True if paragraph has 1.5 line spacing."""
    lsr = para_line_spacing_rule(para)
    if lsr == 1:  # WD_LINE_SPACING.ONE_POINT_FIVE
        return True
    ls = para_line_spacing_float(para)
    if ls is not None and abs(ls - 1.5) < 0.05:
        return True
    return False


def check_para_is_single(para):
    """Return True if paragraph has single (1.0) line spacing."""
    lsr = para_line_spacing_rule(para)
    if lsr == 0:  # WD_LINE_SPACING.SINGLE
        return True
    ls = para_line_spacing_float(para)
    if ls is not None and abs(ls - 1.0) < 0.05:
        return True
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    The document has:
      - Para 0: Heading 1 — 'Project Overview'   (should remain single/1.0 spacing)
      - Para 1: Normal    — body paragraph 1     (should become 1.5 spacing)
      - Para 2: Normal    — body paragraph 2     (should become 1.5 spacing)
      - Para 3: Heading 1 — 'Risk Assessment'    (should remain single/1.0 spacing)
      - Para 4: Normal    — body paragraph 3     (should become 1.5 spacing)

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
    if len(paragraphs) < 5:
        print(f"CRITICAL: Expected at least 5 paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    # Identify body paragraphs (Normal style) and heading paragraphs (Heading 1)
    body_para_indices = []
    heading_para_indices = []
    for i, para in enumerate(paragraphs):
        style_name = para.style.name if para.style else ''
        if style_name == 'Heading 1':
            heading_para_indices.append(i)
        elif style_name == 'Normal':
            body_para_indices.append(i)

    print(f"Document structure: {len(paragraphs)} paragraphs total")
    print(f"  Heading 1 paragraphs at indices: {heading_para_indices}")
    print(f"  Normal/body paragraphs at indices: {body_para_indices}")

    # -------------------------------------------------------------------------
    # Component 1: All 3 body (Normal) paragraphs have 1.5 line spacing (0.6 pts)
    # FAILS on initial_env (all are single spacing) — PASSES on golden_env
    # -------------------------------------------------------------------------
    try:
        expected_body_count = 3
        body_at_1_5 = sum(1 for idx in body_para_indices if check_para_is_1_5(paragraphs[idx]))
        body_not_1_5 = [idx for idx in body_para_indices if not check_para_is_1_5(paragraphs[idx])]

        for idx in body_para_indices:
            para = paragraphs[idx]
            ls = para.paragraph_format.line_spacing
            lsr = para.paragraph_format.line_spacing_rule
            if check_para_is_1_5(para):
                print(f"PASS: Body para {idx} has 1.5 line spacing (ls={ls}, rule={lsr})")
            else:
                print(f"FAIL: Body para {idx} expected 1.5 spacing, found ls={ls}, rule={lsr}")

        if body_at_1_5 == expected_body_count:
            print(f"PASS: Component 1 — all {expected_body_count} body paragraphs have 1.5 line spacing (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — only {body_at_1_5}/{expected_body_count} body paragraphs have 1.5 spacing")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: All 2 Heading 1 paragraphs remain at single (1.0) spacing (0.4 pts)
    # Awarded only when body paragraphs also have 1.5 spacing (compound gate),
    # so this returns 0.0 on initial_env where body is still at single spacing.
    # -------------------------------------------------------------------------
    try:
        expected_heading_count = 2
        headings_at_single = sum(1 for idx in heading_para_indices if check_para_is_single(paragraphs[idx]))

        for idx in heading_para_indices:
            para = paragraphs[idx]
            ls = para.paragraph_format.line_spacing
            lsr = para.paragraph_format.line_spacing_rule
            if check_para_is_single(para):
                print(f"PASS: Heading para {idx} remains at single line spacing (ls={ls}, rule={lsr})")
            else:
                print(f"FAIL: Heading para {idx} expected single spacing, found ls={ls}, rule={lsr}")

        # Gate: only award heading points when body task is also complete
        body_completed = (total_score >= 0.6)

        if headings_at_single == expected_heading_count and body_completed:
            print(f"PASS: Component 2 — all {expected_heading_count} heading paragraphs remain at single spacing (0.4 pts)")
            total_score += 0.4
        elif headings_at_single == expected_heading_count and not body_completed:
            print(f"FAIL: Component 2 — headings are single spacing but body not yet at 1.5 (0.0 pts)")
        else:
            print(f"FAIL: Component 2 — only {headings_at_single}/{expected_heading_count} headings at single spacing")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved LibreOffice GUI edits before scoring
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
