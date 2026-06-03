"""
Reward Script: PDF statistics generator for thesis.pdf
Task ID: pdf_cross_107
Domain: pdf

Task: Write ~/scripts/pdf_stats.py that generates 8 statistics for ~/Documents/thesis.pdf
and outputs a formatted table to both terminal and ~/Documents/thesis_stats.txt. Then run it.

Scoring Rubric:
  Component 1: pdf_stats.py exists with all 8 required statistics  — 0.30 points
  Component 2: thesis_stats.txt exists with a formatted table containing all 8 labels — 0.35 points
  Component 3: Statistics values in thesis_stats.txt are correct (match actual PDF) — 0.35 points
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cross_107'

SCRIPT_PATH = os.path.join(WORKDIR, 'scripts', 'pdf_stats.py')
STATS_FILE_PATH = os.path.join(WORKDIR, 'Documents', 'thesis_stats.txt')
PDF_PATH = os.path.join(WORKDIR, 'Documents', 'thesis.pdf')

# The 8 required statistics labels to check in the output file
REQUIRED_STAT_LABELS = [
    'Total Pages',
    'Total Words',
    'Total Characters',
    'Words per Page',
    'Reading Time',
    'Number of Images',
    'Number of Links',
    'File Size',
]

# The 8 required capabilities to look for in the script
REQUIRED_SCRIPT_FEATURES = [
    # page count
    ('page_count|page count|pages', 'total pages'),
    # word count
    ('split|words|word count', 'total words'),
    # character count
    ('char|characters', 'total characters'),
    # words per page (derived)
    ('per_page|per page|avg|average|words_per', 'words per page'),
    # reading time
    ('reading|250|read.*time|time.*read', 'reading time'),
    # images
    ('get_images|images|image count', 'number of images'),
    # links
    ('get_links|links|link count', 'number of links'),
    # file size
    ('getsize|file.*size|size.*file|KB|MB|bytes', 'file size'),
]


def check_script_features(script_content):
    """Return list of missing feature labels. Empty list means all present."""
    missing = []
    for pattern, label in REQUIRED_SCRIPT_FEATURES:
        if not re.search(pattern, script_content, re.IGNORECASE):
            missing.append(label)
    return missing


def check_stat_labels(stats_content):
    """Return list of missing stat labels. Empty list means all present."""
    missing = []
    for label in REQUIRED_STAT_LABELS:
        if label.lower() not in stats_content.lower():
            missing.append(label)
    return missing


def has_table_format(stats_content):
    """Return True if content appears to have a formatted table."""
    return ('|' in stats_content or
            '-' * 5 in stats_content or
            '=' * 5 in stats_content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ----------------------------------------------------------------
    # Component 1: pdf_stats.py exists and contains all 8 stat features
    # (0.30 points)
    # ----------------------------------------------------------------
    try:
        script_exists = os.path.exists(SCRIPT_PATH)
        if not script_exists:
            print(f"FAIL: Component 1 — pdf_stats.py not found at {SCRIPT_PATH}")
        else:
            script_content = open(SCRIPT_PATH, 'r', errors='replace').read()
            is_python = ('import' in script_content or 'def ' in script_content
                         or 'print' in script_content)
            if not is_python:
                print("FAIL: Component 1 — file exists but is not a valid Python script")
            else:
                missing_features = check_script_features(script_content)
                if missing_features:
                    print(f"FAIL: Component 1 — script missing features: {missing_features}")
                if not missing_features:
                    print("PASS: Component 1 — pdf_stats.py exists with all 8 stat features (0.30 pts)")
                    total_score += 0.30
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: thesis_stats.txt exists with a formatted table
    # containing all 8 stat labels (0.35 points)
    # ----------------------------------------------------------------
    try:
        stats_exists = os.path.exists(STATS_FILE_PATH)
        if not stats_exists:
            print(f"FAIL: Component 2 — thesis_stats.txt not found at {STATS_FILE_PATH}")
        else:
            stats_content = open(STATS_FILE_PATH, 'r', errors='replace').read()
            if len(stats_content.strip()) == 0:
                print("FAIL: Component 2 — thesis_stats.txt is empty")
            else:
                missing_labels = check_stat_labels(stats_content)
                table_ok = has_table_format(stats_content)
                if missing_labels:
                    print(f"FAIL: Component 2 — thesis_stats.txt missing labels: {missing_labels}")
                elif not table_ok:
                    print("FAIL: Component 2 — thesis_stats.txt lacks formatted table structure")
                if not missing_labels and table_ok:
                    print("PASS: Component 2 — thesis_stats.txt has all 8 labels in formatted table (0.35 pts)")
                    total_score += 0.35
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: Values in thesis_stats.txt are consistent with
    # running the script against the actual thesis.pdf (0.35 points)
    # ----------------------------------------------------------------
    try:
        if not os.path.exists(STATS_FILE_PATH):
            print(f"FAIL: Component 3 — thesis_stats.txt not found, cannot verify values")
        elif not os.path.exists(PDF_PATH):
            print(f"FAIL: Component 3 — thesis.pdf not found at {PDF_PATH}")
        else:
            stats_content = open(STATS_FILE_PATH, 'r', errors='replace').read()

            # Compute actual PDF stats to verify the output values
            try:
                import pymupdf as _pdf
            except ImportError:
                import fitz as _pdf

            doc = _pdf.open(PDF_PATH)
            actual_pages = doc.page_count
            actual_words = 0
            actual_chars = 0
            for page in doc:
                text = page.get_text("text")
                actual_words += len(text.split())
                actual_chars += len(text.replace('\n', '').replace(' ', ''))
            actual_images = sum(len(p.get_images()) for p in doc)
            actual_links = sum(len(p.get_links()) for p in doc)
            actual_file_size_bytes = os.path.getsize(PDF_PATH)
            doc.close()

            sub_checks_passed = 0
            sub_checks_total = 6  # pages, words, images, links, file_size, reading_time

            # Check 3a: Page count present and correct
            page_match = re.search(r'Total Pages[^\d]*(\d+)', stats_content, re.IGNORECASE)
            reported_pages = int(page_match.group(1)) if page_match else None
            page_ok = (reported_pages is not None and reported_pages == actual_pages)
            if page_ok:
                print(f"  Sub-check 3a PASS: Total Pages = {reported_pages} (actual: {actual_pages})")
                sub_checks_passed += 1
            else:
                print(f"  Sub-check 3a FAIL: Total Pages reported as {reported_pages}, actual {actual_pages}")

            # Check 3b: Total words within 10% tolerance
            # (minor variation due to whitespace/encoding differences)
            words_match = re.search(r'Total Words[^\d]*([\d,]+)', stats_content, re.IGNORECASE)
            reported_words = int(words_match.group(1).replace(',', '')) if words_match else None
            word_tol = max(50, int(actual_words * 0.10))
            words_ok = (reported_words is not None and
                        abs(reported_words - actual_words) <= word_tol)
            if words_ok:
                print(f"  Sub-check 3b PASS: Total Words = {reported_words} (actual: {actual_words}, tol: ±{word_tol})")
                sub_checks_passed += 1
            else:
                print(f"  Sub-check 3b FAIL: Total Words = {reported_words}, actual {actual_words}")

            # Check 3c: Number of images correct
            images_match = re.search(r'Number of Images[^\d]*(\d+)', stats_content, re.IGNORECASE)
            reported_images = int(images_match.group(1)) if images_match else None
            images_ok = (reported_images is not None and reported_images == actual_images)
            if images_ok:
                print(f"  Sub-check 3c PASS: Number of Images = {reported_images} (actual: {actual_images})")
                sub_checks_passed += 1
            else:
                print(f"  Sub-check 3c FAIL: Number of Images = {reported_images}, actual {actual_images}")

            # Check 3d: Number of links correct
            links_match = re.search(r'Number of Links[^\d]*(\d+)', stats_content, re.IGNORECASE)
            reported_links = int(links_match.group(1)) if links_match else None
            links_ok = (reported_links is not None and reported_links == actual_links)
            if links_ok:
                print(f"  Sub-check 3d PASS: Number of Links = {reported_links} (actual: {actual_links})")
                sub_checks_passed += 1
            else:
                print(f"  Sub-check 3d FAIL: Number of Links = {reported_links}, actual {actual_links}")

            # Check 3e: File size within 5KB tolerance
            size_match = re.search(r'File Size[^\d]*([\d.]+)\s*(KB|MB|bytes)', stats_content, re.IGNORECASE)
            if size_match:
                size_val = float(size_match.group(1))
                size_unit = size_match.group(2).upper()
                if size_unit == 'KB':
                    reported_bytes = size_val * 1024
                elif size_unit == 'MB':
                    reported_bytes = size_val * 1024 * 1024
                else:
                    reported_bytes = size_val
            else:
                size_val, size_unit, reported_bytes = None, None, None
            size_ok = (reported_bytes is not None and
                       abs(reported_bytes - actual_file_size_bytes) <= 5 * 1024)
            if size_ok:
                print(f"  Sub-check 3e PASS: File Size = {size_val} {size_unit} (actual: {actual_file_size_bytes} bytes, tol: ±5KB)")
                sub_checks_passed += 1
            else:
                print(f"  Sub-check 3e FAIL: File Size = {size_val} {size_unit}, actual {actual_file_size_bytes} bytes")

            # Check 3f: Reading time (derived from words/250) — capture value after "|"
            # Format: "Reading Time (250 wpm)  |  8.6 minutes"
            reading_match = re.search(
                r'Reading Time[^|]*\|\s*([\d.]+)\s*min', stats_content, re.IGNORECASE
            )
            if not reading_match:
                reading_match = re.search(
                    r'Reading Time.*?(\d+\.\d+)\s*minutes', stats_content, re.IGNORECASE
                )
            reported_reading = float(reading_match.group(1)) if reading_match else None
            expected_reading = actual_words / 250.0
            reading_tol = max(0.5, expected_reading * 0.10)
            reading_ok = (reported_reading is not None and
                          abs(reported_reading - expected_reading) <= reading_tol)
            if reading_ok:
                print(f"  Sub-check 3f PASS: Reading Time = {reported_reading} min (expected ~{expected_reading:.1f} min)")
                sub_checks_passed += 1
            else:
                print(f"  Sub-check 3f FAIL: Reading Time = {reported_reading} min, expected ~{expected_reading:.1f} min")

            # Award component 3 score proportionally
            if sub_checks_passed == sub_checks_total:
                print(f"PASS: Component 3 — All {sub_checks_total}/{sub_checks_total} value checks passed (0.35 pts)")
                total_score += 0.35
            elif sub_checks_passed >= 4:
                partial = round(0.35 * (sub_checks_passed / sub_checks_total), 3)
                print(f"PARTIAL: Component 3 — {sub_checks_passed}/{sub_checks_total} value checks ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {sub_checks_passed}/{sub_checks_total} value checks passed")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


verify_task()
