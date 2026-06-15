"""
Reward Script: Create a formatted envelope layout in a Writer document
Task ID: writer_rd_050
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Envelope section exists (2+ sections, first section landscape with envelope dimensions)
  Component 2 (0.25): Sender address in envelope section - top-left, Liberation Sans 10pt
  Component 3 (0.25): Recipient address in envelope section - centered, Liberation Sans 12pt
  Component 4 (0.25): Original letter content preserved in subsequent section
"""

import os

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_050'


def verify_task(file_path):
    """
    Verify envelope creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Must have 2+ sections (envelope + letter)
    # If only 1 section, no envelope was created => score 0.0
    num_sections = len(doc.sections)
    if num_sections < 2:
        print(f"FAIL: Only {num_sections} section(s) found. No envelope section created.")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Envelope section has correct dimensions and orientation (0.25 points)
    # Envelope #10: 9.5 x 4.125 inches, landscape
    try:
        env_sec = doc.sections[0]
        pw_in = env_sec.page_width / 914400
        ph_in = env_sec.page_height / 914400

        # Check landscape orientation
        sectPr = env_sec._sectPr
        pgSz = sectPr.find(qn('w:pgSz'))
        orient_attr = pgSz.get(qn('w:orient')) if pgSz is not None else None
        is_landscape = (orient_attr == 'landscape' or env_sec.orientation == WD_ORIENT.LANDSCAPE)

        # Envelope #10: width ~9.5in, height ~4.125in (in landscape mode)
        # Allow tolerance of 0.5 inches
        width_ok = abs(pw_in - 9.5) < 0.5
        height_ok = abs(ph_in - 4.125) < 0.5

        # Also accept inverse dimensions
        alt_width_ok = abs(pw_in - 4.125) < 0.5
        alt_height_ok = abs(ph_in - 9.5) < 0.5

        dims_ok = (width_ok and height_ok) or (alt_width_ok and alt_height_ok)

        if is_landscape and dims_ok:
            print(f"PASS: Component 1 - Envelope section: {pw_in:.3f}x{ph_in:.3f}in, landscape (0.25 pts)")
            total_score += 0.25
        elif dims_ok:
            print(f"PARTIAL: Component 1 - Dimensions correct but not landscape: {pw_in:.3f}x{ph_in:.3f}in (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - Wrong dimensions: {pw_in:.3f}x{ph_in:.3f}in (expected ~9.5x4.125 landscape)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Collect paragraphs belonging to envelope section (section 0, before first section break)
    envelope_paras = []
    try:
        body = doc.element.body
        for child in body:
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag == 'p':
                envelope_paras.append(child)
                # Check if this paragraph contains a section break (marks end of section 0)
                pPr = child.find(qn('w:pPr'))
                if pPr is not None and pPr.find(qn('w:sectPr')) is not None:
                    break
        print(f"INFO: Found {len(envelope_paras)} paragraphs in envelope section")
    except Exception as e:
        print(f"ERROR: Could not parse envelope paragraphs: {e}")

    # Component 2: Sender address in envelope - left-aligned, Liberation Sans 10pt (0.25 points)
    # Sender: "TechVision Inc.", "456 Oak Avenue", "Chicago, IL 60601"
    try:
        sender_lines = ["TechVision Inc.", "456 Oak Avenue", "Chicago, IL 60601"]
        sender_found = 0
        sender_font_ok = 0
        sender_align_ok = 0

        for elem in envelope_paras:
            para_text = ''.join(t.text or '' for t in elem.iter(qn('w:t')))
            para_text_stripped = para_text.strip()

            if para_text_stripped in sender_lines:
                sender_found += 1

                # Check alignment - should be LEFT or default
                pPr = elem.find(qn('w:pPr'))
                jc = None
                if pPr is not None:
                    jc_elem = pPr.find(qn('w:jc'))
                    if jc_elem is not None:
                        jc = jc_elem.get(qn('w:val'))
                if jc in (None, 'left', 'start'):
                    sender_align_ok += 1

                # Check font: Liberation Sans 10pt
                for r in elem.iter(qn('w:r')):
                    rPr = r.find(qn('w:rPr'))
                    if rPr is not None:
                        sz = rPr.find(qn('w:sz'))
                        rFonts = rPr.find(qn('w:rFonts'))
                        font_name = None
                        if rFonts is not None:
                            font_name = rFonts.get(qn('w:ascii')) or rFonts.get(qn('w:hAnsi'))
                        font_size = None
                        if sz is not None:
                            # sz val is in half-points
                            font_size = int(sz.get(qn('w:val'))) / 2
                        # Must be 10pt (not 11pt which is the letter font)
                        if font_name and 'Liberation Sans' in font_name and font_size is not None and abs(font_size - 10.0) < 0.5:
                            sender_font_ok += 1
                        break

        sender_score = 0.0
        if sender_found >= 3:
            sender_score += 0.10
        if sender_align_ok >= 3:
            sender_score += 0.075
        if sender_font_ok >= 2:
            sender_score += 0.075

        if sender_score > 0:
            print(f"PASS: Component 2 - Sender: {sender_found}/3 found, {sender_align_ok}/3 left, {sender_font_ok}/3 font ok ({sender_score:.3f} pts)")
            total_score += sender_score
        else:
            print(f"FAIL: Component 2 - Sender: {sender_found}/3 found, {sender_align_ok}/3 left, {sender_font_ok}/3 font ok")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Recipient address in envelope - centered, Liberation Sans 12pt (0.25 points)
    # Recipient: "John Smith", "Acme Corp", "123 Main Street", "Springfield, IL 62701"
    try:
        recipient_lines = ["John Smith", "Acme Corp", "123 Main Street", "Springfield, IL 62701"]
        recip_found = 0
        recip_center_ok = 0
        recip_font_ok = 0

        for elem in envelope_paras:
            para_text = ''.join(t.text or '' for t in elem.iter(qn('w:t')))
            para_text_stripped = para_text.strip()

            if para_text_stripped in recipient_lines:
                recip_found += 1

                # Check alignment - should be CENTER
                pPr = elem.find(qn('w:pPr'))
                jc = None
                if pPr is not None:
                    jc_elem = pPr.find(qn('w:jc'))
                    if jc_elem is not None:
                        jc = jc_elem.get(qn('w:val'))
                if jc == 'center':
                    recip_center_ok += 1

                # Check font: Liberation Sans 12pt
                for r in elem.iter(qn('w:r')):
                    rPr = r.find(qn('w:rPr'))
                    if rPr is not None:
                        sz = rPr.find(qn('w:sz'))
                        rFonts = rPr.find(qn('w:rFonts'))
                        font_name = None
                        if rFonts is not None:
                            font_name = rFonts.get(qn('w:ascii')) or rFonts.get(qn('w:hAnsi'))
                        font_size = None
                        if sz is not None:
                            font_size = int(sz.get(qn('w:val'))) / 2
                        if font_name and 'Liberation Sans' in font_name and font_size is not None and abs(font_size - 12.0) < 0.5:
                            recip_font_ok += 1
                        break

        recip_score = 0.0
        if recip_found >= 4:
            recip_score += 0.10
        elif recip_found >= 2:
            recip_score += 0.05
        if recip_center_ok >= 3:
            recip_score += 0.075
        if recip_font_ok >= 2:
            recip_score += 0.075

        if recip_score > 0:
            print(f"PASS: Component 3 - Recipient: {recip_found}/4 found, {recip_center_ok}/4 centered, {recip_font_ok}/4 font ok ({recip_score:.3f} pts)")
            total_score += recip_score
        else:
            print(f"FAIL: Component 3 - Recipient: {recip_found}/4 found, {recip_center_ok}/4 centered, {recip_font_ok}/4 font ok")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Original letter content preserved in section 1 (0.25 points)
    # Verify the letter body still exists and section 1 is standard letter size
    try:
        all_text = ' '.join(p.text for p in doc.paragraphs)
        key_phrases = [
            "Dear Mr. Smith",
            "Michael Chen",
            "Director of Client Solutions",
            "Phase 2 rollout",
        ]
        phrases_found = sum(1 for phrase in key_phrases if phrase in all_text)

        sec1 = doc.sections[1]
        sec1_pw = sec1.page_width / 914400
        sec1_ph = sec1.page_height / 914400
        letter_page_ok = abs(sec1_pw - 8.5) < 0.5 and abs(sec1_ph - 11.0) < 0.5

        if phrases_found >= 4 and letter_page_ok:
            print(f"PASS: Component 4 - Letter preserved, {phrases_found}/4 phrases, section 1 is {sec1_pw:.1f}x{sec1_ph:.1f}in (0.25 pts)")
            total_score += 0.25
        elif phrases_found >= 3:
            print(f"PARTIAL: Component 4 - {phrases_found}/4 phrases found, page ok={letter_page_ok} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 - Only {phrases_found}/4 letter phrases found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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
