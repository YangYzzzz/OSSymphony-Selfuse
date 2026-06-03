"""
Reward Script: Export PDF of presentation with transitions included as PDF page transitions
Task ID: impress_el_033
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.3): PDF file exists and is a valid PDF
  - Component 2 (0.3): PDF has 8 pages matching the 8-slide presentation
  - Component 3 (0.4): PDF contains page transition (/Trans) entries
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'impress_el_033'

# The task exports from Animated_Deck.odp -> PDF
# The PDF could be named Animated_Deck.pdf or similar
PDF_CANDIDATES = [
    os.path.join(WORKDIR, 'Animated_Deck.pdf'),
    os.path.join(WORKDIR, 'Desktop', 'Animated_Deck.pdf'),
    os.path.join(WORKDIR, 'Documents', 'Animated_Deck.pdf'),
    os.path.join(WORKDIR, 'Downloads', 'Animated_Deck.pdf'),
]


def find_pdf():
    """Find the exported PDF file. Check known candidates first, then search."""
    for path in PDF_CANDIDATES:
        if os.path.exists(path):
            return path

    # Search /home/user for any .pdf file
    for root, dirs, files in os.walk(WORKDIR):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.lower().endswith('.pdf'):
                return os.path.join(root, f)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find the PDF file
    pdf_path = find_pdf()

    # Component 1: PDF file exists and is a valid PDF (0.3 points)
    try:
        if pdf_path is None:
            print("FAIL: Component 1 -- No PDF file found in /home/user/")
            print("REWARD: 0.0")
            return 0.0

        with open(pdf_path, 'rb') as f:
            header = f.read(5)

        if header == b'%PDF-':
            print(f"PASS: Component 1 -- Valid PDF found at {pdf_path} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- File {pdf_path} is not a valid PDF (header: {header!r})")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read full PDF content for remaining checks
    try:
        with open(pdf_path, 'rb') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read PDF content: {e}")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: PDF has 8 pages matching the presentation (0.3 points)
    try:
        # Count page objects: /Type/Page (not /Type/Pages which is the page tree)
        # Pages appear as /Type/Page/ or /Type /Page followed by non-'s'
        page_matches = re.findall(rb'/Type\s*/Page(?!s)', content)
        page_count = len(page_matches)

        if page_count == 8:
            print(f"PASS: Component 2 -- PDF has {page_count} pages matching 8-slide presentation (0.3 pts)")
            total_score += 0.3
        elif page_count > 0:
            # Partial credit if pages exist but count is off
            partial = 0.15
            print(f"PARTIAL: Component 2 -- PDF has {page_count} pages, expected 8 ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- Could not determine page count from PDF")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: PDF contains page transition entries (0.4 points)
    try:
        # Look for /Trans << ... >> entries which indicate PDF page transitions
        trans_entries = re.findall(rb'/Trans\s*<<[^>]*>>', content)
        trans_count = len(trans_entries)

        if trans_count >= 4:
            # Good: multiple transitions exported (the ODP has 8 slides with transitions)
            print(f"PASS: Component 3 -- PDF contains {trans_count} page transition entries (0.4 pts)")
            total_score += 0.4
        elif trans_count > 0:
            # Partial: some transitions but not all
            partial = 0.2
            print(f"PARTIAL: Component 3 -- PDF contains {trans_count} transition entries, expected >= 4 ({partial} pts)")
            total_score += partial
        else:
            # Also check for /Trans as a keyword anywhere (might have different formatting)
            if b'/Trans' in content:
                partial = 0.1
                print(f"PARTIAL: Component 3 -- Found /Trans keyword but no structured entries ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- No page transition (/Trans) entries found in PDF")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
