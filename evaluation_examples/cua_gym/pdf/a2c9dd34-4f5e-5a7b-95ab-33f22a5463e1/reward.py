"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract the medication schedule table from 'patient_chart.pdf' and save to 'medication_schedule.csv' on Desktop.
Generated: 2025-11-29 09:24:24
Status: success
Model: o3
Total Steps: 9
"""

import csv
from pathlib import Path

def verify_medication_schedule_csv():
    """Verify that the medication schedule table was correctly extracted
    from patient_chart.pdf into medication_schedule.csv on the Desktop.

    Scoring rubric (1.0 max):
        • 0.0  – CSV missing / unreadable
        • 0.2  – CSV file exists and is readable
        • 0.3  – Required column headers present in correct left-to-right order
        • 0.5  – All three expected data rows present in correct order after headers
    """

    total_score = 0.0
    max_score   = 1.0

    # Expected file location
    csv_path = Path("/home/user/Desktop/medication_schedule.csv")

    # ------------------------------------------------------------
    # 1) Check that the CSV file exists and can be opened (0.2 pts)
    # ------------------------------------------------------------
    if not csv_path.exists():
        print(f"✗ CSV file not found at {csv_path}")
        print("REWARD:", 0.0)
        return 0.0

    print(f"✓ CSV file located: {csv_path}")
    total_score += 0.2  # File existence is meaningful (task output)

    # ------------------------------------------------------------
    # 2) Load CSV contents safely
    # ------------------------------------------------------------
    try:
        with csv_path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
    except Exception as exc:
        print(f"✗ Failed to read CSV – {exc}")
        print("REWARD:", total_score)
        return total_score

    # Flatten all non-empty cells for flexible searching
    flat_cells = [cell.strip() for row in rows for cell in row if cell.strip()]
    print(f"Total non-empty cells found: {len(flat_cells)}")

    # ------------------------------------------------------------
    # 3) Verify required headers in correct order (0.3 pts)
    # ------------------------------------------------------------
    required_headers = [
        "Medication",
        "Dosage",
        "Frequency",
        "Start Date",
        "End Date",
    ]

    header_indices = []
    last_idx = -1
    for header in required_headers:
        try:
            idx = next(i for i, val in enumerate(flat_cells)
                        if i > last_idx and val.lower() == header.lower())
            header_indices.append(idx)
            last_idx = idx
        except StopIteration:
            header_indices = []  # Invalidate if any header missing/out of order
            break

    if header_indices and len(header_indices) == len(required_headers):
        print(f"✓ Headers present in correct order @ positions {header_indices}")
        total_score += 0.3
    else:
        print("✗ Required headers missing or out of order")

    # ------------------------------------------------------------
    # 4) Verify medication rows after headers (up to 0.5 pts)
    # ------------------------------------------------------------
    expected_rows = [
        ["Aspirin",   "100 mg", "Daily",        "2023-01-01", "2023-01-31"],
        ["Metformin", "500 mg", "Twice Daily", "2023-02-01", "2023-06-01"],
        ["Lisinopril", "10 mg", "Daily",       "2023-03-15", "2023-09-15"],
    ]

    # Start searching after the last header position (if headers found); else start at 0
    search_pointer = header_indices[-1] + 1 if header_indices else 0
    found_rows = 0

    for row in expected_rows:
        found = False
        for i in range(search_pointer, len(flat_cells) - len(row) + 1):
            if all(flat_cells[i + j].lower() == row[j].lower() for j in range(len(row))):
                found = True
                search_pointer = i + len(row)  # Enforce order
                break
        if found:
            found_rows += 1
            print(f"✓ Row found: {row}")
        else:
            print(f"✗ Missing row: {row}")

    if found_rows:
        row_score = (found_rows / len(expected_rows)) * 0.5
        total_score += row_score

    # ------------------------------------------------------------
    # Final score
    # ------------------------------------------------------------
    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print("REWARD:", final_score)
    return final_score

# Run verification when executed directly
if __name__ == "__main__":
    verify_medication_schedule_csv()
