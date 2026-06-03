"""
Reward Script: Insert changelog content into 'Recent Changes' section
Task ID: writer_tech_088
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3) — Placeholder text removed from 'Recent Changes' section
  Component 2 (0.3) — Changelog content present (version headings from changelog.docx)
  Component 3 (0.2) — All three version sections present with correct version numbers
  Component 4 (0.2) — Bullet items from changelog.docx present in the document
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_088'


def find_section_paragraphs(doc, start_heading, end_heading):
    """Find paragraphs between two headings (exclusive of both)."""
    paras = doc.paragraphs
    start_idx = None
    end_idx = None
    for i, p in enumerate(paras):
        if start_heading in p.text and 'Heading' in p.style.name:
            start_idx = i
        elif end_heading in p.text and 'Heading' in p.style.name and start_idx is not None:
            end_idx = i
            break
    if start_idx is not None and end_idx is not None:
        return paras[start_idx + 1:end_idx]
    elif start_idx is not None:
        return paras[start_idx + 1:]
    return []


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get paragraphs in the 'Recent Changes' section (between heading 5 and heading 6)
    section_paras = find_section_paragraphs(doc, 'Recent Changes', '6. Contact')
    section_texts = [p.text.strip() for p in section_paras if p.text.strip()]

    print(f"INFO: Found {len(section_paras)} paragraphs in 'Recent Changes' section")
    print(f"INFO: Non-empty texts: {section_texts[:5]}...")

    # Component 1: Placeholder text removed (0.3 points)
    # Initial has: "[This section should be linked to the external changelog file..."
    # Golden should NOT have this placeholder
    try:
        placeholder = "should be linked to the external changelog"
        has_placeholder = any(placeholder in p.text for p in section_paras)
        if not has_placeholder and len(section_texts) > 0:
            print(f"PASS: Component 1 — Placeholder text removed and section has content (0.3 pts)")
            total_score += 0.3
        elif not has_placeholder and len(section_texts) == 0:
            print(f"FAIL: Component 1 — Placeholder removed but section is empty")
        else:
            print(f"FAIL: Component 1 — Placeholder text still present")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Changelog content present — version headings exist (0.3 points)
    # Golden should have "Version 3.2.1", "Version 3.2.0", "Version 3.1.4"
    try:
        version_markers = ["Version 3.2.1", "Version 3.2.0", "Version 3.1.4"]
        found_versions = []
        for marker in version_markers:
            if any(marker in t for t in section_texts):
                found_versions.append(marker)

        if len(found_versions) >= 2:
            print(f"PASS: Component 2 — Found {len(found_versions)}/3 version headings: {found_versions} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Found only {len(found_versions)}/3 version headings: {found_versions}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All three version sections present with correct dates (0.2 points)
    try:
        version_date_markers = [
            "Version 3.2.1 - 2025-11-28",
            "Version 3.2.0 - 2025-11-15",
            "Version 3.1.4 - 2025-10-30",
        ]
        found_dated = []
        for marker in version_date_markers:
            if any(marker in t for t in section_texts):
                found_dated.append(marker)

        if len(found_dated) == 3:
            print(f"PASS: Component 3 — All 3 version sections with dates found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Found {len(found_dated)}/3 dated version entries: {found_dated}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Key bullet items from changelog present (0.2 points)
    # Check for at least 5 of the specific changelog bullet items
    try:
        key_items = [
            "memory leak in session handler",
            "race condition in database connection pool",
            "XSS vulnerability",
            "WebSocket-based real-time notifications",
            "two-factor authentication",
            "dark mode theme",
            "OpenSearch 2.11",
            "pagination offset",
            "file upload timeout",
        ]
        found_items = 0
        all_text = " ".join(section_texts)
        for item in key_items:
            if item in all_text:
                found_items += 1

        if found_items >= 5:
            print(f"PASS: Component 4 — Found {found_items}/{len(key_items)} changelog items (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Found only {found_items}/{len(key_items)} changelog items")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
