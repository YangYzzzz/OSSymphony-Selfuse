"""
Reward Script: PDF watermark + encryption verification
Task ID: pdf_pw_012
Domain: pdf
Scoring:
  Component 1 (0.25): File exists, is encrypted, user password 'view2026' opens it
  Component 2 (0.20): Owner password 'owner2026' grants full access
  Component 3 (0.20): Permissions — only printing allowed, others forbidden
  Component 4 (0.20): CONFIDENTIAL watermark on all 16 pages
  Component 5 (0.15): Watermark text is red colored
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_012'
TARGET_FILE = os.path.join(WORKDIR, 'Documents', 'strategy_doc_secured.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------
    # Component 1: File is encrypted and user password works (0.25 pts)
    # ---------------------------------------------------------------
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        is_enc = doc.is_encrypted
        if not is_enc:
            print("FAIL: Component 1 — File is NOT encrypted")
            doc.close()
            # No point continuing if not encrypted
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        auth_result = doc.authenticate('view2026')
        doc.close()
        if auth_result > 0:
            print(f"PASS: Component 1 — File is encrypted and user password 'view2026' works (auth={auth_result}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — User password 'view2026' did not authenticate (auth={auth_result})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: Owner password works (0.20 pts)
    # ---------------------------------------------------------------
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        auth_result = doc.authenticate('owner2026')
        doc.close()
        # auth result of 4 or 6 indicates owner-level access
        if auth_result >= 4:
            print(f"PASS: Component 2 — Owner password 'owner2026' grants full access (auth={auth_result}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Owner password 'owner2026' did not grant owner-level access (auth={auth_result})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: Permissions — only printing allowed (0.20 pts)
    # ---------------------------------------------------------------
    try:
        import pikepdf
        pdf = pikepdf.open(file_path, password='owner2026')
        allow = pdf.allow
        details = []
        perm_failures = 0

        # Printing must be allowed
        if allow.print_lowres and allow.print_highres:
            details.append("print=OK")
        else:
            perm_failures += 1
            details.append(f"print_lowres={allow.print_lowres}, print_highres={allow.print_highres} (expected True)")

        # Modification must be forbidden
        if not allow.modify_other:
            details.append("modify_other=OK(False)")
        else:
            perm_failures += 1
            details.append(f"modify_other={allow.modify_other} (expected False)")

        # Extract must be forbidden
        if not allow.extract:
            details.append("extract=OK(False)")
        else:
            perm_failures += 1
            details.append(f"extract={allow.extract} (expected False)")

        # Form and annotation modification forbidden
        if not allow.modify_form:
            details.append("modify_form=OK(False)")
        else:
            perm_failures += 1
            details.append(f"modify_form={allow.modify_form} (expected False)")

        if not allow.modify_annotation:
            details.append("modify_annotation=OK(False)")
        else:
            perm_failures += 1
            details.append(f"modify_annotation={allow.modify_annotation} (expected False)")

        pdf.close()

        if perm_failures == 0:
            print(f"PASS: Component 3 — Permissions correct: {', '.join(details)} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Permission issues: {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: CONFIDENTIAL watermark on all 16 pages (0.20 pts)
    # ---------------------------------------------------------------
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        doc.authenticate('view2026')
        page_count = len(doc)
        watermarked_count = 0

        for i in range(page_count):
            text = doc[i].get_text('text')
            if 'CONFIDENTIAL' in text:
                watermarked_count += 1

        doc.close()

        if page_count >= 16 and watermarked_count == page_count:
            print(f"PASS: Component 4 — CONFIDENTIAL watermark on all {watermarked_count}/{page_count} pages (0.20 pts)")
            total_score += 0.20
        elif watermarked_count > 0:
            # Partial credit: proportion of pages watermarked
            if watermarked_count > 0:
                partial = 0.20 * (watermarked_count / max(page_count, 16))
                print(f"PARTIAL: Component 4 — CONFIDENTIAL on {watermarked_count}/{page_count} pages ({partial:.2f} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 4 — No CONFIDENTIAL watermark found on any page (0/{page_count})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---------------------------------------------------------------
    # Component 5: Watermark is red colored (0.15 pts)
    # ---------------------------------------------------------------
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        doc.authenticate('view2026')

        # Check the first page for watermark color
        watermark_color_rgb = None
        data = doc[0].get_text('dict')
        for block in data['blocks']:
            if block.get('type') != 0:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    if 'CONFIDENTIAL' in span.get('text', ''):
                        color_int = span.get('color', 0)
                        r = (color_int >> 16) & 0xFF
                        g = (color_int >> 8) & 0xFF
                        b = color_int & 0xFF
                        watermark_color_rgb = (r, g, b)
                        break

        doc.close()

        # Red means high R, low G, low B
        if watermark_color_rgb and watermark_color_rgb[0] >= 200 and watermark_color_rgb[1] <= 50 and watermark_color_rgb[2] <= 50:
            print(f"PASS: Component 5 — Watermark is red (RGB={watermark_color_rgb}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Watermark color is {watermark_color_rgb}, expected red")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)
