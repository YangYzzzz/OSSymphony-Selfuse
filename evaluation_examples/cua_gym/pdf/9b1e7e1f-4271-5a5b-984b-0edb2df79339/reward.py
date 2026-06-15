"""
Reward Script: OCR extraction from scanned PDF and summary generation
Task ID: pdf_gf2_013
Domain: pdf
Scoring:
  C1 (0.15) — contract_text.txt exists and is non-empty UTF-8
  C2 (0.25) — contract_text.txt has exactly 5 '--- Page N ---' markers for pages 1-5
  C3 (0.15) — contract_text.txt contains substantial OCR text (>500 chars of content beyond markers)
  C4 (0.15) — contract_summary.txt exists and is non-empty UTF-8
  C5 (0.15) — contract_summary.txt has exactly 5 '--- Page N ---' markers for pages 1-5
  C6 (0.15) — contract_summary.txt has '...' separator in each of the 5 page sections
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_013'

TEXT_PATH = os.path.join(WORKDIR, 'scans', 'contract_text.txt')
SUMMARY_PATH = os.path.join(WORKDIR, 'scans', 'contract_summary.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ── Component 1: contract_text.txt exists and is non-empty UTF-8 (0.15 pts) ──
    text_content = None
    try:
        if os.path.isfile(TEXT_PATH):
            with open(TEXT_PATH, 'r', encoding='utf-8') as f:
                text_content = f.read()
            if len(text_content.strip()) > 0:
                print(f"PASS: C1 — contract_text.txt exists, {len(text_content)} chars (0.15 pts)")
                total_score += 0.15
            else:
                print("FAIL: C1 — contract_text.txt is empty")
        else:
            print(f"FAIL: C1 — contract_text.txt not found at {TEXT_PATH}")
    except Exception as e:
        print(f"ERROR: C1 — {e}")

    # ── Component 2: contract_text.txt has exactly 5 page markers (0.25 pts) ──
    try:
        if text_content is not None:
            expected_markers = [f'--- Page {i} ---' for i in range(1, 6)]
            found_markers = [m for m in expected_markers if m in text_content]
            if len(found_markers) == 5:
                print(f"PASS: C2 — All 5 page markers found in contract_text.txt (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: C2 — Found {len(found_markers)}/5 page markers: {found_markers}")
        else:
            print("FAIL: C2 — contract_text.txt not readable (skipped)")
    except Exception as e:
        print(f"ERROR: C2 — {e}")

    # ── Component 3: contract_text.txt has substantial OCR content (0.15 pts) ──
    try:
        if text_content is not None:
            # Strip out page markers and whitespace to measure actual OCR text
            stripped = text_content
            for i in range(1, 6):
                stripped = stripped.replace(f'--- Page {i} ---', '')
            content_len = len(stripped.strip())
            # The golden file has ~7177 chars total; require at least 500 chars of real content
            # Also check for some known contract keywords to confirm it's real OCR
            has_keywords = any(kw in text_content for kw in [
                'Agreement', 'Service', 'shall', 'party', 'Provider'
            ])
            if content_len > 500 and has_keywords:
                print(f"PASS: C3 — Substantial OCR content: {content_len} chars, keywords present (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: C3 — Content length {content_len} (need >500) or missing keywords")
        else:
            print("FAIL: C3 — contract_text.txt not readable (skipped)")
    except Exception as e:
        print(f"ERROR: C3 — {e}")

    # ── Component 4: contract_summary.txt exists and is non-empty UTF-8 (0.15 pts) ──
    summary_content = None
    try:
        if os.path.isfile(SUMMARY_PATH):
            with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
                summary_content = f.read()
            if len(summary_content.strip()) > 0:
                print(f"PASS: C4 — contract_summary.txt exists, {len(summary_content)} chars (0.15 pts)")
                total_score += 0.15
            else:
                print("FAIL: C4 — contract_summary.txt is empty")
        else:
            print(f"FAIL: C4 — contract_summary.txt not found at {SUMMARY_PATH}")
    except Exception as e:
        print(f"ERROR: C4 — {e}")

    # ── Component 5: contract_summary.txt has exactly 5 page markers (0.15 pts) ──
    try:
        if summary_content is not None:
            expected_markers = [f'--- Page {i} ---' for i in range(1, 6)]
            found_markers = [m for m in expected_markers if m in summary_content]
            if len(found_markers) == 5:
                print(f"PASS: C5 — All 5 page markers found in contract_summary.txt (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: C5 — Found {len(found_markers)}/5 page markers: {found_markers}")
        else:
            print("FAIL: C5 — contract_summary.txt not readable (skipped)")
    except Exception as e:
        print(f"ERROR: C5 — {e}")

    # ── Component 6: contract_summary.txt has '...' in each page section (0.15 pts) ──
    try:
        if summary_content is not None:
            # Split by page markers and check each section for '...' separator
            sections_with_dots = 0
            for i in range(1, 6):
                marker = f'--- Page {i} ---'
                if marker in summary_content:
                    # Get text between this marker and next marker (or end)
                    start = summary_content.index(marker) + len(marker)
                    next_marker = f'--- Page {i+1} ---'
                    if next_marker in summary_content:
                        end = summary_content.index(next_marker)
                    else:
                        end = len(summary_content)
                    section = summary_content[start:end]
                    if '...' in section:
                        sections_with_dots += 1

            if sections_with_dots == 5:
                print(f"PASS: C6 — All 5 page sections have '...' separator (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: C6 — {sections_with_dots}/5 sections have '...' separator")
        else:
            print("FAIL: C6 — contract_summary.txt not readable (skipped)")
    except Exception as e:
        print(f"ERROR: C6 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
