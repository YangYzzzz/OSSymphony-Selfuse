"""
Reward Script: Add chapter numbering to TOC entries
Task ID: writer_mt_068
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Heading 1 TOC entries have correct chapter numbers (1, 2, 3)
  Component 2 (0.4): Heading 2 TOC entries have correct sub-chapter numbers (1.1, 1.2, 2.1, etc.)
  Component 3 (0.2): All 9 TOC entries have numbering prefix (comprehensive coverage)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_068'


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def get_toc_entries(doc):
    """
    Extract TOC entry texts from the SDT (structured document tag) that
    contains the Table of Contents.
    Returns a list of (style_val, entry_text) tuples for real TOC entries.
    style_val is 'TOC1' or 'TOC2' etc.
    """
    WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    ns = {'w': WNS}
    body = doc.element.body

    sdts = body.findall('.//w:sdt', ns)
    for sdt in sdts:
        galleries = sdt.findall('.//w:docPartGallery', ns)
        is_toc = False
        for g in galleries:
            val = g.get(f'{{{WNS}}}val', '')
            if 'Table of Contents' in val:
                is_toc = True
                break
        if not is_toc:
            continue

        content = sdt.find('.//w:sdtContent', ns)
        if content is None:
            continue

        entries = []
        paras = content.findall('.//w:p', ns)
        for p in paras:
            # Get paragraph style
            pPr = p.find('w:pPr', ns)
            style_val = None
            if pPr is not None:
                pStyle = pPr.find('w:pStyle', ns)
                if pStyle is not None:
                    style_val = pStyle.get(f'{{{WNS}}}val', '')

            # Only process TOC entry paragraphs (TOC1, TOC2, etc.)
            # Skip TOCHeading which is the "Table of Contents" title
            if style_val and style_val.startswith('TOC') and style_val not in ('TOCHeading',):
                # Get the text of the first run (before tab/field codes)
                # This is the entry text with or without numbering
                runs = p.findall('w:r', ns)
                first_run_text = ''
                for r in runs:
                    t_elem = r.find('w:t', ns)
                    # Stop at tab or field char
                    tab = r.find('w:tab', ns)
                    fld = r.find('w:fldChar', ns)
                    if tab is not None or fld is not None:
                        break
                    if t_elem is not None and t_elem.text:
                        first_run_text += t_elem.text

                entries.append((style_val, first_run_text.strip()))
        return entries
    return []


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    from docx import Document

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract TOC entries
    try:
        entries = get_toc_entries(doc)
    except Exception as e:
        print(f"CRITICAL: Cannot parse TOC: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not entries:
        print("FAIL: No TOC entries found")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(entries)} TOC entries")
    for style, text in entries:
        print(f"  {style}: {repr(text)}")

    # Expected TOC entries with numbering:
    # TOC1: "1 Introduction", "2 Procedures", "3 Safety Guidelines"
    # TOC2: "1.1 Scope", "1.2 Purpose", "2.1 Standard Operating Procedures",
    #       "2.2 Emergency Protocols", "3.1 Workplace Safety", "3.2 Equipment Handling"

    expected_h1 = {
        '1 Introduction': 'Introduction',
        '2 Procedures': 'Procedures',
        '3 Safety Guidelines': 'Safety Guidelines',
    }

    expected_h2 = {
        '1.1 Scope': 'Scope',
        '1.2 Purpose': 'Purpose',
        '2.1 Standard Operating Procedures': 'Standard Operating Procedures',
        '2.2 Emergency Protocols': 'Emergency Protocols',
        '3.1 Workplace Safety': 'Workplace Safety',
        '3.2 Equipment Handling': 'Equipment Handling',
    }

    # Component 1: Heading 1 TOC entries have correct chapter numbers (0.4 points)
    try:
        toc1_entries = [(s, t) for s, t in entries if s == 'TOC1']
        h1_matches = 0
        h1_total = len(expected_h1)

        for expected_text, base_name in expected_h1.items():
            found = False
            for style, text in toc1_entries:
                if text == expected_text:
                    found = True
                    break
            if found:
                h1_matches += 1
                print(f"  PASS: Found TOC1 entry '{expected_text}'")
            else:
                print(f"  FAIL: Missing TOC1 entry '{expected_text}' (entries: {[t for _, t in toc1_entries]})")

        if h1_matches == h1_total and h1_total > 0:
            print(f"PASS: Component 1 -- All {h1_total} Heading 1 TOC entries have correct numbering (0.4 pts)")
            total_score += 0.4
        elif h1_matches > 0:
            partial = round(0.4 * h1_matches / h1_total, 2)
            print(f"PARTIAL: Component 1 -- {h1_matches}/{h1_total} Heading 1 entries correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No Heading 1 TOC entries have chapter numbering")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Heading 2 TOC entries have correct sub-chapter numbers (0.4 points)
    try:
        toc2_entries = [(s, t) for s, t in entries if s == 'TOC2']
        h2_matches = 0
        h2_total = len(expected_h2)

        for expected_text, base_name in expected_h2.items():
            found = False
            for style, text in toc2_entries:
                if text == expected_text:
                    found = True
                    break
            if found:
                h2_matches += 1
                print(f"  PASS: Found TOC2 entry '{expected_text}'")
            else:
                print(f"  FAIL: Missing TOC2 entry '{expected_text}' (entries: {[t for _, t in toc2_entries]})")

        if h2_matches == h2_total and h2_total > 0:
            print(f"PASS: Component 2 -- All {h2_total} Heading 2 TOC entries have correct numbering (0.4 pts)")
            total_score += 0.4
        elif h2_matches > 0:
            partial = round(0.4 * h2_matches / h2_total, 2)
            print(f"PARTIAL: Component 2 -- {h2_matches}/{h2_total} Heading 2 entries correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No Heading 2 TOC entries have sub-chapter numbering")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All 9 TOC entries have a numbering prefix (0.2 points)
    # This checks that EVERY entry starts with a digit pattern like "1 " or "1.1 "
    try:
        numbered_count = 0
        total_entries = len(entries)
        number_pattern = re.compile(r'^\d+(\.\d+)?\s+\S')

        for style, text in entries:
            if number_pattern.match(text):
                numbered_count += 1

        if numbered_count == total_entries and total_entries >= 9:
            print(f"PASS: Component 3 -- All {total_entries} TOC entries have numbering prefix (0.2 pts)")
            total_score += 0.2
        elif numbered_count > 0:
            # Only give partial if at least half are numbered
            if numbered_count >= total_entries / 2:
                partial = round(0.2 * numbered_count / total_entries, 2)
                print(f"PARTIAL: Component 3 -- {numbered_count}/{total_entries} entries have numbering ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- Only {numbered_count}/{total_entries} entries have numbering")
        else:
            print(f"FAIL: Component 3 -- No TOC entries have numbering prefix")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
