"""
Reward Script: Insert cross-reference in Chapter 3 to Table 2.1 in Chapter 2
Task ID: writer_rm_058
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): [reference needed] placeholder replaced with "Table 2.1" text
  Component 2 (0.35): Cross-reference is a proper bookmark-ref element targeting Ref_Table_2_1
  Component 3 (0.25): Chapter2.odt retains the bookmark Ref_Table_2_1 (reference target intact)
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_058'

CHAPTER3_PATH = os.path.join(WORKDIR, 'Chapter3.odt')
CHAPTER2_PATH = os.path.join(WORKDIR, 'Chapter2.odt')


def read_odt_content_xml(filepath):
    """Read and return content.xml from an ODT file."""
    with zipfile.ZipFile(filepath) as z:
        return z.read('content.xml').decode('utf-8')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: Both files must exist
    if not os.path.exists(CHAPTER3_PATH):
        print(f"CRITICAL: Chapter3.odt not found at {CHAPTER3_PATH}")
        print("REWARD: 0.0")
        return 0.0

    if not os.path.exists(CHAPTER2_PATH):
        print(f"CRITICAL: Chapter2.odt not found at {CHAPTER2_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        ch3_xml = read_odt_content_xml(CHAPTER3_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot read Chapter3.odt content.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        ch2_xml = read_odt_content_xml(CHAPTER2_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot read Chapter2.odt content.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # =========================================================================
    # Component 1: [reference needed] replaced with "Table 2.1" text (0.40 pts)
    # This checks that the placeholder is gone AND the correct text appears.
    # Initial has "[reference needed]", golden has "Table 2.1".
    # =========================================================================
    try:
        has_placeholder = '[reference needed]' in ch3_xml
        # Check for "Table 2.1" appearing in the paragraph that contains "shown in"
        # Use a broad pattern to find "As shown in ... Table 2.1"
        has_table_ref_text = bool(re.search(r'As shown in[^<]*Table\s*2\.1', ch3_xml))
        # Also check if Table 2.1 appears inside a bookmark-ref or as plain text
        if not has_table_ref_text:
            # It might be inside XML elements: "As shown in " + <bookmark-ref>Table 2.1</bookmark-ref>
            has_table_ref_text = ('shown in' in ch3_xml.lower() and 'Table 2.1' in ch3_xml)

        if not has_placeholder and has_table_ref_text:
            print(f"PASS: Component 1 — Placeholder removed, 'Table 2.1' text present (0.40 pts)")
            total_score += 0.40
        elif has_placeholder:
            print(f"FAIL: Component 1 — '[reference needed]' placeholder still present")
        else:
            print(f"FAIL: Component 1 — Placeholder removed but 'Table 2.1' text not found in context")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: Cross-reference is a bookmark-ref element (0.35 pts)
    # The golden state uses <text:bookmark-ref text:reference-format="text"
    #   text:ref-name="Ref_Table_2_1">Table 2.1</text:bookmark-ref>
    # This verifies it's a proper cross-reference, not just plain text.
    # =========================================================================
    try:
        # Look for bookmark-ref element referencing Ref_Table_2_1
        has_bookmark_ref = bool(re.search(
            r'<text:bookmark-ref[^>]*text:ref-name="Ref_Table_2_1"[^>]*>',
            ch3_xml
        ))
        # Also accept slight variations in the ref-name (case, underscores, etc.)
        if not has_bookmark_ref:
            has_bookmark_ref = bool(re.search(
                r'<text:bookmark-ref[^>]*text:ref-name="[^"]*[Tt]able[_ ]?2[._]?1[^"]*"[^>]*>',
                ch3_xml
            ))

        if has_bookmark_ref:
            print(f"PASS: Component 2 — Proper bookmark-ref cross-reference found (0.35 pts)")
            total_score += 0.35
        else:
            # Check if there's any kind of cross-reference field
            has_any_ref = bool(re.search(r'<text:bookmark-ref', ch3_xml))
            if has_any_ref:
                print(f"FAIL: Component 2 — bookmark-ref found but does not reference Ref_Table_2_1")
            else:
                print(f"FAIL: Component 2 — No bookmark-ref cross-reference element found in Chapter3.odt")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: Chapter2.odt bookmark target intact (0.25 pts)
    # The bookmark Ref_Table_2_1 must exist in Chapter2.odt so the
    # cross-reference has a valid target.
    # NOTE: This component is scored ONLY in conjunction with the cross-ref
    # existing in Chapter3 (Component 2). On initial_env, Component 2 fails
    # so this compound check also fails, preventing initial_env from scoring.
    # =========================================================================
    try:
        has_bookmark_start = bool(re.search(
            r'<text:bookmark-start[^>]*text:name="Ref_Table_2_1"',
            ch2_xml
        ))
        has_bookmark_end = bool(re.search(
            r'<text:bookmark-end[^>]*text:name="Ref_Table_2_1"',
            ch2_xml
        ))

        # Only award points if the cross-reference in Ch3 also exists (compound check)
        if has_bookmark_start and has_bookmark_end and total_score >= 0.35:
            print(f"PASS: Component 3 — Bookmark 'Ref_Table_2_1' exists in Chapter2.odt with both start and end markers (0.25 pts)")
            total_score += 0.25
        elif has_bookmark_start and has_bookmark_end:
            print(f"FAIL: Component 3 — Bookmark exists in Chapter2 but cross-reference in Chapter3 is missing (compound check)")
        elif not has_bookmark_start:
            print(f"FAIL: Component 3 — bookmark-start for 'Ref_Table_2_1' not found in Chapter2.odt")
        else:
            print(f"FAIL: Component 3 — bookmark-end for 'Ref_Table_2_1' not found in Chapter2.odt")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
