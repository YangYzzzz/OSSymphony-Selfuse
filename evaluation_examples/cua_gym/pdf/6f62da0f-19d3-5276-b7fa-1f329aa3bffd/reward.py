"""
FINAL REWARD SCRIPT - SUCCESS
Task: Convert the multi-page TIFF file 'scanned_document.tiff' in /home/user/Downloads to PDF 'scanned_document.pdf'.
Generated: 2025-11-29 09:28:54
Status: success
Model: o3
Total Steps: 13
"""

"""
Reward script for verifying conversion of a multi-page TIFF file to a PDF.
-----------------------------------------------------------------------
Scoring rubric (weights add to 1.0):
  • PDF file exists ............................................. 0.10
  • PDF page-count matches number of TIFF frames ............... 0.35
  • Every PDF page contains at least one embedded image ........ 0.35
  • PDF page aspect-ratio roughly matches TIFF image ........... 0.20
The script prints detailed diagnostics and ends with:
    REWARD: <score>
exactly one floating-point value in [0.0, 1.0].
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from PyPDF2 import PdfReader, generic
from PIL import Image


def _count_tiff_frames(tiff_path: Path) -> int | None:
    """Return number of frames in TIFF or None if unreadable/missing."""
    if not tiff_path.exists():
        print("✗ TIFF source file missing – cannot count frames")
        return None
    try:
        with Image.open(tiff_path) as img:
            frames = 0
            while True:
                try:
                    img.seek(frames)
                    frames += 1
                except EOFError:
                    break
        return frames
    except Exception as exc:  # pragma: no cover
        print(f"Failed to read TIFF: {exc}")
        return None


def _page_image_counts(reader: PdfReader) -> List[int]:
    """Return list with number of /Image XObjects per PDF page."""
    counts: List[int] = []
    for idx, page in enumerate(reader.pages):
        image_count = 0
        try:
            resources = page.get("/Resources") or {}
            if isinstance(resources, generic.IndirectObject):
                resources = resources.get_object()
            xobj = resources.get("/XObject") or {}
            if isinstance(xobj, generic.IndirectObject):
                xobj = xobj.get_object()
            for name in xobj:
                try:
                    obj = xobj[name]
                    if isinstance(obj, generic.IndirectObject):
                        obj = obj.get_object()
                    if obj.get("/Subtype") == "/Image":
                        image_count += 1
                except Exception:
                    # Ignore corrupt objects but continue counting others
                    pass
        except Exception:
            # If resources missing treat as zero images
            pass
        print(f"Page {idx + 1}: {image_count} image(s) detected")
        counts.append(image_count)
    return counts


def verify_tiff_to_pdf(tiff_path: str, pdf_path: str) -> float:
    """Verify conversion task and return a progressive score in [0.0, 1.0]."""
    print("Verifying TIFF to PDF conversion")
    print(f"TIFF path: {tiff_path}\nPDF  path: {pdf_path}")

    # Scoring weights --------------------------------------------------
    weights = {
        "existence": 0.10,
        "page_count": 0.35,
        "images": 0.35,
        "dimensions": 0.20,
    }
    score = 0.0

    tiff = Path(tiff_path).expanduser()
    pdf = Path(pdf_path).expanduser()

    # 1) PDF existence -------------------------------------------------
    if pdf.exists():
        print("✓ PDF file exists")
        score += weights["existence"]
    else:
        print("✗ PDF file does not exist – cannot proceed with full verification")
        print(f"REWARD: {score}")
        return score  # early exit – nothing else can be verified

    # 2) Read PDF ------------------------------------------------------
    try:
        reader = PdfReader(str(pdf))
        num_pdf_pages = len(reader.pages)
        print(f"PDF pages: {num_pdf_pages}")
    except Exception as exc:
        print(f"✗ Failed to open PDF: {exc}")
        print(f"REWARD: {score}")
        return score

    # 3) TIFF frame count + page-count consistency --------------------
    num_tiff_frames = _count_tiff_frames(tiff)
    if num_tiff_frames is not None and num_tiff_frames == num_pdf_pages and num_pdf_pages > 0:
        print("✓ PDF page-count matches TIFF frames")
        score += weights["page_count"]
    else:
        print("✗ Page-count mismatch (TIFF frames vs PDF pages)")

    # 4) Verify embedded image per page -------------------------------
    image_counts = _page_image_counts(reader)
    if image_counts and all(c > 0 for c in image_counts):
        print("✓ Every page contains at least one embedded image")
        score += weights["images"]
    else:
        print("✗ One or more pages lack embedded image content")

    # 5) Rough aspect-ratio comparison --------------------------------
    dims_ok = True
    if num_tiff_frames is not None:
        try:
            with Image.open(str(tiff)) as img0:
                tw, th = img0.size  # pixels
            tiff_ratio = round(tw / th, 2) if th else None
            for idx, page in enumerate(reader.pages):
                box = page.mediabox
                pw, ph = float(box.width), float(box.height)
                pdf_ratio = round(pw / ph, 2) if ph else None
                if tiff_ratio is None or pdf_ratio is None or abs(tiff_ratio - pdf_ratio) > 0.05:
                    print(
                        f"Page {idx + 1}: aspect-ratio mismatch – TIFF {tiff_ratio}, PDF {pdf_ratio}"
                    )
                    dims_ok = False
                    break
            if dims_ok:
                print("✓ PDF page aspect-ratios align with TIFF images")
                score += weights["dimensions"]
        except Exception as exc:  # pragma: no cover
            print(f"Aspect-ratio check failed: {exc}")
    else:
        print("(Aspect-ratio check skipped – TIFF unreadable)")

    # -----------------------------------------------------------------
    final = round(min(score, 1.0), 4)
    print(f"Final score: {final}/1.0")
    print(f"REWARD: {final}")
    return final


if __name__ == "__main__":
    # Absolute task paths (as per instructions)
    TIFF_FILE = "/home/user/Downloads/scanned_document.tiff"
    PDF_FILE = "/home/user/Downloads/scanned_document.pdf"
    verify_tiff_to_pdf(TIFF_FILE, PDF_FILE)
