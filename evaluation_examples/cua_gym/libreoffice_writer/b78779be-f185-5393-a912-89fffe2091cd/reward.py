"""
FINAL REWARD SCRIPT - SUCCESS
Task: Table 1 keeps breaking mid-row when the content flows onto the next page, and it looks messy. In LibreOffice Writer, how do I force every row in that specific table to stay together on one page instead of getting split?
Generated: 2025-09-10 18:40:10
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
import zipfile
from lxml import etree as ET


def verify_table_row_no_split(docx_path: str) -> float:
    """Verify that every row in the FIRST table of the document
    has the <w:cantSplit/> property (row keep-together).

    Returns a progressive score between 0.0-1.0 based on the
    proportion of rows that are protected from splitting.
    """

    print(f"Verifying table row split settings in: {docx_path}")

    # ---------- 0.  Preliminary checks (NO points awarded) ----------
    if not os.path.exists(docx_path):
        print("✗ File not found – task not completed")
        return 0.0  # Cannot continue

    # ---------- 1.  Load document.xml from DOCX ----------
    try:
        with zipfile.ZipFile(docx_path) as z:
            if "word/document.xml" not in z.namelist():
                print("✗ document.xml not present in DOCX – invalid file")
                return 0.0
            doc_xml = z.read("word/document.xml")
    except Exception as e:
        print(f"✗ Error opening DOCX: {e}")
        return 0.0

    # ---------- 2.  Parse XML ----------
    try:
        root = ET.fromstring(doc_xml)
    except Exception as e:
        print(f"✗ Error parsing XML: {e}")
        return 0.0

    NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    # ---------- 3.  Locate tables ----------
    tables = root.findall(".//w:tbl", namespaces=NS)
    if not tables:
        print("✗ No tables found in document – requirement unmet")
        return 0.0

    print(f"✓ Found {len(tables)} table(s) in document")

    # We are asked to check TABLE 1 specifically (first table in the file)
    target_table = tables[0]

    rows = target_table.findall(".//w:tr", namespaces=NS)
    total_rows = len(rows)
    print(f"  Table 1 has {total_rows} row(s)")

    if total_rows == 0:
        print("✗ Table 1 contains no rows – requirement unmet")
        return 0.0

    # ---------- 4.  Evaluate <w:cantSplit/> on each row ----------
    cant_split_rows = 0
    for idx, row in enumerate(rows, start=1):
        trPr = row.find("./w:trPr", namespaces=NS)
        has_cant_split = (
            trPr is not None and trPr.find("./w:cantSplit", namespaces=NS) is not None
        )
        if has_cant_split:
            cant_split_rows += 1
        else:
            print(f"   Row {idx}: ✗ cantSplit NOT set – row may break across pages")

    print(f"  Rows with cantSplit: {cant_split_rows}/{total_rows}")

    # ---------- 5.  Progressive scoring ----------
    ratio = cant_split_rows / total_rows  # 0.0 → 1.0

    # Round only for readability (does NOT affect pass/fail logic)
    score = round(ratio, 2)

    # Ensure perfect score only when EVERY row is protected
    if ratio == 1.0:
        score = 1.0

    print(f"Computed score: {score}")
    return score


if __name__ == "__main__":
    # Path provided by the grading environment
    DOCX_PATH = \
        "/home/user/table_1_keeps_breaking_mid_row_when_the_content_flows_onto_the_next_page_and_it_looks_messy_in_libre.docx"

    reward = verify_table_row_no_split(DOCX_PATH)
    print(f"REWARD: {reward}")
