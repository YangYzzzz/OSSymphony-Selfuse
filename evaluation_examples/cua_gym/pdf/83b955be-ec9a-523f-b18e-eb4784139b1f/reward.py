"""
FINAL REWARD SCRIPT - SUCCESS
Task: Convert all Word documents (.docx files) in /home/user/Documents/Reports to PDF, saving them in folder 'Reports_PDF' with same filenames.
Generated: 2025-11-29 10:12:26
Status: success
Model: o3
Total Steps: 14
"""

from pathlib import Path
from PyPDF2 import PdfReader


def verify_conversion() -> float:
    """Reward script for task:
    Convert all .docx files in /home/user/Documents/Reports to PDFs with the
    same basename, saving them inside /home/user/Documents/Reports_PDF.

    Scoring (progressive):
        • 1.0  – every source .docx has a non-empty PDF counterpart and the
                  destination folder exists.
        • <1.0 – partial completion based on coverage/readability.
        • 0.0  – destination folder missing or no successes.
    """

    source_dir = Path('/home/user/Documents/Reports')
    dest_dir   = Path('/home/user/Documents/Reports_PDF')

    # ------------------------------------------------------------------
    # Requirement 0: destination directory must exist (prerequisite)
    # ------------------------------------------------------------------
    if dest_dir.exists() and dest_dir.is_dir():
        print(f"✓ Destination directory present: {dest_dir}")
        dest_exists = True
    else:
        print(f"✗ Destination directory missing: {dest_dir}")
        dest_exists = False

    # ------------------------------------------------------------------
    # Discover source DOCX files (ignore sub-folders; task scope = top level)
    # ------------------------------------------------------------------
    if source_dir.exists() and source_dir.is_dir():
        docx_files = sorted([p for p in source_dir.glob('*.docx')])
    else:
        docx_files = []

    total_docs = len(docx_files)
    print(f"Found {total_docs} .docx file(s) in {source_dir}")

    # ------------------------------------------------------------------
    # Special case: no source documents
    # Task is considered complete iff destination folder exists (nothing to do)
    # ------------------------------------------------------------------
    if total_docs == 0:
        final_score = 1.0 if dest_exists else 0.0
        verdict = "trivially satisfied" if final_score == 1.0 else "failed"
        print(f"No source documents – task {verdict}.")
        print(f"REWARD: {final_score}")
        return final_score

    # ------------------------------------------------------------------
    # Requirement 1 & 2: PDF counterpart exists and is readable (≥1 page)
    # ------------------------------------------------------------------
    converted_matches = 0  # PDFs that exist for each DOCX
    readable_pdfs     = 0  # PDFs that open & contain ≥1 page

    for docx_path in docx_files:
        target_pdf = dest_dir / f"{docx_path.stem}.pdf"
        if target_pdf.exists():
            converted_matches += 1
            try:
                reader = PdfReader(str(target_pdf))
                num_pages = len(reader.pages)
                print(f"  ✓ {target_pdf.name} exists with {num_pages} page(s)")
                if num_pages > 0:
                    readable_pdfs += 1
                else:
                    print("    ✗ PDF has 0 pages (should have at least 1)")
            except Exception as e:
                print(f"    ✗ Failed to open PDF {target_pdf.name}: {e}")
        else:
            print(f"  ✗ Missing PDF for {docx_path.name}")

    # ------------------------------------------------------------------
    # Progressive scoring
    #   80% weight – conversion coverage (PDF existence)
    #   20% weight – PDF readability (non-empty)
    # ------------------------------------------------------------------
    conversion_rate = converted_matches / total_docs
    readable_rate   = readable_pdfs     / total_docs

    score = 0.8 * conversion_rate + 0.2 * readable_rate

    # If destination directory absent, zero out score (cannot succeed)
    if not dest_exists:
        score = 0.0

    final_score = round(min(score, 1.0), 4)

    print(f"Conversion coverage: {conversion_rate:.2%}")
    print(f"Readable PDFs:       {readable_rate:.2%}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_conversion()

