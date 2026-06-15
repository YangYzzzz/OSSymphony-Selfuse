"""
Reward Script: Verify auto-text entries for standard contract clauses
Task ID: writer_biz_078
Domain: libreoffice_writer
Scoring:
  Component 1: 'indemnity' entry registered in BlockList.xml (0.2 pts)
  Component 2: 'confid' entry registered in BlockList.xml (0.2 pts)
  Component 3: 'indemnity' entry contains indemnification clause text (0.3 pts)
  Component 4: 'confid' entry contains confidentiality clause text (0.3 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import glob

TASK_ID = 'writer_biz_078'

# Auto-text .bau files can be in the user autotext directory
AUTOTEXT_DIR = '/home/user/.config/libreoffice/4/user/autotext'

# Key phrases that must appear in each auto-text entry to confirm correct content
INDEMNITY_KEYWORDS = [
    'indemnify',
    'hold harmless',
    'claims',
    'damages',
]

CONFID_KEYWORDS = [
    'confidential',
    'non-public information',
    'strict confidence',
    'not disclose',
]


def find_bau_files():
    """Find all .bau files in the LibreOffice autotext directory."""
    bau_files = []
    if os.path.isdir(AUTOTEXT_DIR):
        for f in os.listdir(AUTOTEXT_DIR):
            if f.endswith('.bau'):
                bau_files.append(os.path.join(AUTOTEXT_DIR, f))
    return bau_files


def parse_blocklist(bau_path):
    """Parse BlockList.xml from a .bau archive to get entry names."""
    entries = []
    try:
        with zipfile.ZipFile(bau_path, 'r') as z:
            if 'BlockList.xml' in z.namelist():
                data = z.read('BlockList.xml').decode('utf-8')
                root = ET.fromstring(data)
                ns = {'bl': 'http://openoffice.org/2001/block-list'}
                for block in root.findall('.//bl:block', ns):
                    abbr = block.get('{http://openoffice.org/2001/block-list}abbreviated-name', '')
                    name = block.get('{http://openoffice.org/2001/block-list}name', '')
                    entries.append((abbr.lower(), name.lower()))
    except Exception as e:
        print(f"ERROR: Could not parse BlockList in {bau_path}: {e}")
    return entries


def get_entry_text(bau_path, entry_name):
    """Extract text content from an auto-text entry XML file inside a .bau archive."""
    text_parts = []
    try:
        with zipfile.ZipFile(bau_path, 'r') as z:
            # The entry XML could be named entry_name.xml
            xml_name = f'{entry_name}.xml'
            if xml_name not in z.namelist():
                # Try case-insensitive match
                for n in z.namelist():
                    if n.lower() == xml_name.lower():
                        xml_name = n
                        break
                else:
                    return ''
            data = z.read(xml_name).decode('utf-8')
            root = ET.fromstring(data)
            # Extract all text content from the XML
            for elem in root.iter():
                if elem.text:
                    text_parts.append(elem.text)
                if elem.tail:
                    text_parts.append(elem.tail)
    except Exception as e:
        print(f"ERROR: Could not read entry '{entry_name}' from {bau_path}: {e}")
    return ' '.join(text_parts)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find all .bau files
    bau_files = find_bau_files()
    if not bau_files:
        print("CRITICAL: No .bau autotext files found in LibreOffice autotext directory")
        print("REWARD: 0.0")
        return 0.0

    # Collect all entries across all .bau files
    all_entries = {}  # abbr_name -> bau_path
    for bau_path in bau_files:
        entries = parse_blocklist(bau_path)
        for abbr, name in entries:
            all_entries[abbr] = bau_path
            if name and name != abbr:
                all_entries[name] = bau_path

    print(f"INFO: Found autotext entries: {list(all_entries.keys())}")

    # Component 1: 'indemnity' entry registered in BlockList (0.2 points)
    try:
        if 'indemnity' in all_entries:
            print(f"PASS: Component 1 — 'indemnity' entry found in BlockList (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — 'indemnity' entry not found in any BlockList. Found: {list(all_entries.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'confid' entry registered in BlockList (0.2 points)
    try:
        if 'confid' in all_entries:
            print(f"PASS: Component 2 — 'confid' entry found in BlockList (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — 'confid' entry not found in any BlockList. Found: {list(all_entries.keys())}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'indemnity' entry contains indemnification clause text (0.3 points)
    try:
        if 'indemnity' in all_entries:
            bau_path = all_entries['indemnity']
            text = get_entry_text(bau_path, 'indemnity').lower()
            if not text:
                print(f"FAIL: Component 3 — 'indemnity' entry XML is empty or missing")
            else:
                matched = sum(1 for kw in INDEMNITY_KEYWORDS if kw.lower() in text)
                if matched >= 3:
                    print(f"PASS: Component 3 — 'indemnity' entry contains indemnification clause ({matched}/{len(INDEMNITY_KEYWORDS)} keywords matched) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — 'indemnity' entry text does not contain enough indemnification keywords ({matched}/{len(INDEMNITY_KEYWORDS)} matched)")
                    print(f"  Text preview: {text[:200]}")
        else:
            print(f"FAIL: Component 3 — 'indemnity' entry not found, cannot check content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'confid' entry contains confidentiality clause text (0.3 points)
    try:
        if 'confid' in all_entries:
            bau_path = all_entries['confid']
            text = get_entry_text(bau_path, 'confid').lower()
            if not text:
                print(f"FAIL: Component 4 — 'confid' entry XML is empty or missing")
            else:
                matched = sum(1 for kw in CONFID_KEYWORDS if kw.lower() in text)
                if matched >= 3:
                    print(f"PASS: Component 4 — 'confid' entry contains confidentiality clause ({matched}/{len(CONFID_KEYWORDS)} keywords matched) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 4 — 'confid' entry text does not contain enough confidentiality keywords ({matched}/{len(CONFID_KEYWORDS)} matched)")
                    print(f"  Text preview: {text[:200]}")
        else:
            print(f"FAIL: Component 4 — 'confid' entry not found, cannot check content")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
