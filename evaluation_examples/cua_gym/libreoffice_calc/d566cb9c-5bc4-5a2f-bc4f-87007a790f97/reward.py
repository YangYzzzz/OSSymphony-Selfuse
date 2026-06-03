"""
Reward Script: Save MDN CSS Flexbox page content as flexbox_notes.docx on Desktop
Task ID: osworld_multi_apps_web_to_doc_001
Domain: libreoffice_writer (multi-app: web browser + LibreOffice Writer)
Scoring:
  Component 1: flexbox_notes.docx exists at /home/user/Desktop/ with non-zero size (0.30 pts)
  Component 2: Document has Heading 1 = 'Basic concepts of flexbox' (0.30 pts)
  Component 3: Document has at least 4 key H2 sections from the MDN article (0.20 pts)
  Component 4: Document has substantial content (>=20 non-empty paragraphs) (0.20 pts)
  Total: 1.0
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_to_doc_001'

# The expected file path on the VM
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'flexbox_notes.docx')

# Key H2 section headings from the MDN CSS Flexbox article
EXPECTED_H2_SECTIONS = [
    'The two axes of flexbox',
    'Start and end lines',
    'The flex container',
    'Multi-line flex containers with flex-wrap',
    'The flex-flow shorthand',
    'Properties applied to flex items',
    'Alignment, justification and distribution of free space between items',
    'Summary',
]

# Required heading 1 title
EXPECTED_H1 = 'Basic concepts of flexbox'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File exists at the correct Desktop path with non-zero size (0.30 points)
    # This is the primary task artifact — the file must be on the Desktop with exact name.
    # Initial env: Desktop is empty -> FAIL
    # Golden env: flexbox_notes.docx present -> PASS
    try:
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        if file_size > 0:
            print(f"PASS: Component 1 — file exists at {file_path} ({file_size} bytes) (0.30 pts)")
            total_score += 0.30
        elif file_size == 0:
            print(f"FAIL: Component 1 — file is empty: {file_path}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
        else:
            print(f"FAIL: Component 1 — file not found: {file_path}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Check python-docx availability for content verification
    docx_import_error = None
    try:
        from docx import Document as DocxDocument
    except ImportError as ie:
        docx_import_error = str(ie)
        print(f"WARN: python-docx not available ({ie}); skipping content checks (partial 0.30)")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the document for content verification
    try:
        doc = DocxDocument(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load docx {file_path}: {e}")
        # File exists but unreadable — partial credit for existence only
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Gather all paragraphs (text + style)
    paragraphs = [(para.style.name, para.text.strip()) for para in doc.paragraphs]
    all_headings = [(style, text) for style, text in paragraphs if 'Heading' in style]
    all_non_empty = [(style, text) for style, text in paragraphs if text]

    # Component 2: Document has Heading 1 = 'Basic concepts of flexbox' (0.30 points)
    # This verifies the primary article title was correctly extracted from the MDN page.
    # Initial env: no file -> FAIL
    # Golden env: H1 heading with the article title present -> PASS
    try:
        h1_found = any(
            'Heading 1' in style and text.lower().strip() == EXPECTED_H1.lower().strip()
            for style, text in all_headings
        )
        if h1_found:
            print(f"PASS: Component 2 — Heading 1 '{EXPECTED_H1}' found (0.30 pts)")
            total_score += 0.30
        else:
            # Also accept if the title appears as text anywhere (some tools may not preserve styles)
            title_in_text = any(
                EXPECTED_H1.lower() in text.lower()
                for _, text in all_non_empty
            )
            if title_in_text:
                print(f"PASS: Component 2 — Title '{EXPECTED_H1}' found in document text (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — Title '{EXPECTED_H1}' not found in document")
                print(f"  Found headings: {[text for _, text in all_headings[:5]]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Document has at least 4 key H2 sections from the MDN Flexbox article (0.20 points)
    # Verifies that the main content sections of the flexbox article are present.
    # We require at least half (4 of 8) key sections to allow for reasonable variation.
    # Initial env: no file -> FAIL
    # Golden env: all 8 key H2 sections present -> PASS
    try:
        all_heading_texts = [text.lower() for _, text in all_headings]
        all_text_lower = [text.lower() for _, text in all_non_empty]

        matched_sections = []
        for section in EXPECTED_H2_SECTIONS:
            section_lower = section.lower()
            found_in_headings = any(section_lower in ht for ht in all_heading_texts)
            found_in_text = any(section_lower in t for t in all_text_lower)
            if found_in_headings or found_in_text:
                matched_sections.append(section)

        min_required = 4  # At least 4 of the 8 key sections
        if len(matched_sections) >= min_required:
            print(f"PASS: Component 3 — {len(matched_sections)}/{len(EXPECTED_H2_SECTIONS)} key sections found (0.20 pts)")
            print(f"  Matched: {matched_sections}")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Only {len(matched_sections)}/{len(EXPECTED_H2_SECTIONS)} sections found (need >= {min_required})")
            missing = [s for s in EXPECTED_H2_SECTIONS if s not in matched_sections]
            print(f"  Missing: {missing[:3]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Document has substantial content (>= 20 non-empty paragraphs) (0.20 points)
    # Ensures the document contains the full article body, not just a stub.
    # Initial env: no file -> FAIL
    # Golden env: 90 paragraphs -> PASS
    try:
        non_empty_count = len(all_non_empty)
        min_paragraphs = 20
        if non_empty_count >= min_paragraphs:
            print(f"PASS: Component 4 — Document has {non_empty_count} non-empty paragraphs (>= {min_paragraphs}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Document has only {non_empty_count} non-empty paragraphs (need >= {min_paragraphs})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
