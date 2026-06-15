"""
FINAL REWARD SCRIPT - SUCCESS
Task: Highlight all instances of 'TODO' in red and 'DONE' in green throughout 'development_notes.pdf' in /home/user/Documents/Projects.
Generated: 2025-11-29 09:58:51
Status: success
Model: o3
Total Steps: 17
"""

"""
Reward Script: Verify that every instance of the word
  •  TODO  is highlighted in RED  and
  •  DONE  is highlighted in GREEN
throughout  /home/user/Documents/Projects/development_notes.pdf
by comparing it against the instructor-supplied golden answer PDF.

Scoring Philosophy (progressive 0.0‒1.0):
  • coverage  = (# matched expected highlights) / (# expected)
  • extra_pen = (# extra highlights beyond golden) / (# expected)
  • reward    = coverage – extra_penalty   (clamped 0..1)
      → 1.0 only when every expected highlight exists and NO extras
      → partial credit when some are correct but work is incomplete

Implementation notes
--------------------
• PyPDF2 is used exclusively (pre-installed in the environment).
• Highlight annotations are detected by /Subtype == /Highlight.
• Colour is classified via a tolerant RGB heuristic:
      red   : R≥0.6 & G≤0.4 & B≤0.4
      green : G≥0.6 & R≤0.4 & B≤0.4
  (values automatically normalised whether 0-1 or 0-255 scale)
• Each highlight is represented by the page index, colour category,
  and the centre (cx, cy) of its QuadPoints/Rect to allow spatial
  matching with a small tolerance (±2 user units).
• No subprocess usage – fully file-based inspection.
• Ample print statements give an audit trail of what was verified.
"""

import os
from typing import List, Tuple
from PyPDF2 import PdfReader

# --------------------------------------------------
# Configuration – paths (from task description)
# --------------------------------------------------
CANDIDATE_PDF = "/home/user/Documents/Projects/development_notes.pdf"
GOLDEN_PDF    = (
    "/home/user/"
    "highlight_all_instances_of_todo_in_red_and_done_in_green_throughout_"
    "development_notespdf_in_homeuser_golden.pdf"
)

# --------------------------------------------------
# Helper utilities
# --------------------------------------------------

def _normalise_rgb(rgb):
    """Return (r,g,b) in 0..1 range or None if invalid."""
    if not rgb or len(rgb) != 3:
        return None
    r, g, b = rgb
    if max(r, g, b) > 1:  # convert from 0-255 if needed
        r, g, b = [v / 255 for v in (r, g, b)]
    return (r, g, b)


def _classify_colour(rgb):
    """Return 'red', 'green', or None based on simple thresholding."""
    rgb = _normalise_rgb(rgb)
    if not rgb:
        return None
    r, g, b = rgb
    if r >= 0.6 and g <= 0.4 and b <= 0.4:
        return "red"
    if g >= 0.6 and r <= 0.4 and b <= 0.4:
        return "green"
    return None


def _centre_from_coords(coords):
    """Compute an approximate centre (cx, cy) from QuadPoints or Rect list."""
    if not coords:
        return 0.0, 0.0
    if len(coords) >= 8:  # QuadPoints (x1 y1 … x4 y4)
        xs = coords[0:8:2]
        ys = coords[1:8:2]
        cx = sum(xs) / 4.0
        cy = sum(ys) / 4.0
    elif len(coords) == 4:  # Rect (llx lly urx ury)
        x1, y1, x2, y2 = coords
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0
    else:
        cx = cy = 0.0
    return round(cx, 1), round(cy, 1)


def extract_highlights(pdf_path: str) -> List[Tuple[int, str, float, float]]:
    """Return list of (page_index, category, cx, cy) for red/green highlights."""
    reader = PdfReader(pdf_path)
    results: List[Tuple[int, str, float, float]] = []
    for pg_idx, page in enumerate(reader.pages):
        for annot_ref in page.get("/Annots") or []:
            annot = annot_ref.get_object()
            if annot.get("/Subtype") != "/Highlight":
                continue
            cat = _classify_colour(annot.get("/C"))
            if not cat:
                continue  # ignore non-red/non-green highlights
            quad = annot.get("/QuadPoints")
            rect = annot.get("/Rect")
            coords = [float(v) for v in (quad or rect or [])]
            cx, cy = _centre_from_coords(coords)
            results.append((pg_idx, cat, cx, cy))
    return results


# --------------------------------------------------
# Comparison / scoring helpers
# --------------------------------------------------

def _match_lists(
    golden: List[Tuple[int, str, float, float]],
    candidate: List[Tuple[int, str, float, float]],
    tol: float = 2.0,
) -> Tuple[int, int, int]:
    """Return counts: matched, missing, extra."""
    matched = 0
    used = [False] * len(candidate)
    for g in golden:
        g_pg, g_cat, g_cx, g_cy = g
        found = False
        for idx, c in enumerate(candidate):
            if used[idx]:
                continue
            c_pg, c_cat, c_cx, c_cy = c
            if g_pg != c_pg or g_cat != c_cat:
                continue
            if abs(c_cx - g_cx) <= tol and abs(c_cy - g_cy) <= tol:
                used[idx] = True
                matched += 1
                found = True
                break
        # if not found, this golden highlight is missing → handled later
    missing = len(golden) - matched
    extra = len(candidate) - matched
    return matched, missing, extra


def _compute_score(matched: int, missing: int, extra: int) -> float:
    """Progressive score 0.0‒1.0 based on coverage and extra highlights."""
    total_expected = matched + missing
    if total_expected == 0:  # edge case: golden expects nothing
        return 1.0 if extra == 0 else 0.0

    coverage = matched / total_expected        # proportion of required highlights present
    extra_penalty = extra / total_expected     # proportion of surplus highlights

    score = coverage - extra_penalty           # net quality measure
    score = max(0.0, min(1.0, score))          # clamp
    return round(score, 4)


# --------------------------------------------------
# Main verification entry point
# --------------------------------------------------

def verify_task(candidate_pdf: str = CANDIDATE_PDF, golden_pdf: str = GOLDEN_PDF) -> float:
    print("PDF Highlight Verification – 'TODO' in RED & 'DONE' in GREEN")
    print(f"Candidate : {candidate_pdf}")
    print(f"Golden    : {golden_pdf}")

    # Existence checks (no points for merely existing!)
    if not os.path.exists(candidate_pdf):
        print("✗ Candidate PDF not found – cannot verify")
        print("REWARD: 0.0")
        return 0.0
    if not os.path.exists(golden_pdf):
        print("✗ Golden PDF not found – cannot verify")
        print("REWARD: 0.0")
        return 0.0

    # Extract highlight data from both PDFs
    try:
        golden_hls = extract_highlights(golden_pdf)
        cand_hls   = extract_highlights(candidate_pdf)
    except Exception as e:
        print(f"✗ Error reading PDFs: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Golden highlight count   : {len(golden_hls)}")
    print(f"Candidate highlight count: {len(cand_hls)}")

    # Compare highlight sets
    matched, missing, extra = _match_lists(golden_hls, cand_hls)
    print(f"Matched: {matched}, Missing: {missing}, Extra: {extra}")

    # Compute progressive score
    reward = _compute_score(matched, missing, extra)
    print(f"REWARD: {reward}")
    return reward


# When executed directly, perform the verification immediately
if __name__ == "__main__":
    verify_task()

