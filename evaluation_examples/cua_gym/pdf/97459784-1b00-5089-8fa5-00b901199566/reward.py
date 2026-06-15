"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to rotate pages 2, 4, 6, 8, and 10 (all even pages) in 'duplex_scan.pdf' by 180 degrees. Save as 'scan_corrected.pdf' on Desktop.
Generated: 2025-11-29 09:46:34
Status: success
Model: o3
Total Steps: 11
"""

from pathlib import Path
from PyPDF2 import PdfReader

"""
Reward script for the task:
Rotate pages 2, 4, 6, 8, and 10 (all even pages) in 'duplex_scan.pdf' by 180°
and save the result as 'scan_corrected.pdf' on the Desktop.

The script verifies:
1. The corrected file exists at the expected location.
2. The PDF can be opened successfully.
3. The document still contains at least 10 pages (matching the original length).
4. Pages 2,4,6,8,10 are rotated by 180°, while pages 1,3,5,7,9 remain un-rotated.
   Each of the first ten pages is checked individually and awarded fractional
   credit so partial completion yields a partial score.

Scoring (max 1.0):
• 0.1 – corrected file exists.
• 0.1 – PDF has ≥10 pages.
• 0.8 – rotations on the first 10 pages (0.08 per page).
The script prints detailed diagnostics and always outputs a final line:
    REWARD: X.X
where X.X is the progressive score (exactly 1.0 for full success).
"""

def verify_task() -> float:
    target_path = Path("/home/user/Desktop/scan_corrected.pdf")
    total_score = 0.0

    # ------------------------------------------------------------------
    # 1. Check that the corrected PDF exists (0.1)
    # ------------------------------------------------------------------
    if target_path.exists():
        print(f"✓ Found corrected PDF at {target_path} (+0.1)")
        total_score += 0.1
    else:
        print(f"✗ Corrected PDF not found at {target_path}")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # 2. Try to open the PDF
    # ------------------------------------------------------------------
    try:
        reader = PdfReader(str(target_path))
    except Exception as exc:
        print(f"✗ Failed to open PDF: {exc}")
        print("REWARD: 0.0")
        return 0.0

    num_pages = len(reader.pages)
    print(f"PDF contains {num_pages} pages.")

    # ------------------------------------------------------------------
    # 3. Page-count sanity check (0.1)
    # ------------------------------------------------------------------
    if num_pages >= 10:
        print("✓ PDF has at least 10 pages (+0.1)")
        total_score += 0.1
    else:
        print("✗ PDF has fewer than 10 pages (0 points)")

    # ------------------------------------------------------------------
    # 4. Verify rotations on the first 10 pages (0.8 points total)
    # ------------------------------------------------------------------
    per_page_score = 0.8 / 10  # 0.08 each for pages 1-10

    for idx in range(min(10, num_pages)):
        page = reader.pages[idx]
        rotation = page.get("/Rotate")
        if rotation is None:
            rotation = 0
        rotation = rotation % 360  # normalise

        expected_rotation = 180 if (idx + 1) % 2 == 0 else 0  # 1-indexed pages

        if rotation == expected_rotation:
            total_score += per_page_score
            print(
                f"✓ Page {idx + 1}: rotation {rotation}° as expected (+{per_page_score:.2f})"
            )
        else:
            print(
                f"✗ Page {idx + 1}: rotation {rotation}°, expected {expected_rotation}°"
            )

    # ------------------------------------------------------------------
    # 5. Final score & output
    # ------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)  # keep within [0,1]
    print(f"Total score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()

