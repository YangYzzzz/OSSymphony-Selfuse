"""
Reward Script: Add AutoCorrect exception for 'vs.' abbreviation
Task ID: writer_frd_056
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6 pts): 'vs.' found in SentenceExceptList.xml abbreviations
  Component 2 (0.4 pts): 'vs.' entry is properly formed XML block-list entry
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_056'

# Path to LibreOffice autocorrect data for en-US
ACOR_DAT_PATH = os.path.join(
    WORKDIR, '.config', 'libreoffice', '4', 'user', 'autocorr', 'acor_en-US.dat'
)
SENTENCE_EXCEPT_FILE = 'SentenceExceptList.xml'
TARGET_ABBREV = 'vs.'

BLOCK_LIST_NS = 'http://openoffice.org/2001/block-list'


def verify_task():
    """
    Verify that 'vs.' has been added to the AutoCorrect sentence exception list.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: acor_en-US.dat must exist
    if not os.path.exists(ACOR_DAT_PATH):
        print(f"CRITICAL: AutoCorrect data file not found: {ACOR_DAT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be a valid zip with SentenceExceptList.xml
    try:
        zf = zipfile.ZipFile(ACOR_DAT_PATH, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open acor_en-US.dat as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        if SENTENCE_EXCEPT_FILE not in zf.namelist():
            print(f"CRITICAL: {SENTENCE_EXCEPT_FILE} not found in acor_en-US.dat")
            print("REWARD: 0.0")
            return 0.0

        xml_content = zf.read(SENTENCE_EXCEPT_FILE).decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot read {SENTENCE_EXCEPT_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0
    finally:
        zf.close()

    # Component 1: 'vs.' found in SentenceExceptList.xml abbreviations (0.6 points)
    try:
        # Parse the XML and extract all abbreviated-name values
        root = ET.fromstring(xml_content)
        ns = {'bl': BLOCK_LIST_NS}
        abbrevs = []
        for block in root.findall('bl:block', ns):
            name = block.get(f'{{{BLOCK_LIST_NS}}}abbreviated-name')
            if name is not None:
                abbrevs.append(name)

        # Check if 'vs.' is in the list (case-sensitive, as LibreOffice stores it)
        if TARGET_ABBREV in abbrevs:
            print(f"PASS: Component 1 — '{TARGET_ABBREV}' found in sentence exception list (0.6 pts)")
            total_score += 0.6
        elif TARGET_ABBREV.upper() in abbrevs or TARGET_ABBREV.lower() in abbrevs:
            # Accept case variants (Vs., VS.) with partial credit
            found_variant = [a for a in abbrevs if a.lower() == TARGET_ABBREV.lower()][0]
            print(f"PARTIAL: Component 1 — found case variant '{found_variant}' instead of '{TARGET_ABBREV}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — '{TARGET_ABBREV}' NOT found in sentence exception list")
            print(f"  Exception list has {len(abbrevs)} entries")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'vs.' entry is a properly formed block-list entry (0.4 points)
    # This verifies the entry is not just text-injected but is a valid XML element
    try:
        root = ET.fromstring(xml_content)
        ns = {'bl': BLOCK_LIST_NS}
        matching_blocks = [
            block for block in root.findall('bl:block', ns)
            if block.get(f'{{{BLOCK_LIST_NS}}}abbreviated-name', '').lower() == TARGET_ABBREV.lower()
            and block.tag == f'{{{BLOCK_LIST_NS}}}block'
        ]

        if len(matching_blocks) > 0:
            print(f"PASS: Component 2 — '{TARGET_ABBREV}' is a properly formed block-list:block element (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — '{TARGET_ABBREV}' not found as proper block-list:block element")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
