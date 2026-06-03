"""
Reward Script: Insert a frame around the 'Quick Reference Card' section
Task ID: writer_tech_075
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Text frame exists containing Quick Reference Card content
  Component 2 (0.25): Double-line border on the frame
  Component 3 (0.20): 0.5 cm inner padding (~14.17pt)
  Component 4 (0.20): Frame anchored to the page
"""

import os
import re
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_075'

# Namespaces used in OOXML / VML
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'v': 'urn:schemas-microsoft-com:vml',
    'o': 'urn:schemas-microsoft-com:office:office',
    'w10': 'urn:schemas-microsoft-com:office:word',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'wp14': 'http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice document."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def get_text_from_element(elem):
    """Extract all w:t text from an XML element recursively."""
    texts = []
    for t in elem.findall('.//w:t', NS):
        if t.text:
            texts.append(t.text)
    return ' '.join(texts)


def find_text_frames_vml(body):
    """Find VML text frames (v:shape with txbxContent) under w:pict."""
    frames = []
    for pict in body.findall('.//w:pict', NS):
        for shape in pict.findall('.//v:shape', NS):
            txbx = shape.find('.//w:txbxContent', NS)
            if txbx is not None:
                frames.append({
                    'pict': pict,
                    'shape': shape,
                    'txbxContent': txbx,
                    'text': get_text_from_element(txbx),
                })
    return frames


def find_text_frames_wps(body):
    """Find DrawingML text frames (wps:txbx with txbxContent) under w:drawing."""
    frames = []
    for drawing in body.findall('.//w:drawing', NS):
        for txbx in drawing.findall('.//wps:txbx', NS):
            txbx_content = txbx.find('w:txbxContent', NS)
            if txbx_content is not None:
                frames.append({
                    'drawing': drawing,
                    'txbx': txbx,
                    'txbxContent': txbx_content,
                    'text': get_text_from_element(txbx_content),
                })
    return frames


def check_double_border_vml(shape):
    """Check if VML shape has a double-line border.
    VML double-line styles: thinThin, thickThin, thinThick, thickBetweenThin."""
    stroked = shape.get('stroked', 'f')
    if stroked != 't':
        return False
    stroke = shape.find('v:stroke', NS)
    if stroke is None:
        return False
    linestyle = stroke.get('linestyle', '')
    double_styles = {'thinThin', 'thickThin', 'thinThick', 'thickBetweenThin'}
    return linestyle in double_styles


def check_double_border_wps(drawing):
    """Check if DrawingML shape has a double-line border (compound line type)."""
    # Look for a:ln with cmpd attribute
    for ln in drawing.findall('.//' + '{' + NS['a'] + '}ln'):
        cmpd = ln.get('cmpd', 'sng')
        if cmpd in ('dbl', 'thickThin', 'thinThick', 'tri'):
            return True
    return False


def check_padding_vml(shape, target_pt=14.17, tolerance_pt=2.0):
    """Check if VML textbox inset is approximately target_pt on all sides."""
    textbox = shape.find('v:textbox', NS)
    if textbox is None:
        return False
    inset = textbox.get('inset', '')
    if not inset:
        return False
    # Parse inset values — can be in pt, in, cm, mm, or bare numbers (default EMU/inches)
    parts = [p.strip() for p in inset.split(',')]
    if len(parts) < 4:
        return False
    for part in parts:
        m = re.match(r'([\d.]+)\s*(pt|in|cm|mm)?', part)
        if not m:
            return False
        val = float(m.group(1))
        unit = m.group(2) or 'in'
        # Convert to pt
        if unit == 'pt':
            pt_val = val
        elif unit == 'in':
            pt_val = val * 72
        elif unit == 'cm':
            pt_val = val * 28.35
        elif unit == 'mm':
            pt_val = val * 2.835
        else:
            pt_val = val
        if abs(pt_val - target_pt) > tolerance_pt:
            return False
    return True


def check_padding_wps(drawing, target_cm=0.5, tolerance_cm=0.1):
    """Check if DrawingML shape bodyPr has ~0.5cm padding on all sides."""
    target_emu = int(target_cm * 360000)  # 1cm = 360000 EMU
    tol_emu = int(tolerance_cm * 360000)
    for bodyPr in drawing.findall('.//' + '{' + NS['a'] + '}bodyPr'):
        for attr in ['lIns', 'tIns', 'rIns', 'bIns']:
            val_str = bodyPr.get(attr)
            if val_str is None:
                return False
            val = int(val_str)
            if abs(val - target_emu) > tol_emu:
                return False
        return True
    return False


def check_page_anchor_vml(pict, shape):
    """Check if VML frame is anchored to the page."""
    # Method 1: w10:wrap anchorx="page"
    for wrap in pict.findall('.//w10:wrap', NS):
        if wrap.get('anchorx') == 'page':
            return True
    # Method 2: style contains mso-position-horizontal-relative:page
    style = shape.get('style', '')
    if 'mso-position-horizontal-relative:page' in style:
        return True
    return False


