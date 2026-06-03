"""
Reward Script: Apply 7 data transformations from transform_spec.odt to raw_data.ods
Task ID: osworld_multi_apps_doc_follow_instructions_006
Domain: libreoffice_calc (ODS format)
Scoring:
  1. Column H 'Profit_Margin' with formula (D-E)/D present        — 0.20 pts
  2. Column I 'Performance' with IF formula present               — 0.20 pts
  3. Conditional formatting on column I (High/Medium/Low)         — 0.15 pts
  4. SUBTOTAL row at row 2 with SUM(Revenue) and SUM(Cost)        — 0.20 pts
  5. Data sorted by Revenue descending                            — 0.15 pts
  6. Column A hidden                                              — 0.10 pts
  Total: 1.00
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_follow_instructions_006'
FILE_PATH = f'{WORKDIR}/Desktop/raw_data.ods'

# ODF namespaces
NS = {
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'loext': 'urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0',
    'calcext': 'urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0',
}


def load_ods(filepath):
    """Load ODS content and styles XML."""
    with zipfile.ZipFile(filepath, 'r') as z:
        content = z.read('content.xml').decode('utf-8')
        styles = z.read('styles.xml').decode('utf-8') if 'styles.xml' in z.namelist() else ''
    return content, styles


def parse_rows(root):
    """
    Parse all rows from the first sheet, returning a list of lists.
    Each cell is a dict: {type, formula, num_val, text, style_name}.
    """
    sheets = root.findall('.//table:table', NS)
    if not sheets:
        return []
    ws = sheets[0]
    rows_list = []
    for row_elem in ws.findall('table:table-row', NS):
        cells = row_elem.findall('table:table-cell', NS)
        row_data = []
        for cell in cells:
            repeated = int(cell.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated', '1'))
            formula = cell.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}formula', '')
            num_val = cell.get('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}value', '')
            text_elem = cell.find('.//text:p', NS)
            text_val = text_elem.text if text_elem is not None and text_elem.text else ''
            style_name = cell.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}style-name', '')
            val_type = cell.get('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}value-type', '')
            cell_info = {
                'type': val_type,
                'formula': formula,
                'num_val': num_val,
                'text': text_val,
                'style': style_name,
            }
            # Only expand reasonable repeated counts (skip trailing empty cols)
            if repeated < 100:
                for _ in range(repeated):
                    row_data.append(cell_info)
            else:
                row_data.append(cell_info)  # keep first
        rows_list.append(row_data)
    return rows_list


def get_column_visibility(root):
    """Return dict mapping 0-based col index to visibility string."""
    sheets = root.findall('.//table:table', NS)
    if not sheets:
        return {}
    ws = sheets[0]
    col_vis = {}
    col_idx = 0
    for col_elem in ws.findall('table:table-column', NS):
        vis = col_elem.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}visibility', 'visible')
        repeated = int(col_elem.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated', '1'))
        for _ in range(min(repeated, 50)):
            col_vis[col_idx] = vis
            col_idx += 1
        if repeated >= 50:
            col_idx += repeated - 50
    return col_vis


def get_conditional_formats(root, styles_root):
    """
    Return a list of conditional format condition dicts from calcext namespace.
    Also return the style names and their background colors.

    Note: LibreOffice ODS uses '_5f_' to encode underscores in XML style names
    in styles.xml, but uses plain underscores in the CF conditions.
    We normalize by building a lookup that handles both forms.
    """
    cf_conditions = []
    style_ns = 'urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0'

    # Find calcext:conditional-formats
    for cf_elem in root.iter(f'{{{style_ns}}}conditional-format'):
        target = cf_elem.get(f'{{{style_ns}}}target-range-address', '')
        for cond in cf_elem.findall(f'{{{style_ns}}}condition'):
            cf_conditions.append({
                'target': target,
                'value': cond.get(f'{{{style_ns}}}value', ''),
                'style': cond.get(f'{{{style_ns}}}apply-style-name', ''),
            })

    # Get style background colors from styles.xml
    # LibreOffice encodes underscores as '_5f_' in style names within styles.xml
    style_colors = {}
    if styles_root is not None:
        style_ns2 = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'
        fo_ns = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'
        for style_elem in styles_root.iter(f'{{{style_ns2}}}style'):
            s_name = style_elem.get(f'{{{style_ns2}}}name', '')
            for props in style_elem.findall(f'{{{style_ns2}}}table-cell-properties'):
                bg = props.get(f'{{{fo_ns}}}background-color', '')
                if bg:
                    style_colors[s_name] = bg
                    # Also register decoded name (replace _5f_ with _)
                    decoded_name = s_name.replace('_5f_', '_')
                    if decoded_name != s_name:
                        style_colors[decoded_name] = bg

    return cf_conditions, style_colors


def parse_revenue(text):
    """Parse revenue text like '342,600.00' to float."""
    if not text:
        return None
    try:
        return float(text.replace(',', '').replace(' ', ''))
    except (ValueError, TypeError):
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load ODS file
    try:
        content_xml, styles_xml = load_ods(file_path)
        content_root = ET.fromstring(content_xml)
        styles_root = ET.fromstring(styles_xml) if styles_xml else None
        rows = parse_rows(content_root)
        print(f"INFO: Loaded {file_path}, {len(rows)} rows parsed")
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(rows) < 2:
        print("CRITICAL: File has fewer than 2 rows — likely empty")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: Column H 'Profit_Margin' with (Revenue-Cost)/Revenue formula
    # Expected: header row has 'Profit_Margin' at index 7 (column H)
    #           data rows have formula containing (D-E)/D pattern
    # (0.20 points)
    # -----------------------------------------------------------------------
    try:
        header_row = rows[0]
        # Check header H
        h_header = header_row[7]['text'] if len(header_row) > 7 else ''
        h_header_ok = 'profit_margin' in h_header.lower() or h_header == 'Profit_Margin'

        # Check that at least some data rows have a formula in column H
        h_formula_count = 0
        for row in rows[2:]:  # Skip header and possible subtotal
            if len(row) > 7 and row[7]['formula']:
                formula = row[7]['formula']
                # Formula should reference D and E columns with division
                if ('D' in formula or '.D' in formula) and ('E' in formula or '.E' in formula):
                    h_formula_count += 1

        if h_header_ok and h_formula_count >= 20:
            print(f"PASS: Component 1 — Header 'Profit_Margin' present, {h_formula_count} rows with formula (0.20 pts)")
            total_score += 0.20
        elif h_header_ok and h_formula_count > 0:
            print(f"PARTIAL: Component 1 — Header ok, only {h_formula_count} rows with formula (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — H header='{h_header}', formulas={h_formula_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Column I 'Performance' with IF(H>0.3,"High",...) formula
    # Expected: header at index 8, data rows have IF formula
    # (0.20 points)
    # -----------------------------------------------------------------------
    try:
        i_header = header_row[8]['text'] if len(header_row) > 8 else ''
        i_header_ok = 'performance' in i_header.lower()

        i_formula_count = 0
        for row in rows[2:]:
            if len(row) > 8 and row[8]['formula']:
                formula = row[8]['formula']
                # Formula should be IF referencing H column with High/Medium/Low
                if 'IF' in formula.upper() and ('High' in formula or 'HIGH' in formula.upper()):
                    i_formula_count += 1

        if i_header_ok and i_formula_count >= 20:
            print(f"PASS: Component 2 — Header 'Performance' present, {i_formula_count} rows with IF formula (0.20 pts)")
            total_score += 0.20
        elif i_header_ok and i_formula_count > 0:
            print(f"PARTIAL: Component 2 — Header ok, only {i_formula_count} rows with formula (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — I header='{i_header}', formulas={i_formula_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Conditional formatting on column I
    # Expected: 3 conditions (High=green, Medium=yellow, Low=red)
    # (0.15 points)
    # -----------------------------------------------------------------------
    try:
        cf_conditions, style_colors = get_conditional_formats(content_root, styles_root)

        # Check if we have conditions referencing High, Medium, Low
        has_high = any('High' in c['value'] or '"High"' in c['value'] for c in cf_conditions)
        has_medium = any('Medium' in c['value'] or '"Medium"' in c['value'] for c in cf_conditions)
        has_low = any('Low' in c['value'] or '"Low"' in c['value'] for c in cf_conditions)

        # Check colors: High should be green (#00ff00), Medium yellow (#ffff00), Low red (#ff0000)
        # Verify green for "High" condition
        high_green = any(
            ('High' in c['value']) and ('#00ff00' in style_colors.get(c['style'], '').lower() or
             '00ff00' in style_colors.get(c['style'], '').lower())
            for c in cf_conditions
        )

        cf_count = len([c for c in cf_conditions if c['value']])
        if has_high and has_medium and has_low and high_green:
            print(f"PASS: Component 3 — Conditional formatting with High/Medium/Low + green color present ({cf_count} conditions) (0.15 pts)")
            total_score += 0.15
        elif has_high and has_medium and has_low:
            print(f"PARTIAL: Component 3 — Conditional formatting conditions present but colors not verified ({cf_count} conds) (0.08 pts)")
            total_score += 0.08
        elif cf_count > 0:
            print(f"PARTIAL: Component 3 — {cf_count} CF conditions found but not all 3 (High/Medium/Low) (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 — No conditional formatting found on column I")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: SUBTOTAL row at row 2 (index 1) with SUM formulas
    # Expected: row 2 has 'SUBTOTAL' text in B, SUM formula in D and E
    # (0.20 points)
    # -----------------------------------------------------------------------
    try:
        row2 = rows[1] if len(rows) > 1 else []

        # Check B column (index 1) for SUBTOTAL text
        b2_text = row2[1]['text'] if len(row2) > 1 else ''
        subtotal_text_ok = 'subtotal' in b2_text.lower()

        # Check D column (index 3) for SUM formula
        d2_formula = row2[3]['formula'] if len(row2) > 3 else ''
        d2_sum_ok = 'SUM' in d2_formula.upper()

        # Check E column (index 4) for SUM formula
        e2_formula = row2[4]['formula'] if len(row2) > 4 else ''
        e2_sum_ok = 'SUM' in e2_formula.upper()

        # Check that actual values are correct (Revenue sum should be ~3,029,000)
        d2_text = row2[3]['text'] if len(row2) > 3 else ''
        e2_text = row2[4]['text'] if len(row2) > 4 else ''

        if subtotal_text_ok and d2_sum_ok and e2_sum_ok:
            print(f"PASS: Component 4 — SUBTOTAL row at row 2 with SUM(Revenue) and SUM(Cost), B2='{b2_text}', D2={d2_text}, E2={e2_text} (0.20 pts)")
            total_score += 0.20
        elif d2_sum_ok or e2_sum_ok:
            print(f"PARTIAL: Component 4 — SUM formula partially present (subtotal_text={subtotal_text_ok}, D_sum={d2_sum_ok}, E_sum={e2_sum_ok}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — SUBTOTAL row not found at row 2 (B2='{b2_text}', D2_formula='{d2_formula}')")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: Data sorted by Revenue descending
    # Expected: revenue values in rows 3+ are in descending order
    # (0.15 points)
    # -----------------------------------------------------------------------
    try:
        # Get revenue values from data rows (starting at row 3, index 2)
        # Revenue is column D (index 3)
        revenues = []
        for i, row in enumerate(rows[2:], 3):
            if len(row) > 3:
                rev = parse_revenue(row[3]['text'])
                if rev is not None and rev > 0:
                    revenues.append(rev)

        if len(revenues) >= 20:
            is_sorted = all(revenues[i] >= revenues[i+1] for i in range(len(revenues)-1))
            if is_sorted:
                print(f"PASS: Component 5 — {len(revenues)} revenue rows sorted descending (max={revenues[0]:.0f}, min={revenues[-1]:.0f}) (0.15 pts)")
                total_score += 0.15
            else:
                # Check if mostly sorted (allow small deviations)
                unsorted_count = sum(1 for i in range(len(revenues)-1) if revenues[i] < revenues[i+1])
                print(f"FAIL: Component 5 — Revenue NOT sorted descending ({unsorted_count} violations out of {len(revenues)-1} pairs)")
        else:
            print(f"FAIL: Component 5 — Too few revenue rows found ({len(revenues)})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # -----------------------------------------------------------------------
    # Component 6: Column A hidden
    # Expected: first column group has visibility=collapse or hidden
    # (0.10 points)
    # -----------------------------------------------------------------------
    try:
        col_vis = get_column_visibility(content_root)
        col_a_vis = col_vis.get(0, 'visible')
        col_a_hidden = col_a_vis in ('collapse', 'hidden')
        if col_a_hidden:
            print(f"PASS: Component 6 — Column A is hidden (visibility='{col_a_vis}') (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — Column A is NOT hidden (visibility='{col_a_vis}')")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Final score
    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
