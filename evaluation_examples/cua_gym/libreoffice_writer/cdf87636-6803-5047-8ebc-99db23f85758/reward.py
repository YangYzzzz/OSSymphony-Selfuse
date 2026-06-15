"""
Reward Script: Insert quadratic formula using equation editor
Task ID: writer_acad_026
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25) - Placeholder text removed from P9
  Component 2 (0.25) - oMathPara element present in the document
  Component 3 (0.25) - Fraction structure (numerator/denominator) with denominator containing "2a"
  Component 4 (0.25) - Correct quadratic formula elements: variables x, b, radical, plus-minus, superscript b^2, 4ac
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_026'


def persist_app_state(domain):
    """Save any unsaved edits in LibreOffice Writer."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that the quadratic formula was inserted as a Math equation.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from lxml import etree
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    math_ns = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}
    ws_ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = doc.element.body

    # Component 1: Placeholder text removed (0.25 points)
    # The initial doc has "[Insert quadratic formula here using the equation editor]" at P9.
    # After task completion, this placeholder must be gone.
    try:
        placeholder = "[Insert quadratic formula here using the equation editor]"
        full_text = " ".join(p.text for p in doc.paragraphs)
        if placeholder not in full_text:
            print(f"PASS: Component 1 -- Placeholder text removed (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- Placeholder text still present")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: oMathPara element exists in the document (0.25 points)
    # This checks that a Math equation object was inserted (not just plain text).
    try:
        omath_paras = body.findall('.//m:oMathPara', math_ns)
        omaths = body.findall('.//m:oMath', math_ns)
        if len(omath_paras) >= 1 or len(omaths) >= 1:
            print(f"PASS: Component 2 -- oMathPara/oMath found (count: oMathPara={len(omath_paras)}, oMath={len(omaths)}) (0.25 pts)")
            total_score += 0.25
        else:
            # Also check for OLE objects (w:object) as alternative equation embedding
            ole_objects = body.findall('.//w:object', ws_ns)
            if len(ole_objects) >= 1:
                print(f"PASS: Component 2 -- OLE math object found (count: {len(ole_objects)}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- No math equation objects found in document")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Fraction structure with denominator "2a" (0.25 points)
    # The quadratic formula has the form (...) / (2a). Check for m:f (fraction)
    # with m:den containing "2" and "a".
    try:
        fractions = body.findall('.//m:f', math_ns)
        fraction_found = False
        den_correct = False
        for frac in fractions:
            fraction_found = True
            den = frac.find('m:den', math_ns)
            if den is not None:
                # Collect all text in denominator
                den_texts = [t.text for t in den.iter('{http://schemas.openxmlformats.org/officeDocument/2006/math}t') if t.text]
                den_joined = ''.join(den_texts).strip()
                print(f"  DEBUG: Denominator text: {repr(den_joined)}")
                if '2' in den_joined and 'a' in den_joined:
                    den_correct = True

        if fraction_found and den_correct:
            print(f"PASS: Component 3 -- Fraction with denominator '2a' found (0.25 pts)")
            total_score += 0.25
        elif fraction_found:
            print(f"FAIL: Component 3 -- Fraction found but denominator does not contain '2a'")
        else:
            print(f"FAIL: Component 3 -- No fraction structure found in equation")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Correct quadratic formula elements (0.25 points)
    # Check for key structural elements: radical (m:rad), plus-minus sign,
    # superscript (m:sSup), and variable identifiers x, b.
    # Award partial sub-credit within this component.
    try:
        sub_checks = 0
        sub_total = 4

        # 4a: Radical (square root) present
        radicals = body.findall('.//m:rad', math_ns)
        if len(radicals) >= 1:
            print(f"  PASS: Component 4a -- Radical (sqrt) found")
            sub_checks += 1
        else:
            print(f"  FAIL: Component 4a -- No radical (sqrt) found")

        # 4b: Plus-minus sign (U+00B1) in equation
        all_math_text = []
        for omath in body.findall('.//m:oMath', math_ns):
            for t in omath.iter('{http://schemas.openxmlformats.org/officeDocument/2006/math}t'):
                if t.text:
                    all_math_text.append(t.text)
        math_text_joined = ''.join(all_math_text)
        print(f"  DEBUG: All math text: {repr(math_text_joined)}")

        if '\u00b1' in math_text_joined or '+-' in math_text_joined:
            print(f"  PASS: Component 4b -- Plus-minus sign found")
            sub_checks += 1
        else:
            print(f"  FAIL: Component 4b -- No plus-minus sign found")

        # 4c: Superscript (b^2) present
        ssups = body.findall('.//m:sSup', math_ns)
        if len(ssups) >= 1:
            # Verify it contains "2" as the superscript
            has_sq = False
            for ssup in ssups:
                sup_el = ssup.find('m:sup', math_ns)
                if sup_el is not None:
                    sup_texts = [t.text for t in sup_el.iter('{http://schemas.openxmlformats.org/officeDocument/2006/math}t') if t.text]
                    if '2' in ''.join(sup_texts):
                        has_sq = True
            if has_sq:
                print(f"  PASS: Component 4c -- Superscript with '2' (b squared) found")
                sub_checks += 1
            else:
                print(f"  FAIL: Component 4c -- Superscript found but no '2' exponent")
        else:
            print(f"  FAIL: Component 4c -- No superscript structure found")

        # 4d: Key variables present (x, b, a, c) and minus/negative signs
        has_x = 'x' in math_text_joined
        has_b = 'b' in math_text_joined
        has_a = 'a' in math_text_joined
        has_c = 'c' in math_text_joined
        has_4 = '4' in math_text_joined
        if has_x and has_b and has_a and has_c and has_4:
            print(f"  PASS: Component 4d -- Key variables x, b, a, c and constant 4 present")
            sub_checks += 1
        else:
            print(f"  FAIL: Component 4d -- Missing variables (x={has_x}, b={has_b}, a={has_a}, c={has_c}, 4={has_4})")

        comp4_score = 0.25 * (sub_checks / sub_total)
        if comp4_score > 0:
            print(f"PASS: Component 4 -- Quadratic formula elements ({sub_checks}/{sub_total} sub-checks) ({comp4_score:.4f} pts)")
            total_score += comp4_score
        else:
            print(f"FAIL: Component 4 -- No quadratic formula elements found")

    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(round(total_score, 4), 1.0)
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
