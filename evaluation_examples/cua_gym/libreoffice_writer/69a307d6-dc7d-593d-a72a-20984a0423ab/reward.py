"""
FINAL REWARD SCRIPT - SUCCESS
Task: Our company letterhead has to follow a strict layout: Top margin 2.00 cm, Bottom 2.00 cm, Left 3.00 cm, Right 3.00 cm. In LibreOffice Writer, how do I set those values as the default Page Style so every new document automatically opens with those exact margins?
Generated: 2025-09-10 16:47:50
Status: success
Model: azure-o3
Total Steps: 8
"""

import os
import re
import zipfile
from docx import Document
from typing import Dict
from lxml import etree

# ---------------------------------------------------------
# Helper conversion
# ---------------------------------------------------------

def twips_to_cm(twips: float) -> float:
    """Convert twips (1/1440 inch) to centimetres."""
    return float(twips) / 1440 * 2.54

# ---------------------------------------------------------
# DOCX verification
# ---------------------------------------------------------

def verify_docx_margins(file_path: str, target: Dict[str, float]) -> float:
    """Return a score (0-1) for how many DOCX section margins match target."""
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Could not load DOCX '{file_path}': {e}")
        return 0.0

    total_sections = len(doc.sections)
    counts_correct = {side: 0 for side in target}

    for idx, sect in enumerate(doc.sections):
        margins_cm = {
            'top': sect.top_margin.cm,
            'bottom': sect.bottom_margin.cm,
            'left': sect.left_margin.cm,
            'right': sect.right_margin.cm,
        }
        print(f"  Section {idx + 1} margins (cm): {margins_cm}")

        for side in target:
            # allow a small tolerance of ±0.05 cm
            if abs(margins_cm[side] - target[side]) <= 0.05:
                counts_correct[side] += 1

    # Each side worth 0.25, scaled by proportion of sections for which that side is correct
    score = sum(counts_correct[side] / total_sections * 0.25 for side in target)
    return score

# ---------------------------------------------------------
# ODT verification (XML based)
# ---------------------------------------------------------

def verify_odt_margins(file_path: str, target: Dict[str, float]) -> float:
    """Return a score (0-1) for how many page-layout margins in an ODT match target."""
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            # styles.xml is where default page-styles normally live. Fallback to content.xml.
            xml_bytes = z.read('styles.xml') if 'styles.xml' in z.namelist() else z.read('content.xml')
        root = etree.fromstring(xml_bytes)
    except Exception as e:
        print(f"✗ Unable to parse ODT '{file_path}': {e}")
        return 0.0

    ns = {
        'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
        'fo':    'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'
    }

    layouts = root.xpath('.//style:page-layout-properties', namespaces=ns)
    if not layouts:
        print("✗ No <style:page-layout-properties> elements found – cannot evaluate margins")
        return 0.0

    counts_correct = {side: 0 for side in target}

    for layout in layouts:
        raw = {
            'top':    layout.get('{%s}margin-top'    % ns['fo']),
            'bottom': layout.get('{%s}margin-bottom' % ns['fo']),
            'left':   layout.get('{%s}margin-left'   % ns['fo']),
            'right':  layout.get('{%s}margin-right'  % ns['fo'])
        }
        print(f"  Page-layout margins raw: {raw}")

        for side, val in raw.items():
            if val is None:
                continue
            m = re.match(r'([0-9.]+)cm', val)
            if not m:
                continue
            cm_val = float(m.group(1))
            if abs(cm_val - target[side]) <= 0.05:
                counts_correct[side] += 1

    total_layouts = len(layouts)
    score = sum(counts_correct[side] / total_layouts * 0.25 for side in target)
    return score

# ---------------------------------------------------------
# Main verification routine
# ---------------------------------------------------------

def find_documents() -> list:
    """Search user home for .docx / .odt files (recursively)."""
    matches = []
    for root, _, files in os.walk('/home/user'):
        for fn in files:
            if fn.lower().endswith(('.docx', '.odt')):
                matches.append(os.path.join(root, fn))
    return matches


def verify_task() -> float:
    # Target margins in centimetres
    target = {'top': 2.0, 'bottom': 2.0, 'left': 3.0, 'right': 3.0}

    docs = find_documents()
    if not docs:
        print("✗ No document files found. Score = 0.0")
        print("REWARD: 0.0")
        return 0.0

    print("Found document files to evaluate:")
    for p in docs:
        print(f" • {p}")

    best_score = 0.0
    best_file = None

    for path in docs:
        if path.lower().endswith('.docx'):
            score = verify_docx_margins(path, target)
        else:  # .odt
            score = verify_odt_margins(path, target)
        print(f"Score for {os.path.basename(path)}: {score}\n")

        if score > best_score:
            best_score = score
            best_file = path

    best_score = min(best_score, 1.0)  # hard cap at 1.0
    print(f"Best score achieved: {best_score} (file: {best_file})")
    print(f"REWARD: {best_score}")
    return best_score

# ---------------------------------------------------------
# Execute when run as script
# ---------------------------------------------------------
if __name__ == "__main__":
    verify_task()
