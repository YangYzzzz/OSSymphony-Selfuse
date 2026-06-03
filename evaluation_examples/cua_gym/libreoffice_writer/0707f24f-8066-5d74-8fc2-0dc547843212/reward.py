"""
Reward Script: Verify widow/orphan control and keep-lines settings
Task ID: writer_fs_048
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Normal style has widowControl enabled (val="1")
  Component 2 (0.5): Quotations style has keepLines enabled (do not split paragraph)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_048'


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


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Enable widow control of 2 lines and orphan control of 2 lines
    for the Default Paragraph Style, and additionally set 'Do not split
    paragraph' for the 'Quotations' style.

    In OOXML, widowControl is a boolean on the Normal (Default Paragraph)
    style. When enabled (val="1" or attribute absent on a style where
    default is true), it enforces the standard 2-line widow/orphan control.
    'Do not split paragraph' maps to the <w:keepLines/> element in pPr.
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not installed")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    w_ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    styles_el = doc.styles.element

    # Helper: find a style element by styleId
    def find_style(style_id):
        for s in styles_el.findall('.//w:style', ns):
            sid = s.attrib.get(f'{w_ns}styleId', '')
            if sid == style_id:
                return s
        return None

    # Component 1: Normal (Default Paragraph) style has widowControl enabled (0.5 points)
    # Initial state: widowControl val="0" (disabled)
    # Golden state: widowControl val="1" (enabled)
    try:
        normal_style = find_style('Normal')
        if normal_style is None:
            print("FAIL: Component 1 — 'Normal' style not found in document")
        else:
            pPr = normal_style.find('w:pPr', ns)
            if pPr is None:
                print("FAIL: Component 1 — Normal style has no pPr element")
            else:
                wc_el = pPr.find('w:widowControl', ns)
                if wc_el is None:
                    # widowControl absent in Normal style means it inherits default
                    # In OOXML the default for widowControl is true, so absent = enabled
                    print("PASS: Component 1 — widowControl absent (inherits default=true) (0.5 pts)")
                    total_score += 0.5
                else:
                    wc_val = wc_el.attrib.get(f'{w_ns}val', '')
                    # val="1" or val="true" means enabled; val="0" or val="false" means disabled
                    if wc_val in ('1', 'true', ''):
                        print(f"PASS: Component 1 — widowControl val='{wc_val}' (enabled) (0.5 pts)")
                        total_score += 0.5
                    else:
                        print(f"FAIL: Component 1 — widowControl val='{wc_val}' (disabled, expected enabled)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Quotations style has keepLines enabled (0.5 points)
    # Initial state: no keepLines element
    # Golden state: <w:keepLines/> present in pPr
    try:
        quotations_style = find_style('Quotations')
        if quotations_style is None:
            print("FAIL: Component 2 — 'Quotations' style not found in document")
        else:
            pPr = quotations_style.find('w:pPr', ns)
            if pPr is None:
                print("FAIL: Component 2 — Quotations style has no pPr element")
            else:
                kl_el = pPr.find('w:keepLines', ns)
                if kl_el is not None:
                    # Check val attribute: absent means true, val="1"/val="true" means true
                    kl_val = kl_el.attrib.get(f'{w_ns}val', '')
                    if kl_val in ('', '1', 'true'):
                        print(f"PASS: Component 2 — Quotations keepLines enabled (val='{kl_val}') (0.5 pts)")
                        total_score += 0.5
                    else:
                        print(f"FAIL: Component 2 — Quotations keepLines val='{kl_val}' (disabled)")
                else:
                    print("FAIL: Component 2 — Quotations style missing keepLines element")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

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
