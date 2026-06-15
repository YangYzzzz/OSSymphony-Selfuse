"""
Reward Script: Set up document with watermark/background image
Task ID: writer_rd_090
Domain: libreoffice_writer
Scoring:
  Component 1: Image embedded in header (0.3 pts)
  Component 2: Image anchored behind text - behindDoc=1 (0.3 pts)
  Component 3: Image has transparency/alpha modification (0.25 pts)
  Component 4: Image positioned relative to page (0.15 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_090'


def persist_app_state(domain):
    """Try to save any unsaved LibreOffice changes."""
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
    Verify that the document has a watermark/background image.
    Checks for image in header with behindDoc, transparency, and page positioning.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.oxml.ns import qn
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # We need to check multiple possible watermark implementations:
    # 1. Image in header with anchor behind text (the golden approach)
    # 2. w:background element at document level
    # 3. Image anchored in body behind text

    header_has_image = False
    body_has_bg_image = False
    doc_has_background = False
    anchor_behind_doc = False
    has_transparency = False
    positioned_on_page = False

    # Check for w:background at document level
    doc_bg = doc.element.findall(qn('w:background'))
    if len(doc_bg) > 0:
        doc_has_background = True

    # Check header for images
    for section in doc.sections:
        hdr = section.header
        if hdr is None:
            continue

        # Check for blip (embedded image) in header
        blips = list(hdr._element.iter(qn('a:blip')))
        if blips:
            header_has_image = True

        # Check for anchor with behindDoc in header
        for anchor in hdr._element.iter(qn('wp:anchor')):
            behind = anchor.get('behindDoc', '0')
            if behind == '1':
                anchor_behind_doc = True

            # Check positioning relative to page
            for pos_h in anchor.iter(qn('wp:positionH')):
                rel_from = pos_h.get('relativeFrom', '')
                if rel_from in ('page', 'margin', 'column'):
                    positioned_on_page = True
            for pos_v in anchor.iter(qn('wp:positionV')):
                rel_from = pos_v.get('relativeFrom', '')
                if rel_from in ('page', 'margin', 'paragraph'):
                    positioned_on_page = True

        # Check for transparency on blips in header
        for blip in hdr._element.iter(qn('a:blip')):
            for child in blip:
                if 'alphaModFix' in child.tag:
                    amt = child.get('amt', '100000')
                    # amt < 100000 means some transparency applied
                    if int(amt) < 100000:
                        has_transparency = True
                        print(f"  INFO: alphaModFix amt={amt} (transparency: {100 - int(amt)/1000:.0f}%)")

    # Also check body paragraphs for background images (alternative approach)
    for para in doc.paragraphs:
        for anchor in para._element.iter(qn('wp:anchor')):
            behind = anchor.get('behindDoc', '0')
            if behind == '1':
                # Check if this anchor has an image
                blips = list(anchor.iter(qn('a:blip')))
                if blips:
                    body_has_bg_image = True
                    anchor_behind_doc = True
                    # Check positioning
                    for pos_h in anchor.iter(qn('wp:positionH')):
                        rel_from = pos_h.get('relativeFrom', '')
                        if rel_from in ('page', 'margin', 'column'):
                            positioned_on_page = True
                    for pos_v in anchor.iter(qn('wp:positionV')):
                        rel_from = pos_v.get('relativeFrom', '')
                        if rel_from in ('page', 'margin', 'paragraph'):
                            positioned_on_page = True
                    # Check transparency
                    for blip in anchor.iter(qn('a:blip')):
                        for child in blip:
                            if 'alphaModFix' in child.tag:
                                amt = child.get('amt', '100000')
                                if int(amt) < 100000:
                                    has_transparency = True

    # Also check for VML-based watermarks (Word watermark feature uses VML shapes)
    import zipfile
    import io
    vml_watermark = False
    try:
        with open(file_path, 'rb') as f:
            zf = zipfile.ZipFile(io.BytesIO(f.read()))
        # Check header XML files for VML shapes
        for name in zf.namelist():
            if 'header' in name.lower() and name.endswith('.xml'):
                content = zf.read(name).decode('utf-8', errors='ignore')
                if 'imagedata' in content.lower() or 'blip' in content.lower():
                    header_has_image = True
                if 'behindDoc' in content or 'behind' in content.lower():
                    anchor_behind_doc = True
    except Exception as e:
        print(f"  WARN: Could not check zip: {e}")

    has_any_image = header_has_image or body_has_bg_image or doc_has_background

    # Also verify the watermark image file exists (precondition gate)
    watermark_path = os.path.join(WORKDIR, 'watermark_logo.png')
    if not os.path.exists(watermark_path):
        print("WARN: watermark_logo.png not found, but continuing verification")

    # Check media files in zip to confirm image is embedded
    image_embedded = False
    try:
        with open(file_path, 'rb') as f:
            zf = zipfile.ZipFile(io.BytesIO(f.read()))
        media_files = [n for n in zf.namelist() if n.startswith('word/media/')]
        if media_files:
            image_embedded = True
            print(f"  INFO: Found {len(media_files)} media file(s): {media_files}")
    except Exception as e:
        print(f"  WARN: Could not check media files: {e}")

    # Component 1: Image is embedded in the document (header or body) (0.3 points)
    # This fails on initial (no images) and passes on golden (image in header)
    try:
        if has_any_image and image_embedded:
            print(f"PASS: Component 1 - Image embedded in document (header={header_has_image}, body_bg={body_has_bg_image}, doc_bg={doc_has_background}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - No image found in document (header={header_has_image}, body_bg={body_has_bg_image}, doc_bg={doc_has_background}, embedded={image_embedded})")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Image is anchored behind text (behindDoc=1) acting as watermark (0.3 points)
    # This fails on initial (no anchors) and passes on golden (behindDoc=1)
    try:
        if anchor_behind_doc:
            print(f"PASS: Component 2 - Image anchored behind text (behindDoc=1) (0.3 pts)")
            total_score += 0.3
        elif doc_has_background:
            # w:background is also a valid way to have background image
            print(f"PASS: Component 2 - Document-level background element found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 - No behind-text anchor or background element found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Image has transparency making it faint (0.25 points)
    # This fails on initial (no image) and passes on golden (alphaModFix)
    try:
        if has_transparency:
            print(f"PASS: Component 3 - Image has transparency (alphaModFix applied) (0.25 pts)")
            total_score += 0.25
        elif doc_has_background:
            # w:background approach may handle faintness differently
            print(f"PARTIAL: Component 3 - Background element found, assuming faintness handled (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - No transparency/alpha modification detected")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Image positioned relative to page (0.15 points)
    # This fails on initial (no positioning) and passes on golden (relativeFrom=page)
    try:
        if positioned_on_page:
            print(f"PASS: Component 4 - Image positioned relative to page (0.15 pts)")
            total_score += 0.15
        elif doc_has_background or has_any_image:
            # If there is a background image by any method, give partial for positioning
            print(f"PARTIAL: Component 4 - Image exists but positioning not explicitly page-relative (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 - No page-relative positioning found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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
