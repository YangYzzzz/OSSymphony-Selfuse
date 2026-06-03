"""
Reward Script: Create 'Legal Templates' AutoText category with three legal clause entries
Task ID: writer_frd_055
Domain: libreoffice_writer
Scoring:
  Component 1 (0.2): 'Legal Templates' category exists in .bau file with correct list-name
  Component 2 (0.3): 'Force Majeure' entry (shortcut 'fmaj') with legal clause text
  Component 3 (0.25): 'Indemnification' entry (shortcut 'indem') with legal clause text
  Component 4 (0.25): 'Governing Law' entry (shortcut 'glaw') with legal clause text
"""

import os
import glob
import zipfile
import xml.etree.ElementTree as ET

AUTOTEXT_DIR = '/home/user/.config/libreoffice/4/user/autotext'
TASK_ID = 'writer_frd_055'

# Also check common alternative paths
AUTOTEXT_DIRS = [
    '/home/user/.config/libreoffice/4/user/autotext',
    '/home/user/.config/libreoffice/4/user/pack/autotext',
]


def find_legal_templates_bau():
    """Search for a .bau file that contains a 'Legal Templates' category."""
    for autotext_dir in AUTOTEXT_DIRS:
        if not os.path.isdir(autotext_dir):
            continue
        for bau_file in glob.glob(os.path.join(autotext_dir, '*.bau')):
            try:
                with zipfile.ZipFile(bau_file, 'r') as z:
                    if 'BlockList.xml' in z.namelist():
                        content = z.read('BlockList.xml').decode('utf-8')
                        # Check if list-name contains "Legal Templates" (case-insensitive)
                        if 'legal' in content.lower() and 'template' in content.lower():
                            return bau_file
            except Exception:
                continue
    return None


def parse_block_list(bau_path):
    """Parse the BlockList.xml from a .bau file and return category name and entries."""
    entries = {}
    list_name = None
    try:
        with zipfile.ZipFile(bau_path, 'r') as z:
            content = z.read('BlockList.xml').decode('utf-8')
            root = ET.fromstring(content)
            # Extract list-name attribute
            for attr_name, attr_val in root.attrib.items():
                if 'list-name' in attr_name:
                    list_name = attr_val
            # Extract block entries
            for block in root:
                tag = block.tag
                if 'block' in tag.lower():
                    abbrev = None
                    name = None
                    pkg = None
                    for attr_name, attr_val in block.attrib.items():
                        if 'abbreviated-name' in attr_name:
                            abbrev = attr_val
                        if attr_name.endswith('}name') or attr_name == 'name':
                            # Distinguish between 'name' and 'abbreviated-name'
                            if 'abbreviated' not in attr_name and 'package' not in attr_name:
                                name = attr_val
                        if 'package-name' in attr_name:
                            pkg = attr_val
                    if abbrev:
                        entries[abbrev] = {'name': name, 'package': pkg}
    except Exception as e:
        print(f"ERROR: Failed to parse BlockList.xml: {e}")
    return list_name, entries


def get_entry_text(bau_path, package_name, abbrev):
    """Extract the text content of an AutoText entry from its XML inside the .bau."""
    try:
        with zipfile.ZipFile(bau_path, 'r') as z:
            # Try common naming patterns
            xml_candidates = [
                f'{package_name}/{abbrev}.xml',
                f'{abbrev}/{abbrev}.xml',
                f'{package_name}/{package_name}.xml',
            ]
            for candidate in xml_candidates:
                if candidate in z.namelist():
                    content = z.read(candidate).decode('utf-8')
                    # Parse and extract text
                    root = ET.fromstring(content)
                    # Collect all text from all elements
                    texts = []
                    for elem in root.iter():
                        if elem.text and elem.text.strip():
                            texts.append(elem.text.strip())
                    return ' '.join(texts)
    except Exception as e:
        print(f"ERROR: Failed to read entry text for {abbrev}: {e}")
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: find the .bau file containing Legal Templates
    bau_path = find_legal_templates_bau()
    if bau_path is None:
        print("CRITICAL: No .bau file found with 'Legal Templates' category")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found .bau file: {bau_path}")
    list_name, entries = parse_block_list(bau_path)

    # Component 1: Category named 'Legal Templates' (0.2 points)
    try:
        if list_name and 'legal templates' in list_name.lower():
            print(f"PASS: Component 1 - Category name is '{list_name}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 - Expected 'Legal Templates' category, found: {list_name}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: 'Force Majeure' entry with shortcut 'fmaj' and legal text (0.3 points)
    try:
        if 'fmaj' in entries:
            entry = entries['fmaj']
            name_ok = entry.get('name') and 'force majeure' in entry['name'].lower()
            text = get_entry_text(bau_path, entry.get('package', 'fmaj'), 'fmaj')
            # Check that text is substantial legal clause (at least 50 chars with legal keywords)
            text_ok = (text is not None and len(text) > 50 and
                       any(kw in text.lower() for kw in ['liable', 'party', 'force majeure', 'obligation']))
            if name_ok and text_ok:
                print(f"PASS: Component 2 - 'Force Majeure' (fmaj) with legal text ({len(text)} chars) (0.3 pts)")
                total_score += 0.3
            elif name_ok:
                print(f"PARTIAL: Component 2 - Name correct but text insufficient (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 2 - Name mismatch: {entry.get('name')}")
        else:
            print(f"FAIL: Component 2 - No entry with shortcut 'fmaj' found. Available: {list(entries.keys())}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: 'Indemnification' entry with shortcut 'indem' and legal text (0.25 points)
    try:
        if 'indem' in entries:
            entry = entries['indem']
            name_ok = entry.get('name') and 'indemnif' in entry['name'].lower()
            text = get_entry_text(bau_path, entry.get('package', 'indem'), 'indem')
            text_ok = (text is not None and len(text) > 50 and
                       any(kw in text.lower() for kw in ['indemnif', 'party', 'claim', 'damages']))
            if name_ok and text_ok:
                print(f"PASS: Component 3 - 'Indemnification' (indem) with legal text ({len(text)} chars) (0.25 pts)")
                total_score += 0.25
            elif name_ok:
                print(f"PARTIAL: Component 3 - Name correct but text insufficient (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3 - Name mismatch: {entry.get('name')}")
        else:
            print(f"FAIL: Component 3 - No entry with shortcut 'indem' found. Available: {list(entries.keys())}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: 'Governing Law' entry with shortcut 'glaw' and legal text (0.25 points)
    try:
        if 'glaw' in entries:
            entry = entries['glaw']
            name_ok = entry.get('name') and 'governing law' in entry['name'].lower()
            text = get_entry_text(bau_path, entry.get('package', 'glaw'), 'glaw')
            text_ok = (text is not None and len(text) > 50 and
                       any(kw in text.lower() for kw in ['govern', 'law', 'jurisdiction', 'court']))
            if name_ok and text_ok:
                print(f"PASS: Component 4 - 'Governing Law' (glaw) with legal text ({len(text)} chars) (0.25 pts)")
                total_score += 0.25
            elif name_ok:
                print(f"PARTIAL: Component 4 - Name correct but text insufficient (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 4 - Name mismatch: {entry.get('name')}")
        else:
            print(f"FAIL: Component 4 - No entry with shortcut 'glaw' found. Available: {list(entries.keys())}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
