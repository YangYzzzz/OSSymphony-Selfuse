"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please format the introduction and conclusion with single spacing and the body with 1.5 spacing, all at 12 pt.
Generated: 2025-10-14 07:45:05
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
from docx import Document


def verify_writer_spacing_task(file_path: str) -> float:
    """Verify that:
    1. Introduction and conclusion paragraphs use single line spacing (≈1.0)
    2. Body paragraphs use 1.5 line spacing (≈1.5)
    3. Every run of text inside the evaluated paragraphs is 12 pt font

    Progressive scoring (adds up to 1.0):
        • Intro & Conclusion spacing correct ............ 0.3
        • Body spacing correct .......................... 0.4
        • Font size 12 pt across all evaluated text ..... 0.3
    """
    max_score = 1.0
    score = 0.0

    # ------------------------------------------------------------------
    # 1) Basic safety: file must exist and be a DOCX we can open.
    # ------------------------------------------------------------------
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0  # cannot continue – zero points

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Could not load DOCX: {e}")
        return 0.0

    # ------------------------------------------------------------------
    # 2) Split the document into three logical sections using headings.
    #    We assume the author inserted the literal headings:
    #    "Introduction", "Body", "Conclusion" (case-insensitive).
    # ------------------------------------------------------------------
    current_section = None  # intro, body, concl
    intro_paras, body_paras, concl_paras = [], [], []

    for para in doc.paragraphs:
        text = para.text.strip()
        # Detect section heading switches
        if text.lower() == "introduction":
            current_section = "intro"
            continue  # heading itself is not evaluated
        if text.lower() == "body":
            current_section = "body"
            continue
        if text.lower() == "conclusion":
            current_section = "concl"
            continue

        # Skip empty paragraphs altogether – they do not affect results
        if not text:
            continue

        # Append paragraph to the relevant bucket
        if current_section == "intro":
            intro_paras.append(para)
        elif current_section == "body":
            body_paras.append(para)
        elif current_section == "concl":
            concl_paras.append(para)
        # Paragraphs before the first heading are ignored (not part of task)

    print(f"Intro paragraphs: {len(intro_paras)}, Body paragraphs: {len(body_paras)}, "
          f"Conclusion paragraphs: {len(concl_paras)}")

    # Helper to evaluate line-spacing for a paragraph -------------------
    def spacing_matches(p, expected: float, tol: float = 0.05) -> bool:
        ls = p.paragraph_format.line_spacing  # may be None | float | Length object
        if ls is None:
            # No explicit setting → Word treats as single (≈1.0). Treat accordingly.
            ls_val = 1.0
        elif isinstance(ls, float):
            ls_val = ls
        else:
            # For values like docx.shared.Length, convert to line-rule approximation
            # Those are rare for simple spacing tasks; treat as mismatch for safety.
            return False
        return abs(ls_val - expected) < tol

    # ------------------------------------------------------------------
    # 3) Verify spacing in each section
    # ------------------------------------------------------------------
    intro_ok = len(intro_paras) > 0 and all(spacing_matches(p, 1.0) for p in intro_paras)
    concl_ok = len(concl_paras) > 0 and all(spacing_matches(p, 1.0) for p in concl_paras)
    body_ok  = len(body_paras)  > 0 and all(spacing_matches(p, 1.5) for p in body_paras)

    if intro_ok and concl_ok:
        print("✓ Introduction and conclusion spacing correct (0.3 pts)")
        score += 0.3
    else:
        if not intro_ok:
            print("✗ Introduction spacing incorrect")
        if not concl_ok:
            print("✗ Conclusion spacing incorrect")

    if body_ok:
        print("✓ Body spacing correct (0.4 pts)")
        score += 0.4
    else:
        print("✗ Body spacing incorrect")

    # ------------------------------------------------------------------
    # 4) Verify 12 pt font size in every run inside evaluated paragraphs
    # ------------------------------------------------------------------
    def font_size_is_12(run) -> bool:
        if run.font.size is None:
            # Unspecified size inherits – treat as failure (could be anything).
            return False
        return abs(run.font.size.pt - 12.0) < 0.1

    font_ok = True
    for para in intro_paras + body_paras + concl_paras:
        for run in para.runs:
            if not font_size_is_12(run):
                font_ok = False
                print(f"   → Font size mismatch in paragraph: '{para.text[:40]}...'")
                break
        if not font_ok:
            break

    if font_ok:
        print("✓ Font size 12 pt across all content (0.3 pts)")
        score += 0.3
    else:
        print("✗ Not all text is 12 pt")

    # ------------------------------------------------------------------
    # 5) Finalise score (cap at 1.0) and output
    # ------------------------------------------------------------------
    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


# ----------------------------------------------------------------------
# EXECUTION ENTRY POINT – required by evaluation harness
# ----------------------------------------------------------------------
if __name__ == "__main__":
    test_file = "/home/user/please_format_the_introduction_and_conclusion_with_single_spacing_and_the_body_with_15_spacing_all_a.docx"
    verify_writer_spacing_task(test_file)
