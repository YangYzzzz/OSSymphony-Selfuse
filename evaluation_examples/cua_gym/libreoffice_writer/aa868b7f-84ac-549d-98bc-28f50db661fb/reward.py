"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Writer my chapter titles (they’re all set to the built-in “Heading 1” style) blend into the body text too much. I’d like a subtle divider: one straight 0.5 pt bottom border on every Heading 1, and nothing on the other sides. How can I tweak the Heading 1 style so that single 0.50 pt line shows up automatically under each top-level heading?
Generated: 2025-09-10 18:31:51
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
import zipfile
import traceback
from docx import Document
from lxml import etree as ET

def verify_heading1_bottom_border(docx_path="/home/user/in_libreoffice_writer_my_chapter_titles_theyre_all_set_to_the_built_in_heading_1_style_blend_into_th.docx"):
    """Verify that Heading 1 style has ONLY a 0.5 pt (size=4) straight bottom border
    and no other side borders. Returns a progressive score between 0-1."""

    score = 0.0      # progressive score we will build up
    max_score = 1.0  # cap to 1.0

    # ------------------------------------------------------------------
    # 1. Basic file existence (no points – prerequisite only)
    # ------------------------------------------------------------------
    if not os.path.exists(docx_path):
        print("✗ File not found:", docx_path)
        return 0.0

    try:
        # ------------------------------------------------------------------
        # 2. Locate Heading 1 style inside styles.xml and inspect borders
        # ------------------------------------------------------------------
        with zipfile.ZipFile(docx_path) as z:
            if "word/styles.xml" not in z.namelist():
                print("✗ styles.xml missing in DOCX")
                return 0.0
            styles_xml = z.read("word/styles.xml")

        root = ET.fromstring(styles_xml)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

        heading1_style = None
        for st in root.findall(".//w:style", ns):
            style_id = st.get(f"{{{ns['w']}}}styleId", "").lower()
            name_el = st.find("w:name", ns)
            name_val = name_el.get(f"{{{ns['w']}}}val", "").lower() if name_el is not None else ""
            if style_id in ("heading1", "heading 1") or name_val == "heading 1":
                heading1_style = st
                break

        if heading1_style is None:
            print("✗ Heading 1 style not found in styles.xml")
            return 0.0
        print("✓ Heading 1 style found (0 pts – prerequisite)")

        # ------ Border inspection ------
        pPr = heading1_style.find("w:pPr", ns)
        pBdr = pPr.find("w:pBdr", ns) if pPr is not None else None

        # 2a. Verify bottom border exists and is single (straight) 0.5pt (size=4)
        if pBdr is not None:
            bottom = pBdr.find("w:bottom", ns)
            if bottom is not None:
                val = bottom.get(f"{{{ns['w']}}}val")
                sz  = bottom.get(f"{{{ns['w']}}}sz")

                if val == "single":
                    print("✓ Bottom border style is 'single' (0.3 points)")
                    score += 0.3
                else:
                    print(f"✗ Bottom border style is '{val}', expected 'single'")

                # Word uses half-points *8 for size (size 4 == 0.5 pt)
                if sz and sz.isdigit() and int(sz) == 4:
                    print("✓ Bottom border size is 4 → 0.5 pt (0.3 points)")
                    score += 0.3
                else:
                    print(f"✗ Bottom border size is '{sz}', expected '4' (0.5 pt)")
            else:
                print("✗ Bottom border element missing in pBdr")
        else:
            print("✗ No pBdr element found in Heading 1 style")

        # 2b. Ensure NO other borders (top/left/right/between/bar) have visible values
        other_sides_ok = True
        if pBdr is not None:
            for side in ["top", "left", "right", "between", "bar"]:
                el = pBdr.find(f"w:{side}", ns)
                if el is not None:
                    val = el.get(f"{{{ns['w']}}}val", "")
                    if val not in ("nil", "none"):
                        print(f"✗ Unwanted {side} border found (val='{val}')")
                        other_sides_ok = False
        if pBdr is not None and other_sides_ok:
            print("✓ No unwanted borders on other sides (0.2 points)")
            score += 0.2

        # ------------------------------------------------------------------
        # 3. Confirm document actually contains Heading 1 paragraphs
        #    (ensures style is in active use, not just defined)
        # ------------------------------------------------------------------
        try:
            doc = Document(docx_path)
            if any(p.style and p.style.name.lower().startswith("heading 1") for p in doc.paragraphs):
                print("✓ Document contains Heading 1 paragraphs (0.2 points)")
                score += 0.2
            else:
                print("✗ No Heading 1 paragraphs found in the document")
        except Exception as e:
            print("✗ Error reading document for paragraph check:", e)

        # ------------------------------------------------------------------
        final_score = min(score, max_score)
        print(f"Total score: {final_score}")
        return final_score

    except Exception as e:
        print("✗ Unexpected error during verification:", e)
        traceback.print_exc()
        return 0.0

# ----------------------------------------------------------------------
# Execute verification when run as a script
# ----------------------------------------------------------------------
if __name__ == "__main__":
    reward = verify_heading1_bottom_border()
    print(f"REWARD: {reward}")
