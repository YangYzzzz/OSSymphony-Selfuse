"""
FINAL REWARD SCRIPT - SUCCESS
Task: I need to OCR the German text in 'german_document.pdf' on Desktop and save to 'german_text.txt', using German language model for better accuracy.
Generated: 2025-11-29 10:08:04
Status: success
Model: o3
Total Steps: 5
"""

from pathlib import Path
from PyPDF2 import PdfReader
import re
import unicodedata

# -------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------

def clean_text(text: str) -> str:
    """Lower-cases and collapses whitespace so texts become comparable."""
    return re.sub(r"\s+", " ", text).strip().lower()


def strip_accents(text: str) -> str:
    """Remove accents so e.g. 'Sprache' and 'Spräche' compare equal."""
    return "".join(
        ch for ch in unicodedata.normalize("NFD", text) if unicodedata.category(ch) != "Mn"
    )


def extract_keywords(pdf_text: str, min_len: int = 6, max_keywords: int = 8):
    """Pick up to *max_keywords* reasonably long, unique words from the PDF text.
    We later ensure those words also appear in the OCR output. """
    words = re.findall(r"[A-Za-zÄÖÜäöüß]+", pdf_text)
    long_words = [w for w in words if len(w) >= min_len]
    seen, keywords = set(), []
    for w in long_words:
        wl = w.lower()
        if wl not in seen:
            seen.add(wl)
            keywords.append(w)
            if len(keywords) >= max_keywords:
                break
    return keywords

# -------------------------------------------------------------
# Core verification routine
# -------------------------------------------------------------

def verify_ocr_task(pdf_path: Path, txt_candidate_paths: list[Path]) -> float:
    """Verifies that german_text.txt is a good-quality OCR of german_document.pdf.
    Returns a progressive score between 0 and 1."""

    max_score = 1.0
    score = 0.0

    # ---------- 1) Read reference PDF ----------
    try:
        reader = PdfReader(str(pdf_path))
        pdf_text_raw = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        print(f"✗ Could not read PDF '{pdf_path}': {exc}")
        print("REWARD: 0.0")
        return 0.0

    pdf_text_clean = clean_text(pdf_text_raw)
    print(f"PDF cleaned length: {len(pdf_text_clean)} characters")

    # Derive keywords from the PDF to check for actual content match
    keywords = extract_keywords(pdf_text_raw)
    if not keywords:
        print("✗ Failed to derive verification keywords from PDF – aborting")
        print("REWARD: 0.0")
        return 0.0
    print(f"Verification keywords: {keywords}")

    # ---------- 2) Locate OCR text file ----------
    txt_path = next((p for p in txt_candidate_paths if p.exists()), None)
    if not txt_path:
        print("✗ german_text.txt not found in expected location(s)")
        print("REWARD: 0.0")
        return 0.0

    try:
        txt_content_raw = txt_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        print(f"✗ Could not read text file '{txt_path}': {exc}")
        print("REWARD: 0.0")
        return 0.0

    txt_content_clean = clean_text(txt_content_raw)
    print(f"TXT cleaned length: {len(txt_content_clean)} characters")

    # ---------- 3) Scoring ----------

    # 3A) File existence & non-empty (0.2)
    if txt_content_clean:
        score += 0.2
        print("✓ german_text.txt exists and is non-empty (+0.20)")
    else:
        print("✗ german_text.txt is empty (0 points)")

    # 3B) Length coverage relative to PDF (up to 0.2)
    if pdf_text_clean:
        length_ratio = len(txt_content_clean) / len(pdf_text_clean)
        print(f"Length ratio OCR/PDF: {length_ratio:.2f}")
        if length_ratio >= 0.8:
            score += 0.2
            print("✓ OCR text length ≧ 80 % of PDF (+0.20)")
        elif length_ratio >= 0.5:
            score += 0.1
            print("• OCR text length ≧ 50 % of PDF (+0.10)")
        else:
            print("✗ OCR text too short (0 points)")

    # 3C) Keyword presence (up to 0.6)
    found_keywords = 0
    txt_no_accents = strip_accents(txt_content_clean)
    for kw in keywords:
        if strip_accents(kw.lower()) in txt_no_accents:
            print(f"✓ Found keyword '{kw}'")
            found_keywords += 1
        else:
            print(f"✗ Missing keyword '{kw}'")
    coverage = found_keywords / len(keywords)
    keyword_points = 0.6 * coverage
    score += keyword_points
    print(f"Keyword coverage: {found_keywords}/{len(keywords)} → +{keyword_points:.2f}")

    # ---------- 4) Final score ----------
    final_score = round(min(score, max_score), 2)
    print(f"REWARD: {final_score}")
    return final_score

# -------------------------------------------------------------
# Entry point – paths are hard-coded per task description
# -------------------------------------------------------------
if __name__ == "__main__":
    pdf = Path("/home/user/Desktop/german_document.pdf")
    # The user could have saved the text either on Desktop or in the home directory
    txt_candidates = [
        Path("/home/user/Desktop/german_text.txt"),
        Path("/home/user/german_text.txt"),
    ]
    verify_ocr_task(pdf, txt_candidates)
