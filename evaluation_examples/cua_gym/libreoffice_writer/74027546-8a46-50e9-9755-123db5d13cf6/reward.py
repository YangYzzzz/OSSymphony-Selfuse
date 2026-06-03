"""
Reward Script: Add front matter pages (half-title, title, copyright) to novel manuscript
Task ID: writer_creative_053
Domain: libreoffice_writer
Scoring:
  Component 1: Half-title page (para 0 = 'Echoes of Tomorrow', 24pt, centered, page break after) — 0.30 pts
  Component 2: Title page content (para 1 = 'Echoes of Tomorrow' 28pt bold centered; para 2 = 'by Marcus Reeves' 16pt centered; para 3 = 'Publisher Placeholder' 12pt centered, page break after) — 0.30 pts
  Component 3: Copyright page (para 4-6: copyright text, all rights reserved, no-part text, all 10pt left-aligned, page break after) — 0.25 pts
  Component 4: Original novel content preserved starting at correct position — 0.15 pts
Total: 1.0
"""

import os
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_creative_053'
FILE_PATH = f'{WORKDIR}/Desktop/novel_manuscript.docx'

# Namespace for XML lookups
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def has_page_break_in_para(para):
    """Check if a paragraph contains a manual page break."""
    for run in para.runs:
        for br in run.element.findall('.//w:br', NS):
            br_type = br.attrib.get(
                '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type', ''
            )
            if br_type == 'page':
                return True
    return False


def get_para_font_size(para):
    """Return the font size (pt) of the first non-None run in a paragraph, or None."""
    for run in para.runs:
        if run.font.size is not None:
            return run.font.size.pt
    return None


def get_para_bold(para):
    """Return True if any run in the paragraph is explicitly bold."""
    for run in para.runs:
        if run.font.bold is True:
            return True
    return False


def is_centered(para):
    """Return True if paragraph alignment is CENTER."""
    return para.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER


