"""
Reward Script: Insert Pearson correlation coefficient equation
Task ID: writer_acad_060
Domain: libreoffice_writer
Scoring:
  C1 (0.25) - oMath equation element exists in the document
  C2 (0.10) - Placeholder text removed
  C3 (0.15) - Fraction (m:f) structure present in equation
  C4 (0.15) - Square root / radical (m:rad) present in equation
  C5 (0.15) - Summation (nary) operators present (>=4)
  C6 (0.10) - Superscript elements present (>=2) for squared terms
  C7 (0.10) - Core variables r, n, x, y all present in math text
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_060'
MATH_NS = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_writer")
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
    except ImportError:
        print("CRITICAL: python-docx not installed")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body

    # ---- Component 1: oMath equation exists in the document (0.25 points) ----
    try:
        omath_elements = body.findall('.//m:oMath', MATH_NS)
        omath_para_elements = body.findall('.//m:oMathPara', MATH_NS)
        omath_count = len(omath_elements)
        omath_para_count = len(omath_para_elements)

        if omath_count > 0 or omath_para_count > 0:
            print(f"PASS: Component 1 -- oMath equation found (oMath: {omath_count}, oMathPara: {omath_para_count}) (0.25 pts)")
            total_score += 0.25
        else:
            # Also check for OLE objects (alternative equation insertion method)
            w_ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            ole_objects = body.findall('.//w:object', w_ns)
            if len(ole_objects) > 0:
                print(f"PASS: Component 1 -- OLE equation object found ({len(ole_objects)} objects) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- No equation (oMath or OLE) found in document")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # ---- Component 2: Placeholder text removed (0.10 points) ----
    try:
        placeholder_found = False
        for para in doc.paragraphs:
            text = para.text.strip()
            if '[Equation' in text and 'inserted' in text.lower():
                placeholder_found = True
                break
            if '[Equation' in text and 'Pearson' in text:
                placeholder_found = True
                break

        if not placeholder_found:
            print(f"PASS: Component 2 -- Placeholder text removed (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 -- Placeholder text still present")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # For components 3-7, we need oMath elements to exist
    # Find the primary oMath element (could be inside oMathPara or standalone)
    omath_el = None
    try:
        omath_paras = body.findall('.//m:oMathPara', MATH_NS)
        if omath_paras:
            omath_el = omath_paras[0]
        else:
            omaths = body.findall('.//m:oMath', MATH_NS)
            if omaths:
                omath_el = omaths[0]
    except Exception:
        pass

    if omath_el is None:
        # Also try OLE — if OLE, we can't inspect internal structure
        # Give partial for C2 only, skip structural checks
        print("INFO: No oMath element found; structural checks (C3-C7) skipped")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # ---- Component 3: Fraction structure present (0.15 points) ----
    try:
        fracs = omath_el.findall('.//m:f', MATH_NS)
        if len(fracs) >= 1:
            print(f"PASS: Component 3 -- Fraction (m:f) found ({len(fracs)} fractions) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- No fraction (m:f) element found in equation")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # ---- Component 4: Square root / radical present (0.15 points) ----
    try:
        rads = omath_el.findall('.//m:rad', MATH_NS)
        if len(rads) >= 1:
            print(f"PASS: Component 4 -- Radical/sqrt (m:rad) found ({len(rads)} radicals) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- No radical/sqrt (m:rad) element found in equation")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # ---- Component 5: Summation operators present (>=4) (0.15 points) ----
    try:
        narys = omath_el.findall('.//m:nary', MATH_NS)
        # Count specifically summation nary operators (chr = summation symbol)
        sum_count = 0
        for nary in narys:
            nary_pr = nary.find('m:naryPr', MATH_NS)
            if nary_pr is not None:
                chr_el = nary_pr.find('m:chr', MATH_NS)
                if chr_el is not None:
                    val = chr_el.get('{http://schemas.openxmlformats.org/officeDocument/2006/math}val')
                    if val and ord(val) == 8721:  # summation symbol
                        sum_count += 1
                else:
                    # Default nary is integral; without chr, not summation
                    pass
            else:
                # No naryPr — could be default integral, skip
                pass

        # The Pearson formula has at least 5 summation symbols: sum(xy), sum(x), sum(y), sum(x^2), sum(y^2)
        if sum_count >= 4:
            print(f"PASS: Component 5 -- Summation operators found ({sum_count} summations, need >=4) (0.15 pts)")
            total_score += 0.15
        elif sum_count >= 2:
            print(f"PARTIAL: Component 5 -- Some summation operators found ({sum_count}, need >=4) (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 5 -- Insufficient summation operators ({sum_count}, need >=4)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # ---- Component 6: Superscript elements present (>=2) (0.10 points) ----
    try:
        sups = omath_el.findall('.//m:sSup', MATH_NS)
        if len(sups) >= 2:
            print(f"PASS: Component 6 -- Superscript elements found ({len(sups)} superscripts, need >=2) (0.10 pts)")
            total_score += 0.10
        elif len(sups) >= 1:
            print(f"PARTIAL: Component 6 -- Some superscripts found ({len(sups)}, need >=2) (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 6 -- No superscript (m:sSup) elements found")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # ---- Component 7: Core variables r, n, x, y present in math text (0.10 points) ----
    try:
        texts = omath_el.findall('.//m:t', MATH_NS)
        all_text = ''.join(t.text or '' for t in texts)

        required_vars = ['r', 'n', 'x', 'y']
        found_vars = [v for v in required_vars if v in all_text]
        missing_vars = [v for v in required_vars if v not in all_text]

        if len(found_vars) == len(required_vars):
            print(f"PASS: Component 7 -- All core variables found: {found_vars} (0.10 pts)")
            total_score += 0.10
        elif len(found_vars) >= 3:
            print(f"PARTIAL: Component 7 -- Most variables found: {found_vars}, missing: {missing_vars} (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 7 -- Missing variables: {missing_vars} (found: {found_vars})")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    final_score = min(total_score, 1.0)
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
