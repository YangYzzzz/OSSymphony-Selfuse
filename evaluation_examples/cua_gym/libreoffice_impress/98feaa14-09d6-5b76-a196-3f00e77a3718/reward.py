"""
FINAL REWARD SCRIPT - SUCCESS
Task: Create a right tab stop with dashed leader at 13.5 cm in paragraph 1 and press Tab once.
Generated: 2025-10-17 16:16:48
Status: success
Model: azure-o3
Total Steps: 18
"""

import os
import zipfile
from lxml import etree

def verify_tab_stop(file_path: str) -> float:
    """Verify a right-aligned tab stop with a dashed (hyphen) leader at 13.5 cm
    in the presentation’s first paragraph (or anywhere in slide 1).

    Returns a progressive score between 0.0 and 1.0; prints detailed
    verification steps and finally prints "REWARD: X.X".
    """

    print(f"Checking presentation: {file_path}")

    # ----- Constants ---------------------------------------------------------
    EXPECTED_CM = 13.5                 # required tab stop position in cm
    EMU_PER_CM  = 360_000              # OOXML uses EMUs for tab positions
    EXPECTED_POS = int(EXPECTED_CM * EMU_PER_CM)  # 4 860 000 EMUs
    TOLERANCE   = round(EXPECTED_POS * 0.02)      # ±2 %  ≈ 0.27 cm tolerance

    # ----- Preliminary checks ------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File not found")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------------
    score               = 0.0  # progressive score accumulator
    position_match      = False
    alignment_match     = False
    leader_match        = False

    try:
        with zipfile.ZipFile(file_path) as zf:
            slide_files = [f for f in zf.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
            print(f"Found {len(slide_files)} slide XML files")

            ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}

            for slide_file in slide_files:
                root = etree.fromstring(zf.read(slide_file))
                # Locate all <a:tab> definitions inside <a:tabLst>
                tab_nodes = root.xpath('.//a:pPr/a:tabLst/a:tab', namespaces=ns)
                if tab_nodes:
                    print(f"  ✓ {len(tab_nodes)} tab stop(s) found in {slide_file}")

                for tab in tab_nodes:
                    # ---- Position check ------------------------------------
                    try:
                        pos_val = int(tab.get('pos'))
                        if abs(pos_val - EXPECTED_POS) <= TOLERANCE:
                            position_match = True
                    except (TypeError, ValueError):
                        pass

                    # ---- Alignment check -----------------------------------
                    if tab.get('algn') == 'r':
                        alignment_match = True

                    # ---- Leader check --------------------------------------
                    # In OOXML, dashed leader is encoded as leader="hyphen"
                    if tab.get('leader') == 'hyphen':
                        leader_match = True

        # ------------------------ Scoring ------------------------------------
        if position_match:
            print("  ✓ Tab stop position correct (13.5 cm)")
            score += 0.6
        else:
            print("  ✗ No tab stop at 13.5 cm found")

        if alignment_match:
            print("  ✓ Right alignment detected")
            score += 0.2
        else:
            print("  ✗ Right alignment not set")

        if leader_match:
            print("  ✓ Dashed (hyphen) leader detected")
            score += 0.2
        else:
            print("  ✗ Dashed leader not detected")

    except Exception as e:
        print(f"✗ Error during verification: {e}")
        print("REWARD: 0.0")
        return 0.0

    final_score = min(score, 1.0)
    print(f"REWARD: {final_score}")
    return final_score

# ---------------------------------------------------------------------------
# When run as a script, execute verification on the expected file path
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    TEST_PATH = "/home/user/create_a_right_tab_stop_with_dashed_leader_at_135_cm_in_paragraph_1_and_press_tab_once.pptx"
    verify_tab_stop(TEST_PATH)
