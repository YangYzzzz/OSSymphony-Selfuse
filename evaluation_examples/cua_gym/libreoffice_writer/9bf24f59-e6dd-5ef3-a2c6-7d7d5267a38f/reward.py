"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve got a 30-page report where every aside is in italics, but at 12 pt they’re getting lost. In LibreOffice Writer, can I automatically push every single italic word up to 14 pt while keeping everything else exactly at 12 pt? I really don’t want to hunt them down one by one.
Generated: 2025-09-10 15:10:49
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
from docx import Document


def verify_italic_font_sizes(file_path: str) -> float:
    """Verify that all italic text is 14 pt and all non-italic text is 12 pt.

    Returns a progressive score up to 1.0:
      • 0.5 points based on the proportion of italic runs that are exactly 14 pt
      • 0.5 points based on the proportion of non-italic runs that are exactly 12 pt
    """
    print(f"Verifying document: {file_path}")

    # ---------- prerequisite: file must exist & load ----------
    if not os.path.exists(file_path):
        print("✗ File not found → 0.0 points")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Could not load DOCX ({e}) → 0.0 points")
        return 0.0

    # ---------- gather run statistics ----------
    total_italic_runs = 0
    correct_italic_runs = 0  # italic & 14 pt
    total_nonitalic_runs = 0
    correct_nonitalic_runs = 0  # non-italic & 12 pt

    for para in doc.paragraphs:
        for run in para.runs:
            is_italic = bool(run.italic)
            size = run.font.size
            pt = size.pt if size is not None else None  # size may be None (inherits style)

            if is_italic:
                total_italic_runs += 1
                if pt is not None and abs(pt - 14) < 0.1:
                    correct_italic_runs += 1
            else:
                total_nonitalic_runs += 1
                if pt is not None and abs(pt - 12) < 0.1:
                    correct_nonitalic_runs += 1

    print(f"Total italic runs:       {total_italic_runs}")
    print(f"Italic runs @ 14 pt:     {correct_italic_runs}")
    print(f"Total non-italic runs:   {total_nonitalic_runs}")
    print(f"Non-italic runs @ 12 pt: {correct_nonitalic_runs}")

    # ---------- progressive scoring ----------
    score = 0.0

    if total_italic_runs:
        italic_fraction = correct_italic_runs / total_italic_runs
        italic_score = italic_fraction * 0.5  # up to 0.5 points
        score += italic_score
        print(f"Italic correctness:  {italic_fraction:.1%} → {italic_score:.3f} points")
    else:
        print("No italic runs found → 0 points for italic part")

    if total_nonitalic_runs:
        nonitalic_fraction = correct_nonitalic_runs / total_nonitalic_runs
        nonitalic_score = nonitalic_fraction * 0.5  # up to 0.5 points
        score += nonitalic_score
        print(f"Non-italic correctness: {nonitalic_fraction:.1%} → {nonitalic_score:.3f} points")
    else:
        print("No non-italic runs found → 0 points for non-italic part")

    final_score = round(min(score, 1.0), 3)
    print(f"FINAL SCORE: {final_score}")
    return final_score


# -------------------- run verification & print reward --------------------
if __name__ == "__main__":
    DOC_PATH = "/home/user/ive_got_a_30_page_report_where_every_aside_is_in_italics_but_at_12_pt_theyre_getting_lost_in_libreof.docx"
    reward = verify_italic_font_sizes(DOC_PATH)
    print(f"REWARD: {reward}")
