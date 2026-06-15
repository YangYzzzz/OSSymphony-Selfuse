"""
Reward Script: Accept tracked changes in sections 1 & 2, reject in section 3
Task ID: writer_biz_061
Domain: libreoffice_writer
Scoring:
  Component 1 (0.15): No tracked changes remain in the document
  Component 2 (0.25): Section 1 edits accepted (text with insertions kept, deletions gone)
  Component 3 (0.30): Section 2 edits accepted (text with insertions kept, deletions gone)
  Component 4 (0.30): Section 3 edits rejected (insertions removed, deleted text restored)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_061'

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


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


def get_full_para_text(para_element):
    """
    Extract full paragraph text including all tracked change text.
    This returns text as it would appear with ALL changes accepted:
    - Regular runs: included
    - Inserted text (w:ins > w:r > w:t): included
    - Deleted text (w:del > w:r > w:delText): excluded
    """
    text_parts = []
    for child in para_element.iter():
        if child.tag == f'{{{NS["w"]}}}delText':
            # Skip deleted text (we want "accepted" view)
            continue
        if child.tag == f'{{{NS["w"]}}}t' and child.text:
            text_parts.append(child.text)
    return ''.join(text_parts)


def get_rejected_para_text(para_element):
    """
    Extract paragraph text as it would appear with ALL changes rejected:
    - Regular runs: included
    - Inserted text (w:ins > w:r > w:t): excluded
    - Deleted text (w:del > w:r > w:delText): included
    """
    text_parts = []
    # Walk through direct children of paragraph in order
    for child in para_element:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag == 'ins':
            # Skip inserted content entirely (rejection removes insertions)
            continue
        elif tag == 'del':
            # Include deleted text (rejection restores deletions)
            for dt in child.iter(f'{{{NS["w"]}}}delText'):
                if dt.text:
                    text_parts.append(dt.text)
        elif tag == 'r':
            # Regular run - include its text
            for t in child.findall(f'{{{NS["w"]}}}t'):
                if t.text:
                    text_parts.append(t.text)
        # Skip other elements like pPr, bookmarkStart, etc.
    return ''.join(text_parts)


def has_tracked_changes(para_element):
    """Check if a paragraph contains any tracked changes."""
    ins = para_element.findall('.//w:ins', NS)
    dels = para_element.findall('.//w:del', NS)
    return len(ins) + len(dels) > 0


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body

    # ---------------------------------------------------------------
    # Component 1: No tracked changes remain (0.15 points)
    # In the golden doc, all changes should be resolved.
    # In the initial doc, there are 15 tracked changes.
    # ---------------------------------------------------------------
    try:
        insertions = body.findall('.//w:ins', NS)
        deletions = body.findall('.//w:del', NS)
        total_tracked = len(insertions) + len(deletions)
        if total_tracked == 0:
            print(f"PASS: Component 1 — No tracked changes remain (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Found {total_tracked} tracked changes ({len(insertions)} ins, {len(deletions)} del)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Get paragraph elements for XML-level inspection
    paras = doc.paragraphs

    # ---------------------------------------------------------------
    # Component 2: Section 1 edits accepted (0.25 points)
    # After accepting Elena's changes in Section 1:
    #   - Para 10 should contain "comprehensive" and "detailed" and NOT "preliminary"
    #   - Para 12 should contain "digital transformation roadmap development"
    #   - Para 14 should NOT contain "three printed copies"
    # We use para.text for golden (clean doc) and full_text for initial (has markup).
    # Key: these checks must FAIL on initial and PASS on golden.
    # In initial, para.text excludes both ins and del text.
    # In golden, para.text is the final accepted text.
    # So we check para.text directly -- "comprehensive" will be absent in initial
    # (it's inside w:ins) but present in golden (change accepted, now regular text).
    # HOWEVER: "three printed copies" is inside w:del in initial, so para.text
    # already excludes it -- that check would pass on BOTH.
    # FIX: For deletion checks, we also verify no tracked changes exist in the para.
    # ---------------------------------------------------------------
    try:
        s1_checks_passed = 0
        s1_checks_total = 4

        # Check para 10: "comprehensive" present (was inserted by Elena, should be accepted)
        p10_text = paras[10].text
        if 'comprehensive' in p10_text:
            s1_checks_passed += 1
            print(f"  PASS: Section 1 — 'comprehensive' present in 1.1(a)")
        else:
            print(f"  FAIL: Section 1 — 'comprehensive' not in 1.1(a) text")

        # Check para 10: "detailed" present (was inserted by Elena, should be accepted)
        if 'detailed' in p10_text:
            s1_checks_passed += 1
            print(f"  PASS: Section 1 — 'detailed' present in 1.1(a)")
        else:
            print(f"  FAIL: Section 1 — 'detailed' not in 1.1(a) text")

        # Check para 12: "digital transformation roadmap development" present
        p12_text = paras[12].text
        if 'digital transformation roadmap development' in p12_text:
            s1_checks_passed += 1
            print(f"  PASS: Section 1 — 'digital transformation roadmap development' in 1.1(b)")
        else:
            print(f"  FAIL: Section 1 — 'digital transformation roadmap development' not in 1.1(b)")

        # Check para 14: "three printed copies" absent AND no tracked changes in para
        # In initial: "three printed copies" is in w:del, para.text excludes it,
        # but tracked change markup still exists. We require BOTH: text absent AND no markup.
        p14_text = paras[14].text
        p14_has_tc = has_tracked_changes(paras[14]._element)
        if 'three printed copies' not in p14_text and not p14_has_tc:
            s1_checks_passed += 1
            print(f"  PASS: Section 1 — 'three printed copies' removed and no tracked changes in 1.1(c)")
        else:
            if p14_has_tc:
                print(f"  FAIL: Section 1 — 1.1(c) still has tracked change markup")
            else:
                print(f"  FAIL: Section 1 — 'three printed copies' still in 1.1(c)")

        s1_score = 0.25 * (s1_checks_passed / s1_checks_total)
        if s1_checks_passed == s1_checks_total:
            print(f"PASS: Component 2 — All Section 1 edits accepted ({s1_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 2 — {s1_checks_passed}/{s1_checks_total} Section 1 checks ({s1_score:.2f} pts)")
        total_score += s1_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: Section 2 edits accepted (0.30 points)
    # After accepting Elena's changes in Section 2:
    #   - Para 22: "$195 per hour" present (was inserted, replaces "$175 per hour")
    #   - Para 24: "forty-five (45)" present (was inserted, replaces "thirty (30)")
    #   - Para 26: "subject to pre-approval for amounts exceeding $500" present
    # In initial, para.text excludes inserted text, so "$195" won't be there.
    # ---------------------------------------------------------------
    try:
        s2_checks_passed = 0
        s2_checks_total = 3

        # Check para 22: "$195 per hour" present in final text
        p22_text = paras[22].text
        if '$195 per hour' in p22_text:
            s2_checks_passed += 1
            print(f"  PASS: Section 2 — '$195 per hour' present in 2.1(a)")
        else:
            print(f"  FAIL: Section 2 — '$195 per hour' not in 2.1(a): '{p22_text[:80]}'")

        # Check para 24: "forty-five (45)" present
        p24_text = paras[24].text
        if 'forty-five (45)' in p24_text:
            s2_checks_passed += 1
            print(f"  PASS: Section 2 — 'forty-five (45)' present in 2.1(b)")
        else:
            print(f"  FAIL: Section 2 — 'forty-five (45)' not in 2.1(b): '{p24_text[:80]}'")

        # Check para 26: "subject to pre-approval" present in final text
        p26_text = paras[26].text
        if 'subject to pre-approval' in p26_text:
            s2_checks_passed += 1
            print(f"  PASS: Section 2 — 'subject to pre-approval' present in 2.1(c)")
        else:
            print(f"  FAIL: Section 2 — 'subject to pre-approval' not in 2.1(c): '{p26_text[:80]}'")

        s2_score = 0.30 * (s2_checks_passed / s2_checks_total)
        if s2_checks_passed == s2_checks_total:
            print(f"PASS: Component 3 — All Section 2 edits accepted ({s2_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 3 — {s2_checks_passed}/{s2_checks_total} Section 2 checks ({s2_score:.2f} pts)")
        total_score += s2_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: Section 3 edits rejected (0.30 points)
    # After rejecting David Kim's changes in Section 3:
    #   - Para 34: "five (5) years" present in final text (original restored)
    #     In initial, para.text shows neither "five (5) years" nor "two (2) years"
    #     (both are inside tracked change markup). In golden, "five (5) years" is plain text.
    #   - Para 36: no "commercially necessary" AND no tracked changes
    #     In initial, "commercially necessary" is in w:ins so para.text excludes it,
    #     but tracked change markup exists. We require both absent AND no markup.
    #   - Para 38: "injunctive relief" present in final text
    #     In initial, the original text is in w:del (excluded from para.text) and
    #     David's insertion is in w:ins (also excluded). In golden, original is restored.
    # ---------------------------------------------------------------
    try:
        s3_checks_passed = 0
        s3_checks_total = 3

        # Check para 34: "five (5) years" present in para.text
        # In initial: both "five (5) years" (del) and "two (2) years" (ins) are in markup,
        # para.text shows neither. In golden: "five (5) years" is in plain text.
        p34_text = paras[34].text
        if 'five (5) years' in p34_text:
            s3_checks_passed += 1
            print(f"  PASS: Section 3 — 'five (5) years' present in 3.1(a)")
        else:
            print(f"  FAIL: Section 3 — 'five (5) years' not in 3.1(a): '{p34_text[:80]}'")

        # Check para 36: "commercially necessary" absent AND no tracked changes
        p36_text = paras[36].text
        p36_has_tc = has_tracked_changes(paras[36]._element)
        if 'commercially necessary' not in p36_text and not p36_has_tc:
            s3_checks_passed += 1
            print(f"  PASS: Section 3 — 'commercially necessary' absent and no tracked changes in 3.1(b)")
        else:
            if p36_has_tc:
                print(f"  FAIL: Section 3 — 3.1(b) still has tracked change markup")
            else:
                print(f"  FAIL: Section 3 — 'commercially necessary' in 3.1(b)")

        # Check para 38: "injunctive relief" present in para.text
        # In initial: original text is in w:del, David's text in w:ins, para.text is nearly empty.
        # In golden: original text restored as plain text.
        p38_text = paras[38].text
        if 'injunctive relief' in p38_text:
            s3_checks_passed += 1
            print(f"  PASS: Section 3 — 'injunctive relief' present in 3.1(c)")
        else:
            print(f"  FAIL: Section 3 — 'injunctive relief' not in 3.1(c): '{p38_text[:80]}'")

        s3_score = 0.30 * (s3_checks_passed / s3_checks_total)
        if s3_checks_passed == s3_checks_total:
            print(f"PASS: Component 4 — All Section 3 edits rejected ({s3_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 4 — {s3_checks_passed}/{s3_checks_total} Section 3 checks ({s3_score:.2f} pts)")
        total_score += s3_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
