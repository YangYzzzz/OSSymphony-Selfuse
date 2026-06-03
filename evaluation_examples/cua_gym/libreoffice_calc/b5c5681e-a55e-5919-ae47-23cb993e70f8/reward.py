"""
Reward Script: Assign 'LogAccess' macro to 'Secure Data' sheet activation event
Task ID: calc_ps_081
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): 'Secure Data' sheet has an event-listeners element with an event-listener child
  Component 2 (0.3): The event-listener uses the 'sheet:OnFocus' (Activate) event
  Component 3 (0.3): The event-listener references the 'LogAccess' macro
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'calc_ps_081'

# ODS namespace prefixes
NS = {
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'script': 'urn:oasis:names:tc:opendocument:xmlns:script:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid ODS/ZIP
    try:
        zf = zipfile.ZipFile(file_path, 'r')
        content_xml = zf.read('content.xml').decode('utf-8')
        zf.close()
    except Exception as e:
        print(f"CRITICAL: Cannot read ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse XML
    try:
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse content.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the 'Secure Data' sheet
    target_table = None
    tables = root.findall('.//{urn:oasis:names:tc:opendocument:xmlns:table:1.0}table')
    for t in tables:
        name = t.attrib.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name', '')
        if name == 'Secure Data':
            target_table = t
            break

    if target_table is None:
        print("FAIL: 'Secure Data' sheet not found in the file")
        print("REWARD: 0.0")
        return 0.0

    # Find event-listeners element under 'Secure Data' sheet
    event_listeners_elem = target_table.find(
        '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}event-listeners'
    )

    # Collect all event-listener children
    listeners = []
    if event_listeners_elem is not None:
        listeners = event_listeners_elem.findall(
            '{urn:oasis:names:tc:opendocument:xmlns:script:1.0}event-listener'
        )

    # Component 1: 'Secure Data' sheet has at least one event-listener (0.4 points)
    try:
        if event_listeners_elem is not None and len(listeners) > 0:
            print(f"PASS: Component 1 -- 'Secure Data' has {len(listeners)} event-listener(s) (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 -- 'Secure Data' has no event-listeners configured")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Event listener uses 'sheet:OnFocus' event name (Activate event) (0.3 points)
    try:
        onfocus_listeners = []
        for listener in listeners:
            event_name = listener.attrib.get(
                '{urn:oasis:names:tc:opendocument:xmlns:script:1.0}event-name', ''
            )
            if event_name == 'sheet:OnFocus':
                onfocus_listeners.append(listener)

        if len(onfocus_listeners) > 0:
            print(f"PASS: Component 2 -- Found 'sheet:OnFocus' event trigger (0.3 pts)")
            total_score += 0.3
        else:
            event_names = [
                l.attrib.get('{urn:oasis:names:tc:opendocument:xmlns:script:1.0}event-name', 'N/A')
                for l in listeners
            ]
            print(f"FAIL: Component 2 -- No 'sheet:OnFocus' event found. Events present: {event_names}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Event listener references the 'LogAccess' macro (0.3 points)
    try:
        matching_hrefs = [
            l.attrib.get('{http://www.w3.org/1999/xlink}href', '')
            for l in listeners
            if l.attrib.get('{urn:oasis:names:tc:opendocument:xmlns:script:1.0}event-name', '') == 'sheet:OnFocus'
            and 'LogAccess' in l.attrib.get('{http://www.w3.org/1999/xlink}href', '')
        ]

        if len(matching_hrefs) > 0:
            print(f"PASS: Component 3 -- OnFocus event references LogAccess macro (href: {matching_hrefs[0]}) (0.3 pts)")
            total_score += 0.3
        else:
            hrefs = [
                l.attrib.get('{http://www.w3.org/1999/xlink}href', 'N/A')
                for l in listeners
            ]
            print(f"FAIL: Component 3 -- No OnFocus event referencing 'LogAccess' macro. Hrefs: {hrefs}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: check for ODS file
file_path = f'{WORKDIR}/{TASK_ID}.ods'
if not os.path.exists(file_path):
    # Also try xlsx in case format differs
    file_path_xlsx = f'{WORKDIR}/{TASK_ID}.xlsx'
    if os.path.exists(file_path_xlsx):
        file_path = file_path_xlsx
    else:
        print(f"File not found: {file_path} or {file_path_xlsx}")
        print("REWARD: 0.0")
        exit(0)

verify_task(file_path)
