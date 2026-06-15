"""
Reward Script: Highlight statute references in legal brief
Task ID: pdf_legal_064
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists and is a valid 25-page PDF
  Component 2 (0.35): Highlight annotations present with correct count (>= 35)
  Component 3 (0.25): All highlight annotations use blue color (0,0,1)
  Component 4 (0.25): Highlights cover actual statute references on key pages
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_064'

OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'statutory_brief_highlighted.pdf')
# The regex pattern for statute references: "Section XXX.XX" or "ss XXX.XX" or "§ XXX.XX"
STATUTE_PATTERN = re.compile(r'(Section\s+\d+\.\d+|§\s*\d+\.\d+|ss\s+\d+\.\d+)', re.IGNORECASE)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ── Precondition: import fitz ──
    try:
        import fitz
    except ImportError:
        try:
            import pymupdf as fitz
        except ImportError:
            print("CRITICAL: Cannot import fitz/pymupdf")
            print("REWARD: 0.0")
            return 0.0

    # ── Component 1: Output file exists and is a valid 25-page PDF (0.15 pts) ──
    # This is task-introduced: the output file does NOT exist in initial_env.
    try:
        if not os.path.exists(OUTPUT_PATH):
            print(f"FAIL: Component 1 -- Output file not found at {OUTPUT_PATH}")
            print("REWARD: 0.0")
            return 0.0

        doc = fitz.open(OUTPUT_PATH)
        page_count = len(doc)
        if page_count == 25:
            print(f"PASS: Component 1 -- Output PDF exists with {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected 25 pages, found {page_count}")
            # Still continue checking other components
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # ── Component 2: Sufficient highlight annotations (0.35 pts) ──
    # Task says 35 statute references. Golden has 63 highlight annotations (some references
    # span lines creating multiple rects). We accept >= 35 highlights as a strong signal.
    try:
        highlight_count = 0
        for page in doc:
            if page.annots():
                for annot in page.annots():
                    if annot.type[1] == "Highlight":
                        highlight_count += 1

        if highlight_count >= 35:
            print(f"PASS: Component 2 -- Found {highlight_count} highlight annotations (>= 35 required) (0.35 pts)")
            total_score += 0.35
        elif highlight_count >= 20:
            partial = 0.35 * (highlight_count / 35.0)
            print(f"PARTIAL: Component 2 -- Found {highlight_count} highlights, expected >= 35 ({partial:.2f} pts)")
            total_score += partial
        elif highlight_count > 0:
            partial = 0.35 * (highlight_count / 35.0) * 0.5
            print(f"PARTIAL: Component 2 -- Found only {highlight_count} highlights ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No highlight annotations found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ── Component 3: All highlights use blue color (0.25 pts) ──
    # Blue = stroke color (0, 0, 1) with tolerance
    try:
        blue_count = 0
        non_blue_count = 0
        for page in doc:
            if page.annots():
                for annot in page.annots():
                    if annot.type[1] == "Highlight":
                        stroke = annot.colors.get("stroke")
                        if stroke and len(stroke) == 3:
                            r, g, b = stroke
                            if r < 0.2 and g < 0.2 and b > 0.7:
                                blue_count += 1
                            else:
                                non_blue_count += 1
                        else:
                            non_blue_count += 1

        total_highlights = blue_count + non_blue_count
        if total_highlights > 0 and non_blue_count == 0:
            print(f"PASS: Component 3 -- All {blue_count} highlights are blue (0.25 pts)")
            total_score += 0.25
        elif total_highlights > 0:
            if blue_count > 0:  # partial credit for some blue highlights
                partial = 0.25 * (blue_count / total_highlights)
                print(f"PARTIAL: Component 3 -- {blue_count}/{total_highlights} highlights are blue ({partial:.2f} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 3 -- No highlights to check color")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # ── Component 4: Highlights cover actual statute references (0.25 pts) ──
    # Spot-check that highlights overlap with text matching the statute pattern on key pages.
    # We check a sample of pages known to contain statute references.
    try:
        # Pages to spot-check (0-indexed): pages that have statute references
        check_pages = [2, 5, 10, 14, 17, 23]
        pages_with_correct_highlights = 0

        for pg_num in check_pages:
            if pg_num >= len(doc):
                continue
            page = doc[pg_num]
            page_text = page.get_text()
            statute_matches = STATUTE_PATTERN.findall(page_text)
            if not statute_matches:
                # This page may not have matches; skip it
                continue

            # Check if any highlight annotation overlaps with a statute reference
            overlap_found = 0  # use int counter to track overlap detection
            if page.annots():
                for annot in page.annots():
                    if annot.type[1] != "Highlight":
                        continue
                    annot_rect = annot.rect
                    # Search for statute text instances on the page
                    for match_text in statute_matches:
                        search_term = match_text.strip()
                        # Use first word + number for search (handles line breaks)
                        simple_term = search_term.split()[0]  # "Section" or "§" or "ss"
                        instances = page.search_for(simple_term)
                        for inst in instances:
                            if annot_rect.intersects(inst):
                                overlap_found += 1
                                break
                        if overlap_found > 0:
                            break
                    if overlap_found > 0:
                        break

            if overlap_found > 0:
                pages_with_correct_highlights += 1

        if pages_with_correct_highlights >= len(check_pages) - 1:
            # Allow 1 page miss due to edge cases
            print(f"PASS: Component 4 -- {pages_with_correct_highlights}/{len(check_pages)} spot-checked pages have correct highlights (0.25 pts)")
            total_score += 0.25
        elif pages_with_correct_highlights > 0:
            if pages_with_correct_highlights >= 1:  # partial credit
                partial = 0.25 * (pages_with_correct_highlights / len(check_pages))
                print(f"PARTIAL: Component 4 -- {pages_with_correct_highlights}/{len(check_pages)} pages correct ({partial:.2f} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 4 -- No spot-checked pages have highlights over statute references")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
