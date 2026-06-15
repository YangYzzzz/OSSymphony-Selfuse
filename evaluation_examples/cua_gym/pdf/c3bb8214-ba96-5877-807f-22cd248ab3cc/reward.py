"""
FINAL REWARD SCRIPT - SUCCESS
Task: I have a redacted document 'redacted_report.pdf' on Desktop. Extract all visible (non-redacted) text and save to 'visible_content.txt'.
Generated: 2025-11-29 09:17:15
Status: success
Model: o3
Total Steps: 13
"""

from __future__ import annotations
"""Reward script for:
Task: Extract all visible (non-redacted) text from the PDF
      Desktop/redacted_report.pdf ➜ Desktop/visible_content.txt

Scoring rubric (max 1.0)
 0.2 – visible_content.txt exists next to the PDF
 0.3 – TXT contains NO redacted information
 0.5 – All visible (non-redacted) lines from the PDF are present in TXT (awarded pro-rata)

The script uses PyPDF2 for deterministic text extraction and simple
keyword heuristics to identify redacted lines.
"""
import os
from pathlib import Path
from typing import List
from PyPDF2 import PdfReader

def _clean_lines(text: str) -> List[str]:
    """Return stripped, non-empty lines from a text block."""
    return [ln.strip() for ln in text.splitlines() if ln.strip()]

def _pdf_lines(pdf_path: Path) -> List[str]:
    """Extract all text lines from every page of the PDF."""
    reader = PdfReader(str(pdf_path))
    lines: List[str] = []
    for idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        page_lines = _clean_lines(page_text)
        print(f"Page {idx + 1}: {len(page_lines)} non-empty lines extracted")
        lines.extend(page_lines)
    return lines

def verify_task() -> float:
    desktop = Path.home() / "Desktop"
    pdf_path = desktop / "redacted_report.pdf"
    txt_path = desktop / "visible_content.txt"

    if not pdf_path.exists():
        print(f"✗ PDF not found at {pdf_path}")
        return 0.0
    print(f"✓ Found source PDF: {pdf_path}")

    # Extract PDF text
    pdf_lines = _pdf_lines(pdf_path)

    # Heuristic keywords that should be redacted (task-specific, deterministic)
    redacted_kw = ["project:", "budget:", "secretproject", "$"]

    visible_pdf, redacted_pdf = [], []
    for line in pdf_lines:
        (redacted_pdf if any(k in line.lower() for k in redacted_kw) else visible_pdf).append(line)

    print("Redacted PDF lines (must NOT appear in TXT):")
    for ln in redacted_pdf:
        print("  •", ln)
    print("Visible PDF lines (must appear in TXT):")
    for ln in visible_pdf:
        print("  •", ln)

    score = 0.0  # progressive

    # 1) File existence check (0.2)
    if not txt_path.exists():
        print(f"✗ Missing extracted text file: {txt_path}")
        return 0.0
    print(f"✓ Found extracted text file: {txt_path} (0.2 points)")
    score += 0.2

    txt_lines = _clean_lines(txt_path.read_text(encoding="utf-8", errors="ignore"))
    print(f"TXT contains {len(txt_lines)} non-empty lines")

    # 2) Confidentiality check – ensure no redacted data leaked (0.3)
    leaked = [ln for ln in txt_lines if any(k in ln.lower() for k in redacted_kw)]
    if leaked:
        print("✗ Redacted information leaked into TXT – 0 points for confidentiality:")
        for ln in leaked:
            print("  •", ln)
    else:
        print("✓ No redacted information present in TXT (0.3 points)")
        score += 0.3

    # 3) Completeness check – visible lines coverage (≤0.5)
    vis_pdf_set = {ln.lower() for ln in visible_pdf}
    txt_set = {ln.lower() for ln in txt_lines}
    matched = vis_pdf_set & txt_set
    coverage = len(matched) / len(vis_pdf_set) if vis_pdf_set else 1.0
    coverage_score = 0.5 * coverage
    score += coverage_score

    print(f"Visible coverage: {len(matched)}/{len(vis_pdf_set)} lines -> {coverage*100:.1f}% (up to 0.5 points)")
    if coverage == 1.0:
        print("✓ All visible lines extracted (0.5 points)")
    else:
        missing = vis_pdf_set - txt_set
        print("Missing visible lines:")
        for ln in missing:
            print("  •", ln)

    final = round(min(score, 1.0), 2)
    print(f"REWARD: {final}")
    return final

if __name__ == "__main__":
    print(f"REWARD: {verify_task()}")
