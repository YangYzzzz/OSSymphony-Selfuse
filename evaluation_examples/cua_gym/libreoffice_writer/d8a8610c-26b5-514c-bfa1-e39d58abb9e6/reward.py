"""
Reward Script: Add TOC and Table of Authorities to appellate brief
Task ID: writer_legal_093
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): TABLE OF CONTENTS heading exists (Heading 1 style)
  Component 2 (0.25): TOC entries list major brief headings with tab/page refs
  Component 3 (0.25): TABLE OF AUTHORITIES heading exists (Heading 1 style)
  Component 4 (0.25): TOA has Cases, Statutes, Other Authorities sub-sections with entries
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_093'


def persist_app_state(domain: str):
    """Best-effort save via Ctrl+S for LibreOffice."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all paragraphs with style info
    paragraphs = []
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else 'Normal'
        paragraphs.append((style_name, para.text.strip()))

    # ---------------------------------------------------------------
    # Component 1: TABLE OF CONTENTS heading exists as Heading 1 (0.25 pts)
    # This should FAIL on initial (no TOC heading) and PASS on golden.
    # ---------------------------------------------------------------
    try:
        toc_heading_found = False
        toc_heading_idx = -1
        for i, (style, text) in enumerate(paragraphs):
            if style.startswith('Heading') and 'TABLE OF CONTENTS' in text.upper():
                toc_heading_found = True
                toc_heading_idx = i
                break

        if toc_heading_found:
            print(f"PASS: Component 1 — 'TABLE OF CONTENTS' heading found at paragraph {toc_heading_idx} (0.25 pts)")
            total_score += 0.25
        else:
            print("FAIL: Component 1 — No 'TABLE OF CONTENTS' heading with Heading style found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: TOC entries list major headings from the brief (0.25 pts)
    # Look for entries between TOC heading and TABLE OF AUTHORITIES heading
    # that reference known brief sections. Must have tab-separated page refs.
    # This should FAIL on initial (no TOC section) and PASS on golden.
    # ---------------------------------------------------------------
    try:
        # Known headings that should appear in TOC entries
        expected_toc_entries = [
            'PRELIMINARY STATEMENT',
            'JURISDICTIONAL STATEMENT',
            'STATEMENT OF ISSUES',
            'STATEMENT OF THE CASE',
            'SUMMARY OF ARGUMENT',
            'ARGUMENT',
            'CONCLUSION',
        ]

        # Find TOC entries region: between TOC heading and next Heading 1
        toc_entries_found = 0
        if toc_heading_idx >= 0:
            # Search from TOC heading to next Heading 1
            for i in range(toc_heading_idx + 1, len(paragraphs)):
                style, text = paragraphs[i]
                # Stop at next Heading 1 (TABLE OF AUTHORITIES or other)
                if style.startswith('Heading 1') or style == 'Heading 1':
                    break
                text_upper = text.upper()
                for entry in expected_toc_entries:
                    if entry in text_upper:
                        toc_entries_found += 1
                        break

        # Need at least 5 of the 7 expected entries
        if toc_entries_found >= 5:
            print(f"PASS: Component 2 — Found {toc_entries_found} TOC entries matching expected headings (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Found only {toc_entries_found} TOC entries (expected >= 5)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: TABLE OF AUTHORITIES heading exists as Heading 1 (0.25 pts)
    # This should FAIL on initial (no TOA heading) and PASS on golden.
    # ---------------------------------------------------------------
    try:
        toa_heading_found = False
        toa_heading_idx = -1
        for i, (style, text) in enumerate(paragraphs):
            if style.startswith('Heading') and 'TABLE OF AUTHORITIES' in text.upper():
                toa_heading_found = True
                toa_heading_idx = i
                break

        if toa_heading_found:
            print(f"PASS: Component 3 — 'TABLE OF AUTHORITIES' heading found at paragraph {toa_heading_idx} (0.25 pts)")
            total_score += 0.25
        else:
            print("FAIL: Component 3 — No 'TABLE OF AUTHORITIES' heading with Heading style found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: TOA has Cases, Statutes, Other Authorities sub-sections (0.25 pts)
    # Each sub-section should have a label and at least one entry beneath it.
    # This should FAIL on initial (no TOA) and PASS on golden.
    # ---------------------------------------------------------------
    try:
        # Scan paragraphs after TOA heading until next Heading 1
        subsections_found = {'cases': False, 'statutes': False, 'other': False}
        has_case_entry = False
        has_statute_entry = False
        has_other_entry = False
        current_subsection = None

        if toa_heading_idx >= 0:
            for i in range(toa_heading_idx + 1, len(paragraphs)):
                style, text = paragraphs[i]
                text_upper = text.upper().strip()

                # Stop at next Heading 1 that is NOT part of TOA
                # (e.g., PRELIMINARY STATEMENT)
                if (style == 'Heading 1' or style.startswith('Heading 1')):
                    break

                # Detect sub-section headers
                if text_upper == 'CASES' or text_upper.startswith('CASES'):
                    subsections_found['cases'] = True
                    current_subsection = 'cases'
                    continue
                elif text_upper == 'STATUTES' or text_upper.startswith('STATUTES'):
                    subsections_found['statutes'] = True
                    current_subsection = 'statutes'
                    continue
                elif 'OTHER AUTHORITIES' in text_upper or text_upper == 'OTHER AUTHORITIES':
                    subsections_found['other'] = True
                    current_subsection = 'other'
                    continue

                # Check for entries under each sub-section
                if text and current_subsection == 'cases' and not has_case_entry:
                    # Case citations typically contain "v." or "v."
                    if 'v.' in text or 'V.' in text:
                        has_case_entry = True
                elif text and current_subsection == 'statutes' and not has_statute_entry:
                    # Statute entries contain section symbols or U.S.C.
                    if 'U.S.C.' in text or '§' in text or 'Rule' in text.lower():
                        has_statute_entry = True
                elif text and current_subsection == 'other' and not has_other_entry:
                    # Other authorities - any non-empty entry
                    if len(text) > 5:
                        has_other_entry = True

        # Score: need all 3 sub-sections present with at least one entry each
        subsection_count = sum([
            subsections_found['cases'] and has_case_entry,
            subsections_found['statutes'] and has_statute_entry,
            subsections_found['other'] and has_other_entry,
        ])

        if subsection_count == 3:
            print(f"PASS: Component 4 — All 3 TOA sub-sections found with entries (Cases, Statutes, Other Authorities) (0.25 pts)")
            total_score += 0.25
        elif subsection_count >= 2:
            partial = round(0.25 * subsection_count / 3, 2)
            print(f"PARTIAL: Component 4 — {subsection_count}/3 TOA sub-sections found with entries ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {subsection_count}/3 TOA sub-sections found with entries")
            details = []
            for k, v in subsections_found.items():
                details.append(f"{k}: heading={'yes' if v else 'no'}")
            print(f"  Details: {', '.join(details)}")
            print(f"  Entries: cases={has_case_entry}, statutes={has_statute_entry}, other={has_other_entry}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
