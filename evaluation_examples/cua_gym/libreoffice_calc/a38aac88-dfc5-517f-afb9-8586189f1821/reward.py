"""
Reward Script: stats_summary.odt creation from JSON data in data_report.odt
Task ID: osworld_multi_apps_media_doc_edit_010
Domain: libreoffice_writer (ODT documents)
Scoring:
  - Component 1: stats_summary.odt exists with a table of 21 rows (1 header + 20 data rows) [0.25 pts]
  - Component 2: Table has alternating row shading (2+ distinct background colors for even/odd rows) [0.20 pts]
  - Component 3: Summary paragraph contains computed stats for CPU_Usage (avg=54.38, max=73.1, min=38.2) [0.20 pts]
  - Component 4: Summary paragraph contains computed stats for Memory_Usage (avg=7.71, max=10.1, min=5.9) [0.15 pts]
  - Component 5: Document contains an embedded chart/image (matplotlib PNG) [0.10 pts]
  - Component 6: PDF exported (stats_summary.pdf exists and is non-empty) [0.10 pts]
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/documents'
TASK_ID = 'osworld_multi_apps_media_doc_edit_010'

ODT_PATH = os.path.join(WORKDIR, 'stats_summary.odt')
PDF_PATH = os.path.join(WORKDIR, 'stats_summary.pdf')

# XML namespaces used in ODF content
NS = {
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}


def get_odt_content(odt_path):
    """Load content.xml from an ODT file (ZIP archive)."""
    with zipfile.ZipFile(odt_path) as z:
        content = z.read('content.xml').decode('utf-8')
    return ET.fromstring(content)


def get_cell_style_backgrounds(root):
    """
    Extract background colors for each table cell style in content.xml.
    Returns a dict: style_name -> background_color_hex_string (or None).
    """
    bg_map = {}
    for style_elem in root.findall('.//style:style', NS):
        name = style_elem.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name', '')
        for child in style_elem:
            bg = child.get(
                '{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}background-color', None
            )
            if bg is not None:
                bg_map[name] = bg
    return bg_map


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: stats_summary.odt must exist
    if not os.path.exists(ODT_PATH):
        print(f"CRITICAL: stats_summary.odt not found at {ODT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load content from the ODT file
    try:
        root = get_odt_content(ODT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse stats_summary.odt: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: Table with 21 rows (1 header + 20 data rows) (0.25 points)
    # The task requires extracting 20 JSON records and creating a formatted table.
    # Initial env has no stats_summary.odt at all, so this fails on initial.
    # -------------------------------------------------------------------------
    try:
        tables = root.findall('.//table:table', NS)
        if len(tables) >= 1:
            first_table = tables[0]
            rows = first_table.findall('.//table:table-row', NS)
            row_count = len(rows)
            if row_count == 21:
                print(f"PASS: Component 1 — Table has {row_count} rows (1 header + 20 data rows) (0.25 pts)")
                total_score += 0.25
            elif row_count >= 5:
                # Partial credit: table exists with some data rows
                print(f"PARTIAL: Component 1 — Table has {row_count} rows (expected 21); partial credit withheld")
            else:
                print(f"FAIL: Component 1 — Table has {row_count} rows, expected 21")
        else:
            print(f"FAIL: Component 1 — No tables found in stats_summary.odt")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Alternating row shading (0.20 points)
    # Even rows should have a different background than odd rows.
    # The golden file uses 3 distinct styles: header (blue), odd rows (light blue),
    # even rows (white). At minimum, we need 2 distinct non-None backgrounds across rows.
    # -------------------------------------------------------------------------
    try:
        bg_map = get_cell_style_backgrounds(root)
        tables = root.findall('.//table:table', NS)
        if tables:
            first_table = tables[0]
            rows = first_table.findall('.//table:table-row', NS)
            # Collect distinct cell styles used in the data rows (skip header row 0)
            style_to_bg = {}
            for row_idx, row in enumerate(rows[1:], 1):  # data rows only
                cells = row.findall('.//table:table-cell', NS)
                if cells:
                    cell_style = cells[0].get(
                        '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}style-name', None
                    )
                    if cell_style and cell_style in bg_map:
                        style_to_bg[cell_style] = bg_map[cell_style]

            distinct_bgs = set(style_to_bg.values())
            if len(distinct_bgs) >= 2:
                print(f"PASS: Component 2 — Alternating row shading found, {len(distinct_bgs)} distinct background colors: {distinct_bgs} (0.20 pts)")
                total_score += 0.20
            elif len(distinct_bgs) == 1:
                print(f"FAIL: Component 2 — Only 1 background color found across all rows: {distinct_bgs}. Expected alternating shading.")
            else:
                print(f"FAIL: Component 2 — No background color styles found on table rows. Expected alternating shading.")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Summary stats for CPU_Usage present (0.20 points)
    # Expected: average=54.38, max=73.1 (on 2024-06-15), min=38.2 (on 2024-03-15)
    # We check for the presence of these key values in the paragraph text.
    # -------------------------------------------------------------------------
    try:
        paragraphs = root.findall('.//text:p', NS)
        all_text = ' '.join(''.join(p.itertext()) for p in paragraphs)

        cpu_avg_present = '54.38' in all_text
        cpu_max_present = '73.1' in all_text
        cpu_min_present = '38.2' in all_text

        if cpu_avg_present and cpu_max_present and cpu_min_present:
            print(f"PASS: Component 3 — CPU_Usage stats found: avg=54.38, max=73.1, min=38.2 (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not cpu_avg_present:
                missing.append('avg=54.38')
            if not cpu_max_present:
                missing.append('max=73.1')
            if not cpu_min_present:
                missing.append('min=38.2')
            print(f"FAIL: Component 3 — CPU_Usage stats missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Summary stats for Memory_Usage present (0.15 points)
    # Expected: average=7.71, max=10.1 (on 2024-07-15), min=5.9 (on 2024-03-15)
    # -------------------------------------------------------------------------
    try:
        paragraphs = root.findall('.//text:p', NS)
        all_text = ' '.join(''.join(p.itertext()) for p in paragraphs)

        mem_avg_present = '7.71' in all_text
        mem_max_present = '10.1' in all_text
        mem_min_present = '5.9' in all_text

        if mem_avg_present and mem_max_present and mem_min_present:
            print(f"PASS: Component 4 — Memory_Usage stats found: avg=7.71, max=10.1, min=5.9 (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not mem_avg_present:
                missing.append('avg=7.71')
            if not mem_max_present:
                missing.append('max=10.1')
            if not mem_min_present:
                missing.append('min=5.9')
            print(f"FAIL: Component 4 — Memory_Usage stats missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -------------------------------------------------------------------------
    # Component 5: Embedded chart/image (PNG) inserted in document (0.10 points)
    # The task requires inserting a matplotlib chart as a PNG image.
    # Verified by checking for image relationships in the ODT ZIP archive.
    # -------------------------------------------------------------------------
    try:
        with zipfile.ZipFile(ODT_PATH) as z:
            namelist = z.namelist()

        png_files = [f for f in namelist if f.endswith('.png') and 'Thumbnails' not in f]

        if len(png_files) >= 1:
            print(f"PASS: Component 5 — Embedded PNG image found in document: {png_files} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — No embedded PNG image found in stats_summary.odt. Expected a matplotlib chart.")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # -------------------------------------------------------------------------
    # Component 6: PDF exported (0.10 points)
    # The task requires exporting the document as PDF.
    # -------------------------------------------------------------------------
    try:
        if os.path.exists(PDF_PATH):
            pdf_size = os.path.getsize(PDF_PATH)
            if pdf_size > 10000:  # Must be a real PDF, not an empty file
                print(f"PASS: Component 6 — PDF exported at {PDF_PATH} (size: {pdf_size} bytes) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — PDF exists but is too small ({pdf_size} bytes), may be invalid")
        else:
            print(f"FAIL: Component 6 — PDF not found at {PDF_PATH}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # -------------------------------------------------------------------------
    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if __name__ == '__main__':
    verify_task()
