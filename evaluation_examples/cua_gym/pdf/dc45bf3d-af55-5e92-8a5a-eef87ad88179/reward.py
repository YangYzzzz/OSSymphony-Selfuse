"""
FINAL REWARD SCRIPT - SUCCESS
Task: Split 'presentation.pdf' on Desktop into individual slides, saving each slide as a separate PDF (slide_01.pdf, slide_02.pdf, etc.) in folder 'slides_separated' on Desktop.
Generated: 2025-11-29 09:35:28
Status: success
Model: o3
Total Steps: 7
"""

"""Reward verification script for the task:
Split 'presentation.pdf' on Desktop into individual slides, saving each slide as
slide_01.pdf, slide_02.pdf, … inside 'slides_separated' on Desktop.

Scoring (adds up to 1.0):
    0.3 – All expected slide_NN.pdf files exist
    0.2 – Each slide PDF contains exactly ONE page
    0.3 – Text of each slide matches the corresponding page in the original PDF
    0.2 – slide_01.pdf matches a provided golden reference PDF

The script prints detailed diagnostics and finishes with
    REWARD: X.X
where X.X is a float in the range [0.0, 1.0].
"""
from pathlib import Path
from PyPDF2 import PdfReader
import re

def _normalize(text: str | None) -> str:
    """Collapse all whitespace for reliable comparisons."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()

def verify_split_slides() -> float:
    total = 0.0
    desktop = Path.home() / "Desktop"
    original_pdf = desktop / "presentation.pdf"
    slides_dir = desktop / "slides_separated"
    golden = Path(
        "/home/user/"
        "split_presentationpdf_on_desktop_into_individual_slides_saving_each_slide_as_a_separate_pdf_slide_01_golden.pdf"
    )

    # -------- Load original PDF ---------
    if not original_pdf.exists():
        print(f"✗ Original PDF missing: {original_pdf}")
        print("REWARD: 0.0")
        return 0.0
    try:
        orig_reader = PdfReader(str(original_pdf))
    except Exception as e:
        print(f"✗ Cannot read original PDF: {e}")
        print("REWARD: 0.0")
        return 0.0
    pages = len(orig_reader.pages)
    print(f"Original PDF pages: {pages}")

    # -------- Check slide files existence ---------
    if slides_dir.exists() and slides_dir.is_dir():
        expected = [slides_dir / f"slide_{i+1:02d}.pdf" for i in range(pages)]
        missing = [p.name for p in expected if not p.exists()]
        extras = [p.name for p in slides_dir.glob("slide_*.pdf") if p not in expected]
        if missing:
            print(f"✗ Missing slide files: {missing}")
        else:
            print("✓ All expected slide files present (0.3)")
            total += 0.3
        if extras:
            print(f"(info) Extra slide files: {extras}")
    else:
        print(f"✗ Slides directory missing or not a dir: {slides_dir}")
        print(f"REWARD: {total}")
        return total

    # -------- Validate each slide PDF ---------
    one_page_ok = True
    text_match_cnt = 0
    for i in range(pages):
        slide = slides_dir / f"slide_{i+1:02d}.pdf"
        if not slide.exists():
            one_page_ok = False
            continue
        try:
            slide_reader = PdfReader(str(slide))
        except Exception as e:
            print(f"✗ Cannot read {slide.name}: {e}")
            one_page_ok = False
            continue
        if len(slide_reader.pages) != 1:
            print(f"✗ {slide.name} has {len(slide_reader.pages)} pages (expected 1)")
            one_page_ok = False
        orig_txt = _normalize(orig_reader.pages[i].extract_text())
        slide_txt = _normalize(slide_reader.pages[0].extract_text())
        if orig_txt == slide_txt:
            text_match_cnt += 1
        else:
            print(f"✗ Text mismatch in {slide.name}")

    if one_page_ok and pages > 0:
        print("✓ Each slide has exactly one page (0.2)")
        total += 0.2
    else:
        print("✗ Not all slides have one page")

    if text_match_cnt == pages and pages > 0:
        print("✓ Text of all slides matches original (0.3)")
        total += 0.3
    else:
        print(f"✗ {text_match_cnt}/{pages} slide texts match original")

    # -------- Compare slide_01 with golden reference ---------
    slide1 = slides_dir / "slide_01.pdf"
    if slide1.exists() and golden.exists():
        try:
            s_reader = PdfReader(str(slide1))
            g_reader = PdfReader(str(golden))
            if _normalize(s_reader.pages[0].extract_text()) == _normalize(g_reader.pages[0].extract_text()):
                print("✓ slide_01.pdf matches golden reference (0.2)")
                total += 0.2
            else:
                print("✗ slide_01.pdf does not match golden reference")
        except Exception as e:
            print(f"✗ Error comparing to golden reference: {e}")
    else:
        print("(info) Golden reference or slide_01.pdf missing – skipping 0.2 component")

    final = min(total, 1.0)
    print(f"REWARD: {final}")
    return final

if __name__ == "__main__":
    verify_split_slides()
