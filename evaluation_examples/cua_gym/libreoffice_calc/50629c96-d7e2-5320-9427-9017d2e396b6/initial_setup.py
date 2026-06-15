"""
Initial Setup: Create a multi-page style guide PDF with intentional formatting inconsistencies.
Task ID: pdf_cr_067
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_067'
OUTPUT_DIR = f'{WORKDIR}/Desktop'
OUTPUT = f'{OUTPUT_DIR}/style_guide.pdf'

# Page dimensions (A4)
PW, PH = 595, 842
MARGIN_LEFT = 72
MARGIN_RIGHT = 523
MARGIN_TOP = 72
MARGIN_BOTTOM = 770

# Consistent styles (what the guide SHOULD use)
HEADING_FONT = "hebo"    # Helvetica-Bold
HEADING_SIZE = 18.0
BODY_FONT = "helv"       # Helvetica
BODY_SIZE = 11.0

# Inconsistency fonts (deviations to be detected)
WRONG_HEADING_FONT = "tibo"   # Times-Bold (wrong for headings)
WRONG_BODY_FONT = "cour"      # Courier (wrong for body)
WRONG_BODY_SIZE = 13.0


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def insert_heading(page, y, text, fontname=HEADING_FONT, fontsize=HEADING_SIZE):
    """Insert a heading and return new y position."""
    page.insert_text(
        pymupdf.Point(MARGIN_LEFT, y),
        text,
        fontsize=fontsize,
        fontname=fontname,
        color=(0.1, 0.1, 0.3),
    )
    return y + fontsize + 12


def insert_body(page, y, text, fontname=BODY_FONT, fontsize=BODY_SIZE, max_width=None):
    """Insert body text in a textbox and return new y position."""
    if max_width is None:
        max_width = MARGIN_RIGHT
    rect = pymupdf.Rect(MARGIN_LEFT, y, max_width, y + 200)
    excess = page.insert_textbox(
        rect,
        text,
        fontsize=fontsize,
        fontname=fontname,
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )
    # Estimate height used (rough: count lines)
    chars_per_line = int((max_width - MARGIN_LEFT) / (fontsize * 0.5))
    if chars_per_line <= 0:
        chars_per_line = 60
    num_lines = max(1, len(text) // chars_per_line + 1)
    used_height = num_lines * (fontsize + 4) + 8
    return y + used_height


def insert_separator(page, y):
    """Draw a thin horizontal line separator."""
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_LEFT, y), pymupdf.Point(MARGIN_RIGHT, y))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()
    return y + 15


def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc = pymupdf.open()

    # ===== PAGE 1: Title & Introduction =====
    page = doc.new_page(width=PW, height=PH)
    y = MARGIN_TOP

    # Title (uses correct heading style)
    y = insert_heading(page, y, "Meridian Corp Style Guide", fontsize=24)
    y += 5
    y = insert_separator(page, y)
    y += 5

    # Section heading (correct)
    y = insert_heading(page, y, "1. Introduction")
    y += 2

    y = insert_body(page, y,
        "This document outlines the official formatting and typographic standards for all "
        "Meridian Corp communications. All departments must adhere to these guidelines when "
        "producing internal reports, external proposals, and client-facing documentation."
    )
    y += 8

    y = insert_body(page, y,
        "The standards described herein were approved by the Executive Communications Board "
        "on March 15, 2025, and supersede all previous formatting directives. Questions about "
        "specific applications should be directed to the Brand Standards team."
    )
    y += 15

    # Section heading (correct)
    y = insert_heading(page, y, "2. Typography Standards")
    y += 2

    y = insert_body(page, y,
        "All official documents must use Helvetica as the primary typeface. Headings should be "
        "rendered in Helvetica Bold at 18 points. Body text should use Helvetica Regular at 11 "
        "points with single line spacing. No other typefaces are permitted in standard documents."
    )
    y += 8

    y = insert_body(page, y,
        "Exceptions may be granted for technical documentation that requires monospaced fonts "
        "for code samples. In such cases, Courier may be used exclusively within designated "
        "code blocks, but never for body text or headings."
    )
    y += 15

    # Section heading (correct)
    y = insert_heading(page, y, "3. Color Palette")
    y += 2

    y = insert_body(page, y,
        "The primary brand color is Meridian Navy (#1A1A4D) used for all headings and emphasis text. "
        "Body text must use standard black (#000000). Accent colors include Meridian Gold (#C4962A) "
        "for highlights and Meridian Gray (#808080) for secondary text and dividers."
    )
    y += 8

    y = insert_body(page, y,
        "Charts and data visualizations should use the approved palette: Navy, Gold, Forest Green "
        "(#2D5F2D), Slate Blue (#4A7099), and Warm Red (#C44A2A). Gradients are not permitted in "
        "official charts. All colors must meet WCAG AA contrast requirements."
    )

    # ===== PAGE 2: Document Layout & Formatting Rules =====
    page = doc.new_page(width=PW, height=PH)
    y = MARGIN_TOP

    # INCONSISTENCY 1: This heading uses Times-Bold instead of Helvetica-Bold
    y = insert_heading(page, y, "4. Document Layout", fontname=WRONG_HEADING_FONT)
    y += 2

    y = insert_body(page, y,
        "Standard documents use A4 page size with 1-inch margins on all sides. The header area "
        "occupies the top 0.5 inches and contains the document title and date. The footer area "
        "contains the page number centered and the confidentiality classification on the right."
    )
    y += 8

    y = insert_body(page, y,
        "Section breaks should use a thin horizontal rule (0.5pt) in Meridian Gray. New major "
        "sections should begin on a fresh page when the remaining space on the current page is "
        "less than 3 inches."
    )
    y += 15

    # Section heading (correct)
    y = insert_heading(page, y, "5. Tables and Data Presentation")
    y += 2

    y = insert_body(page, y,
        "Tables must use alternating row colors with white and light gray (#F5F5F5) backgrounds. "
        "Header rows use Meridian Navy background with white text in Helvetica Bold at 10 points. "
        "Cell padding should be 4 points minimum on all sides."
    )
    y += 8

    # INCONSISTENCY 2: This body paragraph uses Courier instead of Helvetica
    y = insert_body(page, y,
        "Column widths should be proportional to content. Numeric columns must be right-aligned "
        "with consistent decimal places. Currency values use two decimal places with dollar sign "
        "prefix. Percentage values use one decimal place with percent suffix.",
        fontname=WRONG_BODY_FONT,
    )
    y += 15

    # Section heading (correct)
    y = insert_heading(page, y, "6. Image and Figure Guidelines")
    y += 2

    y = insert_body(page, y,
        "All images must have a minimum resolution of 300 DPI for print and 150 DPI for screen "
        "documents. Figures should be captioned using Helvetica Italic at 9 points, centered below "
        "the image. Figure numbering follows the section number (e.g., Figure 4.1, Figure 4.2)."
    )

    # ===== PAGE 3: Writing Style & Tone =====
    page = doc.new_page(width=PW, height=PH)
    y = MARGIN_TOP

    # Section heading (correct)
    y = insert_heading(page, y, "7. Writing Style and Tone")
    y += 2

    y = insert_body(page, y,
        "Meridian Corp communications use a professional yet approachable tone. Avoid jargon "
        "unless writing for a specialized technical audience. Use active voice whenever possible. "
        "Sentences should average 15-20 words. Paragraphs should contain 3-5 sentences."
    )
    y += 8

    y = insert_body(page, y,
        "First-person plural (we, our) is preferred for internal documents. Third-person "
        "(Meridian Corp, the company) should be used in client-facing materials. Avoid "
        "contractions in formal documents but permit them in internal communications."
    )
    y += 15

    # INCONSISTENCY 3: This heading uses wrong font (Times-Bold) AND wrong heading
    y = insert_heading(page, y, "8. Citation and Reference Format", fontname=WRONG_HEADING_FONT)
    y += 2

    y = insert_body(page, y,
        "Internal references use the Meridian Citation Standard (MCS), which follows a modified "
        "APA format. Author last names appear first, followed by initials. Publication year is "
        "enclosed in parentheses. Titles are italicized for books and in quotation marks for articles."
    )
    y += 8

    y = insert_body(page, y,
        "Web references include the full URL and access date. Internal document references use "
        "the document ID number assigned by the Records Management System. Cross-references "
        "within the same document use section numbers rather than page numbers."
    )
    y += 15

    # Section heading (correct)
    y = insert_heading(page, y, "9. Approval Workflow")
    y += 2

    y = insert_body(page, y,
        "All external documents require approval from the department head and the Brand Standards "
        "team before distribution. Internal documents require only department head approval. Draft "
        "documents must be clearly marked with a DRAFT watermark until final approval is granted."
    )
    y += 8

    # INCONSISTENCY 4: Body text with wrong size (13pt instead of 11pt)
    y = insert_body(page, y,
        "The review cycle is five business days for standard documents and ten business days "
        "for legal or regulatory submissions. Expedited review may be requested through the "
        "Priority Communications channel with VP-level sponsorship.",
        fontsize=WRONG_BODY_SIZE,
    )

    # ===== PAGE 4: Appendix =====
    page = doc.new_page(width=PW, height=PH)
    y = MARGIN_TOP

    # Section heading (correct)
    y = insert_heading(page, y, "Appendix A: Quick Reference Card")
    y += 2

    y = insert_body(page, y,
        "Heading Font: Helvetica Bold, 18pt, Meridian Navy color. "
        "Body Font: Helvetica Regular, 11pt, black. "
        "Page Size: A4 (210mm x 297mm). "
        "Margins: 1 inch (72pt) on all sides."
    )
    y += 15

    y = insert_heading(page, y, "Appendix B: Approved Templates")
    y += 2

    y = insert_body(page, y,
        "The following templates are maintained by the Brand Standards team and available on "
        "the corporate intranet: Internal Memo (MER-TMPL-001), External Proposal (MER-TMPL-002), "
        "Technical Report (MER-TMPL-003), Meeting Minutes (MER-TMPL-004), and Quarterly Review "
        "(MER-TMPL-005). All templates are updated quarterly."
    )
    y += 8

    y = insert_body(page, y,
        "Custom templates may be requested through the Brand Standards team with a minimum "
        "lead time of two weeks. Template requests must include a sample document, intended "
        "audience, and distribution scope. Approved custom templates are assigned a MER-TMPL "
        "identifier and added to the template library."
    )
    y += 15

    # INCONSISTENCY 5: Body text with wrong font (Courier) on page 4
    y = insert_body(page, y,
        "Contact the Brand Standards team at brand-standards@meridian-corp.com for questions "
        "about this style guide or to request exceptions to these formatting rules. Emergency "
        "formatting consultations are available during business hours at extension 4455.",
        fontname=WRONG_BODY_FONT,
    )

    # Set metadata
    doc.set_metadata({
        "title": "Meridian Corp Style Guide",
        "author": "Brand Standards Team",
        "subject": "Corporate Document Formatting Standards",
        "keywords": "style guide, formatting, typography, branding",
        "creator": "Meridian Corp Communications",
    })

    # Set Table of Contents
    toc = [
        [1, "1. Introduction", 1],
        [1, "2. Typography Standards", 1],
        [1, "3. Color Palette", 1],
        [1, "4. Document Layout", 2],
        [1, "5. Tables and Data Presentation", 2],
        [1, "6. Image and Figure Guidelines", 2],
        [1, "7. Writing Style and Tone", 3],
        [1, "8. Citation and Reference Format", 3],
        [1, "9. Approval Workflow", 3],
        [1, "Appendix A: Quick Reference Card", 4],
        [1, "Appendix B: Approved Templates", 4],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
