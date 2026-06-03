"""
Reward Script: Generate PDF report with embedded charts
Task ID: pdf_aw_048
Domain: pdf
Scoring:
  Component 1 (0.20): PDF exists at expected path and has >= 4 pages
  Component 2 (0.20): Page 1 has title about monthly visitors and an embedded chart image
  Component 3 (0.20): Page 2 has title about revenue and an embedded chart image
  Component 4 (0.20): Page 3 has title about traffic sources and an embedded chart image
  Component 5 (0.20): Page 4 has title about conversion rates and an embedded chart image
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_048'
PDF_PATH = os.path.join(WORKDIR, 'reports', 'analytics_dashboard.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: PDF file not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF has at least 4 pages (0.20 points)
    try:
        page_count = doc.page_count
        if page_count >= 4:
            print(f"PASS: Component 1 — PDF has {page_count} pages (>= 4 required) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — PDF has {page_count} pages, expected >= 4")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page 1 has title about monthly visitors AND an embedded chart image (0.20 points)
    try:
        page = doc[0]
        text = page.get_text("text").lower()
        images = page.get_images()
        has_title = any(kw in text for kw in ["visitor", "monthly"])
        has_image = len(images) >= 1
        if has_title and has_image:
            print(f"PASS: Component 2 — Page 1 has visitor-related title and {len(images)} image(s) (0.20 pts)")
            total_score += 0.20
        else:
            reasons = []
            if not has_title:
                reasons.append(f"no visitor/monthly keyword in title text: {repr(text[:100])}")
            if not has_image:
                reasons.append("no embedded images found")
            print(f"FAIL: Component 2 — Page 1: {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page 2 has title about revenue AND an embedded chart image (0.20 points)
    try:
        page = doc[1]
        text = page.get_text("text").lower()
        images = page.get_images()
        has_title = any(kw in text for kw in ["revenue", "product"])
        has_image = len(images) >= 1
        if has_title and has_image:
            print(f"PASS: Component 3 — Page 2 has revenue-related title and {len(images)} image(s) (0.20 pts)")
            total_score += 0.20
        else:
            reasons = []
            if not has_title:
                reasons.append(f"no revenue/product keyword in title text: {repr(text[:100])}")
            if not has_image:
                reasons.append("no embedded images found")
            print(f"FAIL: Component 3 — Page 2: {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page 3 has title about traffic sources AND an embedded chart image (0.20 points)
    try:
        page = doc[2]
        text = page.get_text("text").lower()
        images = page.get_images()
        has_title = any(kw in text for kw in ["traffic", "source"])
        has_image = len(images) >= 1
        if has_title and has_image:
            print(f"PASS: Component 4 — Page 3 has traffic-related title and {len(images)} image(s) (0.20 pts)")
            total_score += 0.20
        else:
            reasons = []
            if not has_title:
                reasons.append(f"no traffic/source keyword in title text: {repr(text[:100])}")
            if not has_image:
                reasons.append("no embedded images found")
            print(f"FAIL: Component 4 — Page 3: {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Page 4 has title about conversion/scatter/campaign AND an embedded chart image (0.20 points)
    try:
        page = doc[3]
        text = page.get_text("text").lower()
        images = page.get_images()
        has_title = any(kw in text for kw in ["conversion", "scatter", "campaign", "ad spend"])
        has_image = len(images) >= 1
        if has_title and has_image:
            print(f"PASS: Component 5 — Page 4 has conversion-related title and {len(images)} image(s) (0.20 pts)")
            total_score += 0.20
        else:
            reasons = []
            if not has_title:
                reasons.append(f"no conversion/scatter/campaign keyword in title text: {repr(text[:100])}")
            if not has_image:
                reasons.append("no embedded images found")
            print(f"FAIL: Component 5 — Page 4: {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(PDF_PATH):
    print(f"File not found: {PDF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PDF_PATH)
