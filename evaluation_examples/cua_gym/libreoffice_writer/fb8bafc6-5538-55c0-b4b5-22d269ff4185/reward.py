"""
FINAL REWARD SCRIPT - SUCCESS
Task: Make DejaVu Serif the default typeface in LibreOffice Writer.
Generated: 2025-10-14 11:17:32
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET

def _has_dejavu_serif(rFonts, ns):
    """Helper to check if a <w:rFonts> element uses DejaVu Serif for ANY of the major font
    attributes (ascii, hAnsi, eastAsia, cs)."""
    if rFonts is None:
        return False
    for attr in ("ascii", "hAnsi", "eastAsia", "cs"):
        val = rFonts.get(f"{{{ns['w']}}}{attr}")
        if val and re.search(r"dejavu\s+serif", val, re.I):
            return True
    return False

def _check_docx(file_path):
    """Return a tuple (docDefaults_ok, normal_ok)."""
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(file_path) as z:
        styles_xml = z.read("word/styles.xml")
    root = ET.fromstring(styles_xml)

    # 1) Check document defaults font family
    rFonts_defaults = root.find(
        "./w:docDefaults/w:rPrDefault/w:rPr/w:rFonts", ns)
    doc_defaults_ok = _has_dejavu_serif(rFonts_defaults, ns)

    # 2) Check the Normal paragraph style (styleId="Normal")
    normal_style = None
    for style in root.findall(".//w:style", ns):
        if style.get(f"{{{ns['w']}}}styleId") == "Normal":
            normal_style = style
            break
    normal_ok = False
    if normal_style is not None:
        rFonts_normal = normal_style.find(".//w:rPr/w:rFonts", ns)
        normal_ok = _has_dejavu_serif(rFonts_normal, ns)

    return doc_defaults_ok, normal_ok

def _check_odt(file_path):
    """Return True if an ODT's default paragraph style uses DejaVu Serif."""
    with zipfile.ZipFile(file_path) as z:
        if "styles.xml" not in z.namelist():
            return False
        styles_xml = z.read("styles.xml").decode("utf-8", errors="ignore")

    # Simple regex search for DejaVu Serif in default paragraph style
    default_style_pattern = re.compile(r"<style:default-style[^>]+style:family=\"paragraph\"[\s\S]*?</style:default-style>", re.I)
    for block in default_style_pattern.findall(styles_xml):
        if re.search(r"dejavu\s+serif", block, re.I):
            return True
    # Fallback global search
    return bool(re.search(r"dejavu\s+serif", styles_xml, re.I))

def verify_default_font(file_path):
    """Verify the task: Make DejaVu Serif the default typeface in LibreOffice Writer.

    Scoring:
    - 0.0  : DejaVu Serif not set anywhere as default
    - 0.3  : Only Normal style updated (partial progress)
    - 1.0  : Document defaults (or ODT default paragraph style) set to DejaVu Serif
    """
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0

    ext = os.path.splitext(file_path)[1].lower()
    score = 0.0

    try:
        if ext == ".docx":
            doc_ok, normal_ok = _check_docx(file_path)
            if doc_ok:
                score = 1.0
                print("✓ docDefaults default font set to DejaVu Serif (DOCX)")
            elif normal_ok:
                score = 0.3
                print("✓ Normal style font set to DejaVu Serif, but docDefaults not updated (partial)")
            else:
                print("✗ DejaVu Serif not set as default in DOCX file")
        elif ext == ".odt":
            odt_ok = _check_odt(file_path)
            if odt_ok:
                score = 1.0
                print("✓ Default paragraph style uses DejaVu Serif (ODT)")
            else:
                print("✗ DejaVu Serif not set as default in ODT file")
        else:
            print("✗ Unsupported file type. Only .docx or .odt are expected for Writer documents.")
            score = 0.0
    except Exception as e:
        # Any parsing error is treated as failure (score 0.0)
        print(f"✗ Error while verifying document: {e}")
        score = 0.0

    print(f"Final score: {score}")
    return score

# --------------------
# MAIN EXECUTION BLOCK
# --------------------
if __name__ == "__main__":
    # Path provided by the task context
    file_path = "/home/user/make_dejavu_serif_the_default_typeface_in_libreoffice_writer.docx"

    reward = verify_default_font(file_path)
    print(f"REWARD: {reward}")

