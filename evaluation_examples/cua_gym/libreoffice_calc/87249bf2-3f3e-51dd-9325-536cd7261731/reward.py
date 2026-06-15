"""
Reward Script: Multi-app terminal task — merge student_ids.xlsx + raw_scores.ods,
               normalize scores, rank, output grades.csv, open in LibreOffice Calc.
Task ID: osworld_multi_apps_terminal_calc_012
Domain: libreoffice_calc / multi_apps_terminal
Scoring:
  Component 1: grades.csv has correct 4-column header (0.25 pts)
  Component 2: All 15 students present with correct StudentIDs (0.25 pts)
  Component 3: NormalizedScore values correct using min-max normalization 0-100 (0.25 pts)
  Component 4: Rank column correct — students sorted descending by NormalizedScore (0.25 pts)
Total: 1.0
"""

import os
import csv

WORKDIR = '/home/user/Desktop'
GRADES_FILE = os.path.join(WORKDIR, 'grades.csv')

# Expected data: all 15 StudentIDs from student_ids.xlsx (S001-S015)
EXPECTED_STUDENT_IDS = {
    'S001', 'S002', 'S003', 'S004', 'S005',
    'S006', 'S007', 'S008', 'S009', 'S010',
    'S011', 'S012', 'S013', 'S014', 'S015'
}

# Raw scores from raw_scores.ods (in order S001..S015 by student_ids index)
# S001=78, S002=92, S003=65, S004=88, S005=45, S006=73, S007=95,
# S008=61, S009=84, S010=57, S011=91, S012=70, S013=82, S014=48, S015=77
RAW_SCORES = {
    'S001': 78, 'S002': 92, 'S003': 65, 'S004': 88, 'S005': 45,
    'S006': 73, 'S007': 95, 'S008': 61, 'S009': 84, 'S010': 57,
    'S011': 91, 'S012': 70, 'S013': 82, 'S014': 48, 'S015': 77
}

def compute_normalized_score(raw, min_raw=45, max_raw=95):
    """Min-max normalization to 0-100 scale."""
    return (raw - min_raw) / (max_raw - min_raw) * 100


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: grades.csv not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load CSV
    try:
        with open(file_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames if reader.fieldnames else []
    except Exception as e:
        print(f"CRITICAL: Cannot parse {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct 4-column header (0.25 points)
    # Expected: StudentID, RawScore, NormalizedScore, Rank
    try:
        expected_headers = ['StudentID', 'RawScore', 'NormalizedScore', 'Rank']
        # Case-insensitive comparison
        actual_headers = [h.strip() for h in fieldnames] if fieldnames else []
        actual_lower = [h.lower() for h in actual_headers]
        expected_lower = [h.lower() for h in expected_headers]

        if actual_lower == expected_lower:
            print(f"PASS: Component 1 — Correct 4-column header: {actual_headers} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected headers {expected_headers}, found {actual_headers}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 15 students present with correct StudentIDs (0.25 points)
    try:
        found_ids = set()
        for row in rows:
            sid = row.get('StudentID', '').strip()
            if sid:
                found_ids.add(sid)

        missing = EXPECTED_STUDENT_IDS - found_ids
        extra = found_ids - EXPECTED_STUDENT_IDS

        if len(rows) == 15 and not missing and not extra:
            print(f"PASS: Component 2 — All 15 students present with correct IDs (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Row count: {len(rows)}, Missing IDs: {missing}, Extra IDs: {extra}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: NormalizedScore values correct (min-max 0-100) (0.25 points)
    # Min raw = 45, Max raw = 95; formula: (raw - 45) / (95 - 45) * 100
    try:
        normalization_correct = True
        normalization_errors = []

        for row in rows:
            try:
                sid = row.get('StudentID', '').strip()
                raw_val = row.get('RawScore', '').strip()
                norm_val = row.get('NormalizedScore', '').strip()

                if not sid or not raw_val or not norm_val:
                    normalization_correct = False
                    normalization_errors.append(f"{sid}: missing values")
                    continue

                raw_score = float(raw_val)
                norm_score = float(norm_val)
                expected_norm = compute_normalized_score(raw_score)

                if abs(norm_score - expected_norm) > 0.1:
                    normalization_correct = False
                    normalization_errors.append(
                        f"{sid}: expected norm={expected_norm:.2f}, got {norm_score:.2f}"
                    )
            except (ValueError, TypeError) as ve:
                normalization_correct = False
                normalization_errors.append(f"Parse error for row {row}: {ve}")

        if normalization_correct:
            print(f"PASS: Component 3 — All NormalizedScore values correct (min-max 0-100) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — NormalizedScore errors: {normalization_errors[:5]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Rank column correct — ordered descending by NormalizedScore,
    # ranks are 1..15 matching position (0.25 points)
    try:
        rank_correct = True
        rank_errors = []

        # Validate that ranks are integers 1..15 and match sorting order
        norm_rank_pairs = []
        for row in rows:
            try:
                norm_val = float(row.get('NormalizedScore', 0))
                rank_val = int(row.get('Rank', 0))
                norm_rank_pairs.append((norm_val, rank_val))
            except (ValueError, TypeError) as ve:
                rank_correct = False
                rank_errors.append(f"Parse error: {ve}")

        if rank_correct and len(norm_rank_pairs) == 15:
            # Check ranks are 1..15 inclusive
            rank_values = [r for _, r in norm_rank_pairs]
            if sorted(rank_values) != list(range(1, 16)):
                rank_correct = False
                rank_errors.append(f"Ranks not 1..15: {sorted(rank_values)}")
            else:
                # Check ranks match descending NormalizedScore order
                # Sort by NormalizedScore descending, expected rank = position+1
                sorted_by_norm = sorted(norm_rank_pairs, key=lambda x: -x[0])
                for expected_rank, (norm, actual_rank) in enumerate(sorted_by_norm, start=1):
                    if actual_rank != expected_rank:
                        rank_correct = False
                        rank_errors.append(
                            f"NormalizedScore={norm:.2f}: expected rank={expected_rank}, got rank={actual_rank}"
                        )

        if rank_correct:
            print(f"PASS: Component 4 — Rank column correct, sorted descending by NormalizedScore (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Rank errors: {rank_errors[:5]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
if not os.path.exists(GRADES_FILE):
    print(f"File not found: {GRADES_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(GRADES_FILE)
