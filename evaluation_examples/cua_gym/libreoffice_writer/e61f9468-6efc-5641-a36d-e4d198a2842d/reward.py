"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Writer, the text in my first table is practically hugging the borders. How can I give each cell in Table 1 exactly 0.15 cm of padding on all four sides so everything has a little breathing room?
Generated: 2025-09-10 16:52:19
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import zipfile
from lxml import etree


def verify_table_padding(file_path: str, target_cm: float = 0.15) -> float:
    """Verify that every cell in the first table has exactly the requested
    padding on all four sides.

    Parameters
    ----------
    file_path : str
        Path to the Writer/Word document (.docx).
    target_cm : float, optional
        Desired padding in centimetres on each side, by default ``0.15``.

    Returns
    -------
    float
        Progressive score between 0.0 and 1.0 representing task completion.
    """

    # Conversion helpers ----------------------------------------------------
    # DOCX stores table cell margins in twips *if* the type is "dxa".
    # 1 twip  = 1/20 pt = 1/1440 inch  (1 inch = 2.54 cm)
    # => twips = cm * 1440 / 2.54
    target_twips = int(round(target_cm * 1440 / 2.54))
    tolerance = 1  # allow ±1 twip tolerance (≈0.00018 cm)

    print(f"Target padding: {target_cm} cm  ->  {target_twips} twips (±{tolerance})")

    # ----------------------------------------------------------------------
    # 1. Basic file checks (NO POINTS – prerequisite only)
    # ----------------------------------------------------------------------
    if not os.path.exists(file_path):
        print(f"✗ File does not exist: {file_path}")
        return 0.0
    if not file_path.lower().endswith(".docx"):
        print("✗ Only .docx verification implemented for this task")
        return 0.0

    # ----------------------------------------------------------------------
    # 2. Load document.xml from the DOCX package
    # ----------------------------------------------------------------------
    try:
        with zipfile.ZipFile(file_path, "r") as docx_zip:
            document_xml = docx_zip.read("word/document.xml")
    except Exception as exc:
        print(f"✗ Unable to open DOCX XML: {exc}")
        return 0.0

    # ----------------------------------------------------------------------
    # 3. Locate the first table in the document
    # ----------------------------------------------------------------------
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    root = etree.fromstring(document_xml)
    first_table = root.find(".//w:tbl", ns)

    score = 0.0  # progressive score (max 1.0)

    if first_table is None:
        print("✗ No table found in the document – 0 points")
        return 0.0

    print("✓ Found the first table")
    score += 0.4  # 40 % for correctly identifying / keeping the table

    # ----------------------------------------------------------------------
    # 4. Determine default cell margins set at the table level (tblCellMar)
    #    These serve as fallback for individual cells without explicit tcMar
    # ----------------------------------------------------------------------
    def get_side_value(parent, side):
        """Helper: extract w attribute for a given <w:side> element."""
        el = parent.find(f"w:{side}", ns)
        if el is not None and f"{{{ns['w']}}}w" in el.attrib:
            try:
                return int(el.attrib[f"{{{ns['w']}}}w"])
            except ValueError:
                pass
        return None

    table_defaults = {}
    tblPr = first_table.find("w:tblPr", ns)
    if tblPr is not None:
        tblCellMar = tblPr.find("w:tblCellMar", ns)
        if tblCellMar is not None:
            for side in ("top", "bottom", "left", "right"):
                val = get_side_value(tblCellMar, side)
                if val is not None:
                    table_defaults[side] = val

    if table_defaults:
        print(f"Default <tblCellMar> detected: {table_defaults}")
    else:
        print("No <tblCellMar> defaults – relying solely on individual cell margins")

    # ----------------------------------------------------------------------
    # 5. Check every cell inside the first table
    # ----------------------------------------------------------------------
    cells = first_table.findall(".//w:tc", ns)
    if not cells:
        print("✗ No cells found inside the first table – cannot verify padding")
        return score  # return whatever we had so far

    total_sides = len(cells) * 4  # 4 sides per cell
    correct_sides = 0

    for tc in cells:
        tcPr = tc.find("w:tcPr", ns)
        tcMar = tcPr.find("w:tcMar", ns) if tcPr is not None else None

        for side in ("top", "bottom", "left", "right"):
            # Priority: individual <tcMar> side -> default <tblCellMar> side
            val = None
            if tcMar is not None:
                val = get_side_value(tcMar, side)
            if val is None:
                val = table_defaults.get(side)

            if val is not None and abs(val - target_twips) <= tolerance:
                correct_sides += 1

    ratio = correct_sides / total_sides if total_sides else 0.0
    print(
        f"Padding verification: {correct_sides}/{total_sides} sides correct "
        f"({ratio:.2%})"
    )

    # Up to 60 % of the score allocated proportionally to how many sides match
    score += 0.6 * ratio
    final_score = min(score, 1.0)

    print(f"Final Score: {final_score}")
    return final_score


# --------------------------------------------------------------------------
# AUTO-RUN VERIFICATION WHEN SCRIPT IS EXECUTED DIRECTLY
# --------------------------------------------------------------------------
if __name__ == "__main__":
    # Attempt to locate the target document in the user's home directory
    search_dir = "/home/user"
    candidate = None
    for fname in os.listdir(search_dir):
        if fname.lower().endswith(".docx"):
            candidate = os.path.join(search_dir, fname)
            break

    if candidate is None:
        print("✗ No .docx file found to verify – REWARD: 0.0")
    else:
        print(f"Verifying file: {candidate}")
        reward_value = verify_table_padding(candidate)
        print(f"REWARD: {reward_value}")

