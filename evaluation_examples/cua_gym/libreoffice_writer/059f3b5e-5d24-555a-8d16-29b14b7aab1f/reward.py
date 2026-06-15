"""
Reward Script: Delete all but most recent version from document version history
Task ID: writer_lec_082
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): VersionList.xml has exactly 1 version entry
  Component 2 (0.3): Only Version8.xml exists in Versions/ dir (1-7 removed)
  Component 3 (0.3): Remaining version is Version8 with correct metadata
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_082'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid ZIP/ODT
    try:
        zf = zipfile.ZipFile(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: VersionList.xml has exactly 1 version entry (0.4 points)
    # Initial has 8 entries; golden should have 1.
    try:
        if 'VersionList.xml' not in zf.namelist():
            print("FAIL: Component 1 — VersionList.xml not found in ODT")
        else:
            vl_xml = zf.read('VersionList.xml').decode('utf-8')
            ns = {
                'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
                'framework': 'urn:oasis:names:tc:opendocument:xmlns:framework:1.0',
                'dc': 'http://purl.org/dc/elements/1.1/'
            }
            root = ET.fromstring(vl_xml)
            version_entries = root.findall('.//framework:version-entry', ns)
            num_versions = len(version_entries)
            if num_versions == 1:
                print(f"PASS: Component 1 — VersionList.xml has exactly 1 version entry (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — VersionList.xml has {num_versions} version entries, expected 1")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Only Version8.xml exists in Versions/ directory (0.3 points)
    # Initial has Version1-8.xml; golden should only have Version8.xml
    try:
        version_files = [n for n in zf.namelist() if n.startswith('Versions/') and n.endswith('.xml')]
        old_versions = [n for n in version_files if n != 'Versions/Version8.xml']
        has_version8 = 'Versions/Version8.xml' in version_files

        if has_version8 and len(old_versions) == 0:
            print(f"PASS: Component 2 — Only Version8.xml in Versions/ dir, old versions removed (0.3 pts)")
            total_score += 0.3
        elif not has_version8:
            print(f"FAIL: Component 2 — Version8.xml is missing from Versions/ dir")
        else:
            print(f"FAIL: Component 2 — Old version files still present: {old_versions}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Remaining version entry is Version8 with correct metadata (0.3 points)
    # Verifies the kept version is the most recent one (Version8) with expected title/comment
    try:
        if 'VersionList.xml' not in zf.namelist():
            print("FAIL: Component 3 — VersionList.xml not found")
        else:
            vl_xml = zf.read('VersionList.xml').decode('utf-8')
            ns = {
                'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
                'framework': 'urn:oasis:names:tc:opendocument:xmlns:framework:1.0',
                'dc': 'http://purl.org/dc/elements/1.1/'
            }
            root = ET.fromstring(vl_xml)
            version_entries = root.findall('.//framework:version-entry', ns)

            if len(version_entries) != 1:
                print(f"FAIL: Component 3 — Expected 1 version entry, found {len(version_entries)}")
            else:
                entry = version_entries[0]
                title = entry.get('{urn:oasis:names:tc:opendocument:xmlns:framework:1.0}title', '')
                comment = entry.get('{urn:oasis:names:tc:opendocument:xmlns:framework:1.0}comment', '')

                # Check that the remaining version is Version8 (most recent)
                is_version8_title = 'Version8' in title or '8' in title
                is_final_comment = 'Final' in comment or 'final' in comment or 'board' in comment.lower()

                if is_version8_title and is_final_comment:
                    print(f"PASS: Component 3 — Remaining version is Version8: title='{title}', comment='{comment}' (0.3 pts)")
                    total_score += 0.3
                elif is_version8_title:
                    # Title matches but comment may differ - still give partial
                    print(f"PASS: Component 3 — Remaining version is Version8: title='{title}' (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — Remaining version is not Version8: title='{title}', comment='{comment}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
