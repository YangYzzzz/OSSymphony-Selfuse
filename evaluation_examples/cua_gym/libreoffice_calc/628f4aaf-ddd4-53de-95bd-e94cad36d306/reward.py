"""
Reward Script: ACL Anthology Best Paper Affiliation Analysis
Task ID: osworld_multi_apps_acl_awards_calc_009
Domain: libreoffice_calc (ODS format)

Scoring Rubric:
  Component 1 (0.4): 4 data rows exist in rows 2-5 for years 2019-2022 with
                      valid Affiliation Type values (Academic or Industry)
  Component 2 (0.3): H2 contains a COUNTIF formula counting 'Academic' affiliations
  Component 3 (0.3): H3 contains a COUNTIF formula counting 'Industry' affiliations,
                      and the computed counts H2+H3 == 4 (all 4 rows accounted for)
  Total: 1.0

Note: This task uses .ods format. We use odfpy to read the file directly.
      If odfpy is not installed, we attempt to install it before reading.
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_acl_awards_calc_009'
ODS_FILE = os.path.join(WORKDIR, 'affiliation_analysis.ods')


def ensure_odfpy():
    """Ensure odfpy is available, install if not."""
    try:
        import odf  # noqa
        return True
    except ImportError:
        import pip
        pip.main(['install', 'odfpy', '-q'])
        try:
            import odf  # noqa
            return True
        except ImportError:
            return False


def get_cell_value(cell):
    """Extract text value from an ODF table cell."""
    from odf.text import P
    ps = cell.getElementsByType(P)
    if ps and ps[0].firstChild:
        return ps[0].firstChild.data
    return None


def get_cell_formula(cell):
    """Extract formula from an ODF table cell (table:formula attribute)."""
    formula = cell.getAttribute('formula')
    return formula  # e.g. 'of:=COUNTIF([.D2:.D5],"Academic")'


def get_cell_cached_value(cell):
    """Get the cached/computed numeric value stored in the cell."""
    val = cell.getAttribute('value')
    if val is not None:
        try:
            return float(val)
        except (ValueError, TypeError):
            return None
    return None


def read_ods_grid(ods_path):
    """
    Read the ODS file and return a dict of {(row, col): value}.
    Also return a dict of {(row, col): formula} for formula cells.
    row and col are 1-indexed.
    """
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell

    doc = load(ods_path)
    sheets = doc.spreadsheet.getElementsByType(Table)
    if not sheets:
        return {}, {}, {}

    sheet = sheets[0]  # Use first sheet
    values = {}
    formulas = {}
    cached_values = {}

    rows = sheet.getElementsByType(TableRow)
    row_idx = 1
    for row in rows:
        col_idx = 1
        cells = row.getElementsByType(TableCell)
        for cell in cells:
            repeat = cell.getAttribute('numbercolumnsrepeated')
            repeat = int(repeat) if repeat else 1

            val = get_cell_value(cell)
            formula = get_cell_formula(cell)
            cached = get_cell_cached_value(cell)

            for _ in range(repeat):
                if val:
                    values[(row_idx, col_idx)] = val
                if formula:
                    formulas[(row_idx, col_idx)] = formula
                if cached is not None:
                    cached_values[(row_idx, col_idx)] = cached
                col_idx += 1
        row_idx += 1

    return values, formulas, cached_values


def verify_task(ods_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Pre-check: file exists
    if not os.path.exists(ods_path):
        print(f"CRITICAL: ODS file not found: {ods_path}")
        print("REWARD: 0.0")
        return 0.0

    # Ensure odfpy is available
    if not ensure_odfpy():
        print("CRITICAL: odfpy library not available and could not be installed.")
        print("REWARD: 0.0")
        return 0.0

    # Load ODS grid
    try:
        values, formulas, cached_values = read_ods_grid(ods_path)
    except Exception as e:
        print(f"CRITICAL: Cannot read ODS file {ods_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: 4 data rows (rows 2-5) have year (2019-2022), non-empty
    # title and author, and valid Affiliation Type ('Academic' or 'Industry')
    # in columns A-D.
    # This FAILS on initial_env (rows 2-5 are empty) and PASSES on golden_env.
    # -----------------------------------------------------------------------
    try:
        valid_rows = 0
        years_found = []
        affiliations = []

        for row_idx in range(2, 6):  # rows 2, 3, 4, 5
            year_val = values.get((row_idx, 1), '')    # Column A
            title_val = values.get((row_idx, 2), '')   # Column B
            author_val = values.get((row_idx, 3), '')  # Column C
            affil_val = values.get((row_idx, 4), '')   # Column D

            year_ok = str(year_val).strip() in ['2019', '2020', '2021', '2022']
            title_ok = len(str(title_val).strip()) > 0
            author_ok = len(str(author_val).strip()) > 0
            affil_ok = str(affil_val).strip() in ['Academic', 'Industry']

            if year_ok and title_ok and author_ok and affil_ok:
                valid_rows += 1
                years_found.append(str(year_val).strip())
                affiliations.append(str(affil_val).strip())

        all_years_present = sorted(years_found) == ['2019', '2020', '2021', '2022']

        if valid_rows == 4 and all_years_present:
            print(f"PASS: Component 1 — 4 data rows found for years 2019-2022 with valid affiliations. "
                  f"Years={sorted(years_found)}, Affiliations={affiliations} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected 4 rows for 2019-2022 with valid affiliations, "
                  f"found {valid_rows} valid rows. Years={years_found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: H2 (row 2, col 8 in ODS — the 'Count' column) contains a
    # COUNTIF formula counting 'Academic' affiliations in column D (0.3 points).
    # Note: ODS cols A=1,B=2,C=3,D=4,E-F=5-6 (blank),G=7,H=8.
    # This FAILS on initial_env (H2 is empty) and PASSES on golden_env.
    # -----------------------------------------------------------------------
    try:
        h2_formula = formulas.get((2, 8), None)
        h2_value = values.get((2, 8), None)

        # Check if either the formula attribute or the text value contains COUNTIF + ACADEMIC
        formula_has_academic = (h2_formula is not None and
                                'COUNTIF' in h2_formula.upper() and
                                'ACADEMIC' in h2_formula.upper())
        value_has_academic = (h2_value is not None and
                              isinstance(h2_value, str) and
                              'COUNTIF' in h2_value.upper() and
                              'ACADEMIC' in h2_value.upper())
        formula_detail = h2_formula if formula_has_academic else (h2_value if value_has_academic else None)

        if formula_has_academic or value_has_academic:
            print(f"PASS: Component 2 — H2 contains COUNTIF formula for 'Academic': {repr(formula_detail)} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — H2 expected COUNTIF formula counting Academic. "
                  f"formula={repr(h2_formula)}, value={repr(h2_value)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: H3 (row 3, col 8 in ODS — the 'Count' column) contains a
    # COUNTIF formula counting 'Industry' affiliations, AND computed counts
    # H2+H3 == 4 (all 4 rows accounted for) (0.3 points).
    # This FAILS on initial_env (H3 is empty, no data rows) and PASSES on golden_env.
    # -----------------------------------------------------------------------
    try:
        h3_formula = formulas.get((3, 8), None)
        h3_value = values.get((3, 8), None)

        # Check if either the formula attribute or the text value contains COUNTIF + INDUSTRY
        formula_has_industry = (h3_formula is not None and
                                'COUNTIF' in h3_formula.upper() and
                                'INDUSTRY' in h3_formula.upper())
        value_has_industry = (h3_value is not None and
                              isinstance(h3_value, str) and
                              'COUNTIF' in h3_value.upper() and
                              'INDUSTRY' in h3_value.upper())
        formula_detail_h3 = h3_formula if formula_has_industry else (h3_value if value_has_industry else None)

        # Verify that the cached sum H2+H3 == 4 (all data rows accounted for)
        h2_cached = cached_values.get((2, 8), None)
        h3_cached = cached_values.get((3, 8), None)

        counts_sum_ok = (h2_cached is not None and h3_cached is not None and
                         int(h2_cached) + int(h3_cached) == 4)
        counts_sum_detail = (f"H2={int(h2_cached)}, H3={int(h3_cached)}, sum={int(h2_cached)+int(h3_cached)}"
                             if h2_cached is not None and h3_cached is not None
                             else f"H2_cached={h2_cached}, H3_cached={h3_cached}")

        if (formula_has_industry or value_has_industry) and counts_sum_ok:
            print(f"PASS: Component 3 — H3 contains COUNTIF formula for 'Industry': {repr(formula_detail_h3)}, "
                  f"and counts sum to 4 ({counts_sum_detail}) (0.3 pts)")
            total_score += 0.3
        elif (formula_has_industry or value_has_industry) and not counts_sum_ok:
            print(f"FAIL: Component 3 — H3 has COUNTIF formula but counts don't sum to 4: {counts_sum_detail}")
        else:
            print(f"FAIL: Component 3 — H3 expected COUNTIF formula counting Industry. "
                  f"formula={repr(h3_formula)}, value={repr(h3_value)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the ODS file at the canonical task path
if not os.path.exists(ODS_FILE):
    print(f"File not found: {ODS_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(ODS_FILE)
