"""
Reward Script: Mail merge template with address block merge fields
Task ID: writer_mt_003
Domain: libreoffice_writer
Scoring:
  Component 1 (0.15) — Placeholder '[ADDRESS HERE]' is removed
  Component 2 (0.25) — '<Name>' merge field on address line 1
  Component 3 (0.25) — '<Street>' merge field on address line 2
  Component 4 (0.25) — '<City>, <State> <ZipCode>' merge field on address line 3
  Component 5 (0.10) — Rest of letter body preserved (date, greeting, closing)
"""

import os
import re
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_003'


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_writer", "libreoffice_calc", "libreoffice_impress"}:
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
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = [p.text for p in doc.paragraphs]

    # Component 1: Placeholder '[ADDRESS HERE]' is removed (0.15 points)
    # In the initial doc, paragraph 0 contains '[ADDRESS HERE]'.
    # In the golden doc, this placeholder must be gone.
    try:
        has_placeholder = any('[ADDRESS HERE]' in p for p in paragraphs)
        if not has_placeholder:
            print("PASS: Component 1 -- Placeholder '[ADDRESS HERE]' removed (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 1 -- Placeholder '[ADDRESS HERE]' still present")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: '<Name>' merge field on address line 1 (0.25 points)
    # The first paragraph should contain '<Name>' (or similar merge field notation)
    try:
        first_para = paragraphs[0] if len(paragraphs) > 0 else ""
        # Check for <Name> or similar merge field patterns
        name_field_found = False
        for p in paragraphs[:3]:
            if re.search(r'<\s*Name\s*>', p, re.IGNORECASE):
                name_field_found = True
                break
        if name_field_found:
            # Additionally verify it's on a dedicated line (first paragraph ideally)
            if re.search(r'<\s*Name\s*>', paragraphs[0], re.IGNORECASE):
                print(f"PASS: Component 2 -- '<Name>' merge field found on line 1: {paragraphs[0]!r} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"PARTIAL: Component 2 -- '<Name>' found but not on line 1 (0.15 pts)")
                total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- '<Name>' merge field not found in first 3 paragraphs")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: '<Street>' merge field on address line 2 (0.25 points)
    try:
        street_field_found = False
        for p in paragraphs[:4]:
            if re.search(r'<\s*Street\s*>', p, re.IGNORECASE):
                street_field_found = True
                break
        if street_field_found:
            if len(paragraphs) > 1 and re.search(r'<\s*Street\s*>', paragraphs[1], re.IGNORECASE):
                print(f"PASS: Component 3 -- '<Street>' merge field found on line 2: {paragraphs[1]!r} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"PARTIAL: Component 3 -- '<Street>' found but not on line 2 (0.15 pts)")
                total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- '<Street>' merge field not found in first 4 paragraphs")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: '<City>, <State> <ZipCode>' on address line 3 (0.25 points)
    # The third paragraph should contain all three: City, State, ZipCode fields
    try:
        city_state_zip_found = False
        city_state_zip_para = None
        for idx, p in enumerate(paragraphs[:5]):
            has_city = bool(re.search(r'<\s*City\s*>', p, re.IGNORECASE))
            has_state = bool(re.search(r'<\s*State\s*>', p, re.IGNORECASE))
            has_zip = bool(re.search(r'<\s*Zip\s*Code\s*>', p, re.IGNORECASE))
            if has_city and has_state and has_zip:
                city_state_zip_found = True
                city_state_zip_para = idx
                break

        if city_state_zip_found:
            if city_state_zip_para == 2:
                print(f"PASS: Component 4 -- City/State/ZipCode merge fields on line 3: {paragraphs[2]!r} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"PARTIAL: Component 4 -- City/State/ZipCode found on line {city_state_zip_para+1} instead of 3 (0.15 pts)")
                total_score += 0.15
        else:
            # Check for individual fields anywhere
            any_city = any(re.search(r'<\s*City\s*>', p, re.IGNORECASE) for p in paragraphs[:5])
            any_state = any(re.search(r'<\s*State\s*>', p, re.IGNORECASE) for p in paragraphs[:5])
            any_zip = any(re.search(r'<\s*Zip\s*Code\s*>', p, re.IGNORECASE) for p in paragraphs[:5])
            found_count = sum([any_city, any_state, any_zip])
            if found_count > 0:
                partial = 0.08 * found_count
                print(f"PARTIAL: Component 4 -- Found {found_count}/3 of City/State/ZipCode fields ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 -- No City/State/ZipCode merge fields found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Address block inserted AND rest of letter body preserved (0.10 points)
    # This is a compound check: merge fields must be present (task change) AND body preserved
    # Anchored to task change so it fails on initial_env (which has no merge fields)
    try:
        full_text = '\n'.join(paragraphs)
        # First gate: at least one merge field must exist (task-introduced change)
        has_any_merge_field = bool(re.search(r'<\s*Name\s*>', full_text, re.IGNORECASE))
        if not has_any_merge_field:
            print("FAIL: Component 5 -- No merge fields present, cannot award body preservation points")
        else:
            preserved_markers = [
                'March 28, 2026',
                'Dear Valued Customer',
                'Greenfield Home & Garden',
                'Warm regards',
                'Patricia Morales',
            ]
            found_markers = sum(1 for m in preserved_markers if m in full_text)
            if found_markers >= 4:
                print(f"PASS: Component 5 -- Merge fields present AND letter body preserved ({found_markers}/5 markers) (0.10 pts)")
                total_score += 0.10
            elif found_markers >= 2:
                partial = 0.05
                print(f"PARTIAL: Component 5 -- Merge fields present but body partially preserved ({found_markers}/5 markers) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 -- Letter body not preserved ({found_markers}/5 markers found)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved state
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
