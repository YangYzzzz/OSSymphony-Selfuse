"""
Reward script for writer_tech_044.

Verifies that each chapter's summary paragraph (the first Normal paragraph
after each Heading 1) has:
  - A paragraph border (pBdr) on all four sides (top, bottom, left, right)
  - Border style "single", size 8 half-points (= 1pt), gray color (~808080)
  - Left/right indent ~283 EMU (5mm padding)
  - Spacing before/after ~280 twips (5mm padding)

Scoring rubric (per chapter, 4 chapters total, 0.25 each):
  - Has pBdr element with all 4 sides present:     0.05
  - Border style is "single" on all sides:          0.05
  - Border size is 8 (1pt) on all sides:            0.05
  - Border color is gray on all sides:              0.05
  - Left indent >= 200 EMU (~4mm tolerance):        0.025
  - Right indent >= 200 EMU:                        0.025
  - Spacing before >= 200 twips:                    0.025
  - Spacing after >= 200 twips:                     0.025
  Total per chapter: 0.25
"""

from docx import Document
from docx.oxml.ns import qn

DOC_PATH = "/home/user/writer_tech_044.docx"
NUM_CHAPTERS = 4
GRAY_COLORS = {"808080", "7f7f7f", "808080ff", "gray", "c0c0c0", "a9a9a9", "999999", "666666", "777777", "888888"}


def is_gray_color(color_str):
    """Check if a color string represents a gray tone."""
    if color_str is None:
        return False
    c = color_str.lower().strip()
    if c in GRAY_COLORS:
        return True
    # Check if it's a hex color where R=G=B (pure gray)
    if len(c) == 6:
        try:
            r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
            # Gray means R, G, B are close to each other and in a gray range
            if max(r, g, b) - min(r, g, b) <= 30 and 40 <= r <= 200:
                return True
        except ValueError:
            pass
    return False


def find_summary_paragraphs(doc):
    """Find the first Normal paragraph after each Heading 1."""
    summaries = []
    paras = doc.paragraphs
    for i, p in enumerate(paras):
        if p.style and p.style.name == "Heading 1":
            # Next paragraph is the summary
            if i + 1 < len(paras):
                summaries.append(paras[i + 1])
    return summaries


def check_paragraph_borders(para):
    """
    Check border properties on a paragraph. Returns a dict of sub-scores.
    """
    scores = {
        "has_all_borders": 0.0,
        "style_single": 0.0,
        "size_8": 0.0,
        "color_gray": 0.0,
        "left_indent": 0.0,
        "right_indent": 0.0,
        "spacing_before": 0.0,
        "spacing_after": 0.0,
    }

    pPr = para._element.find(qn("w:pPr"))
    if pPr is None:
        return scores

    # Check borders
    pBdr = pPr.find(qn("w:pBdr"))
    sides = ["top", "bottom", "left", "right"]

    if pBdr is not None:
        found_sides = {}
        for side in sides:
            elem = pBdr.find(qn(f"w:{side}"))
            if elem is not None:
                found_sides[side] = elem

        if len(found_sides) == 4:
            scores["has_all_borders"] = 1.0

            # Check style
            all_single = all(
                found_sides[s].get(qn("w:val")) == "single" for s in sides
            )
            if all_single:
                scores["style_single"] = 1.0

            # Check size (8 half-points = 1pt)
            all_size_ok = True
            for s in sides:
                sz = found_sides[s].get(qn("w:sz"))
                if sz is None:
                    all_size_ok = False
                    break
                try:
                    sz_val = int(sz)
                    if sz_val < 4 or sz_val > 12:  # Allow 0.5pt to 1.5pt
                        all_size_ok = False
                except ValueError:
                    all_size_ok = False
            if all_size_ok:
                scores["size_8"] = 1.0

            # Check color (gray)
            all_gray = all(
                is_gray_color(found_sides[s].get(qn("w:color"))) for s in sides
            )
            if all_gray:
                scores["color_gray"] = 1.0

    # Check indentation (left/right for padding)
    ind = pPr.find(qn("w:ind"))
    if ind is not None:
        left_val = ind.get(qn("w:left"))
        right_val = ind.get(qn("w:right"))
        if left_val:
            try:
                if int(left_val) >= 200:
                    scores["left_indent"] = 1.0
            except ValueError:
                pass
        if right_val:
            try:
                if int(right_val) >= 200:
                    scores["right_indent"] = 1.0
            except ValueError:
                pass

    # Check spacing before/after
    spacing = pPr.find(qn("w:spacing"))
    if spacing is not None:
        before_val = spacing.get(qn("w:before"))
        after_val = spacing.get(qn("w:after"))
        if before_val:
            try:
                if int(before_val) >= 200:
                    scores["spacing_before"] = 1.0
            except ValueError:
                pass
        if after_val:
            try:
                if int(after_val) >= 200:
                    scores["spacing_after"] = 1.0
            except ValueError:
                pass

    return scores


def reward():
    try:
        doc = Document(DOC_PATH)
    except Exception as e:
        print(f"Error opening document: {e}")
        return 0.0

    summaries = find_summary_paragraphs(doc)

    if len(summaries) == 0:
        print("No summary paragraphs found after Heading 1 paragraphs.")
        return 0.0

    # Weight per chapter
    chapter_weight = 1.0 / NUM_CHAPTERS  # 0.25

    # Sub-weights within each chapter (must sum to 1.0)
    sub_weights = {
        "has_all_borders": 0.20,
        "style_single": 0.20,
        "size_8": 0.20,
        "color_gray": 0.20,
        "left_indent": 0.05,
        "right_indent": 0.05,
        "spacing_before": 0.05,
        "spacing_after": 0.05,
    }

    total_score = 0.0

    for i, para in enumerate(summaries[:NUM_CHAPTERS]):
        sub_scores = check_paragraph_borders(para)
        chapter_score = sum(
            sub_scores[key] * sub_weights[key] for key in sub_weights
        )
        print(f"Chapter {i+1}: sub_scores={sub_scores}, chapter_score={chapter_score:.3f}")
        total_score += chapter_score * chapter_weight

    # If fewer than expected chapters found, score is proportionally lower
    print(f"Found {len(summaries)} summary paragraphs out of {NUM_CHAPTERS} expected.")
    print(f"Total score: {total_score:.4f}")

    # Round to avoid floating point issues
    return round(total_score, 4)


if __name__ == "__main__":
    score = reward()
    print(f"reward:{score}")
