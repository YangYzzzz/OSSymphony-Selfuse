"""
FINAL REWARD SCRIPT - SUCCESS
Task: The photo I dropped into my Writer document is crowding the text. Can you walk me through setting it to Page Wrap and adding a precise 0.30 cm buffer on every side so the words don’t stick to the image?
Generated: 2025-09-10 18:55:20
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import zipfile
from lxml import etree

"""
Reward Script: Verify that an image in the provided Writer/Word document
is set to “Page Wrap” (square-type wrap) and that all four distance
margins (buffer) around the picture are precisely 0.30 cm (≈108 000 EMU).
The script awards partial credit for:
  • locating at least one image (0.2)
  • confirming a valid wrap mode (0.3)
  • confirming the 0.30 cm buffer on every side (0.5)
Only when ALL checks pass will the total reach 1.0.
"""

def verify_writer_page_wrap_buffer(file_path: str) -> float:
    """Return a progressive score (0–1) based on verification results."""

    print(f"Verifying page-wrap and buffer settings in: {file_path}\n")
    score = 0.0
    MAX_SCORE = 1.0

    # ------------------------------------------------------------------
    # 1. Basic file existence check (NO points – prerequisite) ---------
    # ------------------------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File not found\n")
        return 0.0

    # ------------------------------------------------------------------
    # 2. Read document.xml from the DOCX/ODT container -----------------
    # ------------------------------------------------------------------
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            doc_xml = z.read("word/document.xml")  # LibreOffice saves DOCX
    except Exception as exc:
        print(f"✗ Unable to open or read document.xml: {exc}\n")
        return 0.0

    # ------------------------------------------------------------------
    # 3. Parse the XML --------------------------------------------------
    # ------------------------------------------------------------------
    try:
        root = etree.fromstring(doc_xml)
    except Exception as exc:
        print(f"✗ XML parsing error: {exc}\n")
        return 0.0

    ns = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    }

    # ------------------------------------------------------------------
    # 4. Locate drawing elements (images) ------------------------------
    # ------------------------------------------------------------------
    drawings = root.xpath(".//wp:anchor | .//wp:inline", namespaces=ns)
    if not drawings:
        print("✗ No images (drawing elements) found in the document\n")
        return 0.0

    print(f"✓ Found {len(drawings)} image drawing element(s)\n")
    score += 0.2  # Image presence confirms the user inserted a photo

    # ------------------------------------------------------------------
    # 5. Define target buffer distance (0.30 cm) in EMUs ---------------
    #    1 inch = 2.54 cm, 1 inch = 914 400 EMU
    #    0.30 cm  ⇒  0.30 / 2.54 * 914400 ≈ 108000 EMU
    # ------------------------------------------------------------------
    TARGET = 108000       # Desired buffer in EMU
    TOLERANCE = 15000    # ±15 000 EMU ≈ ±0.042 cm

    def within(val: int) -> bool:
        """Return True if *val* is within tolerance of TARGET."""
        return abs(val - TARGET) <= TOLERANCE

    wrap_ok = False
    buffer_ok = False

    # ------------------------------------------------------------------
    # 6. Inspect each drawing for wrap type and buffer distances --------
    # ------------------------------------------------------------------
    for idx, drawing in enumerate(drawings, 1):
        print(f"Analyzing image {idx} …")

        # 6a. Check wrap element ------------------------------------------------
        wrap_child = None
        for child in drawing:
            local = etree.QName(child.tag).localname
            if local.startswith("wrap"):
                wrap_child = child
                break

        if wrap_child is not None:
            wrap_type = etree.QName(wrap_child.tag).localname
            print(f"  ✓ Wrap element detected: {wrap_type}")
            # LibreOffice uses wrapSquare for “Page Wrap”
            if wrap_type in {"wrapSquare", "wrapTight", "wrapThrough", "wrapPolygon"}:
                wrap_ok = True
        else:
            print("  ✗ No wrap element found (image may be inline or wrapNone)")

        # 6b. Determine buffer distances ---------------------------------------
        # First preference: dist* attributes on the anchor element
        dist_values = {}
        for attr in ("distT", "distB", "distL", "distR"):
            raw = drawing.get(attr)
            if raw is not None:
                try:
                    dist_values[attr] = int(raw)
                except ValueError:
                    pass

        if len(dist_values) == 4:
            print(f"  Found anchor distance attributes: {dist_values}")
            if all(within(v) for v in dist_values.values()):
                buffer_ok = True
                print("  ✓ Buffer distances via anchor attributes are correct (0.30 cm)")
        else:
            # Fallback: wp:effectExtent element
            eff = drawing.find("wp:effectExtent", namespaces=ns)
            if eff is not None:
                try:
                    eff_vals = {k: int(eff.get(k)) for k in ("l", "r", "t", "b")}
                    print(f"  Found effectExtent values: {eff_vals}")
                    if all(within(v) for v in eff_vals.values()):
                        buffer_ok = True
                        print("  ✓ Buffer distances via effectExtent are correct (0.30 cm)")
                except Exception as exc:
                    print(f"  ✗ Error reading effectExtent values: {exc}")
            else:
                print("  ✗ No buffer attributes (dist* or effectExtent) found")

        if wrap_ok and buffer_ok:
            print("  → This image satisfies BOTH wrap and buffer requirements\n")
        else:
            print("  → Partial compliance for this image (wrap_ok: {wrap_ok}, buffer_ok: {buffer_ok})\n")

    # ------------------------------------------------------------------
    # 7. Accumulate scores ---------------------------------------------
    # ------------------------------------------------------------------
    if wrap_ok:
        score += 0.3
        print("✓ Wrap requirement satisfied (+0.3)")
    else:
        print("✗ Wrap requirement NOT satisfied")

    if buffer_ok:
        score += 0.5
        print("✓ Buffer requirement satisfied (+0.5)")
    else:
        print("✗ Buffer requirement NOT satisfied")

    # ------------------------------------------------------------------
    final_score = min(score, MAX_SCORE)
    print(f"\nFINAL SCORE: {final_score}")
    print(f"REWARD: {final_score}\n")
    return final_score


if __name__ == "__main__":
    # Path to the (golden) document used for automated verification
    FILE_PATH = "/home/user/the_photo_i_dropped_into_my_writer_document_is_crowding_the_text_can_you_walk_me_through_setting_it_.docx"
    verify_writer_page_wrap_buffer(FILE_PATH)

