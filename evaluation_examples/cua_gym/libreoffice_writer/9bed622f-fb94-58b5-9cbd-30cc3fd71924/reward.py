"""
Reward Script: Remove duplicate MAC address lines from network scan document
Task ID: osworld_writer_dedup_010
Domain: libreoffice_writer
Scoring:
  Component 1: No duplicate MAC address lines remain (0.5 pts)
  Component 2: Document contains exactly 113 lines (all unique devices) (0.3 pts)
  Component 3: Original order of first appearance is preserved (0.2 pts)
"""

import os
import re

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_dedup_010'

# Regex pattern for MAC address format XX:XX:XX:XX:XX:XX
MAC_PATTERN = re.compile(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$')

# Expected unique device count (113 devices scanned 3 times = 339 total → 113 unique)
EXPECTED_UNIQUE_COUNT = 113

# Expected first MAC address in order-of-first-appearance
EXPECTED_FIRST_MAC = '00:1A:2B:3C:4D:5E'
# Expected second MAC address
EXPECTED_SECOND_MAC = 'AA:BB:CC:DD:EE:FF'
# Expected tenth MAC address
EXPECTED_TENTH_MAC = '3C:A9:F4:28:BC:01'


def verify_task(file_path):
    """
    Verify that all duplicate MAC address lines have been removed from the document.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all non-empty lines
    lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    # Validate that lines look like MAC addresses (precondition gate)
    mac_lines = [l for l in lines if MAC_PATTERN.match(l)]
    if len(mac_lines) == 0:
        print("CRITICAL: No MAC address lines found in document")
        print("REWARD: 0.0")
        return 0.0

    non_mac_lines = [l for l in lines if not MAC_PATTERN.match(l)]
    if non_mac_lines:
        print(f"NOTE: {len(non_mac_lines)} non-MAC lines found (ignoring for scoring)")

    # Component 1: No duplicate MAC address lines remain (0.5 points)
    # This FAILS on initial (339 lines, 113 unique → 226 duplicates)
    # This PASSES on golden (113 lines, 113 unique → 0 duplicates)
    try:
        unique_mac_count = len(set(mac_lines))
        total_mac_count = len(mac_lines)
        duplicate_count = total_mac_count - unique_mac_count

        if duplicate_count == 0:
            print(f"PASS: Component 1 — No duplicates found. All {total_mac_count} lines are unique. (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Found {duplicate_count} duplicate MAC lines "
                  f"({total_mac_count} total, {unique_mac_count} unique)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Document contains exactly 113 unique MAC addresses (0.3 points)
    # This FAILS on initial (339 total lines, not 113)
    # This PASSES on golden (113 unique lines)
    try:
        if len(mac_lines) == EXPECTED_UNIQUE_COUNT:
            print(f"PASS: Component 2 — Document has exactly {EXPECTED_UNIQUE_COUNT} MAC address lines. (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected {EXPECTED_UNIQUE_COUNT} MAC lines, "
                  f"found {len(mac_lines)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Order of first discovery is preserved (0.2 points)
    # Verifies that the first, second, and tenth MAC matches the order of first appearance in original
    # This FAILS on initial (too many lines: 339 != 113 so Component 2 already gates this)
    # But to be safe, this check independently verifies order alignment.
    # On initial: first 10 MACs match, BUT line count is 339 so only passes on golden where
    # deduplication has been correctly applied (both count and order must match).
    try:
        if len(mac_lines) >= 10:
            first_ok = mac_lines[0] == EXPECTED_FIRST_MAC
            second_ok = mac_lines[1] == EXPECTED_SECOND_MAC
            tenth_ok = mac_lines[9] == EXPECTED_TENTH_MAC

            if first_ok and second_ok and tenth_ok and len(mac_lines) == EXPECTED_UNIQUE_COUNT:
                print(f"PASS: Component 3 — Order preserved. "
                      f"First='{mac_lines[0]}', Second='{mac_lines[1]}', "
                      f"Tenth='{mac_lines[9]}'. (0.2 pts)")
                total_score += 0.2
            elif not first_ok:
                print(f"FAIL: Component 3 — First MAC should be '{EXPECTED_FIRST_MAC}', "
                      f"found '{mac_lines[0]}'")
            elif not second_ok:
                print(f"FAIL: Component 3 — Second MAC should be '{EXPECTED_SECOND_MAC}', "
                      f"found '{mac_lines[1]}'")
            elif not tenth_ok:
                print(f"FAIL: Component 3 — Tenth MAC should be '{EXPECTED_TENTH_MAC}', "
                      f"found '{mac_lines[9]}'")
            else:
                print(f"FAIL: Component 3 — Line count {len(mac_lines)} != {EXPECTED_UNIQUE_COUNT}, "
                      f"order check skipped")
        else:
            print(f"FAIL: Component 3 — Not enough lines ({len(mac_lines)}) to check order")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
