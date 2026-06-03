"""
Reward Script: Register CSV as data source for mail merge in LibreOffice
Task ID: writer_mt_002
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Employees.odb file exists
  Component 2 (0.30): Data source 'Employees' registered in registrymodifications.xcu
  Component 3 (0.25): ODB contains valid CSV flat-file connection to employees.csv
  Component 4 (0.15): ODB references 'employees' table
"""

import os
import re
import zipfile
import io

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_002'

# Possible ODB paths — the agent might place it in different locations
ODB_CANDIDATES = [
    os.path.join(WORKDIR, 'Employees.odb'),
    os.path.join(WORKDIR, 'employees.odb'),
    os.path.join(WORKDIR, 'Desktop', 'Employees.odb'),
    os.path.join(WORKDIR, 'Desktop', 'employees.odb'),
    os.path.join(WORKDIR, 'Documents', 'Employees.odb'),
    os.path.join(WORKDIR, 'Documents', 'employees.odb'),
]

REGISTRY_PATH = os.path.join(
    WORKDIR, '.config', 'libreoffice', '4', 'user', 'registrymodifications.xcu'
)


def find_odb_file():
    """Find the Employees.odb file in candidate locations."""
    for path in ODB_CANDIDATES:
        if os.path.isfile(path):
            return path
    # Broader search in home directory
    for root, dirs, files in os.walk(WORKDIR):
        # Skip hidden dirs except .config
        dirs[:] = [d for d in dirs if not d.startswith('.') or d == '.config']
        for f in files:
            if f.lower() == 'employees.odb':
                return os.path.join(root, f)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Employees.odb file exists (0.30 points)
    odb_path = None
    try:
        odb_path = find_odb_file()
        if odb_path:
            size = os.path.getsize(odb_path)
            if size > 100:  # Must be a non-trivial file
                print(f"PASS: Component 1 — Employees.odb found at {odb_path} ({size} bytes) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 — Employees.odb at {odb_path} is too small ({size} bytes)")
        else:
            print("FAIL: Component 1 — No Employees.odb file found anywhere in /home/user/")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Data source 'Employees' registered in registrymodifications.xcu (0.30 points)
    try:
        if os.path.isfile(REGISTRY_PATH):
            with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
                registry_content = f.read()

            # Look for RegisteredNames entry with 'Employees' (case-insensitive name match)
            # Pattern: org.openoffice.Office.DataAccess/RegisteredNames with node name containing employees
            pattern = r'org\.openoffice\.Office\.DataAccess/RegisteredNames.*?node\s+oor:name="([^"]*[Ee]mployees[^"]*)"'
            match = re.search(pattern, registry_content)

            if match:
                ds_name = match.group(1)
                # Also check the Location points to an .odb file
                loc_pattern = r'oor:name="' + re.escape(ds_name) + r'".*?<prop\s+oor:name="Location"[^>]*>.*?<value>(.*?)</value>'
                loc_match = re.search(loc_pattern, registry_content, re.DOTALL)
                if loc_match:
                    location = loc_match.group(1)
                    if '.odb' in location.lower():
                        print(f"PASS: Component 2 — Data source '{ds_name}' registered, Location: {location} (0.30 pts)")
                        total_score += 0.30
                    else:
                        print(f"FAIL: Component 2 — Data source '{ds_name}' registered but Location '{location}' is not an .odb file")
                else:
                    # Registration found but could not parse location — still give partial
                    print(f"PASS: Component 2 — Data source '{ds_name}' registered (location parse ambiguous) (0.30 pts)")
                    total_score += 0.30
            else:
                # Also check for any RegisteredNames entry case-insensitively
                if 'RegisteredNames' in registry_content and 'employees' in registry_content.lower():
                    print(f"PASS: Component 2 — Data source registration found (alternate pattern) (0.30 pts)")
                    total_score += 0.30
                else:
                    print("FAIL: Component 2 — No 'Employees' data source found in registrymodifications.xcu")
        else:
            print(f"FAIL: Component 2 — Registry file not found: {REGISTRY_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ODB contains valid CSV flat-file connection (0.25 points)
    if odb_path:
        try:
            with open(odb_path, 'rb') as f:
                data = f.read()
            z = zipfile.ZipFile(io.BytesIO(data))
            if 'content.xml' in z.namelist():
                content_xml = z.read('content.xml').decode('utf-8')
                # Check for flat-file connection to CSV
                has_flat_connection = 'sdbc:flat:' in content_xml or 'sdbc:csv:' in content_xml
                has_csv_ref = 'csv' in content_xml.lower() or 'employees' in content_xml.lower()
                has_desktop_path = 'Desktop' in content_xml or 'desktop' in content_xml

                if has_flat_connection and has_csv_ref:
                    print(f"PASS: Component 3 — ODB contains flat-file CSV connection (0.25 pts)")
                    total_score += 0.25
                elif has_csv_ref:
                    print(f"PARTIAL: Component 3 — ODB references CSV but connection type unclear (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 3 — ODB content.xml does not reference CSV connection")
                    print(f"  content.xml snippet: {content_xml[:500]}")
            else:
                print(f"FAIL: Component 3 — ODB file does not contain content.xml")
        except zipfile.BadZipFile:
            print(f"FAIL: Component 3 — ODB file is not a valid zip/odb archive")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")
    else:
        print("FAIL: Component 3 — Skipped (no ODB file found)")

    # Component 4: ODB references 'employees' table (0.15 points)
    if odb_path:
        try:
            with open(odb_path, 'rb') as f:
                data = f.read()
            z = zipfile.ZipFile(io.BytesIO(data))
            if 'content.xml' in z.namelist():
                content_xml = z.read('content.xml').decode('utf-8')
                # Check for table reference to employees
                if re.search(r'db:name="[^"]*employees[^"]*"', content_xml, re.IGNORECASE):
                    print(f"PASS: Component 4 — ODB references 'employees' table (0.15 pts)")
                    total_score += 0.15
                elif 'employees' in content_xml.lower():
                    print(f"PASS: Component 4 — ODB mentions 'employees' (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — ODB does not reference 'employees' table")
            else:
                print(f"FAIL: Component 4 — No content.xml in ODB")
        except Exception as e:
            print(f"ERROR: Component 4 — {e}")
    else:
        print("FAIL: Component 4 — Skipped (no ODB file found)")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
