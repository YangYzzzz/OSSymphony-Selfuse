"""
FINAL REWARD SCRIPT - SUCCESS
Task: Paragraph 8 is sticking out like a sore thumb—its sentence case doesn’t match the rest of my headings. What’s the quickest way in LibreOffice Writer to flip just that single paragraph (paragraph 8) into Title Case so every word starts with a capital?
Generated: 2025-09-10 14:11:48
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import re
import glob
import zipfile
from typing import List

try:
    from docx import Document  # python-docx for DOCX handling
except ImportError:  # Fallback protection (should be available)
    Document = None

# ----------------------------- Helper Functions ----------------------------- #

def is_title_case(text: str) -> bool:
    """Return True if every word in *text* starts with a capital letter (Title Case).
    Symbols / words without letters are ignored. Fails on the first real word
    that does not begin with an uppercase alphabetical character.
    """
    words = re.split(r'[\s\-]+', text.strip())
    has_alpha_word = False
    for w in words:
        if not w:
            continue  # skip empty splits
        # locate first alphabetical character in the word
        first_alpha = next((c for c in w if c.isalpha()), None)
        if first_alpha is None:
            continue  # word with no letters (e.g. numbers) – ignore
        has_alpha_word = True
        if not first_alpha.isupper():
            return False
    return has_alpha_word  # must contain at least one word with letters


# --------------------------- Paragraph Extraction --------------------------- #

def extract_paragraphs_docx(path: str) -> List[str]:
    """Extract non-empty paragraph texts from a DOCX file."""
    if Document is None:
        raise ImportError("python-docx library is not available in environment")
    doc = Document(path)
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]


def extract_paragraphs_odt(path: str) -> List[str]:
    """Extract non-empty paragraph texts from an ODT file via XML parsing."""
    paragraphs: List[str] = []
    try:
        with zipfile.ZipFile(path, "r") as zf:
            content_xml = zf.read("content.xml")
        import xml.etree.ElementTree as ET

        ns = {"text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"}
        root = ET.fromstring(content_xml)
        for p in root.findall(".//text:p", ns):
            txt = "".join(p.itertext()).strip()
            if txt:
                paragraphs.append(txt)
    except Exception as e:
        print("✗ Error extracting ODT paragraphs:", e)
    return paragraphs


# --------------------------- File Location Logic --------------------------- #

def locate_document(base_dir: str = "/home/user") -> str:
    """Locate first DOCX/ODT file in *base_dir* (prefers filenames with 'paragraph_8')."""
    paths: List[str] = []
    # search top level
    for ext in ("*.docx", "*.odt"):
        paths.extend(glob.glob(os.path.join(base_dir, ext)))
    # recursive search
    for root_dir, _dirs, _files in os.walk(base_dir):
        for ext in ("*.docx", "*.odt"):
            paths.extend(glob.glob(os.path.join(root_dir, ext)))
    if not paths:
        return ""
    # prefer file that clearly belongs to the current task
    for p in paths:
        if "paragraph_8" in os.path.basename(p).lower():
            return p
    # otherwise return the first found
    return paths[0]


# ------------------------------- Verification ------------------------------ #

def verify_task() -> float:
    """Verify that paragraph 8 is converted to Title Case and award a progressive score."""
    max_score = 1.0
    score = 0.0

    file_path = locate_document()
    if not file_path:
        print("✗ No DOCX/ODT document found in workspace")
        print("REWARD: 0.0")
        return 0.0
    print(f"Document found: {file_path}")

    # Extract paragraphs according to file type
    paragraphs: List[str] = []
    try:
        if file_path.lower().endswith(".docx"):
            paragraphs = extract_paragraphs_docx(file_path)
        elif file_path.lower().endswith(".odt"):
            paragraphs = extract_paragraphs_odt(file_path)
        else:
            print("✗ Unsupported file format – only DOCX or ODT accepted")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print("✗ Error reading document:", e)
        print("REWARD: 0.0")
        return 0.0

    total_para = len(paragraphs)
    print(f"Found {total_para} non-empty paragraphs")
    if total_para == 0:
        print("✗ Document has no paragraphs")
        print("REWARD: 0.0")
        return 0.0

    # ---- Requirement 1: Paragraph 8 is Title Case (worth 0.7) ---- #
    para8_ok = False
    if total_para >= 8:
        para8_text = paragraphs[7]
        para8_ok = is_title_case(para8_text)
        status = "✓" if para8_ok else "✗"
        print(f"{status} Paragraph 8 Title Case Check: \"{para8_text}\"")
    else:
        print("✗ Document does not contain 8 paragraphs to test")

    if para8_ok:
        score += 0.7  # major portion of score

    # ---- Requirement 2: Other paragraphs keep Title Case consistency (0.2 max) ---- #
    other_flags = [is_title_case(t) for idx, t in enumerate(paragraphs) if idx != 7]
    if other_flags:
        proportion_other = sum(other_flags) / len(other_flags)
        score += 0.2 * proportion_other
        print(f"Other paragraphs Title Case proportion: {proportion_other:.2f}")

    # ---- Bonus: Entire document is Title Case (0.1 bonus) ---- #
    if all(is_title_case(t) for t in paragraphs):
        score += 0.1
        print("✓ All paragraphs are Title Case (bonus +0.1)")

    # Ensure score does not exceed 1.0 and round sensibly
    score = round(min(score, max_score), 3)

    print(f"Score breakdown: {score}/{max_score}")
    print(f"REWARD: {score}")
    return score


# ------------------------------ Script Entrypoint --------------------------- #

if __name__ == "__main__":
    verify_task()

