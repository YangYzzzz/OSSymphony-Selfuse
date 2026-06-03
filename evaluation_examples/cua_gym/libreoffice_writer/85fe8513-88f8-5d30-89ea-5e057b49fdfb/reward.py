"""
FINAL REWARD SCRIPT - SUCCESS
Task: The content in my first table looks jammed up against the lines. In LibreOffice Writer, what steps do I follow to add a uniform 0.15 cm cushion on every side of each cell in “Table 1”?
Generated: 2025-09-10 18:10:59
Status: success
Model: azure-o3
Total Steps: 16
"""

import zipfile
from lxml import etree
import os

EXPECTED_MARGIN_TWIPS = 85  # 0.15 cm ≈ 85 twips (1 twip = 1/1440 inch)
TOLERANCE_TWIPS = 5         # Allow small rounding differences


def _extract_margin_values(mar_parent):
    """Return a dict with integer twip values for each side found in a <w:tcMar> or <w:tblCellMar>."""
    values = {}
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for side in ("top", "bottom", "left", "right"):
        elem = mar_parent.find(f"./w:{side}", namespaces=ns)
        if elem is not None:
            # margin value can be stored in either w:w or w:val attribute
            val = (
                elem.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w")
                or elem.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val")
            )
            if val is not None:
                try:
                    values[side] = int(val)
                except ValueError:
                    pass  # ignore non-numeric values
    return values


def verify_uniform_cell_padding(docx_path):
    """Verify that Table 1 (first table) has a uniform 0.15 cm padding on every cell side."""
    if not os.path.exists(docx_path):
        print(f"✗ File does not exist: {docx_path}")
        return 0.0

    try:
        # ------------------------------------------------------------------
        # 1) Load document XML ------------------------------------------------
        # ------------------------------------------------------------------
        with zipfile.ZipFile(docx_path) as z:
            doc_xml = z.read("word/document.xml")
        root = etree.fromstring(doc_xml)
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

        # ------------------------------------------------------------------
        # 2) Locate first table (Table 1) ------------------------------------
        # ------------------------------------------------------------------
        tables = root.findall('.//w:tbl', namespaces=ns)
        if not tables:
            print("✗ No tables found in document")
            return 0.0  # no progress if required table missing
        first_table = tables[0]

        # ------------------------------------------------------------------
        # 3) Collect margin data --------------------------------------------
        #    LibreOffice can store cell margins at either table level
        #    (<w:tblCellMar>) or individual cell level (<w:tcMar>). We
        #    therefore check both and use whichever is present.
        # ------------------------------------------------------------------
        table_level_mar = None
        tbl_pr = first_table.find('./w:tblPr', namespaces=ns)
        if tbl_pr is not None:
            tbl_cell_mar = tbl_pr.find('./w:tblCellMar', namespaces=ns)
            if tbl_cell_mar is not None:
                table_level_mar = _extract_margin_values(tbl_cell_mar)

        cell_level_mars = []
        for tc_mar in first_table.findall('.//w:tcMar', namespaces=ns):
            cell_level_mars.append(_extract_margin_values(tc_mar))

        # Decide which data source to evaluate
        if table_level_mar:
            print("✓ Using table-level <w:tblCellMar> for evaluation")
            margin_sets = [table_level_mar]
        elif cell_level_mars:
            print("✓ Using individual <w:tcMar> elements for evaluation")
            margin_sets = cell_level_mars
        else:
            print("✗ No margin information found for Table 1")
            return 0.0  # task clearly not done

        # ------------------------------------------------------------------
        # 4) Evaluate margins ------------------------------------------------
        # ------------------------------------------------------------------
        # a) Completeness ─ each examined margin set must specify all 4 sides
        completeness_ok = all(
            all(side in m for side in ("top", "bottom", "left", "right"))
            for m in margin_sets
        )
        print("✓ Margins specified for all four sides" if completeness_ok else "✗ Missing some side margins")

        # Gather all numerical values for further checks
        all_values = [m[side] for m in margin_sets for side in m]

        # b) Uniformity ─ all sides (and all cells) should have identical value
        if all_values:
            uniform_ok = max(all_values) - min(all_values) <= TOLERANCE_TWIPS
        else:
            uniform_ok = False
        print("✓ Margins are uniformly set" if uniform_ok else "✗ Margins are not uniform across sides/cells")

        # c) Accuracy ─ value should be close to 0.15 cm (≈85 twips)
        expected_ok = all(abs(v - EXPECTED_MARGIN_TWIPS) <= TOLERANCE_TWIPS for v in all_values)
        print("✓ Margins ≈ 0.15 cm" if expected_ok else "✗ Margins are not 0.15 cm")

        # ------------------------------------------------------------------
        # 5) Progressive scoring --------------------------------------------
        # ------------------------------------------------------------------
        score = 0.0
        if completeness_ok:
            score += 0.4
        if uniform_ok:
            score += 0.3
        if expected_ok:
            score += 0.3
        score = min(score, 1.0)

        print(f"Total score: {score}")
        return score

    except Exception as e:
        print(f"✗ Error during verification: {e}")
        return 0.0


if __name__ == "__main__":
    DOCX_PATH = "/home/user/the_content_in_my_first_table_looks_jammed_up_against_the_lines_in_libreoffice_writer_what_steps_do_.docx"
    reward = verify_uniform_cell_padding(DOCX_PATH)
    print(f"REWARD: {reward}")

