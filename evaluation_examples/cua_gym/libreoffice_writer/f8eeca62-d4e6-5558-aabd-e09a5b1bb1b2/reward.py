"""
Reward Script: Verify LibreOffice Writer autocorrect legal abbreviation entries
Task ID: writer_legal_088
Domain: libreoffice_writer
Scoring: 5 autocorrect entries x 0.2 points each = 1.0 total
  - Plf -> Plaintiff (0.2)
  - Def -> Defendant (0.2)
  - Jdg -> Judgment (0.2)
  - Mtn -> Motion (0.2)
  - Stip -> Stipulation (0.2)
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import glob

TASK_ID = 'writer_legal_088'

# Required autocorrect entries: abbreviation -> replacement
REQUIRED_ENTRIES = {
    'Plf': 'Plaintiff',
    'Def': 'Defendant',
    'Jdg': 'Judgment',
    'Mtn': 'Motion',
    'Stip': 'Stipulation',
}

# Points per entry
POINTS_PER_ENTRY = 0.2


def find_autocorrect_dat():
    """
    Find the LibreOffice autocorrect .dat file for English.
    Searches common paths for the user-level autocorrect data.
    """
    search_paths = [
        '/home/user/.config/libreoffice/4/user/autocorr/acor_en-US.dat',
        '/home/user/.config/libreoffice/4/user/autocorr/acor_en-GB.dat',
    ]
    # Also glob for any acor_en*.dat in the autocorr directory
    glob_pattern = '/home/user/.config/libreoffice/*/user/autocorr/acor_en*.dat'
    found = glob.glob(glob_pattern)

    for path in search_paths + found:
        if os.path.exists(path):
            return path
    return None


def parse_autocorrect_entries(dat_path):
    """
    Parse the autocorrect .dat file (ZIP archive) and extract all
    abbreviation -> replacement mappings from DocumentList.xml.
    Returns a dict of {abbreviated_name: replacement_name}.
    """
    entries = {}
    try:
        with zipfile.ZipFile(dat_path, 'r') as zf:
            if 'DocumentList.xml' not in zf.namelist():
                print("FAIL: DocumentList.xml not found in autocorrect archive")
                return entries
            content = zf.read('DocumentList.xml').decode('utf-8')

        root = ET.fromstring(content)
        ns_uri = 'http://openoffice.org/2001/block-list'
        ns = {'bl': ns_uri}

        for block in root.findall('bl:block', ns):
            abbr = block.get(f'{{{ns_uri}}}abbreviated-name')
            name = block.get(f'{{{ns_uri}}}name')
            if abbr and name:
                entries[abbr] = name
    except zipfile.BadZipFile as e:
        print(f"ERROR: Invalid ZIP file: {e}")
    except ET.ParseError as e:
        print(f"ERROR: XML parse error: {e}")
    except Exception as e:
        print(f"ERROR: Unexpected error parsing autocorrect data: {e}")

    return entries


def verify_task():
    """
    Verify that the 5 required legal abbreviation autocorrect entries exist.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find the autocorrect dat file
    dat_path = find_autocorrect_dat()
    if dat_path is None:
        print("FAIL: No autocorrect .dat file found in LibreOffice user config")
        print("  Searched: /home/user/.config/libreoffice/*/user/autocorr/acor_en*.dat")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found autocorrect file: {dat_path}")

    # Parse all autocorrect entries from the file
    all_entries = parse_autocorrect_entries(dat_path)
    if not all_entries:
        print("FAIL: No autocorrect entries found or parse error")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Total autocorrect entries in file: {len(all_entries)}")

    # Component 1-5: Check each required legal abbreviation entry (0.2 pts each)
    for abbr, expected_replacement in REQUIRED_ENTRIES.items():
        try:
            if abbr in all_entries:
                actual = all_entries[abbr]
                if actual == expected_replacement:
                    print(f"PASS: '{abbr}' -> '{actual}' matches expected '{expected_replacement}' ({POINTS_PER_ENTRY} pts)")
                    total_score += POINTS_PER_ENTRY
                else:
                    print(f"FAIL: '{abbr}' -> '{actual}' does NOT match expected '{expected_replacement}'")
            else:
                print(f"FAIL: Autocorrect entry '{abbr}' not found")
        except Exception as e:
            print(f"ERROR: Checking entry '{abbr}': {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
