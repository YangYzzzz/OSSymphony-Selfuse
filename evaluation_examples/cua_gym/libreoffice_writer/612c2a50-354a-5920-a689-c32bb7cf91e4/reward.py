"""
Reward Script: Outline numbering for legal document
Task ID: writer_bs_081
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3) - Multilevel numbering definition exists
  Component 2 (0.3) - Level 1: uppercase Roman numerals with 'Article ' prefix
  Component 3 (0.2) - Level 2: Arabic numbers with 'Section ' prefix
  Component 4 (0.2) - Level 3: lowercase letters with '(' prefix and ')' suffix
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_081'

def verify_task(file_path):
    """
    Verify outline numbering configuration in legal document.
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
    w_ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    # Get numbering part
    try:
        numbering = doc.part.numbering_part._element
    except Exception as e:
        print(f"CRITICAL: No numbering part found: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all multilevel abstractNum definitions
    multilevel_abstracts = []
    for an in numbering.findall('.//w:abstractNum', ns):
        mlt = an.find('w:multiLevelType', ns)
        if mlt is not None and mlt.get(f'{{{w_ns}}}val') == 'multilevel':
            multilevel_abstracts.append(an)

    # Component 1: A multilevel numbering definition exists (0.3 points)
    # This is the core change — initial has NO multilevel abstractNum
    try:
        if len(multilevel_abstracts) > 0:
            print(f"PASS: Component 1 — Found {len(multilevel_abstracts)} multilevel abstractNum definition(s) (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 — No multilevel abstractNum definition found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if len(multilevel_abstracts) == 0:
        # No multilevel numbering at all, remaining checks cannot pass
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Use the first multilevel abstractNum for level checks
    ml_abstract = multilevel_abstracts[0]
    levels = {}
    for lvl in ml_abstract.findall('w:lvl', ns):
        ilvl = lvl.get(f'{{{w_ns}}}ilvl')
        fmt_el = lvl.find('w:numFmt', ns)
        txt_el = lvl.find('w:lvlText', ns)
        fmt = fmt_el.get(f'{{{w_ns}}}val') if fmt_el is not None else None
        txt = txt_el.get(f'{{{w_ns}}}val') if txt_el is not None else None
        levels[ilvl] = {'numFmt': fmt, 'lvlText': txt}

    # Component 2: Level 1 (ilvl=0) — uppercase Roman numerals with 'Article ' prefix (0.3 points)
    try:
        lvl0 = levels.get('0', {})
        fmt0 = lvl0.get('numFmt', '')
        txt0 = lvl0.get('lvlText', '')

        # Check numFmt is upperRoman
        fmt_ok = fmt0 == 'upperRoman'
        # Check lvlText contains 'Article' prefix with the %1 placeholder
        # Expected: "Article %1" (with space between Article and number)
        txt_ok = txt0 is not None and 'Article' in txt0 and '%1' in txt0

        if fmt_ok and txt_ok:
            print(f"PASS: Component 2 — Level 1: numFmt='{fmt0}', lvlText='{txt0}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Level 1: numFmt='{fmt0}' (expected 'upperRoman'), lvlText='{txt0}' (expected 'Article %1' pattern)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Level 2 (ilvl=1) — Arabic numbers with 'Section ' prefix (0.2 points)
    try:
        lvl1 = levels.get('1', {})
        fmt1 = lvl1.get('numFmt', '')
        txt1 = lvl1.get('lvlText', '')

        # Check numFmt is decimal (Arabic numbers)
        fmt_ok = fmt1 == 'decimal'
        # Check lvlText contains 'Section' prefix with the %2 placeholder
        txt_ok = txt1 is not None and 'Section' in txt1 and '%2' in txt1

        if fmt_ok and txt_ok:
            print(f"PASS: Component 3 — Level 2: numFmt='{fmt1}', lvlText='{txt1}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Level 2: numFmt='{fmt1}' (expected 'decimal'), lvlText='{txt1}' (expected 'Section %2' pattern)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Level 3 (ilvl=2) — lowercase letters with parentheses (0.2 points)
    try:
        lvl2 = levels.get('2', {})
        fmt2 = lvl2.get('numFmt', '')
        txt2 = lvl2.get('lvlText', '')

        # Check numFmt is lowerLetter
        fmt_ok = fmt2 == 'lowerLetter'
        # Check lvlText has parentheses pattern: "(%3)" or similar
        txt_ok = txt2 is not None and '(' in txt2 and ')' in txt2 and '%3' in txt2

        if fmt_ok and txt_ok:
            print(f"PASS: Component 4 — Level 3: numFmt='{fmt2}', lvlText='{txt2}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Level 3: numFmt='{fmt2}' (expected 'lowerLetter'), lvlText='{txt2}' (expected '(%3)' pattern)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
