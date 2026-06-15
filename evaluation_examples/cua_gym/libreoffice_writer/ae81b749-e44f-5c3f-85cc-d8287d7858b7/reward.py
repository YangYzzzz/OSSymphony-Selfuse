"""
Reward Script: Company Timeline Visual Formatting
Task ID: writer_mktg_041
Domain: libreoffice_writer
Scoring:
  - Component 1: Title 'Company Timeline' formatted as 20pt bold centered (0.20 pts)
  - Component 2: 8 year lines each 16pt bold dark blue (#003366) (0.35 pts)
  - Component 3: 8 milestone lines each 12pt regular with 0.5 inch left indent (0.25 pts)
  - Component 4: Year line spacing — 12pt before, 4pt after (0.10 pts)
  - Component 5: Correct structure — 8 year-milestone pairs (0.10 pts)
Total: 1.0
"""

import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_mktg_041'
FILE_PATH = f'{WORKDIR}/Desktop/media_kit_timeline.docx'

YEARS = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']

# Expected EMU values (precomputed for clarity)
TITLE_SIZE_EMU = Pt(20)   # 254000
YEAR_SIZE_EMU  = Pt(16)   # 203200
MILE_SIZE_EMU  = Pt(12)   # 152400
INDENT_EMU     = Inches(0.5)  # 457200
SPACE_BEFORE_EMU = Pt(12) # 152400
SPACE_AFTER_EMU  = Pt(4)  # 50800

# Dark blue color: #003366
DARK_BLUE = RGBColor(0x00, 0x33, 0x66)

# Milestone identifiers
MILESTONE_KEYWORDS = [
    'Founded in San Francisco',
    'Launched first product',
    'Reached 100 customers',
    'International expansion',
    'Product awarded',
    '$45M Series B',
    'Launched AI-powered',
    'Surpassed 2,000 customers',
]


def color_close(c1, c2, threshold=15):
    """Check if two RGBColor values are close enough (Manhattan distance)."""
    if c1 is None or c2 is None:
        return False
    return (abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])) <= threshold


def get_rgb(run):
    """Safely extract RGB color from a run."""
    try:
        if run.font.color and run.font.color.type is not None:
            return run.font.color.rgb
    except Exception:
        pass
    return None


def runs_are_bold(runs):
    """Return True if any run is explicitly bold."""
    return any(r.bold is True for r in runs)


def runs_have_size(runs, size_emu):
    """Return True if any run matches the given EMU size."""
    return any(r.font.size == size_emu for r in runs)


def runs_are_not_bold(runs):
    """Return True if no run is explicitly bold (None or False)."""
    return all(r.bold is not True for r in runs)


