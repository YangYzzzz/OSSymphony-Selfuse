"""
Reward Script: Research specialty coffee shops in 5 major cities and build cross-city comparison
Task ID: osworld_multi_apps_web_location_013
Domain: libreoffice_calc + libreoffice_writer
Scoring:
  Component 1 (0.4): specialty_coffee_global.ods has 20+ data rows with required 8 columns
  Component 2 (0.3): specialty_coffee_global.ods covers all 5 required cities with 4+ shops each
  Component 3 (0.3): coffee_city_guide.odt has real content: 5 tables and no placeholder text
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_location_013'

REQUIRED_CITIES = {'New York', 'London', 'Tokyo', 'Melbourne', 'Seoul'}
REQUIRED_COLUMNS = {
    'City', 'Shop_Name', 'Address', 'Rating',
    'Specialty_Type', 'Hours', 'Roasts_In_House', 'Source_URL'
}
ODS_PATH = os.path.join(WORKDIR, 'specialty_coffee_global.ods')
ODT_PATH = os.path.join(WORKDIR, 'Documents', 'coffee_city_guide.odt')


def extract_ods_rows(path):
    """
    Extract rows from an ODS file (ODF format with content.xml).
    Returns list of lists (each inner list is row cell values).
    Returns None if file is not valid ODS format.
    """
    try:
        with zipfile.ZipFile(path) as z:
            if 'content.xml' not in z.namelist():
                return None
            content = z.read('content.xml').decode('utf-8')
        row_pattern = re.compile(
            r'<table:table-row[^>]*>(.*?)</table:table-row>', re.DOTALL
        )
        raw_rows = row_pattern.findall(content)
        result = []
        for row_xml in raw_rows:
            cells = re.findall(r'<text:p[^>]*>(.*?)</text:p>', row_xml, re.DOTALL)
            # Strip XML tags within cells
            cells = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
            result.append(cells)
        return result
    except Exception as e:
        print(f"ERROR: Could not parse ODS file {path}: {e}")
        return None


def extract_odt_info(path):
    """
    Extract info from an ODT file (ODF format with content.xml).
    Returns dict with 'tables_count' and 'has_placeholders', or None if not ODF.
    """
    try:
        with zipfile.ZipFile(path) as z:
            if 'content.xml' not in z.namelist():
                return None
            content = z.read('content.xml').decode('utf-8')
        tables_count = content.count('<table:table ')
        p_pattern = re.compile(r'<text:p[^>]*>(.*?)</text:p>', re.DOTALL)
        paras = p_pattern.findall(content)
        all_text = ''
        for p in paras:
            clean = re.sub(r'<[^>]+>', '', p).strip()
            all_text += clean + ' '
        has_placeholder = '[Research' in all_text or '[research' in all_text
        return {
            'tables_count': tables_count,
            'has_placeholders': has_placeholder,
            'all_text': all_text,
        }
    except Exception as e:
        print(f"ERROR: Could not parse ODT file {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -------------------------------------------------------------------------
    # Component 1: specialty_coffee_global.ods has 20+ data rows with
    #              the 8 required column headers (0.4 points)
    # Fails on initial_env (only 1 header row, no data) → Passes on golden_env
    # -------------------------------------------------------------------------
    try:
        if not os.path.exists(ODS_PATH):
            print(f"FAIL: Component 1 — {ODS_PATH} does not exist")
        else:
            rows = extract_ods_rows(ODS_PATH)
            if rows is None:
                print("FAIL: Component 1 — specialty_coffee_global.ods is not a valid ODS file")
            elif len(rows) < 2:
                print(f"FAIL: Component 1 — ODS has only {len(rows)} row(s), expected header + 20+ data rows")
            else:
                header = [c.strip() for c in rows[0]]
                data_rows = [r for r in rows[1:] if any(c.strip() for c in r)]
                num_data = len(data_rows)
                # Check required columns exist
                missing_cols = REQUIRED_COLUMNS - set(header)
                if missing_cols:
                    print(f"FAIL: Component 1 — ODS header missing columns: {missing_cols}")
                elif num_data < 20:
                    print(f"FAIL: Component 1 — ODS has {num_data} data rows, expected 20+")
                else:
                    print(f"PASS: Component 1 — ODS has {num_data} data rows with all 8 required columns (0.4 pts)")
                    total_score += 0.4
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: specialty_coffee_global.ods covers all 5 required cities
    #              with at least 4 shops each (0.3 points)
    # Fails on initial_env (0 data rows) → Passes on golden_env
    # -------------------------------------------------------------------------
    try:
        if not os.path.exists(ODS_PATH):
            print(f"FAIL: Component 2 — {ODS_PATH} does not exist")
        else:
            rows = extract_ods_rows(ODS_PATH)
            if rows is None or len(rows) < 2:
                print("FAIL: Component 2 — ODS is empty or not valid")
            else:
                header = [c.strip() for c in rows[0]]
                if 'City' not in header:
                    print("FAIL: Component 2 — ODS missing 'City' column")
                else:
                    city_idx = header.index('City')
                    city_counts = {}
                    for row in rows[1:]:
                        if len(row) > city_idx:
                            city = row[city_idx].strip()
                            if city:
                                city_counts[city] = city_counts.get(city, 0) + 1

                    # Check all 5 cities are represented with 4+ shops
                    missing_cities = []
                    insufficient_cities = []
                    for city in REQUIRED_CITIES:
                        count = city_counts.get(city, 0)
                        if count == 0:
                            missing_cities.append(city)
                        elif count < 4:
                            insufficient_cities.append(f"{city}({count})")

                    if missing_cities:
                        print(f"FAIL: Component 2 — Cities missing from ODS: {missing_cities}")
                    elif insufficient_cities:
                        print(f"FAIL: Component 2 — Cities with <4 shops: {insufficient_cities}")
                    else:
                        print(f"PASS: Component 2 — All 5 cities present with 4+ shops each: {city_counts} (0.3 pts)")
                        total_score += 0.3
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: coffee_city_guide.odt has real content — 5 tables (one per
    #              city) and no placeholder text (0.3 points)
    # Fails on initial_env (0 tables, 5 placeholder paras) → Passes on golden_env
    # -------------------------------------------------------------------------
    try:
        if not os.path.exists(ODT_PATH):
            print(f"FAIL: Component 3 — {ODT_PATH} does not exist")
        else:
            info = extract_odt_info(ODT_PATH)
            if info is None:
                print("FAIL: Component 3 — coffee_city_guide.odt is not a valid ODT file")
            else:
                tables_count = info['tables_count']
                has_placeholders = info['has_placeholders']

                if has_placeholders:
                    print(f"FAIL: Component 3 — coffee_city_guide.odt still contains placeholder text")
                elif tables_count < 5:
                    print(f"FAIL: Component 3 — coffee_city_guide.odt has {tables_count} tables, expected 5 (one per city)")
                else:
                    print(f"PASS: Component 3 — coffee_city_guide.odt has {tables_count} tables and no placeholders (0.3 pts)")
                    total_score += 0.3
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
