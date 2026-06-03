"""
FINAL REWARD SCRIPT - SUCCESS
Task: My presentation has reached slide 200, and I want to park a safety copy before I tweak anything else. In LibreOffice Impress, how do I export the entire deck in its native ODP format straight to ~/Desktop/deck.odp and then keep working in that new file once it’s saved (i.e., leave the freshly exported copy open)?
Generated: 2025-09-10 20:20:30
Status: success
Model: azure-o3
Total Steps: 9
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from pptx import Presentation

# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def is_valid_odp(file_path: str) -> bool:
    """Basic sanity-check that file is an ODP (zip with content.xml)."""
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            return "content.xml" in z.namelist()
    except zipfile.BadZipFile:
        return False


def count_pptx_slides(file_path: str) -> int:
    """Return slide count in a PPTX using python-pptx."""
    try:
        prs = Presentation(file_path)
        return len(prs.slides)
    except Exception as exc:
        print(f"✗ Error loading PPTX: {exc}")
        return 0


def count_odp_slides(file_path: str) -> int:
    """Return slide count in an ODP by parsing content.xml."""
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            content = z.read("content.xml")
        ns = {
            "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
            "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
            "presentation": "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
        }
        root = ET.fromstring(content)
        pages = root.findall(".//draw:page", ns)
        # Count pages classified as slides (or without the class attr)
        slide_pages = [p for p in pages if p.get("{urn:oasis:names:tc:opendocument:xmlns:presentation:1.0}class") in (None, "slide")]
        if not slide_pages:  # fallback – some ODPs omit class attr
            slide_pages = pages
        return len(slide_pages)
    except Exception as exc:
        print(f"✗ Error reading ODP: {exc}")
        return 0

# ------------------------------------------------------------
# Main Verification Logic
# ------------------------------------------------------------

def verify_impress_export() -> float:
    """Verify that a safety copy was exported to ~/Desktop/deck.odp correctly."""

    original_pptx = "/home/user/my_presentation_has_reached_slide_200_and_i_want_to_park_a_safety_copy_before_i_tweak_anything_else__golden.pptx"
    exported_odp = os.path.expanduser("~/Desktop/deck.odp")

    max_score = 1.0
    score = 0.0

    print("--- Verifying LibreOffice Impress safety-copy task ---")
    print(f"Original deck : {original_pptx}")
    print(f"Exported deck : {exported_odp}\n")

    # 1. File exists at the exact requested location (0.2)
    if os.path.exists(exported_odp):
        print("✓ Exported file exists at requested path (0.2)")
        score += 0.2
    else:
        print("✗ Exported file not found – cannot continue further checks")
        print(f"REWARD: {score}")
        return score  # early exit – other checks depend on file

    # 2. File is a valid ODP archive (0.2)
    if is_valid_odp(exported_odp):
        print("✓ File is a valid ODP archive with content.xml (0.2)")
        score += 0.2
    else:
        print("✗ File is not a valid ODP archive (0 points)")

    # 3. Slide count matches original deck (up to 0.4, proportional)
    orig_count = count_pptx_slides(original_pptx)
    new_count = count_odp_slides(exported_odp)
    print(f"Original slide count : {orig_count}")
    print(f"Exported slide count : {new_count}")

    if orig_count > 0:
        if new_count == orig_count:
            print("✓ Slide counts match exactly (0.4)")
            score += 0.4
        else:
            ratio = new_count / orig_count
            proportional = 0.4 * max(0.0, min(1.0, ratio))
            print(f"✗ Slide count mismatch – awarding proportional credit {proportional:.2f}")
            score += proportional
    else:
        print("✗ Could not determine original slide count (0 points)")

    # 4. Exported file timestamp is newer than original (0.1)
    try:
        if os.path.getmtime(exported_odp) >= os.path.getmtime(original_pptx):
            print("✓ Exported file timestamp is newer than original (0.1)")
            score += 0.1
        else:
            print("✗ Exported file timestamp is older than original (0 points)")
    except Exception as exc:
        print(f"✗ Error comparing timestamps: {exc}")

    # 5. Non-empty deck safeguard (0.1)
    if new_count > 0:
        print("✓ Exported deck is non-empty (0.1)")
        score += 0.1
    else:
        print("✗ Exported deck appears empty (0 points)")

    # Clamp & report final score
    final_score = round(min(score, max_score), 2)
    print("------------------------------------------------------")
    print(f"Total Score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score

# ------------------------------------------------------------
# Auto-execute when run as a script
# ------------------------------------------------------------
if __name__ == "__main__":
    verify_impress_export()

