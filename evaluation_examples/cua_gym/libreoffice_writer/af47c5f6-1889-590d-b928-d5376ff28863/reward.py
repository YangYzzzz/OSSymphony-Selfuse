"""
Reward Script: Insert firm logo in header with left alignment and 1.5cm height
Task ID: writer_legal_082
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Header contains an inline image
  Component 2 (0.30): Image height is ~1.5 cm (within tolerance)
  Component 3 (0.20): Header paragraph alignment is LEFT
  Component 4 (0.15): Firm name text 'Mitchell & Associates, LLP' remains in header
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_082'


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.shared import Emu
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the header from the first section
    try:
        section = doc.sections[0]
        header = section.header
        header_paras = header.paragraphs
        if not header_paras:
            print("FAIL: No paragraphs found in header")
            print("REWARD: 0.0")
            return 0.0
        header_para = header_paras[0]
    except Exception as e:
        print(f"CRITICAL: Cannot access header: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    }

    # Component 1: Header contains an inline image (0.35 points)
    try:
        has_image = 'graphicData' in header_para._element.xml
        if has_image:
            print(f"PASS: Component 1 -- Image found in header paragraph (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- No image found in header paragraph")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Image height is approximately 1.5 cm (0.30 points)
    # 1.5 cm = 540000 EMU; allow tolerance of 0.3 cm (108000 EMU)
    try:
        drawings = header_para._element.findall('.//w:drawing', ns)
        height_ok = False
        for drawing in drawings:
            for inline in drawing.findall('.//wp:inline', ns):
                extent = inline.find('wp:extent', ns)
                if extent is not None:
                    cy = int(extent.get('cy', 0))
                    height_cm = cy / 360000.0  # EMU to cm
                    print(f"  Image height: {height_cm:.2f} cm ({cy} EMU)")
                    if abs(height_cm - 1.5) <= 0.3:
                        height_ok = True
        if height_ok:
            print(f"PASS: Component 2 -- Image height within 1.5cm tolerance (0.30 pts)")
            total_score += 0.30
        else:
            if not drawings:
                print(f"FAIL: Component 2 -- No drawing elements found in header")
            else:
                print(f"FAIL: Component 2 -- Image height not within 1.5cm +/- 0.3cm")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Header paragraph alignment is LEFT (0.20 points)
    # Initial state has CENTER alignment; task requires left-aligned logo
    try:
        from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
        alignment = header_para.paragraph_format.alignment
        # Check alignment is LEFT or None-with-left-in-xml
        xml_str = header_para._element.xml
        is_left = False
        if alignment == WD_PARAGRAPH_ALIGNMENT.LEFT:
            is_left = True
        elif 'w:jc w:val="left"' in xml_str:
            is_left = True
        # Also accept if alignment is None (default=left) AND not center
        elif alignment is None and 'w:jc' not in xml_str:
            # Default alignment is left when no jc element present
            is_left = True

        if is_left:
            print(f"PASS: Component 3 -- Header alignment is LEFT (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- Header alignment is {alignment}, expected LEFT")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Firm name text still present in header (0.15 points)
    # The text 'Mitchell & Associates, LLP' should appear in the header after the image
    try:
        header_text = header_para.text
        if 'Mitchell' in header_text and 'Associates' in header_text and 'LLP' in header_text:
            # Also verify it appears AFTER the image (image run should come before text run)
            runs = header_para.runs
            image_run_idx = -1
            text_run_idx = -1
            for idx, run in enumerate(runs):
                if 'graphicData' in run._element.xml:
                    image_run_idx = idx
                if 'Mitchell' in run.text:
                    text_run_idx = idx
            if image_run_idx >= 0 and text_run_idx > image_run_idx:
                print(f"PASS: Component 4 -- Firm name present after image in header (0.15 pts)")
                total_score += 0.15
            elif image_run_idx < 0:
                # No image but text is there -- partial: text exists but ordering can't be verified
                print(f"FAIL: Component 4 -- Firm name present but no image to verify ordering")
            else:
                print(f"FAIL: Component 4 -- Firm name not positioned after image (img_idx={image_run_idx}, text_idx={text_run_idx})")
        else:
            print(f"FAIL: Component 4 -- Firm name 'Mitchell & Associates, LLP' not found in header text: {repr(header_text)}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
