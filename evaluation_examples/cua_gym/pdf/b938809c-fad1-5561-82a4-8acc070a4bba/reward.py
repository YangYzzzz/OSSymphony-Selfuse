"""
Reward Script: Extract PDF text page-by-page to structured JSON
Task ID: pdf_gf2_023
Domain: pdf
Scoring:
  Component 1 (0.15): JSON file exists and is valid parseable JSON
  Component 2 (0.15): Top-level structure is a list with exactly 15 entries
  Component 3 (0.20): Each entry has required keys: 'page', 'text', 'word_count'
  Component 4 (0.15): Page numbers are 1-indexed and sequential (1 through 15)
  Component 5 (0.20): Text content is non-empty for all pages and reasonably matches PDF source
  Component 6 (0.15): word_count equals len(text.split()) for every entry
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_023'

JSON_PATH = os.path.join(WORKDIR, 'Documents', 'financial_report_text.json')
PDF_PATH = os.path.join(WORKDIR, 'Documents', 'financial_report.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ─── Component 1: JSON file exists and is valid JSON (0.15 pts) ───
    data = None
    try:
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
        print(f"PASS: Component 1 — JSON file exists and is valid JSON (0.15 pts)")
        total_score += 0.15
    except FileNotFoundError:
        print(f"FAIL: Component 1 — JSON file not found at {JSON_PATH}")
        # Cannot continue without the file
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — JSON file exists but is not valid JSON: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # ─── Component 2: List of exactly 15 entries (0.15 pts) ───
    try:
        if not isinstance(data, list):
            print(f"FAIL: Component 2 — Expected a list, got {type(data).__name__}")
        elif len(data) != 15:
            print(f"FAIL: Component 2 — Expected 15 entries, got {len(data)}")
        else:
            print(f"PASS: Component 2 — List with exactly 15 entries (0.15 pts)")
            total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ─── Component 3: Each entry has 'page', 'text', 'word_count' keys (0.20 pts) ───
    try:
        required_keys = {'page', 'text', 'word_count'}
        all_keys_ok = True
        if isinstance(data, list) and len(data) > 0:
            for i, entry in enumerate(data):
                if not isinstance(entry, dict):
                    print(f"FAIL: Component 3 — Entry {i} is not a dict: {type(entry).__name__}")
                    all_keys_ok = False
                    break
                missing = required_keys - set(entry.keys())
                if missing:
                    print(f"FAIL: Component 3 — Entry {i} missing keys: {missing}")
                    all_keys_ok = False
                    break
            if all_keys_ok:
                print(f"PASS: Component 3 — All entries have required keys (0.20 pts)")
                total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Cannot check keys: data is not a non-empty list")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ─── Component 4: Page numbers 1-15 sequential (0.15 pts) ───
    try:
        if isinstance(data, list) and len(data) == 15:
            pages = [entry.get('page') for entry in data if isinstance(entry, dict)]
            expected_pages = list(range(1, 16))
            if pages == expected_pages:
                print(f"PASS: Component 4 — Pages sequential 1-15 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Expected pages {expected_pages}, got {pages}")
        else:
            print(f"FAIL: Component 4 — Cannot verify page sequence: data length != 15")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ─── Component 5: Text content is non-empty and reasonably matches PDF (0.20 pts) ───
    try:
        import fitz
        pdf_doc = fitz.open(PDF_PATH)
        pdf_page_count = len(pdf_doc)

        if not isinstance(data, list) or len(data) == 0:
            print(f"FAIL: Component 5 — No data to check text content")
        else:
            all_text_ok = True
            for i, entry in enumerate(data):
                if not isinstance(entry, dict):
                    all_text_ok = False
                    break
                text = entry.get('text', '')
                if not isinstance(text, str) or len(text.strip()) == 0:
                    print(f"FAIL: Component 5 — Page {i+1} has empty or non-string text")
                    all_text_ok = False
                    break

            if all_text_ok:
                # Verify text roughly matches the PDF by checking a few pages
                match_count = 0
                check_pages = [0, 7, 14]  # first, middle, last
                for pg_idx in check_pages:
                    if pg_idx < pdf_page_count and pg_idx < len(data):
                        pdf_text = pdf_doc[pg_idx].get_text().strip()
                        json_text = data[pg_idx].get('text', '').strip()
                        # Check that at least some significant overlap exists
                        # Use first 50 chars of PDF text as a signature
                        if len(pdf_text) > 20:
                            signature = pdf_text[:50]
                            if signature in json_text:
                                match_count += 1
                            else:
                                # Try a more lenient check: first few words
                                pdf_words = pdf_text.split()[:5]
                                json_words = json_text.split()[:5]
                                if pdf_words == json_words:
                                    match_count += 1
                        else:
                            match_count += 1  # very short page, give benefit of doubt

                if match_count >= 2:
                    print(f"PASS: Component 5 — Text non-empty, matches PDF content ({match_count}/3 spot checks) (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 5 — Text does not match PDF content ({match_count}/3 spot checks passed)")

        pdf_doc.close()
    except ImportError:
        # If fitz not available, fall back to just checking non-emptiness
        all_text_ok = True
        if isinstance(data, list):
            for i, entry in enumerate(data):
                if not isinstance(entry, dict):
                    all_text_ok = False
                    break
                text = entry.get('text', '')
                if not isinstance(text, str) or len(text.strip()) == 0:
                    all_text_ok = False
                    break
            if all_text_ok:
                print(f"PASS: Component 5 — All text entries are non-empty (fitz unavailable for cross-check) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — Some text entries are empty or invalid")
        else:
            print(f"FAIL: Component 5 — Data is not a list")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ─── Component 6: word_count matches len(text.split()) (0.15 pts) ───
    try:
        if isinstance(data, list) and len(data) > 0:
            all_wc_ok = True
            for i, entry in enumerate(data):
                if not isinstance(entry, dict):
                    all_wc_ok = False
                    break
                text = entry.get('text', '')
                wc = entry.get('word_count')
                if not isinstance(text, str):
                    all_wc_ok = False
                    print(f"FAIL: Component 6 — Page {i+1}: text is not a string")
                    break
                expected_wc = len(text.split())
                if wc != expected_wc:
                    all_wc_ok = False
                    print(f"FAIL: Component 6 — Page {i+1}: word_count={wc}, expected {expected_wc}")
                    break
            if all_wc_ok:
                print(f"PASS: Component 6 — All word_count values match len(text.split()) (0.15 pts)")
                total_score += 0.15
        else:
            print(f"FAIL: Component 6 — Cannot verify word_count: data is not a non-empty list")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(JSON_PATH):
    print(f"File not found: {JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
