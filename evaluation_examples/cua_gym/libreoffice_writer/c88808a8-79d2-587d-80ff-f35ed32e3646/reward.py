"""
Reward Script: Poetry Chapbook Table of Contents
Task ID: writer_creative_038
Domain: libreoffice_writer
Scoring:
  Component 1: 'Contents' heading at start — centered, 18pt, bold, space_after~24pt (0.30 pts)
  Component 2: All 8 TOC entries with correct poem titles and page numbers 1-8 (0.40 pts)
  Component 3: TOC entries have RIGHT-aligned tab stop with dot leader (0.20 pts)
  Component 4: Page break after TOC separating it from poem content (0.10 pts)
  Total: 1.00
"""

import os
from docx import Document
from docx.shared import Pt, Emu
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_TAB_ALIGNMENT, WD_TAB_LEADER

WORKDIR = '/home/user/Desktop'
TASK_ID = 'chapbook'

# Expected TOC entries: (poem_title, page_number)
EXPECTED_TOC = [
    ('First Snow', '2'),
    ('Harbor Lights', '3'),
    ("Grandmother's Garden", '4'),
    ('The Last Train', '5'),
    ('Wildflowers', '6'),
    ('Sunday Morning', '7'),
    ('Letters from Abroad', '8'),
    ('Coming Home', '9'),
]


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

    # ----------------------------------------------------------------
    # Component 1: 'Contents' heading at document start (0.30 points)
    # Must be: first paragraph, text='Contents', centered, 18pt bold, space_after~24pt
    # ----------------------------------------------------------------
    try:
        if len(paragraphs) == 0:
            print("FAIL: Component 1 — document has no paragraphs")
        else:
            p0 = paragraphs[0]
            # Check text
            text_ok = p0.text.strip().lower() == 'contents'
            # Check alignment (CENTER = 1)
            align_ok = p0.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER
            # Check bold and font size from runs
            bold_ok = False
            size_ok = False
            for run in p0.runs:
                if run.text.strip():
                    if run.bold is True or run.font.bold is True:
                        bold_ok = True
                    if run.font.size is not None:
                        # 18pt in EMU = 18 * 12700 = 228600
                        if abs(run.font.size - Pt(18)) < 6350:  # within 0.5pt tolerance
                            size_ok = True
            # Check space_after (~24pt = 304800 EMU)
            space_after = p0.paragraph_format.space_after
            space_ok = space_after is not None and abs(space_after - Pt(24)) < 12700  # within 1pt

            if text_ok and align_ok and bold_ok and size_ok and space_ok:
                print(f"PASS: Component 1 — 'Contents' heading: centered, bold, 18pt, space_after~24pt (0.30 pts)")
                total_score += 0.30
            elif text_ok and align_ok:
                # Partial: heading exists and is centered but formatting incomplete
                print(f"FAIL: Component 1 — 'Contents' at para[0], centered={align_ok}, bold={bold_ok}, size_ok={size_ok}, space_ok={space_ok}")
            else:
                # Check if 'Contents' appears anywhere in first few paragraphs
                found_contents = any(
                    p.text.strip().lower() == 'contents'
                    for p in paragraphs[:5]
                )
                print(f"FAIL: Component 1 — First paragraph is not 'Contents' heading. text={p0.text!r}, align={p0.paragraph_format.alignment}, found_in_first5={found_contents}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: All 8 TOC entries with correct titles and page numbers (0.40 points)
    # Each entry should contain the poem title and page number separated by a tab
    # ----------------------------------------------------------------
    try:
        # Collect all paragraphs that look like TOC entries
        # TOC entries contain a tab and a page number
        toc_entries_found = []
        for p in paragraphs[:20]:  # TOC should be in first ~20 paragraphs
            text = p.text.strip()
            if '\t' in text:
                parts = text.split('\t')
                if len(parts) >= 2:
                    title_part = parts[0].strip()
                    page_part = parts[-1].strip()
                    toc_entries_found.append((title_part, page_part))

        # Match against expected TOC
        matched = 0
        for expected_title, expected_page in EXPECTED_TOC:
            found = False
            for found_title, found_page in toc_entries_found:
                # Case-insensitive title match, exact page match
                if found_title.lower() == expected_title.lower() and found_page == expected_page:
                    found = True
                    break
            if found:
                matched += 1
            else:
                print(f"  MISSING: '{expected_title}' -> p{expected_page}")

        if matched == 8:
            print(f"PASS: Component 2 — All 8 TOC entries found with correct titles and page numbers (0.40 pts)")
            total_score += 0.40
        elif matched >= 4:
            partial = round(0.40 * (matched / 8), 2)
            print(f"PARTIAL: Component 2 — {matched}/8 TOC entries correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {matched}/8 TOC entries found. entries_found={toc_entries_found}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: TOC entries have RIGHT-aligned tab stop with dot leader (0.20 points)
    # At least 6 of 8 entries must have a RIGHT tab stop with DOTS leader
    # ----------------------------------------------------------------
    try:
        toc_with_dot_leader = 0
        toc_para_count = 0

        for p in paragraphs[:20]:
            text = p.text.strip()
            if '\t' in text and any(title.lower() in text.lower() for title, _ in EXPECTED_TOC):
                toc_para_count += 1
                tab_stops = list(p.paragraph_format.tab_stops)
                # Filter out default/clear stops
                real_stops = [
                    ts for ts in tab_stops
                    if ts.alignment != WD_TAB_ALIGNMENT.CLEAR
                    and not (ts.alignment == WD_TAB_ALIGNMENT.LEFT and ts.position == 0)
                ]
                has_right_dot = any(
                    ts.alignment == WD_TAB_ALIGNMENT.RIGHT
                    and ts.leader == WD_TAB_LEADER.DOTS
                    for ts in real_stops
                )
                if has_right_dot:
                    toc_with_dot_leader += 1

        if toc_para_count > 0 and toc_with_dot_leader >= 6:
            print(f"PASS: Component 3 — {toc_with_dot_leader}/{toc_para_count} TOC entries have RIGHT tab stop with dot leader (0.20 pts)")
            total_score += 0.20
        elif toc_para_count > 0 and toc_with_dot_leader >= 3:
            partial = round(0.20 * (toc_with_dot_leader / 8), 2)
            print(f"PARTIAL: Component 3 — {toc_with_dot_leader}/{toc_para_count} TOC entries have dot leader ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — {toc_with_dot_leader}/{toc_para_count} TOC entries have RIGHT tab stop with dot leader. Need >=6")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ----------------------------------------------------------------
    # Component 4: Page break after TOC (0.10 points)
    # The golden document has 8 page breaks (initial has 7).
    # The first page break should appear near the end of the TOC section (within first 15 paragraphs).
    # ----------------------------------------------------------------
    try:
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        toc_page_break_found = False
        for i, para in enumerate(paragraphs[:15]):
            for run in para.runs:
                brs = run.element.findall('.//w:br', ns)
                for br in brs:
                    br_type = br.attrib.get(
                        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type'
                    )
                    if br_type == 'page':
                        toc_page_break_found = True
                        break
                if toc_page_break_found:
                    break
            if toc_page_break_found:
                break

        if toc_page_break_found:
            print(f"PASS: Component 4 — Page break found after TOC section (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — No page break found in first 15 paragraphs after TOC")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in given env
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
