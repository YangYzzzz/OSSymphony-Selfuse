"""
Reward Script: Configure AutoCorrect to replace 'teh' -> 'the' and 'adn' -> 'and'
Task ID: osworld_writer_spell_check_autocorrect_003
Domain: libreoffice_writer
Scoring:
  Component 1: User-level acor_en-US.dat exists (0.2 points)
  Component 2: 'teh' -> 'the' entry present in user autocorrect file (0.4 points)
  Component 3: 'adn' -> 'and' entry present in user autocorrect file (0.4 points)
  Total: 1.0
"""

import os
import zipfile
import io
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_spell_check_autocorrect_003'

# Path to the user-level LibreOffice AutoCorrect file
AUTOCORR_PATH = '/home/user/.config/libreoffice/4/user/autocorr/acor_en-US.dat'
AUTOCORR_NS = 'http://openoffice.org/2001/block-list'


def load_autocorr_entries(dat_path):
    """
    Load autocorrect entries from an acor_en-US.dat file (a zip archive).
    Returns a dict {abbreviated_name: replacement_name} or raises on error.
    """
    with open(dat_path, 'rb') as f:
        data = f.read()

    zf = zipfile.ZipFile(io.BytesIO(data))
    if 'DocumentList.xml' not in zf.namelist():
        raise ValueError("DocumentList.xml not found in autocorr archive")

    content = zf.read('DocumentList.xml').decode('utf-8', errors='replace')
    root = ET.fromstring(content)
    entries = {}
    for block in root.findall('{%s}block' % AUTOCORR_NS):
        abbr = block.get('{%s}abbreviated-name' % AUTOCORR_NS)
        name = block.get('{%s}name' % AUTOCORR_NS)
        if abbr is not None and name is not None:
            entries[abbr] = name
    return entries


def verify_task():
    """
    Verify that the user-level AutoCorrect file contains the required entries:
    - 'teh' -> 'the'
    - 'adn' -> 'and'
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Component 1: User-level acor_en-US.dat file exists (0.2 points)
    # This FAILS on initial_env (no user autocorr file) and PASSES on golden_env
    try:
        if os.path.isfile(AUTOCORR_PATH):
            print("PASS: Component 1 — User-level acor_en-US.dat exists (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 1 — User-level acor_en-US.dat not found at: " + AUTOCORR_PATH)
            # Cannot proceed to check entries if file doesn't exist
            print("\nScore: 0.0/1.0")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print("ERROR: Component 1 — " + str(e))
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Load entries from user autocorr file
    try:
        entries = load_autocorr_entries(AUTOCORR_PATH)
        print("INFO: Loaded " + str(len(entries)) + " entries from user autocorr file")
    except Exception as e:
        print("ERROR: Cannot load autocorr entries — " + str(e))
        print("\nScore: " + str(total_score) + "/1.0")
        final_score = min(total_score, 1.0)
        print("REWARD: " + str(final_score))
        return final_score

    # Component 2: 'teh' -> 'the' entry present (0.4 points)
    # This FAILS on initial_env (no user autocorr file) and PASSES on golden_env
    try:
        teh_value = entries.get('teh')
        if teh_value == 'the':
            print("PASS: Component 2 — 'teh' -> 'the' autocorrect entry found (0.4 pts)")
            total_score += 0.4
        elif teh_value is not None:
            print("FAIL: Component 2 — 'teh' maps to '" + str(teh_value) + "', expected 'the'")
        else:
            print("FAIL: Component 2 — 'teh' entry not found in user autocorr file")
    except Exception as e:
        print("ERROR: Component 2 — " + str(e))

    # Component 3: 'adn' -> 'and' entry present (0.4 points)
    # This FAILS on initial_env (no user autocorr file) and PASSES on golden_env
    try:
        adn_value = entries.get('adn')
        if adn_value == 'and':
            print("PASS: Component 3 — 'adn' -> 'and' autocorrect entry found (0.4 pts)")
            total_score += 0.4
        elif adn_value is not None:
            print("FAIL: Component 3 — 'adn' maps to '" + str(adn_value) + "', expected 'and'")
        else:
            print("FAIL: Component 3 — 'adn' entry not found in user autocorr file")
    except Exception as e:
        print("ERROR: Component 3 — " + str(e))

    final_score = min(total_score, 1.0)
    print("\nScore: " + str(total_score) + "/1.0")
    print("REWARD: " + str(final_score))
    return final_score


verify_task()
