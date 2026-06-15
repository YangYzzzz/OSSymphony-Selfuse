"""
Reward Script: Cross-references in master document subdocuments
Task ID: writer_rm_094
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.15): Ch3 bookmark exists in Chapter3_Database.odt
  - Component 2 (0.15): Ch4 bookmark exists in Chapter4_Security.odt
  - Component 3 (0.15): Ch5 bookmark exists in Chapter5_Performance.odt
  - Component 4 (0.20): Introduction.odt has bookmark-ref to Database Architecture (replacing placeholder)
  - Component 5 (0.20): Introduction.odt has bookmark-ref to Security Protocols (replacing placeholder)
  - Component 6 (0.15): Introduction.odt has bookmark-ref to Performance Benchmarks (replacing placeholder)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_094'

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
}


def get_content_xml(odt_path):
    """Extract content.xml from an ODF file as an ElementTree."""
    with zipfile.ZipFile(odt_path) as z:
        with z.open('content.xml') as f:
            return ET.parse(f)


def get_full_xml_string(odt_path):
    """Extract raw content.xml string for regex/string-based checks."""
    with zipfile.ZipFile(odt_path) as z:
        with z.open('content.xml') as f:
            return f.read().decode('utf-8')


def check_bookmark_in_chapter(xml_str, bookmark_name, heading_text):
    """Check if a bookmark with the given name wraps the expected heading text."""
    # Look for bookmark-start with the expected name
    has_bookmark_start = f'text:name="{bookmark_name}"' in xml_str
    # Also check that heading text is present near the bookmark
    has_heading = heading_text in xml_str
    return has_bookmark_start and has_heading


def check_bookmark_ref_in_intro(xml_str, ref_name, display_text, placeholder):
    """Check that Introduction has a bookmark-ref replacing the placeholder."""
    # The placeholder should NOT be present
    has_placeholder = placeholder in xml_str
    # The bookmark-ref should be present
    has_ref = f'text:ref-name="{ref_name}"' in xml_str
    # The display text should appear (as content of the bookmark-ref element)
    has_display = display_text in xml_str
    return not has_placeholder, has_ref, has_display


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    parts_dir = os.path.join(WORKDIR, 'SystemDoc_Parts')
    intro_path = os.path.join(parts_dir, 'Introduction.odt')
    ch3_path = os.path.join(parts_dir, 'Chapter3_Database.odt')
    ch4_path = os.path.join(parts_dir, 'Chapter4_Security.odt')
    ch5_path = os.path.join(parts_dir, 'Chapter5_Performance.odt')

    # Precondition: All files must exist
    for fpath, fname in [(intro_path, 'Introduction.odt'), (ch3_path, 'Chapter3_Database.odt'),
                         (ch4_path, 'Chapter4_Security.odt'), (ch5_path, 'Chapter5_Performance.odt')]:
        if not os.path.exists(fpath):
            print(f"CRITICAL: File not found: {fpath}")
            print("REWARD: 0.0")
            return 0.0

    # Load XML strings
    try:
        ch3_xml = get_full_xml_string(ch3_path)
    except Exception as e:
        print(f"CRITICAL: Cannot read Chapter3_Database.odt: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        ch4_xml = get_full_xml_string(ch4_path)
    except Exception as e:
        print(f"CRITICAL: Cannot read Chapter4_Security.odt: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        ch5_xml = get_full_xml_string(ch5_path)
    except Exception as e:
        print(f"CRITICAL: Cannot read Chapter5_Performance.odt: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        intro_xml = get_full_xml_string(intro_path)
    except Exception as e:
        print(f"CRITICAL: Cannot read Introduction.odt: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Ch3 bookmark for 'Database Architecture' (0.15 pts)
    # In golden, Chapter3 has <text:bookmark-start text:name="__RefHeading__Database_Architecture"/>
    # In initial, it does NOT have this bookmark.
    try:
        if check_bookmark_in_chapter(ch3_xml, '__RefHeading__Database_Architecture', 'Database Architecture'):
            print("PASS: Component 1 - Bookmark '__RefHeading__Database_Architecture' found in Chapter3_Database.odt (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 1 - Bookmark '__RefHeading__Database_Architecture' not found in Chapter3_Database.odt")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Ch4 bookmark for 'Security Protocols' (0.15 pts)
    try:
        if check_bookmark_in_chapter(ch4_xml, '__RefHeading__Security_Protocols', 'Security Protocols'):
            print("PASS: Component 2 - Bookmark '__RefHeading__Security_Protocols' found in Chapter4_Security.odt (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 2 - Bookmark '__RefHeading__Security_Protocols' not found in Chapter4_Security.odt")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Ch5 bookmark for 'Performance Benchmarks' (0.15 pts)
    try:
        if check_bookmark_in_chapter(ch5_xml, '__RefHeading__Performance_Benchmarks', 'Performance Benchmarks'):
            print("PASS: Component 3 - Bookmark '__RefHeading__Performance_Benchmarks' found in Chapter5_Performance.odt (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 3 - Bookmark '__RefHeading__Performance_Benchmarks' not found in Chapter5_Performance.odt")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Introduction has cross-ref to Database Architecture, replacing [see Ch3 ref] (0.20 pts)
    try:
        no_placeholder, has_ref, has_display = check_bookmark_ref_in_intro(
            intro_xml, '__RefHeading__Database_Architecture', 'Database Architecture', '[see Ch3 ref]')
        if no_placeholder and has_ref and has_display:
            print("PASS: Component 4 - Cross-reference to 'Database Architecture' found in Introduction, placeholder removed (0.20 pts)")
            total_score += 0.20
        else:
            details = []
            if not no_placeholder:
                details.append("placeholder '[see Ch3 ref]' still present")
            if not has_ref:
                details.append("bookmark-ref to __RefHeading__Database_Architecture not found")
            if not has_display:
                details.append("display text 'Database Architecture' not found")
            print(f"FAIL: Component 4 - {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Introduction has cross-ref to Security Protocols, replacing [see Ch4 ref] (0.20 pts)
    try:
        no_placeholder, has_ref, has_display = check_bookmark_ref_in_intro(
            intro_xml, '__RefHeading__Security_Protocols', 'Security Protocols', '[see Ch4 ref]')
        if no_placeholder and has_ref and has_display:
            print("PASS: Component 5 - Cross-reference to 'Security Protocols' found in Introduction, placeholder removed (0.20 pts)")
            total_score += 0.20
        else:
            details = []
            if not no_placeholder:
                details.append("placeholder '[see Ch4 ref]' still present")
            if not has_ref:
                details.append("bookmark-ref to __RefHeading__Security_Protocols not found")
            if not has_display:
                details.append("display text 'Security Protocols' not found")
            print(f"FAIL: Component 5 - {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Introduction has cross-ref to Performance Benchmarks, replacing [see Ch5 ref] (0.15 pts)
    try:
        no_placeholder, has_ref, has_display = check_bookmark_ref_in_intro(
            intro_xml, '__RefHeading__Performance_Benchmarks', 'Performance Benchmarks', '[see Ch5 ref]')
        if no_placeholder and has_ref and has_display:
            print("PASS: Component 6 - Cross-reference to 'Performance Benchmarks' found in Introduction, placeholder removed (0.15 pts)")
            total_score += 0.15
        else:
            details = []
            if not no_placeholder:
                details.append("placeholder '[see Ch5 ref]' still present")
            if not has_ref:
                details.append("bookmark-ref to __RefHeading__Performance_Benchmarks not found")
            if not has_display:
                details.append("display text 'Performance Benchmarks' not found")
            print(f"FAIL: Component 6 - {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
