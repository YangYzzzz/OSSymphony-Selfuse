"""
Reward Script: Multi-app workflow — Extract PDF references, parse with Python,
               create Writer bibliography, export as PDF.
Task ID: pdf_cross_148
Domain: cross-domain (PDF + Writer + Python scripting)
Scoring:
  Component 1: bibliography.pdf exists and is a valid PDF (gate only)
  Component 2: Document has 2-3 pages (0.10 pts)
  Component 3: Contains 'Bibliography' title/heading (0.10 pts)
  Component 4: Contains all 35 numbered entries (1-35) (0.40 pts)
  Component 5: APA format quality — entries contain year patterns and author structure (0.20 pts)
  Component 6: Hanging indent structure present in PDF layout (0.20 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_148'
BIBLIOGRAPHY_PATH = os.path.join(WORKDIR, 'bibliography.pdf')


def verify_task(file_path):
    """
    Verify that ~/Documents/bibliography.pdf is a properly formatted bibliography
    with 35 numbered APA-format references.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: Open the PDF — if it fails, return 0.0 immediately
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            print("CRITICAL: PyMuPDF (fitz) not available — cannot verify PDF")
            print("REWARD: 0.0")
            return 0.0

    try:
        doc = pymupdf.open(file_path)
        page_count = doc.page_count
    except Exception as e:
        print(f"CRITICAL: Cannot open {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract full text across all pages
    try:
        all_text = ""
        for page in doc:
            all_text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"CRITICAL: Cannot extract text from PDF: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page count — bibliography should be 2-3 pages (0.10 pts)
    try:
        if 2 <= page_count <= 3:
            print(f"PASS: Component 1 — Page count is {page_count} (within expected 2-3 pages) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — Expected 2-3 pages, found {page_count} pages")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Bibliography' title or heading present (0.10 pts)
    try:
        # Check for "Bibliography" as a heading in the document
        if re.search(r'\bBibliography\b', all_text, re.IGNORECASE):
            print(f"PASS: Component 2 — 'Bibliography' title/heading found (0.10 pts)")
            total_score += 0.10
        else:
            # Also accept "References" as an equivalent heading
            if re.search(r'\bReferences\b', all_text, re.IGNORECASE):
                print(f"PASS: Component 2 — 'References' heading found (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — Neither 'Bibliography' nor 'References' heading found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 35 numbered entries (1. through 35.) present (0.40 pts)
    # Each numbered entry must start with a digit-period pattern at the beginning of a block/line
    try:
        # Find all entries matching "N." patterns at line starts
        # We look for patterns like "1.", "2.", ..., "35." in the text
        numbered_entries = set()

        # Pattern: line starting with a number followed by period/dot
        # Handles "1. Author" or "1.Author" patterns
        entry_pattern = re.compile(r'(?:^|\n)\s*(\d{1,2})\.\s+\w', re.MULTILINE)
        for match in entry_pattern.finditer(all_text):
            num = int(match.group(1))
            if 1 <= num <= 35:
                numbered_entries.add(num)

        found_count = len(numbered_entries)
        missing = sorted(set(range(1, 36)) - numbered_entries)

        if found_count == 35:
            print(f"PASS: Component 3 — All 35 numbered entries found (entries 1-35) (0.40 pts)")
            total_score += 0.40
        elif found_count >= 30:
            # Partial credit: most entries present
            print(f"PARTIAL: Component 3 — {found_count}/35 numbered entries found, missing: {missing[:5]} (0.25 pts)")
            if found_count >= 30:
                total_score += 0.25
        elif found_count >= 20:
            print(f"PARTIAL: Component 3 — {found_count}/35 numbered entries found, missing: {missing[:5]} (0.15 pts)")
            if found_count >= 20:
                total_score += 0.15
        elif found_count >= 10:
            print(f"PARTIAL: Component 3 — {found_count}/35 numbered entries found (0.08 pts)")
            if found_count >= 10:
                total_score += 0.08
        else:
            print(f"FAIL: Component 3 — Only {found_count}/35 numbered entries found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: APA format quality — entries contain year patterns (YYYY) and author names (0.20 pts)
    # APA format: Author, A. (YEAR). Title. Journal.
    # Check: year pattern (19xx or 20xx) appears in parentheses near authors
    try:
        # Count entries with a year in parentheses — APA citation year pattern
        year_pattern = re.compile(r'\((?:19|20)\d{2}\)')
        year_matches = year_pattern.findall(all_text)
        year_count = len(year_matches)

        # Count entries with author pattern: "LastName, F." or "LastName, F. F."
        author_pattern = re.compile(r'[A-Z][a-z]+,\s+[A-Z](?:\.[A-Z])?\.', re.MULTILINE)
        author_matches = author_pattern.findall(all_text)
        author_count = len(author_matches)

        # We expect at least 35 year patterns and significant author patterns
        apa_ok = year_count >= 30 and author_count >= 30
        if apa_ok:
            print(f"PASS: Component 4 — APA format verified: {year_count} year citations, {author_count} author patterns found (0.20 pts)")
            total_score += 0.20
        elif year_count >= 20 and author_count >= 20:
            partial = 0.10
            print(f"PARTIAL: Component 4 — Partial APA: {year_count} year citations, {author_count} author patterns (0.10 pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Insufficient APA format: {year_count} year citations, {author_count} author patterns")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Hanging indent structure — first line at lower x, continuation at higher x (0.20 pts)
    # In a hanging indent, the first line of each entry starts at left margin,
    # continuation lines are indented (higher x value)
    try:
        first_line_x_values = []
        continuation_line_x_values = []

        # Examine blocks on all pages to detect hanging indent pattern
        for page in doc:
            data = page.get_text("dict")
            for block in data["blocks"]:
                if block["type"] != 0:  # skip non-text blocks
                    continue
                lines = block["lines"]
                if len(lines) < 2:
                    continue
                # Get x0 of first span on first line vs continuation lines
                if lines[0]["spans"] and lines[1]["spans"]:
                    first_x = lines[0]["spans"][0]["bbox"][0]
                    cont_x = lines[1]["spans"][0]["bbox"][0]
                    # Hanging indent: first line x <= continuation line x
                    # But continuation should have LARGER x (indented)
                    if cont_x > first_x + 5:  # at least 5pt indent difference
                        first_line_x_values.append(first_x)
                        continuation_line_x_values.append(cont_x)

        if len(first_line_x_values) >= 10:
            avg_first_x = sum(first_line_x_values) / len(first_line_x_values)
            avg_cont_x = sum(continuation_line_x_values) / len(continuation_line_x_values)
            indent_diff = avg_cont_x - avg_first_x
            print(f"PASS: Component 5 — Hanging indent detected in {len(first_line_x_values)} blocks "
                  f"(avg first_x={avg_first_x:.1f}, avg cont_x={avg_cont_x:.1f}, diff={indent_diff:.1f}pt) (0.20 pts)")
            if len(first_line_x_values) >= 10:
                total_score += 0.20
        elif len(first_line_x_values) >= 5:
            print(f"PARTIAL: Component 5 — Hanging indent found in only {len(first_line_x_values)} blocks (0.10 pts)")
            if len(first_line_x_values) >= 5:
                total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Hanging indent structure not detected (found {len(first_line_x_values)} qualifying blocks)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the bibliography.pdf at the canonical path
if not os.path.exists(BIBLIOGRAPHY_PATH):
    print(f"File not found: {BIBLIOGRAPHY_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(BIBLIOGRAPHY_PATH)
