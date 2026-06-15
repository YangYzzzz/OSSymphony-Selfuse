"""
Reward Script: Remove 'Old_Notes' section while keeping its contents
Task ID: writer_fs_095
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Section 'Old_Notes' no longer exists in the document
  Component 2 (0.3): The three paragraphs from the section remain in the document body
  Component 3 (0.3): No gray background or write-protection on the formerly-sectioned paragraphs
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_095'

# Namespaces used in ODF content.xml
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}

# The three paragraphs that were inside the Old_Notes section (initial state)
EXPECTED_PARAGRAPHS = [
    "Meeting with stakeholders on Feb 12 concluded that the legacy API endpoints should be deprecated by end of Q2. Migration documentation has been shared with all affected teams.",
    "Budget allocation for the server upgrade was approved on Jan 30. The total approved amount is $142,500, which covers hardware procurement, installation, and three months of extended support.",
    "Action items from the retrospective: (1) implement automated regression testing for the payment module, (2) schedule weekly sync meetings with the QA team, (3) update the deployment runbook with the new rollback procedures.",
]


def get_all_text(elem):
    """Recursively get all text from an element and its children."""
    parts = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        parts.extend(get_all_text(child))
        if child.tail:
            parts.append(child.tail)
    return parts


def get_element_text(elem):
    """Get the full text content of an element."""
    return ''.join(get_all_text(elem)).strip()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with zipfile.ZipFile(file_path) as z:
            content_xml = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Section 'Old_Notes' no longer exists (0.4 points)
    # In the initial state, there is a <text:section text:name="Old_Notes"> element.
    # After removal, no such section should exist.
    try:
        sections = root.findall('.//' + '{' + NS['text'] + '}section')
        old_notes_sections = [
            s for s in sections
            if s.get('{' + NS['text'] + '}name') == 'Old_Notes'
        ]
        if len(old_notes_sections) == 0:
            print(f"PASS: Component 1 — No 'Old_Notes' section found (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — 'Old_Notes' section still exists ({len(old_notes_sections)} found)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The three paragraphs exist as direct children of <office:text>,
    # NOT inside any <text:section> element (0.3 points)
    # In initial state they are inside the section; in golden state they are free in body.
    try:
        body = root.find('.//' + '{' + NS['office'] + '}text')

        # Collect paragraphs that are direct children of <office:text> (not inside a section)
        direct_paragraphs = []
        for child in body:
            tag = child.tag
            if tag == '{' + NS['text'] + '}p' or tag == '{' + NS['text'] + '}h':
                p_text = get_element_text(child)
                if p_text:
                    direct_paragraphs.append(p_text)
            # Skip <text:section> children — those paragraphs are still section-wrapped

        found_count = 0
        for expected in EXPECTED_PARAGRAPHS:
            if any(expected in p_text for p_text in direct_paragraphs):
                found_count += 1
            else:
                print(f"FAIL: Component 2 — Paragraph not found as direct body child: '{expected[:60]}...'")

        if found_count == 3:
            print(f"PASS: Component 2 — All 3 paragraphs are direct body children, not in section (0.3 pts)")
            total_score += 0.3
        elif found_count > 0:
            partial = round(0.3 * found_count / 3, 2)
            print(f"PARTIAL: Component 2 — {found_count}/3 paragraphs as direct body children ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — None of the 3 paragraphs found as direct body children")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No gray background or write-protection on those paragraphs (0.3 points)
    # In the initial state, the section has style SectOldNotes with fo:background-color="#d0d0d0"
    # and text:protected="true". After removal, these properties should not apply.
    # We check: (a) no text:section wrapping those paragraphs with protection, and
    # (b) no section style with gray background referencing those paragraphs.
    try:
        # Check that no section element wraps any of the expected paragraphs
        # and that the SectOldNotes style is gone from automatic-styles
        auto_styles = root.find('{' + NS['office'] + '}automatic-styles')

        # Count section styles with gray background
        gray_section_styles = 0
        if auto_styles is not None:
            for style_elem in auto_styles.findall('{' + NS['style'] + '}style'):
                style_name = style_elem.get('{' + NS['style'] + '}name', '')
                style_family = style_elem.get('{' + NS['style'] + '}family', '')
                if style_family == 'section':
                    # Check if it has gray background
                    for prop in style_elem:
                        bg = prop.get('{' + NS['fo'] + '}background-color', '')
                        if bg.lower() in ('#d0d0d0', '#c0c0c0', 'gray', 'grey'):
                            gray_section_styles += 1
                            print(f"FAIL: Component 3 — Section style with gray background still exists: {style_name}")

        # Also check: count protected sections wrapping these paragraphs
        protected_para_count = 0
        for section in root.findall('.//' + '{' + NS['text'] + '}section'):
            if section.get('{' + NS['text'] + '}protected', 'false') == 'true':
                # Check if any expected paragraph is inside this section
                for p in section.iter('{' + NS['text'] + '}p'):
                    p_text = get_element_text(p)
                    for expected in EXPECTED_PARAGRAPHS:
                        if expected in p_text:
                            protected_para_count += 1
                            print(f"FAIL: Component 3 — Paragraph still in protected section")

        if gray_section_styles == 0 and protected_para_count == 0:
            print(f"PASS: Component 3 — No gray background or write-protection on paragraphs (0.3 pts)")
            total_score += 0.3
        elif protected_para_count == 0 and gray_section_styles > 0:
            # Style exists but paragraphs not in protected section — partial
            print(f"PARTIAL: Component 3 — Protection removed but style artifact remains (0.15 pts)")
            total_score += 0.15
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
