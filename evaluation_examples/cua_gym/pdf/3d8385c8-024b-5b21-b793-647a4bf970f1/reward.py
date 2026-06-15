"""
Reward Script: PDF System Health Report creation
Task ID: pdf_mbc_090
Domain: pdf
Scoring:
  Component 1: Title 'System Health Report' in bold >= 20pt (0.25)
  Component 2: Date subtitle present (0.15)
  Component 3: Table header with Service/Status/Uptime columns (0.25)
  Component 4: Table has 5 data rows (0.20)
  Component 5: Footer 'Generated automatically' at bottom (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_090'


def _check_title(page, pymupdf):
    """Check title is 'System Health Report' in bold >= 20pt. Returns score."""
    data = page.get_text("dict")
    for block in data["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if "System Health Report" in span["text"]:
                    is_bold = bool(span["flags"] & 16)
                    size = span["size"]
                    if is_bold and size >= 20.0:
                        print("PASS: Component 1 - Title 'System Health Report' bold=yes, size=%.1f (0.25 pts)" % size)
                        return 0.25
                    else:
                        print("FAIL: Component 1 - Title found but bold=%s, size=%.1f (need bold >= 20pt)" % (is_bold, size))
                        return 0.0
    print("FAIL: Component 1 - Title 'System Health Report' not found")
    return 0.0


def _check_date_subtitle(full_text):
    """Check for a date subtitle. Returns score."""
    date_patterns = [
        r'\b\d{4}[-/]\d{2}[-/]\d{2}\b',
        r'\b\d{2}[-/]\d{2}[-/]\d{4}\b',
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
        r'\bDate\b.*\d{2,4}',
    ]
    for pattern in date_patterns:
        if re.search(pattern, full_text, re.IGNORECASE):
            print("PASS: Component 2 - Date subtitle found in text (0.15 pts)")
            return 0.15
    print("FAIL: Component 2 - No date subtitle found in text")
    return 0.0


def _check_table_header(page, full_text):
    """Check table with Service/Status/Uptime headers. Returns (score, rows_or_None)."""
    try:
        tf = page.find_tables()
        for table in tf:
            rows = table.extract()
            if len(rows) >= 1:
                header = [str(c).strip().lower() if c else "" for c in rows[0]]
                if "service" in header and "status" in header and "uptime" in header:
                    print("PASS: Component 3 - Table with Service/Status/Uptime headers found (0.25 pts)")
                    return 0.25, rows
    except Exception as e:
        print("WARN: Component 3 - find_tables error: %s, falling back to text" % e)

    # Fallback: check text for column headers
    if "Service" in full_text and "Status" in full_text and "Uptime" in full_text:
        print("PASS: Component 3 - Service/Status/Uptime column headers found in text (0.25 pts)")
        return 0.25, None
    print("FAIL: Component 3 - Table with Service/Status/Uptime headers not found")
    return 0.0, None


def _check_data_rows(table_rows, full_text):
    """Check table has 5 data rows. Returns score."""
    if table_rows is not None:
        data_row_count = len(table_rows) - 1  # subtract header
        if data_row_count >= 5:
            print("PASS: Component 4 - Table has %d data rows (>= 5 required) (0.20 pts)" % data_row_count)
            return 0.20
        elif data_row_count >= 3:
            print("PARTIAL: Component 4 - Table has %d data rows (5 required), awarding 0.10 pts" % data_row_count)
            return 0.10
        else:
            print("FAIL: Component 4 - Table has %d data rows (need >= 5)" % data_row_count)
            return 0.0
    else:
        # Fallback: count uptime-like percentage values
        uptime_matches = re.findall(r'\d{2}\.\d{2}%', full_text)
        if len(uptime_matches) >= 5:
            print("PASS: Component 4 - Found %d uptime values (>= 5 data rows) (0.20 pts)" % len(uptime_matches))
            return 0.20
        elif len(uptime_matches) >= 3:
            print("PARTIAL: Component 4 - Found %d uptime values, awarding 0.10 pts" % len(uptime_matches))
            return 0.10
        else:
            print("FAIL: Component 4 - Found only %d uptime-like values" % len(uptime_matches))
            return 0.0


def _check_footer(page, full_text):
    """Check footer 'Generated automatically' in bottom portion of page. Returns score."""
    page_height = page.rect.height
    instances = page.search_for("Generated automatically")
    if instances:
        rect = instances[0]
        center_y = rect.y0 + rect.height / 2
        if center_y > page_height * 0.4:
            print("PASS: Component 5 - Footer 'Generated automatically' at y=%.1f (page height=%.1f) (0.15 pts)" % (center_y, page_height))
            return 0.15
        else:
            print("FAIL: Component 5 - 'Generated automatically' at y=%.1f which is too high" % center_y)
            return 0.0
    elif "Generated automatically" in full_text:
        # Text exists but search_for didn't find it (encoding issue)
        print("PASS: Component 5 - Footer 'Generated automatically' found in text (0.15 pts)")
        return 0.15
    else:
        print("FAIL: Component 5 - 'Generated automatically' not found in PDF")
        return 0.0


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    if doc.page_count < 1:
        print("FAIL: PDF has no pages")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[0]
    full_text = page.get_text("text")

    # Component 1: Title 'System Health Report' in bold >= 20pt (0.25 points)
    try:
        comp1 = _check_title(page, pymupdf)
        if comp1 > 0:
            total_score += comp1
    except Exception as e:
        print("ERROR: Component 1 - %s" % e)

    # Component 2: Date subtitle present (0.15 points)
    try:
        comp2 = _check_date_subtitle(full_text)
        if comp2 > 0:
            total_score += comp2
    except Exception as e:
        print("ERROR: Component 2 - %s" % e)

    # Component 3: Table with header row containing Service, Status, Uptime (0.25 points)
    table_rows = None
    try:
        comp3_score, table_rows = _check_table_header(page, full_text)
        if comp3_score > 0:
            total_score += comp3_score
    except Exception as e:
        print("ERROR: Component 3 - %s" % e)

    # Component 4: Table has 5 data rows (excluding header) (0.20 points)
    try:
        comp4 = _check_data_rows(table_rows, full_text)
        if comp4 > 0:
            total_score += comp4
    except Exception as e:
        print("ERROR: Component 4 - %s" % e)

    # Component 5: Footer 'Generated automatically' at bottom of page (0.15 points)
    try:
        comp5 = _check_footer(page, full_text)
        if comp5 > 0:
            total_score += comp5
    except Exception as e:
        print("ERROR: Component 5 - %s" % e)

    doc.close()

    final_score = min(total_score, 1.0)
    print()
    print("Score: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
file_path = WORKDIR + '/Documents/system_report.pdf'
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
