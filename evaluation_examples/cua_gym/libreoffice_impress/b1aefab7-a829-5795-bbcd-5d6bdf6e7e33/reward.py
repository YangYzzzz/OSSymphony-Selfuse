"""
FINAL REWARD SCRIPT - SUCCESS
Task: The image on slide 228 looks a bit harsh against the background. In LibreOffice Impress, how can I either soften its edges by exactly 2 px, or—if that option isn’t available—apply a soft shadow instead?
Generated: 2025-09-10 21:44:02
Status: success
Model: azure-o3
Total Steps: 8
"""

import os
import glob
import zipfile
import xml.etree.ElementTree as ET

# ------------------------------------------------------------
# Reward script for verifying LibreOffice Impress task:
# "Soften the image edges by exactly 2 px OR apply a soft shadow
#  to the image on slide 228 of the provided presentation."
# ------------------------------------------------------------
# Scoring rules (progressive):
#  • 0.3  – Presentation contains at least one image on slide 228
#  • 0.7  – That image has EITHER a 2-px soft edge (≈19 050 EMUs) OR
#           any kind of soft shadow (outerShdw / innerShdw)
#  • 0.4  – Partial credit if a soft edge exists but radius is wrong
#  • 1.0  – All requirements satisfied (soft edge ≈2 px OR soft shadow)
# ------------------------------------------------------------
# Absolutely NO hard-coding of “success”; all checks are data-driven.
# ------------------------------------------------------------

def find_presentation_file():
    """Return the most likely PPTX file to verify."""
    candidates = glob.glob("*.pptx")
    if not candidates:
        candidates = glob.glob("**/*.pptx", recursive=True)
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    # Prefer a name that references this task (contains '228')
    for c in candidates:
        if "228" in c:
            return c
    return sorted(candidates)[0]


def verify_soft_effect(file_path: str, slide_number: int = 228):
    """Verify 2-px soft edge OR soft shadow on any image in the given slide."""
    details = []
    score = 0.0

    # ——— File existence ———
    if not os.path.exists(file_path):
        details.append(f"✗ File not found: {file_path}")
        return 0.0, details
    details.append(f"✓ Found presentation file: {file_path}")

    # ——— Extract slide XML ———
    slide_path = f"ppt/slides/slide{slide_number}.xml"
    try:
        with zipfile.ZipFile(file_path) as z:
            if slide_path not in z.namelist():
                details.append(f"✗ Slide {slide_number} not found in presentation")
                return 0.0, details
            slide_xml = z.read(slide_path)
    except Exception as e:
        details.append(f"✗ Error opening PPTX: {e}")
        return 0.0, details

    # ——— Parse XML ———
    try:
        root = ET.fromstring(slide_xml)
    except ET.ParseError as e:
        details.append(f"✗ XML parse error: {e}")
        return 0.0, details

    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    }

    pictures = root.findall(".//p:pic", ns)
    if not pictures:
        details.append(f"✗ No images found on slide {slide_number}")
        return 0.0, details

    details.append(f"✓ Found {len(pictures)} image(s) on slide {slide_number}")
    score += 0.3  # progress: correct slide & image detected

    # ——— Check effects on each picture ———
    target_rad = 19050  # ≈ 2 px in EMUs at 96 DPI (9525 EMUs per px)
    tolerance = 3000    # ± 3 000 EMUs tolerance (~0.3 px)
    softedge_ok = False
    softedge_wrong = False
    softshadow_ok = False

    for pic in pictures:
        soft_edge = pic.find(".//a:softEdge", ns)
        if soft_edge is not None:
            try:
                rad_val = int(soft_edge.attrib.get("rad", "0"))
            except ValueError:
                rad_val = 0
            if abs(rad_val - target_rad) <= tolerance:
                softedge_ok = True
                details.append(f"✓ 2 px soft edge detected (radius {rad_val} EMUs)")
            else:
                softedge_wrong = True
                details.append(
                    f"• Soft edge present but radius {rad_val} EMUs ≠ 2 px target"
                )

        # Look for soft shadow (outer or inner)
        if pic.find(".//a:outerShdw", ns) is not None or pic.find(
            ".//a:innerShdw", ns
        ) is not None:
            softshadow_ok = True
            details.append("✓ Soft shadow detected on image")

    # ——— Scoring based on findings ———
    if softedge_ok or softshadow_ok:
        score += 0.7  # main requirement met
    elif softedge_wrong:
        score += 0.4  # partial credit: soft edge but wrong radius

    score = min(score, 1.0)

    if score == 1.0:
        details.append("✓ All verification checks passed – task complete.")
    else:
        details.append("✗ Task not fully completed – missing/incorrect effect.")

    return score, details


if __name__ == "__main__":
    pptx_file = find_presentation_file()
    if pptx_file is None:
        print("✗ No .pptx file found in the workspace. Cannot evaluate task.")
        print("REWARD: 0.0")
    else:
        final_score, log_messages = verify_soft_effect(pptx_file, slide_number=228)
        print("\nVerification breakdown:")
        for line in log_messages:
            print(line)
        print(f"\nREWARD: {final_score}")
