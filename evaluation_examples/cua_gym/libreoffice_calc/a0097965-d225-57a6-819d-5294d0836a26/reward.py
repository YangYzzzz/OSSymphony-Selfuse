"""
Reward Script: Configure PDF export with bookmarks from sheet names and 100% zoom level
Task ID: calc_gsi_054
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): PDF has bookmarks matching all 4 sheet names
  Component 2 (0.25): PDF OpenAction sets zoom to 100% (factor 1.0)
  Component 3 (0.25): Bookmarks point to correct pages (each sheet starts on a different page)
  Component 4 (0.15): PDF has the Outlines catalog entry and correct bookmark count
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_054'

EXPECTED_SHEET_NAMES = ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025']


def verify_task(pdf_path):
    """
    Verify PDF export with bookmarks and zoom settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: PDF file must exist and be loadable
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {pdf_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(doc) == 0:
        print("CRITICAL: PDF has no pages")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF has bookmarks matching all 4 sheet names (0.35 points)
    try:
        toc = doc.get_toc()  # list of [level, title, page_number]
        bookmark_titles = [entry[1] for entry in toc]
        matched_count = 0
        for name in EXPECTED_SHEET_NAMES:
            if name in bookmark_titles:
                matched_count += 1
                print(f"  FOUND bookmark: '{name}'")
            else:
                print(f"  MISSING bookmark: '{name}'")

        if matched_count == len(EXPECTED_SHEET_NAMES):
            print(f"PASS: Component 1 — All {len(EXPECTED_SHEET_NAMES)} sheet bookmarks found (0.35 pts)")
            total_score += 0.35
        elif matched_count > 0:
            partial = 0.35 * (matched_count / len(EXPECTED_SHEET_NAMES))
            print(f"PARTIAL: Component 1 — {matched_count}/{len(EXPECTED_SHEET_NAMES)} bookmarks found ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No sheet bookmarks found. TOC: {toc}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: PDF OpenAction sets zoom to 100% (0.25 points)
    # OpenAction should be [page_ref /XYZ left top zoom] where zoom=1 means 100%
    try:
        # Find the catalog xref
        catalog_xref = None
        xref_count = doc.xref_length()
        for xref in range(1, xref_count):
            try:
                t = doc.xref_get_key(xref, 'Type')
                if t[1] == '/Catalog':
                    catalog_xref = xref
                    break
            except:
                continue

        if catalog_xref is None:
            print("FAIL: Component 2 — Cannot find PDF catalog")
        else:
            oa = doc.xref_get_key(catalog_xref, 'OpenAction')
            if oa[0] == 'null' or oa[1] is None:
                print("FAIL: Component 2 — No OpenAction defined in catalog")
            else:
                oa_str = oa[1]
                print(f"  OpenAction raw: {oa_str}")
                # Parse the zoom factor from the OpenAction array
                # Format: [page_ref /XYZ left top zoom]
                # zoom=1 means 100%, zoom=0.5 means 50%, etc.
                # The last number in the array is the zoom factor
                if '/XYZ' in oa_str:
                    # Extract the last number (zoom factor)
                    # Pattern like "[1 0 R/XYZ null null 1]" or "[1 0 R /XYZ 0 0 1.0]"
                    parts = oa_str.replace('[', '').replace(']', '').strip().split()
                    # Find /XYZ and get the zoom value (3rd param after /XYZ)
                    xyz_idx = None
                    for i, p in enumerate(parts):
                        if '/XYZ' in p:
                            xyz_idx = i
                            break
                    if xyz_idx is not None:
                        # The zoom is the 3rd value after /XYZ (left, top, zoom)
                        # But /XYZ might be concatenated with the page ref
                        remaining = parts[xyz_idx:]
                        # Extract numeric values after /XYZ
                        zoom_candidates = []
                        for p in remaining:
                            p_clean = p.replace('/XYZ', '').strip()
                            if p_clean and p_clean != 'null':
                                try:
                                    zoom_candidates.append(float(p_clean))
                                except ValueError:
                                    pass
                        # Also check remaining parts
                        for p in parts[xyz_idx+1:]:
                            if p != 'null':
                                try:
                                    zoom_candidates.append(float(p))
                                except ValueError:
                                    pass

                        # The last numeric value should be the zoom factor
                        if zoom_candidates:
                            zoom_val = zoom_candidates[-1]
                            if abs(zoom_val - 1.0) < 0.01:
                                print(f"PASS: Component 2 — Zoom is {zoom_val} (100%) (0.25 pts)")
                                total_score += 0.25
                            else:
                                print(f"FAIL: Component 2 — Zoom is {zoom_val}, expected 1.0 (100%)")
                        else:
                            print(f"FAIL: Component 2 — Could not parse zoom from OpenAction: {oa_str}")
                    else:
                        print(f"FAIL: Component 2 — /XYZ not found in OpenAction: {oa_str}")
                else:
                    print(f"FAIL: Component 2 — OpenAction is not XYZ type: {oa_str}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bookmarks point to distinct pages (each sheet on different page) (0.25 points)
    try:
        toc = doc.get_toc()
        if len(toc) >= len(EXPECTED_SHEET_NAMES):
            pages = [entry[2] for entry in toc]  # 1-based page numbers
            # Each bookmark should point to a different page
            unique_pages = set(pages)
            # Also verify they're in ascending order (Q1 before Q2 before Q3 before Q4)
            is_ascending = all(pages[i] < pages[i+1] for i in range(len(pages)-1))

            if len(unique_pages) == len(EXPECTED_SHEET_NAMES) and is_ascending:
                print(f"PASS: Component 3 — Bookmarks point to {len(unique_pages)} distinct pages in order: {pages} (0.25 pts)")
                total_score += 0.25
            elif len(unique_pages) == len(EXPECTED_SHEET_NAMES):
                print(f"PARTIAL: Component 3 — Distinct pages but not in order: {pages} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Bookmarks don't point to distinct pages: {pages}")
        else:
            print(f"FAIL: Component 3 — Not enough bookmarks ({len(toc)}) to verify page mapping")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: PDF has Outlines in catalog and correct bookmark count (0.15 points)
    try:
        toc = doc.get_toc()
        # Check catalog for Outlines entry
        outlines_found = (
            catalog_xref is not None
            and doc.xref_get_key(catalog_xref, 'Outlines')[0] != 'null'
        ) if catalog_xref is not None else False

        bookmark_count = len(toc)
        if outlines_found and bookmark_count == len(EXPECTED_SHEET_NAMES):
            print(f"PASS: Component 4 — Outlines present, {bookmark_count} bookmarks (0.15 pts)")
            total_score += 0.15
        elif outlines_found and bookmark_count > 0:
            print(f"PARTIAL: Component 4 — Outlines present but {bookmark_count} bookmarks, expected {len(EXPECTED_SHEET_NAMES)} (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 4 — Outlines: {outlines_found}, bookmark count: {bookmark_count}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: persist app state then verify
def persist_app_state(domain):
    import os, time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


persist_app_state("libreoffice_calc")

pdf_path = f'{WORKDIR}/{TASK_ID}.pdf'
if not os.path.exists(pdf_path):
    print(f"File not found: {pdf_path}")
    print("REWARD: 0.0")
else:
    verify_task(pdf_path)
