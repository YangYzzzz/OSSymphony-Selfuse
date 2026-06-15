"""
Reward Script: Apply SEALED watermark + encrypt court record PDF
Task ID: pdf_legal_095
Domain: pdf
Scoring:
  Component 1 (0.25): File is encrypted, user password 'sealed_2024!' works
  Component 2 (0.15): Owner password 'court_admin_2024!' works
  Component 3 (0.25): All permissions restricted (no print, no edit, no copy, no annotate, no form, no assembly)
  Component 4 (0.35): 'SEALED' watermark present on all 40 pages (large font, dark red)
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_095'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'sealed', 'court_record_sealed.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist (not a scoring component)
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File is encrypted and user password works (0.25 points)
    try:
        import fitz
        doc = fitz.open(file_path)
        is_enc = doc.is_encrypted
        if is_enc:
            auth_result = doc.authenticate('sealed_2024!')
            if auth_result > 0:
                print(f"PASS: Component 1 — File is encrypted, user password 'sealed_2024!' accepted (auth={auth_result}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — File is encrypted but user password 'sealed_2024!' rejected (auth={auth_result})")
        else:
            print(f"FAIL: Component 1 — File is NOT encrypted")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Owner password works (0.15 points)
    try:
        import fitz
        doc = fitz.open(file_path)
        if doc.is_encrypted:
            auth_result = doc.authenticate('court_admin_2024!')
            # auth > 2 means owner-level access
            if auth_result >= 4:
                print(f"PASS: Component 2 — Owner password 'court_admin_2024!' accepted with owner privileges (auth={auth_result}) (0.15 pts)")
                total_score += 0.15
            elif auth_result > 0:
                print(f"PARTIAL: Component 2 — Owner password accepted but only user-level access (auth={auth_result})")
                total_score += 0.05
            else:
                print(f"FAIL: Component 2 — Owner password 'court_admin_2024!' rejected (auth={auth_result})")
        else:
            print(f"FAIL: Component 2 — File is not encrypted, cannot test owner password")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Permissions restricted — only viewing allowed (0.25 points)
    try:
        import pikepdf
        pdf = pikepdf.open(file_path, password='court_admin_2024!')
        allow = pdf.allow

        # All these should be False for "restricting all permissions except viewing"
        expected_restrictions = {
            'extract': False,
            'modify_annotation': False,
            'modify_assembly': False,
            'modify_form': False,
            'modify_other': False,
            'print_lowres': False,
            'print_highres': False,
        }

        passed_count = 0
        total_checks = len(expected_restrictions)
        for perm_name, expected_val in expected_restrictions.items():
            actual_val = getattr(allow, perm_name, None)
            if actual_val == expected_val:
                passed_count += 1
            else:
                print(f"  FAIL: Permission '{perm_name}' expected {expected_val}, got {actual_val}")

        if passed_count == total_checks:
            print(f"PASS: Component 3 — All {total_checks} permissions correctly restricted (0.25 pts)")
            total_score += 0.25
        elif passed_count >= total_checks - 2:
            partial = round(0.25 * (passed_count / total_checks), 2)
            print(f"PARTIAL: Component 3 — {passed_count}/{total_checks} permissions correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {passed_count}/{total_checks} permissions correct")

        pdf.close()
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: SEALED watermark on all 40 pages (large dark red text) (0.35 points)
    try:
        import fitz
        doc = fitz.open(file_path)
        if doc.is_encrypted:
            doc.authenticate('sealed_2024!')

        total_pages = len(doc)
        watermark_pages = 0

        for i in range(total_pages):
            page = doc[i]
            blocks = page.get_text('dict')['blocks']
            page_has_watermark = False
            for b in blocks:
                if b['type'] == 0:  # text block
                    for line in b['lines']:
                        for span in line['spans']:
                            txt = span['text'].strip()
                            sz = span['size']
                            color_int = span['color']
                            # Watermark: standalone "SEALED" text, large font (>40pt)
                            if txt == 'SEALED' and sz > 40:
                                # Check dark red color: extract RGB components
                                r = (color_int >> 16) & 0xFF
                                g = (color_int >> 8) & 0xFF
                                b_val = color_int & 0xFF
                                # Dark red: high R, low G, low B
                                if r > 100 and g < 50 and b_val < 50:
                                    page_has_watermark = True
                                    break
                        if page_has_watermark:
                            break
                if page_has_watermark:
                    break
            if page_has_watermark:
                watermark_pages += 1

        doc.close()

        if total_pages == 40 and watermark_pages == 40:
            print(f"PASS: Component 4 — SEALED watermark found on all {watermark_pages}/{total_pages} pages (0.35 pts)")
            total_score += 0.35
        elif watermark_pages > 0:
            # Partial credit proportional to pages with watermark
            ratio = watermark_pages / max(total_pages, 40)
            partial = round(0.35 * ratio, 2)
            print(f"PARTIAL: Component 4 — SEALED watermark found on {watermark_pages}/{total_pages} pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No SEALED watermark found on any page (checked {total_pages} pages)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
