"""
FINAL REWARD SCRIPT - SUCCESS
Task: Merge all PDF files from /home/user/Documents/Certificates (completion_cert.pdf, participation_cert.pdf, excellence_cert.pdf) into 'all_certificates.pdf' on Desktop.
Generated: 2025-11-29 09:36:56
Status: success
Model: o3
Total Steps: 6
"""

#!/usr/bin/env python3
"""
Reward script for task:
"Merge all PDF files from /home/user/Documents/Certificates (completion_cert.pdf, participation_cert.pdf, excellence_cert.pdf) into 'all_certificates.pdf' on Desktop."

The script awards points for:
1. Merged file existence & readability (0.2)
2. Correct total page-count (0.3)
3. Presence of each certificate’s unique title text (0.3, split equally per keyword)
4. Correct ordering – Completion, Participation, Excellence (0.2)

Returns a float in [0,1] and prints detailed verification steps plus
"REWARD: X.X".
"""
from pathlib import Path
from PyPDF2 import PdfReader

def verify_pdf_merge() -> float:
    total_score = 0.0
    max_score   = 1.0

    # Weights for progressive scoring
    WEIGHTS = {
        'exists'          : 0.2,
        'page_count'      : 0.3,
        'keyword_presence': 0.3,  # divided equally among 3 keywords
        'ordering'        : 0.2,
    }

    merged_path = Path('/home/user/Desktop/all_certificates.pdf')
    source_dir  = Path('/home/user/Documents/Certificates')
    source_files = ['completion_cert.pdf', 'participation_cert.pdf', 'excellence_cert.pdf']

    # ------------------------------------------------------------------
    # 1. Existence & readability
    # ------------------------------------------------------------------
    if not merged_path.exists():
        print(f"✗ Merged PDF not found at {merged_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        reader = PdfReader(str(merged_path))
        print(f"✓ Loaded merged PDF ({len(reader.pages)} pages)")
        total_score += WEIGHTS['exists']
    except Exception as e:
        print(f"✗ Failed to read merged PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # 2. Page-count verification
    # ------------------------------------------------------------------
    expected_pages = 0
    for fname in source_files:
        fpath = source_dir / fname
        try:
            src_reader = PdfReader(str(fpath))
            expected_pages += len(src_reader.pages)
        except Exception as e:
            print(f"Warning: Could not open source {fpath}: {e}")

    if len(reader.pages) == expected_pages:
        print(f"✓ Page count matches expected ({expected_pages})")
        total_score += WEIGHTS['page_count']
    else:
        print(f"✗ Page count mismatch – expected {expected_pages}, found {len(reader.pages)}")

    # ------------------------------------------------------------------
    # 3. Keyword presence (unique title on each certificate)
    # ------------------------------------------------------------------
    keywords = [
        ('Completion'   , 'Certificate of Completion'),
        ('Participation', 'Certificate of Participation'),
        ('Excellence'   , 'Certificate of Excellence'),
    ]
    found_pages = {}
    per_keyword = WEIGHTS['keyword_presence'] / len(keywords)

    for idx, page in enumerate(reader.pages):
        text = (page.extract_text() or '')
        for key, label in keywords:
            if key not in found_pages and label in text:
                found_pages[key] = idx
                print(f"✓ Found '{label}' on page {idx + 1}")

    for key, _ in keywords:
        if key in found_pages:
            total_score += per_keyword
        else:
            print(f"✗ Missing page containing certificate for {key}")

    # ------------------------------------------------------------------
    # 4. Ordering check (only if all keywords were found)
    # ------------------------------------------------------------------
    if all(key in found_pages for key, _ in keywords):
        order = [found_pages['Completion'], found_pages['Participation'], found_pages['Excellence']]
        if order == sorted(order):
            print("✓ Certificates appear in correct order (Completion, Participation, Excellence)")
            total_score += WEIGHTS['ordering']
        else:
            print("✗ Certificates are not in the required order")
    else:
        print("Ordering check skipped due to missing certificates")

    final_score = min(total_score, max_score)
    print(f"REWARD: {final_score}")
    return final_score

# ----------------------------------------------------------------------
# Execute verification when run as a script
# ----------------------------------------------------------------------
if __name__ == '__main__':
    verify_pdf_merge()
