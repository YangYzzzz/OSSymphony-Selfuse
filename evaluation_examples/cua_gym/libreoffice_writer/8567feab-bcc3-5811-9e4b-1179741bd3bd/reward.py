"""
Reward Script: Convert ODP lecture to ODT study guide
Task ID: osworld_multi_apps_doc_pres_to_writer_009
Domain: libreoffice_writer
Scoring:
  Component 1: Title page with 'Neural Networks Study Guide'     (0.20)
  Component 2: Table of Contents section with 10+ entries        (0.20)
  Component 3: 10 content sections with H1 headings              (0.25)
  Component 4: Instructor Note paragraphs with italic formatting (0.20)
  Component 5: Summary section with key terms in bold            (0.15)
  Total: 1.00
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_doc_pres_to_writer_009'
FILE_PATH = f'{WORKDIR}/nn_study_guide.odt'

# ---- ODT namespace constants ----
TEXT_NS  = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
STYLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'
FO_NS    = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'
OFFICE_NS = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'


def get_text(elem):
    """Recursively extract all text from an XML element."""
    text = elem.text or ''
    for child in elem:
        text += get_text(child)
        if child.tail:
            text += child.tail
    return text


def load_odt(file_path):
    """Load ODT file, return (root, body) or raise on error."""
    with zipfile.ZipFile(file_path) as z:
        content = z.read('content.xml').decode('utf-8')
    root = ET.fromstring(content)
    body = root.find(f'{{urn:oasis:names:tc:opendocument:xmlns:office:1.0}}body'
                     f'/{{urn:oasis:names:tc:opendocument:xmlns:office:1.0}}text')
    return root, body


def get_style_properties(root):
    """
    Build dicts mapping style name -> {font-weight, font-style, ...}
    from automatic-styles section.
    """
    style_props = {}
    auto_styles = root.find(f'{{{OFFICE_NS}}}automatic-styles')
    if auto_styles is None:
        return style_props
    for style in auto_styles:
        name = style.get(f'{{{STYLE_NS}}}name', '')
        props = {}
        for prop in style:
            for k, v in prop.attrib.items():
                k_short = k.split('}')[-1] if '}' in k else k
                props[k_short] = v
        style_props[name] = props
    return style_props


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition gate: file must exist ---
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        root, body = load_odt(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if body is None:
        print("CRITICAL: ODT body/text element not found")
        print("REWARD: 0.0")
        return 0.0

    # Collect all top-level body elements with their tag, style, text, outline level
    elements = list(body)
    style_props = get_style_properties(root)

    # -----------------------------------------------------------------------
    # Component 1: Title page — must contain 'Neural Networks Study Guide'
    #              as a prominent heading/paragraph                 (0.20 pts)
    # -----------------------------------------------------------------------
    try:
        title_matches = [
            get_text(elem).strip()
            for elem in elements
            if 'neural networks study guide' in get_text(elem).lower()
        ]
        if len(title_matches) >= 1:
            print(f"PASS: Component 1 — Title found: {repr(title_matches[0][:60])}")
            total_score += 0.20
        else:
            print("FAIL: Component 1 — 'Neural Networks Study Guide' title not found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Table of Contents section present with >= 10 entries (0.20 pts)
    # The TOC section should have a heading containing 'Table of Contents'
    # or 'Contents', and list entries matching the 10 slide topics.
    # -----------------------------------------------------------------------
    try:
        toc_heading_found = False
        toc_entries = 0
        # Known TOC keywords from the context
        slide_titles_keywords = [
            'introduction', 'perceptron', 'feedforward', 'activation',
            'backpropagation', 'optimization', 'convolutional', 'recurrent',
            'training', 'modern'
        ]
        # Scan for a TOC heading, then count entries nearby
        toc_idx = next(
            (i for i, elem in enumerate(elements)
             if 'table of contents' in get_text(elem).strip().lower()
             or get_text(elem).strip().lower() == 'contents'),
            -1
        )
        toc_heading_found = (toc_idx >= 0)
        if toc_heading_found:
            for j in range(toc_idx + 1, min(toc_idx + 20, len(elements))):
                entry_text = get_text(elements[j]).strip().lower()
                if any(kw in entry_text for kw in slide_titles_keywords):
                    toc_entries += 1
                elif entry_text == '' and toc_entries > 0:
                    break

        if toc_heading_found and toc_entries >= 8:
            print(f"PASS: Component 2 — TOC found with {toc_entries} entries")
            total_score += 0.20
        elif toc_heading_found:
            # Partial: heading present but few entries
            print(f"PARTIAL: Component 2 — TOC heading found but only {toc_entries} entries (need >= 8)")
            total_score += 0.10
        else:
            print("FAIL: Component 2 — Table of Contents section not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: 10 content sections with H1 headings for each slide topic
    #                                                                 (0.25 pts)
    # Each of the 10 slides should have its title as a section heading.
    # -----------------------------------------------------------------------
    try:
        expected_headings = [
            'introduction to neural networks',
            'perceptron',
            'feedforward neural networks',
            'activation functions',
            'backpropagation',
            'optimization',
            'convolutional neural networks',
            'recurrent neural networks',
            'training challenges',
            'modern architectures',
        ]
        h1_headings = []
        for elem in elements:
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            if tag == 'h':
                level = elem.get(f'{{{TEXT_NS}}}outline-level', '0')
                if level == '1':
                    h_text = get_text(elem).strip().lower()
                    h1_headings.append(h_text)

        # Count how many expected headings are matched
        matched = 0
        for expected in expected_headings:
            for h in h1_headings:
                if expected in h:
                    matched += 1
                    break

        # Also count H1 headings that are slide content (not ToC or Summary)
        content_headings = [h for h in h1_headings
                            if 'table of contents' not in h
                            and 'contents' != h.strip()
                            and 'summary' not in h]

        print(f"INFO: H1 headings found: {len(h1_headings)}, content headings: {len(content_headings)}, matched expected: {matched}")

        if matched >= 9:
            print(f"PASS: Component 3 — {matched}/10 slide headings found as H1 sections")
            total_score += 0.25
        elif matched >= 6:
            print(f"PARTIAL: Component 3 — {matched}/10 slide headings found (partial credit)")
            total_score += 0.15
        elif matched >= 3:
            print(f"PARTIAL: Component 3 — {matched}/10 slide headings found (minimal credit)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 3 — Only {matched}/10 slide headings found as H1 sections")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Instructor Note paragraphs with italic formatting (0.20 pts)
    # Should have >= 8 'Instructor Note:' paragraphs (one per content section)
    # and those paragraphs must use italic text.
    # -----------------------------------------------------------------------
    try:
        # Identify italic styles
        italic_styles = set()
        for style_name, props in style_props.items():
            fw = props.get('font-style', '')
            if fw == 'italic':
                italic_styles.add(style_name)

        instructor_note_count = 0
        italic_instructor_count = 0

        for elem in elements:
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            if tag == 'p':
                full_text = get_text(elem).strip()
                if 'Instructor Note:' in full_text or 'instructor note:' in full_text.lower():
                    instructor_note_count += 1
                    # Check if any span uses an italic style
                    has_italic = any(
                        span.get(f'{{{TEXT_NS}}}style-name', '') in italic_styles
                        for span in elem.iter(f'{{{TEXT_NS}}}span')
                    )
                    if has_italic:
                        italic_instructor_count += 1

        print(f"INFO: Instructor Note paragraphs: {instructor_note_count}, italic: {italic_instructor_count}")

        if instructor_note_count >= 8 and italic_instructor_count >= 8:
            print(f"PASS: Component 4 — {instructor_note_count} Instructor Note paragraphs, all italic")
            total_score += 0.20
        elif instructor_note_count >= 8:
            # Notes present but maybe not italic
            print(f"PARTIAL: Component 4 — {instructor_note_count} Instructor Notes found but only {italic_instructor_count} italic")
            total_score += 0.10
        elif instructor_note_count >= 4:
            print(f"PARTIAL: Component 4 — Only {instructor_note_count} Instructor Note paragraphs (need >= 8)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 — Only {instructor_note_count} Instructor Note paragraphs found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: Summary section with key terms in bold             (0.15 pts)
    # A 'Summary' heading followed by bold key terms from the lecture.
    # -----------------------------------------------------------------------
    try:
        # Identify bold styles
        bold_styles = set()
        for style_name, props in style_props.items():
            fw = props.get('font-weight', '')
            if fw == 'bold':
                bold_styles.add(style_name)

        summary_idx = next(
            (i for i, elem in enumerate(elements)
             if elem.tag.split('}')[-1] == 'h'
             and 'summary' in get_text(elem).strip().lower()),
            -1
        )
        summary_heading_found = (summary_idx >= 0)
        in_summary = summary_heading_found
        bold_terms_in_summary = 0

        for elem in (elements[summary_idx + 1:] if in_summary else []):
            # Count paragraphs with bold spans (key terms)
            for span in elem.iter(f'{{{TEXT_NS}}}span'):
                span_style = span.get(f'{{{TEXT_NS}}}style-name', '')
                if span_style in bold_styles:
                    span_text = get_text(span).strip()
                    if span_text:
                        bold_terms_in_summary += 1

        print(f"INFO: Summary heading found: {summary_heading_found}, bold term instances: {bold_terms_in_summary}")

        if summary_heading_found and bold_terms_in_summary >= 10:
            print(f"PASS: Component 5 — Summary section with {bold_terms_in_summary} bold key terms")
            total_score += 0.15
        elif summary_heading_found and bold_terms_in_summary >= 4:
            print(f"PARTIAL: Component 5 — Summary section found with {bold_terms_in_summary} bold terms (partial)")
            total_score += 0.08
        elif summary_heading_found:
            print(f"PARTIAL: Component 5 — Summary heading found but only {bold_terms_in_summary} bold terms")
            total_score += 0.05
        else:
            print("FAIL: Component 5 — Summary section not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# ---- Entry point ----
verify_task(FILE_PATH)
