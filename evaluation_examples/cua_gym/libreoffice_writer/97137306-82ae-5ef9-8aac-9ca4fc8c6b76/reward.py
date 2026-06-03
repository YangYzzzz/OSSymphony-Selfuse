"""
Reward Script: DOI Resolution and Chicago-format Citation in LibreOffice Writer
Task ID: osworld_multi_apps_doi_resolve_writer_013
Domain: libreoffice_writer
Scoring:
  Component 1: TOC with clickable internal links for all 15 references (0.25 pts)
  Component 2: 15 Chicago author-date formatted references with DOI hyperlinks (0.35 pts)
  Component 3: 8 gray-background abstract boxes for Primary Studies (0.25 pts)
  Component 4: 15 bookmark anchors providing TOC navigation targets (0.15 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doi_resolve_writer_013'

def persist_app_state():
    """Attempt to save any unsaved LibreOffice Writer state."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        import time
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: LibreOffice Writer document systematic_review.odt should have:
    - 15 Chicago author-date formatted citations with DOI hyperlinks
    - 8 Primary Studies each with a gray-background abstract text box
    - A clickable Table of Contents at the top linking to all 15 references
    """
    total_score = 0.0

    # Load the ODT document
    try:
        from odf.opendocument import load
        from odf.text import P, A, BookmarkStart
        doc = load(file_path)
    except ImportError:
        print("CRITICAL: odfpy not available. Trying python-docx fallback.")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Helper: get full text of a paragraph node (recursively)
    def get_para_text(para):
        text = ''
        for node in para.childNodes:
            if hasattr(node, 'data'):
                text += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if hasattr(child, 'data'):
                        text += child.data
                    elif hasattr(child, 'childNodes'):
                        for gchild in child.childNodes:
                            if hasattr(gchild, 'data'):
                                text += gchild.data
        return text

    # -----------------------------------------------------------------------
    # Component 1: TOC with clickable internal links for all 15 references (0.25 pts)
    # The TOC section should contain hyperlinks pointing to #ref-p1..#ref-p8
    # and #ref-s1..#ref-s7 (15 total internal links)
    # -----------------------------------------------------------------------
    try:
        all_links = doc.getElementsByType(A)
        toc_links = [
            lnk for lnk in all_links
            if lnk.getAttribute('href') and lnk.getAttribute('href').startswith('#')
        ]
        num_toc_links = len(toc_links)
        if num_toc_links >= 15:
            print(f"PASS: Component 1 — TOC has {num_toc_links} clickable internal links (>= 15 required) (0.25 pts)")
            total_score += 0.25
        elif num_toc_links >= 8:
            # Partial: at least half of references linked
            partial = 0.10
            print(f"PARTIAL: Component 1 — TOC has {num_toc_links} internal links (need 15) (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — TOC has only {num_toc_links} internal links (expected >= 15)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: 15 references with Chicago author-date format + DOI hyperlinks (0.35 pts)
    # Chicago author-date: "LastName, FirstName, ... Year. 'Title.' Journal ..."
    # Each reference should include a clickable DOI hyperlink (doi.org)
    # -----------------------------------------------------------------------
    try:
        doi_links = [
            lnk for lnk in all_links
            if lnk.getAttribute('href') and 'doi.org' in lnk.getAttribute('href')
        ]
        num_doi_links = len(doi_links)

        # Check for Chicago formatting: reference paragraphs should follow "LastName, First..."
        # Chicago author-date: starts with "LastName, FirstName" format
        paras = doc.getElementsByType(P)
        # Pattern: Capital letter + word chars + comma + space + word char (name, firstname)
        chicago_pattern = re.compile(r'^[A-Z]\w+,\s+\w')
        year_pattern = re.compile(r'\.\s+\d{4}\.')
        chicago_refs = []
        for para in paras:
            text = get_para_text(para)
            # Must start with LastName, First AND contain a year marker
            if chicago_pattern.match(text) and year_pattern.search(text):
                chicago_refs.append(text[:80])

        num_chicago = len(chicago_refs)

        if num_doi_links >= 15 and num_chicago >= 15:
            print(f"PASS: Component 2 — {num_doi_links} DOI hyperlinks + {num_chicago} Chicago-format refs (0.35 pts)")
            total_score += 0.35
        elif num_doi_links >= 15 and num_chicago >= 8:
            partial = 0.20
            print(f"PARTIAL: Component 2 — {num_doi_links} DOI links but only {num_chicago} Chicago-format refs (+{partial} pts)")
            total_score += partial
        elif num_doi_links >= 8 and num_chicago >= 8:
            partial = 0.15
            print(f"PARTIAL: Component 2 — {num_doi_links} DOI links, {num_chicago} Chicago-format refs (+{partial} pts)")
            total_score += partial
        elif num_doi_links > 0 or num_chicago > 0:
            partial = 0.05
            print(f"PARTIAL: Component 2 — {num_doi_links} DOI links, {num_chicago} Chicago-format refs (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No DOI hyperlinks and no Chicago-format references found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: 8 gray-background abstract boxes for Primary Studies (0.25 pts)
    # Paragraphs with gray background style (GrayBoxPara or similar background)
    # starting with "Abstract:" should appear after each of the 8 primary study refs
    # -----------------------------------------------------------------------
    try:
        paras = doc.getElementsByType(P)
        # Method 1: Check for paragraphs using a gray-background style
        abstract_style_paras = [
            p for p in paras
            if p.getAttribute('stylename') == 'GrayBoxPara'
        ]

        # Method 2: Fallback - check for paragraphs starting with "Abstract:"
        # that have a background color set in their style
        abstract_text_paras = [
            p for p in paras
            if get_para_text(p).startswith('Abstract:')
        ]

        # Check automatic styles for any style with gray background color
        gray_bg_styles = set()
        try:
            for style in doc.automaticstyles.childNodes:
                style_name = style.getAttribute('name') if hasattr(style, 'getAttribute') else None
                if style_name:
                    for child in style.childNodes:
                        bg = child.getAttribute('backgroundcolor') if hasattr(child, 'getAttribute') else None
                        if bg and bg.lower() not in ('#ffffff', '#000000', 'transparent', ''):
                            gray_bg_styles.add(style_name)
        except Exception:
            pass

        # Count paragraphs with any gray/colored background style
        bg_paras = [
            p for p in paras
            if p.getAttribute('stylename') in gray_bg_styles
            or p.getAttribute('stylename') == 'GrayBoxPara'
        ]

        num_abstract_boxes = max(len(abstract_style_paras), len(bg_paras))
        # Also verify they contain abstract text
        if num_abstract_boxes == 0 and len(abstract_text_paras) >= 8:
            # Abstract text found but without proper styling
            partial = 0.10
            print(f"PARTIAL: Component 3 — {len(abstract_text_paras)} abstract paragraphs found but no gray background styling (+{partial} pts)")
            total_score += partial
        elif num_abstract_boxes >= 8:
            print(f"PASS: Component 3 — {num_abstract_boxes} gray-background abstract boxes (>= 8 required) (0.25 pts)")
            total_score += 0.25
        elif num_abstract_boxes >= 4:
            partial = 0.12
            print(f"PARTIAL: Component 3 — {num_abstract_boxes} gray-background abstract boxes (need 8) (+{partial} pts)")
            total_score += partial
        elif num_abstract_boxes > 0:
            partial = 0.05
            print(f"PARTIAL: Component 3 — only {num_abstract_boxes} gray-background abstract boxes (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No gray-background abstract boxes found (expected 8)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: 15 bookmark anchors for TOC navigation targets (0.15 pts)
    # Each reference entry should have a bookmark (e.g. ref-p1..ref-p8, ref-s1..ref-s7)
    # so that the TOC hyperlinks can navigate to them
    # -----------------------------------------------------------------------
    try:
        bookmarks = doc.getElementsByType(BookmarkStart)
        num_bookmarks = len(bookmarks)

        # Check that bookmark names match expected ref-p1..ref-p8, ref-s1..ref-s7 pattern
        bookmark_names = set()
        for bm in bookmarks:
            name = bm.getAttribute('name')
            if name:
                bookmark_names.add(name)

        ref_pattern = re.compile(r'^ref-(p[1-8]|s[1-7])$')
        matching_bookmarks = [n for n in bookmark_names if ref_pattern.match(n)]

        if len(matching_bookmarks) >= 15:
            print(f"PASS: Component 4 — {len(matching_bookmarks)} reference bookmark anchors (>= 15 required) (0.15 pts)")
            total_score += 0.15
        elif len(matching_bookmarks) >= 8:
            partial = 0.08
            print(f"PARTIAL: Component 4 — {len(matching_bookmarks)} reference bookmarks (need 15) (+{partial} pts)")
            total_score += partial
        elif num_bookmarks >= 1:
            partial = 0.05
            print(f"PARTIAL: Component 4 — {num_bookmarks} bookmarks found but only {len(matching_bookmarks)} match expected naming (+{partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No bookmark anchors found (expected 15: ref-p1..ref-p8, ref-s1..ref-s7)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/systematic_review.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
