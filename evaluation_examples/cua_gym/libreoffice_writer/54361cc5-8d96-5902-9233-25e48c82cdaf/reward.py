"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Writer, I want all my Heading 2 sub-headings to start exactly 1.25 cm in from the left margin instead of being flush. What’s the quickest way to make that change stick for every Heading 2 in the whole document?
Generated: 2025-09-10 15:18:13
Status: success
Model: azure-o3
Total Steps: 12
"""

import os
import glob
import zipfile
from lxml import etree as ET

"""
Reward Script for LibreOffice Writer Task
Task: Ensure every Heading 2 paragraph starts exactly 1.25 cm (709 twips) from the left margin.
This script verifies:
 1. The document contains a Heading 2 style.
 2. The Heading 2 style’s left-indent equals 1.25 cm (±20 twips).
 3. All paragraphs using Heading 2 inherit the correct indent (no local overrides).
Progressive scoring (adds up to 1.0):
 • 0.1 – Heading 2 style present.
 • 0.4 – Heading 2 style indent set correctly.
 • 0.4 – Every Heading 2 paragraph effectively indented correctly.
 • 0.1 – Indent comes solely from the style (good practice, no manual overrides).
The script prints detailed diagnostics and the final score as "REWARD: X.X".
"""

TARGET_CM = 1.25                       # Required indent in centimetres
TWIPS_PER_CM = 567.0                   # 1 cm = 567 twips
TARGET_TWIPS = int(round(TARGET_CM * TWIPS_PER_CM))  # 709 twips
TOLERANCE = 20                         # Acceptable deviation in twips (~0.035 cm)
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

def _twips(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def _find_docx_file():
    """Locate the task DOCX file inside /home/user."""
    paths = glob.glob("/home/user/**/*.docx", recursive=True)
    # Prefer files whose names hint at this task
    preferred = [p for p in paths if "heading" in os.path.basename(p).lower() or "125" in p]
    return preferred[0] if preferred else (paths[0] if paths else None)

def _load_style_map(zipf):
    """Return dict(styleId -> {name, indent}). indent is left indent in twips or None."""
    try:
        styles_xml = zipf.read("word/styles.xml")
    except KeyError:
        print("✗ styles.xml not found – cannot verify styles")
        return {}
    root = ET.fromstring(styles_xml)
    style_map = {}
    for style in root.findall(".//w:style", NS):
        style_id = style.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}styleId")
        name_el  = style.find("w:name", NS)
        name_val = name_el.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val").lower() if name_el is not None else None
        # indent on style level
        indent_twips = None
        ppr = style.find("w:pPr", NS)
        if ppr is not None:
            ind = ppr.find("w:ind", NS)
            if ind is not None and ind.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left"):
                indent_twips = _twips(ind.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left"))
        style_map[style_id] = {"name": name_val, "indent": indent_twips}
    return style_map

def verify_heading2_indent(docx_path):
    print(f"Verifying document: {docx_path}")
    score = 0.0

    try:
        with zipfile.ZipFile(docx_path) as z:
            style_map = _load_style_map(z)

            # 1) Heading 2 style existence
            h2_ids = [sid for sid, info in style_map.items() if info["name"] == "heading 2"]
            if not h2_ids:
                print("✗ No Heading 2 style found")
            else:
                print(f"✓ Found Heading 2 style IDs: {h2_ids}")
                score += 0.1

            # 2) Heading 2 style indent correctness
            style_indent_ok = False
            if h2_ids:
                indent_val = next((style_map[sid]["indent"] for sid in h2_ids if style_map[sid]["indent"] is not None), None)
                if indent_val is not None and abs(indent_val - TARGET_TWIPS) <= TOLERANCE:
                    style_indent_ok = True
                    print(f"✓ Heading 2 style indent matches target ({indent_val} twips)")
                else:
                    print(f"✗ Heading 2 style indent incorrect (value={indent_val})")
            if style_indent_ok:
                score += 0.4

            # 3) Inspect each Heading 2 paragraph
            doc_xml = z.read("word/document.xml")
            root = ET.fromstring(doc_xml)
            h2_paras = []
            for p in root.findall(".//w:p", NS):
                ppr = p.find("w:pPr", NS)
                if ppr is None:
                    continue
                pstyle = ppr.find("w:pStyle", NS)
                if pstyle is None:
                    continue
                if pstyle.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val") in h2_ids:
                    h2_paras.append(p)

            if h2_paras:
                print(f"✓ Found {len(h2_paras)} Heading 2 paragraphs")
            else:
                print("✗ No paragraphs with Heading 2 style found")

            all_ok = True
            uses_style_only = True
            for p in h2_paras:
                ppr = p.find("w:pPr", NS)
                local_left = None
                if ppr is not None:
                    ind = ppr.find("w:ind", NS)
                    if ind is not None and ind.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left"):
                        local_left = _twips(ind.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left"))
                # effective indent
                if local_left is not None:
                    effective = local_left
                    uses_style_only = False  # manual override present
                else:
                    sid = ppr.find("w:pStyle", NS).get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val")
                    effective = style_map.get(sid, {}).get("indent")
                if effective is None or abs(effective - TARGET_TWIPS) > TOLERANCE:
                    all_ok = False
                    print(f"   ✗ Paragraph indent incorrect (value={effective})")
                else:
                    print(f"   ✓ Paragraph indent ok (value={effective})")

            if h2_paras and all_ok:
                score += 0.4
            if h2_paras and uses_style_only and all_ok:
                score += 0.1  # best practice bonus

    except Exception as e:
        print(f"✗ Error processing document: {e}")
        return 0.0

    final_score = round(min(score, 1.0), 2)
    print(f"Computed score: {final_score}")
    return final_score

def main():
    docx_path = _find_docx_file()
    if not docx_path:
        print("✗ No DOCX file found to verify")
        print("REWARD: 0.0")
        return
    reward = verify_heading2_indent(docx_path)
    print(f"REWARD: {reward}")

# Execute verification when script runs
if __name__ == "__main__":
    main()

