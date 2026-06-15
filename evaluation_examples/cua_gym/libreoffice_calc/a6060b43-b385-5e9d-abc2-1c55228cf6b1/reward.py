"""
Reward Script: Create nlp_faculty.ods spreadsheet with NLP researcher data
Task ID: osworld_multi_apps_web_scholar_003
Domain: libreoffice_calc (ODS format)
Scoring:
  - Component 1: File nlp_faculty.ods exists on Desktop (0.2 pts)
  - Component 2: Correct column headers present (0.2 pts)
  - Component 3: All 5 researchers present with correct data (0.4 pts)
  - Component 4: Data sorted by H_Index descending (0.1 pts)
  - Component 5: Header row has bold formatting (0.1 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_scholar_003'
FILE_PATH = '/home/user/Desktop/nlp_faculty.ods'

# ODS XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}

EXPECTED_HEADERS = ['Name', 'Institution', 'H_Index', 'Citations', 'Specialty']
EXPECTED_RESEARCHERS = [
    ('Christopher Manning', 'Stanford NLP Group', 112, 'NLP, Parsing'),
    ('Noah Smith', 'University of Washington', 70, 'NLP, Computational Social Science'),
    ('Regina Barzilay', 'MIT', 58, 'NLP, Medical AI'),
    ('Rada Mihalcea', 'University of Michigan', 54, 'NLP, Computational Linguistics'),
    ('Lillian Lee', 'Cornell University', 47, 'NLP, Sentiment Analysis'),
]
# Sorted by H-Index descending
EXPECTED_ORDER = [112, 70, 58, 54, 47]


def read_ods_content(filepath):
    """Read ODS file content.xml and return parsed XML tree."""
    with zipfile.ZipFile(filepath, 'r') as z:
        if 'content.xml' not in z.namelist():
            raise ValueError("No content.xml in ODS archive")
        content_xml = z.read('content.xml').decode('utf-8')
    return ET.fromstring(content_xml), content_xml


def get_cell_text(cell_elem):
    """Extract text value from a table-cell element."""
    text_p = cell_elem.find('.//text:p', NS)
    if text_p is not None and text_p.text:
        return text_p.text.strip()
    return None


def get_bold_styles(content_xml_str):
    """Parse style definitions and return a set of style names that are bold."""
    root = ET.fromstring(content_xml_str)
    bold_styles = set()
    auto_styles = root.find('.//office:automatic-styles', NS)
    if auto_styles is None:
        return bold_styles
    for style_elem in auto_styles.findall('style:style', NS):
        style_name = style_elem.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name')
        text_props = style_elem.find('style:text-properties', NS)
        if text_props is not None:
            fw = text_props.get('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}font-weight')
            if fw == 'bold':
                bold_styles.add(style_name)
    return bold_styles


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File exists on Desktop (0.2 points)
    # This FAILS on initial_env (empty Desktop) and PASSES on golden_env
    try:
        if os.path.exists(FILE_PATH):
            print(f"PASS: Component 1 — nlp_faculty.ods exists on Desktop (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — nlp_faculty.ods NOT found at {FILE_PATH}")
            # File doesn't exist — remaining checks are pointless
            final_score = min(total_score, 1.0)
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {final_score}")
            return final_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load ODS content
    try:
        root, content_xml_str = read_ods_content(FILE_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot read ODS file {FILE_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get rows
    all_rows = []
    table_elem = root.find('.//table:table', NS)
    if table_elem is not None:
        for row_elem in table_elem.findall('table:table-row', NS):
            cells = row_elem.findall('table:table-cell', NS)
            row_data = [get_cell_text(c) for c in cells]
            # Remove trailing None cells
            while row_data and row_data[-1] is None:
                row_data.pop()
            if row_data:  # skip empty rows
                all_rows.append((row_elem, row_data))

    if len(all_rows) < 2:
        print(f"FAIL: File has fewer than 2 rows (found {len(all_rows)} rows)")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    header_row_elem, header_values = all_rows[0]
    data_rows = [(elem, vals) for elem, vals in all_rows[1:]]

    # Component 2: Correct column headers (0.2 points)
    # FAILS on initial_env (no file) — PASSES on golden_env
    try:
        # Check header count and names
        headers_match = (
            len(header_values) >= 5 and
            header_values[0] == 'Name' and
            header_values[1] == 'Institution' and
            header_values[2] == 'H_Index' and
            header_values[3] == 'Citations' and
            header_values[4] == 'Specialty'
        )
        if headers_match:
            print(f"PASS: Component 2 — Correct headers: {header_values[:5]} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Expected headers {EXPECTED_HEADERS}, found: {header_values}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 5 researchers present with correct data (0.4 points)
    # FAILS on initial_env (no file) — PASSES on golden_env
    try:
        # Extract Name and H_Index from data rows
        found_researchers = {}
        for _, row_vals in data_rows:
            if len(row_vals) >= 3:
                name = row_vals[0]
                institution = row_vals[1]
                h_index_raw = row_vals[2]
                try:
                    h_index = int(float(h_index_raw)) if h_index_raw else None
                except (ValueError, TypeError):
                    h_index = None
                specialty = row_vals[4] if len(row_vals) >= 5 else None
                if name:
                    found_researchers[name] = {
                        'institution': institution,
                        'h_index': h_index,
                        'specialty': specialty,
                    }

        correct_count = 0
        for exp_name, exp_inst, exp_h_index, exp_specialty in EXPECTED_RESEARCHERS:
            if exp_name in found_researchers:
                researcher = found_researchers[exp_name]
                if (researcher['institution'] == exp_inst and
                        researcher['h_index'] == exp_h_index and
                        researcher['specialty'] == exp_specialty):
                    correct_count += 1
                    print(f"  PASS: {exp_name} — institution, H-Index, specialty all correct")
                else:
                    print(f"  PARTIAL: {exp_name} found but data mismatch. "
                          f"institution={researcher['institution']!r} (expected {exp_inst!r}), "
                          f"h_index={researcher['h_index']} (expected {exp_h_index}), "
                          f"specialty={researcher['specialty']!r} (expected {exp_specialty!r})")
            else:
                print(f"  FAIL: {exp_name} not found in spreadsheet")

        if correct_count == 5:
            print(f"PASS: Component 3 — All 5 researchers with correct data (0.4 pts)")
            total_score += 0.4
        elif correct_count > 0:
            partial = round(0.4 * correct_count / 5, 2)
            print(f"PARTIAL: Component 3 — {correct_count}/5 researchers correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No researchers found with correct data")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Data sorted by H_Index descending (0.1 points)
    # FAILS on initial_env (no file) — PASSES on golden_env
    try:
        h_indices = []
        for _, row_vals in data_rows:
            if len(row_vals) >= 3 and row_vals[2] is not None:
                try:
                    h_indices.append(int(float(row_vals[2])))
                except (ValueError, TypeError):
                    pass

        if len(h_indices) >= 2:
            is_sorted_desc = all(h_indices[i] >= h_indices[i+1] for i in range(len(h_indices)-1))
            if is_sorted_desc and h_indices == sorted(h_indices, reverse=True):
                print(f"PASS: Component 4 — H_Index sorted descending: {h_indices} (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 4 — H_Index NOT sorted descending, found: {h_indices}, expected: {sorted(h_indices, reverse=True)}")
        else:
            print(f"FAIL: Component 4 — Not enough H_Index values to check sort (found: {h_indices})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Header row has bold formatting (0.1 points)
    # FAILS on initial_env (no file) — PASSES on golden_env
    try:
        bold_styles = get_bold_styles(content_xml_str)

        # Check if header cells use a bold style
        header_cells = header_row_elem.findall('table:table-cell', NS)
        bold_header_count = 0
        for cell in header_cells[:5]:  # check first 5 header cells
            style_name = cell.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}style-name')
            if style_name in bold_styles:
                bold_header_count += 1

        if bold_header_count >= 5:
            print(f"PASS: Component 5 — All {bold_header_count} header cells use bold style (0.1 pts)")
            total_score += 0.1
        elif bold_header_count > 0:
            print(f"PARTIAL: Component 5 — Only {bold_header_count}/5 header cells are bold (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 — Header cells are NOT bold (styles found: {bold_styles})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
