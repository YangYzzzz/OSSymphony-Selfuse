"""
Reward Script: Add speaker notes to Lecture.pptx and export as PDF with notes pages
Task ID: impress_wf_009
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.15 x 4 = 0.60): Speaker notes on slides 1-4 with correct text
  - Component 2 (0.40): Lecture_Notes.pdf exists on Desktop and is a valid PDF
"""

import os
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'impress_wf_009'
PPTX_PATH = os.path.join(WORKDIR, 'Desktop', 'Lecture.pptx')
PDF_PATH = os.path.join(WORKDIR, 'Desktop', 'Lecture_Notes.pdf')

# Expected notes for each slide (1-indexed)
EXPECTED_NOTES = {
    1: 'Welcome the audience, introduce topic',
    2: 'Explain key concepts with examples',
    3: 'Show demo if time permits',
    4: 'Summarize and open for questions',
}


def get_notes_from_zip(pptx_path, slide_num):
    """
    Extract notes text for a slide by parsing the ZIP/XML directly.
    This avoids python-pptx's side effect of creating notes slides on access.
    slide_num is 1-based.
    """
    import xml.etree.ElementTree as ET
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            # First check if any notesSlides exist
            notes_files = [n for n in zf.namelist() if 'notesSlides/notesSlide' in n]
            if not notes_files:
                return ""

            # Find the relationship from the slide to its notes slide
            slide_rels_path = f'ppt/slides/_rels/slide{slide_num}.xml.rels'
            if slide_rels_path not in zf.namelist():
                return ""

            with zf.open(slide_rels_path) as rf:
                rels_root = ET.parse(rf).getroot()

            notes_target = None
            for rel in rels_root.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
                if 'notesSlide' in rel.get('Target', ''):
                    notes_target = rel.get('Target')
                    break

            if notes_target is None:
                return ""

            # Resolve the path
            notes_path = 'ppt/slides/' + notes_target
            # Normalize (e.g., ../notesSlides/notesSlide1.xml)
            notes_path = os.path.normpath(notes_path).replace('\\', '/')
            # Ensure it starts with ppt/
            if not notes_path.startswith('ppt/'):
                notes_path = 'ppt/' + notes_path

            if notes_path not in zf.namelist():
                return ""

            with zf.open(notes_path) as nf:
                notes_root = ET.parse(nf).getroot()

            # Extract text from notes body, skipping the slide number placeholder
            # The notes text frame is typically in sp elements with ph type="body"
            texts = []
            for sp in notes_root.findall('.//p:sp', ns):
                # Check if this is the body placeholder (notes text), not slide image or slide number
                nvSpPr = sp.find('.//p:nvSpPr/p:nvPr/p:ph', ns)
                if nvSpPr is not None:
                    ph_type = nvSpPr.get('type', '')
                    if ph_type == 'body':
                        for para in sp.findall('.//a:p', ns):
                            para_text = ''.join(
                                t.text for t in para.findall('.//a:t', ns) if t.text
                            )
                            if para_text.strip():
                                texts.append(para_text.strip())

            return '\n'.join(texts)
    except Exception as e:
        print(f"  ZIP parse error for slide {slide_num}: {e}")
        return ""


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: pptx file must exist
    if not os.path.exists(PPTX_PATH):
        print(f"CRITICAL: PPTX file not found: {PPTX_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Components 1a-1d: Speaker notes on each slide (0.15 points each, 0.60 total)
    for slide_num, expected_text in EXPECTED_NOTES.items():
        try:
            actual_notes = get_notes_from_zip(PPTX_PATH, slide_num)
            if actual_notes and expected_text.lower() in actual_notes.lower():
                print(f"PASS: Component 1{chr(96+slide_num)} — Slide {slide_num} notes contain '{expected_text}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1{chr(96+slide_num)} — Slide {slide_num} notes expected '{expected_text}', found: '{actual_notes}'")
        except Exception as e:
            print(f"ERROR: Component 1{chr(96+slide_num)} — Could not check slide {slide_num} notes: {e}")

    # Component 2: PDF file exists and is a valid PDF (0.40 points)
    try:
        if os.path.exists(PDF_PATH):
            with open(PDF_PATH, 'rb') as f:
                header = f.read(5)
            if header == b'%PDF-':
                # Also check file size is reasonable (>1KB means it has content)
                pdf_size = os.path.getsize(PDF_PATH)
                if pdf_size > 1024:
                    print(f"PASS: Component 2 — Lecture_Notes.pdf exists, valid PDF header, size={pdf_size} bytes (0.40 pts)")
                    total_score += 0.40
                else:
                    print(f"FAIL: Component 2 — Lecture_Notes.pdf too small ({pdf_size} bytes), likely empty")
            else:
                print(f"FAIL: Component 2 — Lecture_Notes.pdf has invalid header: {header}")
        else:
            print(f"FAIL: Component 2 — Lecture_Notes.pdf not found at {PDF_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check PDF: {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
