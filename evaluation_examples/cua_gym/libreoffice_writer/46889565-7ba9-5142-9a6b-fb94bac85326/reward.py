"""
Reward Script: Insert 3 image placeholder text frames with captions and text wrapping
Task ID: writer_mktg_048
Domain: libreoffice_writer
Scoring:
  Component 1: 3 text box drawing elements present with correct labels (0.4 pts)
  Component 2: Text boxes are ~3 inches wide with text wrap (wrapSquare/wrapTight/wrapThrough) (0.3 pts)
  Component 3: 3 caption paragraphs exist: italic, 10pt, centered with correct caption text (0.3 pts)
Total: 1.0
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_mktg_048'

# Namespace map for XML parsing
NS = {
    'w':   'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
    'wp':  'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a':   'http://schemas.openxmlformats.org/drawingml/2006/main',
    'mc':  'http://schemas.openxmlformats.org/markup-compatibility/2006',
}

# Expected label texts inside the 3 text frames
EXPECTED_LABELS = ['Keynote Photo', 'Expo Hall Photo', 'Award Ceremony Photo']

# Expected caption texts (order-insensitive)
EXPECTED_CAPTIONS = ['Photo 1: Opening Keynote', 'Photo 2: Exhibition Hall', 'Photo 3: Award Ceremony']

# 3 inches in EMU = 3 * 914400 = 2743200
THREE_INCHES_EMU = 2743200
# Allow ±10% tolerance (~274320 EMU = ±0.3 inches)
WIDTH_TOLERANCE = 274320

# Wrap types that indicate text-around-frame wrapping
WRAP_TAGS = {'wrapSquare', 'wrapTight', 'wrapThrough', 'wrapTopAndBottom'}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid docx
    try:
        if not os.path.exists(file_path):
            print(f"CRITICAL: File not found: {file_path}")
            print("REWARD: 0.0")
            return 0.0

        with zipfile.ZipFile(file_path, 'r') as z:
            with z.open('word/document.xml') as f:
                xml_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        root = etree.fromstring(xml_content)
    except Exception as e:
        print(f"CRITICAL: Cannot parse XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Also load with python-docx for caption paragraph checks
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load docx via python-docx: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: 3 text box drawing elements with correct label text (0.4 pts)
    # -----------------------------------------------------------------------
    # Each text box should contain one of the expected label texts.
    try:
        drawings = root.findall('.//w:drawing', NS)
        found_labels = []
        drawing_details = []

        for drawing in drawings:
            # Collect text content inside this drawing
            texts = drawing.findall('.//w:t', NS)
            text_content = ''.join(t.text or '' for t in texts).strip()
            drawing_details.append(text_content)

            # Check if this drawing is a text box (has wps:txbx or txbxContent)
            txbx = drawing.find('.//wps:txbx', NS)
            txbx_content = drawing.find('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}txbxContent')
            if txbx is not None or txbx_content is not None:
                found_labels.append(text_content)

        # Check how many expected labels are present (case-insensitive substring match)
        matched_labels = []
        for expected in EXPECTED_LABELS:
            for found in found_labels:
                if expected.lower() in found.lower() or found.lower() in expected.lower():
                    matched_labels.append(expected)
                    break

        num_matched = len(matched_labels)
        if num_matched == 3:
            print(f"PASS: Component 1 — All 3 text frame labels found: {matched_labels} (0.4 pts)")
            total_score += 0.4
        elif num_matched >= 1:
            partial = round(0.4 * num_matched / 3, 4)
            print(f"PARTIAL: Component 1 — {num_matched}/3 text frame labels found: {matched_labels} ({partial} pts)")
            print(f"  Expected: {EXPECTED_LABELS}")
            print(f"  Found text boxes: {found_labels}")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 1 — No matching text frame labels found")
            print(f"  Expected: {EXPECTED_LABELS}")
            print(f"  Found drawings ({len(drawings)}): {drawing_details}")
            print(f"  Found text boxes: {found_labels}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Text boxes are ~3 inches wide AND have text wrapping (0.3 pts)
    # -----------------------------------------------------------------------
    try:
        drawings_for_width = root.findall('.//w:drawing', NS)
        width_ok_count = 0
        wrap_ok_count = 0
        textbox_count = 0

        for drawing in drawings_for_width:
            # Only check drawings that contain text boxes
            txbx = drawing.find('.//wps:txbx', NS)
            txbx_content = drawing.find('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}txbxContent')
            if txbx is None and txbx_content is None:
                continue
            textbox_count += 1

            # Check extent (width)
            extent = drawing.find('.//wp:extent', NS)
            if extent is not None:
                cx_str = extent.get('cx')
                if cx_str:
                    cx = int(cx_str)
                    width_inches = cx / 914400.0
                    if abs(cx - THREE_INCHES_EMU) <= WIDTH_TOLERANCE:
                        width_ok_count += 1
                    else:
                        print(f"  Width check: cx={cx} EMU = {width_inches:.3f} inches (expected ~3.0)")

            # Check wrap type — anchor element must exist with a wrap child
            anchor = drawing.find('.//wp:anchor', NS)
            if anchor is not None:
                for child in anchor:
                    local_tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    if local_tag in WRAP_TAGS:
                        wrap_ok_count += 1
                        break

        # Score: need all 3 text boxes to have correct width AND wrap
        if textbox_count == 0:
            print("FAIL: Component 2 — No text boxes found for width/wrap check")
        else:
            width_pass = width_ok_count == 3
            wrap_pass = wrap_ok_count == 3

            if width_pass and wrap_pass:
                print(f"PASS: Component 2 — All 3 text boxes are 3 inches wide with text wrap (0.3 pts)")
                total_score += 0.3
            elif width_pass and not wrap_pass:
                print(f"PARTIAL: Component 2 — Width correct ({width_ok_count}/3) but wrap missing ({wrap_ok_count}/3) (0.15 pts)")
                total_score += 0.15
            elif not width_pass and wrap_pass:
                print(f"PARTIAL: Component 2 — Wrap correct ({wrap_ok_count}/3) but width wrong ({width_ok_count}/3 are ~3in) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Width correct: {width_ok_count}/3, Wrap correct: {wrap_ok_count}/3")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Caption paragraphs present — italic, 10pt, centered (0.3 pts)
    # -----------------------------------------------------------------------
    try:
        from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

        caption_texts_found = []
        caption_italic_ok = 0
        caption_size_ok = 0
        caption_center_ok = 0

        for para in doc.paragraphs:
            para_text = para.text.strip()
            if not para_text:
                continue
            # Check if this paragraph matches any expected caption
            matched_caption = None
            for expected_cap in EXPECTED_CAPTIONS:
                if expected_cap.lower() == para_text.lower() or expected_cap in para_text:
                    matched_caption = expected_cap
                    break
            if matched_caption is None:
                continue

            caption_texts_found.append(para_text)

            # Check italic
            all_italic = all(
                (run.italic is True or run.italic is None) and run.text.strip()
                for run in para.runs if run.text.strip()
            )
            # More strict: check any run is explicitly italic
            any_italic = any(run.italic is True for run in para.runs if run.text.strip())
            if any_italic:
                caption_italic_ok += 1

            # Check font size (10pt)
            any_10pt = any(
                run.font.size is not None and abs(run.font.size.pt - 10.0) < 0.5
                for run in para.runs if run.text.strip()
            )
            if any_10pt:
                caption_size_ok += 1

            # Check center alignment
            align = para.paragraph_format.alignment
            if align == WD_PARAGRAPH_ALIGNMENT.CENTER:
                caption_center_ok += 1

        num_captions_found = len(caption_texts_found)
        print(f"  Captions found: {caption_texts_found}")
        print(f"  Italic OK: {caption_italic_ok}/{num_captions_found}")
        print(f"  Size 10pt OK: {caption_size_ok}/{num_captions_found}")
        print(f"  Centered OK: {caption_center_ok}/{num_captions_found}")

        # Score by how many conditions are fully met across all 3 captions
        if num_captions_found == 3 and caption_italic_ok == 3 and caption_size_ok == 3 and caption_center_ok == 3:
            print(f"PASS: Component 3 — All 3 captions present, italic 10pt centered (0.3 pts)")
            total_score += 0.3
        elif num_captions_found >= 1:
            # Partial: award proportionally
            fraction = (
                (num_captions_found / 3) * 0.1
                + (caption_italic_ok / 3) * 0.1
                + (caption_size_ok / 3) * 0.05
                + (caption_center_ok / 3) * 0.05
            )
            partial = round(min(fraction, 0.3), 4)
            print(f"PARTIAL: Component 3 — Captions: {num_captions_found}/3, italic: {caption_italic_ok}/3, "
                  f"10pt: {caption_size_ok}/3, centered: {caption_center_ok}/3 → {partial} pts")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 3 — No matching caption paragraphs found")
            print(f"  Expected captions: {EXPECTED_CAPTIONS}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Final score
    # -----------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: use canonical artifact path on VM
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
