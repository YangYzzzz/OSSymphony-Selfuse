"""
FINAL REWARD SCRIPT - SUCCESS
Task: The print shop wants my book laid out with mirrored margins—exactly Inner 2.50 cm and Outer 2.50 cm for every page. How do I set that up for the whole document in LibreOffice Writer?
Generated: 2025-09-10 18:01:25
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import glob
import zipfile
from lxml import etree


def verify_mirrored_margins(file_path: str) -> float:
    """Verify that every section in the DOCX uses mirrored margins
    and that both the inner and outer margins are exactly 2.50 cm (≈1417 twips).

    Scoring (progressive):
      • Mirror-margins tag correctness – 40 %
      • Exact inner/outer margin values – 60 %
    Returns a float between 0.0 and 1.0 and prints a detailed breakdown.
    """
    print(f"Verifying mirrored margins for: {file_path}")
    if not os.path.exists(file_path):
        print("✗ File not found – 0 points")
        return 0.0

    try:
        # ------------------------------------------------------------------
        # 1) Extract document.xml from the DOCX package
        # ------------------------------------------------------------------
        with zipfile.ZipFile(file_path) as z:
            if "word/document.xml" not in z.namelist():
                print("✗ document.xml missing – 0 points")
                return 0.0
            doc_xml = z.read("word/document.xml")

        # ------------------------------------------------------------------
        # 2) Parse XML and collect <w:sectPr> sections
        # ------------------------------------------------------------------
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        root = etree.fromstring(doc_xml)
        sect_prs = root.xpath("//w:sectPr", namespaces=ns)

        if not sect_prs:
            print("✗ No <w:sectPr> elements found – cannot verify")
            return 0.0

        total_sections = len(sect_prs)
        mirror_ok = 0  # sections with <w:mirrorMargins>
        margin_ok = 0  # sections with correct inside/outside values

        # 2.50 cm ⇒ twips (1 inch = 2.54 cm = 1440 twips)
        expected_twips = int(round(2.5 / 2.54 * 1440))  # ≈1417 twips
        tolerance = 25  # allow ~0.04 cm deviation
        print(f"Expected margin (twips): {expected_twips} ±{tolerance}")

        # ------------------------------------------------------------------
        # 3) Inspect each section for mirrored margins & correct values
        # ------------------------------------------------------------------
        for idx, sect in enumerate(sect_prs, start=1):
            # 3a) mirrorMargins tag
            has_mirror = bool(sect.xpath("./w:mirrorMargins", namespaces=ns))
            if has_mirror:
                mirror_ok += 1
                print(f"  Section {idx}: ✓ mirrorMargins present")
            else:
                print(f"  Section {idx}: ✗ mirrorMargins missing")

            # 3b) pgMar element & inside/outside attributes
            pg_mar = sect.xpath("./w:pgMar", namespaces=ns)
            if not pg_mar:
                print(f"  Section {idx}: ✗ <w:pgMar> missing")
                continue
            pg_mar = pg_mar[0]

            # inside/outside are preferred for mirrored docs; fall back to left/right if absent
            inside_val = pg_mar.get(f"{{{ns['w']}}}inside") or pg_mar.get(f"{{{ns['w']}}}left")
            outside_val = pg_mar.get(f"{{{ns['w']}}}outside") or pg_mar.get(f"{{{ns['w']}}}right")

            try:
                inside_val = int(inside_val) if inside_val is not None else None
                outside_val = int(outside_val) if outside_val is not None else None
            except ValueError:
                inside_val = outside_val = None

            if inside_val is None or outside_val is None:
                print(f"  Section {idx}: ✗ Unable to read inside/outside values")
            else:
                in_diff = abs(inside_val - expected_twips)
                out_diff = abs(outside_val - expected_twips)
                if in_diff <= tolerance and out_diff <= tolerance:
                    margin_ok += 1
                    print(
                        f"  Section {idx}: ✓ Margins correct (inside={inside_val}, outside={outside_val})"
                    )
                else:
                    print(
                        f"  Section {idx}: ✗ Margins incorrect (inside={inside_val}, outside={outside_val})"
                    )

        # ------------------------------------------------------------------
        # 4) Progressive scoring
        # ------------------------------------------------------------------
        mirror_score = (mirror_ok / total_sections) * 0.4
        margin_score = (margin_ok / total_sections) * 0.6
        total_score = round(min(mirror_score + margin_score, 1.0), 2)

        print(
            f"Scoring: mirror {mirror_ok}/{total_sections} → {mirror_score:.2f}, "
            f"margins {margin_ok}/{total_sections} → {margin_score:.2f}"
        )
        print(f"Total score: {total_score}")
        return total_score

    except Exception as exc:
        print(f"✗ Verification failed with exception: {exc}")
        return 0.0


if __name__ == "__main__":
    # Automatically pick a DOCX in /home/user (task environment)
    docx_files = glob.glob("/home/user/*.docx")
    target_file = docx_files[0] if docx_files else "document.docx"

    reward = verify_mirrored_margins(target_file)
    print(f"REWARD: {reward}")
