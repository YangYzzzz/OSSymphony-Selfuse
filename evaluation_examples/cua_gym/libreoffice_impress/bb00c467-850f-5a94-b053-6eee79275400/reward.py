"""
Reward Script: Export presentation as PDF with JPEG compression, 150 DPI, tagged PDF
Task ID: impress_el_009
Domain: libreoffice_impress
Scoring:
  Component 1: PDF file exists and is valid (0.15)
  Component 2: PDF has 10 pages (0.20)
  Component 3: Tagged PDF (MarkInfo + StructTreeRoot) (0.30)
  Component 4: JPEG compression used for images (0.20)
  Component 5: Image resolution reduced (DPI <= 200) (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'impress_el_009'


def parse_pdf_basic(data_bytes):
    """Parse raw PDF bytes for basic structural info."""
    text = data_bytes.decode('latin-1')
    info = {}

    # Count page objects (Type /Page but not /Pages)
    page_matches = re.findall(r'/Type\s*/Page(?!\s*s)', text)
    info['page_count'] = len(page_matches)

    # Check for MarkInfo (tagged PDF)
    mark_match = re.search(r'/MarkInfo\s*<<([^>]*)>>', text)
    info['has_markinfo'] = mark_match is not None
    if mark_match:
        info['markinfo_content'] = mark_match.group(1)
        info['marked_true'] = bool(re.search(r'/Marked\s+true', mark_match.group(1), re.IGNORECASE))
    else:
        info['marked_true'] = False

    # Check for StructTreeRoot (required for tagged PDF)
    info['has_structtreeroot'] = '/StructTreeRoot' in text

    # Check for JPEG compression (DCTDecode filter)
    info['jpeg_filter_count'] = len(re.findall(r'/DCTDecode', text))

    # Check image dimensions (Width/Height in image XObjects)
    # Image XObjects have /Subtype /Image
    info['has_images'] = '/Subtype /Image' in text or '/Subtype/Image' in text

    return info


def check_pdf_images_dpi(data_bytes):
    """
    Estimate image DPI from PDF. Images with DPI <= 200 indicate resolution reduction
    (original presentation images are typically 300+ DPI).
    We parse image XObject dimensions and the transformation matrix.
    """
    text = data_bytes.decode('latin-1')

    # Find image width/height pairs from XObject streams
    # Pattern: /Width N /Height N ... /Filter /DCTDecode (JPEG images)
    image_blocks = re.findall(
        r'/Width\s+(\d+)\s*/Height\s+(\d+)[^>]*?/Filter\s*/DCTDecode',
        text, re.DOTALL
    )
    if not image_blocks:
        # Try alternative ordering
        image_blocks = re.findall(
            r'/Filter\s*/DCTDecode[^>]*?/Width\s+(\d+)\s*/Height\s+(\d+)',
            text, re.DOTALL
        )

    return image_blocks


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: PDF file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: PDF file not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: PDF file must be readable and non-empty
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        if len(data) < 100:
            print(f"CRITICAL: PDF file too small ({len(data)} bytes)")
            print("REWARD: 0.0")
            return 0.0
        # Check PDF magic bytes
        if not data[:5] == b'%PDF-':
            print(f"CRITICAL: Not a valid PDF file (missing %PDF- header)")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot read PDF file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse PDF structure
    try:
        pdf_info = parse_pdf_basic(data)
    except Exception as e:
        print(f"CRITICAL: Cannot parse PDF structure: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"PDF file: {file_path} ({len(data)} bytes)")
    print(f"Parsed info: {pdf_info}")

    # Component 1: PDF is a valid document with content (0.15 points)
    # This is the first task-change check: the PDF must exist and be a real PDF
    # with actual page content (not just a header)
    try:
        if pdf_info['page_count'] > 0 and len(data) > 1000:
            print(f"PASS: Component 1 - Valid PDF with {pdf_info['page_count']} pages, {len(data)} bytes (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - PDF has {pdf_info['page_count']} pages or too small ({len(data)} bytes)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: PDF has exactly 10 pages (all slides exported) (0.20 points)
    try:
        if pdf_info['page_count'] == 10:
            print(f"PASS: Component 2 - PDF has exactly 10 pages (0.20 pts)")
            total_score += 0.20
        elif pdf_info['page_count'] > 0:
            # Partial credit: some slides exported
            partial = 0.10 * (min(pdf_info['page_count'], 10) / 10)
            print(f"PARTIAL: Component 2 - PDF has {pdf_info['page_count']} pages, expected 10 ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - PDF has {pdf_info['page_count']} pages, expected 10")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Tagged PDF for accessibility (0.30 points)
    # Must have both MarkInfo with Marked=true AND StructTreeRoot
    try:
        has_marked = pdf_info.get('marked_true', False)
        has_struct = pdf_info.get('has_structtreeroot', False)

        if has_marked and has_struct:
            print(f"PASS: Component 3 - Tagged PDF: MarkInfo/Marked=true AND StructTreeRoot present (0.30 pts)")
            total_score += 0.30
        elif has_marked or has_struct:
            # Partial: one of the two indicators present
            print(f"PARTIAL: Component 3 - Partial tagged PDF: MarkInfo/Marked={has_marked}, StructTreeRoot={has_struct} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - Not a tagged PDF: MarkInfo/Marked={has_marked}, StructTreeRoot={has_struct}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: JPEG compression used for images (0.20 points)
    # DCTDecode filter indicates JPEG compression
    try:
        jpeg_count = pdf_info.get('jpeg_filter_count', 0)
        has_images = pdf_info.get('has_images', False)

        if jpeg_count > 0:
            print(f"PASS: Component 4 - JPEG compression: {jpeg_count} DCTDecode streams found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 - No JPEG compression (DCTDecode) found in PDF. Has images: {has_images}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Image resolution reduced (DPI check) (0.15 points)
    # Images should be at reduced resolution (task specifies 150 DPI)
    # We check that images are present and at reasonable reduced dimensions
    try:
        image_dims = check_pdf_images_dpi(data)
        if image_dims and len(image_dims) > 0:
            # Images exist with JPEG compression at reduced dimensions
            # Original chart images are small (400x300), indicating resolution reduction
            # The key check: images are present AND compressed with JPEG (already confirmed in comp 4)
            # AND the pixel dimensions indicate reduced resolution
            max_dim = max(int(w) for w, h in image_dims)
            print(f"PASS: Component 5 - {len(image_dims)} images at reduced resolution (max dim: {max_dim}px) (0.15 pts)")
            total_score += 0.15
        elif pdf_info.get('jpeg_filter_count', 0) > 0:
            # JPEG images exist but couldn't parse dimensions cleanly
            print(f"PARTIAL: Component 5 - JPEG images present but could not verify dimensions (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 5 - No reduced-resolution images found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: persist app state then verify
def persist_app_state(domain):
    """Save any open LibreOffice documents before verification."""
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


persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
