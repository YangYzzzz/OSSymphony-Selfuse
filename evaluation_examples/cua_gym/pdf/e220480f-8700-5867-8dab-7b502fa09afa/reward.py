"""
FINAL REWARD SCRIPT - SUCCESS
Task: Convert the scanned presentation slides 'slides_scan.pdf' on Desktop to searchable PDF 'slides_searchable.pdf', preserving original page images with OCR text layer.
Generated: 2025-11-29 10:08:45
Status: success
Model: o3
Total Steps: 8
"""

from pathlib import Path
from PyPDF2 import PdfReader
import hashlib
import difflib

"""
Reward script for the task:
"Convert the scanned presentation slides 'slides_scan.pdf' on Desktop to searchable PDF
 'slides_searchable.pdf', preserving original page images with OCR text layer."

Scoring logic (progressive up to 1.0):
 1. If the produced PDF is byte-identical to the golden answer → 1.0 instantly.
 2. Otherwise, award partial credit for:
    • page-count matching original scan (+0.25)
    • page-dimensions matching original scan on first few pages (+0.15)
    • OCR coverage – text present on ≥90 % pages (+0.45) or ≥50 % (+0.25)
    • average OCR characters per page (≥50 chars → +0.15, ≥20 chars → +0.05)

No points are ever given for natural conditions (e.g., file merely existing).
The script prints detailed diagnostics and always outputs a single line
"REWARD: X.X" where X.X ∈ [0.0, 1.0].
"""

# Paths (adjust only if task spec changes)
DESKTOP = Path.home() / "Desktop"
CANDIDATE_PATH = DESKTOP / "slides_searchable.pdf"
SCAN_PATH = DESKTOP / "slides_scan.pdf"
GOLDEN_PATH = Path(
    "/home/user/convert_the_scanned_presentation_slides_slides_scanpdf_on_desktop_to_searchable_pdf_slides_searchabl_golden.pdf"
)


def md5(path: Path, chunk: int = 8192) -> str:
    """Return MD5 hash of a file (binary-safe, streamed)."""
    h = hashlib.md5()
    with path.open("rb") as f:
        for blk in iter(lambda: f.read(chunk), b""):
            h.update(blk)
    return h.hexdigest()


def verify_task() -> float:
    total = 0.0

    # 0) Candidate existence (prerequisite: no points)
    if not CANDIDATE_PATH.exists():
        print(f"✗ Missing searchable PDF at {CANDIDATE_PATH}")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Found candidate PDF: {CANDIDATE_PATH}")

    # 1) Perfect match with golden ⇒ immediate success
    if GOLDEN_PATH.exists():
        cand_hash = md5(CANDIDATE_PATH)
        gold_hash = md5(GOLDEN_PATH)
        print(f"Candidate MD5: {cand_hash}")
        print(f"Golden    MD5: {gold_hash}")
        if cand_hash == gold_hash:
            print("✓ Candidate PDF matches golden exactly. Full credit awarded ✔")
            print("REWARD: 1.0")
            return 1.0
        print("Hash mismatch – doing detailed checks …")
    else:
        print("Golden reference missing – resorting to heuristic checks …")

    # Safe load of PDFs
    try:
        cand_reader = PdfReader(str(CANDIDATE_PATH))
    except Exception as e:
        print(f"✗ Failed to open candidate PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # 2) Page-count comparison with original scan
    if SCAN_PATH.exists():
        try:
            scan_pages = len(PdfReader(str(SCAN_PATH)).pages)
            cand_pages = len(cand_reader.pages)
            if cand_pages == scan_pages:
                print(f"✓ Page count matches original scan: {cand_pages} pages (+0.25)")
                total += 0.25
            else:
                print(
                    f"✗ Page count differs (scan={scan_pages} vs searchable={cand_pages})"
                )
        except Exception as e:
            print(f"Warning: could not open scan PDF for page-count check: {e}")
    else:
        print("Original scan PDF missing – skipping page-count comparison.")

    # 3) Page-dimension consistency on first three pages
    if SCAN_PATH.exists():
        try:
            scan_reader = PdfReader(str(SCAN_PATH))
            dims_ok = True
            for idx in range(min(3, len(cand_reader.pages))):
                c_box = cand_reader.pages[idx].mediabox
                s_box = scan_reader.pages[idx].mediabox
                if not (
                    abs(c_box.width - s_box.width) < 2 and abs(c_box.height - s_box.height) < 2
                ):
                    dims_ok = False
                    break
            if dims_ok:
                print("✓ Page dimensions match scan on sampled pages (+0.15)")
                total += 0.15
            else:
                print("✗ Page dimensions differ from scan (no points)")
        except Exception as e:
            print(f"Warning: dimension check failed: {e}")

    # 4) OCR coverage & quality
    text_pages = 0
    total_chars = 0
    for i, page in enumerate(cand_reader.pages, start=1):
        txt = (page.extract_text() or "").strip()
        n_chars = len(txt)
        total_chars += n_chars
        if n_chars >= 20:
            text_pages += 1
        print(f"Page {i}: {n_chars} OCR chars")

    num_pages = len(cand_reader.pages)
    coverage = text_pages / num_pages if num_pages else 0
    avg_chars = total_chars / num_pages if num_pages else 0

    if coverage >= 0.9:
        total += 0.45
        print(f"✓ OCR text on {coverage*100:.1f}% pages (+0.45)")
    elif coverage >= 0.5:
        total += 0.25
        print(f"✓ OCR text on {coverage*100:.1f}% pages (+0.25)")
    else:
        print(f"✗ OCR coverage low ({coverage*100:.1f}% pages)")

    # 5) Average characters per page – quality nuance
    if avg_chars >= 50:
        total += 0.15
        print(f"✓ Average {avg_chars:.1f} OCR chars per page (+0.15)")
    elif avg_chars >= 20:
        total += 0.05
        print(f"✓ Average {avg_chars:.1f} OCR chars per page (+0.05)")
    else:
        print(f"✗ Very low OCR density ({avg_chars:.1f} chars/page)")

    # Cap at 1.0
    final_score = min(total, 1.0)
    print(f"Total score: {final_score:.2f}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()

