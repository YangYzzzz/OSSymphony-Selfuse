"""
Reward Script: Protect Section 5 of contract document
Task ID: writer_legal_032
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Document protection is enabled (readOnly + enforcement)
  Component 2 (0.35): Section 5 paragraphs are NOT inside any editable permission range
  Component 3 (0.30): Other sections (1-4, 6-8) ARE inside editable permission ranges
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_032'

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


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
    # Component 1: Document protection enabled (0.35 points)
    # The document must have documentProtection with edit=readOnly
    # and enforcement=1 (or "true") in the settings.
    # This is a prerequisite for section-level protection to work.
    # ---------------------------------------------------------------
    try:
        settings_elem = doc.settings.element
        doc_prot = settings_elem.find('w:documentProtection', NS)
        if doc_prot is not None:
            edit_val = doc_prot.get(f'{{{WNS}}}edit', '')
            enforce_val = doc_prot.get(f'{{{WNS}}}enforcement', '')
            # readOnly or sections are valid protection modes
            prot_mode_ok = edit_val in ('readOnly', 'sections')
            enforce_ok = enforce_val in ('1', 'true')
            if prot_mode_ok and enforce_ok:
                print(f"PASS: Component 1 — Document protection enabled (edit={edit_val}, enforcement={enforce_val}) (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — Protection mode/enforcement incorrect: edit={edit_val}, enforcement={enforce_val}")
        else:
            print("FAIL: Component 1 — No documentProtection element found in settings")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Helper: Map body children to identify paragraph positions and
    # which are inside editable (permStart/permEnd) ranges.
    # ---------------------------------------------------------------
    try:
        all_children = list(body)
        # Build list of editable ranges based on permStart/permEnd
        editable_ranges = []  # list of (start_idx, end_idx) inclusive
        open_perms = {}  # id -> start_idx

        for i, child in enumerate(all_children):
            tag = etree.QName(child.tag).localname if isinstance(child.tag, str) else str(child.tag)
            if tag == 'permStart':
                pid = child.get(f'{{{WNS}}}id', '')
                edGrp = child.get(f'{{{WNS}}}edGrp', '')
                if edGrp == 'everyone' or edGrp:  # any editable group counts
                    open_perms[pid] = i
            elif tag == 'permEnd':
                pid = child.get(f'{{{WNS}}}id', '')
                if pid in open_perms:
                    editable_ranges.append((open_perms[pid], i))
                    del open_perms[pid]

        # Also check for permStart/permEnd as direct children of paragraphs
        # (they can appear inside <w:p> elements too)
        para_perm_map = {}  # body_child_index -> list of perm events
        for i, child in enumerate(all_children):
            tag = etree.QName(child.tag).localname if isinstance(child.tag, str) else str(child.tag)
            if tag == 'p':
                for pchild in child:
                    ptag = etree.QName(pchild.tag).localname if isinstance(pchild.tag, str) else str(pchild.tag)
                    if ptag in ('permStart', 'permEnd'):
                        pid = pchild.get(f'{{{WNS}}}id', '')
                        edGrp = pchild.get(f'{{{WNS}}}edGrp', '')
                        if ptag == 'permStart' and (edGrp == 'everyone' or edGrp):
                            open_perms[pid] = i
                        elif ptag == 'permEnd' and pid in open_perms:
                            editable_ranges.append((open_perms[pid], i))
                            del open_perms[pid]

        print(f"  INFO: Found {len(editable_ranges)} editable ranges: {editable_ranges}")

        # Identify which body children are paragraphs and map to heading sections
        # Find indices of Section 5 heading and the next section heading
        section5_start = None
        section5_end = None  # exclusive (the next heading or end)
        heading_indices = []

        for i, child in enumerate(all_children):
            tag = etree.QName(child.tag).localname if isinstance(child.tag, str) else str(child.tag)
            if tag == 'p':
                # Get style
                pPr = child.find('w:pPr', NS)
                if pPr is not None:
                    pStyle = pPr.find('w:pStyle', NS)
                    if pStyle is not None:
                        style_val = pStyle.get(f'{{{WNS}}}val', '')
                        if style_val in ('Heading1', 'Heading 1'):
                            # Get text
                            runs = child.findall('.//w:t', NS)
                            text = ''.join(r.text or '' for r in runs)
                            heading_indices.append((i, text))
                            if 'Section 5' in text or 'Standard Terms and Conditions' in text:
                                section5_start = i

        # Find where Section 5 ends (start of next heading after Section 5)
        if section5_start is not None:
            for idx, text in heading_indices:
                if idx > section5_start:
                    section5_end = idx
                    break
            if section5_end is None:
                # Section 5 goes to the end of document
                section5_end = len(all_children)

        print(f"  INFO: Section 5 range: body children [{section5_start}, {section5_end})")
        print(f"  INFO: All headings: {[(i, t[:40]) for i, t in heading_indices]}")

    except Exception as e:
        print(f"ERROR: Helper section mapping — {e}")
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    # ---------------------------------------------------------------
    # Component 2: Section 5 paragraphs are NOT editable (0.35 points)
    # All body children in the Section 5 range must NOT be inside
    # any editable permission range. REQUIRES document protection to
    # be enabled (otherwise "not in editable range" is meaningless).
    # ---------------------------------------------------------------
    try:
        if section5_start is None:
            print("FAIL: Component 2 — Could not locate Section 5 heading")
        elif len(editable_ranges) == 0:
            # No editable ranges means no section-level protection scheme at all.
            # Without document protection + permStart/permEnd, nothing is protected.
            print("FAIL: Component 2 — No editable permission ranges found (no protection scheme)")
        else:
            def is_in_editable_range(idx):
                """Check if body child at idx is inside an editable range."""
                for (rs, re_) in editable_ranges:
                    if rs < idx < re_:
                        return True
                return False

            section5_protected = True
            unprotected_indices = []
            for idx in range(section5_start, section5_end):
                tag = etree.QName(all_children[idx].tag).localname if isinstance(all_children[idx].tag, str) else str(all_children[idx].tag)
                if tag in ('permStart', 'permEnd', 'sectPr'):
                    continue  # skip non-content elements
                if is_in_editable_range(idx):
                    section5_protected = False
                    unprotected_indices.append(idx)

            if section5_protected:
                print(f"PASS: Component 2 — Section 5 (indices {section5_start}-{section5_end-1}) is fully protected (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — Section 5 has {len(unprotected_indices)} unprotected body children: {unprotected_indices[:5]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: Other sections ARE editable (0.30 points)
    # Sections 1-4 and 6-8 content paragraphs should be inside
    # editable permission ranges.
    # ---------------------------------------------------------------
    try:
        if section5_start is None or section5_end is None:
            print("FAIL: Component 3 — Could not locate Section 5 boundaries")
        elif len(editable_ranges) == 0:
            print("FAIL: Component 3 — No editable permission ranges found")
        else:
            def is_in_editable_range(idx):
                for (rs, re_) in editable_ranges:
                    if rs < idx < re_:
                        return True
                return False

            # Check a sample of paragraphs outside Section 5
            # Before Section 5: first content paragraph and last content paragraph before Section 5
            # After Section 5: first content paragraph and last content paragraph
            other_paras = []
            for i, child in enumerate(all_children):
                tag = etree.QName(child.tag).localname if isinstance(child.tag, str) else str(child.tag)
                if tag == 'p' and (i < section5_start or i >= section5_end):
                    runs = child.findall('.//w:t', NS)
                    text = ''.join(r.text or '' for r in runs).strip()
                    if text:
                        other_paras.append(i)

            if not other_paras:
                print("FAIL: Component 3 — No non-Section5 paragraphs found")
            else:
                # Check that a majority of other paragraphs are editable
                editable_count = sum(1 for idx in other_paras if is_in_editable_range(idx))
                ratio = editable_count / len(other_paras)
                print(f"  INFO: {editable_count}/{len(other_paras)} non-Section5 paragraphs are editable ({ratio:.1%})")

                if ratio >= 0.8:
                    print(f"PASS: Component 3 — Other sections are editable ({editable_count}/{len(other_paras)} paragraphs) (0.30 pts)")
                    total_score += 0.30
                elif ratio >= 0.5:
                    partial = round(0.30 * ratio, 2)
                    print(f"PARTIAL: Component 3 — Only {ratio:.0%} of other sections editable ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 3 — Only {ratio:.0%} of other paragraphs are editable")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
