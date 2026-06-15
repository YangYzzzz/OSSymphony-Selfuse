"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to extract all tables from the research paper 'experimental_data.pdf' in /home/user/Research and save each table as a separate CSV file named 'table_1.csv', 'table_2.csv', etc.
Generated: 2025-11-29 09:18:20
Status: success
Model: o3
Total Steps: 12
"""

# Reward script for verifying table extraction task
# Task: Extract all tables from experimental_data.pdf and save as table_1.csv, table_2.csv, ...
# Author: Autonomous verification agent

from pathlib import Path
import re
import csv
from PyPDF2 import PdfReader

#######################################################################
# Helper functions                                                    #
#######################################################################

def extract_tables_info(pdf_path: str):
    """Parse the PDF and return basic metadata for every detected table.

    We look for heading patterns of the form "Table N:" (case-insensitive)
    and capture some header lines that immediately follow each heading.
    This information will later be compared against the corresponding CSV
    headers to ensure the right data were exported.
    """
    reader = PdfReader(pdf_path)
    full_text = "\n".join(page.extract_text() or "" for page in reader.pages)

    # Regex to locate each table heading
    pattern = re.compile(r"Table\s+(\d+)\s*:?\s*(.*?)\n", re.IGNORECASE)
    tables = []

    for match_idx, m in enumerate(pattern.finditer(full_text)):
        table_num = int(m.group(1))
        title = m.group(2).strip()

        # Text segment belonging to this table (until next heading or EOF)
        seg_start = m.end()
        next_match = pattern.search(full_text, pos=seg_start)
        seg_end = next_match.start() if next_match else len(full_text)
        segment = full_text[seg_start:seg_end]

        # Collect a handful of non-empty lines that most likely represent
        # the table header / first rows (max 5 lines).
        header_lines = []
        for line in segment.splitlines():
            cleaned = line.strip()
            if cleaned:
                header_lines.append(cleaned)
            if len(header_lines) >= 5:
                break

        tables.append({
            "number": table_num,
            "title": title,
            "header_lines": header_lines,
        })

    return tables


def _tokenize(text: str):
    """Return a set of lowercase alphabetic tokens (>1 char)."""
    return {tok.lower() for tok in re.split(r"[^A-Za-z]+", text) if len(tok) > 1}


def verify_csv_for_table(csv_path: Path, table_info: dict) -> float:
    """Score a single CSV against the corresponding table information.

    Scoring breakdown (max 1.0 per table):
      • 0.3  – CSV is readable & non-empty (basic existence of export)
      • 0.4  – Header tokens match those detected in PDF (proportional)
      • 0.3  – At least 2 data rows (very small tables still get partial credit)
    """
    try:
        rows = list(csv.reader(csv_path.open(newline="", encoding="utf-8")))
    except Exception as exc:
        print(f"✗ Failed to read {csv_path}: {exc}")
        return 0.0

    if not rows:
        print(f"✗ {csv_path} is empty")
        return 0.0

    # ---- Header verification ----------------------------------------
    header_tokens_csv = set()
    for row in rows[:3]:  # inspect first 3 rows for header words
        for cell in row:
            header_tokens_csv.update(_tokenize(cell))

    # Expected tokens come from PDF header lines (excluding very generic words)
    generic = {"table", "experimental", "data", "environmental",
               "conditions", "measurements"}
    expected_tokens = set()
    for line in table_info["header_lines"]:
        expected_tokens.update(_tokenize(line))
    expected_tokens -= generic

    matched = expected_tokens & header_tokens_csv
    header_score = (len(matched) / len(expected_tokens)) if expected_tokens else 0.0

    # ---- Row-count verification -------------------------------------
    data_rows = rows[1:] if len(rows) > 1 else []
    row_score = 1.0 if len(data_rows) >= 2 else 0.0

    # ---- Aggregate per-table score ----------------------------------
    table_score = 0.3 + 0.4 * header_score + 0.3 * row_score
    table_score = min(table_score, 1.0)

    print(f"Header tokens in {csv_path.name}: {sorted(header_tokens_csv)}")
    print(f"Expected tokens: {sorted(expected_tokens)} — matched {len(matched)}/{len(expected_tokens)}")
    print(f"Data rows: {len(data_rows)} – Table score: {table_score:.2f}\n")

    return table_score

#######################################################################
# Main verification routine                                           #
#######################################################################

def verify_task() -> float:
    pdf_path = "/home/user/Research/experimental_data.pdf"
    csv_dir = Path("/home/user/Research")

    # -------- Parse PDF for table metadata ---------------------------
    tables = extract_tables_info(pdf_path)
    if not tables:
        print("✗ No table headings detected in PDF – task appears incomplete")
        print("REWARD: 0.0")
        return 0.0

    print(f"Detected {len(tables)} table(s) in PDF: {[t['number'] for t in tables]}")

    # -------- Verify each expected CSV -------------------------------
    total_score = 0.0
    for tbl in tables:
        num = tbl["number"]
        csv_path = csv_dir / f"table_{num}.csv"

        if not csv_path.exists():
            print(f"✗ Missing CSV for table {num}: {csv_path}")
            # No score added for this missing table (implicitly 0)
            continue

        print(f"✓ Found CSV for table {num}: {csv_path}")
        total_score += verify_csv_for_table(csv_path, tbl)

    # Average score across all detected tables to get final reward
    final_score = round(total_score / len(tables), 2)
    print(f"Final aggregated score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score

#######################################################################
# Entrypoint                                                          #
#######################################################################

if __name__ == "__main__":
    verify_task()

