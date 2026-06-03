"""
Reward Script: Create protected section 'Confidential_Notes' with password 'Secure2024'
Task ID: writer_fs_053
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Section named 'Confidential_Notes' exists
  Component 2 (0.35): Section is protected with correct password hash (SHA-1 of 'Secure2024')
  Component 3 (0.30): Section contains the confidential paragraphs
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import hashlib
import base64

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_053'

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
}

TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'


def persist_app_state(domain):
    """Try to save any unsaved LibreOffice state via Ctrl+S."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODT file (ZIP archive) and parse content.xml
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content_xml = z.read('content.xml')
        root = ET.fromstring(content_xml)
        body = root.find('.//office:body/office:text', NS)
        if body is None:
            print("CRITICAL: Cannot find office:body/office:text in content.xml")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load/parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all text:section elements
    sections = body.findall('.//text:section', NS)

    # Component 1: Section named 'Confidential_Notes' exists (0.35 points)
    target_section = None
    try:
        for sec in sections:
            name = sec.attrib.get(f'{{{TEXT_NS}}}name', '')
            if name == 'Confidential_Notes':
                target_section = sec
                break

        if target_section is not None:
            print(f"PASS: Component 1 — Section 'Confidential_Notes' found (0.35 pts)")
            total_score += 0.35
        else:
            section_names = [sec.attrib.get(f'{{{TEXT_NS}}}name', '?') for sec in sections]
            print(f"FAIL: Component 1 — Section 'Confidential_Notes' not found. Found sections: {section_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Section is protected with correct password (0.35 points)
    try:
        if target_section is not None:
            protected_attr = target_section.attrib.get(f'{{{TEXT_NS}}}protected', 'false')
            protection_key = target_section.attrib.get(f'{{{TEXT_NS}}}protection-key', '')

            is_protected = protected_attr.lower() == 'true'

            # Compute expected SHA-1 hash of 'Secure2024'
            expected_hash = base64.b64encode(
                hashlib.sha1('Secure2024'.encode('utf-8')).digest()
            ).decode('ascii')

            key_matches = (protection_key == expected_hash)

            if is_protected and key_matches:
                print(f"PASS: Component 2 — Section protected=true, key matches SHA-1('Secure2024') (0.35 pts)")
                total_score += 0.35
            elif is_protected and not key_matches:
                print(f"FAIL: Component 2 — Section is protected but key mismatch. Expected: {expected_hash}, Got: {protection_key}")
                # Partial: at least protection is enabled
                total_score += 0.15
                print(f"  Partial credit: 0.15 pts for protection being enabled")
            else:
                print(f"FAIL: Component 2 — Section not protected. protected={protected_attr}, key={protection_key}")
        else:
            print(f"FAIL: Component 2 — No section found, cannot check protection")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Section contains the confidential paragraphs (0.30 points)
    try:
        if target_section is not None:
            # Extract text from paragraphs inside the section
            section_paras = []
            for child in target_section:
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if tag in ('p', 'h'):
                    txt = ''.join(child.itertext()).strip()
                    if txt:
                        section_paras.append(txt)

            # The confidential content should mention the acquisition and restructuring
            has_acquisition = any('DataSync' in p or 'acquisition' in p.lower() or '2.4 million' in p for p in section_paras)
            has_restructuring = any('restructure' in p.lower() or 'Customer Success' in p or 'elimination' in p.lower() for p in section_paras)

            if has_acquisition and has_restructuring:
                print(f"PASS: Component 3 — Section contains both confidential paragraphs (0.30 pts)")
                print(f"  Found {len(section_paras)} paragraph(s) in section")
                total_score += 0.30
            elif has_acquisition or has_restructuring:
                print(f"FAIL: Component 3 — Section contains only one confidential paragraph")
                print(f"  acquisition={has_acquisition}, restructuring={has_restructuring}")
                total_score += 0.15
                print(f"  Partial credit: 0.15 pts for partial content")
            else:
                print(f"FAIL: Component 3 — Section does not contain expected confidential content")
                print(f"  Section paragraphs: {[p[:60] for p in section_paras]}")
        else:
            print(f"FAIL: Component 3 — No section found, cannot check content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
