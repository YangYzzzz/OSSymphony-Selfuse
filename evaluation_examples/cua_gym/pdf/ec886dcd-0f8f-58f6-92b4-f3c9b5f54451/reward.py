"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract all visible text from the form 'application_form.pdf' on Desktop, including field labels and filled-in values, and save to 'form_data.txt'.
Generated: 2025-11-29 09:11:37
Status: success
Model: o3
Total Steps: 6
"""

"""
Reward script for task:
Extract all visible text from the form 'application_form.pdf' on Desktop, including field labels and filled-in values, and save to 'form_data.txt'.

The script verifies task completion by:
1. Ensuring both the source PDF and the newly-created TXT file exist in the expected locations.
2. Using PyPDF2 to extract *visible* text from every page of the PDF (no form-field key lookup – only what a reader would see).
3. Normalising both the PDF-extracted text and the contents of the TXT file (trim whitespace, collapse multiple spaces, drop blank lines).
4. Awarding progressive points:
   • 0.1 – required files found (TXT presence proves extraction attempt)
   • 0.2 – non-empty visible text successfully extracted from the PDF
   • 0.2 – TXT file contains non-empty lines
   • 0.5 – TXT lines perfectly match the normalised visible text from the PDF
     (If all PDF lines appear in order in the TXT but extra/different lines exist, 0.3 is given instead.)
5. Printing detailed diagnostics and the final float score in the format:  "REWARD: X.X".

The script never hard-codes success, uses no forbidden modules, and gives 1.0 only when the extraction is perfect.
"""
from pathlib import Path
import re
from typing import List
from PyPDF2 import PdfReader

def _normalise_lines(text: str) -> List[str]:
    """Collapse consecutive whitespace & drop blank lines for fair comparison."""
    out: List[str] = []
    for line in text.split("\n"):
        cleaned = re.sub(r"\s+", " ", line).strip()
        if cleaned:
            out.append(cleaned)
    return out

def verify_extraction(pdf_path: str, txt_path: str) -> float:
    """Return a progressive score 0.0–1.0 based on how well the TXT mirrors PDF text."""
    max_score = 1.0
    score = 0.0

    pdf = Path(pdf_path)
    txt = Path(txt_path)

    # ---------- Requirement 1: artefacts present ----------
    if pdf.exists() and txt.exists():
        # TXT is the key new artefact; credit only if both present.
        print("✓ Both PDF and extracted TXT files found (0.1 points)")
        score += 0.1
    else:
        missing = pdf_path if not pdf.exists() else txt_path
        print(f"✗ Missing required file: {missing}")
        print(f"REWARD: {score}")
        return score  # Early exit – cannot proceed without artefacts

    # ---------- Requirement 2: extract visible text from PDF ----------
    try:
        reader = PdfReader(str(pdf))
        pdf_visible_text = "\n".join((page.extract_text() or "") for page in reader.pages)
        pdf_lines = _normalise_lines(pdf_visible_text)
        if pdf_lines:
            print(f"✓ Extracted {len(pdf_lines)} non-empty text lines from PDF (0.2 points)")
            score += 0.2
        else:
            print("✗ No visible text detected in PDF – task obviously failed")
            print(f"REWARD: {score}")
            return score
    except Exception as e:
        print(f"✗ Error reading PDF: {e}")
        print(f"REWARD: {score}")
        return score

    # ---------- Requirement 3: read & normalise TXT file ----------
    try:
        txt_content = txt.read_text(encoding="utf-8", errors="ignore")
        txt_lines = _normalise_lines(txt_content)
        if txt_lines:
            print(f"✓ Extracted text file contains {len(txt_lines)} non-empty lines (0.2 points)")
            score += 0.2
        else:
            print("✗ TXT file is empty – task not completed")
            print(f"REWARD: {score}")
            return score
    except Exception as e:
        print(f"✗ Cannot read TXT file: {e}")
        print(f"REWARD: {score}")
        return score

    # ---------- Requirement 4: content comparison ----------
    if pdf_lines == txt_lines:
        score += 0.5
        print("✓ TXT perfectly matches PDF visible text (0.5 points)")
    else:
        # Allow partial credit if all PDF lines appear in order within TXT
        idx = 0
        all_found = True
        for line in pdf_lines:
            found = False
            while idx < len(txt_lines):
                if txt_lines[idx] == line:
                    found = True
                    idx += 1
                    break
                idx += 1
            if not found:
                all_found = False
                break
        if all_found:
            score += 0.3
            print("✓ TXT contains all PDF lines but with extra / ordering differences (0.3 points)")
        else:
            print("✗ TXT does not fully contain the PDF text – no additional points")

    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score

# ----------------------------
# Execute verification when run
# ----------------------------
if __name__ == "__main__":
    PDF_PATH = "/home/user/Desktop/application_form.pdf"  # source PDF path
    TXT_PATH = "/home/user/Desktop/form_data.txt"          # expected TXT output
    verify_extraction(PDF_PATH, TXT_PATH)
