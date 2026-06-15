"""
Reward Script: Convert PDF to HTML with preserved headings and paragraph structure
Task ID: pdf_mbc_065
Domain: pdf
Scoring:
  - Component 1 (0.20): Valid HTML structure (DOCTYPE, html, head, body tags)
  - Component 2 (0.30): Heading tags present matching PDF section headings
  - Component 3 (0.25): Paragraph tags with substantial text content
  - Component 4 (0.25): Key text content from PDF preserved in HTML
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_065'

# Key section headings from the PDF that must appear in HTML
EXPECTED_HEADINGS = [
    "Abstract",
    "Introduction",
    "Related Work",
    "Methodology",
    "Experimental Setup",
    "Results and Discussion",
    "Conclusion",
    "References",
]

# Key phrases from PDF text that should be preserved in HTML
KEY_PHRASES = [
    "Adaptive Neural Network Architectures",
    "Climate Modeling",
    "Elena Vasquez",
    "Stanford University",
    "Physics-Informed",
    "Multi-Resolution Feature Pyramid",
    "Stochastic Ensemble",
    "Data Preparation",
    "Deterministic Forecast",
    "Extreme Weather",
]


def verify_task(html_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: HTML file must exist
    if not os.path.exists(html_path):
        print(f"CRITICAL: HTML file not found at {html_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read HTML file {html_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must have reasonable content length
    if len(content) < 500:
        print(f"CRITICAL: HTML file too small ({len(content)} bytes), likely incomplete")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid HTML structure (0.20 points)
    # Checks for DOCTYPE, html, head, body tags - the basic structural requirements
    try:
        structure_checks = {
            'DOCTYPE': bool(re.search(r'<!DOCTYPE\s+html', content, re.IGNORECASE)),
            'html_tag': bool(re.search(r'<html[\s>]', content, re.IGNORECASE)),
            'head_tag': bool(re.search(r'<head[\s>]', content, re.IGNORECASE)),
            'body_tag': bool(re.search(r'<body[\s>]', content, re.IGNORECASE)),
            'closing_html': bool(re.search(r'</html>', content, re.IGNORECASE)),
        }
        passed = sum(1 for v in structure_checks.values() if v)
        structure_score = (passed / len(structure_checks)) * 0.20
        if passed == len(structure_checks):
            print(f"PASS: Component 1 - Valid HTML structure, all {passed}/{len(structure_checks)} checks passed (0.20 pts)")
            total_score += 0.20
        elif passed > 0:
            print(f"PARTIAL: Component 1 - HTML structure {passed}/{len(structure_checks)} checks passed ({structure_score:.2f} pts)")
            total_score += structure_score
        else:
            print(f"FAIL: Component 1 - No valid HTML structure found")
            details = ', '.join(f"{k}={'OK' if v else 'MISSING'}" for k, v in structure_checks.items())
            print(f"  Details: {details}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Heading tags present matching PDF section headings (0.30 points)
    # The PDF has major section headings (Abstract, Introduction, etc.) that should
    # appear within <h1> or <h2> tags in the HTML output
    try:
        # Extract text from all heading tags (h1-h6)
        heading_pattern = re.compile(r'<h[1-6][^>]*>(.*?)</h[1-6]>', re.DOTALL | re.IGNORECASE)
        heading_matches = heading_pattern.findall(content)
        # Strip HTML tags from heading content
        heading_texts = [re.sub(r'<[^>]+>', '', h).strip() for h in heading_matches]
        heading_texts_lower = [h.lower() for h in heading_texts]

        found_headings = 0
        for expected in EXPECTED_HEADINGS:
            expected_lower = expected.lower()
            # Check if expected heading appears in any heading tag
            if any(expected_lower in ht for ht in heading_texts_lower):
                found_headings += 1

        heading_ratio = found_headings / len(EXPECTED_HEADINGS)
        heading_score = heading_ratio * 0.30

        if found_headings == len(EXPECTED_HEADINGS):
            print(f"PASS: Component 2 - All {found_headings}/{len(EXPECTED_HEADINGS)} expected headings found in HTML heading tags (0.30 pts)")
            total_score += 0.30
        elif found_headings > 0:
            print(f"PARTIAL: Component 2 - {found_headings}/{len(EXPECTED_HEADINGS)} expected headings found ({heading_score:.2f} pts)")
            total_score += heading_score
        else:
            print(f"FAIL: Component 2 - No expected headings found in HTML heading tags")
            print(f"  Expected headings: {EXPECTED_HEADINGS}")
            print(f"  Found heading tags: {heading_texts[:5]}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Paragraph tags with substantial text content (0.25 points)
    # The PDF has ~55 paragraphs of text. The HTML should preserve these using <p> tags.
    try:
        p_pattern = re.compile(r'<p[^>]*>(.*?)</p>', re.DOTALL | re.IGNORECASE)
        p_matches = p_pattern.findall(content)
        # Strip tags and count paragraphs with meaningful content (> 20 chars)
        meaningful_paragraphs = []
        for p in p_matches:
            clean = re.sub(r'<[^>]+>', '', p).strip()
            if len(clean) > 20:
                meaningful_paragraphs.append(clean)

        num_paragraphs = len(meaningful_paragraphs)
        # PDF has ~55 paragraphs; expect at least 15 meaningful ones for full credit
        if num_paragraphs >= 15:
            print(f"PASS: Component 3 - {num_paragraphs} meaningful paragraphs found (>= 15 required) (0.25 pts)")
            total_score += 0.25
        elif num_paragraphs >= 5:
            para_score = (num_paragraphs / 15.0) * 0.25
            print(f"PARTIAL: Component 3 - {num_paragraphs} meaningful paragraphs found ({para_score:.2f} pts)")
            total_score += para_score
        else:
            print(f"FAIL: Component 3 - Only {num_paragraphs} meaningful paragraphs found (need >= 5)")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Key text content from PDF preserved in HTML (0.25 points)
    # Check that important phrases from the PDF appear in the HTML text
    try:
        # Strip all HTML tags to get plain text
        plain_text = re.sub(r'<[^>]+>', ' ', content)
        plain_text_lower = plain_text.lower()

        found_phrases = 0
        for phrase in KEY_PHRASES:
            if phrase.lower() in plain_text_lower:
                found_phrases += 1

        phrase_ratio = found_phrases / len(KEY_PHRASES)
        phrase_score = phrase_ratio * 0.25

        if found_phrases == len(KEY_PHRASES):
            print(f"PASS: Component 4 - All {found_phrases}/{len(KEY_PHRASES)} key phrases preserved (0.25 pts)")
            total_score += 0.25
        elif found_phrases > 0:
            print(f"PARTIAL: Component 4 - {found_phrases}/{len(KEY_PHRASES)} key phrases preserved ({phrase_score:.2f} pts)")
            total_score += phrase_score
        else:
            print(f"FAIL: Component 4 - No key phrases from PDF found in HTML")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
html_path = f'{WORKDIR}/Documents/article.html'
if not os.path.exists(html_path):
    print(f"File not found: {html_path}")
    print("REWARD: 0.0")
else:
    verify_task(html_path)
