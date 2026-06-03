"""
FINAL REWARD SCRIPT - SUCCESS
Task: Set Heading 3 to Italic 12 pt with Small caps.
Generated: 2025-10-17 10:31:00
Status: success
Model: azure-o3
Total Steps: 10
"""

import os
import zipfile
import xml.etree.ElementTree as ET


def verify_heading3_style(file_path: str) -> float:
    """Verify that every text run containing exactly the text
    'Heading 3' is formatted as Italic, 12 pt, Small caps.

    Scoring (progressive):
    • 0.4  – at least one matching text run found
    • 0.2  – italic correctly applied (per-run proportion)
    • 0.2  – font size ≈12 pt (1200 in EMU units, ≤±50 tolerance)
    • 0.2  – small-caps correctly applied (cap="small")
    Total = 1.0 only if all three properties are correct for every
    Heading 3 run.
    """

    print(f"Verifying file: {file_path}")
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    # XML namespaces used inside PPTX files
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }

    try:
        with zipfile.ZipFile(file_path) as z:
            # Collect all slide XML files
            slide_files = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]

            found = italic_ok = size_ok = caps_ok = 0

            for slide_file in slide_files:
                root = ET.fromstring(z.read(slide_file))
                # Iterate over all text runs in slide XML
                for run in root.findall('.//a:r', ns):
                    t = run.find('a:t', ns)
                    if t is None or not t.text or t.text.strip() != 'Heading 3':
                        continue  # not our target text

                    found += 1
                    rPr = run.find('a:rPr', ns)
                    if rPr is None:
                        print(f"✗ Missing rPr for Heading 3 in {slide_file}")
                        continue

                    # --- Italic check ---
                    if rPr.attrib.get('i') in {'1', 'true', 'on'}:
                        italic_ok += 1
                    else:
                        print(f"✗ Italic NOT set in {slide_file}")

                    # --- Font size check (12 pt = 1200) ---
                    sz_val = rPr.attrib.get('sz')
                    if sz_val is not None and sz_val.isdigit() and abs(int(sz_val) - 1200) <= 50:
                        size_ok += 1
                    else:
                        print(f"✗ Size incorrect in {slide_file} (value: {sz_val})")

                    # --- Small-caps check ---
                    if rPr.attrib.get('cap') == 'small':
                        caps_ok += 1
                    else:
                        print(f"✗ Small-caps NOT set in {slide_file}")

            # ------------------ Scoring ------------------
            score = 0.0
            if found:
                print(f"✓ Found {found} 'Heading 3' run(s)")
                score += 0.4  # presence of heading 3 text

                # Add proportional scores for each property
                score += 0.2 * (italic_ok / found)
                score += 0.2 * (size_ok / found)
                score += 0.2 * (caps_ok / found)
            else:
                print("✗ No 'Heading 3' text found in presentation")

            score = round(min(score, 1.0), 2)
            print(f"Total score: {score}")
            return score

    except Exception as e:
        print(f"✗ Error verifying presentation: {e}")
        return 0.0


if __name__ == "__main__":
    FILE_PATH = "/home/user/set_heading_3_to_italic_12_pt_with_small_caps.pptx"
    reward = verify_heading3_style(FILE_PATH)
    print(f"REWARD: {reward}")