def runs_have_dark_blue(runs):
    """Return True if all runs with text have dark blue color."""
    text_runs = [r for r in runs if r.text.strip()]
    if not text_runs:
        return False
    return all(color_close(get_rgb(r), DARK_BLUE) for r in text_runs)


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
    print(f"INFO: Document has {len(paragraphs)} paragraphs")

    # -----------------------------------------------------------------------
    # Component 1: Title 'Company Timeline' formatted 20pt bold centered (0.20 pts)
    # In initial: plain paragraph, no size/bold/alignment set
    # In golden: 20pt bold, centered
    # -----------------------------------------------------------------------
    try:
        title_para = next(
            (p for p in paragraphs if 'Company Timeline' in p.text),
            None
        )

        if title_para is None:
            print("FAIL: Component 1 — 'Company Timeline' title paragraph not found")
        else:
            pf = title_para.paragraph_format
            is_centered = (pf.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER)
            is_bold = runs_are_bold(title_para.runs)
            is_20pt = runs_have_size(title_para.runs, TITLE_SIZE_EMU)

            if is_centered and is_bold and is_20pt:
                print("PASS: Component 1 — Title is 20pt bold centered (0.20 pts)")
                total_score += 0.20
            else:
                print(
                    f"FAIL: Component 1 — Title centered={is_centered}, bold={is_bold}, 20pt={is_20pt}"
                )
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: 8 year lines each 16pt bold dark blue (#003366) (0.35 pts)
    # In initial: all content in one paragraph, no separate year lines
    # In golden: years are separate paragraphs with proper formatting
    # -----------------------------------------------------------------------
    try:
        year_paras = [p for p in paragraphs if p.text.strip() in YEARS]
        year_paras_correct = 0
        year_details = []

        for para in year_paras:
            text = para.text.strip()
            is_bold = runs_are_bold(para.runs)
            is_16pt = runs_have_size(para.runs, YEAR_SIZE_EMU)
            is_dark_blue = runs_have_dark_blue(para.runs)

            if is_bold and is_16pt and is_dark_blue:
                year_paras_correct += 1
            else:
                year_details.append(
                    f"  Year {text}: bold={is_bold}, 16pt={is_16pt}, dark_blue={is_dark_blue}"
                )

        if len(year_paras) == 8 and year_paras_correct == 8:
            print("PASS: Component 2 — All 8 year paragraphs are 16pt bold dark blue (0.35 pts)")
            total_score += 0.35
        elif year_paras_correct >= 6:
            print(f"PARTIAL: Component 2 — {year_paras_correct}/8 year paras correct (0.20 pts)")
            total_score += 0.20
        else:
            print(
                f"FAIL: Component 2 — {len(year_paras)} year paras found, "
                f"{year_paras_correct} correctly formatted"
            )
            for d in year_details:
                print(d)
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: 8 milestone lines 12pt regular + 0.5 inch left indent (0.25 pts)
    # In initial: milestone text embedded in single paragraph, not separate lines
    # In golden: each milestone is its own paragraph with 12pt, 0.5 indent
    # -----------------------------------------------------------------------
    try:
        milestone_paras = [
            p for p in paragraphs
            if any(kw in p.text for kw in MILESTONE_KEYWORDS)
        ]
        milestone_correct = 0
        mile_details = []

        for para in milestone_paras:
            pf = para.paragraph_format
            indent_ok = (pf.left_indent == INDENT_EMU)
            size_ok = runs_have_size(para.runs, MILE_SIZE_EMU)
            not_bold = runs_are_not_bold(para.runs)

            if indent_ok and size_ok and not_bold:
                milestone_correct += 1
            else:
                mile_details.append(
                    f"  '{para.text[:40]}': indent={indent_ok}({pf.left_indent}), "
                    f"12pt={size_ok}, not_bold={not_bold}"
                )

        if len(milestone_paras) == 8 and milestone_correct == 8:
            print("PASS: Component 3 — All 8 milestone paragraphs are 12pt indented (0.25 pts)")
            total_score += 0.25
        elif milestone_correct >= 6:
            print(f"PARTIAL: Component 3 — {milestone_correct}/8 milestones correct (0.15 pts)")
            total_score += 0.15
        else:
            print(
                f"FAIL: Component 3 — {len(milestone_paras)} milestone paras found, "
                f"{milestone_correct} correctly formatted"
            )
            for d in mile_details:
                print(d)
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Year line spacing — 12pt space_before, 4pt space_after (0.10 pts)
    # In initial: no year paragraphs exist, hence no spacing
    # In golden: year paragraphs have 12pt before and 4pt after
    # -----------------------------------------------------------------------
    try:
        year_spacing_paras = [p for p in paragraphs if p.text.strip() in YEARS]
        year_spacing_correct = 0
        spacing_details = []

        for para in year_spacing_paras:
            pf = para.paragraph_format
            before_ok = (pf.space_before == SPACE_BEFORE_EMU)
            after_ok = (pf.space_after == SPACE_AFTER_EMU)

            if before_ok and after_ok:
                year_spacing_correct += 1
            else:
                spacing_details.append(
                    f"  Year {para.text.strip()}: "
                    f"space_before={before_ok}({pf.space_before}), "
                    f"space_after={after_ok}({pf.space_after})"
                )

        if len(year_spacing_paras) == 8 and year_spacing_correct == 8:
            print("PASS: Component 4 — All 8 year paragraphs have 12pt before / 4pt after (0.10 pts)")
            total_score += 0.10
        elif year_spacing_correct >= 6:
            print(f"PARTIAL: Component 4 — {year_spacing_correct}/8 year spacings correct (0.05 pts)")
            total_score += 0.05
        else:
            print(
                f"FAIL: Component 4 — {len(year_spacing_paras)} year paras checked, "
                f"{year_spacing_correct} have correct spacing"
            )
            for d in spacing_details:
                print(d)
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: Correct structure — 8 year-milestone pairs present (0.10 pts)
    # In initial: all 8 years + milestones are in ONE paragraph (no separate lines)
    # In golden: 17 paragraphs total (1 title + 8 year + 8 milestone)
    # -----------------------------------------------------------------------
    try:
        year_para_count = sum(1 for p in paragraphs if p.text.strip() in YEARS)
        mile_para_count = sum(
            1 for p in paragraphs
            if any(kw in p.text for kw in MILESTONE_KEYWORDS)
        )

        structure_ok = (year_para_count == 8 and mile_para_count == 8)
        if structure_ok:
            print("PASS: Component 5 — 8 year paragraphs + 8 milestone paragraphs correctly structured (0.10 pts)")
            total_score += 0.10
        else:
            print(
                f"FAIL: Component 5 — year_paras={year_para_count}/8, "
                f"milestone_paras={mile_para_count}/8"
            )
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # -----------------------------------------------------------------------
    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
