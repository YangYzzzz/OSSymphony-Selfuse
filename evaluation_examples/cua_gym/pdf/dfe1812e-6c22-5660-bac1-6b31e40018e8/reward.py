"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to merge all PDFs in subfolders of /home/user/Documents/Projects into one PDF per subfolder, naming each merged PDF after its folder name.
Generated: 2025-11-29 10:15:59
Status: success
Model: o3
Total Steps: 4
"""

from pathlib import Path
from PyPDF2 import PdfReader

ROOT_DIR = Path('/home/user/Documents/Projects')

def verify_merge(root_dir: Path = ROOT_DIR) -> float:
    """Verify that every immediate sub-folder of `root_dir` contains **one merged PDF**
    named exactly after that folder (e.g. `Alpha/Alpha.pdf`).  The merged file must
    contain *all* pages of the other PDFs in the same folder.

    Scoring (per qualifying sub-folder – i.e. a folder that holds ≥2 PDFs):
        • 0.5 pts – `merged PDF` exists and its name (case-insensitive) equals
                    `<folder>.pdf`
        • 0.5 pts – page-count of the merged PDF equals the sum of pages of the
                    remaining PDFs in that folder

    The final reward is the **average** across all qualifying folders, capped at 1.0.
    """

    if not root_dir.exists():
        print(f"✗ Root directory {root_dir} does not exist – task incomplete")
        print("REWARD: 0.0")
        return 0.0

    subfolders = [p for p in root_dir.iterdir() if p.is_dir()]
    if not subfolders:
        print("✗ No subfolders found underneath Projects – nothing to verify")
        print("REWARD: 0.0")
        return 0.0

    total_possible = 0.0  # total points that could be earned
    total_scored = 0.0    # points actually earned

    for folder in sorted(subfolders):
        pdfs = list(folder.glob('*.pdf'))
        # Need at least two PDFs to consider merging meaningful
        if len(pdfs) < 2:
            continue

        total_possible += 1.0
        folder_score = 0.0

        expected_merged_name = f"{folder.name}.pdf".lower()
        merged_pdf = next((p for p in pdfs if p.name.lower() == expected_merged_name), None)

        print(f"\nFolder: {folder.name}")

        # --------------- Existence & naming (0.5) ---------------
        if merged_pdf and merged_pdf.exists():
            print(f" ✓ Merged PDF found: {merged_pdf.name} (0.5 pts)")
            folder_score += 0.5
        else:
            print(" ✗ Correctly-named merged PDF not found (0 pts)")

        # --------------- Page-count integrity (0.5) ---------------
        try:
            source_pdfs = [p for p in pdfs if p != merged_pdf]
            source_pages = sum(len(PdfReader(str(p)).pages) for p in source_pdfs)

            if merged_pdf and merged_pdf.exists():
                merged_pages = len(PdfReader(str(merged_pdf)).pages)
                print(f"   Source pages: {source_pages} | Merged pages: {merged_pages}")
                if merged_pages == source_pages and merged_pages > 0:
                    print(" ✓ Page counts match (0.5 pts)")
                    folder_score += 0.5
                else:
                    print(" ✗ Page count mismatch (0 pts)")
            else:
                print("   Skipping page-count check – merged PDF missing")
        except Exception as e:
            print(f"   Error while reading PDFs: {e}")

        total_scored += folder_score

    if total_possible == 0:
        print("No qualifying sub-folders with ≥2 PDFs; score is 0.0")
        print("REWARD: 0.0")
        return 0.0

    final_score = round(min(total_scored / total_possible, 1.0), 2)
    print(f"\nOverall score: {total_scored} / {total_possible}")
    print(f"REWARD: {final_score}")
    return final_score

if __name__ == "__main__":
    verify_merge()

