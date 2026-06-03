"""
Reward Script: CMU ML Faculty data collection and RL/robotics highlighting
Task ID: osworld_multi_apps_web_faculty_006
Domain: libreoffice_calc (ODS format)
Scoring:
  - Component 1: File exists at correct path with correct sheet and columns (0.3 pts)
  - Component 2: File contains sufficient faculty data rows (>= 10 rows) (0.2 pts)
  - Component 3: At least one row is yellow-highlighted (0.2 pts)
  - Component 4: Yellow rows correctly match RL/robotics keywords AND non-RL/non-robotics rows are NOT highlighted (0.3 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_faculty_006'
FILE_PATH = f'{WORKDIR}/Desktop/cmu_ml_faculty.ods'

# Keywords that should trigger yellow highlight (case-insensitive)
RL_KEYWORDS = ['reinforcement learning']
ROBOTICS_KEYWORDS = ['robotics', 'robot']


def get_cell_text(cell):
    """Extract text content from an ODF cell."""
    try:
        from odf.text import P
        ps = cell.getElementsByType(P)
        return ''.join([str(p) for p in ps]) if ps else ''
    except Exception:
        return ''


def get_cell_style(cell):
    """Get style name of an ODF cell."""
    try:
        return cell.getAttribute('stylename')
    except Exception:
        return None


def is_yellow_style(style_name, style_map):
    """Check if a style name corresponds to yellow background."""
    if style_name is None:
        return False
    style_info = style_map.get(style_name, {})
    bg = style_info.get('background-color', '').lower()
    # Yellow is #ffff00 or similar
    return bg in ('#ffff00', 'yellow', '#ffff00')


def has_rl_or_robotics(research_interests):
    """Return True if the research interests mention RL or robotics."""
    text_lower = research_interests.lower()
    for kw in RL_KEYWORDS:
        if kw in text_lower:
            return True
    for kw in ROBOTICS_KEYWORDS:
        if kw in text_lower:
            return True
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load ODF document
    try:
        from odf.opendocument import load
        from odf.table import Table, TableRow, TableCell
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build style map from automatic styles: style_name -> {property: value}
    style_map = {}
    try:
        from odf.namespaces import FONS, STYLENS
        for s in doc.automaticstyles.childNodes:
            try:
                name = s.getAttribute('name')
                if not name:
                    continue
                style_map[name] = {}
                for child in s.childNodes:
                    try:
                        attrs = child.attributes
                        for k, v in attrs.items():
                            # k is (namespace, localname) tuple
                            local = k[1] if isinstance(k, tuple) else str(k)
                            style_map[name][local] = v
                    except Exception:
                        pass
            except Exception:
                pass
    except Exception as e:
        print(f"WARN: Could not parse styles: {e}")

    # Get sheets
    try:
        sheets = doc.spreadsheet.getElementsByType(Table)
    except Exception as e:
        print(f"CRITICAL: Cannot get sheets: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------
    # Component 1: File has correct sheet name and required columns (0.3 pts)
    # -------------------------------------------------------------------
    # Check: at least one sheet, with expected columns (Name, Title, Research_Interests, Profile_URL)
    try:
        from odf.table import TableRow, TableCell
        required_columns = {'name', 'title', 'research_interests', 'profile_url'}
        found_columns = set()
        active_sheet = None

        for sheet in sheets:
            rows = sheet.getElementsByType(TableRow)
            if rows:
                header_row = rows[0]
                cells = header_row.getElementsByType(TableCell)
                header_vals = [get_cell_text(c).strip().lower() for c in cells if get_cell_text(c).strip()]
                for col in required_columns:
                    if col in header_vals:
                        found_columns.add(col)
                if len(found_columns) >= 3:
                    active_sheet = sheet
                    break

        if active_sheet is not None and len(found_columns) >= 4:
            print(f"PASS: Component 1 — Sheet found with all required columns: {found_columns} (0.3 pts)")
            total_score += 0.3
        elif active_sheet is not None and len(found_columns) >= 3:
            print(f"PASS: Component 1 (partial) — Sheet found with columns: {found_columns} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Required columns not found. Found: {found_columns}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        active_sheet = sheets[0] if sheets else None

    if active_sheet is None and sheets:
        active_sheet = sheets[0]

    # -------------------------------------------------------------------
    # Component 2: File contains >= 10 faculty data rows (0.2 pts)
    # -------------------------------------------------------------------
    try:
        rows = active_sheet.getElementsByType(TableRow)
        # Count non-empty data rows (skip header row 0)
        data_rows = []
        for row in rows[1:]:
            cells = row.getElementsByType(TableCell)
            if not cells:
                continue
            name_val = get_cell_text(cells[0]).strip()
            if name_val:
                data_rows.append(row)

        row_count = len(data_rows)
        if row_count >= 10:
            print(f"PASS: Component 2 — {row_count} faculty data rows found (>= 10) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Only {row_count} faculty data rows found (need >= 10)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")
        data_rows = []

    # -------------------------------------------------------------------
    # Component 3: At least one row is yellow-highlighted (0.2 pts)
    # -------------------------------------------------------------------
    try:
        yellow_rows = []
        for row in data_rows:
            cells = row.getElementsByType(TableCell)
            if not cells:
                continue
            first_style = get_cell_style(cells[0])
            if is_yellow_style(first_style, style_map):
                name_val = get_cell_text(cells[0]).strip()
                yellow_rows.append(name_val)

        if len(yellow_rows) >= 1:
            print(f"PASS: Component 3 — {len(yellow_rows)} yellow-highlighted row(s) found (0.2 pts)")
            print(f"  Yellow rows: {yellow_rows}")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — No yellow-highlighted rows found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")
        yellow_rows = []

    # -------------------------------------------------------------------
    # Component 4: Yellow rows match RL/robotics AND non-matching rows are NOT yellow (0.3 pts)
    # -------------------------------------------------------------------
    # Sub-check 4a: All yellow rows actually mention RL or robotics
    # Sub-check 4b: No non-RL/non-robotics row is highlighted yellow
    try:
        correct_highlights = 0
        wrong_highlights = 0  # non-RL/non-robotics rows that are yellow
        missed_highlights = 0  # RL/robotics rows that are NOT yellow
        total_rl_robotics = 0

        for row in data_rows:
            cells = row.getElementsByType(TableCell)
            if len(cells) < 3:
                continue
            name_val = get_cell_text(cells[0]).strip()
            if len(cells) > 2:
                research_val = get_cell_text(cells[2]).strip()
            else:
                research_val = ''

            first_style = get_cell_style(cells[0])
            is_yellow = is_yellow_style(first_style, style_map)

            should_be_yellow = has_rl_or_robotics(research_val)

            if should_be_yellow:
                total_rl_robotics += 1
                if is_yellow:
                    correct_highlights += 1
                else:
                    missed_highlights += 1
            else:
                if is_yellow:
                    wrong_highlights += 1

        print(f"  Component 4 details: total_rl_robotics={total_rl_robotics}, "
              f"correct={correct_highlights}, missed={missed_highlights}, wrong={wrong_highlights}")

        if total_rl_robotics == 0:
            print(f"FAIL: Component 4 — No RL/robotics rows found to verify against")
        else:
            # Full 0.3 points: all RL/robotics rows highlighted, no wrong highlights
            if wrong_highlights == 0 and missed_highlights == 0 and correct_highlights >= 1:
                print(f"PASS: Component 4 — All {correct_highlights}/{total_rl_robotics} RL/robotics rows highlighted yellow, "
                      f"no wrong highlights (0.3 pts)")
                total_score += 0.3
            elif wrong_highlights == 0 and correct_highlights >= 1:
                # At least some correct, no wrong ones — partial credit
                ratio = correct_highlights / total_rl_robotics
                print(f"PASS (partial): Component 4 — {correct_highlights}/{total_rl_robotics} RL/robotics rows highlighted, "
                      f"no wrong highlights ({round(0.3 * ratio, 2)} pts)")
                if wrong_highlights == 0 and correct_highlights >= 1:
                    total_score += round(0.3 * ratio, 2)
            else:
                print(f"FAIL: Component 4 — {wrong_highlights} non-RL/non-robotics rows incorrectly highlighted "
                      f"and/or {missed_highlights} RL/robotics rows missed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against the canonical ODS file on the VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
