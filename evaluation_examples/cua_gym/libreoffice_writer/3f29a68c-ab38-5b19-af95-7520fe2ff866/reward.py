"""
Reward Script: Literature review section in LibreOffice Writer
Task ID: writer_wf_079
Domain: libreoffice_writer
Scoring:
  Component 1: Title heading 'Chapter 2: Literature Review' as Heading 1 (0.15)
  Component 2: Four Heading 2 subsections with correct names (0.20)
  Component 3: Body text with in-text citations (Author, Year) (0.25)
  Component 4: 6 footnotes in the document (0.20)
  Component 5: References section with 8 APA entries (0.20)
"""

import os
import re
import lxml.etree as ET

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_wf_079'

EXPECTED_SUBSECTIONS = [
    'Theoretical Framework',
    'Previous Studies on Online Learning',
    'Technology Acceptance Models',
    'Research Gaps',
]


def count_footnotes(doc):
    """Count real footnotes (excluding separator/continuationSeparator) via XML."""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for rel in doc.part.rels.values():
        if 'footnote' in rel.reltype.lower():
            fn_xml = rel.target_part.blob
            root = ET.fromstring(fn_xml)
            footnotes = root.findall('.//w:footnote', ns)
            count = 0
            for fn in footnotes:
                fn_type = fn.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type', 'normal')
                if fn_type == 'normal':
                    count += 1
            return count
    return 0


def count_footnote_refs_in_body(doc):
    """Count footnoteReference elements in the document body."""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    refs = doc.element.body.findall('.//w:footnoteReference', ns)
    return len(refs)


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

    # Collect structure info
    headings_h1 = []
    headings_h2 = []
    all_paras = []
    for p in doc.paragraphs:
        style_name = p.style.name if p.style else ''
        all_paras.append((style_name, p.text.strip()))
        if style_name == 'Heading 1':
            headings_h1.append(p.text.strip())
        elif style_name == 'Heading 2':
            headings_h2.append(p.text.strip())

    # Component 1: Title heading 'Chapter 2: Literature Review' as Heading 1 (0.15 points)
    try:
        title_found = any(
            'chapter 2' in h.lower() and 'literature review' in h.lower()
            for h in headings_h1
        )
        if title_found:
            print(f"PASS: Component 1 - Title 'Chapter 2: Literature Review' found as Heading 1 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - Expected Heading 1 with 'Chapter 2: Literature Review', found H1s: {headings_h1}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Four Heading 2 subsections with correct names (0.20 points)
    # Award partial: 0.05 per matching subsection
    try:
        matched_subsections = 0
        for expected in EXPECTED_SUBSECTIONS:
            if any(expected.lower() in h.lower() for h in headings_h2):
                matched_subsections += 1
            else:
                print(f"  MISS: Subsection '{expected}' not found in Heading 2 list")

        sub_score = 0.05 * matched_subsections
        if matched_subsections == 4:
            print(f"PASS: Component 2 - All 4 subsections found as Heading 2 (0.20 pts)")
        elif matched_subsections > 0:
            print(f"PARTIAL: Component 2 - {matched_subsections}/4 subsections found ({sub_score:.2f} pts)")
        else:
            print(f"FAIL: Component 2 - No expected subsections found. H2s: {headings_h2}")
        total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Body text with in-text citations (Author, Year) format (0.25 points)
    # Check that subsections have body paragraphs containing (Author, Year) citations
    try:
        # Find body paragraphs between H2 headings (before References section)
        citation_pattern = re.compile(r'\([A-Z][a-z]+(?:\s+(?:et al\.|&\s+[A-Z][a-z]+))?,\s*\d{4}\)')
        ref_heading_idx = None
        for i, (style, text) in enumerate(all_paras):
            if style == 'Heading 1' and 'reference' in text.lower():
                ref_heading_idx = i
                break

        body_paras_with_citations = 0
        total_body_paras = 0
        for i, (style, text) in enumerate(all_paras):
            if ref_heading_idx is not None and i >= ref_heading_idx:
                break
            if style == 'Normal' and text:
                total_body_paras += 1
                if citation_pattern.search(text):
                    body_paras_with_citations += 1

        # Need body paragraphs AND citations
        has_body = total_body_paras >= 4  # at least 1 per subsection
        has_citations = body_paras_with_citations >= 3  # at least a few paragraphs with citations

        comp3_score = 0.0
        if has_body and has_citations:
            comp3_score = 0.25
            print(f"PASS: Component 3 - {total_body_paras} body paragraphs, {body_paras_with_citations} with citations (0.25 pts)")
        elif has_body:
            comp3_score = 0.10
            print(f"PARTIAL: Component 3 - {total_body_paras} body paragraphs but only {body_paras_with_citations} with citations (0.10 pts)")
        elif has_citations:
            comp3_score = 0.10
            print(f"PARTIAL: Component 3 - Found citations but only {total_body_paras} body paragraphs (0.10 pts)")
        else:
            print(f"FAIL: Component 3 - {total_body_paras} body paragraphs, {body_paras_with_citations} with citations")
        total_score += comp3_score
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: 6 footnotes in the document (0.20 points)
    try:
        fn_count = count_footnotes(doc)
        fn_ref_count = count_footnote_refs_in_body(doc)
        # Use the higher of the two counts (both should agree)
        actual_fn = max(fn_count, fn_ref_count)

        if actual_fn >= 6:
            print(f"PASS: Component 4 - Found {actual_fn} footnotes (need >= 6) (0.20 pts)")
            total_score += 0.20
        elif actual_fn >= 3:
            partial = 0.10
            print(f"PARTIAL: Component 4 - Found {actual_fn} footnotes (need >= 6) (0.10 pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 - Found {actual_fn} footnotes (need >= 6)")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: References section with 8 APA entries (0.20 points)
    try:
        # Find paragraphs after the 'References' heading
        ref_section_started = False
        ref_entries = []
        for style, text in all_paras:
            if style == 'Heading 1' and 'reference' in text.lower():
                ref_section_started = True
                continue
            if ref_section_started and text:
                ref_entries.append(text)

        # Check APA-like format: Author(s) (Year). Title...
        apa_pattern = re.compile(r'.*\(\d{4}\)\.')
        apa_count = sum(1 for entry in ref_entries if apa_pattern.search(entry))

        has_ref_heading = any(
            style == 'Heading 1' and 'reference' in text.lower()
            for style, text in all_paras
        )

        comp5_score = 0.0
        if has_ref_heading and apa_count >= 8:
            comp5_score = 0.20
            print(f"PASS: Component 5 - References heading found + {apa_count} APA entries (0.20 pts)")
        elif has_ref_heading and apa_count >= 4:
            comp5_score = 0.10
            print(f"PARTIAL: Component 5 - References heading found but only {apa_count} APA entries (need >= 8) (0.10 pts)")
        elif has_ref_heading:
            comp5_score = 0.05
            print(f"PARTIAL: Component 5 - References heading found but only {apa_count} APA entries (0.05 pts)")
        else:
            print(f"FAIL: Component 5 - No References heading found")
        total_score += comp5_score
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state before verification
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
