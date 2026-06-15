"""
Reward Script: PDF/A-1b Archival Conversion
Task ID: pdf_aw_038
Domain: pdf
Scoring:
  - Component 1: Output file exists and is valid PDF with 20 pages (0.15)
  - Component 2: No JavaScript actions remain (0.20)
  - Component 3: No interactive form fields remain (0.20)
  - Component 4: XMP metadata contains PDF/A identification (part=1, conformance=B) (0.25)
  - Component 5: sRGB output intent present (0.20)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_038'
OUTPUT_FILE = os.path.join(WORKDIR, 'archive', 'quarterly_report_pdfa.pdf')
SOURCE_FILE = os.path.join(WORKDIR, 'archive', 'quarterly_report.pdf')


def verify_task(file_path):
    """
    Verify PDF/A-1b conversion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must be loadable as PDF with correct page count
    # Component 1: Output file is a valid PDF with 20 pages (0.15 points)
    try:
        import pikepdf
        pdf = pikepdf.open(file_path)
        page_count = len(pdf.pages)
        if page_count == 20:
            print(f"PASS: Component 1 — Valid PDF with {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 20 pages, found {page_count}")
        pdf.close()
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot open PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: No JavaScript actions remain (0.20 points)
    # Initial PDF has 2 JS actions; golden should have 0
    try:
        pdf = pikepdf.open(file_path)
        js_found = False

        # Check for /Names -> /JavaScript in catalog
        catalog = pdf.Root
        if '/Names' in catalog:
            names = catalog['/Names']
            if '/JavaScript' in names:
                js_found = True
                print("FAIL: Component 2 — /Names/JavaScript still present in catalog")

        # Check for /OpenAction with JavaScript
        if '/OpenAction' in catalog:
            oa = catalog['/OpenAction']
            oa_str = str(oa)
            if 'JavaScript' in oa_str or '/JS' in oa_str:
                js_found = True
                print("FAIL: Component 2 — /OpenAction contains JavaScript")

        # Scan all PDF objects for JavaScript action dictionaries
        js_action_count = 0
        for obj_id in pdf.objects:
            try:
                obj = pdf.objects[obj_id]
                if hasattr(obj, 'keys') and '/S' in obj:
                    if str(obj['/S']) == '/JavaScript':
                        js_action_count += 1
            except Exception:
                pass

        if js_action_count > 0:
            js_found = True
            print(f"FAIL: Component 2 — Found {js_action_count} JavaScript action objects")

        if not js_found:
            print("PASS: Component 2 — No JavaScript actions found (0.20 pts)")
            total_score += 0.20

        pdf.close()
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No interactive form fields remain (0.20 points)
    # Initial PDF has 4 form widgets; golden should have 0
    try:
        import fitz
        doc = fitz.open(file_path)
        widget_count = 0
        for i in range(doc.page_count):
            page = doc[i]
            widgets = list(page.widgets())
            widget_count += len(widgets)
        doc.close()

        # Also check via pikepdf for /AcroForm
        pdf = pikepdf.open(file_path)
        has_acroform = '/AcroForm' in pdf.Root
        acroform_fields = 0
        if has_acroform:
            acroform = pdf.Root['/AcroForm']
            if '/Fields' in acroform:
                acroform_fields = len(acroform['/Fields'])
        pdf.close()

        if widget_count == 0 and acroform_fields == 0:
            print(f"PASS: Component 3 — No form fields found (widgets={widget_count}, AcroForm fields={acroform_fields}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Found {widget_count} widgets, {acroform_fields} AcroForm fields")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: XMP metadata with PDF/A identification (0.25 points)
    # pdfaid:part=1, pdfaid:conformance=B
    try:
        pdf = pikepdf.open(file_path)
        xmp = pdf.open_metadata()
        xmp_str = str(xmp)

        has_part = False
        has_conformance = False

        # Check for pdfaid:part = 1
        if 'pdfaid:part' in xmp_str:
            # Extract the value
            import re
            part_match = re.search(r'pdfaid:part[^>]*>(\d+)<', xmp_str)
            if part_match and part_match.group(1) == '1':
                has_part = True

        # Check for pdfaid:conformance = B
        if 'pdfaid:conformance' in xmp_str:
            conf_match = re.search(r'pdfaid:conformance[^>]*>([A-Za-z]+)<', xmp_str)
            if conf_match and conf_match.group(1).upper() == 'B':
                has_conformance = True

        if has_part and has_conformance:
            print("PASS: Component 4 — XMP PDF/A-1b identification present (part=1, conformance=B) (0.25 pts)")
            total_score += 0.25
        elif has_part:
            print("PARTIAL: Component 4 — pdfaid:part=1 found but conformance=B missing (0.10 pts)")
            total_score += 0.10
        elif has_conformance:
            print("PARTIAL: Component 4 — pdfaid:conformance=B found but part=1 missing (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — No PDF/A identification in XMP metadata")

        pdf.close()
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: sRGB output intent present (0.20 points)
    try:
        pdf = pikepdf.open(file_path)
        catalog = pdf.Root

        if '/OutputIntents' in catalog:
            intents = catalog['/OutputIntents']
            srgb_found = False
            pdfa_intent_found = False
            for intent in intents:
                # Check for GTS_PDFA1 subtype
                s_val = str(intent.get('/S', ''))
                if 'GTS_PDFA1' in s_val:
                    pdfa_intent_found = True

                # Check for sRGB identifier
                oci = str(intent.get('/OutputConditionIdentifier', ''))
                info = str(intent.get('/Info', ''))
                if 'sRGB' in oci or 'sRGB' in info:
                    srgb_found = True

                # Check for ICC profile stream
                has_profile = '/DestOutputProfile' in intent

            if pdfa_intent_found and srgb_found:
                print("PASS: Component 5 — sRGB output intent with GTS_PDFA1 present (0.20 pts)")
                total_score += 0.20
            elif srgb_found:
                print("PARTIAL: Component 5 — sRGB output intent found but not GTS_PDFA1 type (0.10 pts)")
                total_score += 0.10
            elif pdfa_intent_found:
                print("PARTIAL: Component 5 — GTS_PDFA1 intent found but not sRGB (0.10 pts)")
                total_score += 0.10
            else:
                print("FAIL: Component 5 — OutputIntents present but no sRGB/GTS_PDFA1")
        else:
            print("FAIL: Component 5 — No OutputIntents in PDF catalog")

        pdf.close()
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point — test against canonical artifact path
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
