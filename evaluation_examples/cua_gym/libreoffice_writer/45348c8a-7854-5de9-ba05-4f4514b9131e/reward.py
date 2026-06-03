"""
Reward Script: Mail merge — generate 8 personalized PDF letters from Welcome_Letter.docx
Task ID: writer_mt_008
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Exactly 8 PDF files in ~/Desktop/Merged_Letters/
  Component 2 (0.3): Files named Welcome_Letter_1.pdf through Welcome_Letter_8.pdf
  Component 3 (0.4): Each PDF contains personalized content (FirstName, LastName, Department)
"""

import os
import csv

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_008'
MERGED_DIR = os.path.join(WORKDIR, 'Desktop', 'Merged_Letters')
CSV_PATH = os.path.join(WORKDIR, 'NewHires.csv')


def verify_task():
    """
    Verify mail merge task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the expected records from NewHires.csv
    try:
        with open(CSV_PATH, 'r') as f:
            reader = csv.DictReader(f)
            records = list(reader)
        print(f"INFO: Loaded {len(records)} records from NewHires.csv")
    except Exception as e:
        print(f"CRITICAL: Cannot load NewHires.csv: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check that Merged_Letters directory exists
    if not os.path.isdir(MERGED_DIR):
        print(f"FAIL: Directory {MERGED_DIR} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Exactly 8 PDF files exist in Merged_Letters (0.3 points)
    try:
        pdf_files = [f for f in os.listdir(MERGED_DIR) if f.lower().endswith('.pdf')]
        pdf_count = len(pdf_files)
        if pdf_count == 8:
            print(f"PASS: Component 1 — Found exactly 8 PDF files in Merged_Letters (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected 8 PDF files, found {pdf_count}: {pdf_files}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Files named Welcome_Letter_1.pdf through Welcome_Letter_8.pdf (0.3 points)
    try:
        expected_names = {f'Welcome_Letter_{i}.pdf' for i in range(1, 9)}
        actual_names = set(pdf_files)
        if expected_names == actual_names:
            print(f"PASS: Component 2 — All 8 files follow correct naming pattern (0.3 pts)")
            total_score += 0.3
        else:
            missing = expected_names - actual_names
            extra = actual_names - expected_names
            print(f"FAIL: Component 2 — Naming mismatch. Missing: {missing}, Extra: {extra}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each PDF contains personalized content from corresponding record (0.4 points)
    # Each PDF is worth 0.05 points (0.05 * 8 = 0.4)
    try:
        import fitz  # PyMuPDF
        personalization_score = 0.0
        per_pdf_weight = 0.4 / 8.0  # 0.05 per PDF

        for i in range(1, 9):
            pdf_path = os.path.join(MERGED_DIR, f'Welcome_Letter_{i}.pdf')
            if not os.path.exists(pdf_path):
                print(f"FAIL: Component 3.{i} — File {pdf_path} not found")
                continue

            try:
                doc = fitz.open(pdf_path)
                if len(doc) < 1:
                    print(f"FAIL: Component 3.{i} — PDF has no pages")
                    continue

                text = doc[0].get_text()
                record = records[i - 1]  # 0-indexed
                first_name = record.get('FirstName', '').strip()
                last_name = record.get('LastName', '').strip()
                department = record.get('Department', '').strip()

                has_first = first_name in text
                has_last = last_name in text
                has_dept = department in text

                if has_first and has_last and has_dept:
                    print(f"PASS: Component 3.{i} — PDF {i} contains {first_name} {last_name}, {department} ({per_pdf_weight:.3f} pts)")
                    personalization_score += per_pdf_weight
                else:
                    missing_fields = []
                    if not has_first:
                        missing_fields.append(f"FirstName='{first_name}'")
                    if not has_last:
                        missing_fields.append(f"LastName='{last_name}'")
                    if not has_dept:
                        missing_fields.append(f"Department='{department}'")
                    print(f"FAIL: Component 3.{i} — PDF {i} missing: {', '.join(missing_fields)}")
                doc.close()
            except Exception as e:
                print(f"ERROR: Component 3.{i} — Cannot read PDF {i}: {e}")

        total_score += personalization_score
        print(f"INFO: Component 3 subtotal — {personalization_score:.2f}/0.40")
    except ImportError:
        print("ERROR: Component 3 — PyMuPDF (fitz) not available, cannot verify PDF content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
