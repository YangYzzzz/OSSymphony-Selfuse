"""
Reward Script: Extract PPTX text to ODT speaker notes document
Task ID: osworld_multi_apps_impress_text_to_writer_005
Domain: libreoffice_writer (ODT output)
Scoring:
  Component 1: File conference_speaker_notes.odt exists in Documents (0.1)
  Component 2: 6 slide sections with correct 'Slide N — [title]' format (0.4)
  Component 3: Slide headers have bold formatting (0.3)
  Component 4: Sufficient content paragraphs (bullets converted to regular text) (0.2)
"""

import os
import re

WORKDIR = '/home/user/Documents'
TASK_ID = 'osworld_multi_apps_impress_text_to_writer_005'
OUTPUT_FILE = 'conference_speaker_notes.odt'

EXPECTED_SLIDE_TITLES = [
    'Introduction',
    'Related Work',
    'Methodology',
    'Results',
    'Discussion',
    'Conclusion',
]

# Style name that should be bold (from odf automatic styles)
BOLD_STYLE_NAME = 'T1'


def get_para_text(para):
    """Extract full text from an ODT paragraph node."""
    text = ''
    for node in para.childNodes:
        if node.nodeType == node.TEXT_NODE:
            text += node.data
        elif hasattr(node, 'childNodes'):
            for child in node.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    text += child.data
    return text


