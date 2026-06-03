"""
Reward Script: Protected sections in a contract template
Task ID: writer_legal_048
Domain: libreoffice_writer
Scoring:
  Component 1 (0.20): Exactly 3 SDT (Structured Document Tag) elements exist
  Component 2 (0.30): All 3 SDTs have sdtContentLocked lock (write protection)
  Component 3 (0.15): An SDT contains Section 1 (Preamble) content
  Component 4 (0.15): An SDT contains Section 5 (Standard Terms) content
  Component 5 (0.20): An SDT contains Section 9 (Governing Law) content
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_048'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that three protected sections exist in the contract document.
    Sections 1 (Preamble), 5 (Standard Terms), and 9 (Governing Law)
    should be enclosed in write-protected SDT elements.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from lxml import etree
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = doc.element.body

    # Find all SDT elements at body level (protected sections)
    sdts = body.findall('.//w:sdt', ns)
    sdt_count = len(sdts)

    # Component 1: Exactly 3 SDT elements exist (0.20 points)
    try:
        if sdt_count == 3:
            print(f"PASS: Component 1 -- Found exactly 3 SDT elements (0.20 pts)")
            total_score += 0.20
        elif sdt_count > 0:
            # Partial credit if some SDTs exist but not exactly 3
            partial = 0.10 * min(sdt_count, 3) / 3
            print(f"PARTIAL: Component 1 -- Found {sdt_count} SDT elements, expected 3 ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No SDT elements found, expected 3")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Helper: extract SDT info
    sdt_info = []
    for i, sdt in enumerate(sdts):
        info = {'index': i, 'locked': False, 'alias': '', 'content_text': ''}
        try:
            pr = sdt.find('w:sdtPr', ns)
            if pr is not None:
                lock_el = pr.find('w:lock', ns)
                if lock_el is not None:
                    lock_val = lock_el.get(f'{{{ns["w"]}}}val', '')
                    info['locked'] = lock_val == 'sdtContentLocked'
                alias_el = pr.find('w:alias', ns)
                if alias_el is not None:
                    info['alias'] = alias_el.get(f'{{{ns["w"]}}}val', '')

            content_el = sdt.find('w:sdtContent', ns)
            if content_el is not None:
                paras = content_el.findall('.//w:p', ns)
                all_text = []
                for p in paras:
                    texts = p.findall('.//w:t', ns)
                    text = ''.join(t.text or '' for t in texts)
                    all_text.append(text)
                info['content_text'] = '\n'.join(all_text)
        except Exception as e:
            print(f"WARN: Could not parse SDT {i}: {e}")
        sdt_info.append(info)

    # Component 2: All SDTs have sdtContentLocked (0.30 points)
    try:
        if sdt_count > 0:
            locked_count = sum(1 for s in sdt_info if s['locked'])
            if locked_count == sdt_count and sdt_count >= 3:
                print(f"PASS: Component 2 -- All {locked_count} SDTs are write-protected (0.30 pts)")
                total_score += 0.30
            elif locked_count > 0:
                partial = 0.30 * locked_count / max(sdt_count, 3)
                print(f"PARTIAL: Component 2 -- {locked_count}/{sdt_count} SDTs locked ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- No SDTs are write-protected")
        else:
            print(f"FAIL: Component 2 -- No SDTs to check for protection")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: An SDT contains Section 1 Preamble content (0.15 points)
    try:
        found_s1 = any(
            'Section 1' in s['content_text'] and 'Preamble' in s['content_text']
            for s in sdt_info
        )
        if found_s1:
            print(f"PASS: Component 3 -- Found protected section with Section 1: Preamble (0.15 pts)")
            total_score += 0.15
        else:
            # Also check if any SDT contains the preamble text without exact heading
            found_preamble = any(
                'Professional Services Agreement' in s['content_text'] and
                'WHEREAS' in s['content_text']
                for s in sdt_info
            )
            if found_preamble:
                print(f"PARTIAL: Component 3 -- Found SDT with preamble content but no 'Section 1' heading (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 -- No SDT contains Section 1 (Preamble) content")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: An SDT contains Section 5 Standard Terms content (0.15 points)
    try:
        found_s5 = any(
            'Section 5' in s['content_text'] and 'Standard Terms' in s['content_text']
            for s in sdt_info
        )
        if found_s5:
            print(f"PASS: Component 4 -- Found protected section with Section 5: Standard Terms (0.15 pts)")
            total_score += 0.15
        else:
            # Check for section content without exact heading
            found_terms = any(
                'workmanlike manner' in s['content_text'] and
                'confidentiality' in s['content_text'].lower()
                for s in sdt_info
            )
            if found_terms:
                print(f"PARTIAL: Component 4 -- Found SDT with standard terms content but no 'Section 5' heading (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 -- No SDT contains Section 5 (Standard Terms) content")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: An SDT contains Section 9 Governing Law content (0.20 points)
    try:
        found_s9 = any(
            'Section 9' in s['content_text'] and 'Governing Law' in s['content_text']
            for s in sdt_info
        )
        if found_s9:
            print(f"PASS: Component 5 -- Found protected section with Section 9: Governing Law (0.20 pts)")
            total_score += 0.20
        else:
            # Check for section content without exact heading
            found_gov = any(
                'governed by' in s['content_text'].lower() and
                'dispute' in s['content_text'].lower()
                for s in sdt_info
            )
            if found_gov:
                print(f"PARTIAL: Component 5 -- Found SDT with governing law content but no 'Section 9' heading (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 -- No SDT contains Section 9 (Governing Law) content")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

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
