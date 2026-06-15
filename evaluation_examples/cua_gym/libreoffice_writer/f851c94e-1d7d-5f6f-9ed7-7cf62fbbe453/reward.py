"""
Reward Script: Protect master document so subdocuments cannot be added/removed without password
Task ID: writer_rm_087
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.4): All 7 sections have text:protected="true"
  - Component 2 (0.3): All 7 sections have a non-empty text:protection-key
  - Component 3 (0.3): Protection key matches SHA-1 of 'MasterEdit2026' AND all 7 subdoc links preserved
"""

import os
import zipfile
import hashlib
import base64
from xml.etree import ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_087'

NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
}

EXPECTED_SUBDOCS = [
    'Chapter1_Introduction.odt',
    'Chapter2_Policies.odt',
    'Chapter3_Procedures.odt',
    'Chapter4_Guidelines.odt',
    'Chapter5_Compliance.odt',
    'Chapter6_Training.odt',
    'Chapter7_Appendices.odt',
]

def compute_odf_protection_key(password):
    """Compute ODF section protection key: base64(SHA-1(password))."""
    sha1 = hashlib.sha1(password.encode('utf-8')).digest()
    return base64.b64encode(sha1).decode('ascii')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load ODM file (ODF zip)
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all text:section elements
    body = root.find('.//office:body/office:text', NS)
    if body is None:
        print("CRITICAL: No office:text body found")
        print("REWARD: 0.0")
        return 0.0

    sections = body.findall('text:section', NS)
    print(f"INFO: Found {len(sections)} sections")

    if len(sections) < 7:
        print(f"FAIL: Expected 7 sections, found {len(sections)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 7 sections have text:protected="true" (0.4 points)
    try:
        protected_count = 0
        for sec in sections:
            prot_attr = sec.get(f'{{{NS["text"]}}}protected')
            if prot_attr and prot_attr.lower() == 'true':
                protected_count += 1

        if protected_count == 7:
            print(f"PASS: Component 1 — All 7 sections have text:protected='true' (0.4 pts)")
            total_score += 0.4
        elif protected_count > 0:
            partial = round(0.4 * (protected_count / 7), 2)
            print(f"PARTIAL: Component 1 — {protected_count}/7 sections protected (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No sections have text:protected='true'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 7 sections have a non-empty text:protection-key (0.3 points)
    try:
        key_count = 0
        keys_found = []
        for sec in sections:
            key_attr = sec.get(f'{{{NS["text"]}}}protection-key')
            if key_attr and len(key_attr.strip()) > 0:
                key_count += 1
                keys_found.append(key_attr)

        if key_count == 7:
            print(f"PASS: Component 2 — All 7 sections have a protection-key (0.3 pts)")
            total_score += 0.3
        elif key_count > 0:
            partial = round(0.3 * (key_count / 7), 2)
            print(f"PARTIAL: Component 2 — {key_count}/7 sections have protection-key (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No sections have a protection-key")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Protection key matches SHA-1('MasterEdit2026') AND all subdoc links preserved (0.3 points)
    try:
        expected_key = compute_odf_protection_key('MasterEdit2026')
        print(f"INFO: Expected protection key for 'MasterEdit2026': {expected_key}")

        # Check key matches
        correct_key_count = 0
        for sec in sections:
            key_attr = sec.get(f'{{{NS["text"]}}}protection-key')
            if key_attr and key_attr.strip() == expected_key:
                correct_key_count += 1

        # Check subdoc links preserved
        subdoc_links = []
        for sec in sections:
            source = sec.find('text:section-source', NS)
            if source is not None:
                href = source.get(f'{{{NS["xlink"]}}}href', '')
                subdoc_links.append(href)

        links_ok = sorted(subdoc_links) == sorted(EXPECTED_SUBDOCS)

        if correct_key_count == 7 and links_ok:
            print(f"PASS: Component 3 — All keys match 'MasterEdit2026' hash and all 7 subdoc links intact (0.3 pts)")
            total_score += 0.3
        elif correct_key_count == 7:
            print(f"PARTIAL: Component 3 — Keys correct but subdoc links changed (+0.15 pts)")
            total_score += 0.15
        elif links_ok and correct_key_count > 0:
            partial = round(0.15 * (correct_key_count / 7), 2)
            print(f"PARTIAL: Component 3 — {correct_key_count}/7 keys match, links OK (+{0.15 + partial} pts)")
            total_score += 0.15 + partial
        else:
            print(f"FAIL: Component 3 — correct_key_count={correct_key_count}/7, links_ok={links_ok}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.odm'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
