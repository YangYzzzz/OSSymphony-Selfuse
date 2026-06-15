"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m giving Table 1 a minimalist look in LibreOffice Writer. Could you walk me through the steps to completely remove its borders and set the spacing to contents to exactly 0.20 cm on all sides?
Generated: 2025-09-10 15:02:27
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import zipfile
from lxml import etree


def verify_borders_no_borders(tbl, ns):
    """Return True only if every exterior & interior border is explicitly set to NIL."""
    borders = tbl.xpath('./w:tblPr/w:tblBorders', namespaces=ns)
    if not borders:
        print('✗ <tblBorders> element missing (borders likely default)')
        return False

    border_tags = ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']
    for tag in border_tags:
        elems = borders[0].xpath(f'w:{tag}', namespaces=ns)
        if not elems:
            print(f'✗ Border tag <{tag}> missing')
            return False
        val = elems[0].get(f'{{{ns["w"]}}}val')
        if val != 'nil':
            print(f'✗ Border {tag} is not nil (val={val})')
            return False
    print('✓ All borders set to nil (no borders)')
    return True


def twips_to_cm(twips):
    """Convert twips (1/20 pt) to centimetres."""
    return twips / 1440 * 2.54


def verify_spacing_0_20(tbl, ns, tolerance_twips=5):
    """Return True only if spacing-to-contents equals 0.20 cm (≈113 twips) on every side."""
    cellMar = tbl.xpath('./w:tblPr/w:tblCellMar', namespaces=ns)
    if not cellMar:
        print('✗ <tblCellMar> element missing (no cell margins defined)')
        return False

    expected_twips = 113  # 0.20 cm ≈ 113.386 twips
    ok = True
    for tag in ['top', 'bottom', 'left', 'right']:
        elems = cellMar[0].xpath(f'w:{tag}', namespaces=ns)
        if not elems:
            print(f'✗ Spacing element <{tag}> missing')
            ok = False
            continue
        w_val = elems[0].get(f'{{{ns["w"]}}}w')
        if w_val is None:
            print(f'✗ Spacing {tag} has no w attribute')
            ok = False
            continue
        try:
            w_int = int(w_val)
        except ValueError:
            print(f'✗ Spacing {tag} w value not integer: {w_val}')
            ok = False
            continue
        if abs(w_int - expected_twips) > tolerance_twips:
            print(f'✗ Spacing {tag} = {w_int} twips (expected {expected_twips}±{tolerance_twips})')
            ok = False
        else:
            print(f'✓ Spacing {tag} = {w_int} twips ({twips_to_cm(w_int):.2f} cm)')
    return ok


def verify_writer_table_minimalist(file_path):
    """Reward script for the task: borders removed & spacing-to-contents 0.20 cm."""
    score = 0.0
    max_score = 1.0

    if not os.path.exists(file_path):
        print(f'✗ File not found: {file_path}')
        print('REWARD: 0.0')
        return 0.0

    try:
        with zipfile.ZipFile(file_path) as z:
            if 'word/document.xml' not in z.namelist():
                print('✗ document.xml not found in DOCX')
                print('REWARD: 0.0')
                return 0.0
            xml_bytes = z.read('word/document.xml')

        root = etree.fromstring(xml_bytes)
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        tables = root.xpath('.//w:tbl', namespaces=ns)
        if not tables:
            print('✗ No tables found in document')
            print('REWARD: 0.0')
            return 0.0

        print(f'Found {len(tables)} table(s) in document')

        border_ok = False
        spacing_ok = False

        # Evaluate every table; award points only when requirements met
        for idx, tbl in enumerate(tables):
            print(f'--- Evaluating Table {idx + 1} ---')
            borders_good = verify_borders_no_borders(tbl, ns)
            spacing_good = verify_spacing_0_20(tbl, ns)

            # Capture best (first full-match stops further checks)
            if borders_good:
                border_ok = True
            if spacing_good:
                spacing_ok = True
            if borders_good and spacing_good:
                print(f'Table {idx + 1} satisfies all requirements')
                break

        # Progressive scoring
        if border_ok:
            score += 0.5
        if spacing_ok:
            score += 0.5

        final_score = min(score, max_score)
        print(f'Total score breakdown: {final_score}/{max_score}')
        print(f'REWARD: {final_score}')
        return final_score

    except Exception as e:
        print(f'✗ Error processing document: {e}')
        print('REWARD: 0.0')
        return 0.0


# ----------------------------
# Execute verification when run directly
# ----------------------------
if __name__ == "__main__":
    FILE_PATH = "/home/user/im_giving_table_1_a_minimalist_look_in_libreoffice_writer_could_you_walk_me_through_the_steps_to_com.docx"
    verify_writer_table_minimalist(FILE_PATH)
