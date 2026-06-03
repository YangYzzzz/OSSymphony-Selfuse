"""
FINAL REWARD SCRIPT - SUCCESS
Task: Insert the document title field in the header, right-aligned.
Generated: 2025-10-17 12:05:13
Status: success
Model: azure-o3
Total Steps: 9
"""

import os
import zipfile
from lxml import etree as ET


def verify_document_title_header(file_path: str) -> float:
    """Verify that the presentation contains a *document title* field that
    is positioned in the header area and right-aligned.

    Scoring (progressive):
      • 0.5 – document-title field exists anywhere in the file
      • +0.3 – the paragraph containing the field is right-aligned **or** the
        shape is physically located on the right side of the slide
      • +0.2 – the shape sits in the *header region* (top 25 % of the slide)
      = 1.0 – perfect score when all three conditions are satisfied
    """
    print(f"Verifying file: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File does not exist")
        return 0.0

    try:
        with zipfile.ZipFile(file_path) as pptx_zip:
            ns = {
                "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
                "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
            }

            # Get slide size (used for spatial heuristics)
            pres_xml = ET.fromstring(pptx_zip.read("ppt/presentation.xml"))
            sldSz = pres_xml.find(".//p:sldSz", ns)
            width = int(sldSz.get("cx")) if sldSz is not None else None
            height = int(sldSz.get("cy")) if sldSz is not None else None
            print(f"Slide dimensions: width={width}, height={height}")

            # -----------------------------------------------------------------
            # 1) Search all XML parts for <a:fld type="title"> elements
            # -----------------------------------------------------------------
            xml_parts = [n for n in pptx_zip.namelist() if n.startswith("ppt/") and n.endswith(".xml")]
            title_fields = []  # list of tuples (xml_part_name, fld_element)

            for part in xml_parts:
                try:
                    root = ET.fromstring(pptx_zip.read(part))
                except ET.XMLSyntaxError:
                    # Skip parts that aren't valid XML (rare but safe-guard)
                    continue

                for fld in root.findall(".//a:fld", ns):
                    if fld.get("type") == "title":
                        title_fields.append((part, fld))

            if not title_fields:
                print("✗ No document title field found")
                return 0.0

            print(f"✓ Found {len(title_fields)} document title field instance(s)")
            score = 0.5  # field presence earns 0.5

            # -----------------------------------------------------------------
            # 2) Check alignment + position heuristics for each field found
            # -----------------------------------------------------------------
            right_aligned_found = False
            header_region_found = False

            for part_name, fld in title_fields:
                # Locate the paragraph (<a:p>) that contains the field
                node = fld
                para = None
                while node is not None:
                    if node.tag == "{" + ns["a"] + "}p":
                        para = node
                        break
                    node = node.getparent()

                # A) Text alignment attribute on the paragraph
                if para is not None:
                    pPr = para.find("./a:pPr", ns)
                    if pPr is not None and pPr.get("algn") == "r":
                        right_aligned_found = True
                        print(f"✓ Paragraph alignment right in {part_name}")

                # Ascend further to the shape (<p:sp>) to analyse geometry
                shape = para
                while shape is not None and not shape.tag.endswith("}sp"):
                    shape = shape.getparent()

                if shape is not None and width and height:
                    off = shape.find(".//a:off", ns)
                    ext = shape.find(".//a:ext", ns)
                    if off is not None and ext is not None:
                        x = int(off.get("x"))
                        y = int(off.get("y"))
                        cx = int(ext.get("cx"))
                        cy = int(ext.get("cy"))

                        right_edge = x + cx
                        center_x = x + cx / 2

                        # Heuristic for *right side* positioning
                        if center_x > 0.70 * width or right_edge > 0.90 * width:
                            right_aligned_found = True

                        # Header area = top 25 % of slide
                        if y < 0.25 * height:
                            header_region_found = True

            # Scoring for alignment and header positioning
            if right_aligned_found:
                print("✓ Title field appears right-aligned (visually or via attribute)")
                score += 0.3
            else:
                print("✗ Title field not right-aligned")

            if header_region_found:
                print("✓ Title field located in header region (top of slide)")
                score += 0.2
            else:
                print("✗ Title field not in header region")

            final_score = min(score, 1.0)
            print(f"Final score: {final_score}")
            return final_score

    except Exception as e:
        print(f"✗ Error verifying PPTX: {e}")
        return 0.0


def main():
    target_file = "/home/user/insert_the_document_title_field_in_the_header_right_aligned.pptx"
    reward = verify_document_title_header(target_file)
    print(f"REWARD: {reward}")


if __name__ == "__main__":
    main()