def check_page_anchor_wps(drawing):
    """Check if DrawingML frame is anchored to the page."""
    # Look for wp:anchor with simplePos or positionH relativeFrom="page"
    for anchor in drawing.findall('.//wp:anchor', NS):
        for posH in anchor.findall('wp:positionH', NS):
            if posH.get('relativeFrom') == 'page':
                return True
    for anchor in drawing.findall('.//wp14:anchor', NS):
        for posH in anchor.findall('wp14:positionH', NS):
            if posH.get('relativeFrom') == 'page':
                return True
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body

    # Find all text frames (both VML and DrawingML approaches)
    vml_frames = find_text_frames_vml(body)
    wps_frames = find_text_frames_wps(body)

    # Key content phrases from the Quick Reference Card section
    key_phrases = [
        "uname -a",
        "ps aux",
        "df -h",
        "journalctl",
        "systemctl",
        "apt update",
    ]

    # Find the frame containing Quick Reference Card content
    qrc_frame = None
    frame_type = None  # 'vml' or 'wps'

    for f in vml_frames:
        text = f['text']
        matches = sum(1 for phrase in key_phrases if phrase in text)
        if matches >= 4:  # At least 4 of 6 key phrases found
            qrc_frame = f
            frame_type = 'vml'
            break

    if qrc_frame is None:
        for f in wps_frames:
            text = f['text']
            matches = sum(1 for phrase in key_phrases if phrase in text)
            if matches >= 4:
                qrc_frame = f
                frame_type = 'wps'
                break

    # Component 1: Text frame exists with Quick Reference Card content (0.35 points)
    try:
        if qrc_frame is not None:
            matched = sum(1 for p in key_phrases if p in qrc_frame['text'])
            print(f"PASS: Component 1 — Text frame found ({frame_type}) with Quick Reference content ({matched}/6 key phrases) (0.35 pts)")
            total_score += 0.35
        else:
            all_frames = len(vml_frames) + len(wps_frames)
            print(f"FAIL: Component 1 — No text frame with Quick Reference Card content found. Total frames: {all_frames}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Components 2-4 only apply if a frame was found
    if qrc_frame is None:
        print("SKIP: Components 2-4 — no qualifying frame found")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Double-line border (0.25 points)
    try:
        if frame_type == 'vml':
            has_double = check_double_border_vml(qrc_frame['shape'])
        else:
            has_double = check_double_border_wps(qrc_frame['drawing'])

        if has_double:
            print(f"PASS: Component 2 — Double-line border detected (0.25 pts)")
            total_score += 0.25
        else:
            if frame_type == 'vml':
                stroke = qrc_frame['shape'].find('v:stroke', NS)
                ls = stroke.get('linestyle', 'none') if stroke is not None else 'no stroke element'
                stroked = qrc_frame['shape'].get('stroked', 'f')
                print(f"FAIL: Component 2 — Expected double-line border, found stroked={stroked}, linestyle={ls}")
            else:
                print(f"FAIL: Component 2 — Double-line border not detected in DrawingML shape")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 0.5 cm padding (0.20 points)
    try:
        if frame_type == 'vml':
            has_padding = check_padding_vml(qrc_frame['shape'], target_pt=14.17, tolerance_pt=2.5)
        else:
            has_padding = check_padding_wps(qrc_frame['drawing'], target_cm=0.5, tolerance_cm=0.1)

        if has_padding:
            print(f"PASS: Component 3 — 0.5 cm padding detected (0.20 pts)")
            total_score += 0.20
        else:
            if frame_type == 'vml':
                textbox = qrc_frame['shape'].find('v:textbox', NS)
                inset = textbox.get('inset', 'not set') if textbox is not None else 'no textbox'
                print(f"FAIL: Component 3 — Expected ~14.17pt padding (0.5cm), found inset={inset}")
            else:
                print(f"FAIL: Component 3 — 0.5cm padding not found in DrawingML bodyPr")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Anchored to page (0.20 points)
    try:
        if frame_type == 'vml':
            anchored = check_page_anchor_vml(qrc_frame['pict'], qrc_frame['shape'])
        else:
            anchored = check_page_anchor_wps(qrc_frame['drawing'])

        if anchored:
            print(f"PASS: Component 4 — Frame anchored to page (0.20 pts)")
            total_score += 0.20
        else:
            if frame_type == 'vml':
                style = qrc_frame['shape'].get('style', '')
                print(f"FAIL: Component 4 — Frame not anchored to page. Style: {style[:120]}")
            else:
                print(f"FAIL: Component 4 — Frame not anchored to page in DrawingML")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
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
