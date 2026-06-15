"""
Reward Script: Create a list of figures and a list of tables after the TOC
Task ID: writer_rm_078
Domain: libreoffice_writer (ODT)
Scoring:
  Component 1 (0.25): illustration-index element exists
  Component 2 (0.25): table-index element exists
  Component 3 (0.20): Both indices are positioned after TOC and before first chapter heading
  Component 4 (0.15): illustration-index contains entries for all 7 figures
  Component 5 (0.15): table-index contains entries for all 6 tables
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_078'

# ODF XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
}

# Expected figure captions (the text after "Figure N: ")
EXPECTED_FIGURES = [
    "Healthcare Analytics Framework Overview",
    "Research Methodology and Data Collection Process",
    "Patient Outcome Improvement Trends (2023-2025)",
    "ROC Curves for Predictive Models",
    "Feature Importance Rankings for Sepsis Prediction Model",
    "Return on Investment Timeline by Institution",
    "Recommended Implementation Roadmap",
]

# Expected table captions (the text after "Table N: ")
EXPECTED_TABLES = [
    "Healthcare Network Overview",
    "Research Phases and Parameters",
    "Key Patient Outcome Metrics",
    "Predictive Model Performance Comparison",
    "Investment and ROI Summary",
    "Strategic Recommendations Summary",
]


def get_all_text(elem):
    """Recursively get all text content from an XML element."""
    texts = []
    if elem.text:
        texts.append(elem.text)
    for child in elem:
        texts.extend(get_all_text(child))
    if elem.tail:
        texts.append(elem.tail)
    return texts


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load ODT file (it's a zip containing content.xml)
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the office:text body element and its direct children
    body = root.find('.//{urn:oasis:names:tc:opendocument:xmlns:office:1.0}text')
    if body is None:
        print("CRITICAL: No office:text element found")
        print("REWARD: 0.0")
        return 0.0

    children = list(body)

    # Component 1: illustration-index element exists (0.25 points)
    try:
        illust_indices = root.findall('.//text:illustration-index', NS)
        if len(illust_indices) >= 1:
            illust_name = illust_indices[0].get(
                '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}name', ''
            )
            print(f"PASS: Component 1 — illustration-index exists (name='{illust_name}') (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — No illustration-index element found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: table-index element exists (0.25 points)
    try:
        table_indices = root.findall('.//text:table-index', NS)
        if len(table_indices) >= 1:
            tab_name = table_indices[0].get(
                '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}name', ''
            )
            print(f"PASS: Component 2 — table-index exists (name='{tab_name}') (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — No table-index element found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Both indices are positioned after TOC and before first chapter heading (0.20 points)
    try:
        toc_idx = None
        illust_idx = None
        table_idx = None
        first_heading_after_toc_idx = None

        for idx, child in enumerate(children):
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

            if tag == 'table-of-content':
                toc_idx = idx
            elif tag == 'illustration-index':
                illust_idx = idx
            elif tag == 'table-index':
                table_idx = idx
            elif tag == 'h' and toc_idx is not None and first_heading_after_toc_idx is None:
                # First heading after the TOC
                first_heading_after_toc_idx = idx

        position_ok = True
        details = []

        if toc_idx is None:
            position_ok = False
            details.append("No TOC found")
        if illust_idx is None:
            position_ok = False
            details.append("No illustration-index found")
        if table_idx is None:
            position_ok = False
            details.append("No table-index found")

        if position_ok:
            # Both must be after TOC
            if illust_idx <= toc_idx:
                position_ok = False
                details.append(f"illustration-index (pos {illust_idx}) not after TOC (pos {toc_idx})")
            if table_idx <= toc_idx:
                position_ok = False
                details.append(f"table-index (pos {table_idx}) not after TOC (pos {toc_idx})")
            # Both must be before first heading after TOC (if any)
            if first_heading_after_toc_idx is not None:
                if illust_idx >= first_heading_after_toc_idx:
                    position_ok = False
                    details.append(f"illustration-index (pos {illust_idx}) not before first heading (pos {first_heading_after_toc_idx})")
                if table_idx >= first_heading_after_toc_idx:
                    position_ok = False
                    details.append(f"table-index (pos {table_idx}) not before first heading (pos {first_heading_after_toc_idx})")

        if position_ok:
            print(f"PASS: Component 3 — Both indices positioned after TOC (pos {toc_idx}) and before first heading (pos {first_heading_after_toc_idx}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Positioning issues: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: illustration-index contains entries for all 7 figures (0.15 points)
    try:
        if len(illust_indices) >= 1:
            all_text = ' '.join(get_all_text(illust_indices[0]))
            matched = 0
            for fig_caption in EXPECTED_FIGURES:
                if fig_caption in all_text:
                    matched += 1
                else:
                    print(f"  DETAIL: Missing figure caption: '{fig_caption}'")

            if matched == len(EXPECTED_FIGURES):
                print(f"PASS: Component 4 — All {len(EXPECTED_FIGURES)} figure captions found in illustration-index (0.15 pts)")
                total_score += 0.15
            elif matched > 0:
                # Partial credit proportional to figures found
                partial = 0.15 * (matched / len(EXPECTED_FIGURES))
                print(f"PARTIAL: Component 4 — {matched}/{len(EXPECTED_FIGURES)} figure captions found ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — No figure captions found in illustration-index")
        else:
            print(f"FAIL: Component 4 — No illustration-index to check entries")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: table-index contains entries for all 6 tables (0.15 points)
    try:
        if len(table_indices) >= 1:
            all_text = ' '.join(get_all_text(table_indices[0]))
            matched = 0
            for tab_caption in EXPECTED_TABLES:
                if tab_caption in all_text:
                    matched += 1
                else:
                    print(f"  DETAIL: Missing table caption: '{tab_caption}'")

            if matched == len(EXPECTED_TABLES):
                print(f"PASS: Component 5 — All {len(EXPECTED_TABLES)} table captions found in table-index (0.15 pts)")
                total_score += 0.15
            elif matched > 0:
                # Partial credit proportional to tables found
                partial = 0.15 * (matched / len(EXPECTED_TABLES))
                print(f"PARTIAL: Component 5 — {matched}/{len(EXPECTED_TABLES)} table captions found ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — No table captions found in table-index")
        else:
            print(f"FAIL: Component 5 — No table-index to check entries")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
