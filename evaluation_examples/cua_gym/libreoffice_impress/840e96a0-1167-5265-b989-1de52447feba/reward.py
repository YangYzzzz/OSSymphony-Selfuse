"""
FINAL REWARD SCRIPT - SUCCESS
Task: Set the 'First Page' style on page 1 and suppress both header and footer.
Generated: 2025-10-17 15:37:20
Status: success
Model: azure-o3
Total Steps: 12
"""

import os
import re
import zipfile


def detect_header_footer(xml_text: str):
    """Detect presence of header and footer placeholders in raw slide XML.

    Returns:
        tuple(bool, bool): (header_present, footer_present)
    """
    header_regex = r"(HeaderPlaceholder|ph[^>]*type=\"hdr\")"
    footer_regex = r"(FooterPlaceholder|ph[^>]*type=\"ftr\")"

    header_present = bool(re.search(header_regex, xml_text, flags=re.IGNORECASE))
    footer_present = bool(re.search(footer_regex, xml_text, flags=re.IGNORECASE))
    return header_present, footer_present


def verify_task(file_path: str):
    """Reward-script verification for Impress task:
    "Set the 'First Page' style on page 1 and suppress both header and footer."""

    print(f"Starting verification for: {file_path}")

    # Basic existence check (NO points awarded for this!)
    if not os.path.exists(file_path):
        print("✗ File not found – task failed")
        print("REWARD: 0.0")
        return 0.0

    total_score = 0.0
    max_score = 1.0  # Cap for safety

    try:
        with zipfile.ZipFile(file_path) as pptx_zip:
            # Collect slide XML files and sort numerically (slide1.xml, slide2.xml, ...)
            slide_files = [f for f in pptx_zip.namelist()
                           if f.startswith("ppt/slides/slide") and f.endswith(".xml")]
            if not slide_files:
                print("✗ No slide XML files detected – invalid PPTX")
                print("REWARD: 0.0")
                return 0.0

            slide_files.sort(key=lambda x: int(re.search(r"slide(\d+)\.xml", x).group(1)))
            print(f"✓ Detected {len(slide_files)} slide(s)")

            # ---------------- Requirement 1 & 2 ----------------
            # Header & footer must be suppressed on FIRST slide
            first_slide_xml = pptx_zip.read(slide_files[0]).decode("utf-8", errors="ignore")
            first_has_header, first_has_footer = detect_header_footer(first_slide_xml)

            # Header suppression (0.4 points)
            if not first_has_header:
                print("✓ Header is suppressed on first slide (0.4 pts)")
                total_score += 0.4
            else:
                print("✗ Header still present on first slide (0 pts)")

            # Footer suppression (0.4 points)
            if not first_has_footer:
                print("✓ Footer is suppressed on first slide (0.4 pts)")
                total_score += 0.4
            else:
                print("✗ Footer still present on first slide (0 pts)")

            # ---------------- Requirement 3 ----------------
            # Subsequent slides SHOULD retain header & footer (0.2 pts)
            other_header_found = False
            other_footer_found = False

            for slide_path in slide_files[1:]:
                xml_text = pptx_zip.read(slide_path).decode("utf-8", errors="ignore")
                hdr_present, ftr_present = detect_header_footer(xml_text)
                other_header_found = other_header_found or hdr_present
                other_footer_found = other_footer_found or ftr_present

            if slide_files[1:]:  # Only evaluate if more than one slide exists
                if other_header_found and other_footer_found:
                    print("✓ Header & footer present on subsequent slide(s) (0.2 pts)")
                    total_score += 0.2
                else:
                    print("✗ Could not confirm header & footer on subsequent slides (0 pts)")
            else:
                # If there is only one slide, we cannot award the extra 0.2 pts
                print("! Single-slide file – skipping subsequent slide check (0 pts)")

    except Exception as e:
        print(f"✗ Exception during verification: {e}")
        print("REWARD: 0.0")
        return 0.0

    final_score = min(total_score, max_score)
    print(f"Final score: {final_score} / {max_score}")
    print(f"REWARD: {final_score}")
    return final_score


# ---------------- Execute verification ----------------
if __name__ == "__main__":
    verify_task("/home/user/set_the_first_page_style_on_page_1_and_suppress_both_header_and_footer.pptx")
