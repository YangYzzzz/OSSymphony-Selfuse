"""
Reward Script: Apply different line spacing to different parts of a business proposal document.
Task ID: wrpara_050
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Title & subtitle line spacing = proportional 150%
  Component 2 (0.15): Title space_after ~30pt, subtitle space_after ~18pt
  Component 3 (0.25): TOC entries (P11-P18) have fixed ~0.6cm line spacing (EXACTLY rule)
  Component 4 (0.20): Executive summary paragraphs (P21-P22) have exactly 20pt line spacing (EXACTLY rule)
  Component 5 (0.15): Main body paragraphs have proportional 115% line spacing (MULTIPLE rule, ls=1.15)
"""

import os
from docx import Document
from docx.shared import Pt, Cm, Emu

WORKDIR = '/home/user'
TASK_ID = 'wrpara_050'

# EMU constants for tolerance checks
PT_30 = 381000   # 30pt in EMU
PT_18 = 228600   # 18pt in EMU
CM_06 = 216000   # 0.6cm in EMU
PT_20 = 254000   # 20pt in EMU
TOLERANCE = 15000  # ~0.4mm / ~1.2pt tolerance for spacing values


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

    # Identify key paragraphs by content
    title_idx = None
    subtitle_idx = None
    toc_indices = []
    exec_summary_body_indices = []
    main_body_indices = []

    # Find title "Strategic Partnership Proposal" and subtitle "Prepared for Acme Corp"
    for i, p in enumerate(paras):
        t = p.text.strip()
        if t == 'Strategic Partnership Proposal':
            title_idx = i
        elif t == 'Prepared for Acme Corp':
            subtitle_idx = i

    # TOC entries: paragraphs with tab character between text and page number, after "Table of Contents" heading
    toc_heading_idx = None
    for i, p in enumerate(paras):
        if p.text.strip() == 'Table of Contents':
            toc_heading_idx = i
            break

    if toc_heading_idx is not None:
        for i in range(toc_heading_idx + 1, len(paras)):
            t = paras[i].text.strip()
            if not t:
                break  # empty paragraph ends TOC section
            if '\t' in paras[i].text:
                toc_indices.append(i)

    # Executive Summary body: paragraphs after "Executive Summary" heading, before next empty paragraph
    exec_heading_idx = None
    for i, p in enumerate(paras):
        if p.text.strip() == 'Executive Summary' and (toc_heading_idx is None or i > toc_heading_idx + 1):
            exec_heading_idx = i
            break

    if exec_heading_idx is not None:
        for i in range(exec_heading_idx + 1, len(paras)):
            t = paras[i].text.strip()
            if not t:
                break
            exec_summary_body_indices.append(i)

    # Main body: all non-empty content paragraphs in sections after executive summary
    # These are the section headings (numbered) and their body paragraphs
    # Section headings: "1. Company Overview", "2. Market Analysis", etc.
    # Body paragraphs: those that follow section headings and are not empty
    found_main_body_start = 0  # 0=not found, 1=found
    section_heading_indices = set()
    for i, p in enumerate(paras):
        t = p.text.strip()
        if t.startswith('1. Company Overview'):
            found_main_body_start = 1
        if found_main_body_start == 1 and t:
            # Check if this is a section heading (starts with number + period or is a known heading)
            if (len(t) > 2 and t[0].isdigit() and t[1] == '.') or t.startswith('5. '):
                section_heading_indices.add(i)
            else:
                main_body_indices.append(i)

    print(f"INFO: title_idx={title_idx}, subtitle_idx={subtitle_idx}")
    print(f"INFO: toc_indices={toc_indices}")
    print(f"INFO: exec_summary_body_indices={exec_summary_body_indices}")
    print(f"INFO: main_body_indices={main_body_indices}")

    # Component 1: Title & subtitle line spacing = proportional 150% (0.25 points)
    # In python-docx, proportional 150% can be ls_rule=ONE_POINT_FIVE (1) with ls=1.5,
    # or ls_rule=MULTIPLE (5) with ls=1.5
    try:
        comp1_checks_passed = 0  # need 2 of 2

        def check_proportional_150(para_name, idx):
            """Returns 1 if proportional 150%, 0 otherwise."""
            if idx is None:
                print(f"FAIL: Could not find {para_name} paragraph")
                return 0
            pf = paras[idx].paragraph_format
            ls = pf.line_spacing
            rule = pf.line_spacing_rule
            rule_val = rule.value if rule is not None else None
            # Accept ONE_POINT_FIVE (1) or MULTIPLE (5) with ls ~1.5
            if rule_val in (1, 5) and ls is not None and isinstance(ls, (int, float)) and abs(float(ls) - 1.5) < 0.05:
                print(f"PASS: {para_name} line spacing = {ls}, rule = {rule} (proportional 150%)")
                return 1
            print(f"FAIL: {para_name} ls_rule = {rule_val}, ls = {ls} (expected proportional 150%)")
            return 0

        comp1_checks_passed += check_proportional_150("Title", title_idx)
        comp1_checks_passed += check_proportional_150("Subtitle", subtitle_idx)

        if comp1_checks_passed == 2:
            print(f"PASS: Component 1 -- Title & subtitle proportional 150% (0.25 pts)")
            total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Title space_after ~30pt (381000 EMU), subtitle space_after ~18pt (228600 EMU) (0.15 points)
    try:
        comp2_checks_passed = 0  # need 2 of 2
        if title_idx is not None:
            sa = paras[title_idx].paragraph_format.space_after
            if sa is not None and abs(int(sa) - PT_30) <= TOLERANCE:
                print(f"PASS: Title space_after = {sa} EMU (~30pt, expected {PT_30})")
                comp2_checks_passed += 1
            else:
                print(f"FAIL: Title space_after = {sa}, expected ~{PT_30} (30pt)")

        if subtitle_idx is not None:
            sa = paras[subtitle_idx].paragraph_format.space_after
            if sa is not None and abs(int(sa) - PT_18) <= TOLERANCE:
                print(f"PASS: Subtitle space_after = {sa} EMU (~18pt, expected {PT_18})")
                comp2_checks_passed += 1
            else:
                print(f"FAIL: Subtitle space_after = {sa}, expected ~{PT_18} (18pt)")

        if comp2_checks_passed == 2:
            print(f"PASS: Component 2 -- Title/subtitle spacing after (0.15 pts)")
            total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: TOC entries have fixed 0.6cm line spacing, EXACTLY rule (0.25 points)
    # 0.6cm = 216000 EMU. In EXACTLY mode, ls is stored as EMU integer.
    try:
        if len(toc_indices) >= 6:  # expect 8 entries, require at least 6
            toc_pass_count = 0
            for idx in toc_indices:
                pf = paras[idx].paragraph_format
                ls = pf.line_spacing
                rule = pf.line_spacing_rule
                rule_val = rule.value if rule is not None else None
                # EXACTLY rule = 4
                if rule_val == 4 and ls is not None:
                    ls_emu = int(ls)
                    if abs(ls_emu - CM_06) <= TOLERANCE:
                        toc_pass_count += 1
                    else:
                        print(f"FAIL: TOC P{idx} ls={ls_emu} EMU, expected ~{CM_06} (0.6cm)")
                else:
                    print(f"FAIL: TOC P{idx} rule={rule_val} (expected 4=EXACTLY), ls={ls}")

            ratio = toc_pass_count / len(toc_indices)
            if ratio >= 0.75:
                print(f"PASS: Component 3 -- TOC fixed 0.6cm spacing ({toc_pass_count}/{len(toc_indices)} entries) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Only {toc_pass_count}/{len(toc_indices)} TOC entries have correct spacing")
        else:
            print(f"FAIL: Component 3 -- Found only {len(toc_indices)} TOC entries (expected >= 6)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Executive summary body paragraphs have exactly 20pt line spacing (0.20 points)
    # 20pt = 254000 EMU, EXACTLY rule (4)
    try:
        if len(exec_summary_body_indices) >= 1:
            exec_pass_count = 0
            for idx in exec_summary_body_indices:
                pf = paras[idx].paragraph_format
                ls = pf.line_spacing
                rule = pf.line_spacing_rule
                rule_val = rule.value if rule is not None else None
                if rule_val == 4 and ls is not None:
                    ls_emu = int(ls)
                    if abs(ls_emu - PT_20) <= TOLERANCE:
                        exec_pass_count += 1
                    else:
                        print(f"FAIL: Exec summary P{idx} ls={ls_emu} EMU, expected ~{PT_20} (20pt)")
                else:
                    print(f"FAIL: Exec summary P{idx} rule={rule_val} (expected 4=EXACTLY), ls={ls}")

            ratio = exec_pass_count / len(exec_summary_body_indices)
            if ratio >= 0.75:
                print(f"PASS: Component 4 -- Exec summary 20pt spacing ({exec_pass_count}/{len(exec_summary_body_indices)}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 -- Only {exec_pass_count}/{len(exec_summary_body_indices)} exec summary paras correct")
        else:
            print(f"FAIL: Component 4 -- No executive summary body paragraphs found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Main body paragraphs have proportional 115% line spacing (0.15 points)
    # ls=1.15, ls_rule=MULTIPLE (5)
    try:
        if len(main_body_indices) >= 5:
            body_pass_count = 0
            for idx in main_body_indices:
                pf = paras[idx].paragraph_format
                ls = pf.line_spacing
                rule = pf.line_spacing_rule
                rule_val = rule.value if rule is not None else None
                if rule_val == 5 and ls is not None:
                    if isinstance(ls, (int, float)) and abs(float(ls) - 1.15) < 0.05:
                        body_pass_count += 1
                    else:
                        print(f"FAIL: Body P{idx} ls={ls}, expected ~1.15")
                else:
                    print(f"FAIL: Body P{idx} rule={rule_val} (expected 5=MULTIPLE), ls={ls}")

            ratio = body_pass_count / len(main_body_indices)
            if ratio >= 0.75:
                print(f"PASS: Component 5 -- Main body 115% spacing ({body_pass_count}/{len(main_body_indices)}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 -- Only {body_pass_count}/{len(main_body_indices)} body paras correct")
        else:
            print(f"FAIL: Component 5 -- Found only {len(main_body_indices)} main body paragraphs (expected >= 5)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
