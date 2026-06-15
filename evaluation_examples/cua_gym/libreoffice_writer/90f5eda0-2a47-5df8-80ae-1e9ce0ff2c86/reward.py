"""
Reward Script: Change footnote numbering to restart at 1 for each chapter/section
Task ID: writer_bs_030
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): At least one section has footnote numRestart=eachSect
  Component 2 (0.5): ALL sections have footnote numRestart=eachSect and document integrity preserved
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_030'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NSMAP = {'w': W_NS}


def persist_app_state(domain):
    """Save any unsaved edits in LibreOffice Writer."""
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
    Verify that footnote numbering restarts per section (chapter).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid docx (zip)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open docx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc_xml = zf.read('word/document.xml')
        doc_root = etree.fromstring(doc_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse document.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gather all sections
    sections = doc_root.findall('.//w:sectPr', NSMAP)
    num_sections = len(sections)
    print(f"INFO: Found {num_sections} sections in document")

    if num_sections == 0:
        print("CRITICAL: No sections found in document")
        print("REWARD: 0.0")
        return 0.0

    # Check section-level footnote restart settings
    sections_with_restart = 0
    for i, sect in enumerate(sections):
        fn_pr = sect.find('w:footnotePr', NSMAP)
        if fn_pr is not None:
            num_restart = fn_pr.find('w:numRestart', NSMAP)
            if num_restart is not None:
                val = num_restart.get(f'{{{W_NS}}}val', '')
                if val == 'eachSect':
                    sections_with_restart += 1
                    print(f"  Section {i}: numRestart=eachSect (GOOD)")
                else:
                    print(f"  Section {i}: numRestart={val} (unexpected)")
            else:
                print(f"  Section {i}: footnotePr exists but no numRestart")
        else:
            print(f"  Section {i}: no footnotePr")

    # Also check global settings.xml for document-wide footnote restart
    global_restart = False
    try:
        if 'word/settings.xml' in zf.namelist():
            settings_xml = zf.read('word/settings.xml')
            settings_root = etree.fromstring(settings_xml)
            fn_pr_global = settings_root.find('.//w:footnotePr', NSMAP)
            if fn_pr_global is not None:
                num_restart_global = fn_pr_global.find('w:numRestart', NSMAP)
                if num_restart_global is not None:
                    val = num_restart_global.get(f'{{{W_NS}}}val', '')
                    if val == 'eachSect':
                        global_restart = True
                        print(f"  Global settings.xml: numRestart=eachSect (GOOD)")
    except Exception as e:
        print(f"  WARN: Could not check settings.xml: {e}")

    zf.close()

    # Component 1: At least one section has restart per section OR global setting (0.5 points)
    # This verifies the core change was made at all
    try:
        if sections_with_restart > 0 or global_restart:
            print(f"\nPASS: Component 1 - Footnote restart per section is configured "
                  f"({sections_with_restart} sections + global={global_restart}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"\nFAIL: Component 1 - No section has numRestart=eachSect and "
                  f"no global restart setting found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: ALL sections have restart AND document integrity (0.5 points)
    # Checks completeness: every section must have the setting, and document structure is preserved
    try:
        all_sections_configured = (sections_with_restart == num_sections) or global_restart
        # Verify document integrity: still has expected 5 sections and 15 footnotes
        integrity_ok = True
        if num_sections != 5:
            print(f"  WARN: Expected 5 sections, found {num_sections}")
            integrity_ok = False

        # Count real footnotes
        try:
            zf2 = zipfile.ZipFile(file_path, 'r')
            fn_xml = zf2.read('word/footnotes.xml')
            fn_root = etree.fromstring(fn_xml)
            footnotes = fn_root.findall('w:footnote', NSMAP)
            real_fns = [fn for fn in footnotes
                        if fn.get(f'{{{W_NS}}}type') is None]
            num_footnotes = len(real_fns)
            zf2.close()
            print(f"  INFO: Found {num_footnotes} footnotes")
            if num_footnotes != 15:
                print(f"  WARN: Expected 15 footnotes, found {num_footnotes}")
                integrity_ok = False
        except Exception as e:
            print(f"  WARN: Could not count footnotes: {e}")
            integrity_ok = False

        if all_sections_configured and integrity_ok:
            print(f"PASS: Component 2 - All {num_sections} sections configured "
                  f"with restart AND document integrity preserved (0.5 pts)")
            total_score += 0.5
        elif all_sections_configured and not integrity_ok:
            print(f"PARTIAL: Component 2 - All sections configured but integrity issues (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - Only {sections_with_restart}/{num_sections} sections "
                  f"configured (global={global_restart})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

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
