"""
Reward Script: Three-column layout for middle section of Writer document
Task ID: writer_fs_031
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Document has 3+ sections with continuous section breaks
  Component 2 (0.3): Middle section uses 3 columns
  Component 3 (0.2): Column spacing in middle section is approximately 0.5cm
  Component 4 (0.2): Intro and Conclusion sections remain single-column
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_031'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse all sectPr elements from the document body to understand section layout
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    body = doc.element.body

    # Collect section info: each section has cols_num and type
    # In docx, sections are delimited by sectPr in paragraph pPr (for all but last)
    # and the final sectPr at body level
    sections_info = []

    for child in body:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag == "p":
            pPr = child.find("w:pPr", ns)
            if pPr is not None:
                sect_pr = pPr.find("w:sectPr", ns)
                if sect_pr is not None:
                    cols = sect_pr.findall("w:cols", ns)
                    num = 1
                    space = 0
                    sect_type = "default"
                    for c in cols:
                        wnum_key = "{" + ns["w"] + "}num"
                        wspace_key = "{" + ns["w"] + "}space"
                        num = int(c.get(wnum_key, "1"))
                        space = int(c.get(wspace_key, "0"))
                    type_el = sect_pr.findall("w:type", ns)
                    if type_el:
                        wval_key = "{" + ns["w"] + "}val"
                        sect_type = type_el[0].get(wval_key, "default")
                    sections_info.append({
                        "cols_num": num,
                        "cols_space": space,
                        "type": sect_type
                    })
        elif tag == "sectPr":
            # Final section
            cols = child.findall("w:cols", ns)
            num = 1
            space = 0
            sect_type = "default"
            for c in cols:
                wnum_key = "{" + ns["w"] + "}num"
                wspace_key = "{" + ns["w"] + "}space"
                num = int(c.get(wnum_key, "1"))
                space = int(c.get(wspace_key, "0"))
            type_el = child.findall("w:type", ns)
            if type_el:
                wval_key = "{" + ns["w"] + "}val"
                sect_type = type_el[0].get(wval_key, "default")
            sections_info.append({
                "cols_num": num,
                "cols_space": space,
                "type": sect_type
            })

    print(f"INFO: Found {len(sections_info)} section(s)")
    for i, si in enumerate(sections_info):
        print(f"  Section {i}: cols={si['cols_num']}, space={si['cols_space']}, type={si['type']}")

    # Component 1: Document has at least 3 sections (0.3 points)
    # Initial doc has only 1 section; golden has 3 with continuous breaks
    try:
        if len(sections_info) >= 3:
            # Also check that section breaks are continuous (not new page)
            continuous_count = sum(1 for s in sections_info if s["type"] == "continuous")
            if continuous_count >= 2:
                print(f"PASS: Component 1 -- {len(sections_info)} sections with {continuous_count} continuous breaks (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 -- {len(sections_info)} sections but only {continuous_count} continuous breaks (need >= 2)")
        else:
            print(f"FAIL: Component 1 -- Only {len(sections_info)} section(s), need at least 3")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: A middle section has exactly 3 columns (0.3 points)
    # The middle section (not first, not last) should have cols_num == 3
    try:
        if len(sections_info) >= 3:
            # Check any non-first, non-last section for 3 columns
            middle_sections = sections_info[1:-1]
            has_three_col = any(s["cols_num"] == 3 for s in middle_sections)
            if has_three_col:
                print(f"PASS: Component 2 -- Middle section has 3 columns (0.3 pts)")
                total_score += 0.3
            else:
                col_vals = [s["cols_num"] for s in middle_sections]
                print(f"FAIL: Component 2 -- Middle section(s) have columns: {col_vals}, expected 3")
        else:
            print(f"FAIL: Component 2 -- Not enough sections to have a middle section")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Column spacing in middle section is approximately 0.5cm (0.2 points)
    # 0.5cm = ~284 twips. Allow tolerance: 200-400 twips (roughly 0.35-0.7cm)
    try:
        if len(sections_info) >= 3:
            middle_sections = sections_info[1:-1]
            three_col_sections = [s for s in middle_sections if s["cols_num"] == 3]
            if three_col_sections:
                space = three_col_sections[0]["cols_space"]
                # 284 twips = 0.5cm. Allow 200-400 twips tolerance
                if 200 <= space <= 400:
                    print(f"PASS: Component 3 -- Column spacing {space} twips (~{space/567:.2f}cm) within tolerance (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 -- Column spacing {space} twips (~{space/567:.2f}cm), expected ~284 twips (~0.5cm)")
            else:
                print(f"FAIL: Component 3 -- No 3-column middle section found to check spacing")
        else:
            print(f"FAIL: Component 3 -- Not enough sections")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Introduction (first section) and Conclusion (last section) are single-column (0.2 points)
    try:
        if len(sections_info) >= 3:
            first_cols = sections_info[0]["cols_num"]
            last_cols = sections_info[-1]["cols_num"]
            if first_cols == 1 and last_cols == 1:
                print(f"PASS: Component 4 -- Intro (cols={first_cols}) and Conclusion (cols={last_cols}) are single-column (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 -- Intro cols={first_cols}, Conclusion cols={last_cols}; both should be 1")
        else:
            print(f"FAIL: Component 4 -- Not enough sections to verify intro/conclusion layout")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
