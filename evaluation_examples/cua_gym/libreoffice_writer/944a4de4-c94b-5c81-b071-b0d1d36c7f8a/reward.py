"""
Reward Script: Remove duplicate entries from mailing list, keeping first occurrence of each address.
Task ID: osworld_writer_duplicate_line_removal_009
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.4): Exactly 37 unique address entries remain (15 duplicates removed from 52 total)
  - Component 2 (0.3): No duplicate addresses in the document
  - Component 3 (0.3): Addresses appear in their original first-occurrence order
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_duplicate_line_removal_009'

# Expected 37 unique addresses in order of first appearance (derived from golden artifact)
# The golden file preserves first occurrences of 52 initial entries, removing 15 duplicates
EXPECTED_ADDRESSES = [
    '742 Evergreen Terrace, Springfield, IL 62704',
    '1600 Pennsylvania Ave NW, Washington, DC 20500',
    '221B Baker Street, London, NW1 6XE, UK',
    '350 Fifth Avenue, New York, NY 10118',
    '1 Infinite Loop, Cupertino, CA 95014',
    '4059 Mt Lee Dr, Hollywood, CA 90068',
    '800 N Michigan Ave, Chicago, IL 60611',
    '1 Harbor Drive, San Diego, CA 92101',
    '500 W 2nd St, Austin, TX 78701',
    '55 Water Street, New York, NY 10041',
    '1234 Oak Hill Blvd, Nashville, TN 37201',
    '88 Pine Street, Portland, OR 97201',
    '310 Maple Avenue, Denver, CO 80203',
    '9900 Wilshire Blvd, Beverly Hills, CA 90210',
    '47 Riverside Road, Boston, MA 02101',
    '623 Sunset Strip, Los Angeles, CA 90028',
    '1 Embarcadero Center, San Francisco, CA 94111',
    '3400 N Lake Shore Dr, Chicago, IL 60657',
    '890 Peachtree St NE, Atlanta, GA 30309',
    '2200 Mission College Blvd, Santa Clara, CA 95054',
    '150 Broadway, New York, NY 10038',
    '7 World Trade Center, New York, NY 10007',
    '1000 Main Street, Houston, TX 77002',
    '412 Elm Street, Cincinnati, OH 45202',
    '675 Ponce De Leon Ave NE, Atlanta, GA 30308',
    '330 N Wabash Ave, Chicago, IL 60611',
    '1 Microsoft Way, Redmond, WA 98052',
    '1600 Amphitheatre Pkwy, Mountain View, CA 94043',
    '2100 Geng Road, Palo Alto, CA 94303',
    '1601 S California Ave, Palo Alto, CA 94304',
    '500 Oracle Pkwy, Redwood Shores, CA 94065',
    '901 Cherry Ave, San Bruno, CA 94066',
    '770 Broadway, New York, NY 10003',
    '1455 Market St, San Francisco, CA 94103',
    '410 Terry Ave N, Seattle, WA 98109',
    '2380 McGaw Ave, Irvine, CA 92614',
    '100 Universal City Plaza, Universal City, CA 91608',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Remove all 15 duplicate addresses from a 52-entry mailing list,
    keeping only the first occurrence. Result should have exactly 37 unique addresses.
    """
    total_score = 0.0

    # Load the document — if it fails, return 0.0 immediately
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all non-empty mailing address paragraphs
    # The document starts with a title and subtitle, followed by a blank line, then addresses
    # Header lines to skip: title, subtitle, empty separator
    HEADER_LINES = {
        'Community Newsletter Mailing List',
        'Subscriber Addresses \u2014 Spring 2025 Edition',
        'Subscriber Addresses - Spring 2025 Edition',
    }
    all_paragraphs = [p.text for p in doc.paragraphs]

    # Skip header paragraphs (title, subtitle, blank separator), collect addresses
    # Address entries start after the first non-header, non-blank paragraph
    start_idx = 0
    for idx, para_text in enumerate(all_paragraphs):
        stripped = para_text.strip()
        if stripped and stripped not in HEADER_LINES:
            start_idx = idx
            break

    address_entries = [
        p.strip() for p in all_paragraphs[start_idx:]
        if p.strip()
    ]

    print(f"INFO: Found {len(address_entries)} non-empty address entries in document")

    # Component 1: Exactly 37 unique addresses remain (0.4 points)
    # The task asks to remove 15 duplicates from 52 entries, leaving 37 unique addresses
    try:
        if len(address_entries) == 37:
            print(f"PASS: Component 1 — Exactly 37 address entries found (correct count after removing 15 duplicates)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected 37 address entries, found {len(address_entries)} "
                  f"(task requires removing 15 duplicates from 52 original entries)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No duplicate addresses remain (0.3 points)
    # After removing duplicates, every address should appear exactly once
    try:
        seen = set()
        duplicates_found = []
        for addr in address_entries:
            if addr in seen:
                duplicates_found.append(addr)
            seen.add(addr)

        if len(duplicates_found) == 0:
            print(f"PASS: Component 2 — No duplicate addresses found ({len(address_entries)} unique entries)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — {len(duplicates_found)} duplicate(s) still present: "
                  f"{duplicates_found[:3]}{'...' if len(duplicates_found) > 3 else ''}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Addresses are in the correct first-occurrence order (0.3 points)
    # The task says keep only the first occurrence of each address in original order
    # We verify against the known correct list of 37 addresses
    try:
        if len(address_entries) == len(EXPECTED_ADDRESSES):
            mismatches = []
            for i, (actual, expected) in enumerate(zip(address_entries, EXPECTED_ADDRESSES)):
                if actual != expected:
                    mismatches.append(f"Position {i}: expected '{expected}', found '{actual}'")

            if len(mismatches) == 0:
                print(f"PASS: Component 3 — All 37 addresses match expected first-occurrence order exactly")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — {len(mismatches)} order/content mismatch(es): "
                      f"{mismatches[:2]}{'...' if len(mismatches) > 2 else ''}")
        else:
            # Can't check order if count is wrong, but partial overlap check
            # Find how many of the expected addresses are present and in order
            actual_set = set(address_entries)
            expected_set = set(EXPECTED_ADDRESSES)
            overlap = actual_set & expected_set
            print(f"FAIL: Component 3 — Cannot verify order, count mismatch "
                  f"(found {len(address_entries)}, expected {len(EXPECTED_ADDRESSES)}). "
                  f"{len(overlap)}/{len(EXPECTED_ADDRESSES)} addresses match content-wise.")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the VM environment
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
