"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please convert the PDF 'invoice_template.pdf' on Desktop to an editable LibreOffice Writer document 'invoice_template.odt'.
Generated: 2025-11-29 09:31:28
Status: success
Model: o3
Total Steps: 18
"""

import zipfile
import re
import html
from pathlib import Path

# -----------------------------------------------------------------------------
# Reward Script : verify_invoice_conversion
# -----------------------------------------------------------------------------
# 1. Looks for a file called  "invoice_template.odt" anywhere under /home/user
# 2. Confirms it is a valid ODT container (ZIP with required entries)
# 3. Extracts visible text from content.xml and checks for key invoice tokens
# 4. Returns a progressive score from 0.0-1.0 based on the evidence found
# -----------------------------------------------------------------------------

# Scoring weights (must add up to 1.0 when everything passes)
ODT_EXISTENCE_SCORE   = 0.20   # File located with the exact name
CONTENT_XML_SCORE     = 0.20   # Valid ODT structure (mimetype + content.xml)
TEXT_MATCH_MAX_SCORE  = 0.60   # Text-content similarity to original PDF

# Tokens that should appear in the editable text version of the invoice
EXPECTED_TOKENS = [
    "invoice",
    "seller",
    "acme",
    "corporation",
    "business",
    "metropolis",
    "description",
    "qty",
    "unit price",
    "line total",
    "total",
]

def _extract_visible_text(xml_bytes: bytes) -> str:
    """Remove XML tags and unescape entities to obtain human-readable text."""
    try:
        text = xml_bytes.decode("utf-8", errors="ignore")
    except Exception:
        text = xml_bytes.decode("latin-1", errors="ignore")
    text = re.sub(r"<[^>]+>", " ", text)          # strip tags
    return html.unescape(text).lower()

def _find_odt() -> Path | None:
    """Return first path matching invoice_template.odt under /home/user."""
    root = Path("/home/user")
    for p in root.rglob("invoice_template.odt"):
        if p.is_file():
            return p
    return None

def verify_invoice_conversion() -> float:
    print("Verifying conversion of invoice_template.pdf -> invoice_template.odt …")
    score = 0.0

    odt_path = _find_odt()
    if not odt_path:
        print("✗ invoice_template.odt not found")
        print(f"REWARD: {score}")
        return score

    print(f"✓ Found ODT: {odt_path}")
    score += ODT_EXISTENCE_SCORE  # small credit for correct file creation

    # ------------------------------------------------------------------
    # Validate ODT container and read content.xml
    # ------------------------------------------------------------------
    try:
        with zipfile.ZipFile(odt_path, "r") as zf:
            names = zf.namelist()
            if "content.xml" not in names or "mimetype" not in names:
                print("✗ Missing content.xml or mimetype entry – invalid ODT")
                print(f"REWARD: {score}")
                return score

            mimetype_ok = b"application/vnd.oasis.opendocument.text" in zf.read("mimetype")
            if mimetype_ok:
                print("✓ Valid mimetype entry detected")
            else:
                print("✗ Invalid mimetype entry (still continuing)")

            content_xml = zf.read("content.xml")
            print("✓ content.xml extracted successfully")
            score += CONTENT_XML_SCORE
    except zipfile.BadZipFile:
        print("✗ File is not a valid ZIP / ODT")
        print(f"REWARD: {score}")
        return score
    except Exception as e:
        print(f"✗ Error opening ODT: {e}")
        print(f"REWARD: {score}")
        return score

    # ------------------------------------------------------------------
    # Text verification – ensure key invoice phrases survived the conversion
    # ------------------------------------------------------------------
    visible_text = _extract_visible_text(content_xml)
    token_hits = 0
    for token in EXPECTED_TOKENS:
        if token in visible_text:
            print(f"✓ Token '{token}' found")
            token_hits += 1
        else:
            print(f"✗ Token '{token}' missing")

    # Pro-rate the remaining 0.6 points based on token coverage
    if EXPECTED_TOKENS:
        token_score = (token_hits / len(EXPECTED_TOKENS)) * TEXT_MATCH_MAX_SCORE
    else:
        token_score = 0.0

    score += token_score
    final_score = min(score, 1.0)

    print(f"Token hits: {token_hits}/{len(EXPECTED_TOKENS)}  -> token_score = {token_score:.2f}")
    print(f"REWARD: {final_score}")
    return final_score

# -----------------------------------------------------------------------------
# Execute when run directly
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    verify_invoice_conversion()
