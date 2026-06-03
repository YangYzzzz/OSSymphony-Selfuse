"""
Reward Script: Three-day HuggingFace papers survey in LibreOffice Writer
Task ID: osworld_multi_apps_hf_papers_writer_011
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Three date sections (2024-01-10, 2024-01-11, 2024-01-12) each contain paper entries
  Component 2 (0.30): Paper titles are formatted with bold style (BoldTitle span or explicit bold font-weight)
  Component 3 (0.20): Paper authors are formatted with italic style (ItalicAuthors span or explicit italic font-style)
  Component 4 (0.10): Paper abstracts use IndentedAbstract paragraph style (left/right margin indentation)
  Component 5 (0.10): Duplicates section exists and contains non-empty content
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_hf_papers_writer_011'

FILE_PATH = f'{WORKDIR}/three_day_survey.odt'


def get_auto_styles(doc):
    """Build a dict of automatic style name -> dict of properties."""
    styles = {}
    for style in doc.automaticstyles.childNodes:
        name = style.getAttribute('name')
        if not name:
            continue
        props = {}
        for child in style.childNodes:
            tag = getattr(child, 'tagName', None)
            if tag in ('style:text-properties', 'style:paragraph-properties'):
                for k, v in child.attributes.items():
                    # Store local name -> value
                    local_key = k[1] if isinstance(k, tuple) else k
                    props[local_key] = v
        styles[name] = props
    return styles


def get_document_elements(doc):
    """Return all top-level text elements in order from office:text body."""
    body = doc.body
    text_body = None
    for child in body.childNodes:
        if hasattr(child, 'tagName') and child.tagName == 'office:text':
            text_body = child
            break
    return text_body.childNodes if text_body else []


def get_para_text(elem):
    """Extract plain text from a paragraph/heading element."""
    parts = []
    for node in elem.childNodes:
        if node.nodeType == node.TEXT_NODE:
            parts.append(node.data)
        elif hasattr(node, 'tagName') and node.tagName == 'text:span':
            for child in node.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    parts.append(child.data)
    return ''.join(parts)


def get_span_styles(elem):
    """Return list of span style names used in this element."""
    span_styles = []
    for node in elem.childNodes:
        if hasattr(node, 'tagName') and node.tagName == 'text:span':
            span_style = node.getAttribute('stylename')
            if span_style:
                span_styles.append(span_style)
    return span_styles


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from odf.opendocument import load
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get automatic styles for bold/italic/indent detection
    try:
        auto_styles = get_auto_styles(doc)
    except Exception as e:
        print(f"WARN: Could not parse auto styles: {e}")
        auto_styles = {}

    # Get all document elements in order
    elements = list(get_document_elements(doc))

    # Find headings and their positions
    heading_positions = {}
    for i, elem in enumerate(elements):
        tag = getattr(elem, 'tagName', None)
        if tag == 'text:h':
            text = get_para_text(elem)
            heading_positions[text.strip()] = i

    # ------------------------------------------------------------------
    # Component 1: Three date sections each contain at least one paper entry
    # Score: 0.30 — fails on initial (no paper entries in any date section)
    # ------------------------------------------------------------------
    try:
        required_dates = ['2024-01-10', '2024-01-11', '2024-01-12']
        sections_with_papers = 0

        for date in required_dates:
            if date not in heading_positions:
                print(f"FAIL: Heading '{date}' not found in document")
                continue
            start_idx = heading_positions[date] + 1
            # Find end: next heading or end of document
            end_idx = len(elements)
            for other_date in required_dates + ['Duplicates']:
                if other_date != date and other_date in heading_positions:
                    pos = heading_positions[other_date]
                    if pos > start_idx:
                        end_idx = min(end_idx, pos)

            # Count non-empty paragraphs in this section
            section_elems = elements[start_idx:end_idx]
            non_empty_paras = 0
            for elem in section_elems:
                tag = getattr(elem, 'tagName', None)
                if tag == 'text:p':
                    text = get_para_text(elem).strip()
                    if text:
                        non_empty_paras += 1
            if non_empty_paras >= 3:  # At least one paper (title + authors + abstract)
                sections_with_papers += 1

        if sections_with_papers == 3:
            print(f"PASS: Component 1 — all three date sections contain paper content ({sections_with_papers}/3 sections)")
            total_score += 0.30
        elif sections_with_papers > 0:
            partial = round(0.10 * sections_with_papers, 2)
            print(f"PARTIAL: Component 1 — {sections_with_papers}/3 date sections have paper content (+{partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 1 — no date sections contain paper content")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: Paper titles use bold formatting
    # Score: 0.30 — fails on initial (only empty sections with headings)
    # Detection: span style name contains 'bold'/'Bold' or font-weight=bold in auto style
    # OR span style maps to a style with font-weight=bold
    # ------------------------------------------------------------------
    try:
        bold_title_count = 0
        total_title_count = 0

        # Identify "bold" styles: either named with 'Bold'/'bold' or having font-weight=bold
        bold_style_names = set()
        for sname, sprops in auto_styles.items():
            fw = sprops.get('font-weight', '')
            if fw == 'bold' or 'bold' in sname.lower():
                bold_style_names.add(sname)

        # Scan all text:p paragraphs for bold span usage
        for elem in elements:
            tag = getattr(elem, 'tagName', None)
            if tag != 'text:p':
                continue
            para_text = get_para_text(elem).strip()
            if not para_text:
                continue
            para_style = elem.getAttribute('stylename') or ''
            if para_style == 'IndentedAbstract':
                continue  # abstracts are not titles

            # Check if any span in this paragraph uses a bold style
            span_styles_used = get_span_styles(elem)
            if any(s in bold_style_names for s in span_styles_used):
                bold_title_count += 1
                total_title_count += 1
            elif span_styles_used:
                # Has spans but none are bold
                total_title_count += 1
            # Paragraphs without spans are plain text (no formatting) — count as non-bold title
            # but only if they have substantial text (likely a title)
            # We do NOT count these as bold_title_count

        if total_title_count == 0:
            print("FAIL: Component 2 — no paper entries with span formatting found")
        elif bold_title_count >= 4:  # At least 4 bold titles across 3 days (generous threshold)
            print(f"PASS: Component 2 — {bold_title_count} paper titles have bold formatting")
            total_score += 0.30
        elif bold_title_count >= 2:
            print(f"PARTIAL: Component 2 — {bold_title_count} paper titles have bold formatting (+0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — only {bold_title_count} titles found with bold formatting")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: Paper authors use italic formatting
    # Score: 0.20 — fails on initial (no paper entries)
    # Detection: span style name contains 'italic'/'Italic' or font-style=italic
    # ------------------------------------------------------------------
    try:
        italic_author_count = 0

        # Identify "italic" styles
        italic_style_names = set()
        for sname, sprops in auto_styles.items():
            fs = sprops.get('font-style', '')
            if fs == 'italic' or 'italic' in sname.lower():
                italic_style_names.add(sname)

        for elem in elements:
            tag = getattr(elem, 'tagName', None)
            if tag != 'text:p':
                continue
            para_text = get_para_text(elem).strip()
            if not para_text:
                continue
            para_style = elem.getAttribute('stylename') or ''
            if para_style == 'IndentedAbstract':
                continue

            span_styles_used = get_span_styles(elem)
            if any(s in italic_style_names for s in span_styles_used):
                italic_author_count += 1

        if italic_author_count >= 4:  # At least 4 author lines across 3 days
            print(f"PASS: Component 3 — {italic_author_count} author lines have italic formatting")
            total_score += 0.20
        elif italic_author_count >= 2:
            print(f"PARTIAL: Component 3 — {italic_author_count} author lines have italic formatting (+0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — only {italic_author_count} author lines found with italic formatting")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------
    # Component 4: Abstracts use indented paragraph style
    # Score: 0.10 — fails on initial (no paper content)
    # Detection: paragraphs with IndentedAbstract style OR margin-left > 0
    # ------------------------------------------------------------------
    try:
        indented_abstract_count = 0

        # Identify "indented" styles: margin-left set
        indented_style_names = set()
        for sname, sprops in auto_styles.items():
            ml = sprops.get('margin-left', '')
            if ml and ml not in ('0', '0cm', '0mm', '0in', '0pt'):
                indented_style_names.add(sname)
            if 'indent' in sname.lower() or 'abstract' in sname.lower():
                indented_style_names.add(sname)

        for elem in elements:
            tag = getattr(elem, 'tagName', None)
            if tag != 'text:p':
                continue
            para_text = get_para_text(elem).strip()
            if not para_text:
                continue
            para_style = elem.getAttribute('stylename') or ''
            if para_style in indented_style_names or 'indent' in para_style.lower():
                indented_abstract_count += 1

        if indented_abstract_count >= 3:  # At least 3 abstracts across 3 days
            print(f"PASS: Component 4 — {indented_abstract_count} abstract paragraphs use indented style")
            total_score += 0.10
        elif indented_abstract_count >= 1:
            print(f"PARTIAL: Component 4 — {indented_abstract_count} abstract paragraphs use indented style (+0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 — no indented abstract paragraphs found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ------------------------------------------------------------------
    # Component 5: Duplicates section exists with non-empty content
    # Score: 0.10 — fails on initial (Duplicates heading exists but no content)
    # ------------------------------------------------------------------
    try:
        dup_heading_found = 'Duplicates' in heading_positions
        dup_content_found = False

        if dup_heading_found:
            dup_idx = heading_positions['Duplicates']
            dup_texts = []
            # Collect non-empty paragraphs after Duplicates heading
            for elem in elements[dup_idx + 1:]:
                tag = getattr(elem, 'tagName', None)
                if tag == 'text:h':
                    break  # Hit next section
                if tag == 'text:p':
                    text = get_para_text(elem).strip()
                    if text:
                        dup_texts.append(text)
            dup_content_found = len(dup_texts) > 0
            if dup_content_found:
                print(f"  Duplicates section content: {repr(dup_texts[0][:80])}")

        if dup_heading_found and dup_content_found:
            print("PASS: Component 5 — Duplicates section exists with content")
            total_score += 0.10
        elif dup_heading_found:
            print("FAIL: Component 5 — Duplicates heading found but section has no content")
        else:
            print("FAIL: Component 5 — Duplicates heading not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
