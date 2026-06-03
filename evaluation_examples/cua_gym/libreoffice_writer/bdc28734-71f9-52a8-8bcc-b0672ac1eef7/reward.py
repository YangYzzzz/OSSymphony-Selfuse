"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Writer my bullet points are sitting way too close to the page edge. For the whole list, I need each bullet to start exactly 0.80 cm in from the left margin. How do I set that indent across the board?
Generated: 2025-09-10 12:14:56
Status: success
Model: azure-o3
Total Steps: 11
"""

import os
import glob
import zipfile
import lxml.etree as ET

"""
Reward script for task:
"In LibreOffice Writer my bullet points are sitting way too close to the page edge. For the whole list, I need each bullet to start exactly 0.80 cm in from the left margin."  

Verification logic:
1. Locate the user-created DOCX file (the template/library files inside site-packages are ignored).
2. Parse word/document.xml from the DOCX package.
3. Identify paragraphs that are part of a bulleted or numbered list by checking:
   • presence of <w:numPr> (standard list paragraphs)
   • OR paragraph style names starting with "List" (e.g., ListBullet, ListParagraph)
   • OR first text run beginning with a bullet character (•)
4. For every bullet paragraph found, read its left indent value ( <w:ind w:left="…"> ).
5. Desired left indent = 0.80 cm → 0.80 × 567 twips ≈ 454 twips. A tolerance of ±10 twips (~0.018 cm) is allowed.
6. Progressive scoring:
   • 0.3 points if at least one bullet paragraph exists (task context addressed).
   • Up to 0.5 points proportional to the share of bullets whose left indent matches 0.80 cm within tolerance.
   • Extra 0.2 points if ALL bullet indents are both correct and identical (uniform across the board).
7. Final score is clamped to 1.0 and printed as "REWARD: X.X".
"""

def locate_relevant_docx() -> str | None:
    """Find the task-related .docx file, ignoring library templates."""
    candidates = glob.glob('/home/user/**/*.docx', recursive=True)
    # Prefer filenames that mention list/bullet/indent – most likely the task file
    priority = [f for f in candidates if any(k in f.lower() for k in (
        'bullet', 'list', 'indent')) and 'site-packages' not in f]
    if priority:
        return priority[0]
    # Otherwise, return the first non-library DOCX
    for f in candidates:
        if 'site-packages' not in f:
            return f
    return None

def is_bullet_paragraph(p, ns) -> bool:
    """Heuristically decide whether a paragraph is part of a list."""
    if p.find('.//w:numPr', namespaces=ns) is not None:
        return True
    pStyle = p.find('.//w:pPr/w:pStyle', namespaces=ns)
    if pStyle is not None:
        style_val = pStyle.get(f'{{{ns["w"]}}}val', '').lower()
        if style_val.startswith('list'):
            return True
    texts = p.xpath('.//w:t/text()', namespaces=ns)
    if texts and texts[0].strip().startswith('•'):
        return True
    return False

def verify_bullet_indent(file_path: str) -> float:
    print(f'Verifying bullet indent for file: {file_path}')
    score = 0.0
    try:
        with zipfile.ZipFile(file_path) as z:
            if 'word/document.xml' not in z.namelist():
                print('✗ document.xml missing in DOCX')
                return 0.0
            doc_root = ET.fromstring(z.read('word/document.xml'))
    except Exception as e:
        print(f'✗ Cannot load DOCX XML: {e}')
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    bullet_paras = [p for p in doc_root.xpath('.//w:p', namespaces=ns) if is_bullet_paragraph(p, ns)]
    print(f'Found {len(bullet_paras)} bullet paragraph(s)')

    if not bullet_paras:
        print('✗ No bullet paragraphs found – score 0')
        print('REWARD: 0.0')
        return 0.0

    score += 0.3  # bullets present – work on correct element

    desired_twips = int(round(0.8 * 567))  # 0.80 cm in twips
    tolerance = 10  # twips

    correct_count = 0
    left_values = []
    for p in bullet_paras:
        ind = p.find('.//w:pPr/w:ind', namespaces=ns)
        left_attr = ind.get(f'{{{ns["w"]}}}left') if ind is not None else None
        try:
            left_val = int(left_attr) if left_attr is not None else None
        except ValueError:
            left_val = None
        left_values.append(left_val)
        if left_val is not None and abs(left_val - desired_twips) <= tolerance:
            correct_count += 1

    indent_accuracy = correct_count / len(bullet_paras)
    print(f'Indent within 0.80 cm ±{tolerance} twips for {correct_count}/{len(bullet_paras)} bullet(s)')
    score += 0.5 * indent_accuracy  # up to 0.5 points for accuracy

    unique_vals = {v for v in left_values if v is not None}
    if len(unique_vals) == 1 and correct_count == len(bullet_paras):
        print('✓ All bullet indents are uniform and correct')
        score += 0.2  # uniformity bonus
    elif len(unique_vals) > 1:
        print('✗ Bullet indents not uniform')

    final_score = min(score, 1.0)
    print(f'Total score: {final_score}/1.0')
    print(f'REWARD: {final_score}')
    return final_score

# ------------------ RUN VERIFICATION ------------------

docx_path = locate_relevant_docx()
if not docx_path:
    print('✗ No relevant .docx file found')
    print('REWARD: 0.0')
else:
    verify_bullet_indent(docx_path)