def is_left(para):
    """Return True if paragraph alignment is LEFT (0) or None (default left)."""
    align = para.paragraph_format.alignment
    return align == WD_PARAGRAPH_ALIGNMENT.LEFT or align is None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must load
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = doc.paragraphs
    print(f"INFO: Document has {len(paras)} paragraphs")

    # Precondition: document must have at least 10 paragraphs (front matter + original content)
    if len(paras) < 10:
        print(f"FAIL: Document too short ({len(paras)} paragraphs), expected at least 10")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: Half-title page (0.30 points)
    # Para 0: 'Echoes of Tomorrow', centered, 24pt, with a page break
    # This FAILS on initial (left-aligned, 12pt, no page break) → PASSES on golden
    # -----------------------------------------------------------------------
    try:
        p0 = paras[0]
        text_ok = 'Echoes of Tomorrow' in p0.text.strip()
        size_ok = get_para_font_size(p0) == 24.0
        centered_ok = is_centered(p0)
        page_break_ok = has_page_break_in_para(p0)

        if text_ok and size_ok and centered_ok and page_break_ok:
            print(f"PASS: Component 1 — half-title page: 'Echoes of Tomorrow' 24pt, centered, with page break (0.30 pts)")
            total_score += 0.30
        else:
            reasons = []
            if not text_ok:
                reasons.append(f"text not 'Echoes of Tomorrow' (found: {repr(p0.text[:30])})")
            if not size_ok:
                reasons.append(f"font size not 24pt (found: {get_para_font_size(p0)}pt)")
            if not centered_ok:
                reasons.append(f"not centered (align={p0.paragraph_format.alignment})")
            if not page_break_ok:
                reasons.append("no page break found after half-title")
            print(f"FAIL: Component 1 — half-title page issues: {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 1 (half-title) — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Title page content (0.30 points)
    # Para 1: 'Echoes of Tomorrow', 28pt, bold=True, centered
    # Para 2: 'by Marcus Reeves', 16pt, centered
    # Para 3: 'Publisher Placeholder', 12pt, centered, with page break
    # This FAILS on initial → PASSES on golden
    # -----------------------------------------------------------------------
    try:
        p1 = paras[1]
        p2 = paras[2]
        p3 = paras[3]

        # Check para 1: title
        title_text_ok = 'Echoes of Tomorrow' in p1.text.strip()
        title_size_ok = get_para_font_size(p1) == 28.0
        title_bold_ok = get_para_bold(p1)
        title_centered_ok = is_centered(p1)

        # Check para 2: author
        author_text_ok = 'by Marcus Reeves' in p2.text.strip() or 'Marcus Reeves' in p2.text.strip()
        author_size_ok = get_para_font_size(p2) == 16.0
        author_centered_ok = is_centered(p2)

        # Check para 3: publisher placeholder with page break
        pub_text_ok = 'Publisher Placeholder' in p3.text.strip() or 'placeholder' in p3.text.lower()
        pub_centered_ok = is_centered(p3)
        pub_page_break_ok = has_page_break_in_para(p3)

        title_page_ok = (title_text_ok and title_size_ok and title_bold_ok and title_centered_ok
                         and author_text_ok and author_size_ok and author_centered_ok
                         and pub_text_ok and pub_centered_ok and pub_page_break_ok)

        if title_page_ok:
            print(f"PASS: Component 2 — title page: title 28pt bold centered, author 16pt centered, publisher placeholder 12pt centered with page break (0.30 pts)")
            total_score += 0.30
        else:
            reasons = []
            if not (title_text_ok and title_size_ok and title_bold_ok and title_centered_ok):
                reasons.append(f"para 1 title issues: text_ok={title_text_ok}, size_ok={title_size_ok} (found: {get_para_font_size(p1)}pt), bold_ok={title_bold_ok}, centered={title_centered_ok}")
            if not (author_text_ok and author_size_ok and author_centered_ok):
                reasons.append(f"para 2 author issues: text_ok={author_text_ok}, size_ok={author_size_ok} (found: {get_para_font_size(p2)}pt), centered={author_centered_ok}")
            if not (pub_text_ok and pub_centered_ok and pub_page_break_ok):
                reasons.append(f"para 3 publisher issues: text_ok={pub_text_ok} (found: {repr(p3.text[:30])}), centered={pub_centered_ok}, page_break={pub_page_break_ok}")
            print(f"FAIL: Component 2 — title page issues: {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 2 (title page) — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Copyright page (0.25 points)
    # Para 4: 'Copyright © 2026 Marcus Reeves', 10pt, left-aligned
    # Para 5: 'All rights reserved.', 10pt, left-aligned
    # Para 6: 'No part of this publication...', 10pt, left-aligned, with page break
    # This FAILS on initial → PASSES on golden
    # -----------------------------------------------------------------------
    try:
        p4 = paras[4]
        p5 = paras[5]
        p6 = paras[6]

        # Copyright line
        copyright_text_ok = 'Copyright' in p4.text and 'Marcus Reeves' in p4.text and '2026' in p4.text
        copyright_size_ok = get_para_font_size(p4) == 10.0
        copyright_left_ok = is_left(p4)

        # All rights reserved
        rights_text_ok = 'All rights reserved' in p5.text
        rights_size_ok = get_para_font_size(p5) == 10.0
        rights_left_ok = is_left(p5)

        # No-part text with page break
        nopart_text_ok = 'No part of this publication' in p6.text or 'no part' in p6.text.lower()
        nopart_size_ok = get_para_font_size(p6) == 10.0
        nopart_left_ok = is_left(p6)
        nopart_page_break_ok = has_page_break_in_para(p6)

        copyright_page_ok = (copyright_text_ok and copyright_size_ok and copyright_left_ok
                              and rights_text_ok and rights_size_ok and rights_left_ok
                              and nopart_text_ok and nopart_size_ok and nopart_left_ok
                              and nopart_page_break_ok)

        if copyright_page_ok:
            print(f"PASS: Component 3 — copyright page: all 3 lines present at 10pt left-aligned with page break (0.25 pts)")
            total_score += 0.25
        else:
            reasons = []
            if not (copyright_text_ok and copyright_size_ok and copyright_left_ok):
                reasons.append(f"para 4 copyright issues: text_ok={copyright_text_ok} (found: {repr(p4.text[:40])}), size_ok={copyright_size_ok} ({get_para_font_size(p4)}pt), left={copyright_left_ok}")
            if not (rights_text_ok and rights_size_ok and rights_left_ok):
                reasons.append(f"para 5 rights issues: text_ok={rights_text_ok} (found: {repr(p5.text[:30])}), size_ok={rights_size_ok} ({get_para_font_size(p5)}pt), left={rights_left_ok}")
            if not (nopart_text_ok and nopart_size_ok and nopart_left_ok and nopart_page_break_ok):
                reasons.append(f"para 6 no-part issues: text_ok={nopart_text_ok} (found: {repr(p6.text[:40])}), size_ok={nopart_size_ok} ({get_para_font_size(p6)}pt), left={nopart_left_ok}, page_break={nopart_page_break_ok}")
            print(f"FAIL: Component 3 — copyright page issues: {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 3 (copyright page) — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Original novel content preserved (0.15 points)
    # After front matter (para 7+), original text should start with 'Echoes of Tomorrow'
    # then 'by Marcus Reeves', then 'Chapter 1' — all at 12pt, left-aligned
    # This FAILS on initial (because para 0 is 'Echoes of Tomorrow' but at index 0, not 7+)
    # and the document structure check inherently ties to the front matter having been added
    # -----------------------------------------------------------------------
    try:
        # After the 3 front matter pages, original text begins
        # Expected: paras[7] = 'Echoes of Tomorrow' (12pt, left), paras[8] = 'by Marcus Reeves' (12pt, left), paras[9] = 'Chapter 1' (12pt, left)
        # On initial, these are at index 0, 1, 2 — not 7+, so this check fails on initial
        if len(paras) < 10:
            print("FAIL: Component 4 — not enough paragraphs for original content at expected position")
        else:
            # Find the original content starting position (after front matter)
            # We expect 'Chapter 1' to appear somewhere after index 5 (after front matter)
            chapter1_idx = None
            for i in range(5, min(15, len(paras))):
                if 'Chapter 1' in paras[i].text:
                    chapter1_idx = i
                    break

            if chapter1_idx is None:
                print(f"FAIL: Component 4 — 'Chapter 1' not found at expected position (after front matter, index 5+)")
            else:
                # Chapter 1 found at a valid post-front-matter position
                # Check it's at 12pt left-aligned
                p_ch1 = paras[chapter1_idx]
                ch1_size_ok = get_para_font_size(p_ch1) == 12.0
                ch1_left_ok = is_left(p_ch1)

                # Also verify the paragraph before Chapter 1 contains 'by Marcus Reeves' (original title block)
                # and 2 paragraphs before is 'Echoes of Tomorrow'
                if chapter1_idx >= 2:
                    prev1 = paras[chapter1_idx - 1]
                    prev2 = paras[chapter1_idx - 2]
                    content_intact = ('by Marcus Reeves' in prev1.text and 'Echoes of Tomorrow' in prev2.text)
                else:
                    content_intact = False

                if ch1_size_ok and ch1_left_ok and content_intact:
                    print(f"PASS: Component 4 — original novel content preserved: 'Chapter 1' at para {chapter1_idx}, 12pt left-aligned, preceded by original title block (0.15 pts)")
                    total_score += 0.15
                else:
                    reasons = []
                    if not ch1_size_ok:
                        reasons.append(f"'Chapter 1' font size not 12pt (found: {get_para_font_size(p_ch1)}pt)")
                    if not ch1_left_ok:
                        reasons.append(f"'Chapter 1' not left-aligned (align={p_ch1.paragraph_format.alignment})")
                    if not content_intact:
                        reasons.append("original title block not found before Chapter 1")
                    print(f"FAIL: Component 4 — original content issues: {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 4 (original content) — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
