"""
Reward Script: Research world's top food festivals and compile event database
Task ID: osworld_multi_apps_web_location_014
Domain: libreoffice_calc (ODS file)
Scoring:
  Component 1: Festivals sheet exists with 15+ rows (0.25 pts)
  Component 2: All required columns present in Festivals sheet (0.25 pts)
  Component 3: Data is sorted by month (calendar order) (0.20 pts)
  Component 4: Prestige_Tier column contains valid tiers (A/B/C) (0.10 pts)
  Component 5: By_Continent sheet exists with continent/count/avg columns (0.20 pts)
Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_location_014'
FILE_PATH = f'{WORKDIR}/food_festivals_world.ods'

# Month order mapping for sorting verification
MONTH_ORDER = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12
}

REQUIRED_COLUMNS = {
    'Festival_Name', 'City', 'Country', 'Continent',
    'Month', 'Avg_Ticket_USD', 'Signature_Event',
    'Annual_Attendance', 'Prestige_Tier', 'Website'
}

VALID_TIERS = {'A', 'B', 'C'}
VALID_CONTINENTS = {'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America', 'Antarctica'}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pandas as pd
        sheets = pd.read_excel(file_path, sheet_name=None, engine='odf')
    except ImportError:
        # Try openpyxl if odf not available (shouldn't happen for .ods)
        try:
            import pandas as pd
            sheets = pd.read_excel(file_path, sheet_name=None)
        except Exception as e:
            print(f"CRITICAL: Cannot load file {file_path}: {e}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Festivals sheet exists with 15+ data rows (0.25 points)
    try:
        festivals_sheet = None
        for sheet_name in sheets.keys():
            if 'festival' in sheet_name.lower():
                festivals_sheet = sheet_name
                break

        if festivals_sheet is None:
            print(f"FAIL: Component 1 — No 'Festivals' sheet found. Available sheets: {list(sheets.keys())}")
        else:
            df = sheets[festivals_sheet]
            row_count = len(df)
            if row_count >= 15:
                print(f"PASS: Component 1 — Festivals sheet '{festivals_sheet}' found with {row_count} rows (>= 15 required)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — Festivals sheet '{festivals_sheet}' has only {row_count} rows, need at least 15")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All required columns present in Festivals sheet (0.25 points)
    try:
        if festivals_sheet is None:
            print("FAIL: Component 2 — Skipped because Festivals sheet not found")
        else:
            df = sheets[festivals_sheet]
            actual_columns = set(df.columns)
            missing_cols = REQUIRED_COLUMNS - actual_columns
            if not missing_cols:
                print(f"PASS: Component 2 — All {len(REQUIRED_COLUMNS)} required columns present: {sorted(REQUIRED_COLUMNS)}")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Missing columns: {sorted(missing_cols)}. Found: {sorted(actual_columns)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Data sorted by month in calendar order (0.20 points)
    try:
        if festivals_sheet is None:
            print("FAIL: Component 3 — Skipped because Festivals sheet not found")
        else:
            df = sheets[festivals_sheet]
            if 'Month' not in df.columns:
                print("FAIL: Component 3 — 'Month' column not found")
            else:
                months = [str(m).strip().lower() for m in df['Month'].dropna()]
                month_nums = [MONTH_ORDER.get(m, None) for m in months]

                # Filter out None values (unrecognized month names)
                valid_months = [(i, n) for i, n in enumerate(month_nums) if n is not None]

                if len(valid_months) < 2:
                    print(f"FAIL: Component 3 — Too few recognizable months to verify sorting: {months[:5]}")
                else:
                    nums_only = [n for _, n in valid_months]
                    is_sorted = all(nums_only[i] <= nums_only[i+1] for i in range(len(nums_only)-1))
                    if is_sorted:
                        print(f"PASS: Component 3 — Data sorted by month in calendar order. First 5 months: {months[:5]}")
                        total_score += 0.20
                    else:
                        # Find first out-of-order pair
                        for i in range(len(nums_only)-1):
                            if nums_only[i] > nums_only[i+1]:
                                print(f"FAIL: Component 3 — Data not sorted by month. Row {i} ({months[i]}) comes before row {i+1} ({months[i+1]})")
                                break
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Prestige_Tier column contains only valid tiers A/B/C (0.10 points)
    try:
        if festivals_sheet is None:
            print("FAIL: Component 4 — Skipped because Festivals sheet not found")
        else:
            df = sheets[festivals_sheet]
            if 'Prestige_Tier' not in df.columns:
                print("FAIL: Component 4 — 'Prestige_Tier' column not found")
            else:
                tiers = set(str(t).strip() for t in df['Prestige_Tier'].dropna())
                invalid_tiers = tiers - VALID_TIERS
                has_all_categories = len(tiers) >= 2  # Should have multiple tiers
                if not invalid_tiers and has_all_categories:
                    print(f"PASS: Component 4 — Prestige_Tier column uses valid tiers: {sorted(tiers)}")
                    total_score += 0.10
                elif invalid_tiers:
                    print(f"FAIL: Component 4 — Invalid tier values found: {invalid_tiers}. Valid values: {VALID_TIERS}")
                else:
                    print(f"FAIL: Component 4 — Only {len(tiers)} unique tier(s) found: {tiers}. Expected multiple (A, B, C)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: By_Continent sheet exists with continent groupings (0.20 points)
    try:
        continent_sheet = None
        for sheet_name in sheets.keys():
            if 'continent' in sheet_name.lower():
                continent_sheet = sheet_name
                break

        if continent_sheet is None:
            print(f"FAIL: Component 5 — No 'By_Continent' sheet found. Available sheets: {list(sheets.keys())}")
        else:
            df_cont = sheets[continent_sheet]
            # Must have continent, count, and avg_ticket columns
            col_names_lower = [c.lower().replace('_', '').replace(' ', '') for c in df_cont.columns]
            has_continent_col = any('continent' in c for c in col_names_lower)
            has_count_col = any('count' in c or 'num' in c or 'total' in c for c in col_names_lower)
            has_avg_col = any('avg' in c or 'average' in c or 'mean' in c for c in col_names_lower)

            if has_continent_col and has_count_col and has_avg_col:
                num_continents = len(df_cont)
                print(f"PASS: Component 5 — By_Continent sheet '{continent_sheet}' found with {num_continents} continent groups. Columns: {list(df_cont.columns)}")
                total_score += 0.20
            else:
                missing = []
                if not has_continent_col:
                    missing.append('Continent')
                if not has_count_col:
                    missing.append('count/festival_count')
                if not has_avg_col:
                    missing.append('avg_ticket/average')
                print(f"FAIL: Component 5 — By_Continent sheet '{continent_sheet}' missing columns: {missing}. Found: {list(df_cont.columns)}")
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
    verify_task(FILE_PATH)
