"""
Reward Script: Build a reading tracker with 5 articles.ods
Task ID: osworld_multi_apps_multi_simple_011
Domain: libreoffice_calc
Scoring:
  - Component 1: All 5 word counts filled in column E (0.25 pts)
  - Component 2: All 5 notes filled in column D (0.25 pts)
  - Component 3: SUM formula in E7 totaling all word counts (0.25 pts)
  - Component 4: Data rows sorted by word count ascending (0.25 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_multi_simple_011'
FILE_PATH = f'{WORKDIR}/reading/articles.ods'


def get_cell_text(cell):
    """Extract text content from an ODF cell."""
    from odf.text import P
    paras = cell.getElementsByType(P)
    return ' '.join([str(p) for p in paras]).strip()


def get_cell_numeric_value(cell):
    """Extract the numeric value attribute from an ODF cell (for float cells)."""
    attrs = dict(cell.attributes.items())
    for key, val in attrs.items():
        if 'value' in key[1] and 'type' not in key[1] and 'formula' not in key[1]:
            try:
                return float(val)
            except (ValueError, TypeError):
                pass
    return None


def get_cell_formula(cell):
    """Extract the formula attribute from an ODF cell."""
    attrs = dict(cell.attributes.items())
    for key, val in attrs.items():
        if 'formula' in key[1]:
            return val
    return None


def collect_word_counts(rows):
    """
    Read word counts from column E in rows 2-6 (0-indexed 1-5).
    Returns a list of numeric values, or None for missing/invalid entries.
    """
    from odf.table import TableCell
    counts = []
    for row_idx in range(1, 6):
        row = rows[row_idx]
        cells = row.getElementsByType(TableCell)
        if len(cells) < 5:
            counts.append(None)
            continue
        e_cell = cells[4]
        num_val = get_cell_numeric_value(e_cell)
        if num_val is None:
            # Try parsing from text
            text = get_cell_text(e_cell)
            if text:
                try:
                    num_val = float(text)
                except ValueError:
                    pass
        counts.append(num_val if (num_val is not None and num_val > 0) else None)
    return counts


def collect_notes(rows):
    """
    Read notes from column D in rows 2-6 (0-indexed 1-5).
    Returns a list of strings (empty string for missing/empty entries).
    """
    from odf.table import TableCell
    notes = []
    for row_idx in range(1, 6):
        row = rows[row_idx]
        cells = row.getElementsByType(TableCell)
        if len(cells) < 4:
            notes.append('')
            continue
        d_cell = cells[3]
        text = get_cell_text(d_cell)
        notes.append(text)
    return notes


def verify_task(file_path):
    """
    Verify reading tracker task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from odf.opendocument import load
        from odf.table import Table, TableRow, TableCell
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the spreadsheet sheet
    try:
        sheets = doc.spreadsheet.getElementsByType(Table)
        if not sheets:
            print("CRITICAL: No sheets found in ODS file")
            print("REWARD: 0.0")
            return 0.0
        sheet = sheets[0]  # Articles sheet
        rows = sheet.getElementsByType(TableRow)
        print(f"INFO: Found {len(rows)} rows in sheet '{sheet.getAttribute('name')}'")
    except Exception as e:
        print(f"CRITICAL: Cannot read sheet structure: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: at least 6 rows (header + 5 data rows)
    if len(rows) < 6:
        print(f"CRITICAL: Expected at least 6 rows (header + 5 data), found {len(rows)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 5 word counts filled in column E (rows 2-6)
    # Word counts should be positive numeric values (agent estimated them by running wc -w)
    try:
        word_counts = collect_word_counts(rows)
        valid_counts = [c for c in word_counts if c is not None]
        missing_count = word_counts.count(None)

        if missing_count == 0 and len(valid_counts) == 5:
            print(f"PASS: Component 1 — all 5 word counts filled: {valid_counts} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — {missing_count}/5 word count entries missing or invalid: {word_counts}")
            # No partial credit for this component - all 5 must be present
    except Exception as e:
        print(f"ERROR: Component 1 (word counts) — {e}")
        word_counts = []
        valid_counts = []

    # Component 2: All 5 notes filled in column D (rows 2-6)
    # Notes should be non-empty strings (at least 5 chars) describing the article's main point
    try:
        notes = collect_notes(rows)
        filled_notes = [n for n in notes if n and len(n.strip()) >= 5]
        missing_notes = sum(1 for n in notes if not n or len(n.strip()) < 5)

        if missing_notes == 0 and len(filled_notes) == 5:
            print(f"PASS: Component 2 — all 5 notes filled in column D (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — {missing_notes}/5 notes missing or too short: {notes}")
    except Exception as e:
        print(f"ERROR: Component 2 (notes) — {e}")

    # Component 3: SUM formula in E7 covering E2:E6
    # Row 7 (index 6) column E should have a SUM formula and a valid total
    try:
        from odf.table import TableCell
        if len(rows) < 7:
            print(f"FAIL: Component 3 — only {len(rows)} rows, row 7 missing (SUM formula not added)")
        else:
            row7 = rows[6]
            row7_cells = row7.getElementsByType(TableCell)
            if len(row7_cells) < 5:
                print(f"FAIL: Component 3 — row 7 has only {len(row7_cells)} cells, expected 5")
            else:
                e7_cell = row7_cells[4]  # column E
                formula = get_cell_formula(e7_cell)
                num_val = get_cell_numeric_value(e7_cell)
                text = get_cell_text(e7_cell)

                if num_val is None and text:
                    try:
                        num_val = float(text)
                    except ValueError:
                        pass

                # Check formula contains SUM and references E column range
                has_sum_formula = (
                    formula is not None and
                    'SUM' in formula.upper() and
                    'E' in formula.upper()
                )

                if has_sum_formula and num_val is not None and num_val > 0:
                    print(f"PASS: Component 3 — SUM formula in E7 (formula='{formula}', value={num_val}) (0.25 pts)")
                    total_score += 0.25
                elif not has_sum_formula:
                    print(f"FAIL: Component 3 — E7 has no SUM formula referencing E column (formula='{formula}', text='{text}')")
                else:
                    print(f"FAIL: Component 3 — SUM formula present but invalid/zero value (formula='{formula}', value={num_val})")
    except Exception as e:
        print(f"ERROR: Component 3 (SUM formula) — {e}")

    # Component 4: Data rows sorted by word count ascending
    # Verify that word counts in E2:E6 are in non-decreasing order
    try:
        if len(valid_counts) == 5:
            sorted_check = all(valid_counts[i] <= valid_counts[i+1] for i in range(4))
            if sorted_check:
                print(f"PASS: Component 4 — rows sorted by word count ascending: {valid_counts} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — rows NOT sorted by word count ascending: {valid_counts}")
        else:
            print(f"FAIL: Component 4 — cannot check sort order, only {len(valid_counts)}/5 word counts available")
    except Exception as e:
        print(f"ERROR: Component 4 (sort order) — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against the canonical artifact path in the VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
