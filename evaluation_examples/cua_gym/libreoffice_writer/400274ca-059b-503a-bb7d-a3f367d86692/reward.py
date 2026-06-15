"""
Reward Script: Fix broken subdocument link in master document
Task ID: writer_rm_075
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Chapter4_Section href points to /home/user/docs/current/Chapter4.odt
  Component 2 (0.2): Chapter4_Section href no longer points to old broken path
  Component 3 (0.3): All other section hrefs remain unchanged (no collateral damage)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_075'

# Expected section hrefs (unchanged sections)
EXPECTED_OTHER_SECTIONS = {
    'Chapter1_Section': '/home/user/docs/chapters/Chapter1.odt',
    'Chapter2_Section': '/home/user/docs/chapters/Chapter2.odt',
    'Chapter3_Section': '/home/user/docs/chapters/Chapter3.odt',
    'Chapter5_Section': '/home/user/docs/chapters/Chapter5.odt',
    'Chapter6_Section': '/home/user/docs/chapters/Chapter6.odt',
}

BROKEN_PATH = '/home/user/docs/old/Chapter4.odt'
CORRECT_PATH = '/home/user/docs/current/Chapter4.odt'


def parse_odm_sections(file_path):
    """Parse ODM file and return dict of section_name -> xlink:href."""
    sections = {}
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open('content.xml') as f:
            content = f.read().decode('utf-8')

    root = ET.fromstring(content)

    # Define namespaces
    ns = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'xlink': 'http://www.w3.org/1999/xlink',
    }

    # Find all text:section elements
    for section in root.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}section'):
        section_name = section.get('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}name')
        # Find the section-source child
        for source in section.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}section-source'):
            href = source.get('{http://www.w3.org/1999/xlink}href')
            if section_name and href:
                sections[section_name] = href

    return sections


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid ODM
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        sections = parse_odm_sections(file_path)
        print(f"INFO: Found {len(sections)} sections: {list(sections.keys())}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODM file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Chapter4_Section must exist
    if 'Chapter4_Section' not in sections:
        print("CRITICAL: Chapter4_Section not found in document")
        print("REWARD: 0.0")
        return 0.0

    ch4_href = sections.get('Chapter4_Section', '')

    # Component 1: Chapter4_Section href points to correct path (0.5 points)
    # This FAILS on initial (points to /docs/old/) -> PASSES on golden (points to /docs/current/)
    try:
        if ch4_href == CORRECT_PATH:
            print(f"PASS: Component 1 — Chapter4 href is correct: {ch4_href} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected href '{CORRECT_PATH}', found '{ch4_href}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Chapter4_Section href is NOT the old broken path (0.2 points)
    # This FAILS on initial (href IS the broken path) -> PASSES on golden (href is different)
    try:
        if ch4_href != BROKEN_PATH:
            print(f"PASS: Component 2 — Chapter4 href is not the broken path (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Chapter4 href still points to broken path: {ch4_href}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All other sections remain unchanged (0.3 points)
    # This is a compound check: only awards points if Chapter4 is fixed AND others are intact.
    # On initial_env, Chapter4 is NOT fixed, so Component 1 fails -> score stays 0.
    # We still check other sections to ensure no collateral damage.
    try:
        other_ok = True
        for sect_name, expected_href in EXPECTED_OTHER_SECTIONS.items():
            actual_href = sections.get(sect_name, None)
            if actual_href != expected_href:
                print(f"FAIL: Component 3 — Section '{sect_name}' href mismatch: expected '{expected_href}', found '{actual_href}'")
                other_ok = False

        # Only award points if Chapter4 is also correctly updated (compound check)
        if other_ok and ch4_href == CORRECT_PATH:
            print(f"PASS: Component 3 — All other section hrefs intact and Chapter4 is correct (0.3 pts)")
            total_score += 0.3
        elif other_ok:
            print(f"FAIL: Component 3 — Other sections intact but Chapter4 not yet fixed")
        # else: already printed specific failures above
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.odm'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
