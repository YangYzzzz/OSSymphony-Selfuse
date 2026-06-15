"""
Reward Script: Set up three-level heading numbering (1., 1.1., 1.1.1.)
Task ID: writer_tech_058
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Heading styles have numbering references (numPr present)
  Component 2 (0.25): Numbering definition is multilevel with decimal format
  Component 3 (0.25): Level text formats match '1.', '1.1.', '1.1.1.' patterns
  Component 4 (0.25): pStyle links connect correct heading levels
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_058'


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    import time
    os.environ["DISPLAY"] = ":0"
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
        from docx.oxml.ns import qn
    except ImportError as e:
        print(f"CRITICAL: Missing library: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    wval = qn('w:val')

    # ---------------------------------------------------------------
    # Component 1: Heading 1/2/3 styles have numPr (0.25 points)
    # This is the core change: numbering must be linked to heading styles.
    # In the initial doc, no heading style has numPr.
    # ---------------------------------------------------------------
    try:
        heading_num_info = {}  # style_name -> (numId, ilvl)
        styles_with_numpr = 0
        target_styles = {'Heading 1': 0, 'Heading 2': 1, 'Heading 3': 2}

        for style in doc.styles:
            if style.name in target_styles:
                style_elem = style.element
                pPr = style_elem.find(qn('w:pPr'))
                if pPr is not None:
                    numPr = pPr.find(qn('w:numPr'))
                    if numPr is not None:
                        numId_elem = numPr.find(qn('w:numId'))
                        ilvl_elem = numPr.find(qn('w:ilvl'))
                        numId_val = numId_elem.get(wval) if numId_elem is not None else None
                        ilvl_val = ilvl_elem.get(wval) if ilvl_elem is not None else None
                        heading_num_info[style.name] = (numId_val, ilvl_val)
                        styles_with_numpr += 1

        if styles_with_numpr == 3:
            print(f"PASS: Component 1 -- All 3 heading styles have numPr (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- Only {styles_with_numpr}/3 heading styles have numPr")
            # If no numbering at all, no point checking further
            if styles_with_numpr == 0:
                print(f"\nScore: {total_score}/1.0")
                print(f"REWARD: {total_score}")
                return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # ---------------------------------------------------------------
    # Component 2: All heading styles reference the SAME numId and use
    # correct ilvl (0=H1, 1=H2, 2=H3) (0.25 points)
    # ---------------------------------------------------------------
    try:
        num_ids = set()
        ilvl_correct = 0

        for style_name, expected_ilvl in target_styles.items():
            if style_name in heading_num_info:
                nid, il = heading_num_info[style_name]
                if nid is not None:
                    num_ids.add(nid)
                if il is not None and int(il) == expected_ilvl:
                    ilvl_correct += 1

        same_numid = len(num_ids) == 1
        all_ilvl_correct = ilvl_correct == 3

        if same_numid and all_ilvl_correct:
            print(f"PASS: Component 2 -- Same numId ({num_ids.pop()}) and correct ilvl mapping (0.25 pts)")
            total_score += 0.25
        else:
            details = []
            if not same_numid:
                details.append(f"numIds differ: {num_ids}")
            if not all_ilvl_correct:
                details.append(f"only {ilvl_correct}/3 ilvl values correct")
            print(f"FAIL: Component 2 -- {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ---------------------------------------------------------------
    # Component 3: The referenced abstract numbering definition uses
    # correct lvlText formats: '%1.', '%1.%2.', '%1.%2.%3.' and
    # decimal numFmt for levels 0-2 (0.25 points)
    # ---------------------------------------------------------------
    try:
        # Resolve numId -> abstractNumId from numbering part
        numbering_part = doc.part.numbering_part
        if numbering_part is None:
            print("FAIL: Component 3 -- No numbering part found")
        else:
            numbering_elem = numbering_part.element
            # Get the numId used by heading styles
            ref_numid = None
            for sn in target_styles:
                if sn in heading_num_info:
                    ref_numid = heading_num_info[sn][0]
                    break

            # Find num element and get abstractNumId
            abstract_num_id = None
            for num_elem in numbering_elem.findall('w:num', ns):
                if num_elem.get(qn('w:numId')) == ref_numid:
                    abst_ref = num_elem.find('w:abstractNumId', ns)
                    if abst_ref is not None:
                        abstract_num_id = abst_ref.get(wval)
                    break

            if abstract_num_id is None:
                print(f"FAIL: Component 3 -- Could not resolve abstractNumId for numId={ref_numid}")
            else:
                # Find the abstract numbering definition
                abstract_elem = None
                for abst in numbering_elem.findall('w:abstractNum', ns):
                    if abst.get(qn('w:abstractNumId')) == abstract_num_id:
                        abstract_elem = abst
                        break

                if abstract_elem is None:
                    print(f"FAIL: Component 3 -- abstractNum {abstract_num_id} not found")
                else:
                    expected_formats = {
                        '0': '%1.',
                        '1': '%1.%2.',
                        '2': '%1.%2.%3.',
                    }
                    format_checks = 0
                    for lvl in abstract_elem.findall('w:lvl', ns):
                        ilvl = lvl.get(qn('w:ilvl'))
                        if ilvl in expected_formats:
                            lvl_text = lvl.find('w:lvlText', ns)
                            num_fmt = lvl.find('w:numFmt', ns)

                            lvl_text_val = lvl_text.get(wval) if lvl_text is not None else None
                            num_fmt_val = num_fmt.get(wval) if num_fmt is not None else None

                            if lvl_text_val == expected_formats[ilvl] and num_fmt_val == 'decimal':
                                format_checks += 1
                            else:
                                print(f"  Level {ilvl}: lvlText={lvl_text_val} (expected {expected_formats[ilvl]}), numFmt={num_fmt_val}")

                    if format_checks == 3:
                        print(f"PASS: Component 3 -- Correct lvlText formats and decimal numFmt for all 3 levels (0.25 pts)")
                        total_score += 0.25
                    else:
                        print(f"FAIL: Component 3 -- Only {format_checks}/3 levels have correct format")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # ---------------------------------------------------------------
    # Component 4: The abstract numbering definition is multilevel type
    # and has pStyle links to Heading1/Heading2/Heading3 (0.25 points)
    # ---------------------------------------------------------------
    try:
        numbering_part = doc.part.numbering_part
        if numbering_part is None:
            print("FAIL: Component 4 -- No numbering part found")
        else:
            numbering_elem = numbering_part.element

            ref_numid = None
            for sn in target_styles:
                if sn in heading_num_info:
                    ref_numid = heading_num_info[sn][0]
                    break

            abstract_num_id = None
            for num_elem in numbering_elem.findall('w:num', ns):
                if num_elem.get(qn('w:numId')) == ref_numid:
                    abst_ref = num_elem.find('w:abstractNumId', ns)
                    if abst_ref is not None:
                        abstract_num_id = abst_ref.get(wval)
                    break

            abstract_elem = None
            for abst in numbering_elem.findall('w:abstractNum', ns):
                if abst.get(qn('w:abstractNumId')) == abstract_num_id:
                    abstract_elem = abst
                    break

            if abstract_elem is None:
                print("FAIL: Component 4 -- abstract numbering not found")
            else:
                # Check multiLevelType
                mlt = abstract_elem.find('w:multiLevelType', ns)
                is_multilevel = mlt is not None and mlt.get(wval) == 'multilevel'

                # Check pStyle links
                expected_pstyles = {'0': 'Heading1', '1': 'Heading2', '2': 'Heading3'}
                pstyle_checks = 0
                for lvl in abstract_elem.findall('w:lvl', ns):
                    ilvl = lvl.get(qn('w:ilvl'))
                    if ilvl in expected_pstyles:
                        pstyle = lvl.find('w:pStyle', ns)
                        pstyle_val = pstyle.get(wval) if pstyle is not None else None
                        if pstyle_val == expected_pstyles[ilvl]:
                            pstyle_checks += 1
                        else:
                            print(f"  Level {ilvl}: pStyle={pstyle_val} (expected {expected_pstyles[ilvl]})")

                if is_multilevel and pstyle_checks == 3:
                    print(f"PASS: Component 4 -- Multilevel type and correct pStyle links for all 3 levels (0.25 pts)")
                    total_score += 0.25
                else:
                    details = []
                    if not is_multilevel:
                        mlt_val = mlt.get(wval) if mlt is not None else 'missing'
                        details.append(f"multiLevelType={mlt_val} (expected multilevel)")
                    if pstyle_checks < 3:
                        details.append(f"only {pstyle_checks}/3 pStyle links correct")
                    print(f"FAIL: Component 4 -- {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
