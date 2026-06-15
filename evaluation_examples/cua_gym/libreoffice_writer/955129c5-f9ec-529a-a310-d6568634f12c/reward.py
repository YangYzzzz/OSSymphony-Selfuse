"""
FINAL REWARD SCRIPT - SUCCESS
Task: With font size 12 throughout, give the body paragraph double spacing, while the intro and conclusion are both single-spaced.
Generated: 2025-10-14 06:39:11
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
from docx import Document
from docx.oxml.ns import qn

"""
Reward Script for Writer Task:
"With font size 12 throughout, give the body paragraph double spacing, 
while the intro and conclusion are both single-spaced."

This script verifies three key requirements:
1. Every run in the document must use a 12-point font (or inherit 12 pt from its style).
2. All body paragraphs (every paragraph except the first and the last) must be double-spaced.
3. The intro (first paragraph) and the conclusion (last paragraph) must be single-spaced.

Progressive scoring:
• Font size check – 0.4 pts
• Body paragraph spacing – 0.3 pts
• Intro & conclusion spacing – 0.3 pts
Total possible = 1.0

The script prints detailed diagnostics for each requirement and finally prints
"REWARD: X.X" where X.X ∈ [0.0, 1.0].
"""

# -------------------------------------------------------------
# Helper: determine paragraph line-spacing type ----------------
# -------------------------------------------------------------

def _get_line_spacing_type(paragraph):
    """Return 'single', 'double', or 'other' based on the w:spacing@w:line value.

    In Word XML, line spacing is stored in twentieths of a point (twips).
    • ~240 twips → single (roughly 1.0 line)
    • ~480 twips → double (roughly 2.0 lines)
    Anything else is returned as 'other'.  If spacing isn’t specified the
    default is treated as single.
    """
    pPr = paragraph._p.pPr
    if pPr is None:
        return 'single'  # Default behaviour

    spacing = pPr.find(qn('w:spacing'))
    if spacing is None:
        return 'single'

    line_attr = spacing.get(qn('w:line'))
    if line_attr is None:
        return 'single'

    try:
        line_twips = int(line_attr)
    except ValueError:
        return 'other'

    # Classify spacing by twip range (allow small tolerance)
    if 420 <= line_twips <= 540:   # ≈480 twips
        return 'double'
    if 200 <= line_twips <= 300:   # ≈240 twips
        return 'single'
    return 'other'

# -------------------------------------------------------------
# Core verification routine -----------------------------------
# -------------------------------------------------------------

def verify_writer_task(file_path):
    """Validate the document against the specified formatting rules."""

    MAX_SCORE = 1.0
    score = 0.0

    # 1) File existence & loading (no points for this – prerequisite)
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as exc:
        print(f"✗ Error loading DOCX: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # Gather non-empty paragraphs
    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    if len(paragraphs) < 1:
        print("✗ Document contains no text paragraphs")
        print("REWARD: 0.0")
        return 0.0

    intro_paragraph = paragraphs[0]
    conclusion_paragraph = paragraphs[-1]
    body_paragraphs = paragraphs[1:-1]  # may be empty for very short docs

    # ---------------------------------------------------------
    # Requirement 1: Font size 12 pt throughout (0.4 pts)
    # ---------------------------------------------------------
    size_ok = True
    for p in paragraphs:
        for run in p.runs:
            if not run.text.strip():
                continue
            size = run.font.size
            # If size is None it inherits from style – assume style is 12pt.
            if size is not None and abs(size.pt - 12.0) > 0.2:
                print(f"✗ Font size mismatch -> '{run.text[:40]}...' is {size.pt} pt")
                size_ok = False
                break
        if not size_ok:
            break

    if size_ok:
        print("✓ All text is 12 pt font")
        score += 0.4

    # ---------------------------------------------------------
    # Requirement 2: Body paragraphs double-spaced (0.3 pts)
    # ---------------------------------------------------------
    body_ok = True
    if body_paragraphs:
        for p in body_paragraphs:
            spacing_type = _get_line_spacing_type(p)
            if spacing_type != 'double':
                print(f"✗ Body paragraph spacing error -> '{p.text[:40]}...' is {spacing_type}")
                body_ok = False
                break
    # If there are no body paragraphs (single-paragraph doc), the rule
    # cannot be satisfied, so treat as failure.
    else:
        body_ok = False
        print("✗ No body paragraphs detected – cannot verify double spacing")

    if body_ok:
        print("✓ All body paragraphs are double-spaced")
        score += 0.3

    # ---------------------------------------------------------
    # Requirement 3: Intro & conclusion single-spaced (0.3 pts)
    # ---------------------------------------------------------
    intro_spacing = _get_line_spacing_type(intro_paragraph)
    conclusion_spacing = _get_line_spacing_type(conclusion_paragraph)

    intro_ok = intro_spacing == 'single'
    conclusion_ok = conclusion_spacing == 'single'

    if intro_ok and conclusion_ok:
        print("✓ Intro and conclusion are single-spaced")
        score += 0.3
    else:
        if not intro_ok:
            print(f"✗ Intro spacing is {intro_spacing}")
        if not conclusion_ok:
            print(f"✗ Conclusion spacing is {conclusion_spacing}")

    # ---------------------------------------------------------
    final_score = min(score, MAX_SCORE)
    print(f"REWARD: {final_score}")
    return final_score

# -------------------------------------------------------------
# Execute verification when run as a script -------------------
# -------------------------------------------------------------
if __name__ == "__main__":
    file_to_check = "/home/user/with_font_size_12_throughout_give_the_body_paragraph_double_spacing_while_the_intro_and_conclusion_a.docx"
    verify_writer_task(file_to_check)

