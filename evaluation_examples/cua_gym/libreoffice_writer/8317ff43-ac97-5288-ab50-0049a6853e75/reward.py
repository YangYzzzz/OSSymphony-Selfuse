"""
Reward Script: Reject the tracked deletion of the confidentiality clause in Section 4
Task ID: writer_rm_004
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Tracked deletion by James Rivera is removed (no w:del elements)
  Component 2 (0.3): Confidentiality paragraph restored as normal text in Section 4
  Component 3 (0.2): Deletion rejected AND other tracked insertions preserved (compound)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_004'


def persist_app_state(domain):
    """Attempt to save any unsaved state in LibreOffice."""
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
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = doc.element.body

    # Component 1: Tracked deletion by James Rivera is removed (0.5 points)
    # In the initial state there is 1 tracked deletion (w:del). After rejecting it, there should be 0.
    deletion_rejected = False
    try:
        dels = body.findall('.//w:del', ns)
        num_dels = len(dels)
        if num_dels == 0:
            print(f"PASS: Component 1 — No tracked deletions found (0.5 pts)")
            total_score += 0.5
            deletion_rejected = True
        else:
            # Check if specifically the James Rivera deletion is gone
            james_dels = [d for d in dels if d.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author', '') == 'James Rivera']
            if len(james_dels) == 0:
                print(f"PASS: Component 1 — James Rivera deletion removed, {num_dels} other deletions remain (0.5 pts)")
                total_score += 0.5
                deletion_rejected = True
            else:
                del_texts = []
                for d in james_dels:
                    texts = d.findall('.//w:delText', ns)
                    del_texts.append(''.join(t.text for t in texts if t.text)[:80])
                print(f"FAIL: Component 1 — Found {len(james_dels)} James Rivera deletion(s): {del_texts}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Confidentiality paragraph restored as normal text in Section 4 (0.3 points)
    # The paragraph starting with "Both parties agree to maintain strict confidentiality" should
    # appear as normal text (not inside a w:del) between Section 4 heading and Section 5 heading.
    try:
        target_phrase = "Both parties agree to maintain strict confidentiality"
        found_in_section4 = False

        in_section4 = False
        for para in doc.paragraphs:
            # Detect Section 4 heading
            if para.style and para.style.name == 'Heading 1' and 'Section 4' in para.text:
                in_section4 = True
                continue
            # Detect next section heading (end of Section 4)
            if in_section4 and para.style and para.style.name == 'Heading 1':
                break
            # Check if the confidentiality paragraph is in Section 4
            if in_section4 and target_phrase in para.text:
                found_in_section4 = True

        if found_in_section4:
            # Also verify it's NOT inside a tracked deletion (normal text)
            del_texts_all = []
            for d in body.findall('.//w:del', ns):
                texts = d.findall('.//w:delText', ns)
                del_texts_all.append(''.join(t.text for t in texts if t.text))
            in_deletion = any(target_phrase in dt for dt in del_texts_all)

            if not in_deletion:
                print(f"PASS: Component 2 — Confidentiality paragraph found as normal text in Section 4 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Confidentiality paragraph found but still inside a tracked deletion")
        else:
            print(f"FAIL: Component 2 — Confidentiality paragraph not found in Section 4")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Deletion rejected AND other tracked insertions preserved (0.2 points)
    # This is a compound check: only awards points if the deletion was already rejected (Component 1)
    # AND the 3 other tracked insertions remain intact.
    # This ensures we only score task-introduced changes (the insertions alone are preconditions).
    try:
        if not deletion_rejected:
            print(f"FAIL: Component 3 — Deletion not yet rejected, skipping insertion preservation check")
        else:
            inss = body.findall('.//w:ins', ns)
            num_inss = len(inss)

            # Check for the specific expected insertions
            expected_authors_texts = [
                ("Lisa Thompson", "The scope of this Agreement extends to any subsidiaries"),
                ("Lisa Thompson", "three (3)"),
                ("James Rivera", "Liquidated damages"),
            ]

            found_count = 0
            for exp_author, exp_text_start in expected_authors_texts:
                for ins in inss:
                    author = ins.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author', '')
                    texts = ins.findall('.//w:t', ns)
                    text_content = ''.join(t.text for t in texts if t.text)
                    if author == exp_author and exp_text_start in text_content:
                        found_count += 1
                        break

            if found_count >= 3:
                print(f"PASS: Component 3 — Deletion rejected AND all 3 tracked insertions preserved (0.2 pts)")
                total_score += 0.2
            elif found_count >= 2:
                partial = round(0.2 * found_count / 3, 2)
                print(f"PARTIAL: Component 3 — Deletion rejected but only {found_count}/3 insertions preserved ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {found_count}/3 expected tracked insertions found ({num_inss} total)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state("libreoffice_writer")
    verify_task(file_path)
