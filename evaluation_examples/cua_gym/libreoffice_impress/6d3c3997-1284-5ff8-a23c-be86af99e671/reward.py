"""
FINAL REWARD SCRIPT - SUCCESS
Task: Apply 'Keep lines together' to paragraphs 7–8 (prevent splitting within a paragraph).
Generated: 2025-10-17 16:15:21
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import zipfile
from lxml import etree as ET

# =============================================================
# Reward Script: Verify “Keep lines together” for Paragraphs 7–8
# =============================================================
# Task:  Apply the “Keep lines together” paragraph option to
#        paragraphs 7 and 8 so they are not split across lines.
# Verification strategy:
#   1.  Locate all <a:p> (paragraph) elements inside every slide.
#   2.  Identify paragraphs whose combined text begins with
#       “Paragraph 7” or “Paragraph 8”.
#   3.  For those paragraphs, confirm their <a:pPr> element has
#       attribute keepLines="1" (or true/True).
#   4.  Award 0.5 points for each correctly-formatted paragraph
#       for a maximum reward of 1.0.
# =============================================================

def _iter_slide_roots(pptx_path):
    """Yield (slide_name, xml_root) for each slide in the pptx."""
    with zipfile.ZipFile(pptx_path) as zf:
        for name in zf.namelist():
            if name.startswith("ppt/slides/") and name.endswith(".xml"):
                yield name, ET.fromstring(zf.read(name))


def _get_paragraph_text(p, ns):
    """Return concatenated text for a paragraph element."""
    return "".join(t.text for t in p.findall('.//a:t', ns) if t.text).strip()


def verify_keep_lines_together(pptx_path):
    # --- Progressive-scoring setup -----------------------------------------
    targets = {  # paragraph prefix -> verification status
        "Paragraph 7": False,
        "Paragraph 8": False,
    }
    per_target = 1.0 / len(targets)  # 0.5 each (progressive scoring)
    total_score = 0.0

    # --- Preliminary file-existence check (no points!) ----------------------
    if not os.path.exists(pptx_path):
        print("✗ File not found:", pptx_path)
        return 0.0

    # Namespaces used inside PPTX drawing XML
    ns = {
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    }

    # --- Core verification --------------------------------------------------
    try:
        for slide_name, root in _iter_slide_roots(pptx_path):
            for p in root.findall('.//a:p', ns):
                text = _get_paragraph_text(p, ns)
                for target in list(targets.keys()):  # copy keys for safe iteration
                    if text.startswith(target):
                        pPr = p.find('a:pPr', ns)
                        keep_attr = None if pPr is None else pPr.get('keepLines')
                        if keep_attr in {"1", "true", "True"}:
                            targets[target] = True
                            print(f"✓ {target} has keepLines attribute in {slide_name}")
                        else:
                            print(f"✗ {target} found in {slide_name} but keepLines attribute is missing")
                        break  # stop checking other targets for this paragraph
    except Exception as e:
        print("✗ Error while parsing PPTX:", e)
        return 0.0

    # --- Scoring ------------------------------------------------------------
    for ok in targets.values():
        if ok:
            total_score += per_target
    print("Score breakdown:", targets)
    print(f"Total score: {total_score}/1.0")
    return total_score

# ---------------------------------------------------------------------------
# Execute verification when run as main module
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    FILE = "/home/user/apply_keep_lines_together_to_paragraphs_78_prevent_splitting_within_a_paragraph.pptx"
    reward = verify_keep_lines_together(FILE)
    print(f"REWARD: {reward}")

