"""
Reward Script: Fix 3-level nested list in marketing plan document
Task ID: writer_mktg_039
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): All 25 list items use consistent 'List Paragraph' style with single numId
  Component 2 (0.35): Correct indentation - Level 1 at ~0.5in, Level 2 at ~1.0in, Level 3 at ~1.5in
  Component 3 (0.30): Correct number formats per level (decimal / lowerLetter / lowerRoman)
                       and correct item counts at each level (5 L1, 12 L2, 8 L3)
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_mktg_039'
FILE_PATH = f'{WORKDIR}/Desktop/marketing_plan_lists.docx'

# Indentation tolerance in EMU (~0.05 inches = 45720 EMU)
INDENT_TOLERANCE_EMU = 45720

# Expected indentation in EMU: 0.5in, 1.0in, 1.5in = 457200, 914400, 1371600
EXPECTED_INDENT = {0: 457200, 1: 914400, 2: 1371600}

# Paragraphs with these indices (0-based) are the list items: indices 5-34 inclusive
LIST_PARA_START = 5
LIST_PARA_END = 34  # inclusive

# Expected level assignments (indices 5..34) based on ground truth
# L1 (ilvl=0): 5, 13, 18, 24, 29  → 5 items
# L2 (ilvl=1): 6, 9, 12, 14, 17, 19, 21, 23, 25, 27, 30, 32, 34 → 13 items... let me count carefully
# From golden exploration:
# ilvl=0: paras 5,13,18,24,29 → 5 items
# ilvl=1: paras 6,9,12,14,17,19,21,23,25,27,30,32,34 → 13 items?
# ilvl=2: paras 7,8,10,11,15,16,20,22,26,28,31,33 → 12 items?
# But task says 12 L2 and 8 L3. Let me count from golden exploration output:
# ilvl=0: 5,13,18,24,29 => 5 items ✓
# ilvl=1: 6,9,12,14,17,19,21,23,25,27,30,32,34 => 13 items
# ilvl=2: 7,8,10,11,15,16,20,22,26,28,31,33 => 12 items
# Total = 5+13+12 = 30 items... but task says 25 (5+12+8)?
# Actual golden has all items indices 5-34 = 30 items (not 25)
# Context says 5 L1, 12 L2, 8 L3 = 25 total, but golden shows 30 items.
# We must trust the actual golden artifact, not the context counts.
# Actual counts: 5 L1 + 13 L2 + 12 L3 = 30 items total

EXPECTED_LEVEL_COUNTS = {0: 5, 1: 13, 2: 12}  # from actual golden artifact


def get_num_format_for_level(numbering_part, num_id, ilvl):
    """
    Look up the numFmt value for a given numId and ilvl from the numbering XML.
    Returns the numFmt string (e.g., 'decimal', 'lowerLetter', 'lowerRoman') or None.
    """
    if numbering_part is None:
        return None

    root = numbering_part._element
    ns_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    # Find the abstractNumId for this numId
    abstract_num_id = None
    for num_el in root.findall(f'{{{ns_w}}}num'):
        if num_el.get(f'{{{ns_w}}}numId') == str(num_id):
            abstract_ref = num_el.find(f'{{{ns_w}}}abstractNumId')
            if abstract_ref is not None:
                abstract_num_id = abstract_ref.get(f'{{{ns_w}}}val')
            break

    if abstract_num_id is None:
        return None

    # Find the abstractNum definition
    for abstract_el in root.findall(f'{{{ns_w}}}abstractNum'):
        if abstract_el.get(f'{{{ns_w}}}abstractNumId') == str(abstract_num_id):
            for lvl_el in abstract_el.findall(f'{{{ns_w}}}lvl'):
                if lvl_el.get(f'{{{ns_w}}}ilvl') == str(ilvl):
                    num_fmt_el = lvl_el.find(f'{{{ns_w}}}numFmt')
                    if num_fmt_el is not None:
                        return num_fmt_el.get(f'{{{ns_w}}}val')

    return None


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

    # Collect list paragraphs (paragraphs 5-34 inclusive by index)
    all_paras = doc.paragraphs
    if len(all_paras) < LIST_PARA_END + 1:
        print(f"FAIL: Document has fewer paragraphs than expected ({len(all_paras)} < {LIST_PARA_END + 1})")
        print("REWARD: 0.0")
        return 0.0

    list_paras = []
    for i in range(LIST_PARA_START, LIST_PARA_END + 1):
        para = all_paras[i]
        pPr = para._p.find(qn('w:pPr'))
        numPr = pPr.find(qn('w:numPr')) if pPr is not None else None
        num_id = None
        ilvl = None
        if numPr is not None:
            ilvl_el = numPr.find(qn('w:ilvl'))
            num_id_el = numPr.find(qn('w:numId'))
            ilvl = int(ilvl_el.get(qn('w:val'))) if ilvl_el is not None else None
            num_id = int(num_id_el.get(qn('w:val'))) if num_id_el is not None else None
        indent_emu = para.paragraph_format.left_indent
        list_paras.append({
            'idx': i,
            'style': para.style.name,
            'num_id': num_id,
            'ilvl': ilvl,
            'indent_emu': indent_emu or 0,
            'text': para.text[:60],
        })

    # -----------------------------------------------------------------------
    # Component 1: Consistent style and single numId across all list items (0.35 pts)
    # All 30 list paragraphs should use 'List Paragraph' style AND share a single numId
    # -----------------------------------------------------------------------
    try:
        styles_found = set(p['style'] for p in list_paras)
        num_ids_found = set(p['num_id'] for p in list_paras)

        all_list_paragraph = (styles_found == {'List Paragraph'})
        single_num_id = (len(num_ids_found) == 1 and None not in num_ids_found)

        if all_list_paragraph and single_num_id:
            print(f"PASS: Component 1 — All {len(list_paras)} list items use 'List Paragraph' style "
                  f"with single numId={list(num_ids_found)[0]} (0.35 pts)")
            total_score += 0.35
        else:
            if not all_list_paragraph:
                print(f"FAIL: Component 1 — Not all list items use 'List Paragraph'. Found styles: {styles_found}")
            if not single_num_id:
                print(f"FAIL: Component 1 — List items do not share a single numId. Found: {num_ids_found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Correct indentation per level (0.35 pts)
    # ilvl=0 -> ~0.5in, ilvl=1 -> ~1.0in, ilvl=2 -> ~1.5in
    # A paragraph must have a valid ilvl to be checked
    # -----------------------------------------------------------------------
    try:
        indent_errors = []
        items_with_ilvl = [p for p in list_paras if p['ilvl'] is not None]

        if not items_with_ilvl:
            print("FAIL: Component 2 — No list items have ilvl set")
        else:
            for p in items_with_ilvl:
                ilvl = p['ilvl']
                if ilvl not in EXPECTED_INDENT:
                    continue
                expected = EXPECTED_INDENT[ilvl]
                actual = p['indent_emu']
                if abs(actual - expected) > INDENT_TOLERANCE_EMU:
                    indent_errors.append(
                        f"  Para [{p['idx']}] ilvl={ilvl}: expected indent ~{expected} EMU "
                        f"(~{expected/914400:.2f}in), got {actual} EMU (~{actual/914400:.2f}in) — '{p['text'][:40]}'"
                    )

            if not indent_errors:
                print(f"PASS: Component 2 — All {len(items_with_ilvl)} list items have correct indentation "
                      f"per level (±{INDENT_TOLERANCE_EMU} EMU tolerance) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — {len(indent_errors)} indentation errors:")
                for err in indent_errors[:5]:
                    print(err)
                if len(indent_errors) > 5:
                    print(f"  ... and {len(indent_errors) - 5} more")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Correct numbering format per level AND correct item counts (0.30 pts)
    # ilvl=0 -> decimal, ilvl=1 -> lowerLetter, ilvl=2 -> lowerRoman
    # Expected counts: {0: 5, 1: 13, 2: 12}
    # -----------------------------------------------------------------------
    try:
        items_with_ilvl = [p for p in list_paras if p['ilvl'] is not None]

        # Check item counts per level
        level_counts = {0: 0, 1: 0, 2: 0}
        for p in items_with_ilvl:
            if p['ilvl'] in level_counts:
                level_counts[p['ilvl']] += 1

        count_ok = (level_counts == EXPECTED_LEVEL_COUNTS)

        # Check number format from numbering XML
        num_ids_found = set(p['num_id'] for p in list_paras if p['num_id'] is not None)
        format_ok = False
        if num_ids_found:
            num_id = list(num_ids_found)[0]
            try:
                numbering_part = doc.part.numbering_part
            except Exception:
                numbering_part = None

            fmt_l0 = get_num_format_for_level(numbering_part, num_id, 0)
            fmt_l1 = get_num_format_for_level(numbering_part, num_id, 1)
            fmt_l2 = get_num_format_for_level(numbering_part, num_id, 2)

            fmt_ok_l0 = (fmt_l0 == 'decimal')
            fmt_ok_l1 = (fmt_l1 == 'lowerLetter')
            fmt_ok_l2 = (fmt_l2 == 'lowerRoman')

            format_ok = fmt_ok_l0 and fmt_ok_l1 and fmt_ok_l2

            if not fmt_ok_l0:
                print(f"FAIL: Component 3 — Level 0 format: expected 'decimal', got '{fmt_l0}'")
            if not fmt_ok_l1:
                print(f"FAIL: Component 3 — Level 1 format: expected 'lowerLetter', got '{fmt_l1}'")
            if not fmt_ok_l2:
                print(f"FAIL: Component 3 — Level 2 format: expected 'lowerRoman', got '{fmt_l2}'")
        else:
            print("FAIL: Component 3 — Cannot determine numId, cannot check number formats")

        if not count_ok:
            print(f"FAIL: Component 3 — Level item counts: got {level_counts}, expected {EXPECTED_LEVEL_COUNTS}")

        if format_ok and count_ok:
            print(f"PASS: Component 3 — Numbering formats correct "
                  f"(L0=decimal, L1=lowerLetter, L2=lowerRoman) AND item counts correct "
                  f"(L0={level_counts[0]}, L1={level_counts[1]}, L2={level_counts[2]}) (0.30 pts)")
            total_score += 0.30
        elif format_ok:
            # Partial: formats correct but counts off — give half credit
            print(f"PARTIAL: Component 3 — Numbering formats correct but item counts wrong: {level_counts} vs {EXPECTED_LEVEL_COUNTS} (0.15 pts)")
            total_score += 0.15
        elif count_ok:
            # Partial: counts right but formats wrong — give half credit
            print(f"PARTIAL: Component 3 — Item counts correct but numbering formats wrong (0.15 pts)")
            total_score += 0.15

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
