"""
Reward Script: Insert image from file with square text wrapping in top-right corner
Task ID: osworld_writer_image_insertion_003
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): Image is inserted into the document (image relationship exists)
  Component 2 (0.35): Image uses Square text wrapping (wp:wrapSquare anchor element)
  Component 3 (0.25): Image is positioned in the upper-right corner of the first page
Total: 1.0
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_image_insertion_003'

# Namespace constants for WordprocessingML Drawing
NS_WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Insert 'banner.jpg' with Square text wrapping, positioned in the
    upper-right corner of the first page.

    Verification strategy:
    - The golden env adds the image as a floating anchor (wp:anchor) with
      wp:wrapSquare wrapping.
    - Position: ~5.7 inches from page-left (right half of 8.5-inch page),
      ~1.0 inch from page-top.
    - The initial env has 0 images, 0 anchors.
    """
    total_score = 0.0

    # Load document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: Image is present in the document (0.40 points)
    # Check that at least one image relationship exists in the document part.
    # Initial env has 0 images; golden env has 1 (banner.jpg).
    # -------------------------------------------------------------------------
    try:
        image_rels = [
            rel for rel in doc.part.rels.values()
            if "image" in rel.reltype
        ]
        # Verify image count: initial has 0, golden has 1
        image_count = len(image_rels)
        banner_found = image_count >= 1 and any(
            'banner' in str(rel.target_ref).lower()
            for rel in image_rels
        )
        if image_count >= 1 and banner_found:
            print(f"PASS: Component 1 — banner.jpg image inserted (found {image_count} image rel(s)) (0.40 pts)")
            total_score += 0.40
        elif image_count >= 1:
            print(f"PASS: Component 1 — image inserted (found {image_count} rel(s), name may vary) (0.40 pts)")
            total_score += 0.40
        else:
            print("FAIL: Component 1 — no image found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Image uses Square text wrapping (0.35 points)
    # A floating image with Square wrap appears as wp:anchor with a
    # wp:wrapSquare child element.  An inline image (wp:inline) has no wrap.
    # -------------------------------------------------------------------------
    try:
        anchors = doc.element.findall('.//{%s}anchor' % NS_WP)
        if len(anchors) >= 1:
            anchor = anchors[0]
            wrap_square_elements = anchor.findall('{%s}wrapSquare' % NS_WP)
            if wrap_square_elements:
                print(f"PASS: Component 2 — Square text wrapping confirmed (wp:wrapSquare present) (0.35 pts)")
                total_score += 0.35
            else:
                # Check what wrapping is actually present
                wrap_children = [child.tag.split('}')[-1] for child in anchor if 'wrap' in child.tag.lower()]
                print(f"FAIL: Component 2 — anchor exists but wrapSquare not found; wrap elements: {wrap_children}")
        else:
            # Check if inline image exists (wrong wrapping type)
            inlines = doc.element.findall('.//{%s}inline' % NS_WP)
            if inlines:
                print("FAIL: Component 2 — image is inline (no text wrap), expected Square wrap anchor")
            else:
                print("FAIL: Component 2 — no anchor or inline drawing element found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Image positioned in the upper-right corner of the first page
    # (0.25 points)
    # Golden env: posH = 5212080 EMU (~5.7 inches from page-left on 8.5-inch page),
    #             posV = 914400 EMU (~1.0 inch from page-top).
    # Criteria:
    #   - Horizontal: in the right half of the page (posH > page_width / 2)
    #   - Vertical: within the upper portion (posV <= 2 * 914400 = 1828800 EMU ~2 inches)
    # -------------------------------------------------------------------------
    try:
        anchors = doc.element.findall('.//{%s}anchor' % NS_WP)
        if len(anchors) >= 1:
            anchor = anchors[0]

            # Get page width for reference
            section = doc.sections[0]
            page_width = section.page_width  # EMU

            # Read horizontal position (relative to page)
            pos_h_elem = anchor.find('{%s}positionH' % NS_WP)
            pos_v_elem = anchor.find('{%s}positionV' % NS_WP)

            pos_h_ok = False
            pos_v_ok = False

            if pos_h_elem is not None:
                pos_offset_h = pos_h_elem.find('{%s}posOffset' % NS_WP)
                if pos_offset_h is not None and pos_offset_h.text:
                    h_emu = int(pos_offset_h.text)
                    # Right half of page: h > page_width / 2
                    pos_h_ok = (h_emu > page_width / 2)
                    print(f"  posH = {h_emu} EMU ({h_emu/914400:.2f} in), page_width/2 = {page_width//2} EMU => right_half={pos_h_ok}")

            if pos_v_elem is not None:
                pos_offset_v = pos_v_elem.find('{%s}posOffset' % NS_WP)
                if pos_offset_v is not None and pos_offset_v.text:
                    v_emu = int(pos_offset_v.text)
                    # Upper portion: within 2 inches from top (2 * 914400 = 1828800 EMU)
                    pos_v_ok = (v_emu <= 1828800)
                    print(f"  posV = {v_emu} EMU ({v_emu/914400:.2f} in), threshold=1828800 EMU => upper={pos_v_ok}")

            if pos_h_ok and pos_v_ok:
                print("PASS: Component 3 — image positioned in upper-right corner (0.25 pts)")
                total_score += 0.25
            elif pos_h_ok:
                print("FAIL: Component 3 — image is right-aligned but NOT in upper portion")
            elif pos_v_ok:
                print("FAIL: Component 3 — image is in upper portion but NOT right-aligned")
            else:
                print("FAIL: Component 3 — image is NOT in upper-right corner")
        else:
            print("FAIL: Component 3 — no anchor element found (cannot check position)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
