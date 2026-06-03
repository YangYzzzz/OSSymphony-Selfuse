"""
Reward Script: Change footnote numbering to lowercase Roman numerals with per-page restart
Task ID: writer_bs_010
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5 pts): Footnote numFmt is 'lowerRoman' (both body-level and section-level)
  Component 2 (0.5 pts): Footnote numRestart is 'eachPage' (both body-level and section-level)
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_010'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W_NS}


def persist_app_state(domain: str):
    """Save any unsaved changes in LibreOffice before verification."""
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


def get_footnote_props(file_path):
    """Extract footnote properties from both body-level and section-level footnotePr elements.

    Returns a dict with collected numFmt and numRestart values from all footnotePr locations.
    We check both the body-level (direct child of <w:body>) and section-level (inside <w:sectPr>).
    """
    result = {
        'body_numFmt': None,
        'body_numRestart': None,
        'sect_numFmt': None,
        'sect_numRestart': None,
    }

    zf = zipfile.ZipFile(file_path)
    doc_xml = zf.read('word/document.xml')
    doc_root = etree.fromstring(doc_xml)

    # Body-level footnotePr: direct child of w:body
    body = doc_root.find('.//w:body', NS)
    if body is not None:
        for child in body:
            tag = etree.QName(child).localname
            if tag == 'footnotePr':
                fmt_el = child.find('w:numFmt', NS)
                restart_el = child.find('w:numRestart', NS)
                if fmt_el is not None:
                    result['body_numFmt'] = fmt_el.get(f'{{{W_NS}}}val')
                if restart_el is not None:
                    result['body_numRestart'] = restart_el.get(f'{{{W_NS}}}val')

    # Section-level footnotePr: inside w:sectPr
    for sect_pr in doc_root.findall('.//w:sectPr', NS):
        fn_pr = sect_pr.find('w:footnotePr', NS)
        if fn_pr is not None:
            fmt_el = fn_pr.find('w:numFmt', NS)
            restart_el = fn_pr.find('w:numRestart', NS)
            if fmt_el is not None:
                result['sect_numFmt'] = fmt_el.get(f'{{{W_NS}}}val')
            if restart_el is not None:
                result['sect_numRestart'] = restart_el.get(f'{{{W_NS}}}val')

    # Also check settings.xml for document-wide footnote properties
    if 'word/settings.xml' in zf.namelist():
        settings_xml = zf.read('word/settings.xml')
        settings_root = etree.fromstring(settings_xml)
        fn_pr = settings_root.find('.//w:footnotePr', NS)
        if fn_pr is not None:
            fmt_el = fn_pr.find('w:numFmt', NS)
            restart_el = fn_pr.find('w:numRestart', NS)
            if fmt_el is not None and result['body_numFmt'] is None:
                result['body_numFmt'] = fmt_el.get(f'{{{W_NS}}}val')
            if restart_el is not None and result['body_numRestart'] is None:
                result['body_numRestart'] = restart_el.get(f'{{{W_NS}}}val')

    zf.close()
    return result


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        props = get_footnote_props(file_path)
        print(f"INFO: Extracted footnote properties: {props}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Footnote numbering format is 'lowerRoman' (0.5 points)
    # The task requires changing from decimal (1,2,3) to lowercase Roman (i,ii,iii).
    # We check that at least one location (body or section) specifies lowerRoman,
    # and no location overrides it back to decimal.
    try:
        body_fmt = props['body_numFmt']
        sect_fmt = props['sect_numFmt']

        # Effective format: section-level overrides body-level if present.
        # Both should be lowerRoman, or at minimum the effective value must be lowerRoman.
        all_fmts = [f for f in [body_fmt, sect_fmt] if f is not None]

        if all_fmts and all(f == 'lowerRoman' for f in all_fmts):
            print(f"PASS: Component 1 -- numFmt is 'lowerRoman' (body={body_fmt}, sect={sect_fmt}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- expected numFmt='lowerRoman', found body={body_fmt}, sect={sect_fmt}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Footnote restart is 'eachPage' (0.5 points)
    # The task requires counting to restart on each page (instead of continuous).
    try:
        body_restart = props['body_numRestart']
        sect_restart = props['sect_numRestart']

        all_restarts = [r for r in [body_restart, sect_restart] if r is not None]

        if all_restarts and all(r == 'eachPage' for r in all_restarts):
            print(f"PASS: Component 2 -- numRestart is 'eachPage' (body={body_restart}, sect={sect_restart}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 -- expected numRestart='eachPage', found body={body_restart}, sect={sect_restart}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state before verification
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
