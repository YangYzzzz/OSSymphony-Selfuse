"""
Reward Script: Depreciation Schedule PDF Verification
Task ID: pdf_fin_048
Domain: pdf
Scoring:
  Component 1: PDF exists and has content (0.10)
  Component 2: Title/header present (0.10)
  Component 3: All 8 required column headers present (0.20)
  Component 4: 10 asset data rows with required fields (0.25)
  Component 5: Totals row present with values (0.15)
  Component 6: Mathematical correctness - Annual Dep = Cost / Useful Life (0.20)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_048'
FILE_PATH = os.path.join(WORKDIR, 'finance', 'depreciation_2024.pdf')


def parse_currency(s):
    """Parse currency string like '$4,500.00' to float."""
    if s is None:
        return None
    s = str(s).strip().replace('$', '').replace(',', '')
    try:
        return float(s)
    except ValueError:
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all text from the PDF
    all_text = ""
    for page in doc:
        all_text += page.get_text("text")
    doc.close()

    # Shared variables used across components
    lines = all_text.split('\n')
    asset_id_pattern = re.compile(r'[A-Z]{1,4}[-_]?\d{2,5}')
    dollar_pattern = re.compile(r'\$[\d,]+\.\d{2}')

    # Component 1: PDF has meaningful content — at least 200 chars (0.10 points)
    # Initial env has no PDF so this fails; golden has a full depreciation table
    try:
        if len(all_text.strip()) >= 200:
            print(f"PASS: Component 1 — PDF has meaningful content ({len(all_text.strip())} chars) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — PDF text too short ({len(all_text.strip())} chars), expected >= 200")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Title/header references depreciation schedule (0.10 points)
    try:
        text_lower = all_text.lower()
        if 'depreciation' in text_lower and 'schedule' in text_lower:
            print(f"PASS: Component 2 — Title contains 'depreciation schedule' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Missing 'depreciation schedule' in title")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 8 required column headers present (0.20 points)
    # Columns: Asset ID, Description, Acquisition Date, Cost, Useful Life, Annual Depreciation,
    #          Accumulated Depreciation, Net Book Value
    try:
        required_columns = [
            'asset id',
            'description',
            'acquisition',  # "Acquisition Date" may be split
            'cost',
            'useful life',
            'annual',       # "Annual Depreciation"
            'accumulated',  # "Accumulated Depreciation"
            'net book',     # "Net Book Value"
        ]
        found_cols = 0
        for col in required_columns:
            if col in text_lower:
                found_cols += 1

        if found_cols == len(required_columns):
            print(f"PASS: Component 3 — All 8 required column headers found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Found {found_cols}/{len(required_columns)} column headers")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 10 asset data rows with proper structure (0.25 points)
    # PDF table rows may be in blocks or spread across lines. Use blocks for structured parsing.
    try:
        doc2 = pymupdf.open(file_path)
        blocks = doc2[0].get_text("blocks")
        doc2.close()

        # Count blocks that are data rows: contain asset ID + dollar values, not totals/notes
        data_rows = []
        for block in blocks:
            block_text = block[4] if len(block) > 4 else ""
            block_text = block_text.strip()
            if not block_text:
                continue
            if asset_id_pattern.search(block_text) and dollar_pattern.search(block_text):
                if 'total' not in block_text.lower() and 'note' not in block_text.lower():
                    data_rows.append(block_text)

        # Fallback: if blocks don't capture rows, count unique asset ID lines
        if len(data_rows) < 5:
            lines = all_text.split('\n')
            asset_ids = [l.strip() for l in lines if asset_id_pattern.match(l.strip()) and len(l.strip()) < 20]
            # Filter out header-like matches
            asset_ids = [a for a in asset_ids if 'asset' not in a.lower()]
            num_assets = len(asset_ids)
        else:
            num_assets = len(data_rows)

        if num_assets >= 10:
            print(f"PASS: Component 4 — Found {num_assets} asset data rows (0.25 pts)")
            total_score += 0.25
        elif num_assets >= 5:
            partial = round(0.25 * (num_assets / 10), 2)
            print(f"PARTIAL: Component 4 — Found {num_assets}/10 asset rows ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Found only {num_assets} asset data rows, expected 10")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Totals row present with aggregated values (0.15 points)
    try:
        if 'total' in text_lower:
            # Check blocks for a totals block with dollar values
            doc3 = pymupdf.open(file_path)
            blocks3 = doc3[0].get_text("blocks")
            doc3.close()
            totals_dollars = []
            for block in blocks3:
                bt = block[4] if len(block) > 4 else ""
                if 'total' in bt.lower():
                    totals_dollars = dollar_pattern.findall(bt)
                    break
            if len(totals_dollars) >= 2:
                print(f"PASS: Component 5 — Totals row found with {len(totals_dollars)} aggregated values (0.15 pts)")
                total_score += 0.15
            else:
                # Fallback: check lines near 'total' keyword
                totals_idx = next((i for i, l in enumerate(lines) if 'total' in l.lower()), None)
                if totals_idx is not None:
                    totals_region = ' '.join(lines[totals_idx:totals_idx+5])
                    dollars_nearby = dollar_pattern.findall(totals_region)
                    if len(dollars_nearby) >= 2:
                        print(f"PASS: Component 5 — Totals row found in region with {len(dollars_nearby)} values (0.15 pts)")
                        total_score += 0.15
                    else:
                        print(f"FAIL: Component 5 — Totals keyword found but insufficient dollar values nearby")
                else:
                    print(f"FAIL: Component 5 — No totals row found")
        else:
            print(f"FAIL: Component 5 — No 'totals' keyword found in PDF")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Mathematical correctness — Annual Depreciation = Cost / Useful Life (0.20 points)
    # Parse asset rows and verify straight-line depreciation math
    try:
        # Re-extract text as blocks for structured parsing
        doc2 = pymupdf.open(file_path)
        blocks = doc2[0].get_text("blocks")
        doc2.close()

        # Find data row blocks (those with asset IDs and dollar values)
        verified_count = 0
        checked_count = 0

        for block in blocks:
            block_text = block[4] if len(block) > 4 else ""
            block_text = block_text.strip()

            # Skip non-data blocks
            if not asset_id_pattern.search(block_text):
                continue
            if 'total' in block_text.lower() or 'note' in block_text.lower():
                continue

            # Extract dollar values from the block
            dollars = dollar_pattern.findall(block_text)
            if len(dollars) < 3:
                continue

            # Extract useful life (integer)
            # The block text typically contains: ID, Description, Date, Cost, UsefulLife, AnnualDep, AccumDep, NBV
            # Find all numbers that could be useful life (small integers 1-30)
            numbers = re.findall(r'\b(\d{1,2})\b', block_text)
            useful_life_candidates = [int(n) for n in numbers if 1 <= int(n) <= 30]

            if not useful_life_candidates or len(dollars) < 4:
                continue

            checked_count += 1

            # Parse values: Cost is typically first dollar, Annual Dep, Accum Dep, NBV follow
            cost = parse_currency(dollars[0])
            annual_dep = parse_currency(dollars[1])
            accum_dep = parse_currency(dollars[2])
            nbv = parse_currency(dollars[3])

            if cost is None or annual_dep is None:
                continue

            # Find the useful life that makes Annual Dep = Cost / Life
            dep_verified = any(
                abs(round(cost / ul, 2) - annual_dep) < 0.02
                for ul in useful_life_candidates
            )

            if dep_verified:
                verified_count += 1

            # Also verify NBV = Cost - Accum Dep (if available)
            if nbv is not None and accum_dep is not None and cost is not None:
                expected_nbv = round(cost - accum_dep, 2)
                if abs(expected_nbv - nbv) > 0.05:
                    # NBV doesn't match, but we still count annual dep correctness
                    pass

        if checked_count > 0 and verified_count >= checked_count * 0.8:
            print(f"PASS: Component 6 — Math verified for {verified_count}/{checked_count} assets (0.20 pts)")
            total_score += 0.20
        elif checked_count > 0 and verified_count > 0:
            partial = round(0.20 * (verified_count / checked_count), 2)
            print(f"PARTIAL: Component 6 — Math verified for {verified_count}/{checked_count} assets ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — Could not verify depreciation math (checked {checked_count} rows, verified {verified_count})")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
