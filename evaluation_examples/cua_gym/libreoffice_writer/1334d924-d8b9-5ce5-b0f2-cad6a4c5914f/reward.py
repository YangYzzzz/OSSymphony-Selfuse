"""
Reward Script: Meeting minutes template with placeholder fields
Task ID: writer_rd_045
Domain: libreoffice_writer
Scoring:
  Component 1: Date field in body (0.15)
  Component 2: Time field in body (0.15)
  Component 3: User field declarations (Meeting Title + Chairperson) (0.15)
  Component 4: User field get references in body (0.10)
  Component 5: Section headings (Attendees, Agenda, Discussion, Action Items, Next Meeting) (0.15)
  Component 6: Header with 'Meeting Minutes' (0.15)
  Component 7: Footer with page number (0.15)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_045'

# Namespaces used in ODF XML
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}


def parse_ott(file_path):
    """Parse .ott file (ZIP archive) and return content.xml and styles.xml as ET roots."""
    z = zipfile.ZipFile(file_path, 'r')
    content_xml = z.read('content.xml').decode('utf-8')
    styles_xml = z.read('styles.xml').decode('utf-8')
    z.close()
    return ET.fromstring(content_xml), ET.fromstring(styles_xml)


def get_all_text(elem):
    """Recursively get all text content from an XML element."""
    parts = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        parts.extend(get_all_text(child))
        if child.tail:
            parts.append(child.tail)
    return parts


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        content_root, styles_root = parse_ott(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse OTT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Date field in body (0.15 points)
    # Check for <text:date> element in content.xml
    try:
        date_fields = content_root.findall('.//' + '{' + NS['text'] + '}date')
        if len(date_fields) > 0:
            print(f"PASS: Component 1 -- Date field found ({len(date_fields)} occurrence(s)) (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 1 -- No <text:date> element found in content.xml")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Time field in body (0.15 points)
    # Check for <text:time> element in content.xml
    try:
        time_fields = content_root.findall('.//' + '{' + NS['text'] + '}time')
        if len(time_fields) > 0:
            print(f"PASS: Component 2 -- Time field found ({len(time_fields)} occurrence(s)) (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 2 -- No <text:time> element found in content.xml")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: User field declarations for 'Meeting Title' and 'Chairperson' (0.15 points)
    # Check for <text:user-field-decl> elements with the correct names
    try:
        user_field_decls = content_root.findall('.//' + '{' + NS['text'] + '}user-field-decl')
        decl_names = set()
        for decl in user_field_decls:
            name = decl.get('{' + NS['text'] + '}name')
            if name:
                decl_names.add(name.lower().strip())

        has_meeting_title = any('meeting' in n and 'title' in n for n in decl_names)
        has_chairperson = any('chairperson' in n for n in decl_names)

        if has_meeting_title and has_chairperson:
            print(f"PASS: Component 3 -- Both 'Meeting Title' and 'Chairperson' user fields declared (names: {decl_names}) (0.15 pts)")
            total_score += 0.15
        elif has_meeting_title or has_chairperson:
            found = 'Meeting Title' if has_meeting_title else 'Chairperson'
            missing = 'Chairperson' if has_meeting_title else 'Meeting Title'
            print(f"PARTIAL: Component 3 -- Only '{found}' declared, missing '{missing}' (0.075 pts)")
            total_score += 0.075
        else:
            print(f"FAIL: Component 3 -- No user field declarations found for Meeting Title or Chairperson (found: {decl_names})")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: User field get references in body (0.10 points)
    # Check for <text:user-field-get> elements referencing the declared fields
    try:
        user_field_gets = content_root.findall('.//' + '{' + NS['text'] + '}user-field-get')
        get_names = set()
        for field_get in user_field_gets:
            name = field_get.get('{' + NS['text'] + '}name')
            if name:
                get_names.add(name.lower().strip())

        has_mt_get = any('meeting' in n and 'title' in n for n in get_names)
        has_cp_get = any('chairperson' in n for n in get_names)

        if has_mt_get and has_cp_get:
            print(f"PASS: Component 4 -- Both user field references found in body (0.10 pts)")
            total_score += 0.10
        elif has_mt_get or has_cp_get:
            print(f"PARTIAL: Component 4 -- Only one user field reference found (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 -- No user-field-get references found (found names: {get_names})")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Section headings present (0.15 points)
    # Check for headings: Attendees, Agenda, Discussion, Action Items, Next Meeting
    try:
        required_sections = ['attendees', 'agenda', 'discussion', 'action items', 'next meeting']
        # Find all heading elements
        headings = content_root.findall('.//' + '{' + NS['text'] + '}h')
        heading_texts = []
        for h in headings:
            text_parts = get_all_text(h)
            full_text = ''.join(text_parts).strip().lower()
            heading_texts.append(full_text)

        found_sections = []
        for section in required_sections:
            if any(section in ht for ht in heading_texts):
                found_sections.append(section)

        ratio = len(found_sections) / len(required_sections)
        points = round(0.15 * ratio, 4)
        if ratio == 1.0:
            print(f"PASS: Component 5 -- All 5 section headings found: {found_sections} (0.15 pts)")
            total_score += 0.15
        elif ratio > 0:
            print(f"PARTIAL: Component 5 -- {len(found_sections)}/5 sections found: {found_sections} ({points} pts)")
            total_score += points
        else:
            print(f"FAIL: Component 5 -- No required section headings found (headings in doc: {heading_texts})")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Header with 'Meeting Minutes' text (0.15 points)
    # Check styles.xml for <style:header> containing 'Meeting Minutes'
    try:
        header_texts = []
        for elem in styles_root.iter():
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            if tag == 'header':
                text_parts = get_all_text(elem)
                header_texts.append(''.join(text_parts).strip())

        matching_headers = [h for h in header_texts if 'meeting minutes' in h.lower()]
        if len(matching_headers) > 0:
            print(f"PASS: Component 6 -- Header contains 'Meeting Minutes' (text: '{matching_headers[0]}') (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 -- Header does not contain 'Meeting Minutes' (headers found: {header_texts})")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: Footer with page number field (0.15 points)
    # Check styles.xml for <style:footer> containing <text:page-number>
    try:
        footer_page_num_count = 0
        footer_text_content = ""
        for elem in styles_root.iter():
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            if tag == 'footer':
                text_parts = get_all_text(elem)
                footer_text_content = ''.join(text_parts).strip()
                # Check for page-number element inside footer
                page_nums = elem.findall('.//' + '{' + NS['text'] + '}page-number')
                footer_page_num_count += len(page_nums)

        if footer_page_num_count > 0:
            print(f"PASS: Component 7 -- Footer contains page number field (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 7 -- Footer does not contain <text:page-number> element (footer text: '{footer_text_content}')")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.ott'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
