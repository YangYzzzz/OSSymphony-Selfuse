"""
Reward Script: Tri-fold brochure layout for tradeshow handout
Task ID: writer_mktg_035
Domain: libreoffice_writer
Scoring:
  Component 1: Page setup (landscape, letter size, 0.5-inch margins)  — 0.30 pts
  Component 2: Three equal columns with 0.2-inch gutter               — 0.20 pts
  Component 3: Column 1 content (company name 18pt bold, tagline 12pt italic) — 0.20 pts
  Component 4: Column 2 content (Product Highlights 14pt bold + 4 bullet items) — 0.15 pts
  Component 5: Column 3 content (Contact Us 14pt bold + contact lines) — 0.15 pts
  Total: 1.0
"""

import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.section import WD_ORIENT

WORKDIR = '/home/user'
TASK_ID = 'writer_mktg_035'
FILE_PATH = f'{WORKDIR}/Desktop/tradeshow_handout.docx'

WNS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

# Tolerance for floating-point comparisons (inches)
TOLERANCE_IN = 0.1


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

    if not doc.sections:
        print("CRITICAL: Document has no sections")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]

    # ------------------------------------------------------------------
    # Component 1: Page setup — landscape orientation, letter size (11x8.5"),
    #              0.5-inch margins on all sides  (0.30 points)
    # ------------------------------------------------------------------
    try:
        is_landscape = (section.orientation == WD_ORIENT.LANDSCAPE)
        page_w_ok = abs(section.page_width.inches - 11.0) < TOLERANCE_IN
        page_h_ok = abs(section.page_height.inches - 8.5) < TOLERANCE_IN
        margin_left_ok   = abs(section.left_margin.inches   - 0.5) < TOLERANCE_IN
        margin_right_ok  = abs(section.right_margin.inches  - 0.5) < TOLERANCE_IN
        margin_top_ok    = abs(section.top_margin.inches    - 0.5) < TOLERANCE_IN
        margin_bottom_ok = abs(section.bottom_margin.inches - 0.5) < TOLERANCE_IN
        margins_ok = margin_left_ok and margin_right_ok and margin_top_ok and margin_bottom_ok

        sub_score = 0.0
        if is_landscape:
            sub_score += 0.10
            print(f"PASS: Component 1a — Landscape orientation confirmed")
        else:
            print(f"FAIL: Component 1a — Expected LANDSCAPE, found {section.orientation}")

        if page_w_ok and page_h_ok:
            sub_score += 0.10
            print(f"PASS: Component 1b — Letter size confirmed ({section.page_width.inches:.2f}\" x {section.page_height.inches:.2f}\")")
        else:
            print(f"FAIL: Component 1b — Expected 11x8.5\", found {section.page_width.inches:.2f}x{section.page_height.inches:.2f}")

        if margins_ok:
            sub_score += 0.10
            print(f"PASS: Component 1c — 0.5\" margins confirmed (L={section.left_margin.inches:.2f}, R={section.right_margin.inches:.2f}, T={section.top_margin.inches:.2f}, B={section.bottom_margin.inches:.2f})")
        else:
            print(f"FAIL: Component 1c — Expected 0.5\" margins, found L={section.left_margin.inches:.2f} R={section.right_margin.inches:.2f} T={section.top_margin.inches:.2f} B={section.bottom_margin.inches:.2f}")

        total_score += sub_score
        print(f"Component 1 subtotal: {sub_score}/0.30")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: Three equal columns with ~0.2-inch gutter  (0.20 points)
    # Gutter stored as EMU in w:cols @w:space; 1 inch = 914400 EMU
    # ------------------------------------------------------------------
    try:
        sectPr = section._sectPr
        cols_elem = sectPr.find(WNS + 'cols')
        num_cols = 1  # default when no cols element
        equal_width = True
        gutter_emu = 0

        if cols_elem is not None:
            num_str = cols_elem.attrib.get(WNS + 'num')
            num_cols = int(num_str) if num_str else 1
            equal_raw = cols_elem.attrib.get(WNS + 'equalWidth')
            # equalWidth='1' or absence means equal; '0' means unequal
            equal_width = (equal_raw != '0')
            space_str = cols_elem.attrib.get(WNS + 'space')
            gutter_emu = int(space_str) if space_str else 0

        gutter_inches = gutter_emu / 914400.0
        num_cols_ok = (num_cols == 3)
        equal_ok = equal_width
        # Allow gutter within 0.05" of 0.2"
        gutter_ok = abs(gutter_inches - 0.2) < 0.05

        sub_score = 0.0
        if num_cols_ok:
            sub_score += 0.10
            print(f"PASS: Component 2a — 3 columns confirmed")
        else:
            print(f"FAIL: Component 2a — Expected 3 columns, found {num_cols}")

        if equal_ok and gutter_ok:
            sub_score += 0.10
            print(f"PASS: Component 2b — Equal-width columns with ~0.2\" gutter ({gutter_inches:.3f}\")")
        else:
            if not equal_ok:
                print(f"FAIL: Component 2b — Columns are not equal width")
            if not gutter_ok:
                print(f"FAIL: Component 2b — Gutter is {gutter_inches:.3f}\" (expected ~0.2\")")

        total_score += sub_score
        print(f"Component 2 subtotal: {sub_score}/0.20")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: Column 1 content — "Apex Dynamics" in 18pt bold,
    #              tagline in 12pt italic  (0.20 points)
    # Column 1 ends at a column-break paragraph; paragraphs before it.
    # ------------------------------------------------------------------
    try:
        # Find column-break positions in paragraphs
        def has_col_break(para):
            for run in para.runs:
                for br in run.element.findall('.//' + WNS + 'br'):
                    br_type = br.attrib.get(WNS + 'type')
                    if br_type == 'column':
                        return True
            return False

        paragraphs = doc.paragraphs
        col_break_indices = [i for i, p in enumerate(paragraphs) if has_col_break(p)]

        # Column 1: paragraphs before first column break (exclusive)
        col1_end = col_break_indices[0] if col_break_indices else len(paragraphs)
        col1_paras = [p for p in paragraphs[:col1_end] if p.text.strip()]

        # Look for company name (Apex Dynamics) in 18pt bold
        company_found = False
        tagline_found = False

        for p in col1_paras:
            text_lower = p.text.lower()
            # Company name
            if 'apex dynamics' in text_lower:
                for run in p.runs:
                    if 'apex dynamics' in run.text.lower():
                        is_bold = run.bold or (run.font.bold is not None and run.font.bold)
                        size_ok = run.font.size and abs(run.font.size.pt - 18.0) < 1.0
                        if is_bold and size_ok:
                            company_found = True
                            print(f"PASS: Component 3a — 'Apex Dynamics' found with 18pt bold (size={run.font.size.pt}pt)")
                        elif not is_bold:
                            print(f"FAIL: Component 3a — 'Apex Dynamics' found but not bold")
                        elif not size_ok:
                            sz = run.font.size.pt if run.font.size else None
                            print(f"FAIL: Component 3a — 'Apex Dynamics' found but size={sz}pt (expected 18pt)")
            # Tagline
            if 'intelligent automation' in text_lower:
                for run in p.runs:
                    if 'intelligent automation' in run.text.lower():
                        is_italic = run.italic or (run.font.italic is not None and run.font.italic)
                        size_ok = run.font.size and abs(run.font.size.pt - 12.0) < 1.0
                        if is_italic and size_ok:
                            tagline_found = True
                            print(f"PASS: Component 3b — Tagline found with 12pt italic (size={run.font.size.pt}pt)")
                        elif not is_italic:
                            print(f"FAIL: Component 3b — Tagline found but not italic")
                        elif not size_ok:
                            sz = run.font.size.pt if run.font.size else None
                            print(f"FAIL: Component 3b — Tagline found but size={sz}pt (expected 12pt)")

        if not company_found and not any('apex dynamics' in p.text.lower() for p in col1_paras):
            print(f"FAIL: Component 3a — 'Apex Dynamics' not found in column 1")
        if not tagline_found and not any('intelligent automation' in p.text.lower() for p in col1_paras):
            print(f"FAIL: Component 3b — Tagline not found in column 1")

        sub_score = 0.0
        if company_found:
            sub_score += 0.10
        if tagline_found:
            sub_score += 0.10

        total_score += sub_score
        print(f"Component 3 subtotal: {sub_score}/0.20")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------
    # Component 4: Column 2 content — "Product Highlights" heading in 14pt bold,
    #              plus 4 bullet-point items  (0.15 points)
    # ------------------------------------------------------------------
    try:
        # Column 2: between first and second column break
        if len(col_break_indices) >= 2:
            col2_start = col_break_indices[0] + 1
            col2_end = col_break_indices[1]
        elif len(col_break_indices) == 1:
            col2_start = col_break_indices[0] + 1
            col2_end = len(paragraphs)
        else:
            col2_start = 0
            col2_end = len(paragraphs)

        col2_paras = paragraphs[col2_start:col2_end]

        heading_found = False
        bullet_count = 0

        for p in col2_paras:
            text_lower = p.text.lower()
            # Heading check
            if 'product highlights' in text_lower:
                for run in p.runs:
                    if 'product highlights' in run.text.lower():
                        is_bold = run.bold or (run.font.bold is not None and run.font.bold)
                        size_ok = run.font.size and abs(run.font.size.pt - 14.0) < 1.0
                        if is_bold and size_ok:
                            heading_found = True
                            print(f"PASS: Component 4a — 'Product Highlights' heading found 14pt bold")
                        else:
                            sz = run.font.size.pt if run.font.size else None
                            print(f"FAIL: Component 4a — 'Product Highlights' found but bold={is_bold}, size={sz}pt")
            # Bullet points — style name contains 'List' or 'Bullet'
            style_name = p.style.name.lower() if p.style else ''
            if ('list' in style_name or 'bullet' in style_name) and p.text.strip():
                bullet_count += 1

        sub_score = 0.0
        if heading_found:
            sub_score += 0.07
        else:
            if not any('product highlights' in p.text.lower() for p in col2_paras):
                print(f"FAIL: Component 4a — 'Product Highlights' heading not found in column 2")

        if bullet_count >= 4:
            sub_score += 0.08
            print(f"PASS: Component 4b — {bullet_count} bullet items found in column 2 (expected 4)")
        elif bullet_count > 0:
            sub_score += 0.04
            print(f"PARTIAL: Component 4b — Only {bullet_count} bullet items found (expected 4)")
        else:
            print(f"FAIL: Component 4b — No bullet items found in column 2")

        total_score += sub_score
        print(f"Component 4 subtotal: {sub_score}/0.15")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ------------------------------------------------------------------
    # Component 5: Column 3 content — "Contact Us" heading in 14pt bold,
    #              plus contact lines (address, phone, email, website)  (0.15 points)
    # ------------------------------------------------------------------
    try:
        # Column 3: after second column break
        if len(col_break_indices) >= 2:
            col3_start = col_break_indices[1] + 1
        elif len(col_break_indices) == 1:
            # Fallback: everything after single break
            col3_start = col_break_indices[0] + 1
            col2_end_idx = col3_start
        else:
            col3_start = len(paragraphs)

        col3_paras = paragraphs[col3_start:]

        contact_heading_found = False
        contact_items = 0

        for p in col3_paras:
            text_lower = p.text.lower()
            if 'contact us' in text_lower or 'contact' in text_lower:
                for run in p.runs:
                    if 'contact' in run.text.lower():
                        is_bold = run.bold or (run.font.bold is not None and run.font.bold)
                        size_ok = run.font.size and abs(run.font.size.pt - 14.0) < 1.0
                        if is_bold and size_ok:
                            contact_heading_found = True
                            print(f"PASS: Component 5a — 'Contact Us' heading found 14pt bold")
                        elif p.text.strip() and not (is_bold and size_ok):
                            sz = run.font.size.pt if run.font.size else None
                            print(f"INFO: Component 5a — Contact text found: '{p.text[:40]}' bold={is_bold} size={sz}pt")
            # Contact lines: phone, email, website, address
            if any(kw in text_lower for kw in ['phone', 'email', 'website', 'innovation drive', 'austin', '@', 'www.']):
                if p.text.strip():
                    contact_items += 1

        sub_score = 0.0
        if contact_heading_found:
            sub_score += 0.07
        else:
            if not any('contact' in p.text.lower() for p in col3_paras):
                print(f"FAIL: Component 5a — 'Contact Us' heading not found in column 3")
            else:
                print(f"FAIL: Component 5a — Contact heading found but missing 14pt bold formatting")

        if contact_items >= 4:
            sub_score += 0.08
            print(f"PASS: Component 5b — {contact_items} contact info lines found in column 3")
        elif contact_items > 0:
            sub_score += 0.04
            print(f"PARTIAL: Component 5b — Only {contact_items} contact info lines found (expected 4+)")
        else:
            print(f"FAIL: Component 5b — No contact info lines found in column 3")

        total_score += sub_score
        print(f"Component 5 subtotal: {sub_score}/0.15")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ------------------------------------------------------------------
    # Final score
    # ------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
