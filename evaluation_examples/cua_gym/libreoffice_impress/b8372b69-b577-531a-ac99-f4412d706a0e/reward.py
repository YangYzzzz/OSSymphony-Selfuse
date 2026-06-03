"""
FINAL REWARD SCRIPT - SUCCESS
Task: Export the document to PDF with watermark text 'DRAFT' at 45°.
Generated: 2025-10-17 16:25:12
Status: success
Model: azure-o3
Total Steps: 19
"""

import os
import re
import math
from typing import Tuple

try:
    import PyPDF2
except ImportError:  # Safety-net – PyPDF2 should be available in the VM
    PyPDF2 = None

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def _extract_page_stream_text(page) -> str:
    """Extract **raw decoded** content stream text from a PyPDF2 page.
    This is lower-level than extract_text() and lets us inspect graphics /
    text-matrix operators (Tm, cm) to infer rotation angles.
    """
    try:
        contents = page.get_contents()
        if contents is None:
            return ""

        # PyPDF2 ≥ 3 returns a ContentStream object exposing get_data()
        if hasattr(contents, "get_data"):
            raw_bytes = contents.get_data()
        # Sometimes we get the bytes directly
        elif isinstance(contents, bytes):
            raw_bytes = contents
        # Older PyPDF2 can return a list-like of indirect objects / streams
        elif hasattr(contents, "__iter__"):
            parts = []
            for c in contents:
                if hasattr(c, "get_data"):
                    parts.append(c.get_data())
                elif isinstance(c, bytes):
                    parts.append(c)
            raw_bytes = b"".join(parts)
        else:
            raw_bytes = bytes(contents)

        return raw_bytes.decode("latin1", errors="ignore")
    except Exception:
        # Any problem -> treat as empty string
        return ""


def _detect_watermark_text(page, keyword: str = "DRAFT") -> bool:
    """True if *keyword* is found in the page (either via extract_text()
    or by scanning the raw stream).  Case-insensitive.
    """
    kw = keyword.lower()

    # 1) High-level text extraction
    try:
        txt = (page.extract_text() or "").lower()
        if kw in txt:
            return True
    except Exception:
        pass  # fall through to raw stream

    # 2) Raw content stream scan
    raw = _extract_page_stream_text(page).lower()
    return kw in raw


def _detect_45_deg_rotation(stream_text: str) -> bool:
    """Inspect graphics/text matrices in *stream_text* to see if any angle is
    approximately 45° (or –135°, which looks the same). We look for six numbers
    followed by the Tm or cm operator.
    """
    matrix_regex = re.compile(
        r"([-]?\d*\.?\d+)\s+([-]?\d*\.?\d+)\s+([-]?\d*\.?\d+)\s+([-]?\d*\.?\d+)\s+([-]?\d*\.?\d+)\s+([-]?\d*\.?\d+)\s+(Tm|cm)"
    )

    for m in matrix_regex.finditer(stream_text):
        try:
            a, b, c, d = map(float, m.groups()[:4])
        except ValueError:
            continue  # corrupt numbers – skip

        angle = math.degrees(math.atan2(b, a))  # from matrix elements
        # Normalise to –180 … 180
        while angle <= -180:
            angle += 360
        while angle > 180:
            angle -= 360

        # 45° or –135° both give the visual 45° orientation
        if abs(angle - 45) < 5 or abs(angle + 135) < 5:
            return True
    return False

# ------------------------------------------------------------
# Core verification functions
# ------------------------------------------------------------

def verify_pdf(pdf_path: str, keyword: str = "DRAFT") -> Tuple[float, str]:
    """Return (progressive_score, verbose_details) for *pdf_path*.
    Scoring rubric:
      • 0.6  – keyword watermark present
      • 0.3  – ~45° rotation detected
      • 0.1  – filename indicates correct export
      → Perfect score = 1.0
    """
    if PyPDF2 is None:
        return 0.0, "PyPDF2 library unavailable"

    if not os.path.isfile(pdf_path):
        return 0.0, "PDF file not found"

    # Try reading the PDF
    try:
        reader = PyPDF2.PdfReader(pdf_path)
    except Exception as e:
        return 0.0, f"Unable to open PDF: {e}"

    watermark_ok = False
    rotation_ok = False

    for page in reader.pages:
        if not watermark_ok:
            watermark_ok = _detect_watermark_text(page, keyword)
        if not rotation_ok:
            rotation_ok = _detect_45_deg_rotation(_extract_page_stream_text(page))
        if watermark_ok and rotation_ok:  # done early if both satisfied
            break

    score = 0.0
    details = []

    if watermark_ok:
        score += 0.6
        details.append("Watermark found")
    else:
        details.append("Watermark NOT found")

    if rotation_ok:
        score += 0.3
        details.append("≈45° rotation detected")
    else:
        details.append("45° rotation NOT detected")

    # Bonus for correctly-named file (helps pick the intended file if many PDFs exist)
    stem = os.path.splitext(os.path.basename(pdf_path))[0].lower()
    if stem == "export_the_document_to_pdf_with_watermark_text_draft_at_45_golden" or "draft" in stem:
        score += 0.1
        details.append("Filename matches requirement")

    return min(score, 1.0), "; ".join(details)


def _gather_candidate_pdfs(root_dir: str = "/home/user"):
    """Yield potential PDF paths inside *root_dir* (skip site-packages etc.)."""
    for root, _, files in os.walk(root_dir):
        if "/.local/" in root or "/site-packages/" in root:
            continue  # ignore library resources
        for f in files:
            if f.lower().endswith(".pdf"):
                yield os.path.join(root, f)


# ------------------------------------------------------------
# Main entry point
# ------------------------------------------------------------

def main() -> float:
    expected = "/home/user/export_the_document_to_pdf_with_watermark_text_draft_at_45_golden.pdf"

    # Build candidate list – expected path first (if present), then others
    candidates = [expected] if os.path.isfile(expected) else []
    candidates.extend(_gather_candidate_pdfs())

    best_score = 0.0
    best_details = ""
    best_path = ""

    for pdf in candidates:
        # Skip common Matplotlib resource PDFs – irrelevant to the task
        if "/mpl-data/" in pdf:
            continue
        score, details = verify_pdf(pdf)
        if score > best_score:
            best_score, best_details, best_path = score, details, pdf

    # floating-point safety
    if abs(best_score - 1.0) < 1e-9:
        best_score = 1.0

    print(f"Best candidate PDF: {best_path or 'None'}")
    print(f"Verification details: {best_details}")
    print(f"REWARD: {best_score}")

    return best_score


if __name__ == "__main__":
    # Execute verification when run as script
    main()
