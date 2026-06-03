"""
FINAL REWARD SCRIPT - SUCCESS
Task: Make all body text use Times New Roman, but leave the headings as they are.
Generated: 2025-10-14 10:49:51
Status: success
Model: azure-o3
Total Steps: 1
"""

from docx import Document
import os


def get_effective_font(run):
    """Determine the effective font name for a run.
    It checks, in order:
      1. Direct formatting on the run
      2. Character style applied to the run
      3. Paragraph style
    If none of these define a font, it returns None.
    """
    # 1. Direct formatting on the run
    if run.font and run.font.name:
        return run.font.name

    # 2. Character style applied to the run
    try:
        run_style = run.style  # may raise if style not accessible
    except Exception:
        run_style = None

    if run_style is not None and hasattr(run_style, "font") and run_style.font.name:
        return run_style.font.name

    # 3. Paragraph style (the parent of run is a paragraph)
    para_style = getattr(run._parent, "style", None)
    if para_style and para_style.font and para_style.font.name:
        return para_style.font.name

    return None  # Font not explicitly specified


def verify_body_text_font(file_path: str, body_font_target: str = "Times New Roman") -> float:
    """Verify that all *body text* (i.e., non-heading paragraphs) use the target font.

    Headings (styles starting with "Heading") are explicitly excluded from this check.

    Scoring:
        • 1.0  when every body paragraph that contains text is entirely formatted in the
               target font (case-insensitive match).
        • Otherwise, the score is the proportion of correctly-formatted body paragraphs.

    The function prints detailed diagnostics and always returns a float in [0, 1].
    """

    # ---------- Basic sanity checks ----------
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0

    try:
        document = Document(file_path)
    except Exception as exc:
        print(f"✗ Unable to load DOCX: {exc}")
        return 0.0

    # Retrieve the default font of the Normal style (used when no explicit font is set)
    normal_default_font = None
    try:
        normal_style = document.styles["Normal"]
        normal_default_font = normal_style.font.name
    except Exception:
        pass  # It's fine if we cannot obtain it; we'll fall back to None

    total_body_paragraphs = 0  # paragraphs that are considered "body" and contain visible text
    correct_body_paragraphs = 0  # of those, how many are fully in the target font

    # ---------- Paragraph inspection ----------
    for para in document.paragraphs:
        style_name = para.style.name if para.style else ""

        # Skip headings entirely — they are intentionally *not* checked
        if style_name.startswith("Heading"):
            continue

        # Determine if this paragraph actually has visible text (ignore empty ones)
        if not any(run.text.strip() for run in para.runs):
            continue  # Empty paragraph ⇒ not scored

        total_body_paragraphs += 1
        paragraph_ok = True  # Assume correct until proven otherwise

        for run in para.runs:
            if not run.text.strip():
                continue  # Ignore whitespace-only runs

            # Determine effective font for this run
            font_name = get_effective_font(run)
            if font_name is None:
                # If font is unspecified at run/char/para level, fall back to Normal style default
                font_name = normal_default_font

            # If still None, we cannot verify, so treat as incorrect (conservative)
            if font_name is None or font_name.lower() != body_font_target.lower():
                paragraph_ok = False
                break  # No need to check further runs in this paragraph

        if paragraph_ok:
            correct_body_paragraphs += 1

    # ---------- Scoring ----------
    if total_body_paragraphs == 0:
        print("✗ No body text paragraphs found – cannot verify task completion")
        return 0.0

    score = correct_body_paragraphs / total_body_paragraphs

    # ---------- Reporting ----------
    print(
        f"Body paragraphs correctly formatted: {correct_body_paragraphs}/{total_body_paragraphs}"
        f"  →  {score:.2%}"
    )

    return score


# ------------------ MAIN EXECUTION ------------------
if __name__ == "__main__":
    DOC_PATH = "/home/user/make_all_body_text_use_times_new_roman_but_leave_the_headings_as_they_are.docx"

    final_reward = verify_body_text_font(DOC_PATH)
    print(f"REWARD: {final_reward}")
