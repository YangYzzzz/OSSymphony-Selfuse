"""
Reward Script: Configure PDF export with security permissions
Task ID: impress_el_025
Domain: libreoffice_impress
Scoring:
  Component 1 — PDF file exists (0.15)
  Component 2 — PDF is encrypted with permissions password (0.20)
  Component 3 — Printing is NOT permitted (0.25)
  Component 4 — Content copying is NOT permitted (0.25)
  Component 5 — Accessibility/screen reading IS permitted (0.15)
"""

import os
import glob

WORKDIR = '/home/user'
TASK_ID = 'impress_el_025'


def verify_task():
    """
    Verify PDF export with correct security settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find the PDF file - check expected path first, then search for any PDF
    pdf_path = os.path.join(WORKDIR, f'{TASK_ID}.pdf')
    if not os.path.exists(pdf_path):
        # Search for any PDF in WORKDIR
        pdfs = glob.glob(os.path.join(WORKDIR, '*.pdf'))
        if pdfs:
            pdf_path = pdfs[0]
            print(f"INFO: Using found PDF: {pdf_path}")
        else:
            # Also check common export locations
            for subdir in ['Desktop', 'Documents', 'Downloads']:
                pdfs = glob.glob(os.path.join(WORKDIR, subdir, '*.pdf'))
                if pdfs:
                    pdf_path = pdfs[0]
                    print(f"INFO: Using found PDF: {pdf_path}")
                    break

    # Component 1: PDF file exists (0.15 points)
    # This is a task-introduced change — no PDF exists in initial_env
    try:
        if os.path.exists(pdf_path) and pdf_path.endswith('.pdf'):
            file_size = os.path.getsize(pdf_path)
            if file_size > 0:
                print(f"PASS: Component 1 — PDF file exists at {pdf_path}, size={file_size} bytes (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — PDF file exists but is empty")
                print("REWARD: 0.0")
                return 0.0
        else:
            print(f"FAIL: Component 1 — No PDF file found in {WORKDIR}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load PDF with pikepdf
    try:
        import pikepdf
        pdf = pikepdf.open(pdf_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {pdf_path}: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: PDF is encrypted with permissions password (0.20 points)
    try:
        if pdf.is_encrypted:
            enc = pdf.encryption
            # R >= 4 and V >= 4 indicate proper encryption (RC4 128-bit or AES)
            if enc.R >= 4 and enc.V >= 4:
                print(f"PASS: Component 2 — PDF is encrypted (R={enc.R}, V={enc.V}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — PDF encrypted but weak (R={enc.R}, V={enc.V})")
        else:
            print(f"FAIL: Component 2 — PDF is NOT encrypted (no permissions password set)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Printing is NOT permitted (0.25 points)
    try:
        if pdf.is_encrypted:
            print_lowres = pdf.allow.print_lowres
            print_highres = pdf.allow.print_highres
            if not print_lowres and not print_highres:
                print(f"PASS: Component 3 — Printing disabled (lowres={print_lowres}, highres={print_highres}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Printing still allowed (lowres={print_lowres}, highres={print_highres})")
        else:
            print(f"FAIL: Component 3 — No encryption, cannot check print permissions")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Content copying/extraction is NOT permitted (0.25 points)
    try:
        if pdf.is_encrypted:
            extract_allowed = pdf.allow.extract
            if not extract_allowed:
                print(f"PASS: Component 4 — Content copying disabled (extract={extract_allowed}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — Content copying still allowed (extract={extract_allowed})")
        else:
            print(f"FAIL: Component 4 — No encryption, cannot check copy permissions")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Accessibility/screen reading IS permitted (0.15 points)
    try:
        if pdf.is_encrypted:
            accessibility = pdf.allow.accessibility
            if accessibility:
                print(f"PASS: Component 5 — Accessibility enabled (accessibility={accessibility}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — Accessibility NOT enabled (accessibility={accessibility})")
        else:
            print(f"FAIL: Component 5 — No encryption, cannot check accessibility permissions")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    pdf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
