"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please perform OCR with high accuracy mode on the legal document 'court_filing.pdf' on Desktop and save to 'filing_text.txt', preserving paragraph structure.
Generated: 2025-11-29 10:11:48
Status: success
Model: o3
Total Steps: 13
"""

"""Reward script for verifying OCR extraction of court_filing.pdf -> filing_text.txt
Scoring rubric (total 1.0):
  • 0.2 – filing_text.txt exists and is non-empty
  • 0.1 – paragraph structure preserved (≥1 blank line between blocks)
  • 0.2 – extracted text length ≥ 80 % of golden PDF text
  • 0.5 – textual similarity with golden PDF (≥0.9 → +0.5, ≥0.8 → +0.35, ≥0.7 → +0.25, ≥0.6 → +0.15)
The golden PDF path is deterministic and supplied by the evaluation harness.
The script never awards points for natural conditions such as mere file existence of the PDF; all points reflect true task accomplishments.
"""

from pathlib import Path
import re
import difflib
from PyPDF2 import PdfReader

# ---------------- Helper functions ---------------- #

def _read_text(path: Path) -> str:
    """Read text file with UTF-8 fallback; return empty string on failure."""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        print(f"✗ Failed to read {path}: {exc}")
        return ""

def _pdf_to_text(pdf_path: Path) -> str:
    """Extract raw text from all pages of a PDF using PyPDF2."""
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        print(f"✗ Could not open PDF {pdf_path}: {exc}")
        return ""

    pages = []
    for idx, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        print(f"Page {idx}: {len(page_text)} chars extracted")
        pages.append(page_text)
    return "\n".join(pages)

def _normalize(text: str) -> str:
    """Collapse all whitespace and lowercase – aids robust similarity checks."""
    return re.sub(r"\s+", " ", text).strip().lower()

def _similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()

# ---------------- Verification routine ---------------- #

def verify_task() -> float:
    score = 0.0

    # 1) Locate golden PDF (deterministic path provided by evaluator)
    pdf_path = Path("/home/user/please_perform_ocr_with_high_accuracy_mode_on_the_legal_document_court_filingpdf_on_desktop_and_save_golden.pdf")
    if not pdf_path.exists():
        print(f"✗ Expected golden PDF not found at {pdf_path}")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Golden PDF located at {pdf_path}")

    golden_norm = _normalize(_pdf_to_text(pdf_path))
    print(f"Golden text length (normalized): {len(golden_norm)} characters")

    # 2) Locate filing_text.txt (expected on Desktop, but search a few common paths)
    candidate_paths = [
        Path("/home/user/Desktop/filing_text.txt"),
        Path("/home/user/filing_text.txt"),
        Path("/home/user/Documents/filing_text.txt"),
    ]
    filing_path = next((p for p in candidate_paths if p.exists()), None)
    if filing_path is None:
        # fallback: limited recursive search
        for p in Path("/home/user").rglob("filing_text.txt"):
            filing_path = p
            break

    if filing_path is None or not filing_path.exists():
        print("✗ filing_text.txt not found anywhere under /home/user")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Found filing_text.txt at {filing_path}")

    user_raw = _read_text(filing_path)
    user_norm = _normalize(user_raw)

    # ---------- Scoring ---------- #
    # A) File is non-empty (0.2)
    if user_norm:
        score += 0.2
        print("✓ filing_text.txt is non-empty (+0.2)")
    else:
        print("✗ filing_text.txt is empty → cannot award points")
        print(f"REWARD: {score}")
        return score

    # B) Paragraph structure: at least one blank line present (0.1)
    if re.search(r"\n\s*\n", user_raw):
        score += 0.1
        print("✓ Detected blank line separation (paragraph structure) (+0.1)")
    else:
        print("✗ No blank lines detected between paragraphs (0 points)")

    # C) Length coverage ≥ 80 % of golden text (0.2)
    if len(user_norm) >= 0.8 * len(golden_norm):
        score += 0.2
        print("✓ User text length ≥ 80 % of golden (+0.2)")
    else:
        print("✗ User text shorter than 80 % of golden (0 points)")

    # D) Textual similarity (up to 0.5)
    sim = _similarity(user_norm, golden_norm)
    print(f"Similarity ratio: {sim:.3f}")
    if sim >= 0.90:
        score += 0.5
        print("✓ High similarity ≥ 0.90 (+0.5)")
    elif sim >= 0.80:
        score += 0.35
        print("✓ Moderate-high similarity ≥ 0.80 (+0.35)")
    elif sim >= 0.70:
        score += 0.25
        print("✓ Moderate similarity ≥ 0.70 (+0.25)")
    elif sim >= 0.60:
        score += 0.15
        print("✓ Low similarity ≥ 0.60 (+0.15)")
    else:
        print("✗ Similarity below 0.60 (0 points)")

    final_score = min(score, 1.0)
    print(f"REWARD: {final_score}")
    return final_score

# --------------- Execute when run directly --------------- #
if __name__ == "__main__":
    verify_task()
