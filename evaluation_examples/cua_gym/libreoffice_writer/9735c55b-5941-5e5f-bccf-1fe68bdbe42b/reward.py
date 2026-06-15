"""
Reward Script: Create AutoText entry for legal disclaimer paragraph
Task ID: writer_frd_051
Domain: libreoffice_writer
Scoring:
  Component 1: AutoText entry with shortcut 'ldisc' exists (0.3 pts)
  Component 2: AutoText entry display name is 'LegalDisc' (0.2 pts)
  Component 3: AutoText entry preserves formatting (unformatted-text=false) (0.2 pts)
  Component 4: AutoText entry contains the disclaimer text (0.3 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import glob

TASK_ID = 'writer_frd_051'

# AutoText .bau files are stored in user's LibreOffice autotext directory
AUTOTEXT_DIR = '/home/user/.config/libreoffice/4/user/autotext'

# The expected disclaimer text (core content to match)
EXPECTED_DISCLAIMER = (
    "DISCLAIMER: This document is provided for informational purposes only "
    "and does not constitute legal advice. The information contained herein "
    "is subject to change without notice. No liability is assumed for any "
    "errors or omissions."
)

def find_autotext_bau_files():
    """Find all .bau files in autotext directory."""
    if not os.path.isdir(AUTOTEXT_DIR):
        return []
    return glob.glob(os.path.join(AUTOTEXT_DIR, '*.bau'))

def parse_blocklist(bau_path):
    """Parse BlockList.xml from a .bau file to find autotext entries.
    Returns list of dicts with keys: abbreviated-name, name, package-name, unformatted-text
    """
    entries = []
    try:
        with zipfile.ZipFile(bau_path, 'r') as z:
            if 'BlockList.xml' not in z.namelist():
                return entries
            content = z.read('BlockList.xml').decode('utf-8')
            # Parse XML with namespace
            ns = {'bl': 'http://openoffice.org/2001/block-list'}
            root = ET.fromstring(content)
            for block in root.findall('.//bl:block', ns):
                entry = {}
                for attr_name in ['abbreviated-name', 'name', 'package-name', 'unformatted-text']:
                    full_attr = '{http://openoffice.org/2001/block-list}' + attr_name
                    entry[attr_name] = block.get(full_attr, '')
                entries.append(entry)
    except Exception as e:
        print(f"ERROR: Failed to parse {bau_path}: {e}")
    return entries

def get_autotext_content(bau_path, package_name):
    """Extract text content of an autotext entry from the .bau archive."""
    try:
        with zipfile.ZipFile(bau_path, 'r') as z:
            # The content XML is typically at <package>/<package>.xml
            xml_path = f"{package_name}/{package_name}.xml"
            if xml_path not in z.namelist():
                # Try other XML files in the package directory
                for name in z.namelist():
                    if name.startswith(package_name + '/') and name.endswith('.xml') and 'atevent' not in name:
                        xml_path = name
                        break
                else:
                    return None

            content = z.read(xml_path).decode('utf-8')
            # Extract text from XML body - parse all text nodes
            # Use a simple approach: strip XML tags to get text
            root = ET.fromstring(content)
            texts = []
            for elem in root.iter():
                if elem.text and elem.text.strip():
                    texts.append(elem.text.strip())
                if elem.tail and elem.tail.strip():
                    texts.append(elem.tail.strip())
            return ' '.join(texts)
    except Exception as e:
        print(f"ERROR: Failed to read content from {bau_path}/{package_name}: {e}")
    return None

def verify_task():
    """
    Verify AutoText entry creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find all .bau files
    bau_files = find_autotext_bau_files()
    if not bau_files:
        print("FAIL: No .bau files found in autotext directory")
        print("REWARD: 0.0")
        return 0.0

    # Search all .bau files for the 'ldisc' entry
    target_entry = None
    target_bau = None
    for bau_path in bau_files:
        entries = parse_blocklist(bau_path)
        for entry in entries:
            if entry.get('abbreviated-name', '').lower() == 'ldisc':
                target_entry = entry
                target_bau = bau_path
                break
        if target_entry:
            break

    # Component 1: AutoText entry with shortcut 'ldisc' exists (0.3 points)
    try:
        if target_entry is not None:
            print(f"PASS: Component 1 -- AutoText entry with shortcut 'ldisc' found in {os.path.basename(target_bau)} (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 -- No AutoText entry with shortcut 'ldisc' found in any .bau file")
            # If no entry found, remaining checks cannot pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Display name is 'LegalDisc' (0.2 points)
    try:
        display_name = target_entry.get('name', '')
        if display_name == 'LegalDisc':
            print(f"PASS: Component 2 -- Display name is 'LegalDisc' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- Expected display name 'LegalDisc', found: '{display_name}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Preserves formatting (unformatted-text="false") (0.2 points)
    try:
        unformatted = target_entry.get('unformatted-text', '')
        if unformatted.lower() == 'false':
            print(f"PASS: Component 3 -- AutoText preserves formatting (unformatted-text=false) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Expected unformatted-text='false', found: '{unformatted}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: AutoText content contains the disclaimer text (0.3 points)
    try:
        package_name = target_entry.get('package-name', 'ldisc')
        content_text = get_autotext_content(target_bau, package_name)
        if content_text is not None:
            # Normalize whitespace for comparison
            normalized_content = ' '.join(content_text.split())
            normalized_expected = ' '.join(EXPECTED_DISCLAIMER.split())
            if normalized_expected in normalized_content:
                print(f"PASS: Component 4 -- AutoText contains the full disclaimer text (0.3 pts)")
                total_score += 0.3
            else:
                # Check partial match - at least key phrases present
                key_phrases = [
                    "DISCLAIMER",
                    "informational purposes only",
                    "does not constitute legal advice",
                    "subject to change without notice",
                    "No liability is assumed"
                ]
                matches = sum(1 for phrase in key_phrases if phrase in normalized_content)
                if matches >= 4:
                    partial = 0.2
                    print(f"PARTIAL: Component 4 -- AutoText contains {matches}/5 key phrases (0.2 pts)")
                    total_score += partial
                elif matches >= 2:
                    partial = 0.1
                    print(f"PARTIAL: Component 4 -- AutoText contains {matches}/5 key phrases (0.1 pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 -- AutoText content does not match disclaimer. Found: '{normalized_content[:200]}'")
        else:
            print("FAIL: Component 4 -- Could not extract AutoText content from .bau file")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