def get_bold_style_names(doc):
    """Return a set of style names defined with bold font-weight in automatic styles."""
    bold_styles = set()
    if not hasattr(doc, 'automaticstyles') or doc.automaticstyles is None:
        return bold_styles
    for style in doc.automaticstyles.childNodes:
        if not hasattr(style, 'getAttribute'):
            continue
        style_name = style.getAttribute('name')
        for child in (style.childNodes if hasattr(style, 'childNodes') else []):
            if not hasattr(child, 'tagName'):
                continue
            if 'text-properties' in child.tagName.lower():
                fw = child.getAttribute('fontweight')
                if fw == 'bold':
                    bold_styles.add(style_name)
    return bold_styles


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist
    if not os.path.exists(file_path):
        print(f"FAIL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load ODT document
    try:
        from odf.opendocument import load
        from odf.text import P
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all paragraphs and their text
    try:
        all_paras = doc.getElementsByType(P)
        para_texts = []
        for para in all_paras:
            t = get_para_text(para).strip()
            para_texts.append(t)
    except Exception as e:
        print(f"CRITICAL: Cannot read paragraphs: {e}")
        print("REWARD: 0.0")
        return 0.0

    non_empty_paras = [t for t in para_texts if t]
    print(f"INFO: Total paragraphs={len(para_texts)}, non-empty={len(non_empty_paras)}")

    # Component 1: Output file exists and is a valid ODT document (0.1 points)
    # Verified by successful load above; doc is not None
    try:
        if doc is not None:
            print(f"PASS: Component 1 — file {OUTPUT_FILE} exists and is valid ODT (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — doc is None after load")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 6 slide sections with correct 'Slide N — [title]' format (0.4 points)
    # Check for all 6 expected slide headers: "Slide 1 — Introduction", etc.
    try:
        slide_header_pattern = re.compile(r'^Slide\s+(\d+)\s*[—\-]+\s*(.+)$')
        found_slides = {}
        for t in non_empty_paras:
            m = slide_header_pattern.match(t)
            if m:
                slide_num = int(m.group(1))
                slide_title = m.group(2).strip()
                found_slides[slide_num] = slide_title

        print(f"INFO: Found slide headers: {found_slides}")

        # Check that all 6 expected slide numbers are present
        all_6_found = all(n in found_slides for n in range(1, 7))
        # Check that the titles contain the expected keywords (case-insensitive)
        title_matches = 0
        for n, expected_title in enumerate(EXPECTED_SLIDE_TITLES, start=1):
            if n in found_slides and expected_title.lower() in found_slides[n].lower():
                title_matches += 1

        if all_6_found and title_matches == 6:
            comp2_score = 0.4
            print(f"PASS: Component 2 — all 6 slide sections with correct titles found ({comp2_score} pts)")
        elif all_6_found:
            comp2_score = round(title_matches / 6 * 0.4, 3)
            print(f"PARTIAL: Component 2 — all 6 sections found but {title_matches}/6 titles match ({comp2_score:.2f} pts)")
        elif len(found_slides) >= 4:
            comp2_score = round(len(found_slides) / 6 * 0.4, 3)
            print(f"PARTIAL: Component 2 — {len(found_slides)}/6 slide sections found ({comp2_score:.2f} pts)")
        else:
            comp2_score = 0.0
            print(f"FAIL: Component 2 — only {len(found_slides)}/6 slide sections found. Expected 'Slide N — [Title]' format")
        if comp2_score > 0:
            total_score += comp2_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Slide headers have bold formatting (0.3 points)
    # The slide header paragraphs should contain spans with bold font-weight style
    try:
        bold_styles = get_bold_style_names(doc)
        print(f"INFO: Bold automatic style names: {bold_styles}")

        bold_header_count = 0
        for para in all_paras:
            para_text = get_para_text(para).strip()
            # Only check slide header paragraphs
            if not slide_header_pattern.match(para_text):
                continue
            # Check if any child span has a bold style
            for node in para.childNodes:
                if hasattr(node, 'tagName') and 'span' in node.tagName.lower():
                    span_style = node.getAttribute('stylename')
                    if span_style in bold_styles:
                        bold_header_count += 1
                        break

        if bold_header_count == 6:
            comp3_score = 0.3
            print(f"PASS: Component 3 — all 6 slide headers are bold formatted ({comp3_score} pts)")
        elif bold_header_count >= 4:
            comp3_score = round(bold_header_count / 6 * 0.3, 3)
            print(f"PARTIAL: Component 3 — {bold_header_count}/6 slide headers are bold ({comp3_score:.2f} pts)")
        else:
            # Also check using paragraph style name (some implementations use heading styles)
            heading_count = 0
            for para in all_paras:
                para_text = get_para_text(para).strip()
                if not slide_header_pattern.match(para_text):
                    continue
                style_name = para.getAttribute('stylename') or ''
                if 'heading' in style_name.lower() or 'Heading' in style_name:
                    heading_count += 1
            if heading_count >= 4:
                comp3_score = round(heading_count / 6 * 0.3, 3)
                print(f"PARTIAL: Component 3 — {heading_count}/6 slide headers use heading styles ({comp3_score:.2f} pts)")
            else:
                comp3_score = 0.0
                print(f"FAIL: Component 3 — only {bold_header_count}/6 slide headers are bold. Expected bold formatting on 'Slide N — [Title]' lines")
        if comp3_score > 0:
            total_score += comp3_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Sufficient content paragraphs (bullets converted to regular text) (0.2 points)
    # The task requires converting 4-6 bullets per slide to regular paragraphs.
    # With 6 slides having 4-6 bullets + text box notes, expect at least 30 non-empty paras total
    # (6 slide headers + ~24+ content paragraphs). Minimum threshold: 20 non-empty paragraphs.
    try:
        # Exclude slide header lines from content count
        content_paras = [t for t in non_empty_paras if not slide_header_pattern.match(t)]
        content_count = len(content_paras)
        print(f"INFO: Content (non-header) non-empty paragraphs: {content_count}")

        # Minimum expected: at least 4 content paragraphs per slide = 24 total
        # Generous threshold: 20 (allows for some variation)
        if content_count >= 20:
            comp4_score = 0.2
            print(f"PASS: Component 4 — {content_count} content paragraphs found (>= 20 required) ({comp4_score} pts)")
        elif content_count >= 12:
            comp4_score = round(content_count / 24 * 0.2, 3)
            print(f"PARTIAL: Component 4 — only {content_count} content paragraphs (expected >= 20) ({comp4_score:.2f} pts)")
        else:
            comp4_score = 0.0
            print(f"FAIL: Component 4 — only {content_count} content paragraphs (expected >= 20)")
        if comp4_score > 0:
            total_score += comp4_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{OUTPUT_FILE}'
verify_task(file_path)
