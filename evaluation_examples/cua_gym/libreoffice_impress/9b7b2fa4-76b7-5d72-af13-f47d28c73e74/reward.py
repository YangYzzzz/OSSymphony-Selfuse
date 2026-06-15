"""
FINAL REWARD SCRIPT - SUCCESS
Task: Prevent rows in Table 1 from splitting across pages.
Generated: 2025-10-17 15:49:22
Status: success
Model: azure-o3
Total Steps: 12
"""

import os
import zipfile
import re
import xml.etree.ElementTree as ET


def verify_table_rows_no_split(file_path: str) -> float:
    """Verify that every row in the first table (Table 1) has the
    <a:noSplit/> flag, which prevents the row from splitting across pages.

    Scoring (progressive):
        • 0.0  – File missing / no table found / fatal error
        • 0.2  – A table is found (prerequisite for further checks)
        • +0.8 × (ratio of rows containing a:noSplit)
        → 1.0 only when ALL rows in Table 1 have a:noSplit element.
    """

    max_score = 1.0
    score = 0.0

    if not os.path.exists(file_path):
        print("✗ File not found:", file_path)
        return 0.0

    try:
        with zipfile.ZipFile(file_path) as z:
            # Collect slide XML files and sort by slide number
            slide_xml_files = [f for f in z.namelist()
                               if f.startswith("ppt/slides/slide") and f.endswith(".xml")]

            def slide_number(name: str) -> int:
                m = re.search(r"slide(\d+)\.xml", name)
                return int(m.group(1)) if m else 10 ** 9

            slide_xml_files.sort(key=slide_number)

            ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}

            table_rows = None
            table_slide_name = None
            # Find the first table across slides (Table 1)
            for slide_name in slide_xml_files:
                slide_xml = z.read(slide_name)
                root = ET.fromstring(slide_xml)
                tbl = root.find(".//a:tbl", ns)
                if tbl is not None:
                    table_rows = tbl.findall(".//a:tr", ns)
                    table_slide_name = slide_name
                    break

            if table_rows is None:
                print("✗ No tables found in presentation – cannot verify task")
                return 0.0

            print(f"✓ Found table in {table_slide_name} with {len(table_rows)} rows")
            score += 0.2  # Table located – prerequisite met

            total_rows = len(table_rows)
            rows_with_nosplit = 0

            for idx, tr in enumerate(table_rows, start=1):
                tr_pr = tr.find("a:trPr", ns)
                if tr_pr is not None and tr_pr.find("a:noSplit", ns) is not None:
                    rows_with_nosplit += 1
                    print(f"  ✓ Row {idx}: noSplit present")
                else:
                    print(f"  ✗ Row {idx}: noSplit NOT present")

            ratio = rows_with_nosplit / total_rows if total_rows else 0
            print(f"Rows with noSplit: {rows_with_nosplit}/{total_rows} ({ratio*100:.1f}%)")

            # Award remaining points proportionally to the ratio
            score += 0.8 * ratio
            final_score = round(min(score, max_score), 2)
            print(f"Calculated score: {final_score}")
            return final_score

    except Exception as exc:
        print("✗ Error processing file:", exc)
        return 0.0


if __name__ == "__main__":
    FILE_PATH = "/home/user/prevent_rows_in_table_1_from_splitting_across_pages.pptx"
    reward = verify_table_rows_no_split(FILE_PATH)
    print(f"REWARD: {reward}")
