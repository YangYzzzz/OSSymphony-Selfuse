"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please split 'proceedings.pdf' (300 pages) by bookmarks into separate PDF files in folder 'individual_papers' on Desktop, using bookmark names as filenames.
Generated: 2025-11-29 09:42:20
Status: success
Model: o3
Total Steps: 12
"""

from __future__ import annotations
"""Reward script for verifying that proceedings.pdf was split by bookmarks into
individual PDF files inside ~/Desktop/individual_papers, using the bookmark
names as the basis for each filename.

Scoring (progressive – max 1.0):
  • 0.3  – number of generated PDFs equals number of top-level bookmarks AND all
           generated PDFs are readable.
  • 0.4  – for every bookmark, the corresponding PDF has the exact expected
           number of pages (pro-rated).
  • 0.3  – filenames match (case-insensitive, after sanitising bookmark title)
           (pro-rated).
A perfect split therefore yields 1.0.
"""

import re
from pathlib import Path
from typing import Iterable, List, Tuple

from PyPDF2 import PdfReader

BASE_PDF = Path("/home/user/Desktop/proceedings.pdf")
OUTPUT_DIR = Path("/home/user/Desktop/individual_papers")


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _flatten_outlines(outlines: Iterable) -> Iterable:
    """Recursively yield all outline items (depth-first)."""
    for item in outlines:
        if isinstance(item, list):
            yield from _flatten_outlines(item)
        else:
            yield item


def _bookmark_title(item) -> str | None:
    """Extract the title text from various outline item representations."""
    if item is None:
        return None
    if isinstance(item, dict):
        return item.get("/Title")
    # Older PyPDF2 Destination objects expose .title
    return getattr(item, "title", None)


def _sanitize_variants(title: str) -> set[str]:
    """Generate several filename variants from a bookmark title."""
    raw = title.strip()
    # Basic replacements
    underscored = re.sub(r"\s+", "_", raw)
    # Remove characters that are illegal or troublesome in filenames
    safe = re.sub(r"[^A-Za-z0-9_-]", "", underscored)
    variants = {raw, underscored, safe}
    # All comparisons are lowercase & with .pdf extension
    return {v.lower() + ("" if v.lower().endswith(".pdf") else ".pdf") for v in variants}


# ---------------------------------------------------------------------------
# Core verification routine
# ---------------------------------------------------------------------------

def verify_split(base_pdf_path: str | Path, output_dir: str | Path) -> float:
    base_pdf_path = Path(base_pdf_path)
    output_dir = Path(output_dir)
    total_score = 0.0

    # ---------------------------------------------------------------------
    # 1) Load base PDF & gather top-level bookmarks
    # ---------------------------------------------------------------------
    try:
        reader = PdfReader(str(base_pdf_path))
        base_page_count = len(reader.pages)
        print(f"✓ Loaded base PDF (pages: {base_page_count})")
    except Exception as exc:
        print(f"✗ Cannot open base PDF – aborting verification: {exc}")
        return 0.0

    try:
        raw_outline = reader.outline  # PyPDF2 ≥3.0 preferred attribute
    except Exception as exc:
        print(f"✗ Failed to read outline/bookmarks: {exc}")
        return 0.0

    # Extract first-level bookmarks only
    top_level: List[Tuple[str, int]] = []  # (title, starting page index)
    for item in _flatten_outlines(raw_outline):
        title = _bookmark_title(item)
        if not title:
            continue
        # get_destination_page_number works on Destination objects; fall back for dicts
        try:
            page_index = reader.get_destination_page_number(item)  # type: ignore[arg-type]
        except Exception:
            try:
                dest_page_obj = item.get("/Page") if isinstance(item, dict) else None
                page_index = reader.pages.index(dest_page_obj.get_object()) if dest_page_obj else None
            except Exception:
                page_index = None
        if page_index is not None:
            top_level.append((title.strip(), page_index))

    if not top_level:
        print("✗ No bookmarks found – cannot verify split task")
        return 0.0

    # Order by page index just in case
    top_level.sort(key=lambda t: t[1])
    num_bookmarks = len(top_level)
    print(f"✓ Found {num_bookmarks} top-level bookmarks")

    # Derive expected page ranges per bookmark
    page_ranges: List[Tuple[str, int, int]] = []  # (title, start, end)
    for i, (title, start) in enumerate(top_level):
        end = top_level[i + 1][1] - 1 if i + 1 < num_bookmarks else base_page_count - 1
        page_ranges.append((title, start, end))
        print(f"  • '{title}' pages {start + 1}-{end + 1} (expect {end - start + 1})")

    # ---------------------------------------------------------------------
    # 2) Inspect output directory & PDFs
    # ---------------------------------------------------------------------
    if not output_dir.exists():
        print(f"✗ Expected output directory {output_dir} does not exist")
        return 0.0

    pdf_files = sorted(p for p in output_dir.iterdir() if p.suffix.lower() == ".pdf")
    if not pdf_files:
        print(f"✗ No PDF files found in {output_dir}")
        return 0.0

    readable: List[Tuple[Path, int]] = []  # (path, page count)
    for pdf in pdf_files:
        try:
            pg_cnt = len(PdfReader(str(pdf)).pages)
            readable.append((pdf, pg_cnt))
        except Exception as exc:
            print(f"✗ Unable to open {pdf.name}: {exc}")

    # 2A) Basic count & readability score (0.3)
    if len(readable) == len(pdf_files) == num_bookmarks:
        print("✓ File count equals bookmark count & all files readable (0.3)")
        total_score += 0.3
    else:
        print("✗ Count/readability mismatch – 0 points for this section")

    # ---------------------------------------------------------------------
    # 3) Match each bookmark to a PDF by name & page count
    # ---------------------------------------------------------------------
    matched_pages = 0
    matched_names = 0
    for idx, (title, start, end) in enumerate(page_ranges):
        expected_pages = end - start + 1
        variants = _sanitize_variants(title)

        # Try to find by filename variant first
        match: Tuple[Path, int] | None = next(
            ((path, cnt) for path, cnt in readable if path.name.lower() in variants),
            None,
        )
        # Fallback: use ordinal position if count matches number of bookmarks
        if match is None and len(readable) == num_bookmarks and idx < len(readable):
            match = readable[idx]

        if match:
            path, cnt = match
            if path.name.lower() in variants:
                matched_names += 1
            if cnt == expected_pages:
                matched_pages += 1
                print(f"✓ {path.name}: page count {cnt} matches expected {expected_pages}")
            else:
                print(f"✗ {path.name}: page count {cnt} ≠ expected {expected_pages}")
        else:
            print(f"✗ No PDF found corresponding to bookmark '{title}'")

    # 3A) Page-count accuracy score (0.4 proportionally)
    page_score = 0.4 * (matched_pages / num_bookmarks)
    total_score += page_score
    print(f"Page-count score: {page_score:.2f} ({matched_pages}/{num_bookmarks} correct)")

    # 3B) Filename accuracy score (0.3 proportionally)
    name_score = 0.3 * (matched_names / num_bookmarks)
    total_score += name_score
    print(f"Filename score: {name_score:.2f} ({matched_names}/{num_bookmarks} match)")

    final = min(total_score, 1.0)
    print(f"REWARD: {final}")
    return final


# ---------------------------------------------------------------------------
# Script entry-point – run verification immediately when executed standalone
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_split(BASE_PDF, OUTPUT_DIR)
