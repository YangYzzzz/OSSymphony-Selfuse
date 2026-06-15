"""
Reward Script: Corporate heading style for writer_biz_034
Task ID: writer_biz_034
Domain: libreoffice_writer
Task: Apply corporate heading style to all three section headings:
      Calibri 14pt bold, dark blue (#003366), 12pt space before, 6pt space after.

Scoring Rubric:
  Component 1: Font name is Calibri on all 3 headings        (0.25 pts)
  Component 2: Font color is #003366 on all 3 headings        (0.25 pts)
  Component 3: Space before is 12pt on all 3 headings          (0.25 pts)
  Component 4: Space after is 6pt on all 3 headings            (0.25 pts)

Note: Font size (14pt) and bold are the same in initial and golden, so they are
preconditions, not scoring components. We gate on them but don't award points.
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_034'
TARGET_HEADINGS = ['Market Analysis', 'Competitive Landscape', 'Growth Strategy']
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def get_effective_font_name(run, doc):
    """Get the effective font name for a run, checking run-level then style-level."""
    # Check direct run-level font name
    if run.font.name is not None:
        return run.font.name
    # Check run XML for explicit rFonts ascii attribute
    rpr = run._element.find('.//w:rPr', NS)
    if rpr is not None:
        rfonts = rpr.find('w:rFonts', NS)
        if rfonts is not None:
            ascii_font = rfonts.get(f'{{{NS["w"]}}}ascii')
            if ascii_font:
                return ascii_font
    # Fall back to the paragraph style's font
    para = run._element.getparent()
    ppr = para.find('w:pPr', NS)
    if ppr is not None:
        pstyle = ppr.find('w:pStyle', NS)
        if pstyle is not None:
            style_id = pstyle.get(f'{{{NS["w"]}}}val')
            try:
                style = doc.styles[style_id]
                if style.font.name is not None:
                    return style.font.name
                # Check style XML for rFonts ascii
                srpr = style.element.find('w:rPr', NS)
                if srpr is not None:
                    srfonts = srpr.find('w:rFonts', NS)
                    if srfonts is not None:
                        ascii_font = srfonts.get(f'{{{NS["w"]}}}ascii')
                        if ascii_font:
                            return ascii_font
            except KeyError:
                pass
    return None


def get_effective_color(run, doc):
    """Get effective font color RGB, checking run-level then style-level."""
    # Check direct run-level color
    if run.font.color and run.font.color.rgb is not None:
        return str(run.font.color.rgb)
    # Check run XML for direct color element
    rpr = run._element.find('.//w:rPr', NS)
    if rpr is not None:
        color_el = rpr.find('w:color', NS)
        if color_el is not None:
            val = color_el.get(f'{{{NS["w"]}}}val')
            if val:
                return val.upper()
    # Fall back to paragraph style
    para = run._element.getparent()
    ppr = para.find('w:pPr', NS)
    if ppr is not None:
        pstyle = ppr.find('w:pStyle', NS)
        if pstyle is not None:
            style_id = pstyle.get(f'{{{NS["w"]}}}val')
            try:
                style = doc.styles[style_id]
                if style.font.color and style.font.color.rgb is not None:
                    return str(style.font.color.rgb)
            except KeyError:
                pass
    return None


def get_effective_spacing(para, doc, attr):
    """Get effective space_before or space_after in pt, checking para-level then style."""
    pf = para.paragraph_format
    value = getattr(pf, attr)
    if value is not None:
        return value.pt

    # Fall back to style
    if para.style:
        style_pf = para.style.paragraph_format
        style_value = getattr(style_pf, attr)
        if style_value is not None:
            return style_value.pt
    return None


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

    # Find the three heading paragraphs
    heading_paras = []
    for para in doc.paragraphs:
        if para.text.strip() in TARGET_HEADINGS:
            heading_paras.append(para)

    if len(heading_paras) != 3:
        print(f"PRECONDITION FAIL: Expected 3 headings, found {len(heading_paras)}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(heading_paras)} heading paragraphs: {[p.text for p in heading_paras]}")

    # Component 1: Font name is Calibri on all 3 headings (0.25 pts)
    # INITIAL: font is theme-based (majorHAnsi), no explicit Calibri
    # GOLDEN: font is explicitly Calibri
    try:
        calibri_pass_count = 0
        calibri_total_count = 0
        for para in heading_paras:
            for run in para.runs:
                if run.text.strip():
                    calibri_total_count += 1
                    effective_name = get_effective_font_name(run, doc)
                    if effective_name is not None and effective_name.lower() == 'calibri':
                        print(f"  OK: '{para.text}' run font = '{effective_name}'")
                        calibri_pass_count += 1
                    else:
                        print(f"  FAIL: '{para.text}' run font = '{effective_name}', expected 'Calibri'")
        if calibri_total_count > 0 and calibri_pass_count == calibri_total_count:
            print(f"PASS: Component 1 -- All headings use Calibri font (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- {calibri_pass_count}/{calibri_total_count} heading runs use Calibri")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Font color is #003366 on all 3 headings (0.25 pts)
    # INITIAL: color is 365F91 (theme accent1 shade)
    # GOLDEN: color is 003366 (explicit)
    try:
        color_pass_count = 0
        color_total_count = 0
        for para in heading_paras:
            for run in para.runs:
                if run.text.strip():
                    color_total_count += 1
                    effective_color = get_effective_color(run, doc)
                    if effective_color is not None and effective_color.upper() == '003366':
                        print(f"  OK: '{para.text}' run color = '{effective_color}'")
                        color_pass_count += 1
                    else:
                        print(f"  FAIL: '{para.text}' run color = '{effective_color}', expected '003366'")
        if color_total_count > 0 and color_pass_count == color_total_count:
            print(f"PASS: Component 2 -- All headings have color #003366 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- {color_pass_count}/{color_total_count} heading runs have correct color")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Space before is 12pt on all 3 headings (0.25 pts)
    # INITIAL: space before is 24pt
    # GOLDEN: space before is 12pt
    try:
        sb_pass_count = 0
        for para in heading_paras:
            sb = get_effective_spacing(para, doc, 'space_before')
            if sb is not None and abs(sb - 12.0) <= 0.5:
                print(f"  OK: '{para.text}' space_before = {sb}pt")
                sb_pass_count += 1
            else:
                print(f"  FAIL: '{para.text}' space_before = {sb}pt, expected 12.0pt")
        if sb_pass_count == 3:
            print(f"PASS: Component 3 -- All headings have 12pt space before (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- {sb_pass_count}/3 headings have correct space before")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Space after is 6pt on all 3 headings (0.25 pts)
    # INITIAL: space after is 0pt
    # GOLDEN: space after is 6pt
    try:
        sa_pass_count = 0
        for para in heading_paras:
            sa = get_effective_spacing(para, doc, 'space_after')
            if sa is not None and abs(sa - 6.0) <= 0.5:
                print(f"  OK: '{para.text}' space_after = {sa}pt")
                sa_pass_count += 1
            else:
                print(f"  FAIL: '{para.text}' space_after = {sa}pt, expected 6.0pt")
        if sa_pass_count == 3:
            print(f"PASS: Component 4 -- All headings have 6pt space after (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 -- {sa_pass_count}/3 headings have correct space after")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
