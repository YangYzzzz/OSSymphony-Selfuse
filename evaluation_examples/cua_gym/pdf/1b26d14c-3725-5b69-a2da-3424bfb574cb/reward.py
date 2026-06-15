"""
Reward Script: Check all annotations in reviewed.pdf and write annotation_report.txt
Task ID: pdf_cr_054
Domain: pdf
Scoring:
  Component 1: Report file exists at correct path (0.1 pts)
  Component 2: All 11 annotations listed (0.3 pts)
  Component 3: Correct annotation types identified (0.2 pts)
  Component 4: Correct page attribution (0.1 pts)
  Component 5: Annotation content text present (0.15 pts)
  Component 6: Color values present (0.1 pts)
  Component 7: Summary line with correct totals (0.05 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_054'
REPORT_PATH = os.path.join(WORKDIR, 'Desktop', 'annotation_report.txt')

# Ground truth annotations extracted from the PDF
EXPECTED_ANNOTATIONS = [
    {"page": 1, "type": "Highlight", "content": "Excellent achievement rate", "color_approx": "(255,255,0)"},
    {"page": 1, "type": "Note", "content": "Need to discuss the two-week delay with stakeholders", "color_approx": "(255,166,0)"},
    {"page": 1, "type": "Rectangle", "content": "High priority section", "color_approx": "(255,0,0)"},
    {"page": 1, "type": "Underline", "content": "Urgent: library reaches EOL soon", "color_approx": "(0,0,255)"},
    {"page": 2, "type": "Highlight", "content": "Impressive throughput metric", "color_approx": "(0,255,0)"},
    {"page": 2, "type": "Note", "content": "Target is 95% unit test coverage by Q3", "color_approx": "(0,0,255)"},
    {"page": 2, "type": "Rectangle", "content": "Good security posture", "color_approx": "(0,128,0)"},
    {"page": 2, "type": "Underline", "content": "Compliance deadline approaching", "color_approx": "(128,0,128)"},
    {"page": 3, "type": "Highlight", "content": "Significant cost savings", "color_approx": "(255,255,0)"},
    {"page": 3, "type": "Note", "content": "Coordinate with infrastructure team for load test scheduling", "color_approx": "(255,0,0)"},
    {"page": 3, "type": "Underline", "content": "Calendar reminder set", "color_approx": "(0,0,0)"},
]


def verify_task():
    """
    Verify annotation_report.txt was created with correct content.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Report file exists (0.1 points)
    # This is the task-introduced change: file does NOT exist in initial_env
    try:
        if os.path.isfile(REPORT_PATH):
            report_content = open(REPORT_PATH, 'r').read()
            if len(report_content.strip()) > 20:
                print(f"PASS: Component 1 -- Report file exists with content ({len(report_content)} chars) (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 1 -- Report file exists but content too short ({len(report_content)} chars)")
        else:
            print(f"FAIL: Component 1 -- Report file not found at {REPORT_PATH}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read report content for subsequent checks
    report_lower = report_content.lower()
    report_lines = report_content.strip().split('\n')

    # Component 2: All 11 annotations listed (0.3 points)
    # Check that report mentions content from all annotations
    # Award partial credit: 0.3 * (found/11)
    try:
        found_count = 0
        for annot in EXPECTED_ANNOTATIONS:
            # Check if the annotation's content text appears in the report
            content_key = annot["content"].lower()
            # Use a substring match — the content should appear somewhere in report
            if content_key in report_lower:
                found_count += 1
            else:
                # Try partial match (first 15 chars)
                partial = content_key[:15]
                if partial in report_lower:
                    found_count += 1
                else:
                    print(f"  MISS: Annotation content not found: '{annot['content'][:40]}...'")

        comp2_score = 0.3 * (found_count / 11)
        if found_count == 11:
            print(f"PASS: Component 2 -- All 11 annotations listed (0.3 pts)")
            total_score += comp2_score
        elif found_count > 0:
            print(f"PARTIAL: Component 2 -- {found_count}/11 annotations found ({comp2_score:.3f} pts)")
            total_score += comp2_score
        else:
            print(f"FAIL: Component 2 -- No annotations found in report")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Correct annotation types identified (0.2 points)
    # Check that each type keyword appears: Highlight, Note (or Sticky Note/Text), Rectangle (or Square), Underline
    try:
        type_mappings = {
            "Highlight": ["highlight"],
            "Note": ["note", "sticky", "text annotation"],
            "Rectangle": ["rectangle", "square", "rect"],
            "Underline": ["underline"],
        }
        types_found = 0
        total_type_checks = 0
        for annot in EXPECTED_ANNOTATIONS:
            expected_type = annot["type"]
            acceptable_names = type_mappings.get(expected_type, [expected_type.lower()])
            total_type_checks += 1
            # Check if any acceptable type name appears near the annotation's content
            content_key = annot["content"].lower()
            # Find the line that contains this annotation's content
            matched_line = None
            for line in report_lines:
                if content_key[:20] in line.lower():
                    matched_line = line.lower()
                    break
            if matched_line:
                if any(name in matched_line for name in acceptable_names):
                    types_found += 1

        comp3_score = 0.2 * (types_found / max(total_type_checks, 1))
        if types_found == total_type_checks:
            print(f"PASS: Component 3 -- All annotation types correctly identified ({types_found}/{total_type_checks}) (0.2 pts)")
            total_score += comp3_score
        elif types_found > 0:
            print(f"PARTIAL: Component 3 -- {types_found}/{total_type_checks} types correct ({comp3_score:.3f} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 -- No annotation types correctly identified")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Correct page attribution (0.1 points)
    # Check that page numbers are correctly assigned to annotations
    try:
        page_correct = 0
        for annot in EXPECTED_ANNOTATIONS:
            content_key = annot["content"].lower()[:20]
            expected_page = annot["page"]
            for line in report_lines:
                if content_key in line.lower():
                    # Look for page number pattern in the line
                    page_match = re.search(r'page\s*(\d+)', line, re.IGNORECASE)
                    if page_match and int(page_match.group(1)) == expected_page:
                        page_correct += 1
                    break

        comp4_score = 0.1 * (page_correct / 11)
        if page_correct == 11:
            print(f"PASS: Component 4 -- All page attributions correct (0.1 pts)")
            total_score += comp4_score
        elif page_correct > 0:
            print(f"PARTIAL: Component 4 -- {page_correct}/11 pages correct ({comp4_score:.3f} pts)")
            total_score += comp4_score
        else:
            print(f"FAIL: Component 4 -- No page attributions correct")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Annotation content text present (0.15 points)
    # Check that quoted content is present for annotations
    try:
        content_quoted = 0
        for annot in EXPECTED_ANNOTATIONS:
            content_text = annot["content"]
            # Check if the content appears quoted (with single or double quotes)
            if (f'"{content_text}"' in report_content or
                f"'{content_text}'" in report_content or
                content_text in report_content):
                content_quoted += 1

        comp5_score = 0.15 * (content_quoted / 11)
        if content_quoted == 11:
            print(f"PASS: Component 5 -- All annotation contents present with text (0.15 pts)")
            total_score += comp5_score
        elif content_quoted > 0:
            print(f"PARTIAL: Component 5 -- {content_quoted}/11 contents found ({comp5_score:.3f} pts)")
            total_score += comp5_score
        else:
            print(f"FAIL: Component 5 -- No annotation contents found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Color values present (0.1 points)
    # Check that RGB color information is included for annotations
    try:
        colors_found = 0
        # Look for any RGB-like pattern: (R,G,B) or R,G,B or #RRGGBB
        color_pattern = re.compile(r'\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)|#[0-9a-fA-F]{6}|\d+\s*,\s*\d+\s*,\s*\d+')
        for annot in EXPECTED_ANNOTATIONS:
            content_key = annot["content"].lower()[:20]
            for line in report_lines:
                if content_key in line.lower():
                    if color_pattern.search(line):
                        colors_found += 1
                    break

        comp6_score = 0.1 * (colors_found / 11)
        if colors_found == 11:
            print(f"PASS: Component 6 -- All color values present (0.1 pts)")
            total_score += comp6_score
        elif colors_found > 0:
            print(f"PARTIAL: Component 6 -- {colors_found}/11 colors found ({comp6_score:.3f} pts)")
            total_score += comp6_score
        else:
            print(f"FAIL: Component 6 -- No color values found in report")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: Summary line with correct totals (0.05 points)
    # Check for summary line with total count and breakdown
    try:
        has_summary = any(
            'total' in line.lower() and '11' in line
            for line in report_lines
        )
        if has_summary:
            print(f"PASS: Component 7 -- Summary line with total count found (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 7 -- No summary line with total=11 found")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isfile(REPORT_PATH):
    print(f"File not found: {REPORT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
