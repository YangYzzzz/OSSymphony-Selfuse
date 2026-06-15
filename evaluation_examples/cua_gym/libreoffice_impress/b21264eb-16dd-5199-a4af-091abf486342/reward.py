"""
FINAL REWARD SCRIPT - SUCCESS
Task: Quick question: In LibreOffice Impress, how do I switch the bullets on slide 95 to the 'Arrow' symbol and set their size to exactly 105%? I can’t find where that option lives in the Format menu.
Generated: 2025-09-10 23:24:30
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import zipfile
from lxml import etree


def verify_bullet_format(file_path: str) -> float:
    """Verify that slide 95 bullets are set to an arrow symbol and sized to 105%.

    The function awards up to 1.0 points:
        • 0.6 points for having ALL bullets on slide 95 use the arrow (→ / \u2192) symbol.
        • 0.4 points for having ALL bullet sizes on slide 95 set to exactly 105 %.
    Partial credit is awarded proportionally when only some bullets satisfy a criterion.
    """
    # Open XML namespace maps used in PPTX files
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }

    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0

    score = 0.0
    max_score = 1.0

    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            slide_name = 'ppt/slides/slide95.xml'  # zero-based index 94 ➜ slide95.xml
            if slide_name not in z.namelist():
                print("✗ slide95.xml not present – cannot verify")
                return 0.0

            slide_xml = z.read(slide_name)
            root = etree.fromstring(slide_xml)

            # --------------- Bullet CHARACTER verification ---------------
            bu_chars = root.xpath('//a:pPr/a:buChar', namespaces=ns)
            total_chars = len(bu_chars)
            arrow_chars = sum(
                1 for bu in bu_chars if bu.get('char') in {'\u2192', '→'}
            )
            print(f"Bullet characters using arrow: {arrow_chars}/{total_chars}")

            if total_chars:
                char_score = 0.6 * arrow_chars / total_chars
                score += char_score
                if arrow_chars == total_chars:
                    print("✓ All bullets use arrow symbol (+0.6)")
                elif arrow_chars:
                    print(f"✓ Partial arrow bullets (+{char_score:.2f})")
                else:
                    print("✗ No arrow bullets found (+0.00)")
            else:
                print("✗ No <a:buChar> elements found on slide 95")

            # --------------- Bullet SIZE verification ---------------
            bu_sizes = root.xpath('//a:pPr/a:buSzPct', namespaces=ns)
            total_sizes = len(bu_sizes)
            correct_sizes = sum(
                1
                for sz in bu_sizes
                if sz.get('val', '').rstrip('%') == '105'
            )
            print(f"Bullet size 105%: {correct_sizes}/{total_sizes}")

            if total_sizes:
                size_score = 0.4 * correct_sizes / total_sizes
                score += size_score
                if correct_sizes == total_sizes:
                    print("✓ All bullet sizes set to 105% (+0.4)")
                elif correct_sizes:
                    print(f"✓ Partial bullet sizing correct (+{size_score:.2f})")
                else:
                    print("✗ Bullet sizes not set to 105% (+0.00)")
            else:
                print("✗ No <a:buSzPct> elements found on slide 95")

    except Exception as e:
        print(f"✗ Error during verification: {e}")
        return 0.0

    final_score = min(score, max_score)
    print(f"Final score: {final_score}")
    return final_score


if __name__ == "__main__":
    # Path from task context – adjust if the evaluator places the file elsewhere
    FILE_PATH = "/home/user/quick_question_in_libreoffice_impress_how_do_i_switch_the_bullets_on_slide_95_to_the_arrow_symbol_an_golden.pptx"

    reward = verify_bullet_format(FILE_PATH)
    print(f"REWARD: {reward}")

