"""
Reward Script: Compare Contract_v1 and Contract_v2, accept formatting changes,
reject the 30->15 day termination notice change, save as Contract_Final.docx.
Task ID: writer_pd_040
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.30): Rejected change — para 29 retains "thirty (30) days"
  - Component 2 (0.30): Accepted content changes (3 of 4 content changes accepted)
  - Component 3 (0.25): Accepted formatting changes (italic/bold applied)
  - Component 4 (0.15): No tracked changes remaining
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_pd_040'


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice documents."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            import time
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


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

    paras = doc.paragraphs

    # Precondition: document has expected structure (~53 paragraphs)
    if len(paras) < 40:
        print(f"CRITICAL: Document has only {len(paras)} paragraphs, expected ~53")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Rejected change — paragraph 29 retains "thirty (30) days" (0.30 points)
    # In v2, this was changed to "fifteen (15) days". The task requires rejecting this change.
    # This check FAILS on initial_env because Contract_Final.docx does not exist there.
    try:
        para29_text = paras[29].text
        has_thirty = "thirty (30) days" in para29_text
        has_fifteen = "fifteen (15) days" in para29_text
        if has_thirty and not has_fifteen:
            print(f"PASS: Component 1 — Para 29 retains 'thirty (30) days' (rejected change) (0.30 pts)")
            total_score += 0.30
        elif has_fifteen:
            print(f"FAIL: Component 1 — Para 29 has 'fifteen (15) days' (change was NOT rejected)")
        else:
            print(f"FAIL: Component 1 — Para 29 does not contain expected termination text: {para29_text[:100]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Accepted content changes (0.30 points)
    # 3 content changes should be accepted from v2:
    #   - Para 8: "five (5)" -> "six (6)" qualified professionals
    #   - Para 12: rates updated to $195/$210
    #   - Para 30: "fifteen (15)" -> "ten (10)" business days for delivery
    # Each sub-check is worth 0.10 points.
    try:
        accepted_content_score = 0.0

        # Sub-check 2a: Para 8 should have "six (6)"
        para8_text = paras[8].text
        if "six (6)" in para8_text and "five (5)" not in para8_text:
            print(f"PASS: Component 2a — Para 8 has 'six (6)' (accepted change) (0.10 pts)")
            accepted_content_score += 0.10
        else:
            print(f"FAIL: Component 2a — Para 8 expected 'six (6)', found: {para8_text[:100]}")

        # Sub-check 2b: Para 12 should have updated rates $195/$210
        para12_text = paras[12].text
        if "$195" in para12_text and "$210" in para12_text:
            print(f"PASS: Component 2b — Para 12 has updated rates $195/$210 (accepted change) (0.10 pts)")
            accepted_content_score += 0.10
        else:
            print(f"FAIL: Component 2b — Para 12 expected '$195' and '$210', found: {para12_text[:100]}")

        # Sub-check 2c: Para 30 should have "ten (10) business days"
        para30_text = paras[30].text
        if "ten (10) business days" in para30_text:
            print(f"PASS: Component 2c — Para 30 has 'ten (10) business days' (accepted change) (0.10 pts)")
            accepted_content_score += 0.10
        else:
            print(f"FAIL: Component 2c — Para 30 expected 'ten (10) business days', found: {para30_text[:100]}")

        total_score += accepted_content_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Accepted formatting changes (0.25 points)
    # v2 introduced formatting changes that should be accepted:
    #   - Para 4: company names "Meridian Technologies Inc." and "Cascade Financial Group LLC" are italic
    #   - Para 9: "SOC 2 Type II" is bold (run split)
    #   - Para 17: "sixty (60) days" is bold (run split)
    #   - Para 22: "three (3) years" is italic (run split)
    #   - Para 25: "Work Product" is bold (run split)
    # Each sub-check is worth 0.05 points.
    try:
        fmt_score = 0.0

        # Sub-check 3a: Para 4 — italic company names
        para4_runs = paras[4].runs
        italic_found = 0
        for r in para4_runs:
            if "Meridian Technologies" in r.text and r.font.italic:
                italic_found += 1
            if "Cascade Financial" in r.text and r.font.italic:
                italic_found += 1
        if italic_found >= 2:
            print(f"PASS: Component 3a — Company names are italic (0.05 pts)")
            fmt_score += 0.05
        else:
            print(f"FAIL: Component 3a — Expected italic on company names, found {italic_found}/2")

        # Sub-check 3b: Para 9 — "SOC 2 Type II" is bold
        soc_bold = False
        for r in paras[9].runs:
            if "SOC 2 Type II" in r.text and r.font.bold:
                soc_bold = True
                break
        if soc_bold:
            print(f"PASS: Component 3b — 'SOC 2 Type II' is bold (0.05 pts)")
            fmt_score += 0.05
        else:
            print(f"FAIL: Component 3b — 'SOC 2 Type II' not found as bold in para 9")

        # Sub-check 3c: Para 17 — "sixty (60) days" is bold
        sixty_bold = False
        for r in paras[17].runs:
            if "sixty (60) days" in r.text and r.font.bold:
                sixty_bold = True
                break
        if sixty_bold:
            print(f"PASS: Component 3c — 'sixty (60) days' is bold (0.05 pts)")
            fmt_score += 0.05
        else:
            print(f"FAIL: Component 3c — 'sixty (60) days' not found as bold in para 17")

        # Sub-check 3d: Para 22 — "three (3) years" is italic
        three_italic = False
        for r in paras[22].runs:
            if "three (3) years" in r.text and r.font.italic:
                three_italic = True
                break
        if three_italic:
            print(f"PASS: Component 3d — 'three (3) years' is italic (0.05 pts)")
            fmt_score += 0.05
        else:
            print(f"FAIL: Component 3d — 'three (3) years' not found as italic in para 22")

        # Sub-check 3e: Para 25 — "Work Product" is bold
        wp_bold = False
        for r in paras[25].runs:
            if "Work Product" in r.text and r.font.bold:
                wp_bold = True
                break
        if wp_bold:
            print(f"PASS: Component 3e — 'Work Product' is bold (0.05 pts)")
            fmt_score += 0.05
        else:
            print(f"FAIL: Component 3e — 'Work Product' not found as bold in para 25")

        total_score += fmt_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: No tracked changes remaining (0.15 points)
    # All changes should be resolved — no insertions or deletions in XML.
    try:
        from lxml import etree
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        body = doc.element.body
        inserts = body.findall('.//w:ins', ns)
        deletes = body.findall('.//w:del', ns)
        total_tracked = len(inserts) + len(deletes)
        if total_tracked == 0:
            print(f"PASS: Component 4 — No tracked changes remaining (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Found {len(inserts)} insertions and {len(deletes)} deletions still tracked")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook — save any open LibreOffice documents before verification
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Contract_Final.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
