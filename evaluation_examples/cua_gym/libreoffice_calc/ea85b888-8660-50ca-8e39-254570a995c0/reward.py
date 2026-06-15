"""
Reward Script: Desktop Cleanup and Document Organization
Task ID: osworld_multi_apps_doc_desktop_organize_008
Domain: multi_apps (os + libreoffice_calc + libreoffice_writer)

Scoring Rubric:
  Component 1: Root category folders exist on Desktop (Personal, Work, Code, Media, Archives) — 0.20
  Component 2: Desktop root contains no loose files (all moved to category folders) — 0.25
  Component 3: cleanup_inventory.ods exists with correct header columns and 30+ data rows — 0.30
  Component 4: cleanup_report.odt exists in Documents with expected sections and content — 0.25
  Total: 1.00
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_desktop_organize_008'

DESKTOP = os.path.join(WORKDIR, 'Desktop')
INVENTORY_PATH = os.path.join(WORKDIR, 'cleanup_inventory.ods')
REPORT_PATH = os.path.join(WORKDIR, 'Documents', 'cleanup_report.odt')

# Expected root category folders on Desktop
EXPECTED_ROOT_FOLDERS = {'Personal', 'Work', 'Code', 'Media', 'Archives'}

# Expected inventory columns (in order, case-insensitive comparison)
EXPECTED_COLUMNS = [
    'Filename', 'Extension', 'Category', 'Subcategory',
    'Decision_Rationale', 'New_Full_Path'
]

# Expected sections in the cleanup report (keywords to verify presence)
REPORT_REQUIRED_KEYWORDS = [
    'Personal', 'Work', 'Code', 'Media', 'Archives'
]


def parse_ods_content(ods_path):
    """
    Parse an ODS file and return a list of rows (each row is a list of cell strings).
    Returns None if the file cannot be parsed.
    """
    try:
        with zipfile.ZipFile(ods_path, 'r') as z:
            with z.open("content.xml") as f:
                content = f.read().decode('utf-8')

        root = ET.fromstring(content)
        ns_table = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
        ns_text = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'

        tables = root.findall(f'.//{{{ns_table}}}table')
        if not tables:
            return None

        # Use the first table
        t = tables[0]
        rows = t.findall(f'{{{ns_table}}}table-row')

        result = []
        for row in rows:
            cells = row.findall(f'{{{ns_table}}}table-cell')
            row_values = []
            for cell in cells:
                text_elements = cell.findall(f'.//{{{ns_text}}}p')
                cell_text = ' '.join(
                    (te.text or '') for te in text_elements
                ).strip()
                row_values.append(cell_text)
            if any(v.strip() for v in row_values):
                result.append(row_values)

        return result
    except Exception as e:
        print(f"ERROR: Could not parse ODS {ods_path}: {e}")
        return None


def extract_odt_text(odt_path):
    """
    Extract all text content from an ODT file.
    Returns concatenated text string, or None on failure.
    """
    try:
        with zipfile.ZipFile(odt_path, 'r') as z:
            with z.open("content.xml") as f:
                content = f.read().decode('utf-8')

        root = ET.fromstring(content)
        ns_text = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'

        all_texts = []
        # Collect paragraphs
        for p in root.findall(f'.//{{{ns_text}}}p'):
            text = ''.join(p.itertext())
            if text.strip():
                all_texts.append(text)
        # Collect headers
        for h in root.findall(f'.//{{{ns_text}}}h'):
            text = ''.join(h.itertext())
            if text.strip():
                all_texts.append(text)

        return '\n'.join(all_texts)
    except Exception as e:
        print(f"ERROR: Could not parse ODT {odt_path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -------------------------------------------------------------------------
    # Component 1: Root category folders exist on Desktop (0.20 points)
    # The task requires creating exactly these 5 root categories:
    # Personal/, Work/, Code/, Media/, Archives/
    # These folders must be present BEFORE task = 0, AFTER task = these exist
    # -------------------------------------------------------------------------
    try:
        if not os.path.isdir(DESKTOP):
            print(f"FAIL: Component 1 — Desktop directory does not exist: {DESKTOP}")
        else:
            desktop_entries = set(os.listdir(DESKTOP))
            missing_folders = EXPECTED_ROOT_FOLDERS - desktop_entries
            found_folders = EXPECTED_ROOT_FOLDERS & desktop_entries

            if len(missing_folders) == 0:
                print(f"PASS: Component 1 — All 5 root category folders present: {sorted(found_folders)} (0.20 pts)")
                total_score += 0.20
            elif len(found_folders) >= 3:
                # Partial credit: at least 3 of 5 categories created
                partial = 0.10
                print(f"PARTIAL: Component 1 — {len(found_folders)}/5 root folders found: "
                      f"{sorted(found_folders)}, missing: {sorted(missing_folders)} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — Only {len(found_folders)}/5 root folders found: "
                      f"{sorted(found_folders)}, missing: {sorted(missing_folders)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Desktop root contains no loose files (0.25 points)
    # The task requires ALL 30 original files to be moved into category folders.
    # On initial_env the Desktop has ~32 loose files, on golden_env it should
    # only contain the 5 category directories.
    # -------------------------------------------------------------------------
    try:
        if not os.path.isdir(DESKTOP):
            print(f"FAIL: Component 2 — Desktop directory does not exist")
        else:
            desktop_entries = os.listdir(DESKTOP)
            # Count loose files (not directories) on Desktop root
            loose_files = [
                e for e in desktop_entries
                if os.path.isfile(os.path.join(DESKTOP, e))
            ]
            # Count categorized files (files inside subdirectories)
            moved_files = []
            for root_dir, dirs, files in os.walk(DESKTOP):
                if root_dir == DESKTOP:
                    continue  # Skip Desktop root itself
                for f in files:
                    moved_files.append(os.path.join(root_dir, f))

            num_loose = len(loose_files)
            num_moved = len(moved_files)

            if num_loose == 0 and num_moved >= 30:
                print(f"PASS: Component 2 — Desktop root has 0 loose files, "
                      f"{num_moved} files moved to category folders (0.25 pts)")
                total_score += 0.25
            elif num_loose == 0 and num_moved >= 20:
                partial = 0.15
                print(f"PARTIAL: Component 2 — Desktop root has 0 loose files, "
                      f"but only {num_moved}/30 files in categories ({partial} pts)")
                total_score += partial
            elif num_loose <= 5 and num_moved >= 25:
                partial = 0.12
                print(f"PARTIAL: Component 2 — Desktop root has {num_loose} loose files, "
                      f"{num_moved} files in categories ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Desktop root has {num_loose} loose files "
                      f"(expected 0), {num_moved} files in category folders")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: cleanup_inventory.ods exists with correct headers and data (0.30 points)
    # The task requires: cleanup_inventory.ods at /home/user/ with columns:
    # Filename, Extension, Category, Subcategory, Decision_Rationale, New_Full_Path
    # AND at least 30 data rows (one per original Desktop file)
    # -------------------------------------------------------------------------
    try:
        if not os.path.isfile(INVENTORY_PATH):
            print(f"FAIL: Component 3 — cleanup_inventory.ods not found at {INVENTORY_PATH}")
        else:
            rows = parse_ods_content(INVENTORY_PATH)
            if rows is None or len(rows) == 0:
                print(f"FAIL: Component 3 — Could not parse cleanup_inventory.ods or it is empty")
            else:
                # Check headers (first row)
                header_row = [h.strip() for h in rows[0]]
                missing_cols = []
                for col in EXPECTED_COLUMNS:
                    if col not in header_row:
                        # Case-insensitive check
                        col_lower = col.lower()
                        found = any(h.lower() == col_lower for h in header_row)
                        if not found:
                            missing_cols.append(col)

                data_rows = rows[1:]  # rows after header
                num_data_rows = len(data_rows)

                headers_ok = len(missing_cols) == 0
                data_ok = num_data_rows >= 30

                if headers_ok and data_ok:
                    print(f"PASS: Component 3 — cleanup_inventory.ods has all required columns "
                          f"and {num_data_rows} data rows (0.30 pts)")
                    total_score += 0.30
                elif headers_ok and num_data_rows >= 20:
                    partial = 0.20
                    print(f"PARTIAL: Component 3 — correct columns but only {num_data_rows} "
                          f"data rows (expected >=30) ({partial} pts)")
                    total_score += partial
                elif not headers_ok and data_ok:
                    partial = 0.15
                    print(f"PARTIAL: Component 3 — {num_data_rows} data rows but missing columns: "
                          f"{missing_cols} ({partial} pts)")
                    total_score += partial
                elif not headers_ok:
                    print(f"FAIL: Component 3 — missing required columns: {missing_cols}, "
                          f"found columns: {header_row}")
                else:
                    print(f"FAIL: Component 3 — only {num_data_rows} data rows (expected >=30), "
                          f"columns: {header_row}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: cleanup_report.odt exists in Documents with required content (0.25 points)
    # The task requires: cleanup_report.odt at /home/user/Documents/ with:
    # - Title/heading
    # - Summary section
    # - Per-category sections (Personal, Work, Code, Media, Archives)
    # - 5 recommendations for future organization
    # -------------------------------------------------------------------------
    try:
        if not os.path.isfile(REPORT_PATH):
            print(f"FAIL: Component 4 — cleanup_report.odt not found at {REPORT_PATH}")
        else:
            text = extract_odt_text(REPORT_PATH)
            if text is None or len(text.strip()) < 100:
                print(f"FAIL: Component 4 — cleanup_report.odt is empty or too short")
            else:
                # Check for all 5 category keywords
                categories_found = [
                    kw for kw in REPORT_REQUIRED_KEYWORDS if kw in text
                ]
                all_categories = len(categories_found) == len(REPORT_REQUIRED_KEYWORDS)

                # Check for recommendations section
                has_recommendations = (
                    'Recommendation' in text or 'recommendation' in text
                )

                # Check for summary/executive summary
                has_summary = (
                    'Summary' in text or 'summary' in text or
                    'Executive' in text or 'executive' in text
                )

                # Check minimum length (a proper report should be substantial)
                has_content = len(text) >= 500

                if all_categories and has_recommendations and has_summary and has_content:
                    print(f"PASS: Component 4 — cleanup_report.odt found with all 5 category "
                          f"sections, recommendations, and summary (0.25 pts)")
                    total_score += 0.25
                elif all_categories and (has_recommendations or has_summary):
                    partial = 0.15
                    print(f"PARTIAL: Component 4 — all categories present, "
                          f"recommendations={has_recommendations}, summary={has_summary} "
                          f"({partial} pts)")
                    total_score += partial
                elif len(categories_found) >= 3:
                    partial = 0.10
                    print(f"PARTIAL: Component 4 — {len(categories_found)}/5 categories found, "
                          f"recommendations={has_recommendations} ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 — only {len(categories_found)}/5 categories found "
                          f"in report: {categories_found}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Entrypoint
if not os.path.isdir(DESKTOP):
    print(f"CRITICAL: Desktop directory not found: {DESKTOP}")
    print("REWARD: 0.0")
else:
    verify_task()
