"""
Reward Script: Export contract as PDF with restricted permissions
Task ID: writer_legal_066
Domain: libreoffice_writer
Scoring:
  Component 1 (0.2): PDF file exists at expected path
  Component 2 (0.3): PDF is encrypted and owner password 'legal2024' works
  Component 3 (0.2): Printing is allowed (both lowres and highres)
  Component 4 (0.3): Copying (extract) is disabled AND all editing permissions are disabled
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_066'
PDF_PATH = f'{WORKDIR}/{TASK_ID}.pdf'
OWNER_PASSWORD = 'legal2024'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PDF file exists (0.2 points)
    # This FAILS on initial_env (no PDF) and PASSES on golden_env
    try:
        if os.path.isfile(PDF_PATH):
            file_size = os.path.getsize(PDF_PATH)
            if file_size > 1000:  # Must be a real PDF, not empty/trivial
                print(f"PASS: Component 1 — PDF exists at {PDF_PATH} ({file_size} bytes) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — PDF exists but too small ({file_size} bytes)")
        else:
            print(f"FAIL: Component 1 — PDF file not found at {PDF_PATH}")
            # No PDF means nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load PDF with pikepdf for permission checks
    try:
        import pikepdf
    except ImportError:
        print("CRITICAL: pikepdf not available on VM")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: PDF is encrypted and owner password 'legal2024' works (0.3 points)
    # This FAILS on initial_env (no PDF) and PASSES on golden_env
    try:
        # First try opening without password to check encryption exists
        pdf_no_pw = pikepdf.open(PDF_PATH)
        is_encrypted = pdf_no_pw.is_encrypted
        pdf_no_pw.close()

        if not is_encrypted:
            print(f"FAIL: Component 2 — PDF is not encrypted")
        else:
            # Now verify the owner password 'legal2024' works
            pw_check_err = None
            try:
                pdf_with_pw = pikepdf.open(PDF_PATH, password=OWNER_PASSWORD)
                pdf_with_pw.close()
            except pikepdf.PasswordError as pw_e:
                pw_check_err = str(pw_e)
            if pw_check_err is None:
                print(f"PASS: Component 2 — PDF is encrypted, owner password '{OWNER_PASSWORD}' accepted (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — PDF is encrypted but password '{OWNER_PASSWORD}' rejected")
    except pikepdf.PasswordError:
        # If we can't even open without password, it has a user password too
        # Try with the owner password
        try:
            pdf_with_pw = pikepdf.open(PDF_PATH, password=OWNER_PASSWORD)
            if pdf_with_pw.is_encrypted:
                print(f"PASS: Component 2 — PDF is encrypted (user+owner), password '{OWNER_PASSWORD}' accepted (0.3 pts)")
                total_score += 0.3
            pdf_with_pw.close()
        except pikepdf.PasswordError:
            print(f"FAIL: Component 2 — PDF has user password, '{OWNER_PASSWORD}' rejected")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # For components 3 and 4, we need the permissions from the PDF
    try:
        pdf = pikepdf.open(PDF_PATH, password=OWNER_PASSWORD)
        allow = pdf.allow
    except Exception as e:
        print(f"ERROR: Cannot read permissions — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    # Component 3: Printing is allowed (0.2 points)
    # Task says "allow printing" — both lowres and highres should be True
    try:
        print_low = allow.print_lowres
        print_high = allow.print_highres
        if print_low and print_high:
            print(f"PASS: Component 3 — Printing allowed (lowres={print_low}, highres={print_high}) (0.2 pts)")
            total_score += 0.2
        elif print_low or print_high:
            # Partial: at least one print permission
            print(f"PARTIAL: Component 3 — Partial printing (lowres={print_low}, highres={print_high}) (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 — Printing not allowed (lowres={print_low}, highres={print_high})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Copying (extract) disabled AND editing disabled (0.3 points)
    # Task says "disable copying text and editing"
    # extract=False means no text copying; all modify_*=False means no editing
    try:
        extract_disabled = not allow.extract
        modify_annotation_disabled = not allow.modify_annotation
        modify_form_disabled = not allow.modify_form
        modify_assembly_disabled = not allow.modify_assembly
        modify_other_disabled = not allow.modify_other

        all_edit_disabled = (modify_annotation_disabled and modify_form_disabled
                            and modify_assembly_disabled and modify_other_disabled)

        if extract_disabled and all_edit_disabled:
            total_score += 0.3
            print(f"PASS: Component 4 — Copying disabled (extract={allow.extract}), "
                  f"editing disabled (annotation={allow.modify_annotation}, form={allow.modify_form}, "
                  f"assembly={allow.modify_assembly}, other={allow.modify_other}) (0.3 pts)")
        else:
            partial = 0.0
            if extract_disabled:
                partial += 0.15
                print(f"PARTIAL: Component 4a — Copying disabled (extract={allow.extract}) (0.15 pts)")
            else:
                print(f"FAIL: Component 4a — Copying NOT disabled (extract={allow.extract})")
            if all_edit_disabled:
                partial += 0.15
                print(f"PARTIAL: Component 4b — Editing disabled (0.15 pts)")
            else:
                print(f"FAIL: Component 4b — Editing NOT fully disabled "
                      f"(annotation={allow.modify_annotation}, form={allow.modify_form}, "
                      f"assembly={allow.modify_assembly}, other={allow.modify_other})")
            if partial > 0:
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    try:
        pdf.close()
    except:
        pass

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
