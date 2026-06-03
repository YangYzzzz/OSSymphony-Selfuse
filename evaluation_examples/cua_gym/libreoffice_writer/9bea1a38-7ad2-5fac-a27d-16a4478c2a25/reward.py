"""
Reward Script: Export thesis document as PDF/A format with embedded fonts
Task ID: writer_acad_076
Domain: libreoffice_writer
Scoring:
  Component 1 (0.2): PDF file exists at expected path
  Component 2 (0.2): PDF is valid and has pages matching the docx
  Component 3 (0.3): PDF/A conformance marker in XMP metadata
  Component 4 (0.3): All fonts are embedded in the PDF
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_076'

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    pdf_path = os.path.join(WORKDIR, f'{TASK_ID}.pdf')

    # Component 1: PDF file exists (0.2 points)
    # This is the primary task output — the exported PDF file.
    # FAILS on initial_env (no PDF exists), PASSES on golden_env.
    try:
        if os.path.isfile(pdf_path) and os.path.getsize(pdf_path) > 0:
            print(f"PASS: Component 1 — PDF file exists at {pdf_path} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — PDF file not found or empty at {pdf_path}")
            print(f"REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"REWARD: 0.0")
        return 0.0

    # Need pikepdf for remaining checks
    try:
        import pikepdf
    except ImportError:
        print("ERROR: pikepdf not available, installing...")
        os.system("pip3 install pikepdf -q")
        import pikepdf

    try:
        pdf = pikepdf.open(pdf_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {pdf_path}: {e}")
        # File exists but is not a valid PDF — give only the existence points
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: PDF is valid and has pages (0.2 points)
    # A properly exported thesis should have multiple pages.
    try:
        page_count = len(pdf.pages)
        if page_count > 0:
            print(f"PASS: Component 2 — PDF has {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — PDF has 0 pages")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PDF/A conformance in XMP metadata (0.3 points)
    # PDF/A requires specific XMP metadata: pdfaid:part and pdfaid:conformance
    # The task requires PDF/A-1a or PDF/A-2b format.
    try:
        pdfa_found = False
        pdfa_part = None
        pdfa_conformance = None

        # Check XMP metadata for PDF/A identifiers
        if hasattr(pdf, 'open_metadata'):
            with pdf.open_metadata() as meta:
                pdfa_ns = 'http://www.aiim.org/pdfa/ns/id/'
                part_key = f'{{{pdfa_ns}}}part'
                conf_key = f'{{{pdfa_ns}}}conformance'

                if part_key in meta:
                    pdfa_part = meta[part_key]
                if conf_key in meta:
                    pdfa_conformance = meta[conf_key]

                pdfa_found = (pdfa_part is not None)

        # Also check for OutputIntents (PDF/A requires sRGB output intent)
        root = pdf.Root
        has_output_intent = ('/OutputIntents' in root and len(root.OutputIntents) > 0)

        if pdfa_found and has_output_intent:
            print(f"PASS: Component 3 — PDF/A-{pdfa_part}{pdfa_conformance} conformance with OutputIntent (0.3 pts)")
            total_score += 0.3
        elif pdfa_found:
            # Has PDF/A metadata but no OutputIntent — partial
            print(f"PARTIAL: Component 3 — PDF/A-{pdfa_part}{pdfa_conformance} metadata found but no OutputIntent (0.15 pts)")
            total_score += 0.15
        elif has_output_intent:
            print(f"PARTIAL: Component 3 — OutputIntent found but no PDF/A XMP metadata (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 — No PDF/A conformance markers found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All fonts are embedded (0.3 points)
    # PDF/A requires all fonts to be embedded. Check every font in every page.
    try:
        all_fonts = []
        for page_num, page in enumerate(pdf.pages):
            resources = page.get('/Resources', {})
            font_dict = resources.get('/Font', {})
            if font_dict:
                for font_name, font_ref in font_dict.items():
                    font_obj = font_ref
                    base_font = str(font_obj.get('/BaseFont', 'unknown'))
                    has_descriptor = '/FontDescriptor' in font_obj
                    is_embedded = False
                    if has_descriptor:
                        desc = font_obj['/FontDescriptor']
                        is_embedded = any(k in desc for k in ['/FontFile', '/FontFile2', '/FontFile3'])
                    all_fonts.append((base_font, is_embedded))

        if len(all_fonts) == 0:
            print(f"FAIL: Component 4 — No fonts found in PDF")
        else:
            # Deduplicate by font name
            unique_fonts = {}
            for name, emb in all_fonts:
                if name not in unique_fonts:
                    unique_fonts[name] = emb

            embedded_count = sum(1 for emb in unique_fonts.values() if emb)
            total_fonts = len(unique_fonts)

            if embedded_count == total_fonts:
                print(f"PASS: Component 4 — All {total_fonts} fonts are embedded (0.3 pts)")
                total_score += 0.3
            else:
                # Partial credit based on proportion embedded
                ratio = embedded_count / total_fonts
                partial = round(0.3 * ratio, 2)
                if partial > 0:
                    print(f"PARTIAL: Component 4 — {embedded_count}/{total_fonts} fonts embedded ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 — No fonts embedded")

            # Print font details
            for name, emb in sorted(unique_fonts.items()):
                status = "embedded" if emb else "NOT embedded"
                print(f"  Font: {name} — {status}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    try:
        pdf.close()
    except Exception:
        pass

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state before verification
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


persist_app_state()
verify_task()
