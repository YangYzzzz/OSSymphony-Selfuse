"""
Reward Script: Write a BASIC macro called 'ExportToPDF' that saves the current document as PDF
Task ID: writer_tm_088
Domain: libreoffice_writer
Scoring:
  Component 1 (0.20): ExportToPDF.xba file exists in LibreOffice Basic Standard library
  Component 2 (0.20): ExportToPDF is registered in script.xlb
  Component 3 (0.20): Macro defines 'Sub ExportToPDF()'
  Component 4 (0.20): Macro uses 'writer_pdf_Export' filter for PDF export
  Component 5 (0.20): Macro derives PDF path from document URL (changes extension to .pdf)
"""

import os
import re

# LibreOffice BASIC macro storage paths on the VM
BASIC_DIR = '/home/user/.config/libreoffice/4/user/basic/Standard'
XBA_FILE = os.path.join(BASIC_DIR, 'ExportToPDF.xba')
SCRIPT_XLB = os.path.join(BASIC_DIR, 'script.xlb')


def verify_task():
    """
    Verify that the ExportToPDF BASIC macro has been created correctly.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ExportToPDF.xba file exists (0.2 points)
    try:
        if os.path.isfile(XBA_FILE):
            file_size = os.path.getsize(XBA_FILE)
            if file_size > 50:  # Must have real content, not just empty XML
                print(f"PASS: Component 1 — ExportToPDF.xba exists ({file_size} bytes) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — ExportToPDF.xba exists but too small ({file_size} bytes)")
        else:
            print(f"FAIL: Component 1 — ExportToPDF.xba not found at {XBA_FILE}")
            # If macro file doesn't exist, nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ExportToPDF is registered in script.xlb (0.2 points)
    try:
        if os.path.isfile(SCRIPT_XLB):
            with open(SCRIPT_XLB, 'r') as f:
                xlb_content = f.read()
            # Check that script.xlb contains a library:element entry for ExportToPDF
            if 'library:name="ExportToPDF"' in xlb_content:
                print(f"PASS: Component 2 — ExportToPDF registered in script.xlb (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — ExportToPDF not found in script.xlb. Contents: {xlb_content[:200]}")
        else:
            print(f"FAIL: Component 2 — script.xlb not found at {SCRIPT_XLB}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Read the macro content for remaining checks
    try:
        with open(XBA_FILE, 'r') as f:
            macro_content = f.read()
        # Extract just the BASIC code from XML (content inside the script:module tags)
        macro_text = macro_content
    except Exception as e:
        print(f"ERROR: Could not read macro file: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: Macro defines 'Sub ExportToPDF()' (0.2 points)
    try:
        # Look for Sub ExportToPDF declaration (case-insensitive, allow optional params)
        if re.search(r'Sub\s+ExportToPDF\s*\(', macro_text, re.IGNORECASE):
            print(f"PASS: Component 3 — Macro defines 'Sub ExportToPDF()' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — 'Sub ExportToPDF()' declaration not found in macro")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Macro uses 'writer_pdf_Export' filter (0.2 points)
    try:
        # The filter name can appear in various encoded forms in the XML
        # In raw XBA XML, quotes are encoded as &quot;
        if 'writer_pdf_Export' in macro_text or 'writer_pdf_export' in macro_text.lower():
            print(f"PASS: Component 4 — Macro uses 'writer_pdf_Export' filter (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — 'writer_pdf_Export' filter not found in macro. "
                  f"Searched content length: {len(macro_text)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Macro derives PDF path from document URL (0.2 points)
    # The macro should get the document URL and change the extension to .pdf
    try:
        # Check for evidence of URL-based path derivation:
        # - getURL() or URL property usage
        # - Extension change logic (.pdf)
        has_url_access = bool(re.search(r'getURL|\.URL\b|oDoc\.getURL|ThisComponent\.getURL|ThisComponent\.URL', macro_text, re.IGNORECASE))
        has_pdf_extension = bool(re.search(r'\.pdf', macro_text, re.IGNORECASE))
        has_store_method = bool(re.search(r'storeToURL|storeAsURL|StoreToURL', macro_text, re.IGNORECASE))

        if has_url_access and has_pdf_extension and has_store_method:
            print(f"PASS: Component 5 — Macro derives PDF path from document URL and exports (0.2 pts)")
            total_score += 0.2
        else:
            missing = []
            if not has_url_access:
                missing.append("getURL()/URL access")
            if not has_pdf_extension:
                missing.append(".pdf extension reference")
            if not has_store_method:
                missing.append("storeToURL() call")
            print(f"FAIL: Component 5 — Missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
