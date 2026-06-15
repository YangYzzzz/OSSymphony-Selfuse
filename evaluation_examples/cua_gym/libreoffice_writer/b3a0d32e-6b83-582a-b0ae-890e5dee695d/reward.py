"""
Reward Script: Add bookmarks and hyperlinks to brand guidelines document
Task ID: writer_mktg_040
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): 5 bookmarks with correct names (Logo, Colors, Typography, Voice, Imagery)
  Component 2 (0.30): 5 hyperlinks in nav list linking to correct bookmark anchors
  Component 3 (0.20): Hyperlinks have correct styling (blue #0000FF + single underline)
  Component 4 (0.10): Bookmarks placed at correct Heading 1 paragraphs
  Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_mktg_040'
FILE_PATH = f'{WORKDIR}/brand_guidelines_final.docx'

EXPECTED_BOOKMARKS = ['Logo', 'Colors', 'Typography', 'Voice', 'Imagery']
EXPECTED_HEADING_TEXTS = {
    'Logo': 'Logo Usage',
    'Colors': 'Color Palette',
    'Typography': 'Typography',
    'Voice': 'Brand Voice & Tone',
    'Imagery': 'Photography & Imagery',
}
# Nav list paragraph texts mapped to expected anchor
EXPECTED_NAV_HYPERLINKS = {
    'Logo Usage': 'Logo',
    'Color Palette': 'Colors',
    'Typography': 'Typography',
    'Brand Voice & Tone': 'Voice',
    'Photography & Imagery': 'Imagery',
}


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

    body = doc.element.body

    # -----------------------------------------------------------------------
    # Component 1: 5 bookmarks with correct names (0.40 points)
    # All 5 must be present: Logo, Colors, Typography, Voice, Imagery
    # -----------------------------------------------------------------------
    try:
        bm_starts = body.findall('.//' + qn('w:bookmarkStart'))
        found_bookmarks = set()
        for bm in bm_starts:
            name = bm.get(qn('w:name'))
            if name in EXPECTED_BOOKMARKS:
                found_bookmarks.add(name)

        if found_bookmarks == set(EXPECTED_BOOKMARKS):
            print(f"PASS: Component 1 — All 5 bookmarks present: {sorted(found_bookmarks)} (0.40 pts)")
            total_score += 0.40
        else:
            missing = set(EXPECTED_BOOKMARKS) - found_bookmarks
            extra = found_bookmarks - set(EXPECTED_BOOKMARKS)
            print(f"FAIL: Component 1 — Bookmarks incomplete. Found: {sorted(found_bookmarks)}, Missing: {sorted(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: 5 hyperlinks in the nav list with correct anchor targets (0.30 points)
    # Paragraphs 11-15 (0-indexed) should be hyperlinks pointing to the correct anchors.
    # -----------------------------------------------------------------------
    try:
        # Find all hyperlinks in the document body
        all_hyperlinks = body.findall('.//' + qn('w:hyperlink'))
        # Build map of anchor -> hyperlink text
        hl_anchor_to_text = {}
        for hl in all_hyperlinks:
            anchor = hl.get(qn('w:anchor'))
            if anchor:
                texts = hl.findall('.//' + qn('w:t'))
                text = ''.join(t.text or '' for t in texts)
                hl_anchor_to_text[anchor] = text

        correct_hl = 0
        for expected_text, expected_anchor in EXPECTED_NAV_HYPERLINKS.items():
            actual_text = hl_anchor_to_text.get(expected_anchor)
            if actual_text is not None and actual_text.strip() == expected_text:
                correct_hl += 1
            else:
                print(f"FAIL: Component 2 — Hyperlink for anchor={expected_anchor!r}: "
                      f"expected text={expected_text!r}, found={actual_text!r}")

        if correct_hl == 5:
            print(f"PASS: Component 2 — All 5 hyperlinks present with correct anchors and text (0.30 pts)")
            total_score += 0.30
        elif correct_hl > 0:
            partial = round(0.30 * correct_hl / 5, 2)
            print(f"PARTIAL: Component 2 — {correct_hl}/5 hyperlinks correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No correct hyperlinks found (0.00 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Hyperlinks have blue (#0000FF) color + single underline (0.20 points)
    # Check that the runs inside the 5 nav hyperlinks are styled correctly.
    # -----------------------------------------------------------------------
    try:
        all_hyperlinks = body.findall('.//' + qn('w:hyperlink'))
        styled_correctly = 0
        total_hl_checked = 0

        for hl in all_hyperlinks:
            anchor = hl.get(qn('w:anchor'))
            if anchor not in EXPECTED_BOOKMARKS:
                continue

            total_hl_checked += 1
            runs_in_hl = hl.findall('.//' + qn('w:r'))
            run_ok = False
            for r in runs_in_hl:
                rpr = r.find(qn('w:rPr'))
                if rpr is not None:
                    color_el = rpr.find(qn('w:color'))
                    underline_el = rpr.find(qn('w:u'))
                    color_val = color_el.get(qn('w:val')) if color_el is not None else None
                    underline_val = underline_el.get(qn('w:val')) if underline_el is not None else None

                    color_ok = color_val is not None and color_val.upper() == '0000FF'
                    underline_ok = underline_val is not None and underline_val != 'none'

                    if color_ok and underline_ok:
                        run_ok = True
                        break

            if run_ok:
                styled_correctly += 1

        if total_hl_checked == 0:
            print(f"FAIL: Component 3 — No nav hyperlinks found to check styling (0.00 pts)")
        elif styled_correctly == total_hl_checked:
            print(f"PASS: Component 3 — All {styled_correctly}/{total_hl_checked} hyperlinks styled blue+underline (0.20 pts)")
            total_score += 0.20
        else:
            partial = round(0.20 * styled_correctly / total_hl_checked, 2)
            print(f"PARTIAL: Component 3 — {styled_correctly}/{total_hl_checked} hyperlinks correctly styled ({partial} pts)")
            total_score += partial
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Bookmarks placed inside the correct Heading 1 paragraphs (0.10 points)
    # Each bookmark name must be within a paragraph whose text matches the expected heading.
    # -----------------------------------------------------------------------
    try:
        bm_starts = body.findall('.//' + qn('w:bookmarkStart'))
        bm_in_correct_heading = 0
        total_bm_checked = 0

        for bm in bm_starts:
            name = bm.get(qn('w:name'))
            if name not in EXPECTED_HEADING_TEXTS:
                continue
            total_bm_checked += 1
            expected_heading = EXPECTED_HEADING_TEXTS[name]

            # Traverse to the containing paragraph
            parent = bm.getparent()
            while parent is not None and parent.tag != qn('w:p'):
                parent = parent.getparent()

            if parent is not None:
                # Get text of parent paragraph
                texts = parent.findall('.//' + qn('w:t'))
                para_text = ''.join(t.text or '' for t in texts).strip()
                if para_text == expected_heading:
                    bm_in_correct_heading += 1
                else:
                    print(f"FAIL: Component 4 — Bookmark {name!r} is in paragraph "
                          f"{para_text!r}, expected {expected_heading!r}")
            else:
                print(f"FAIL: Component 4 — Bookmark {name!r} has no parent paragraph")

        if total_bm_checked == 0:
            print(f"FAIL: Component 4 — No recognized bookmarks found (0.00 pts)")
        elif bm_in_correct_heading == total_bm_checked:
            print(f"PASS: Component 4 — All {bm_in_correct_heading} bookmarks in correct headings (0.10 pts)")
            total_score += 0.10
        else:
            partial = round(0.10 * bm_in_correct_heading / total_bm_checked, 2)
            print(f"PARTIAL: Component 4 — {bm_in_correct_heading}/{total_bm_checked} bookmarks in correct headings ({partial} pts)")
            total_score += partial
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
