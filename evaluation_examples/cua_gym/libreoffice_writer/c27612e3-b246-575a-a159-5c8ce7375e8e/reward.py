"""
Reward Script: Merge Sections 7 and 8 of a legal contract into one,
               renumber subsequent sections.
Task ID: writer_legal_094
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30) - Combined section heading exists
  Component 2 (0.25) - Old separate Section 8 heading removed; content merged under Section 7
  Component 3 (0.25) - Subsequent sections renumbered (9->8, 10->9, 11->10, 12->11)
  Component 4 (0.20) - Cross-references updated in document body
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_094'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
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

    paragraphs = doc.paragraphs
    para_texts = [p.text.strip() for p in paragraphs]

    # Build list of section headings (paragraphs matching "Section N - ...")
    section_headings = {}  # number -> (para_index, full_text)
    for i, text in enumerate(para_texts):
        m = re.match(r'^Section\s+(\d+)\s*[-\u2013\u2014]\s*(.+)$', text)
        if m:
            sec_num = int(m.group(1))
            sec_title = m.group(2).strip()
            section_headings[sec_num] = (i, sec_title)

    print(f"INFO: Found {len(section_headings)} section headings: {sorted(section_headings.keys())}")
    for num in sorted(section_headings.keys()):
        idx, title = section_headings[num]
        print(f"  Section {num}: '{title}' (para {idx})")

    # =====================================================================
    # Component 1: Combined heading "Section 7 - Limitation of Liability
    #              and Indemnification" exists (0.30 points)
    # =====================================================================
    try:
        if 7 in section_headings:
            title7 = section_headings[7][1].lower()
            has_limitation = 'limitation of liability' in title7
            has_indemnification = 'indemnification' in title7
            if has_limitation and has_indemnification:
                print(f"PASS: Component 1 - Combined heading found: '{section_headings[7][1]}' (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 - Section 7 title missing combined terms. Found: '{section_headings[7][1]}'")
        else:
            print("FAIL: Component 1 - No Section 7 heading found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # =====================================================================
    # Component 2: Old Section 8 "Indemnification" heading is gone;
    #              indemnification content appears under Section 7 (0.25 pts)
    # =====================================================================
    try:
        # Check that there is no standalone "Section 8 - Indemnification" heading
        old_sec8_still_present = (
            8 in section_headings
            and 'indemnification' in section_headings[8][1].lower()
            and 'liability' not in section_headings[8][1].lower()
        )

        if old_sec8_still_present:
            print("FAIL: Component 2 - Old standalone 'Section 8 - Indemnification' heading still exists")
        else:
            # Verify indemnification content exists between Section 7 heading and
            # the next section heading (whatever number it is)
            if 7 in section_headings:
                sec7_idx = section_headings[7][0]
                # Find next section heading after sec7
                next_sec_idx = len(para_texts)
                for num in sorted(section_headings.keys()):
                    if num > 7:
                        next_sec_idx = section_headings[num][0]
                        break

                # Look for indemnification content between sec7 heading and next section
                content_between = ' '.join(para_texts[sec7_idx+1:next_sec_idx]).lower()
                if 'indemnif' in content_between:
                    print(f"PASS: Component 2 - Indemnification content merged under Section 7 (0.25 pts)")
                    total_score += 0.25
                else:
                    print("FAIL: Component 2 - Indemnification content not found under Section 7")
            else:
                print("FAIL: Component 2 - Section 7 heading not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # =====================================================================
    # Component 3: Subsequent sections renumbered correctly (0.25 pts)
    #   Old 9 "Term and Termination"       -> 8
    #   Old 10 "Representations..."        -> 9
    #   Old 11 "Dispute Resolution"        -> 10
    #   Old 12 "General Provisions"        -> 11
    #   Total should be 11 sections (not 12)
    # =====================================================================
    try:
        renumber_checks = 0
        expected_map = {
            8: 'term',             # "Term and Termination"
            9: 'warrant',          # "Representations and Warranties"
            10: 'dispute',         # "Dispute Resolution"
            11: 'general',         # "General Provisions"
        }

        for expected_num, keyword in expected_map.items():
            if expected_num in section_headings:
                title_lower = section_headings[expected_num][1].lower()
                if keyword in title_lower:
                    renumber_checks += 1
                else:
                    print(f"  INFO: Section {expected_num} title '{section_headings[expected_num][1]}' does not contain '{keyword}'")
            else:
                print(f"  INFO: Section {expected_num} not found")

        # Also check that Section 12 does NOT exist (should be renumbered to 11)
        no_sec12 = 12 not in section_headings

        if renumber_checks == 4 and no_sec12:
            print(f"PASS: Component 3 - All 4 subsequent sections correctly renumbered, no Section 12 (0.25 pts)")
            total_score += 0.25
        elif renumber_checks >= 2 and no_sec12:
            partial = 0.15
            print(f"PARTIAL: Component 3 - {renumber_checks}/4 sections renumbered correctly ({partial} pts)")
            total_score += partial
        elif renumber_checks >= 1:
            partial = 0.08
            print(f"PARTIAL: Component 3 - {renumber_checks}/4 sections renumbered ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - Sections not renumbered (found: {renumber_checks}/4, sec12 absent: {no_sec12})")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # =====================================================================
    # Component 4: Cross-references updated in document body (0.20 pts)
    #   The merge changes cross-references. Specifically:
    #   - Old "Section 8 (Indemnification)" refs in Sec 7 body should be
    #     replaced (e.g., with "this Section 7" or removed)
    #   - The indemnification paragraphs (now under Sec 7) should reference
    #     "this Section 7" not "this Section 8"
    #   - The "Term and Termination" section body should self-reference as
    #     "Section 8" (was "Section 9")
    #
    #   Key: these checks must FAIL on initial and PASS on golden.
    #   Initial has "Section 8 (Indemnification)" in sec 7 body -> check absence = FAIL
    #   Initial has "this Section 8" in indemnification body (sec 8) -> doesn't help
    #   So we focus on changes that are specific to the merge.
    # =====================================================================
    try:
        xref_pass = 0
        xref_total = 2

        # Check 1: The limitation-of-liability paragraphs should NOT reference
        # "Section 8 (Indemnification)" as a separate section any more.
        # In the INITIAL doc, paras [24],[25] contain "SECTION 8 (INDEMNIFICATION)".
        # In the GOLDEN doc, these refs should be replaced/updated.
        # This check: absence of "Section 8" + "Indemnification" pattern in sec 7 body
        # AND the indemnification paras under sec 7 should use "this Section 7"
        # not "this Section 8".
        if 7 in section_headings:
            sec7_idx = section_headings[7][0]
            next_sec_idx = len(para_texts)
            for num in sorted(section_headings.keys()):
                if num > 7:
                    next_sec_idx = section_headings[num][0]
                    break
            sec7_body = ' '.join(para_texts[sec7_idx+1:next_sec_idx])

            # In the initial doc, "SECTION 8 (INDEMNIFICATION)" exists in sec 7 body.
            # In the golden doc, it should be gone or replaced.
            has_old_sec8_ref = bool(re.search(r'Section\s+8\s*\(Indemnification\)', sec7_body, re.IGNORECASE))
            if not has_old_sec8_ref:
                # Also confirm indemnification paras say "this Section 7" not "this Section 8"
                # The indemnification obligations para had "this Section 8" in initial
                has_this_sec7 = bool(re.search(r'this\s+Section\s+7', sec7_body, re.IGNORECASE))
                has_this_sec8 = bool(re.search(r'this\s+Section\s+8', sec7_body, re.IGNORECASE))
                if has_this_sec7 and not has_this_sec8:
                    xref_pass += 1
                    print("  INFO: Cross-ref check 1 PASS: 'Section 8 (Indemnification)' removed, 'this Section 7' present in merged body")
                else:
                    print(f"  INFO: Cross-ref check 1 PARTIAL: old ref gone but self-ref issue (this_sec7={has_this_sec7}, this_sec8={has_this_sec8})")
            else:
                print("  INFO: Cross-ref check 1 FAIL: 'Section 8 (Indemnification)' still in sec 7 body")

        # Check 2: "Term and Termination" section self-references should use
        # its new number. In initial, it's Section 9 with "this Section 9".
        # In golden, it's Section 8 with "this Section 8".
        if 8 in section_headings:
            title8_lower = section_headings[8][1].lower()
            if 'term' in title8_lower:
                sec8_idx = section_headings[8][0]
                next_after_8 = len(para_texts)
                for num in sorted(section_headings.keys()):
                    if num > 8:
                        next_after_8 = section_headings[num][0]
                        break
                sec8_body = ' '.join(para_texts[sec8_idx+1:next_after_8]).lower()
                has_this_sec8 = 'this section 8' in sec8_body or 'section 8' in sec8_body
                has_this_sec9 = 'this section 9' in sec8_body or 'section 9' in sec8_body
                if has_this_sec8 and not has_this_sec9:
                    xref_pass += 1
                    print("  INFO: Cross-ref check 2 PASS: Term section self-references as Section 8 (renumbered from 9)")
                else:
                    print(f"  INFO: Cross-ref check 2 FAIL: sec8_ref={has_this_sec8}, old_sec9_ref={has_this_sec9}")
            else:
                print(f"  INFO: Cross-ref check 2 SKIP: Section 8 is '{section_headings[8][1]}', not Term and Termination")
        else:
            print("  INFO: Cross-ref check 2 SKIP: no Section 8 found")

        if xref_pass == xref_total:
            print(f"PASS: Component 4 - Cross-references fully updated ({xref_pass}/{xref_total}, 0.20 pts)")
            total_score += 0.20
        elif xref_pass > 0:
            pts = round(0.20 * xref_pass / xref_total, 2)
            print(f"PARTIAL: Component 4 - Cross-references partially updated ({xref_pass}/{xref_total}, {pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 4 - Cross-references not updated ({xref_pass}/{xref_total})")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
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
