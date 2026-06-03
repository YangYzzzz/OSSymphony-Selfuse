"""
Reward Script: Create 'CodeBlock' paragraph style with specific formatting and apply to code blocks
Task ID: writer_tech_026
Domain: libreoffice_writer
Scoring:
  Component 1: CodeBlock style exists as paragraph style (0.2 pts)
  Component 2: CodeBlock style has correct font (Liberation Mono 9pt) (0.2 pts)
  Component 3: CodeBlock style has correct background shading #F5F5F5 (0.15 pts)
  Component 4: CodeBlock style has correct borders (thin black, all sides, ~0.3cm padding) (0.15 pts)
  Component 5: Both code paragraphs (4 and 8) use CodeBlock style (0.3 pts)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_026'


def persist_app_state(domain: str):
    """Save any unsaved changes in LibreOffice Writer."""
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
        from docx.oxml.ns import qn
    except ImportError as e:
        print(f"CRITICAL: Cannot import python-docx: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # =========================================================================
    # Component 1: CodeBlock style exists as a paragraph style (0.2 points)
    # =========================================================================
    codeblock_style = None
    try:
        para_styles = {s.name: s for s in doc.styles if s.type is not None and s.type.name == 'PARAGRAPH'}
        if 'CodeBlock' in para_styles:
            codeblock_style = para_styles['CodeBlock']
            print(f"PASS: Component 1 — 'CodeBlock' paragraph style exists (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — 'CodeBlock' style not found. Available: {list(para_styles.keys())[:10]}...")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no CodeBlock style, remaining checks that depend on it will fail gracefully
    # =========================================================================
    # Component 2: CodeBlock style has correct font (Liberation Mono 9pt) (0.2 points)
    # =========================================================================
    try:
        if codeblock_style is not None:
            style_elem = codeblock_style.element
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

            # Check font name from style rPr
            rfonts = style_elem.findall('.//w:rPr/w:rFonts', ns)
            font_ok = False
            for rf in rfonts:
                ascii_font = rf.get(qn('w:ascii'), '')
                hAnsi_font = rf.get(qn('w:hAnsi'), '')
                if 'Liberation Mono' in ascii_font or 'Liberation Mono' in hAnsi_font:
                    font_ok = True
                    break

            # Check font size (9pt = w:sz val="18" in half-points)
            sz_elems = style_elem.findall('.//w:rPr/w:sz', ns)
            size_ok = False
            for sz in sz_elems:
                sz_val = sz.get(qn('w:val'), '')
                if sz_val == '18':
                    size_ok = True
                    break

            if font_ok and size_ok:
                print(f"PASS: Component 2 — CodeBlock font is Liberation Mono 9pt (0.2 pts)")
                total_score += 0.2
            elif font_ok:
                print(f"PARTIAL: Component 2 — Font is Liberation Mono but size is wrong (sz={[s.get(qn('w:val')) for s in sz_elems]}) (0.1 pts)")
                total_score += 0.1
            elif size_ok:
                print(f"PARTIAL: Component 2 — Size is 9pt but font is wrong (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 2 — Font/size incorrect. font_ok={font_ok}, size_ok={size_ok}")
        else:
            print(f"FAIL: Component 2 — CodeBlock style does not exist, cannot check font")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: CodeBlock style has background shading #F5F5F5 (0.15 points)
    # =========================================================================
    try:
        if codeblock_style is not None:
            style_elem = codeblock_style.element
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

            shd_elems = style_elem.findall('.//w:pPr/w:shd', ns)
            shd_ok = False
            found_fill = None
            for shd in shd_elems:
                fill = shd.get(qn('w:fill'), '').upper()
                found_fill = fill
                if fill == 'F5F5F5':
                    shd_ok = True
                    break

            if shd_ok:
                print(f"PASS: Component 3 — Background shading is #F5F5F5 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Expected shading fill=F5F5F5, found: {found_fill}")
        else:
            print(f"FAIL: Component 3 — CodeBlock style does not exist, cannot check shading")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: CodeBlock style has thin black borders on all sides with padding (0.15 points)
    # =========================================================================
    try:
        if codeblock_style is not None:
            style_elem = codeblock_style.element
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

            pbdr = style_elem.findall('.//w:pPr/w:pBdr', ns)
            if pbdr:
                pbdr_elem = pbdr[0]
                sides = ['top', 'left', 'bottom', 'right']
                sides_ok = 0
                for side in sides:
                    side_elem = pbdr_elem.find(f'w:{side}', ns)
                    if side_elem is not None:
                        val = side_elem.get(qn('w:val'), '')
                        color = side_elem.get(qn('w:color'), '').upper()
                        sz = side_elem.get(qn('w:sz'), '')
                        # val="single" means thin line, color="000000" is black
                        # sz="4" is thin (half-point), space="6" is ~0.3cm padding
                        if val == 'single' and color in ('000000', 'AUTO'):
                            sides_ok += 1
                            print(f"  Border {side}: val={val}, color={color}, sz={sz}, space={side_elem.get(qn('w:space'), '')}")
                        else:
                            print(f"  Border {side}: unexpected val={val}, color={color}")
                    else:
                        print(f"  Border {side}: MISSING")

                if sides_ok == 4:
                    print(f"PASS: Component 4 — All 4 borders present, thin black (0.15 pts)")
                    total_score += 0.15
                elif sides_ok >= 2:
                    partial = round(0.15 * sides_ok / 4, 3)
                    print(f"PARTIAL: Component 4 — {sides_ok}/4 borders correct ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 — Only {sides_ok}/4 borders correct")
            else:
                print(f"FAIL: Component 4 — No paragraph border (pBdr) found in CodeBlock style")
        else:
            print(f"FAIL: Component 4 — CodeBlock style does not exist, cannot check borders")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================================
    # Component 5: Both code paragraphs use CodeBlock style (0.3 points)
    # =========================================================================
    try:
        # Identify code paragraphs by their content (contain code-like text)
        # From exploration: paragraphs containing "import csv" and "def compute_stats"
        code_markers = [
            ('import csv', 'first code block (import csv)'),
            ('def compute_stats', 'second code block (compute_stats)')
        ]

        code_paras_with_style = 0
        for marker_text, description in code_markers:
            found = False
            for p in doc.paragraphs:
                if marker_text in p.text:
                    found = True
                    style_name = p.style.name if p.style else 'None'
                    if style_name == 'CodeBlock':
                        code_paras_with_style += 1
                        print(f"  {description}: style=CodeBlock -- OK")
                    else:
                        print(f"  {description}: style={style_name} -- expected CodeBlock")
                    break
            if not found:
                print(f"  {description}: paragraph not found in document")

        if code_paras_with_style == 2:
            print(f"PASS: Component 5 — Both code paragraphs use CodeBlock style (0.3 pts)")
            total_score += 0.3
        elif code_paras_with_style == 1:
            print(f"PARTIAL: Component 5 — Only 1/2 code paragraphs use CodeBlock style (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — No code paragraphs use CodeBlock style")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
