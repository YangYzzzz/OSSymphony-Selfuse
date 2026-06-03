"""
Reward Script: Professional report cover page with logo, formatted title, subtitle, author, date
Task ID: writer_rd_069
Domain: libreoffice_writer
Scoring:
  Component 1: Logo image inserted (0.20)
  Component 2: Title is 28pt bold and center-aligned (0.25)
  Component 3: Subtitle is 18pt and center-aligned (0.15)
  Component 4: Author and date are 12pt and center-aligned (0.15)
  Component 5: Vertical centering via large space_before on first element (>= 4cm) (0.15)
  Component 6: Page break after cover page content (0.10)
"""

import os
from docx import Document
from docx.shared import Pt, Emu
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_069'


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

    # Gather paragraph info for analysis
    paras = doc.paragraphs

    # Helper: find paragraph containing specific text
    def find_para(text_fragment):
        for p in paras:
            if text_fragment in p.text:
                return p
        return None

    # Helper: check if a paragraph has an inline image
    def para_has_image(para):
        for run in para.runs:
            if 'graphicData' in run._element.xml:
                return True
        return False

    # Helper: count images in document relationships
    def count_doc_images():
        return sum(1 for r in doc.part.rels.values() if 'image' in r.reltype)

    # =========================================================
    # Component 1: Logo image inserted in document (0.20 points)
    # Initial has 0 images; golden has 1 image
    # =========================================================
    try:
        img_count = count_doc_images()
        if img_count >= 1:
            print(f"PASS: Component 1 — Document contains {img_count} image(s) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — No images found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================
    # Component 2: Title 'Annual Financial Report' is 28pt bold
    #              and center-aligned (0.25 points)
    # Initial: no bold, no size set, no alignment
    # =========================================================
    try:
        title_para = find_para('Annual Financial Report')
        if title_para is None:
            print("FAIL: Component 2 — 'Annual Financial Report' paragraph not found")
        else:
            checks_passed = 0
            total_checks = 3

            # Check center alignment
            if title_para.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
                checks_passed += 1

            # Check bold on at least one run containing title text
            title_runs = [r for r in title_para.runs if 'Annual Financial Report' in r.text or (r.text.strip() and r.text.strip() in 'Annual Financial Report')]
            has_bold = any(r.bold is True for r in title_para.runs if r.text.strip())
            if has_bold:
                checks_passed += 1

            # Check font size ~28pt (allow 26-30 tolerance)
            has_size_28 = False
            for r in title_para.runs:
                if r.text.strip() and r.font.size is not None:
                    sz = r.font.size.pt
                    if 26 <= sz <= 30:
                        has_size_28 = True
                        break
            if has_size_28:
                checks_passed += 1

            if checks_passed == total_checks:
                print(f"PASS: Component 2 — Title is 28pt bold centered ({checks_passed}/{total_checks}) (0.25 pts)")
                total_score += 0.25
            elif checks_passed > 0:
                partial = round(0.25 * checks_passed / total_checks, 2)
                print(f"PARTIAL: Component 2 — Title {checks_passed}/{total_checks} checks (bold/size/align) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Title has no formatting changes (bold/size/align all missing)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================
    # Component 3: Subtitle 'Fiscal Year 2024-2025' is 18pt
    #              and center-aligned (0.15 points)
    # Initial: no size, no alignment
    # =========================================================
    try:
        sub_para = find_para('Fiscal Year 2024-2025')
        if sub_para is None:
            print("FAIL: Component 3 — 'Fiscal Year 2024-2025' paragraph not found")
        else:
            checks_passed = 0
            total_checks = 2

            # Center alignment
            if sub_para.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
                checks_passed += 1

            # Font size ~18pt (allow 16-20)
            has_size_18 = False
            for r in sub_para.runs:
                if r.text.strip() and r.font.size is not None:
                    sz = r.font.size.pt
                    if 16 <= sz <= 20:
                        has_size_18 = True
                        break
            if has_size_18:
                checks_passed += 1

            if checks_passed == total_checks:
                print(f"PASS: Component 3 — Subtitle is 18pt centered (0.15 pts)")
                total_score += 0.15
            elif checks_passed > 0:
                partial = round(0.15 * checks_passed / total_checks, 2)
                print(f"PARTIAL: Component 3 — Subtitle {checks_passed}/{total_checks} checks ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Subtitle has no formatting changes")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================
    # Component 4: Author line and date are 12pt center-aligned
    #              (0.15 points)
    # Initial: no size, no alignment
    # =========================================================
    try:
        author_para = find_para('Prepared by: Finance Department')
        date_para = find_para('January 2025')
        checks_passed = 0
        total_checks = 4

        for label, para in [('Author', author_para), ('Date', date_para)]:
            if para is None:
                print(f"  FAIL: {label} paragraph not found")
                continue
            # Center alignment
            if para.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
                checks_passed += 1
            # Font size ~12pt (allow 10-14)
            for r in para.runs:
                if r.text.strip() and r.font.size is not None:
                    sz = r.font.size.pt
                    if 10 <= sz <= 14:
                        checks_passed += 1
                        break

        if checks_passed == total_checks:
            print(f"PASS: Component 4 — Author and date are 12pt centered (0.15 pts)")
            total_score += 0.15
        elif checks_passed > 0:
            partial = round(0.15 * checks_passed / total_checks, 2)
            print(f"PARTIAL: Component 4 — Author/date {checks_passed}/{total_checks} checks ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Author/date have no formatting changes")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================
    # Component 5: Vertical centering via large space_before
    #              (>= 4cm / ~1440000 EMU) on an early paragraph (0.15 points)
    # Initial: no space_before on any paragraph
    # =========================================================
    try:
        large_spacing_found = False
        # Check first few paragraphs for large space_before (>= 4cm = 1440000 EMU)
        threshold_emu = 1440000  # 4cm
        for i, para in enumerate(paras[:3]):
            sb = para.paragraph_format.space_before
            if sb is not None and sb >= threshold_emu:
                large_spacing_found = True
                cm_val = sb / 360000
                print(f"PASS: Component 5 — P{i} has space_before={sb} EMU ({cm_val:.1f} cm) for vertical centering (0.15 pts)")
                total_score += 0.15
                break

        if not large_spacing_found:
            # Check all paragraphs as fallback
            for i, para in enumerate(paras):
                sb = para.paragraph_format.space_before
                if sb is not None and sb >= threshold_emu:
                    large_spacing_found = True
                    cm_val = sb / 360000
                    print(f"PASS: Component 5 — P{i} has space_before={sb} EMU ({cm_val:.1f} cm) for vertical centering (0.15 pts)")
                    total_score += 0.15
                    break

        if not large_spacing_found:
            print(f"FAIL: Component 5 — No paragraph has space_before >= 4cm for vertical centering")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # =========================================================
    # Component 6: Page break after cover page content (0.10 points)
    # Initial: no page breaks
    # =========================================================
    try:
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        page_break_found = False

        for i, para in enumerate(paras):
            # Check for explicit page break in runs
            for run in para.runs:
                for br in run.element.findall('.//w:br', ns):
                    btype = br.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type')
                    if btype == 'page':
                        page_break_found = True
                        print(f"PASS: Component 6 — Page break found in P{i} (0.10 pts)")
                        break
                if page_break_found:
                    break
            # Also check page_break_before attribute
            if not page_break_found and para.paragraph_format.page_break_before:
                page_break_found = True
                print(f"PASS: Component 6 — page_break_before on P{i} (0.10 pts)")
            if page_break_found:
                break

        if page_break_found:
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — No page break found after cover page")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
