"""
Reward Script: Full structural comparison of two PDFs, writing diff to full_diff.txt
Task ID: pdf_cr_080
Domain: pdf
Scoring:
  - Component 1 (0.15): Page Count section with correct counts (v1: 8, v2: 9)
  - Component 2 (0.15): Metadata section with changed fields
  - Component 3 (0.10): Table of Contents section with entries
  - Component 4 (0.15): Text Differences section with per-page info
  - Component 5 (0.15): Images/Annotations/Links sections present
  - Component 6 (0.15): Form Fields section with added field info
  - Component 7 (0.15): Summary line with total changes across categories
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_080'
DIFF_PATH = os.path.join(WORKDIR, 'Desktop', 'full_diff.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: full_diff.txt must exist
    if not os.path.exists(DIFF_PATH):
        print(f"CRITICAL: Diff file not found: {DIFF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(DIFF_PATH, 'r', encoding='utf-8', errors='replace').read()
    except Exception as e:
        print(f"CRITICAL: Cannot read diff file: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(content.strip()) < 50:
        print(f"CRITICAL: Diff file is too short ({len(content)} chars), likely empty/stub")
        print("REWARD: 0.0")
        return 0.0

    content_lower = content.lower()

    # Component 1: Page Count section (0.15 points)
    # Must contain section header and correct page counts for v1 (8) and v2 (9)
    try:
        has_page_section = 'page count' in content_lower
        # Check for v1 having 8 pages and v2 having 9 pages
        has_v1_pages = bool(re.search(r'v1[^:]*:?\s*8\s*(page|pg)', content_lower)) or \
                       bool(re.search(r'spec_v1[^:]*:?\s*8\s*(page|pg)', content_lower)) or \
                       bool(re.search(r'v1.*\b8\b', content_lower) and 'page' in content_lower)
        has_v2_pages = bool(re.search(r'v2[^:]*:?\s*9\s*(page|pg)', content_lower)) or \
                       bool(re.search(r'spec_v2[^:]*:?\s*9\s*(page|pg)', content_lower)) or \
                       bool(re.search(r'v2.*\b9\b', content_lower) and 'page' in content_lower)

        if has_page_section and has_v1_pages and has_v2_pages:
            print(f"PASS: Component 1 — Page Count section with correct counts (0.15 pts)")
            total_score += 0.15
        elif has_page_section:
            # Partial: has section but not exact counts
            print(f"PARTIAL: Component 1 — Page Count section found but counts not verified")
            total_score += 0.05
        else:
            print(f"FAIL: Component 1 — Page Count section missing")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Metadata section (0.15 points)
    # Must contain metadata section with changed fields (author, subject, keywords)
    try:
        has_meta_section = 'metadata' in content_lower
        # Check for evidence of changed metadata fields
        has_author_change = 'author' in content_lower and ('tanaka' in content_lower or 'kai' in content_lower)
        has_subject_change = 'subject' in content_lower
        has_keywords_change = 'keyword' in content_lower and 'performance' in content_lower

        meta_checks = sum([has_author_change, has_subject_change, has_keywords_change])

        if has_meta_section and meta_checks >= 2:
            print(f"PASS: Component 2 — Metadata section with {meta_checks}/3 changed fields (0.15 pts)")
            total_score += 0.15
        elif has_meta_section and meta_checks >= 1:
            print(f"PARTIAL: Component 2 — Metadata section found, {meta_checks}/3 fields")
            total_score += 0.08
        else:
            print(f"FAIL: Component 2 — Metadata section missing or no changed fields detected")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Table of Contents section (0.10 points)
    # Must mention TOC/table of contents with entry info
    try:
        has_toc_section = 'table of contents' in content_lower or 'toc' in content_lower
        has_toc_detail = 'performance benchmarks' in content_lower or \
                         ('added' in content_lower and ('entries' in content_lower or 'entry' in content_lower or 'benchmark' in content_lower))

        if has_toc_section and has_toc_detail:
            print(f"PASS: Component 3 — Table of Contents section with entry details (0.10 pts)")
            total_score += 0.10
        elif has_toc_section:
            print(f"PARTIAL: Component 3 — TOC section found but missing detail")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 — Table of Contents section missing")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Text Differences section (0.15 points)
    # Must contain text differences with per-page information
    try:
        has_text_section = 'text differ' in content_lower or 'text change' in content_lower
        # Check for per-page text diff info
        page_refs = len(re.findall(r'page\s*\d+', content_lower))
        has_per_page = page_refs >= 3  # At least some pages mentioned

        if has_text_section and has_per_page:
            print(f"PASS: Component 4 — Text Differences section with {page_refs} page references (0.15 pts)")
            total_score += 0.15
        elif has_text_section:
            print(f"PARTIAL: Component 4 — Text section found, only {page_refs} page refs")
            total_score += 0.07
        else:
            print(f"FAIL: Component 4 — Text Differences section missing")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Images, Annotations, Links sections (0.15 points)
    # Must contain all three section types
    try:
        has_images = 'image' in content_lower
        has_annotations = 'annotation' in content_lower
        has_links = 'link' in content_lower

        section_count = sum([has_images, has_annotations, has_links])

        if section_count == 3:
            print(f"PASS: Component 5 — Images/Annotations/Links all present (0.15 pts)")
            total_score += 0.15
        elif section_count >= 2:
            print(f"PARTIAL: Component 5 — {section_count}/3 sections present")
            total_score += 0.10
        elif section_count >= 1:
            print(f"PARTIAL: Component 5 — {section_count}/3 sections present")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 — Images/Annotations/Links sections all missing")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Form Fields section (0.15 points)
    # Must contain form fields section mentioning added 'review_date' field
    try:
        has_form_section = 'form field' in content_lower or 'form_field' in content_lower
        has_review_date = 'review_date' in content_lower
        has_field_counts = bool(re.search(r'v1[^:]*:?\s*2\s*(form|field)', content_lower)) or \
                           bool(re.search(r'spec_v1[^:]*:?\s*2\s*(form|field)', content_lower)) or \
                           ('2 form' in content_lower and '3 form' in content_lower)

        if has_form_section and has_review_date:
            print(f"PASS: Component 6 — Form Fields section with review_date field (0.15 pts)")
            total_score += 0.15
        elif has_form_section:
            print(f"PARTIAL: Component 6 — Form Fields section found but review_date not mentioned")
            total_score += 0.07
        else:
            print(f"FAIL: Component 6 — Form Fields section missing")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Summary line (0.15 points)
    # Must contain "Total changes detected:" with category count
    try:
        has_summary = 'total changes detected' in content_lower or 'total' in content_lower and 'change' in content_lower and 'categor' in content_lower
        has_category_count = bool(re.search(r'(\d+)\s*(across|categor)', content_lower))
        # Also accept "N changes" or "across M categories"
        has_numbers = bool(re.search(r'\d+\s+across\s+\d+\s+categor', content_lower))

        if has_summary and (has_numbers or has_category_count):
            print(f"PASS: Component 7 — Summary line with change/category counts (0.15 pts)")
            total_score += 0.15
        elif has_summary:
            print(f"PARTIAL: Component 7 — Summary present but missing counts")
            total_score += 0.07
        else:
            print(f"FAIL: Component 7 — Summary line missing")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
