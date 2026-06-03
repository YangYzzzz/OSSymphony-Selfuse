"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please add an image watermark using 'logo.png' from Desktop to all pages of 'whitepaper.pdf', positioned at top-right corner with 50% opacity. Save as 'whitepaper_branded.pdf'.
Generated: 2025-11-29 09:45:34
Status: success
Model: o3
Total Steps: 11
"""

from pathlib import Path
import hashlib
from typing import List
from PyPDF2 import PdfReader

"""
Reward script for the PDF watermarking task.

Task to verify:
Add the image watermark `logo.png` (50 % opacity, top-right) on **every** page of
`whitepaper.pdf` and save the result as `whitepaper_branded.pdf`.

Verification strategy
--------------------
1. Locate both the original and branded PDFs on the Desktop (fallback to $HOME).
2. Load the two PDFs with PyPDF2 and make sure they have identical page counts.
3. For each page, collect MD5 hashes of every embedded image.  Any image that is
   present in the branded PDF but **not** in the corresponding original page is
   considered a newly-added candidate watermark.
4. Require **at least one** new image on every page – proves watermark presence.
5. Check that exactly one *identical* new image hash appears on every page –
   proves a uniform watermark (same logo, correct repetition).

Progressive Scoring (total 1.0)
--------------------------------
• 0.2 – Branded PDF exists AND page count matches the original.
• 0.4 – Each page of the branded PDF contains ≥1 new image compared to the
         original (watermark present everywhere).
• 0.4 – Exactly one identical new image hash appears on every page (uniform
         watermark).

No points are awarded for natural conditions (e.g., mere file existence).
The script prints detailed diagnostics and finally outputs
"REWARD: <float>" as required.
"""

def _find_file(filename: str) -> Path | None:
    """Search Desktop first, then the home directory, for *filename*."""
    home = Path.home()
    search_paths = [home / "Desktop", home]
    for directory in search_paths:
        candidate = directory / filename
        if candidate.exists():
            return candidate
    return None


def _image_hashes(page) -> List[str]:
    """Return MD5 hashes of all image XObjects embedded in *page*."""
    hashes = []
    resources = page.get("/Resources")
    if not resources:
        return hashes
    xobj = resources.get("/XObject")
    if not xobj:
        return hashes
    for _, ref in xobj.items():
        obj = ref.get_object()
        if obj.get("/Subtype") == "/Image":
            try:
                data = obj.get_data()
            except Exception:
                # Fallback – extremely rare, but keeps script robust
                data = None
            if data:
                hashes.append(hashlib.md5(data).hexdigest())
    return hashes


def verify_task() -> float:
    branded_pdf = _find_file("whitepaper_branded.pdf")
    original_pdf = _find_file("whitepaper.pdf")

    if not branded_pdf:
        print("✗ Branded PDF 'whitepaper_branded.pdf' not found")
        print("REWARD: 0.0")
        return 0.0

    print(f"Branded PDF located at: {branded_pdf}")
    branded_reader = PdfReader(str(branded_pdf))
    branded_pages = len(branded_reader.pages)

    total_score = 0.0

    # ──────────────────────────────────────────────────────────
    # 1. Page-count equality (0.2 points)
    # ──────────────────────────────────────────────────────────
    if original_pdf and original_pdf.exists():
        original_reader = PdfReader(str(original_pdf))
        original_pages = len(original_reader.pages)
        if branded_pages == original_pages and branded_pages > 0:
            print(f"✓ Page count matches original: {branded_pages} pages")
            total_score += 0.2
        else:
            print(f"✗ Page count mismatch – branded: {branded_pages}, original: {original_pages}")
    else:
        print("Original PDF not found – skipping page-count check")

    # Pre-load original reader once for efficiency
    original_reader = PdfReader(str(original_pdf)) if original_pdf and original_pdf.exists() else None

    # Containers for later uniformity check
    per_page_new_hashes: List[set[str]] = []
    watermark_on_all_pages = True

    # ──────────────────────────────────────────────────────────
    # 2. Watermark presence on every page (0.4 points)
    # ──────────────────────────────────────────────────────────
    for idx in range(branded_pages):
        branded_page = branded_reader.pages[idx]
        branded_hashes = set(_image_hashes(branded_page))

        original_hashes: set[str] = set()
        if original_reader:
            original_hashes = set(_image_hashes(original_reader.pages[idx]))

        new_hashes = branded_hashes - original_hashes  # candidate watermark images
        per_page_new_hashes.append(new_hashes)

        if new_hashes:
            print(f"✓ Page {idx + 1}: {len(new_hashes)} new image(s) detected")
        else:
            print(f"✗ Page {idx + 1}: NO new images – watermark missing")
            watermark_on_all_pages = False

    if watermark_on_all_pages and per_page_new_hashes:
        total_score += 0.4
    else:
        print("Watermark missing on one or more pages – no points for this criterion")

    # ──────────────────────────────────────────────────────────
    # 3. Uniform, single watermark across pages (0.4 points)
    # ──────────────────────────────────────────────────────────
    uniform = False
    if watermark_on_all_pages and per_page_new_hashes:
        first_page_hashes = per_page_new_hashes[0]
        if len(first_page_hashes) == 1:  # should be exactly one new image
            reference_hash = next(iter(first_page_hashes))
            uniform = all(len(h) == 1 and reference_hash in h for h in per_page_new_hashes)

    if uniform:
        print("✓ Identical single watermark detected on every page")
        total_score += 0.4
    else:
        print("✗ Watermark not uniform across pages – no points for this criterion")

    # ──────────────────────────────────────────────────────────
    final_score = min(total_score, 1.0)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()

