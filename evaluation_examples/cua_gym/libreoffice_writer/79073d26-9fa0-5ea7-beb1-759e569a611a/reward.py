"""
Reward Script: Configure footnote numbering to restart per chapter/section
Task ID: writer_acad_024
Domain: libreoffice_writer

Scoring rubric:
  Component 1 (0.4): At least one section has footnotePr with numRestart="eachSect"
  Component 2 (0.3): ALL body-level sectPr elements have numRestart="eachSect"
  Component 3 (0.3): ALL inline sectPr elements (section breaks within paragraphs) also have numRestart="eachSect"
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_024'
WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def persist_app_state(domain):
    """Save any unsaved edits in LibreOffice before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that footnote numbering restarts at each section (chapter).
    Checks all sectPr elements in document.xml for footnotePr/numRestart="eachSect".
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            if 'word/document.xml' not in z.namelist():
                print("CRITICAL: word/document.xml not found in archive")
                print("REWARD: 0.0")
                return 0.0
            doc_xml = z.read('word/document.xml')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    doc_root = etree.fromstring(doc_xml)

    # Collect ALL sectPr elements in the document
    # There are two types:
    #   1. Body-level: last sectPr child of w:body (the final section)
    #   2. Inline: sectPr inside w:pPr of paragraphs (section breaks between chapters)
    body = doc_root.find('{%s}body' % WNS)
    if body is None:
        print("CRITICAL: No w:body element found")
        print("REWARD: 0.0")
        return 0.0

    # Find the body-level (final) sectPr
    body_sect_pr = body.find('{%s}sectPr' % WNS)

    # Find all inline sectPr (inside paragraph properties)
    inline_sect_prs = doc_root.findall('.//{%s}pPr/{%s}sectPr' % (WNS, WNS))

    all_sect_prs = []
    if inline_sect_prs:
        all_sect_prs.extend(inline_sect_prs)
    if body_sect_pr is not None:
        all_sect_prs.append(body_sect_pr)

    print(f"INFO: Found {len(all_sect_prs)} total sectPr elements "
          f"({len(inline_sect_prs)} inline + {1 if body_sect_pr is not None else 0} body-level)")

    if len(all_sect_prs) == 0:
        print("FAIL: No section elements found in document")
        print("REWARD: 0.0")
        return 0.0

    def has_each_sect_restart(sect_pr):
        """Check if a sectPr has footnotePr/numRestart val='eachSect'."""
        fn_pr = sect_pr.find('{%s}footnotePr' % WNS)
        if fn_pr is None:
            return False
        num_restart = fn_pr.find('{%s}numRestart' % WNS)
        if num_restart is None:
            return False
        val = num_restart.get('{%s}val' % WNS)
        return val == 'eachSect'

    # Component 1: At least one section has eachSect restart (0.4 points)
    # This checks the basic requirement: footnote restart is configured somewhere
    try:
        any_has_restart = any(has_each_sect_restart(sp) for sp in all_sect_prs)
        if any_has_restart:
            print(f"PASS: Component 1 -- At least one section has numRestart='eachSect' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- No section has numRestart='eachSect'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Body-level sectPr has eachSect restart (0.3 points)
    # The final section definition must also have the setting
    try:
        if body_sect_pr is not None:
            if has_each_sect_restart(body_sect_pr):
                print(f"PASS: Component 2 -- Body-level sectPr has numRestart='eachSect' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- Body-level sectPr missing numRestart='eachSect'")
        else:
            print(f"FAIL: Component 2 -- No body-level sectPr found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: ALL inline sectPr elements have eachSect restart (0.3 points)
    # Every section break between chapters must also have the setting
    try:
        if len(inline_sect_prs) == 0:
            # No inline section breaks; this is unexpected for a 3-chapter doc but not our fault
            print(f"FAIL: Component 3 -- No inline sectPr elements found (expected section breaks between chapters)")
        else:
            all_inline_ok = all(has_each_sect_restart(sp) for sp in inline_sect_prs)
            restart_count = sum(1 for sp in inline_sect_prs if has_each_sect_restart(sp))
            if all_inline_ok:
                print(f"PASS: Component 3 -- All {len(inline_sect_prs)} inline sectPr elements have numRestart='eachSect' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- Only {restart_count}/{len(inline_sect_prs)} inline sectPr elements have numRestart='eachSect'")
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
