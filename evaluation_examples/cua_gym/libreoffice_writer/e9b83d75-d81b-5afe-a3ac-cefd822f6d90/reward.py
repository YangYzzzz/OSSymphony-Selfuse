"""
Reward Script: cs.CL Papers Bibliography in LibreOffice Writer
Task ID: osworld_multi_apps_hf_papers_writer_012
Domain: libreoffice_writer
Scoring:
  Component 1: 10 numbered paper entries exist              (0.30 pts)
  Component 2: Bold title spans present for each entry      (0.25 pts)
  Component 3: Italic author spans present for each entry   (0.20 pts)
  Component 4: Indented abstract paragraphs for each entry  (0.15 pts)
  Component 5: Keywords section with 10 content words       (0.10 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_hf_papers_writer_012'

FILE_PATH = os.path.join(WORKDIR, 'cls_papers.odt')

TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
STYLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'
FO_NS = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'


def get_text(elem):
    """Extract full text from a paragraph element, including spans."""
    full_text = ''
    for child in elem.childNodes:
        ctag = getattr(child, 'tagName', '')
        if child.nodeType == child.TEXT_NODE:
            full_text += child.data
        elif ctag == 'text:span':
            for gc in child.childNodes:
                if gc.nodeType == gc.TEXT_NODE:
                    full_text += gc.data
    return full_text


def get_span_styles(elem):
    """Return list of (style_name, span_text) for all spans in an element."""
    spans = []
    for child in elem.childNodes:
        ctag = getattr(child, 'tagName', '')
        if ctag == 'text:span':
            sp_style = child.attributes.get((TEXT_NS, 'style-name'), '')
            span_text = ''
            for gc in child.childNodes:
                if gc.nodeType == gc.TEXT_NODE:
                    span_text += gc.data
            spans.append((sp_style, span_text))
    return spans


def get_para_style(elem):
    """Return paragraph style name."""
    return elem.attributes.get((TEXT_NS, 'style-name'), '')


def get_auto_style_props(doc):
    """Build map of auto style name -> property dict."""
    props_map = {}
    for sty in doc.automaticstyles.childNodes:
        sname = sty.attributes.get((STYLE_NS, 'name'), '')
        if not sname:
            continue
        props = {}
        for child in sty.childNodes:
            ctag = getattr(child, 'tagName', '')
            for k, v in child.attributes.items():
                ns_uri, local = k
                props[f'{ctag}/{local}'] = v
        props_map[sname] = props
    return props_map


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODT document
    try:
        from odf.opendocument import load
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.text
    elements = list(body.childNodes)

    # Get auto-style properties for bold/italic/indent detection
    try:
        auto_style_props = get_auto_style_props(doc)
    except Exception as e:
        print(f"WARN: Could not parse auto styles: {e}")
        auto_style_props = {}

    # Identify bold and italic style names from auto styles
    bold_styles = set()
    italic_styles = set()
    indent_styles = set()
    for sname, props in auto_style_props.items():
        fw = props.get('style:text-properties/font-weight', '')
        fs = props.get('style:text-properties/font-style', '')
        ml = props.get('style:paragraph-properties/margin-left', '')
        if fw == 'bold':
            bold_styles.add(sname)
        if fs == 'italic':
            italic_styles.add(sname)
        if ml and ml != '0in' and ml != '0cm' and ml != '0':
            indent_styles.add(sname)

    print(f"Bold styles: {bold_styles}")
    print(f"Italic styles: {italic_styles}")
    print(f"Indent styles: {indent_styles}")

    # Component 1: Exactly 10 numbered paper entries [1] through [10] (0.30 points)
    # This checks for sequential numbered entries - the core structure of the bibliography
    try:
        numbered_entries = []
        for elem in elements:
            text = get_text(elem)
            m = re.match(r'^\[(\d+)\]', text)
            if m:
                numbered_entries.append(int(m.group(1)))

        expected_nums = list(range(1, 11))
        if numbered_entries == expected_nums:
            print(f"PASS: Component 1 — exactly 10 numbered entries [1]-[10] found (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — expected numbered entries [1]-[10], found: {numbered_entries}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Bold title spans present (0.25 points)
    # For each paper entry, the title text (after "[N] ") should be in a bold span
    # Award partial credit per entry found with bold title
    try:
        bold_title_count = 0
        title_paragraphs = []
        for elem in elements:
            text = get_text(elem)
            if re.match(r'^\[\d+\]', text):
                title_paragraphs.append(elem)

        for elem in title_paragraphs:
            spans = get_span_styles(elem)
            # Check if any span has a bold style and contains the title (not just "[N] ")
            has_bold_title = False
            for (sname, stext) in spans:
                if sname in bold_styles and len(stext.strip()) > 5:
                    has_bold_title = True
                    break
            if has_bold_title:
                bold_title_count += 1

        if len(title_paragraphs) > 0 and bold_title_count == len(title_paragraphs):
            print(f"PASS: Component 2 — all {bold_title_count} title paragraphs have bold title spans (0.25 pts)")
            total_score += 0.25
        elif bold_title_count > 0:
            frac = bold_title_count / 10.0
            partial = round(0.25 * frac, 4)
            print(f"PARTIAL: Component 2 — {bold_title_count}/10 titles have bold spans ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no bold title spans found (checked {len(title_paragraphs)} title paras)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Italic author spans present (0.20 points)
    # For each paper, the authors line (immediately after title para) should have italic span
    # Each entry pattern: [N] Title / Authors / arXiv venue / Abstract / blank
    try:
        italic_author_count = 0
        author_paragraphs = []

        # Collect author paragraphs: the element right after a title paragraph
        i = 0
        while i < len(elements):
            elem = elements[i]
            text = get_text(elem)
            if re.match(r'^\[\d+\]', text) and i + 1 < len(elements):
                author_para = elements[i + 1]
                author_text = get_text(author_para)
                # Make sure next paragraph is not another [N] entry or arXiv line
                if author_text and not re.match(r'^\[\d+\]', author_text) and 'arXiv preprint' not in author_text:
                    author_paragraphs.append(author_para)
            i += 1

        for elem in author_paragraphs:
            spans = get_span_styles(elem)
            has_italic = any(sname in italic_styles for (sname, _) in spans)
            if has_italic:
                italic_author_count += 1

        if len(author_paragraphs) > 0 and italic_author_count == len(author_paragraphs):
            print(f"PASS: Component 3 — all {italic_author_count} author paragraphs have italic spans (0.20 pts)")
            total_score += 0.20
        elif italic_author_count > 0:
            frac = italic_author_count / 10.0
            partial = round(0.20 * frac, 4)
            print(f"PARTIAL: Component 3 — {italic_author_count}/10 author paras have italic spans ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no italic author spans found (checked {len(author_paragraphs)} author paras)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Indented abstract paragraphs (0.15 points)
    # Abstract paragraphs should have a left-indent paragraph style (IndentedPara or equivalent)
    try:
        indented_count = 0
        abstract_paragraphs = []

        # Abstracts come after arXiv venue lines: pattern is [..., [N] Title, Authors, arXiv venue, ABSTRACT, blank]
        i = 0
        while i < len(elements):
            elem = elements[i]
            text = get_text(elem)
            if 'arXiv preprint arXiv:' in text and i + 1 < len(elements):
                abstract_para = elements[i + 1]
                abs_text = get_text(abstract_para)
                # Abstract is a non-empty paragraph after the arXiv line
                if abs_text.strip() and not re.match(r'^\[\d+\]', abs_text):
                    abstract_paragraphs.append(abstract_para)
            i += 1

        for elem in abstract_paragraphs:
            para_style = get_para_style(elem)
            if para_style in indent_styles:
                indented_count += 1

        if len(abstract_paragraphs) > 0 and indented_count == len(abstract_paragraphs):
            print(f"PASS: Component 4 — all {indented_count} abstract paragraphs are indented (0.15 pts)")
            total_score += 0.15
        elif indented_count > 0:
            frac = indented_count / 10.0
            partial = round(0.15 * frac, 4)
            print(f"PARTIAL: Component 4 — {indented_count}/10 abstract paras are indented ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — no indented abstract paragraphs found (checked {len(abstract_paragraphs)} abstract paras)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Keywords section with 10 content words (0.10 points)
    # After the last paper entry, there should be a 'Keywords' heading followed by a line with 10 words
    try:
        keywords_heading_found = False
        keywords_list_found = False
        keywords_count = 0
        keywords_text = ''

        for idx, elem in enumerate(elements):
            tag = getattr(elem, 'tagName', '')
            text = get_text(elem).strip()
            if tag == 'text:h' and text.lower() == 'keywords':
                keywords_heading_found = True
                # Next non-empty element should be the keyword list
                for j in range(idx + 1, min(idx + 3, len(elements))):
                    kw_text = get_text(elements[j]).strip()
                    if kw_text:
                        keywords_text = kw_text
                        # Count comma-separated keywords
                        kws = [k.strip() for k in kw_text.split(',') if k.strip()]
                        keywords_count = len(kws)
                        if keywords_count >= 8:  # Allow slight variation (8-12 keywords)
                            keywords_list_found = True
                        break

        if keywords_heading_found and keywords_list_found:
            print(f"PASS: Component 5 — Keywords section found with {keywords_count} words: {keywords_text[:80]!r} (0.10 pts)")
            total_score += 0.10
        elif keywords_heading_found:
            print(f"FAIL: Component 5 — Keywords heading found but list has {keywords_count} words (expected ~10): {keywords_text[:80]!r}")
        else:
            print(f"FAIL: Component 5 — no Keywords heading found in document")
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
