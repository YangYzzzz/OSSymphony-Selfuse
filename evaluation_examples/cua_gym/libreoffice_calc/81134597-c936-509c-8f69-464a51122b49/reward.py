"""
Reward Script: Canada TRV Guide Writer Document
Task ID: osworld_multi_apps_travel_permit_research_006
Domain: libreoffice_writer (ODT)
Scoring:
  Component 1 (0.35): File exists at Desktop/canada_trv_guide.odt with 5 required section headings
  Component 2 (0.40): Required Documents Checklist section has >= 5 formatted [x] checklist items
  Component 3 (0.25): Document contains fee information (CAD amounts) and processing time content
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_travel_permit_research_006'
FILE_PATH = '/home/user/Desktop/canada_trv_guide.odt'

REQUIRED_SECTIONS = [
    'eligibility',
    'application',
    'required documents',
    'processing',
    'fee',
]


def get_text(el):
    """Recursively extract plain text from an ODF element."""
    text = ''
    for node in el.childNodes:
        if node.nodeType == node.TEXT_NODE:
            text += node.data
        elif hasattr(node, 'childNodes'):
            text += get_text(node)
    return text


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.isfile(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load the ODT file
    try:
        from odf.opendocument import load
        from odf.text import P, H
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all headings
    try:
        headings = []
        for el in doc.body.getElementsByType(H):
            t = get_text(el).strip()
            level = el.getAttribute('outlinelevel') or '?'
            if t:
                headings.append((level, t.lower()))
    except Exception as e:
        print(f"ERROR: Could not read headings: {e}")
        headings = []

    # Collect all paragraph texts
    try:
        all_para_texts = []
        for el in doc.body.getElementsByType(P):
            t = get_text(el).strip()
            if t:
                all_para_texts.append(t)
        full_text = '\n'.join(all_para_texts).lower()
    except Exception as e:
        print(f"ERROR: Could not read paragraphs: {e}")
        all_para_texts = []
        full_text = ''

    # -----------------------------------------------------------------------
    # Component 1: Document has a main title heading and all 5 required section
    # headings (Eligibility Requirements, Application Steps, Required Documents
    # Checklist, Processing Times, Fees). (0.35 points)
    # -----------------------------------------------------------------------
    try:
        h1_texts = [t for (level, t) in headings if level == '1']
        h2_texts = [t for (level, t) in headings if level == '2']

        has_title = len(h1_texts) >= 1
        sections_found = []
        for required_kw in REQUIRED_SECTIONS:
            found = any(required_kw in h2 for h2 in h2_texts)
            sections_found.append(found)

        all_sections_present = all(sections_found)
        missing = [REQUIRED_SECTIONS[i] for i, found in enumerate(sections_found) if not found]

        sections_found_count = sum(sections_found)
        if has_title and all_sections_present:
            print(f"PASS: Component 1 — Title found and all 5 required sections present. "
                  f"H1: {h1_texts[0][:60] if h1_texts else 'n/a'}, H2 count: {len(h2_texts)} (0.35 pts)")
            total_score += 0.35
        elif has_title and sections_found_count >= 3:
            # Partial: at least 3 of 5 sections present
            print(f"PARTIAL: Component 1 — Title found but only {sections_found_count}/5 sections. "
                  f"Missing: {missing} (0.20 pts)")
            if sections_found_count >= 3:
                total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Title: {has_title}, missing sections: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Required Documents Checklist section contains >= 5 formatted
    # checklist items marked with [x]. (0.40 points)
    # -----------------------------------------------------------------------
    try:
        checklist_items = []
        for t in all_para_texts:
            if '[x]' in t.lower() or '[x]' in t:
                checklist_items.append(t)

        num_checklist = len(checklist_items)

        if num_checklist >= 5:
            print(f"PASS: Component 2 — Found {num_checklist} formatted [x] checklist items "
                  f"in Required Documents section (0.40 pts)")
            total_score += 0.40
        elif num_checklist >= 2:
            print(f"PARTIAL: Component 2 — Found only {num_checklist} [x] checklist items "
                  f"(expected >= 5) (0.20 pts)")
            if num_checklist >= 2:
                total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Found {num_checklist} [x] checklist items, expected >= 5")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Document contains fee information (CAD dollar amounts) AND
    # processing time content mentioning days or weeks. (0.25 points)
    # -----------------------------------------------------------------------
    try:
        has_fees = 'cad' in full_text or 'canadian dollar' in full_text or '$100' in full_text
        has_processing = ('days' in full_text or 'weeks' in full_text or
                          'processing' in full_text)

        missing_part = []
        if not has_fees:
            missing_part.append('fees')
        if not has_processing:
            missing_part.append('processing times')

        if has_fees and has_processing:
            print("PASS: Component 3 — Fee information (CAD) and processing times found (0.25 pts)")
            total_score += 0.25
        elif has_fees or has_processing:
            print(f"PARTIAL: Component 3 — Missing content: {missing_part} (0.12 pts)")
            if has_fees or has_processing:
                total_score += 0.12
        else:
            print(f"FAIL: Component 3 — Neither fee (CAD) nor processing time content found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if not os.path.isfile(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
