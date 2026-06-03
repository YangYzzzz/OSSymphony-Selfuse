"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please set Liberation Serif as the default font for new Writer documents.
Generated: 2025-10-14 12:29:19
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
from docx import Document


def verify_default_font_for_writer(doc_path: str, expected_font: str = "Liberation Serif") -> float:
    """Reward-function for the task:
    "Please set Liberation Serif as the default font for new Writer documents."

    Scoring (progressive – max 1.0):
      • 0.7  – The main default paragraph style ("Normal" or "Default Style") explicitly
               uses Liberation Serif.
      • 0.3  – No text runs in the sample document use an unexpected explicit font
               (every run either inherits the default -> font is None, or explicitly
               uses Liberation Serif).  If some runs use other fonts, partial credit is
               awarded proportional to the share of compliant runs.
    """

    max_score = 1.0
    total_score = 0.0

    # ────────────────── 0.  Load document (prerequisite – no points) ──────────────────
    if not os.path.exists(doc_path):
        print(f"✗ File not found: {doc_path}")
        return 0.0
    try:
        doc = Document(doc_path)
        print(f"✓ Loaded DOCX file: {doc_path}")
    except Exception as e:
        print(f"✗ Failed to open DOCX file: {e}")
        return 0.0

    # ────────────────── 1.  Default paragraph style uses Liberation Serif ─────────────
    default_style_verified = False
    default_style_checked = False

    for style_name in ("Normal", "Default Style"):
        try:
            style = doc.styles[style_name]
        except KeyError:
            continue  # Style not present in this document
        if style.type == 1:  # WD_STYLE_TYPE.PARAGRAPH (avoiding extra import)
            default_style_checked = True
            font_name = style.font.name
            if font_name and expected_font.lower() in font_name.lower():
                default_style_verified = True
                print(f"✓ Paragraph default style '{style_name}' uses font: {font_name}")
            else:
                print(f"✗ Paragraph default style '{style_name}' does NOT use expected font (found: {font_name})")
            break  # Only need to check the first recognised default style

    if not default_style_checked:
        print("✗ No recognised default paragraph style (Normal / Default Style) found")
    if default_style_verified:
        total_score += 0.7

    # ────────────────── 2.  Scan all runs for unexpected explicit fonts ───────────────
    non_compliant_fonts = {}
    total_runs = 0
    non_compliant_runs = 0

    for para in doc.paragraphs:
        for run in para.runs:
            total_runs += 1
            run_font = run.font.name
            # Compliant if font is inherited (None) or is Liberation Serif
            if run_font is None:
                continue
            if expected_font.lower() not in run_font.lower():
                non_compliant_runs += 1
                non_compliant_fonts[run_font] = non_compliant_fonts.get(run_font, 0) + 1

    if total_runs == 0:
        print("✗ Document contains no text runs to assess explicit font usage")
    else:
        compliant_runs = total_runs - non_compliant_runs
        compliance_ratio = compliant_runs / total_runs
        if non_compliant_runs == 0:
            print("✓ All text runs inherit or explicitly use the expected font")
            total_score += 0.3
        else:
            # award proportional part of 0.3
            awarded = 0.3 * compliance_ratio
            total_score += awarded
            print(f"✗ Found {non_compliant_runs} run(s) using unexpected fonts – partial credit: {awarded:.3f}")
            for font, count in non_compliant_fonts.items():
                print(f"   - Unexpected font '{font}' in {count} run(s)")

    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    return final_score


if __name__ == "__main__":
    # Path supplied by the evaluation environment
    SAMPLE_DOC = "/home/user/please_set_liberation_serif_as_the_default_font_for_new_writer_documents.docx"
    reward = verify_default_font_for_writer(SAMPLE_DOC)
    print(f"REWARD: {reward}")

