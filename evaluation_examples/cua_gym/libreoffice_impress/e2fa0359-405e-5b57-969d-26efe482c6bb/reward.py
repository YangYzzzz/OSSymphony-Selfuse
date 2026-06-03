"""
FINAL REWARD SCRIPT - SUCCESS
Task: Insert the document title field in the header, right-aligned.
Generated: 2025-10-17 09:00:02
Status: success
Model: azure-o3
Total Steps: 18
"""

import os
import zipfile
import lxml.etree as ET


def verify_document_title_header_right_aligned(file_path: str) -> float:
    """Verify that the presentation contains the document-title field in the header, right-aligned.

    Progressive scoring (max 1.0):
        • 0.4  – A document-title field (a:fld type="title") exists in any slide or slide master
        • 0.3  – That field is positioned within the header zone (top 25 % of slide height)
        • 0.3  – That field is right-aligned, determined by either paragraph alignment (algn="r")
                 or the shape’s right edge lying in the rightmost 15 % of the slide width
    """
    print(f"Checking presentation: {file_path}")

    # ---------- Preliminary checks ----------
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0
    if not file_path.lower().endswith(".pptx"):
        print("✗ Unsupported file type (only .pptx allowed)")
        return 0.0

    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    }

    try:
        with zipfile.ZipFile(file_path, "r") as pptx_zip:
            # ---------- Get slide size (EMU) ----------
            try:
                pres_root = ET.fromstring(pptx_zip.read("ppt/presentation.xml"))
                sld_sz = pres_root.find("p:sldSz", namespaces=ns)
                slide_cx = int(sld_sz.get("cx")) if sld_sz is not None else 9144000  # 10 in
                slide_cy = int(sld_sz.get("cy")) if sld_sz is not None else 6858000  # 7.5 in
            except Exception as e:
                print(f"! Could not read slide size ({e}); using defaults")
                slide_cx, slide_cy = 9144000, 6858000
            print(f"Slide size: cx={slide_cx}, cy={slide_cy}")

            # ---------- Search relevant XML parts ----------
            xml_parts = [name for name in pptx_zip.namelist()
                         if name.endswith(".xml") and
                         (name.startswith("ppt/slides/") or name.startswith("ppt/slideMasters/"))]

            field_found = False          # Any title-field at all?
            header_ok = False            # Field sits in header zone?
            right_ok = False             # Field right-aligned?

            for part in xml_parts:
                root = ET.fromstring(pptx_zip.read(part))

                for sp in root.xpath(".//p:sp", namespaces=ns):
                    if not sp.xpath(".//a:fld[@type='title']", namespaces=ns):
                        continue  # this shape does not contain a title field

                    field_found = True
                    print(f"✓ Found title field in {part}")

                    # ---- Shape position ----
                    x = y = cx = None
                    sp_pr = sp.find("p:spPr", namespaces=ns)
                    if sp_pr is not None:
                        xfrm = sp_pr.find("a:xfrm", namespaces=ns)
                        if xfrm is not None:
                            off = xfrm.find("a:off", namespaces=ns)
                            ext = xfrm.find("a:ext", namespaces=ns)
                            if off is not None:
                                x = int(off.get("x"))
                                y = int(off.get("y"))
                            if ext is not None:
                                cx = int(ext.get("cx"))

                    # ---- Header test (top 25 % of slide height) ----
                    if y is not None and y < slide_cy * 0.25:
                        header_ok = True
                        print(f"  ✓ Field is inside header zone (y={y})")

                    # ---- Right-alignment tests ----
                    paragraph_right = any(
                        p_pr is not None and p_pr.get("algn") == "r"
                        for p_pr in (p.find("a:pPr", namespaces=ns) for p in sp.xpath(".//a:p", namespaces=ns))
                    )

                    positional_right = (
                        x is not None and cx is not None and
                        (x + cx) > slide_cx * 0.85  # shape’s right edge in last 15 %
                    )

                    if paragraph_right or positional_right:
                        right_ok = True
                        print(
                            f"  ✓ Field considered right-aligned (paragraph={paragraph_right}, position={positional_right})"
                        )

                # Early exit if all criteria are met
                if field_found and header_ok and right_ok:
                    break

            # ---------- Scoring ----------
            score = 0.0
            if field_found:
                score += 0.4
            if field_found and header_ok:
                score += 0.3
            if field_found and right_ok:
                score += 0.3

            final_score = min(score, 1.0)
            print(f"Scoring — field: {field_found}, header: {header_ok}, right: {right_ok}")
            print(f"REWARD: {final_score}")
            return final_score

    except Exception as e:
        print(f"✗ Error while verifying presentation: {e}")
        return 0.0


if __name__ == "__main__":
    # Default path for manual execution inside the VM
    default_path = "/home/user/insert_the_document_title_field_in_the_header_right_aligned.pptx"
    verify_document_title_header_right_aligned(default_path)

