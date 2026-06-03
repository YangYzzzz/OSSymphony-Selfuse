"""
FINAL REWARD SCRIPT - SUCCESS
Task: Apply 'Preformatted Text' style to the paragraph labeled 'Sample Output'.
Generated: 2025-10-17 16:44:04
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import re
import zipfile
from lxml import etree

"""
Reward Script
-------------
Verifies that the paragraph whose **exact** text is "Sample Output" has been
formatted with the *Preformatted Text* style in the supplied presentation
(`.pptx`) file.

LibreOffice’s *Preformatted Text* style typically applies:
  • A monospaced font such as **Courier New**
  • A 12-point font size  (stored as 1200 in OOXML – hundredths of a point)

The script therefore checks three independent aspects and awards progressive
points ONLY when the corresponding evidence is present:
 1. Target paragraph is found (0.3)
 2. Paragraph (first run) uses a monospaced font – “courier” or “mono” (0.4)
 3. Paragraph (first run) has font size ≤ 14 pt  (≤ 1400) – allowing a small
    tolerance (0.3)

A perfect implementation yields a total of 1.0.  Partial credit is possible
if only some requirements are met.
"""

# -----------------------------------------------------------------------------
# Helper / Core verification function
# -----------------------------------------------------------------------------

def verify_preformatted_paragraph(pptx_path: str) -> float:
    """Return a score in [0.0, 1.0] based on verification results."""

    max_score = 1.0
    score = 0.0

    # Flags for progressive scoring
    paragraph_found = False
    font_is_mono = False
    size_is_preformatted = False

    # Namespace used in PPTX drawingML
    ns = {
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    }

    # ------------------------------------------------------------------
    # 1. Ensure the PPTX file exists and open its XML contents
    # ------------------------------------------------------------------
    if not os.path.exists(pptx_path):
        print(f"✗ File not found: {pptx_path}")
        return 0.0  # No points – task cannot be verified

    try:
        with zipfile.ZipFile(pptx_path, "r") as z:
            slide_files = [
                f for f in z.namelist()
                if f.startswith("ppt/slides/slide") and f.endswith(".xml")
            ]

            # ------------------------------------------------------------------
            # Iterate through all slide XML files looking for the paragraph
            # ------------------------------------------------------------------
            for slide_path in slide_files:
                xml_bytes = z.read(slide_path)
                root = etree.fromstring(xml_bytes)

                # Locate <a:p> elements and reconstruct plain paragraph text
                for pElem in root.xpath(".//a:p", namespaces=ns):
                    texts = [t.text for t in pElem.xpath(".//a:t", namespaces=ns) if t.text]
                    if not texts:
                        continue

                    para_text = "".join(texts).strip()

                    if re.fullmatch(r"Sample Output", para_text):
                        paragraph_found = True
                        print(f"✓ Found target paragraph in '{slide_path}'")

                        # Check first text run (<a:r>) for styling attributes
                        first_run = pElem.find("a:r", namespaces)
                        if first_run is not None:
                            rPr = first_run.find("a:rPr", namespaces)
                            if rPr is not None:
                                # Font face check via <a:latin typeface="…"/>
                                latin = rPr.find("a:latin", namespaces)
                                if latin is not None and "typeface" in latin.attrib:
                                    typeface = latin.attrib["typeface"].lower()
                                    print(f"  Detected font face: {typeface}")
                                    if "courier" in typeface or "mono" in typeface:
                                        font_is_mono = True

                                # Font size check (sz attribute – hundredths of a point)
                                if "sz" in rPr.attrib:
                                    try:
                                        size_val = int(rPr.attrib["sz"])
                                        print(f"  Detected size attribute: {size_val}")
                                        if size_val <= 1400:  # ≤ 14 pt counts as preformatted (12 pt default)
                                            size_is_preformatted = True
                                    except ValueError:
                                        pass

                        # No need to scan further slides once found
                        break
                if paragraph_found:
                    break
    except Exception as e:
        print(f"✗ Error reading PPTX content: {e}")
        return 0.0  # Catastrophic failure – no score

    # ------------------------------------------------------------------
    # Scoring – only award points for *actual* verified evidence
    # ------------------------------------------------------------------
    if paragraph_found:
        score += 0.3
    else:
        print("✗ Paragraph with exact text 'Sample Output' not found")

    if paragraph_found and font_is_mono:
        score += 0.4
    else:
        if paragraph_found:
            print("✗ Paragraph is not using a monospaced font (e.g., Courier)")

    if paragraph_found and size_is_preformatted:
        score += 0.3
    else:
        if paragraph_found:
            print("✗ Paragraph size is not consistent with Preformatted Text style")

    # Cap score at 1.0
    final_score = min(score, max_score)

    # ------------------------------------------------------------------
    # Report summary and final reward
    # ------------------------------------------------------------------
    print(
        f"Score breakdown -> found:{paragraph_found} font:{font_is_mono} size:{size_is_preformatted}"
    )
    print(f"REWARD: {final_score}")

    return final_score

# -----------------------------------------------------------------------------
# Execute verification when script is run directly
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    target_file = "/home/user/apply_preformatted_text_style_to_the_paragraph_labeled_sample_output.pptx"
    verify_preformatted_paragraph(target_file)

