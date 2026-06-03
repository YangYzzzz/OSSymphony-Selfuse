"""
Reward Script: Digital signature workflow for PDF signing
Task ID: pdf_gf3_022
Domain: pdf
Scoring:
  Component 1: sign_pdf.py script exists and is valid Python (0.15)
  Component 2: signed_contract.pdf exists (0.10)
  Component 3: PDF contains a digital signature field (0.25)
  Component 4: Signature signer name is 'Alice Johnson' (0.15)
  Component 5: Signature reason is 'Approved for release' (0.15)
  Component 6: Signature has a timestamp (0.10)
  Component 7: Last page text shows visible signature info (0.10)
"""

import os
import ast

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_022'

SCRIPT_PATH = os.path.join(WORKDIR, 'scripts', 'sign_pdf.py')
SIGNED_PDF_PATH = os.path.join(WORKDIR, 'contracts', 'signed_contract.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: sign_pdf.py script exists and is valid Python (0.15 points)
    try:
        if os.path.exists(SCRIPT_PATH):
            with open(SCRIPT_PATH, 'r') as f:
                script_content = f.read()
            # Verify it's valid Python by parsing the AST
            ast.parse(script_content)
            # Also check it references key elements
            has_crypto = 'cryptography' in script_content or 'x509' in script_content
            has_signing = 'pyhanko' in script_content or 'endesive' in script_content
            if has_crypto and has_signing and len(script_content) > 100:
                print(f"PASS: Component 1 — sign_pdf.py exists, valid Python, references cryptography and signing libs (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Script exists but missing expected library references (crypto={has_crypto}, signing={has_signing})")
        else:
            print(f"FAIL: Component 1 — {SCRIPT_PATH} does not exist")
    except SyntaxError as e:
        print(f"FAIL: Component 1 — sign_pdf.py has syntax error: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: signed_contract.pdf exists (0.10 points)
    # This is a gate for subsequent checks AND a scoring component because
    # the file does NOT exist in initial_env (task creates it)
    try:
        if os.path.exists(SIGNED_PDF_PATH):
            file_size = os.path.getsize(SIGNED_PDF_PATH)
            if file_size > 1000:
                print(f"PASS: Component 2 — signed_contract.pdf exists ({file_size} bytes) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — signed_contract.pdf too small ({file_size} bytes)")
        else:
            print(f"FAIL: Component 2 — {SIGNED_PDF_PATH} does not exist")
            # No signed PDF means components 3-7 will all fail
            final_score = min(total_score, 1.0)
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {final_score}")
            return final_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Load signed PDF for remaining checks
    PdfFileReader = None
    try:
        from pyhanko.pdf_utils.reader import PdfFileReader
    except ImportError:
        pass

    sig_name = None
    sig_reason = None
    sig_timestamp = None

    # Components 3-6: Check digital signature properties via pyhanko
    if PdfFileReader is not None:
        try:
            with open(SIGNED_PDF_PATH, 'rb') as f:
                reader = PdfFileReader(f)
                sigs = list(reader.embedded_signatures)

                # Component 3: PDF contains a digital signature (0.25 points)
                if len(sigs) > 0:
                    print(f"PASS: Component 3 — PDF has {len(sigs)} digital signature(s) (0.25 pts)")
                    total_score += 0.25
                    sig = sigs[0]
                    sig_obj = sig.sig_object

                    # Component 4: Signer name is 'Alice Johnson' (0.15 points)
                    try:
                        if '/Name' in sig_obj:
                            sig_name = str(sig_obj['/Name'])
                            if 'Alice Johnson' in sig_name:
                                print(f"PASS: Component 4 — Signer name is '{sig_name}' (0.15 pts)")
                                total_score += 0.15
                            else:
                                print(f"FAIL: Component 4 — Expected 'Alice Johnson', found '{sig_name}'")
                        else:
                            print(f"FAIL: Component 4 — No /Name field in signature object")
                    except Exception as e:
                        print(f"ERROR: Component 4 — {e}")

                    # Component 5: Reason is 'Approved for release' (0.15 points)
                    try:
                        if '/Reason' in sig_obj:
                            sig_reason = str(sig_obj['/Reason'])
                            if 'Approved for release' in sig_reason:
                                print(f"PASS: Component 5 — Reason is '{sig_reason}' (0.15 pts)")
                                total_score += 0.15
                            else:
                                print(f"FAIL: Component 5 — Expected 'Approved for release', found '{sig_reason}'")
                        else:
                            print(f"FAIL: Component 5 — No /Reason field in signature object")
                    except Exception as e:
                        print(f"ERROR: Component 5 — {e}")

                    # Component 6: Signature has a timestamp (0.10 points)
                    try:
                        if '/M' in sig_obj:
                            sig_timestamp = str(sig_obj['/M'])
                            if len(sig_timestamp) > 5:
                                print(f"PASS: Component 6 — Timestamp found: {sig_timestamp} (0.10 pts)")
                                total_score += 0.10
                            else:
                                print(f"FAIL: Component 6 — Timestamp too short: '{sig_timestamp}'")
                        else:
                            print(f"FAIL: Component 6 — No /M (timestamp) field in signature object")
                    except Exception as e:
                        print(f"ERROR: Component 6 — {e}")

                else:
                    print(f"FAIL: Component 3 — No digital signatures found in PDF")
                    print(f"FAIL: Component 4 — Skipped (no signature)")
                    print(f"FAIL: Component 5 — Skipped (no signature)")
                    print(f"FAIL: Component 6 — Skipped (no signature)")
        except Exception as e:
            print(f"ERROR: Components 3-6 — pyhanko reader error: {e}")
            # Fallback: try pymupdf widgets
            try:
                import pymupdf
                doc = pymupdf.open(SIGNED_PDF_PATH)
                last_page = doc[-1]
                widgets = list(last_page.widgets())
                sig_widgets = [w for w in widgets if w.field_type == 6]
                if len(sig_widgets) > 0:
                    print(f"PASS: Component 3 (fallback) — Found {len(sig_widgets)} signature widget(s) (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 (fallback) — No signature widgets found")
                doc.close()
            except Exception as e2:
                print(f"ERROR: Component 3 fallback — {e2}")
    else:
        # Fallback using pymupdf only
        try:
            import pymupdf
            doc = pymupdf.open(SIGNED_PDF_PATH)
            last_page = doc[-1]
            widgets = list(last_page.widgets())
            sig_widgets = [w for w in widgets if w.field_type == 6]
            if len(sig_widgets) > 0:
                print(f"PASS: Component 3 (pymupdf fallback) — Found {len(sig_widgets)} signature widget(s) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 (pymupdf fallback) — No signature widgets found")
            doc.close()
        except Exception as e:
            print(f"ERROR: Component 3 pymupdf fallback — {e}")

    # Component 7: Visible signature on last page shows key info (0.10 points)
    try:
        import pymupdf
        doc = pymupdf.open(SIGNED_PDF_PATH)
        last_page = doc[-1]
        text = last_page.get_text()
        has_name = 'Alice Johnson' in text
        has_reason = 'Approved for release' in text
        if has_name and has_reason:
            print(f"PASS: Component 7 — Last page text contains 'Alice Johnson' and 'Approved for release' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 — Last page missing visible signature text (name={has_name}, reason={has_reason})")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
