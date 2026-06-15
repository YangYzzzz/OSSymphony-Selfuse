"""
Reward Script: Update all subdocuments in master document (.odm) to reflect latest chapter changes
Task ID: writer_rm_056
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.35): Chapter 2 section updated with new content
  - Component 2 (0.35): Chapter 5 section updated with new content
  - Component 3 (0.30): Chapter 7 section updated with new content
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_056'

# Namespaces for ODF XML
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
}


def persist_app_state(domain):
    """Try to save any unsaved document state via Ctrl+S."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.5)
            print("PERSIST: ctrl+s sent for libreoffice_writer")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def get_section_text(content_xml_bytes, section_name):
    """
    Extract all paragraph text from a named text:section in the ODM content.xml.
    Returns a list of stripped paragraph text strings.
    """
    root = ET.fromstring(content_xml_bytes)
    body = root.find('.//office:body/office:text', NS)
    if body is None:
        return []

    for section in body.findall('text:section', NS):
        name = section.get('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}name', '')
        if name == section_name:
            paragraphs = []
            for p in section.findall('text:p', NS):
                text = ''.join(p.itertext()).strip()
                if text:
                    paragraphs.append(text)
            return paragraphs
    return []


def get_odt_text(odt_path):
    """
    Extract all paragraph text from an .odt file's content.xml.
    Returns a list of stripped paragraph text strings.
    """
    try:
        with zipfile.ZipFile(odt_path, 'r') as z:
            content = z.read('content.xml')
        root = ET.fromstring(content)
        body = root.find('.//office:body/office:text', NS)
        if body is None:
            return []
        paragraphs = []
        for p in body.findall('text:p', NS):
            text = ''.join(p.itertext()).strip()
            if text:
                paragraphs.append(text)
        return paragraphs
    except Exception as e:
        print(f"ERROR: Cannot read {odt_path}: {e}")
        return []


def verify_task(odm_path):
    """
    Verify that the master document has been updated to reflect current subdocument content.
    Checks that Chapters 2, 5, and 7 sections in the ODM now contain the updated text
    from their respective .odt files instead of the stale content.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODM content.xml
    try:
        with zipfile.ZipFile(odm_path, 'r') as z:
            content_xml = z.read('content.xml')
        print(f"OK: Loaded ODM file {odm_path}")
    except Exception as e:
        print(f"CRITICAL: Cannot load ODM file {odm_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Define the chapters that were modified and their distinctive updated content.
    # Each entry: (section_name, odt_file, updated_marker, stale_marker, weight)
    # updated_marker: a substring that ONLY appears in the updated chapter content
    # stale_marker: a substring that ONLY appears in the stale (initial) master doc content
    chapters_to_check = [
        {
            'section': 'Chapter2',
            'odt_file': 'Chapter2.odt',
            'updated_marker': 'Reinforced concrete revolutionized construction',
            'stale_marker': 'Concrete and steel have been the primary materials',
            'weight': 0.35,
            'desc': 'Chapter 2 (Materials and Structural Engineering)',
        },
        {
            'section': 'Chapter5',
            'odt_file': 'Chapter5.odt',
            'updated_marker': 'Contemporary interior design embraces minimalism',
            'stale_marker': 'Interior design focuses on creating functional',
            'weight': 0.35,
            'desc': 'Chapter 5 (Interior Design Philosophy)',
        },
        {
            'section': 'Chapter7',
            'odt_file': 'Chapter7.odt',
            'updated_marker': 'Building Information Modeling (BIM) enables architects',
            'stale_marker': 'Computer-aided design (CAD) software has replaced',
            'weight': 0.30,
            'desc': 'Chapter 7 (Digital Tools in Architecture)',
        },
    ]

    for i, ch in enumerate(chapters_to_check, 1):
        try:
            section_paras = get_section_text(content_xml, ch['section'])
            section_full = ' '.join(section_paras)

            # Get the actual .odt file content for cross-reference
            odt_paras = get_odt_text(os.path.join(WORKDIR, ch['odt_file']))
            odt_full = ' '.join(odt_paras)

            has_updated = ch['updated_marker'] in section_full
            has_stale = ch['stale_marker'] in section_full

            if has_updated and not has_stale:
                # Also verify paragraph count matches the odt file (updated chapters have 5 paras: heading + 4 body)
                if len(section_paras) >= len(odt_paras):
                    print(f"PASS: Component {i} — {ch['desc']} updated correctly with {len(section_paras)} paragraphs ({ch['weight']} pts)")
                    total_score += ch['weight']
                else:
                    # Partial: marker present but paragraph count is off
                    partial = ch['weight'] * 0.7
                    print(f"PARTIAL: Component {i} — {ch['desc']} has updated marker but paragraph count mismatch (section={len(section_paras)}, odt={len(odt_paras)}). ({partial:.2f} pts)")
                    total_score += partial
            elif has_updated and has_stale:
                # Oddly has both old and new content
                partial = ch['weight'] * 0.3
                print(f"PARTIAL: Component {i} — {ch['desc']} has updated content but stale content also present. ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component {i} — {ch['desc']} not updated. Has updated marker: {has_updated}, has stale marker: {has_stale}")
                if section_paras:
                    print(f"  Section content preview: {section_paras[0][:80]}...")
                else:
                    print(f"  Section is empty or not found")
        except Exception as e:
            print(f"ERROR: Component {i} — {ch['desc']}: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/Book_Master.odm'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
