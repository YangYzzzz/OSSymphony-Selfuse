"""
Reward Script: Insert subdocuments into master document at specific positions
Task ID: writer_rm_069
Domain: libreoffice_writer
Scoring:
  Component 1 (0.2): Total subdocument count is 9
  Component 2 (0.2): Preface.odt is inserted before Ch1 (position 0)
  Component 3 (0.2): Midword.odt is inserted between Ch3 and Ch4
  Component 4 (0.2): Afterword.odt is inserted after Ch6 (last position)
  Component 5 (0.2): Full ordering matches exactly
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_069'

# Expected order of subdocuments in the golden master document
EXPECTED_ORDER = [
    'Preface.odt', 'Ch1.odt', 'Ch2.odt', 'Ch3.odt',
    'Midword.odt', 'Ch4.odt', 'Ch5.odt', 'Ch6.odt', 'Afterword.odt'
]


def extract_subdoc_order(odm_path):
    """
    Parse the ODM (ODF master document) content.xml to extract
    the ordered list of subdocument hrefs.
    Returns list of filenames like ['Preface.odt', 'Ch1.odt', ...].
    """
    ns = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'xlink': 'http://www.w3.org/1999/xlink',
    }

    z = zipfile.ZipFile(odm_path)
    content_xml = z.read('content.xml').decode('utf-8')
    z.close()

    root = ET.fromstring(content_xml)
    sections = root.findall('.//text:section', ns)

    subdocs = []
    for section in sections:
        source = section.find('text:section-source', ns)
        if source is not None:
            href = source.get('{http://www.w3.org/1999/xlink}href')
            if href:
                # href is like "../Preface.odt" — extract filename
                filename = href.split('/')[-1]
                subdocs.append(filename)
    return subdocs


def verify_task(odm_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the master document and extract subdocument order
    try:
        subdocs = extract_subdoc_order(odm_path)
        print(f"INFO: Found {len(subdocs)} subdocuments: {subdocs}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODM file {odm_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Total subdocument count is 9 (0.2 points)
    try:
        if len(subdocs) == 9:
            print(f"PASS: Component 1 — subdocument count is 9 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — expected 9 subdocuments, found {len(subdocs)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Preface.odt is first, before Ch1.odt (0.2 points)
    try:
        if len(subdocs) >= 2 and subdocs[0] == 'Preface.odt' and subdocs[1] == 'Ch1.odt':
            print(f"PASS: Component 2 — Preface.odt is at position 0, before Ch1.odt (0.2 pts)")
            total_score += 0.2
        else:
            pos_preface = subdocs.index('Preface.odt') if 'Preface.odt' in subdocs else 'NOT FOUND'
            pos_ch1 = subdocs.index('Ch1.odt') if 'Ch1.odt' in subdocs else 'NOT FOUND'
            print(f"FAIL: Component 2 — Preface.odt at pos {pos_preface}, Ch1.odt at pos {pos_ch1}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Midword.odt is between Ch3.odt and Ch4.odt (0.2 points)
    try:
        if 'Midword.odt' in subdocs and 'Ch3.odt' in subdocs and 'Ch4.odt' in subdocs:
            idx_ch3 = subdocs.index('Ch3.odt')
            idx_mid = subdocs.index('Midword.odt')
            idx_ch4 = subdocs.index('Ch4.odt')
            if idx_ch3 < idx_mid < idx_ch4 and idx_mid == idx_ch3 + 1:
                print(f"PASS: Component 3 — Midword.odt at pos {idx_mid}, between Ch3 (pos {idx_ch3}) and Ch4 (pos {idx_ch4}) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Midword.odt at pos {idx_mid}, Ch3 at pos {idx_ch3}, Ch4 at pos {idx_ch4} — not directly between them")
        else:
            print(f"FAIL: Component 3 — one of Midword.odt, Ch3.odt, Ch4.odt not found in subdocs")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Afterword.odt is last, after Ch6.odt (0.2 points)
    try:
        if len(subdocs) >= 2 and subdocs[-1] == 'Afterword.odt' and subdocs[-2] == 'Ch6.odt':
            print(f"PASS: Component 4 — Afterword.odt is last, after Ch6.odt (0.2 pts)")
            total_score += 0.2
        else:
            pos_after = subdocs.index('Afterword.odt') if 'Afterword.odt' in subdocs else 'NOT FOUND'
            pos_ch6 = subdocs.index('Ch6.odt') if 'Ch6.odt' in subdocs else 'NOT FOUND'
            print(f"FAIL: Component 4 — Afterword.odt at pos {pos_after}, Ch6.odt at pos {pos_ch6}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Full ordering matches exactly (0.2 points)
    try:
        if subdocs == EXPECTED_ORDER:
            print(f"PASS: Component 5 — full ordering matches expected sequence (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — ordering mismatch")
            print(f"  Expected: {EXPECTED_ORDER}")
            print(f"  Actual:   {subdocs}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
odm_path = f'{WORKDIR}/Anthology_Master.odm'
if not os.path.exists(odm_path):
    print(f"File not found: {odm_path}")
    print("REWARD: 0.0")
else:
    verify_task(odm_path)
