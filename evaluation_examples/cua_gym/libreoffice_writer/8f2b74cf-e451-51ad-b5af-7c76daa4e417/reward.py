"""
Reward Script: Verify AutoText entry 'nsfgrant' in LibreOffice Writer
Task ID: writer_acad_089
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): 'nsfgrant' entry registered in BlockList.xml
  Component 2 (0.3): nsfgrant.xml content file exists in BAU archive
  Component 3 (0.3): nsfgrant.xml contains the exact acknowledgment phrase
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_089'

# AutoText .bau files live in the user's LO profile autotext directory
AUTOTEXT_DIR = '/home/user/.config/libreoffice/4/user/autotext'
EXPECTED_SHORTCUT = 'nsfgrant'
EXPECTED_TEXT = 'This research was supported by National Science Foundation Grant #NSF-2024-1234'


def find_bau_files():
    """Find all .bau files in the autotext directory."""
    bau_files = []
    if os.path.isdir(AUTOTEXT_DIR):
        for f in os.listdir(AUTOTEXT_DIR):
            if f.lower().endswith('.bau'):
                bau_files.append(os.path.join(AUTOTEXT_DIR, f))
    return bau_files


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    bau_files = find_bau_files()
    if not bau_files:
        print("CRITICAL: No .bau files found in autotext directory")
        print("REWARD: 0.0")
        return 0.0

    # Search all .bau files for the nsfgrant entry
    entry_found_in_blocklist = False
    nsfgrant_xml_exists = False
    nsfgrant_text_correct = False

    for bau_path in bau_files:
        try:
            zf = zipfile.ZipFile(bau_path, 'r')
        except Exception as e:
            print(f"WARN: Cannot open {bau_path}: {e}")
            continue

        # Component 1: Check BlockList.xml for 'nsfgrant' entry
        try:
            if 'BlockList.xml' in zf.namelist():
                blocklist_data = zf.read('BlockList.xml').decode('utf-8')
                # Parse XML to find abbreviated-name matching expected shortcut
                root = ET.fromstring(blocklist_data)
                ns = {'bl': 'http://openoffice.org/2001/block-list'}
                for block in root.findall('.//bl:block', ns):
                    abbr = block.get('{http://openoffice.org/2001/block-list}abbreviated-name', '')
                    if abbr.lower() == EXPECTED_SHORTCUT.lower():
                        entry_found_in_blocklist = True
                        break
        except Exception as e:
            print(f"WARN: Error parsing BlockList.xml in {bau_path}: {e}")

        # Component 2: Check if nsfgrant.xml exists in the archive
        try:
            possible_names = [f'{EXPECTED_SHORTCUT}.xml', f'{EXPECTED_SHORTCUT.upper()}.xml']
            for name in zf.namelist():
                if name.lower() == f'{EXPECTED_SHORTCUT.lower()}.xml':
                    nsfgrant_xml_exists = True

                    # Component 3: Check the text content of nsfgrant.xml
                    try:
                        content_data = zf.read(name).decode('utf-8')
                        # Parse the ODF content XML and extract text
                        content_root = ET.fromstring(content_data)
                        # Collect all text from text:p elements
                        text_ns = {
                            'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
                            'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
                        }
                        extracted_texts = []
                        for p_elem in content_root.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p'):
                            # Get all text including tail of child elements
                            full_text = ''.join(p_elem.itertext()).strip()
                            if full_text:
                                extracted_texts.append(full_text)

                        combined_text = ' '.join(extracted_texts).strip()
                        print(f"  Extracted text: '{combined_text}'")

                        if EXPECTED_TEXT in combined_text:
                            nsfgrant_text_correct = True
                        else:
                            print(f"  Text mismatch. Expected to contain: '{EXPECTED_TEXT}'")
                    except Exception as e:
                        print(f"WARN: Error reading content of {name}: {e}")
                    break
        except Exception as e:
            print(f"WARN: Error checking files in {bau_path}: {e}")

        zf.close()

        # If we found everything in this bau file, no need to check more
        if entry_found_in_blocklist and nsfgrant_xml_exists and nsfgrant_text_correct:
            break

    # Component 1: 'nsfgrant' entry registered in BlockList.xml (0.4 points)
    if entry_found_in_blocklist:
        print(f"PASS: Component 1 — 'nsfgrant' entry found in BlockList.xml (0.4 pts)")
        total_score += 0.4
    else:
        print(f"FAIL: Component 1 — 'nsfgrant' entry NOT found in any BlockList.xml")

    # Component 2: nsfgrant.xml content file exists in BAU archive (0.3 points)
    if nsfgrant_xml_exists:
        print(f"PASS: Component 2 — nsfgrant.xml found in BAU archive (0.3 pts)")
        total_score += 0.3
    else:
        print(f"FAIL: Component 2 — nsfgrant.xml NOT found in any BAU archive")

    # Component 3: nsfgrant.xml contains the exact acknowledgment phrase (0.3 points)
    if nsfgrant_text_correct:
        print(f"PASS: Component 3 — Correct acknowledgment text found (0.3 pts)")
        total_score += 0.3
    else:
        print(f"FAIL: Component 3 — Expected acknowledgment text not found in nsfgrant.xml")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
