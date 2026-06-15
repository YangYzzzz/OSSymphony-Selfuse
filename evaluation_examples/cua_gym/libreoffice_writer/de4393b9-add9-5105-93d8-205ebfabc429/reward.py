"""
FINAL REWARD SCRIPT - SUCCESS
Task: For Table 1 I only want the inside grid showing—no outer box at all. What steps in LibreOffice Writer will let me drop the outside border but leave every internal cell line visible?
Generated: 2025-09-10 18:19:28
Status: success
Model: azure-o3
Total Steps: 17
"""

import os
import glob
import zipfile
import xml.etree.ElementTree as ET


def verify_task(directory: str = "/home/user") -> float:
    """Reward-script for the LibreOffice-Writer task:

    Task:  In *at least one* document the outer border of **Table 1** must be
    removed while every *internal* grid line (horizontal & vertical) remains
    visible.

    Scoring (progressive):
      • 0.5  – all four outer borders removed (val = nil/none or size = 0)
      • 0.5  – both insideH and insideV borders still visible (NOT nil/none/0)
      • 1.0  – both conditions met (perfect completion)

    The script inspects every .docx file in the given directory (ignoring
    temporary lock files).  It examines each table’s <w:tblBorders> definition
    inside *word/document.xml*.  The highest score across all tables in all
    documents is returned.
    """

    print("Starting verification of LibreOffice Writer task (table border formatting)…")

    # Collect .docx candidates (skip Office lock files like ~$*)
    candidates = [f for f in glob.glob(os.path.join(directory, "*.docx"))
                  if not os.path.basename(f).startswith("~$")]

    if not candidates:
        print("✗ No .docx files found in directory.")
        print("REWARD: 0.0")
        return 0.0  # nothing to grade

    # WordprocessingML namespace
    NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    def evaluate_table(borders: dict) -> tuple[float, bool, bool]:
        """Return (score, outer_removed, internal_present) for one table."""
        # --- check outer borders -------------------------------------------
        outer_removed = True
        for side in ("top", "left", "bottom", "right"):
            attrs = borders.get(side)
            if attrs is None:
                # missing definition usually means default visible border
                outer_removed = False
                continue
            val = attrs.get(f"{{{NS['w']}}}val", "")
            sz = attrs.get(f"{{{NS['w']}}}sz", "1")
            if val not in ("nil", "none") and not (sz == "0"):
                outer_removed = False

        # --- check internal borders ----------------------------------------
        internal_present = True
        for side in ("insideH", "insideV"):
            attrs = borders.get(side)
            if attrs is None:
                internal_present = False
                continue
            val = attrs.get(f"{{{NS['w']}}}val", "")
            sz = attrs.get(f"{{{NS['w']}}}sz", "0")
            if val in ("nil", "none") or sz == "0":
                internal_present = False

        # scoring                                                                
        score = 0.0
        if outer_removed:
            score += 0.5
        if internal_present:
            score += 0.5
        return score, outer_removed, internal_present

    best_score = 0.0

    # ---------------------------------------------------------------------
    for docx_path in candidates:
        print(f"Analyzing document: {os.path.basename(docx_path)}")
        try:
            with zipfile.ZipFile(docx_path) as z:
                if "word/document.xml" not in z.namelist():
                    print("  ✗ document.xml not found – skipping.")
                    continue

                root = ET.fromstring(z.read("word/document.xml"))
                tables = root.findall(".//w:tbl", NS)
                if not tables:
                    print("  ✗ No tables in document.")
                    continue

                for idx, tbl in enumerate(tables, start=1):
                    tblPr = tbl.find("./w:tblPr", NS)
                    if tblPr is None:
                        continue
                    tblBorders = tblPr.find("./w:tblBorders", NS)
                    if tblBorders is None:
                        continue

                    # Gather border attributes for six sides
                    borders = {}
                    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
                        el = tblBorders.find(f"w:{side}", NS)
                        if el is not None:
                            borders[side] = el.attrib

                    score, out_removed, in_present = evaluate_table(borders)
                    print(f"    Table {idx}: outer_removed={out_removed}, internal_present={in_present}, score={score}")

                    best_score = max(best_score, score)
                    if best_score == 1.0:
                        break  # perfect score reached – no need to continue
        except Exception as exc:
            print(f"  ✗ Error processing {docx_path}: {exc}")

        if best_score == 1.0:
            break

    print(f"Final best score across documents: {best_score}")
    print(f"REWARD: {best_score}")
    return best_score


if __name__ == "__main__":
    verify_task("/home/user")

