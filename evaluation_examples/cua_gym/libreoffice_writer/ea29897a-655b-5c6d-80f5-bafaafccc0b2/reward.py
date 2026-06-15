"""
FINAL REWARD SCRIPT - SUCCESS
Task: I want to drop the file "Desktop/1.png" right into the body of my Writer document so it behaves like a letter or number in the sentence—so, anchor it As Character—and the picture has to display at exactly 7.50 cm wide with the aspect ratio locked. How do I do that?
Generated: 2025-09-10 16:35:17
Status: success
Model: azure-o3
Total Steps: 7
"""

import os
import zipfile
from lxml import etree


def verify_writer_inline_image(file_path: str,
                               target_width_cm: float = 7.5,
                               tolerance_cm: float = 0.05) -> float:
    """Reward-script verification for the Writer task:

    Requirements to obtain full credit (1.0):
      1. An image is anchored *As Character* (appears as <wp:inline>) – 0.4 pts
      2. That inline image’s width equals 7.50 cm ± 0.05 cm – 0.4 pts
      3. Aspect ratio is locked (noChangeAspect="1") – 0.2 pts

    Progressive scoring is applied; partial completion earns partial credit.
    """

    print(f"Checking document: {file_path}")
    max_score = 1.0
    score = 0.0

    # --- Preliminary: ensure file exists -------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File does not exist – task failed")
        print(f"REWARD: {score}")
        return score

    # --- Extract document.xml from DOCX --------------------------------------------------
    try:
        with zipfile.ZipFile(file_path, 'r') as docx_zip:
            if 'word/document.xml' not in docx_zip.namelist():
                print("✗ word/document.xml not found – invalid DOCX")
                print(f"REWARD: {score}")
                return score
            document_xml = docx_zip.read('word/document.xml')
    except Exception as e:
        print(f"✗ Error opening DOCX: {e}")
        print(f"REWARD: {score}")
        return score

    # --- Parse XML -----------------------------------------------------------------------
    try:
        root = etree.fromstring(document_xml)
    except Exception as e:
        print(f"✗ Error parsing XML: {e}")
        print(f"REWARD: {score}")
        return score

    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    }

    # --- Requirement 1: inline-anchored image (As Character) ------------------------------
    inlines = root.findall('.//wp:inline', namespaces=ns)
    anchors = root.findall('.//wp:anchor', namespaces=ns)
    print(f"Found {len(inlines)} <wp:inline> and {len(anchors)} <wp:anchor> elements")

    if inlines:
        score += 0.4
        print("✓ Inline-anchored image detected (0.4 pts)")
    else:
        print("✗ No inline-anchored images – cannot satisfy task")
        print(f"REWARD: {score}")
        return score  # width/aspect checks meaningless without inline image

    # --- Requirements 2 & 3: width and aspect-ratio lock ---------------------------------
    width_ok = False
    aspect_ok = False

    for inline in inlines:
        # Width check via <wp:extent cx="…"> where 1 cm = 360 000 EMU
        extent = inline.find('wp:extent', namespaces=ns)
        if extent is not None and extent.get('cx'):
            try:
                cx = int(extent.get('cx'))  # EMU units
                width_cm = cx / 360000.0
                print(f"  • Detected width: {width_cm:.2f} cm")
                if abs(width_cm - target_width_cm) <= tolerance_cm:
                    width_ok = True
                    print("    ✓ Width matches target")
                else:
                    print("    ✗ Width outside tolerance")
            except ValueError:
                print("    ✗ Non-integer width value – skipped")
        else:
            print("    ✗ <wp:extent> missing – width unknown")

        # Aspect lock check via <a:graphicFrameLocks noChangeAspect="1"/>
        gfl = inline.find('.//a:graphicFrameLocks', namespaces=ns)
        if gfl is not None and gfl.get('noChangeAspect') in {"1", "true", "True", "yes"}:
            aspect_ok = True
            print("    ✓ Aspect-ratio lock detected")
        else:
            print("    ✗ Aspect-ratio lock not set for this image")

        # Early exit if both conditions satisfied
        if width_ok and aspect_ok:
            break

    # --- Scoring -------------------------------------------------------------------------
    if width_ok:
        score += 0.4
    else:
        print("✗ No inline image with correct width found")

    if aspect_ok:
        score += 0.2
    else:
        print("✗ No inline image with aspect ratio locked found")

    final_score = min(score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    # Golden-answer path in VM
    DOC_PATH = "/home/user/i_want_to_drop_the_file_desktop1png_right_into_the_body_of_my_writer_document_so_it_behaves_like_a_l.docx"
    verify_writer_inline_image(DOC_PATH)
