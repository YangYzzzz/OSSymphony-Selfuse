"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m mid-way through my geometry handout, and I need to pop the Pythagorean formula—exactly "x^2 + y^2 = z^2"—right at the current cursor spot. How do I insert that as a proper LibreOffice Writer formula instead of plain text?
Generated: 2025-09-10 17:05:31
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import re
from zipfile import ZipFile
from lxml import etree
from docx import Document


def _plain_text_formula_exists(doc: Document) -> bool:
    """Check if the Pythagorean formula exists only as plain text (partial-credit case)."""
    all_text = " ".join(p.text for p in doc.paragraphs if p.text)
    # Allow flexible spacing and the optional caret character
    pattern = r"x\s*\^?2\s*\+\s*y\s*\^?2\s*=\s*z\s*\^?2"
    return re.search(pattern, all_text, re.IGNORECASE) is not None


def _math_formula_object_exists(docx_path: str) -> bool:
    """Inspect the DOCX XML for a proper Math (oMath/oMathPara) object
    containing the Pythagorean formula. LibreOffice Writer and Word both store
    equation objects in the <m:oMath> / <m:oMathPara> tags.
    """
    ns = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    }
    pattern = re.compile(r"x2\s*\+\s*y2\s*=\s*z2", re.IGNORECASE)

    try:
        with ZipFile(docx_path) as z:
            if "word/document.xml" not in z.namelist():
                return False  # Unexpected – cannot locate main document part
            xml_content = z.read("word/document.xml")
            root = etree.fromstring(xml_content)

            # Search all math objects
            math_nodes = root.xpath(".//m:oMath | .//m:oMathPara", namespaces=ns)
            for node in math_nodes:
                # Gather visible text tokens inside the math object
                texts = [t.text for t in node.xpath('.//m:t | .//w:t', namespaces=ns) if t.text]
                concat = "".join(texts).replace("^", "")  # caret not stored but just in case
                if pattern.search(concat):
                    return True  # Found the correct math equation object
    except Exception as e:
        print(f"✗ Error inspecting DOCX math XML: {e}")
        return False

    return False  # No matching math object found


def verify_task(docx_path: str) -> float:
    """Main verification routine that returns a progressive score from 0.0–1.0."""
    print(f"Verifying LibreOffice Writer formula insertion in: {docx_path}")

    # Basic file existence check (no points for merely existing)
    if not os.path.exists(docx_path):
        print("✗ File not found – task automatically fails")
        print("REWARD: 0.0")
        return 0.0

    total_score = 0.0
    MAX_SCORE = 1.0

    # 1) Primary requirement – proper formula object (full credit)
    if _math_formula_object_exists(docx_path):
        print("✓ Proper math formula object for 'x^2 + y^2 = z^2' found (1.0 points)")
        total_score = 1.0  # Perfect completion – skip further checks
    else:
        # 2) Fallback – plain text formula only (partial credit)
        try:
            doc = Document(docx_path)
            if _plain_text_formula_exists(doc):
                print("✗ Formula present only as plain text (0.4 points)")
                total_score = 0.4
            else:
                print("✗ Pythagorean formula not found in any form (0 points)")
        except Exception as e:
            print(f"✗ Error loading DOCX for plain-text check: {e}")
            total_score = 0.0

    # Ensure the score never exceeds MAX_SCORE
    final_score = min(total_score, MAX_SCORE)
    print(f"REWARD: {final_score}")
    return final_score


# ----------------------------
# When executed as a script
# ----------------------------
if __name__ == "__main__":
    USER_DOC = "/home/user/im_mid_way_through_my_geometry_handout_and_i_need_to_pop_the_pythagorean_formulaexactly_x2_y2_z2righ.docx"
    verify_task(USER_DOC)
