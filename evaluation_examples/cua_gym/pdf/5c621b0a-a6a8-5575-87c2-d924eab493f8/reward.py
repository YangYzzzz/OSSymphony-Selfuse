"""
Reward Script: Convert HTML to PDF
Task ID: pdf_mbc_068
Domain: pdf
Scoring:
  Component 1 (0.15): PDF exists and is a valid PDF
  Component 2 (0.35): PDF contains key textual content from the HTML (headers, paragraphs)
  Component 3 (0.25): PDF contains table data (revenue figures)
  Component 4 (0.25): PDF has reasonable structure (multiple pages, sufficient text)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_068'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: PDF file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: PDF file not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Try to load as a valid PDF
    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open {file_path} as PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all text from PDF
    try:
        all_text = ""
        for i in range(doc.page_count):
            all_text += doc[i].get_text()
        all_text_lower = all_text.lower()
    except Exception as e:
        print(f"CRITICAL: Cannot extract text from PDF: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF is valid and non-empty (0.15 points)
    # This distinguishes from initial_env which has NO PDF at all
    try:
        if doc.page_count > 0 and len(all_text.strip()) > 50:
            print(f"PASS: Component 1 - PDF is valid with {doc.page_count} page(s) and {len(all_text)} chars of text (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - PDF has {doc.page_count} pages and {len(all_text)} chars (expected non-trivial content)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: PDF contains key textual content from HTML headers and paragraphs (0.35 points)
    # The HTML has specific headers and content that should be preserved in the PDF
    try:
        key_phrases = [
            "meridian analytics",         # Main title / H1
            "executive summary",          # H2
            "regional revenue",           # H2 (Regional Revenue Breakdown)
            "product performance",        # H2
            "operational highlights",     # H2
        ]
        found_count = 0
        for phrase in key_phrases:
            if phrase in all_text_lower:
                found_count += 1
                print(f"  FOUND: '{phrase}'")
            else:
                print(f"  MISSING: '{phrase}'")

        # Award proportional credit: need at least 4/5 for full marks
        if found_count >= 4:
            print(f"PASS: Component 2 - Found {found_count}/{len(key_phrases)} key phrases (0.35 pts)")
            total_score += 0.35
        elif found_count >= 2:
            partial = round(0.35 * (found_count / len(key_phrases)), 2)
            print(f"PARTIAL: Component 2 - Found {found_count}/{len(key_phrases)} key phrases ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - Found only {found_count}/{len(key_phrases)} key phrases")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: PDF contains table data with revenue figures (0.25 points)
    # The HTML has a table with regional revenue data including dollar amounts
    try:
        # Check for region names and revenue figures from the HTML table
        # Note: PDF text extraction may split multi-word names across lines
        table_indicators = [
            "europe",            # Table region
            "asia",              # Table region (Asia-Pacific)
            "latin",             # Table region (Latin America)
            "$2,145,000",        # North America revenue
            "$1,280,000",        # Europe revenue
        ]
        # Also check for any dollar amounts as evidence of table data
        import re
        dollar_pattern = re.findall(r'\$[\d,]+', all_text)

        table_found = 0
        for indicator in table_indicators:
            if indicator in all_text_lower:
                table_found += 1
                print(f"  TABLE FOUND: '{indicator}'")
            else:
                print(f"  TABLE MISSING: '{indicator}'")

        has_dollar_amounts = len(dollar_pattern) >= 5  # The table has many dollar values

        if table_found >= 4 and has_dollar_amounts:
            print(f"PASS: Component 3 - Found {table_found}/{len(table_indicators)} table indicators and {len(dollar_pattern)} dollar amounts (0.25 pts)")
            total_score += 0.25
        elif table_found >= 2 or has_dollar_amounts:
            partial = 0.15
            print(f"PARTIAL: Component 3 - Found {table_found} table indicators and {len(dollar_pattern)} dollar amounts ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - Found {table_found} table indicators and {len(dollar_pattern)} dollar amounts")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: PDF has reasonable structure - multiple pages and sufficient text (0.25 points)
    # The HTML is a full report with sections; converted PDF should have multiple pages and substantial text
    try:
        text_length = len(all_text.strip())
        page_count = doc.page_count

        # The golden PDF has 3 pages and ~2100+ chars of text
        if page_count >= 2 and text_length >= 1000:
            print(f"PASS: Component 4 - {page_count} pages and {text_length} chars of text (0.25 pts)")
            total_score += 0.25
        elif page_count >= 1 and text_length >= 500:
            partial = 0.15
            print(f"PARTIAL: Component 4 - {page_count} pages and {text_length} chars ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 - Only {page_count} pages and {text_length} chars")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/Documents/web_page.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
