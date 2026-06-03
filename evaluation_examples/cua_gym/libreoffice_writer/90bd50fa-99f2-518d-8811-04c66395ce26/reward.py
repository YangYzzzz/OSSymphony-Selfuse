"""
Reward Script: Add a table of contents at the beginning of the master document
Task ID: writer_af_031
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): TOC element exists in the ODM file
  Component 2 (0.20): TOC is positioned before the first subdocument section
  Component 3 (0.20): TOC includes all 3 Heading 1 entries (chapter titles)
  Component 4 (0.30): TOC includes Heading 2 entries from all 3 chapters
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_af_031'

# Expected headings from subdocuments
EXPECTED_H1 = [
    "Introduction to Machine Learning",
    "Neural Network Architectures",
    "Applications and Future Directions",
]

EXPECTED_H2 = [
    "Historical Background",
    "Types of Machine Learning",
    "Current Challenges",
    "Feedforward Neural Networks",
    "Convolutional Neural Networks",
    "Recurrent Neural Networks and Transformers",
    "Generative Adversarial Networks",
    "Healthcare Applications",
    "Autonomous Systems",
    "Natural Language Processing",
    "Ethical Considerations and Future Outlook",
]

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
}


def get_text_recursive(elem):
    """Extract all text from an element and its descendants."""
    text = elem.text or ''
    for child in elem:
        text += get_text_recursive(child)
        if child.tail:
            text += child.tail
    return text.strip()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid ODM (zip with content.xml)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot read ODM file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse content.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the global-document body
    body = root.find('.//office:body/office:global-document', NS)
    if body is None:
        print("CRITICAL: No office:global-document found in content.xml")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: TOC element exists in the ODM (0.30 points)
    try:
        toc_elements = body.findall('text:table-of-content', NS)
        if len(toc_elements) > 0:
            print(f"PASS: Component 1 — TOC element found ({len(toc_elements)} TOC(s)) (0.30 pts)")
            total_score += 0.30
        else:
            print("FAIL: Component 1 — No text:table-of-content element found in ODM")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: TOC is positioned before the first section (0.20 points)
    try:
        children = list(body)
        toc_index = -1
        first_section_index = -1

        for i, child in enumerate(children):
            tag = child.tag
            # Check for TOC
            if tag == f'{{{NS["text"]}}}table-of-content' and toc_index < 0:
                toc_index = i
            # Check for section (subdocument reference)
            if tag == f'{{{NS["text"]}}}section' and first_section_index < 0:
                first_section_index = i

        if toc_index >= 0 and first_section_index >= 0 and toc_index < first_section_index:
            print(f"PASS: Component 2 — TOC at index {toc_index}, first section at {first_section_index} (0.20 pts)")
            total_score += 0.20
        elif toc_index < 0:
            print("FAIL: Component 2 — No TOC found to check position")
        elif first_section_index < 0:
            print("FAIL: Component 2 — No sections found in document")
        else:
            print(f"FAIL: Component 2 — TOC at index {toc_index} is NOT before first section at {first_section_index}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Extract TOC entries for Components 3 and 4
    toc_entry_texts = []
    toc_h1_texts = []
    toc_h2_texts = []
    try:
        if len(toc_elements) > 0:
            toc = toc_elements[0]
            # Look at all paragraphs in the index-body
            index_body = toc.find('text:index-body', NS)
            if index_body is not None:
                for p in index_body.findall('text:p', NS):
                    style = p.get(f'{{{NS["text"]}}}style-name', '')
                    entry_text = get_text_recursive(p)
                    # Strip page numbers (trailing digits after tab)
                    # The text often looks like "Heading Title\t5"
                    parts = entry_text.rsplit('\t', 1)
                    clean_text = parts[0].strip() if parts else entry_text.strip()
                    # Also try stripping trailing digits
                    import re
                    clean_text2 = re.sub(r'\s*\d+\s*$', '', clean_text).strip()

                    toc_entry_texts.append(clean_text2)

                    if 'Contents_20_1' in style:
                        toc_h1_texts.append(clean_text2)
                    elif 'Contents_20_2' in style:
                        toc_h2_texts.append(clean_text2)

            print(f"  INFO: Found {len(toc_entry_texts)} TOC entries total")
            print(f"  INFO: H1 entries: {toc_h1_texts}")
            print(f"  INFO: H2 entries: {toc_h2_texts}")
    except Exception as e:
        print(f"  ERROR extracting TOC entries: {e}")

    # Component 3: TOC includes all 3 Heading 1 entries (0.20 points)
    try:
        h1_found = 0
        for expected in EXPECTED_H1:
            # Check if any TOC entry contains or matches this heading
            if any(expected.lower() in entry.lower() for entry in toc_h1_texts):
                h1_found += 1
            elif any(expected.lower() in entry.lower() for entry in toc_entry_texts):
                h1_found += 1

        if h1_found == len(EXPECTED_H1):
            print(f"PASS: Component 3 — All {h1_found}/{len(EXPECTED_H1)} Heading 1 entries present in TOC (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Only {h1_found}/{len(EXPECTED_H1)} Heading 1 entries found in TOC")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: TOC includes Heading 2 entries from all 3 chapters (0.30 points)
    try:
        h2_found = 0
        for expected in EXPECTED_H2:
            if any(expected.lower() in entry.lower() for entry in toc_h2_texts):
                h2_found += 1
            elif any(expected.lower() in entry.lower() for entry in toc_entry_texts):
                h2_found += 1

        # Partial credit: at least some H2 entries
        h2_ratio = h2_found / len(EXPECTED_H2)
        if h2_ratio >= 0.9:
            # Full credit if >= 90% of H2 entries present
            print(f"PASS: Component 4 — {h2_found}/{len(EXPECTED_H2)} Heading 2 entries present in TOC (0.30 pts)")
            total_score += 0.30
        elif h2_ratio > 0:
            partial = round(0.30 * h2_ratio, 2)
            print(f"PARTIAL: Component 4 — {h2_found}/{len(EXPECTED_H2)} Heading 2 entries present ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No Heading 2 entries found in TOC")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Complete_Thesis.odm'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
