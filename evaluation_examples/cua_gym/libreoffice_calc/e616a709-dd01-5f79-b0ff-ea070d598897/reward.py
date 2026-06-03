"""
Reward Script: Schengen Visa Application Checklist in LibreOffice Writer
Task ID: osworld_multi_apps_travel_permit_research_001
Domain: libreoffice_writer (ODT)
Scoring:
  Component 1: schengen_checklist.odt exists on the Desktop  (0.2 pts)
  Component 2: Document has heading 'Schengen Visa Application Checklist'  (0.3 pts)
  Component 3: Document has a list element with exactly 5 items  (0.3 pts)
  Component 4: All 5 step texts are present in the list  (0.2 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_travel_permit_research_001'
FILE_PATH = os.path.join(WORKDIR, 'schengen_checklist.odt')

# Expected step texts (stripped, case-insensitive comparison)
EXPECTED_STEPS = [
    'gather required documents',
    'complete the application form',
    'schedule appointment at consulate',
    'pay visa fee',
    'attend appointment and submit documents',
]

EXPECTED_TITLE = 'schengen visa application checklist'

# ODF XML namespaces
NS = {
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
}


def extract_text_content(element):
    """Recursively extract all text content from an XML element."""
    text = element.text or ''
    for child in element:
        text += extract_text_content(child)
        if child.tail:
            text += child.tail
    return text


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File exists on Desktop (0.2 points)
    # This is a task-introduced change: initial_env has no schengen_checklist.odt
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"PASS: Component 1 — schengen_checklist.odt exists on Desktop (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — schengen_checklist.odt not found at {file_path}")
            print(f"Score: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"Score: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load and parse the ODT file (it's a ZIP archive containing XML)
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            with z.open('content.xml') as f:
                content_xml = f.read().decode('utf-8')
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODT file {file_path}: {e}")
        print(f"Score: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Document has heading 'Schengen Visa Application Checklist' (0.3 points)
    # This heading is the document title — not present in initial_env (no ODT existed)
    try:
        headings = root.findall('.//text:h', NS)
        heading_texts = []
        for h in headings:
            txt = extract_text_content(h).strip()
            heading_texts.append(txt)

        found_title = any(t.lower() == EXPECTED_TITLE for t in heading_texts)
        if found_title:
            matched = [t for t in heading_texts if t.lower() == EXPECTED_TITLE][0]
            print(f"PASS: Component 2 — Heading found: {matched!r} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected heading '{EXPECTED_TITLE}', found headings: {heading_texts}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Document has a list element with exactly 5 list items (0.3 points)
    # The task requires converting 5 steps into a numbered list
    try:
        list_items = root.findall('.//text:list-item', NS)
        num_items = len(list_items)
        if num_items == 5:
            print(f"PASS: Component 3 — List has exactly 5 items (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Expected 5 list items, found {num_items}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All 5 step texts are present and correct in the list (0.2 points)
    # Each step text must match the expected content from schengen_steps.txt
    try:
        list_items = root.findall('.//text:list-item', NS)
        found_texts = []
        for li in list_items:
            txt = extract_text_content(li).strip().lower()
            found_texts.append(txt)

        matched_steps = 0
        for expected in EXPECTED_STEPS:
            if any(expected in ft or ft in expected for ft in found_texts):
                matched_steps += 1

        if matched_steps == 5:
            print(f"PASS: Component 4 — All 5 step texts match expected content (0.2 pts)")
            total_score += 0.2
        else:
            missing = [s for s in EXPECTED_STEPS if not any(s in ft or ft in s for ft in found_texts)]
            print(f"FAIL: Component 4 — Only {matched_steps}/5 steps matched. Missing: {missing}")
            print(f"  Found texts: {found_texts}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
