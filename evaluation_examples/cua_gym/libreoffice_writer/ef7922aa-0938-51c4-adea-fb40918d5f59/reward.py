"""
Reward Script: Extract PPTX text to Writer ODT document
Task ID: osworld_multi_apps_impress_text_to_writer_003
Domain: libreoffice_writer (multi-app: impress + writer)

Task: Open 'quarterly_report.pptx' from Documents in LibreOffice Impress.
      Extract all text from each slide (titles and body text).
      Create a Writer document where each slide's content is preceded by
      the label 'Slide X:' (as bold text), followed by the slide title
      and body text. Maintain the bullet point hierarchy from the
      presentation. Save as 'quarterly_report_text.odt' on the Desktop.

Scoring:
  Component 1: Output file 'quarterly_report_text.odt' exists on Desktop (precondition gate)
  Component 2: All 6 slide labels 'Slide 1:' through 'Slide 6:' are present in the document (0.4 pts)
  Component 3: Slide labels are formatted as bold text (0.3 pts)
  Component 4: Slide content (titles and bullet text from PPTX) is present in the document (0.3 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_impress_text_to_writer_003'

# The output file path as required by the task
ODT_PATH = os.path.join(WORKDIR, 'Desktop', 'quarterly_report_text.odt')

# Expected slide titles from the PPTX (ground truth from task context)
EXPECTED_SLIDE_TITLES = [
    'Q3 2025 Financial Overview',
    'Sales Performance by Region',
    'Product Highlights',
    'Operational Efficiency Initiatives',
    'Customer Success Stories',
    'Q4 2025 Strategic Goals',
]

# A sample of expected body text to verify content extraction (one from each slide)
EXPECTED_BODY_SAMPLES = [
    'Total revenue reached',         # Slide 1
    'North America',                 # Slide 2
    'Enterprise Suite',              # Slide 3
    'Automated billing',             # Slide 4
    'Acme Corporation',              # Slide 5
    'Target revenue',                # Slide 6
]


def get_odt_paragraphs_text(odt_path):
    """
    Load ODT file and return list of paragraph texts.
    Uses odfpy library available on the VM.
    """
    from odf.opendocument import load
    from odf.text import P

    odt_doc = load(odt_path)
    paragraphs = odt_doc.getElementsByType(P)

    texts = []
    for para in paragraphs:
        full_text = ''
        for node in para.childNodes:
            if hasattr(node, 'data'):
                full_text += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if hasattr(child, 'data'):
                        full_text += child.data
        texts.append(full_text)
    return texts


def check_bold_labels(odt_path):
    """
    Check if 'Slide X:' labels in the ODT document are formatted as bold.
    Returns (bool, list_of_bold_labels) indicating if all 6 labels are bold.

    Checks:
    1. Via span with bold automatic style (BoldLabel or font-weight:bold)
    2. Via paragraph style with font-weight:bold
    3. Via python-docx bold runs if file is also available as docx (fallback)
    """
    from odf.opendocument import load
    from odf.text import P, Span

    BOLD_FO_NS = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'

    odt_doc = load(odt_path)

    # Build automatic style bold map
    auto_styles_bold = {}
    if hasattr(odt_doc, 'automaticstyles'):
        for ast in odt_doc.automaticstyles.childNodes:
            try:
                name = ast.getAttribute('name')
                bold = False
                for child in ast.childNodes:
                    if hasattr(child, 'attributes'):
                        if child.attributes.get((BOLD_FO_NS, 'font-weight')) == 'bold':
                            bold = True
                auto_styles_bold[name] = bold
            except Exception:
                pass

    # Also check named styles
    named_styles_bold = {}
    try:
        for named_style in odt_doc.styles.childNodes:
            try:
                sname = named_style.getAttribute('name')
                bold = False
                for child in named_style.childNodes:
                    if hasattr(child, 'attributes'):
                        if child.attributes.get((BOLD_FO_NS, 'font-weight')) == 'bold':
                            bold = True
                named_styles_bold[sname] = bold
            except Exception:
                pass
    except Exception:
        pass

    paragraphs = odt_doc.getElementsByType(P)
    slide_label_pattern = re.compile(r'^Slide\s+\d+\s*:', re.IGNORECASE)
    bold_labels = []
    non_bold_labels = []

    for para in paragraphs:
        # Get full text
        full_text = ''
        for node in para.childNodes:
            if hasattr(node, 'data'):
                full_text += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if hasattr(child, 'data'):
                        full_text += child.data

        if not slide_label_pattern.match(full_text.strip()):
            continue

        # This is a "Slide X:" paragraph — check if it has bold formatting
        label_is_bold = False

        # Method 1: Check if any span in the paragraph uses a bold style
        spans = para.getElementsByType(Span)
        for span in spans:
            try:
                sname = span.getAttribute('stylename')
                if auto_styles_bold.get(sname, False) or named_styles_bold.get(sname, False):
                    label_is_bold = True
                    break
            except Exception:
                pass

        # Method 2: Check paragraph's own style for bold
        if not label_is_bold:
            try:
                para_style = para.getAttribute('stylename')
                if auto_styles_bold.get(para_style, False) or named_styles_bold.get(para_style, False):
                    label_is_bold = True
            except Exception:
                pass

        if label_is_bold:
            bold_labels.append(full_text.strip())
        else:
            non_bold_labels.append(full_text.strip())

    return bold_labels, non_bold_labels


def verify_task(odt_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: File must exist
    if not os.path.exists(odt_path):
        print(f"CRITICAL: Output file not found: {odt_path}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found output file: {odt_path}")

    # Load ODT paragraphs
    try:
        para_texts = get_odt_paragraphs_text(odt_path)
        print(f"INFO: Loaded {len(para_texts)} paragraphs from ODT file")
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODT file {odt_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Combine all text for content checks
    all_text = '\n'.join(para_texts)

    # Component 1: All 6 slide labels present (0.4 points)
    # Each label 'Slide 1:' through 'Slide 6:' must appear as its own paragraph
    # or within the document text. We check for paragraph-level presence.
    try:
        slide_labels_found = []
        slide_labels_missing = []
        for n in range(1, 7):
            pattern = re.compile(r'^Slide\s+' + str(n) + r'\s*:', re.IGNORECASE)
            found = any(pattern.match(t.strip()) for t in para_texts)
            if found:
                slide_labels_found.append(f'Slide {n}:')
            else:
                slide_labels_missing.append(f'Slide {n}:')

        if len(slide_labels_found) == 6:
            print(f"PASS: Component 1 — All 6 slide labels found: {slide_labels_found} (0.4 pts)")
            total_score += 0.4
        elif len(slide_labels_found) >= 4:
            partial = round(0.4 * len(slide_labels_found) / 6, 2)
            print(f"PARTIAL: Component 1 — {len(slide_labels_found)}/6 slide labels found: "
                  f"{slide_labels_found}. Missing: {slide_labels_missing} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Only {len(slide_labels_found)}/6 slide labels found. "
                  f"Found: {slide_labels_found}, Missing: {slide_labels_missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Slide labels are bold (0.3 points)
    try:
        bold_labels, non_bold_labels = check_bold_labels(odt_path)
        if len(bold_labels) == 6:
            print(f"PASS: Component 2 — All 6 slide labels are bold: {bold_labels} (0.3 pts)")
            total_score += 0.3
        elif len(bold_labels) >= 4:
            partial = round(0.3 * len(bold_labels) / 6, 2)
            print(f"PARTIAL: Component 2 — {len(bold_labels)}/6 slide labels are bold. "
                  f"Bold: {bold_labels}, Not bold: {non_bold_labels} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {len(bold_labels)}/6 slide labels are bold. "
                  f"Bold: {bold_labels}, Not bold: {non_bold_labels}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Slide content (titles and body text) is present (0.3 points)
    # Check for slide titles AND a sample of body bullet text
    try:
        titles_found = 0
        body_samples_found = 0

        for title in EXPECTED_SLIDE_TITLES:
            if title.lower() in all_text.lower():
                titles_found += 1

        for sample in EXPECTED_BODY_SAMPLES:
            if sample.lower() in all_text.lower():
                body_samples_found += 1

        titles_ratio = titles_found / len(EXPECTED_SLIDE_TITLES)
        body_ratio = body_samples_found / len(EXPECTED_BODY_SAMPLES)

        # Both titles and body content must be present for full credit
        content_score = round(0.3 * min(titles_ratio, body_ratio), 2)

        if titles_found == 6 and body_samples_found == 6:
            print(f"PASS: Component 3 — All slide titles ({titles_found}/6) and body samples "
                  f"({body_samples_found}/6) found in document (0.3 pts)")
            total_score += 0.3
        elif titles_found >= 4 or body_samples_found >= 4:
            print(f"PARTIAL: Component 3 — Titles: {titles_found}/6, Body samples: {body_samples_found}/6 "
                  f"({content_score} pts)")
            total_score += content_score
        else:
            print(f"FAIL: Component 3 — Insufficient content. "
                  f"Titles: {titles_found}/6, Body samples: {body_samples_found}/6")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(ODT_PATH):
    print(f"File not found: {ODT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(ODT_PATH)
