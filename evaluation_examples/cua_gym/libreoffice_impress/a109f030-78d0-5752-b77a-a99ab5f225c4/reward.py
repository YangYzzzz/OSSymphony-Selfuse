"""
FINAL REWARD SCRIPT - SUCCESS
Task: The title on slide 89 feels too airy—letters are spaced out more than I’d like. In LibreOffice Impress, how do I condense that title’s character spacing by exactly 0.3 pt?
Generated: 2025-09-10 23:51:22
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import zipfile
from lxml import etree

def verify_character_spacing(file_path: str, slide_index: int = 89, expected_spacing_pt: float = -0.3):
    """Reward-script verifier for the task:
    "Condense the title on slide 89 by exactly 0.3 pt in LibreOffice Impress."

    Scoring (progressive, max 1.0):
      • +0.3  – Title placeholder exists on the target slide.
      • +0.7  – Proportional to the fraction of text runs whose character-spacing
                equals the expected value (-0.3 pt → ‑30 in 1/100 pt units).
    The script returns a float between 0.0 and 1.0 and prints detailed feedback
    followed by "REWARD: X.X".
    """
    print(f"Starting verification for file: {file_path}")

    # ------------------------------------------------------------------
    # 1. Basic presence checks (no points awarded here!)
    # ------------------------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ Presentation file not found.")
        print("REWARD: 0.0")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as pptx_zip:
            slide_path = f"ppt/slides/slide{slide_index}.xml"
            if slide_path not in pptx_zip.namelist():
                print(f"✗ Expected slide XML not found ({slide_path})")
                print("REWARD: 0.0")
                return 0.0

            slide_xml = pptx_zip.read(slide_path)

        # ------------------------------------------------------------------
        # 2. Parse slide XML & locate title placeholder(s)
        # ------------------------------------------------------------------
        root = etree.fromstring(slide_xml)
        ns = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
        }

        title_shapes = []
        for sp in root.xpath('.//p:sp', namespaces=ns):
            ph = sp.find('.//p:nvSpPr/p:nvPr/p:ph', namespaces=ns)
            if ph is not None and ph.get('type') in ('title', 'ctrTitle'):
                title_shapes.append(sp)

        score = 0.0
        if not title_shapes:
            print("✗ No title placeholder located on the slide.")
        else:
            print(f"✓ Found {len(title_shapes)} title placeholder(s)")
            score += 0.3  # Earned for correctly targeting the title

        # If there is no title, nothing further can be checked
        if not title_shapes:
            final = round(score, 2)
            print(f"REWARD: {final}")
            return final

        # ------------------------------------------------------------------
        # 3. Verify character spacing of each text run in the title
        # ------------------------------------------------------------------
        expected_spacing_hundredths = int(round(expected_spacing_pt * 100))  # -0.3 pt → -30
        total_runs = 0
        correct_runs = 0

        for sp in title_shapes:
            for run in sp.xpath('.//a:r', namespaces=ns):
                total_runs += 1
                rpr = run.find('.//a:rPr', namespaces=ns)
                # Missing rPr or spc → default 0
                spacing_val = 0
                if rpr is not None and rpr.get('spc') is not None:
                    try:
                        spacing_val = int(rpr.get('spc'))
                    except ValueError:
                        spacing_val = None  # malformed value – counts as incorrect

                if spacing_val == expected_spacing_hundredths:
                    correct_runs += 1

        if total_runs == 0:
            print("✗ No text runs found in the title placeholder.")
            final = round(score, 2)
            print(f"REWARD: {final}")
            return final

        print(f"Runs inspected: {total_runs}")
        print(f"Runs with correct spacing: {correct_runs}")

        # Proportional score for correct spacing
        proportion_correct = correct_runs / total_runs
        score += 0.7 * proportion_correct

        final_score = min(1.0, round(score, 2))
        if final_score == 1.0:
            print("✓ All title characters have the correct condensed spacing.")
        elif proportion_correct > 0:
            print("• Partial success: Some runs have the correct spacing.")
        else:
            print("✗ Spacing not correctly applied to any runs.")

        print(f"REWARD: {final_score}")
        return final_score

    except Exception as e:
        print(f"✗ Verification failed due to error: {e}")
        print("REWARD: 0.0")
        return 0.0

# ----------------------------------------------------------------------
# Self-test on the golden answer (will output REWARD: 1.0 when correct)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    GOLDEN_FILE = "/home/user/the_title_on_slide_89_feels_too_airyletters_are_spaced_out_more_than_id_like_in_libreoffice_impress__golden.pptx"
    verify_character_spacing(GOLDEN_FILE)

