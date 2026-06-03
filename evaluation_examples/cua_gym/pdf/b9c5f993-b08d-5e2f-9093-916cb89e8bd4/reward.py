"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to OCR the table of contents from 'book_scan.pdf' (pages 5-8) in /home/user/Books and save the extracted chapter listings to 'toc.txt'.
Generated: 2025-11-29 10:08:57
Status: success
Model: o3
Total Steps: 5
"""

import re
from pathlib import Path
from PyPDF2 import PdfReader

def extract_chapter_lines(text: str):
    """Return lines that look like chapter listings from a text block."""
    lines = []
    for line in text.splitlines():
        cleaned = line.strip()
        # Pattern: Chapter <number>: <title>
        if re.match(r"^Chapter\s+\d+\s*:", cleaned, flags=re.IGNORECASE):
            lines.append(cleaned)
    return lines

def verify_toc(pdf_path: str, toc_path: str) -> float:
    """
    Verify that the OCR-extracted table-of-contents lines from pages 5-8 of
    `pdf_path` have been saved correctly to `toc_path`.

    Scoring (progressive):
      • Coverage (0.6): proportion of unique chapter lines from pages 5-8 that
        appear in toc.txt.
      • Cleanliness (0.4): penalises extra non-chapter lines in toc.txt.
    """
    print(f"Verifying table of contents extraction…\nPDF : {pdf_path}\nTOC : {toc_path}")
    total_score = 0.0

    # ----- Load PDF -----
    try:
        reader = PdfReader(pdf_path)
        print(f"✓ Loaded PDF successfully with {len(reader.pages)} pages")
    except Exception as e:
        print(f"✗ Failed to load PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ----- Extract chapter listings from pages 5-8 (indices 4-7) -----
    pdf_chapters = set()
    for idx in range(4, 8):  # pages 5-8 inclusive
        try:
            page = reader.pages[idx]
        except IndexError:
            print(f"✗ Missing expected page {idx + 1} in PDF")
            print("REWARD: 0.0")
            return 0.0
        text = page.extract_text() or ""
        found = extract_chapter_lines(text)
        pdf_chapters.update(found)
        print(f"Page {idx + 1}: {len(found)} chapter lines found")

    if not pdf_chapters:
        print("✗ No chapter lines detected in specified pages – OCR likely failed")
        print("REWARD: 0.0")
        return 0.0

    print(f"Unique chapter lines expected: {len(pdf_chapters)}")
    for ch in sorted(pdf_chapters):
        print("  •", ch)

    # ----- Load toc.txt -----
    toc_file = Path(toc_path)
    if not toc_file.exists():
        print("✗ toc.txt not found at expected location")
        print("REWARD: 0.0")
        return 0.0

    toc_content = toc_file.read_text(encoding="utf-8", errors="ignore")
    raw_lines = [ln.strip() for ln in toc_content.splitlines() if ln.strip()]
    toc_chapter_lines = [ln for ln in raw_lines if re.match(r"^Chapter\s+\d+\s*:", ln, flags=re.IGNORECASE)]
    extraneous_lines = [ln for ln in raw_lines if ln not in toc_chapter_lines]

    print(f"toc.txt total non-blank lines : {len(raw_lines)}")
    print(f"toc.txt chapter lines detected: {len(toc_chapter_lines)} (unique: {len(set(toc_chapter_lines))})")
    if extraneous_lines:
        print(f"Extraneous lines detected ({len(extraneous_lines)}):")
        for ln in extraneous_lines[:10]:  # show at most first 10
            print("  •", ln)
    else:
        print("✓ No extraneous lines detected in toc.txt")

    # ----- Scoring -----
    # Coverage (0.6)
    covered = [ch for ch in pdf_chapters if ch in toc_chapter_lines]
    coverage_ratio = len(covered) / len(pdf_chapters)
    coverage_score = 0.6 * coverage_ratio
    print(f"Coverage: {len(covered)}/{len(pdf_chapters)} -> {coverage_ratio:.2%} (score {coverage_score:.2f})")

    # Cleanliness (0.4)
    extraneous_ratio = len(extraneous_lines) / len(raw_lines) if raw_lines else 1.0
    cleanliness_score = 0.4 * max(0.0, 1.0 - extraneous_ratio)
    print(f"Extraneous ratio: {extraneous_ratio:.2%} -> cleanliness score {cleanliness_score:.2f}")

    total_score = coverage_score + cleanliness_score
    final_score = round(min(total_score, 1.0), 4)

    print(f"\nTotal verification score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score

# ------------- Entry point -------------
if __name__ == "__main__":
    verify_toc(
        "/home/user/Books/book_scan.pdf",
        "/home/user/Books/toc.txt",
    )
