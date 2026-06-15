"""
Reward Script: Add AutoCorrect exception for 'iPhone'
Task ID: writer_frd_064
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): User autocorr dat file exists with WordExceptList.xml
  Component 2 (0.5): 'iPhone' is listed in WordExceptList.xml as a TWo INitial Capitals exception
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_064'

# Path to the user-level AutoCorrect data file for en-US
AUTOCORR_DIR = os.path.join(WORKDIR, '.config', 'libreoffice', '4', 'user', 'autocorr')
AUTOCORR_DAT = os.path.join(AUTOCORR_DIR, 'acor_en-US.dat')


def verify_task():
    """
    Verify that 'iPhone' has been added as an AutoCorrect exception
    for TWo INitial Capitals in LibreOffice Writer.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: acor_en-US.dat exists and contains WordExceptList.xml (0.5 points)
    # This file is only created/modified when the user adds AutoCorrect exceptions.
    # On initial_env, there is no user-level acor_en-US.dat at all.
    try:
        if os.path.isfile(AUTOCORR_DAT):
            try:
                zf = zipfile.ZipFile(AUTOCORR_DAT, 'r')
                names = zf.namelist()
                if 'WordExceptList.xml' in names:
                    print(f"PASS: Component 1 -- acor_en-US.dat exists with WordExceptList.xml (0.5 pts)")
                    total_score += 0.5
                else:
                    print(f"FAIL: Component 1 -- acor_en-US.dat exists but missing WordExceptList.xml. Contents: {names}")
                zf.close()
            except zipfile.BadZipFile as e:
                print(f"FAIL: Component 1 -- acor_en-US.dat is not a valid ZIP: {e}")
        else:
            print(f"FAIL: Component 1 -- acor_en-US.dat not found at {AUTOCORR_DAT}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: 'iPhone' is in WordExceptList.xml (0.5 points)
    # The WordExceptList.xml stores words that should NOT be corrected for TWo INitial Capitals.
    # We parse the XML and check for an entry with abbreviated-name="iPhone".
    try:
        if os.path.isfile(AUTOCORR_DAT):
            zf = zipfile.ZipFile(AUTOCORR_DAT, 'r')
            if 'WordExceptList.xml' in zf.namelist():
                xml_content = zf.read('WordExceptList.xml').decode('utf-8')
                zf.close()

                # Parse XML to find iPhone entry
                # The namespace is http://openoffice.org/2001/block-list
                ns = {'bl': 'http://openoffice.org/2001/block-list'}
                root = ET.fromstring(xml_content)

                all_entries = [b.get('{http://openoffice.org/2001/block-list}abbreviated-name', '')
                               for b in root.findall('bl:block', ns)]

                if 'iPhone' in all_entries:
                    print(f"PASS: Component 2 -- 'iPhone' found in WordExceptList.xml (0.5 pts)")
                    total_score += 0.5
                else:
                    print(f"FAIL: Component 2 -- 'iPhone' not found in WordExceptList.xml. Entries: {all_entries}")
            else:
                zf.close()
                print(f"FAIL: Component 2 -- WordExceptList.xml not present in acor_en-US.dat")
        else:
            print(f"FAIL: Component 2 -- acor_en-US.dat not found, cannot check WordExceptList.xml")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
