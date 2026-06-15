"""
FINAL REWARD SCRIPT - SUCCESS
Task: I have 8 signed contract pages as separate PDFs (signature_page_1.pdf through signature_page_8.pdf) in /home/user/Documents/Contracts. Merge them into 'signed_contract.pdf' in order.
Generated: 2025-11-29 09:37:07
Status: success
Model: o3
Total Steps: 1
"""

from pathlib import Path
from PyPDF2 import PdfReader
import hashlib

"""
Reward Script for Task:
"I have 8 signed contract pages as separate PDFs (signature_page_1.pdf through
 signature_page_8.pdf) in /home/user/Documents/Contracts. Merge them into
 'signed_contract.pdf' in order."

Verification Logic
------------------
1.  Ensure all eight source PDFs exist (prerequisite, no points awarded).
2.  Verify that the merged file `signed_contract.pdf` exists AND contains exactly
    eight pages (0.3 points).
3.  For each page 1-8, compare the merged page with the corresponding source
    page to confirm:
       • Text content is identical **OR**
       • The raw contents stream hash matches (fallback when text extraction is
         empty—common for scanned/signature PDFs).
    Each correctly-matching page earns an equal share of the remaining
    0.7 points (0.7 ÷ 8 ≈ 0.0875 apiece).
4.  The final reward is the sum of all earned points, capped at 1.0.

The script prints detailed diagnostics for every check and always outputs the
final score in the required format:  "REWARD: X.X".
"""

def _contents_hash(page):
    """Return MD5 of a page's /Contents stream(s) or None on error."""
    try:
        contents = page.get("/Contents")
        if contents is None:
            return None
        data = b""
        if isinstance(contents, list):
            for obj in contents:
                data += obj.get_object().get_data()
        else:
            data = contents.get_object().get_data()
        return hashlib.md5(data).hexdigest()
    except Exception:
        return None

def verify_signed_contract() -> float:
    contract_dir = Path("/home/user/Documents/Contracts")
    merged_path = contract_dir / "signed_contract.pdf"
    source_files = [contract_dir / f"signature_page_{i}.pdf" for i in range(1, 9)]

    total_score = 0.0
    max_score = 1.0

    # ---------- Prerequisite: all source PDFs present ----------
    missing = [str(p) for p in source_files if not p.exists()]
    if missing:
        print(f"✗ Missing source PDFs: {missing}")
        print("REWARD: 0.0")
        return 0.0

    # ---------- Requirement 1: merged PDF exists with 8 pages ----------
    if not merged_path.exists():
        print("✗ Merged file 'signed_contract.pdf' not found")
        print("REWARD: 0.0")
        return 0.0

    try:
        merged_reader = PdfReader(merged_path)
    except Exception as exc:
        print(f"✗ Failed to read merged PDF: {exc}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(merged_reader.pages)
    if page_count == 8:
        print("✓ Merged file has 8 pages (0.3 points)")
        total_score += 0.3
    else:
        print(f"✗ Merged file page count is {page_count}, expected 8")

    # ---------- Requirement 2: per-page content & order check ----------
    per_page_score = 0.7 / 8.0  # ≈ 0.0875 each

    for idx, src_path in enumerate(source_files):
        if idx >= page_count:
            print(f"✗ Merged PDF missing page {idx + 1}")
            continue

        # Load pages
        src_page = PdfReader(src_path).pages[0]
        merged_page = merged_reader.pages[idx]

        # Compare via text first
        src_text = (src_page.extract_text() or "").strip()
        merged_text = (merged_page.extract_text() or "").strip()
        pages_match = False

        if src_text and merged_text:
            pages_match = src_text == merged_text
        else:
            # Fallback to raw content hash comparison
            pages_match = _contents_hash(src_page) == _contents_hash(merged_page)

        if pages_match:
            total_score += per_page_score
            print(f"✓ Page {idx + 1} matches source (+{per_page_score:.3f})")
        else:
            print(f"✗ Page {idx + 1} does NOT match source")

    final_score = round(min(total_score, max_score), 4)
    print(f"REWARD: {final_score}")
    return final_score

# --------------- Execute verification when run directly ---------------
if __name__ == "__main__":
    verify_signed_contract()

