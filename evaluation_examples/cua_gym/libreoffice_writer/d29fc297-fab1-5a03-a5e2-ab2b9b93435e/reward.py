"""
FINAL REWARD SCRIPT - SUCCESS
Task: LibreOffice keeps dropping my image out of place. What’s the precise sequence to insert a 5.00 cm × 3.00 cm frame, anchor it To Character, and park it on the left side of paragraph 10?
Generated: 2025-09-10 19:55:18
Status: success
Model: azure-o3
Total Steps: 9
"""

import os
import zipfile
from lxml import etree
import math

# -------------------------------------------------------------
#  Reward script for verifying the LibreOffice Writer task
#  Task: Insert a 5.00 cm × 3.00 cm frame, anchor it “To Character”,
#        and position it on the left side of paragraph 10.
# -------------------------------------------------------------
#  Scoring rubric (progressive – maximum 1.0):
#    • framePr element present in paragraph 10               0.20
#    • Width ≈ 5 cm (within 10 twips tolerance)              0.25
#    • Height ≈ 3 cm (within 10 twips tolerance)             0.25
#    • xAlign="left"                                         0.15
#    • wrap="around"                                        0.05
#    • anchorLock attribute present (indicates anchoring)    0.10
# -------------------------------------------------------------
#  Total                                                      1.00
# -------------------------------------------------------------

FILE_PATH = "/home/user/libreoffice_keeps_dropping_my_image_out_of_place_whats_the_precise_sequence_to_insert_a_500_cm_300_c.docx"

# Helper: convert centimetres to Word twips (1 inch = 1440 twips, 1 cm = 567 twips)
TWIPS_PER_CM = 1440 / 2.54  # ≈ 567.0
EXPECTED_WIDTH_TWIPS = round(5.0 * TWIPS_PER_CM)   # ≈ 2835 twips
EXPECTED_HEIGHT_TWIPS = round(3.0 * TWIPS_PER_CM)  # ≈ 1701 twips


def verify_frame_attributes(framePr):
    """Return a dict with boolean checks for each required attribute."""
    ns_w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

    def _int_attr(attr_name):
        val = framePr.get(ns_w + attr_name)
        return int(val) if val is not None and val.isdigit() else None

    width_val = _int_attr("w")
    height_val = _int_attr("h")
    x_align = framePr.get(ns_w + "xAlign")
    wrap_val = framePr.get(ns_w + "wrap")
    anchor_lock_val = framePr.get(ns_w + "anchorLock")

    return {
        "width_ok": width_val is not None and abs(width_val - EXPECTED_WIDTH_TWIPS) <= 10,
        "height_ok": height_val is not None and abs(height_val - EXPECTED_HEIGHT_TWIPS) <= 10,
        "left_ok": x_align == "left",
        "wrap_ok": wrap_val == "around",
        "anchor_ok": anchor_lock_val is not None,
        "width_val": width_val,
        "height_val": height_val,
    }


def verify_writer_task(file_path: str) -> float:
    """Main verification routine – returns a float between 0.0 and 1.0."""
    total_score = 0.0

    # ---------- 1. Ensure file and XML are accessible ----------
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0  # cannot proceed

    try:
        with zipfile.ZipFile(file_path) as docx_zip:
            if "word/document.xml" not in docx_zip.namelist():
                print("✗ document.xml missing inside DOCX")
                return 0.0
            document_xml = docx_zip.read("word/document.xml")
    except Exception as e:
        print(f"✗ Error opening DOCX: {e}")
        return 0.0

    # ---------- 2. Parse XML ----------
    try:
        root = etree.fromstring(document_xml)
    except Exception as e:
        print(f"✗ XML parsing failed: {e}")
        return 0.0

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs = root.xpath("//w:body/w:p", namespaces=ns)
    print(f"Found {len(paragraphs)} paragraphs in document")

    # Ensure we have at least 10 paragraphs
    if len(paragraphs) < 10:
        print("✗ Document contains fewer than 10 paragraphs – cannot verify target paragraph.")
        return 0.0

    target_para = paragraphs[9]  # 0-based index, so index 9 is paragraph 10
    para_text = "".join(target_para.xpath(".//w:t/text()", namespaces=ns)).strip()
    print(f"Paragraph 10 text preview: '{para_text[:100]}'")

    # ---------- 3. Look for <w:framePr> ----------
    framePr = target_para.find("w:pPr/w:framePr", namespaces=ns)

    if framePr is None:
        print("✗ No <w:framePr> element found in paragraph 10 – frame not detected.")
        return 0.0  # No frame → zero score

    # Frame exists → add base score
    print("✓ <w:framePr> found in paragraph 10")
    total_score += 0.20

    # ---------- 4. Validate frame attributes ----------
    res = verify_frame_attributes(framePr)

    if res["width_ok"]:
        print(f"✓ Width ≈ 5 cm (twips={res['width_val']})")
        total_score += 0.25
    else:
        print(f"✗ Width incorrect or missing (twips={res['width_val']})")

    if res["height_ok"]:
        print(f"✓ Height ≈ 3 cm (twips={res['height_val']})")
        total_score += 0.25
    else:
        print(f"✗ Height incorrect or missing (twips={res['height_val']})")

    if res["left_ok"]:
        print("✓ xAlign = left (frame parked left)")
        total_score += 0.15
    else:
        print("✗ xAlign not set to left")

    if res["wrap_ok"]:
        print("✓ wrap = around (wrap style correct)")
        total_score += 0.05
    else:
        print("✗ wrap style not set to 'around'")

    if res["anchor_ok"]:
        print("✓ anchorLock attribute present – anchoring info detected")
        total_score += 0.10
    else:
        print("✗ anchorLock attribute missing – anchoring may be incorrect")

    final_score = min(total_score, 1.0)
    print(f"Total score: {final_score}/1.0")
    return final_score


if __name__ == "__main__":
    reward = verify_writer_task(FILE_PATH)
    print(f"REWARD: {reward}")
