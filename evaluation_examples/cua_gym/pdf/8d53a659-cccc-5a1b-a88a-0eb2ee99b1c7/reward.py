"""
Reward Script: Verify multi-app workflow for pdf_cross_146.

Task: Multi-app workflow:
  1. Use Terminal to batch split ~/Documents/combined_report.pdf into
     individual chapter PDFs (Chapters 1-5).
  2. In File Manager, organize chapters into ~/Documents/book/chapters/.
  3. Use GIMP to create chapter divider images (colored title pages).
  4. Use pymupdf to interleave dividers between chapters.
     Save as ~/Documents/book/complete_book.pdf.

Ground truth:
  ~/Documents/book/chapters/chapter_1.pdf  — 8 pages (source pages 1-8)
  ~/Documents/book/chapters/chapter_2.pdf  — 8 pages (source pages 9-16)
  ~/Documents/book/chapters/chapter_3.pdf  — 8 pages (source pages 17-24)
  ~/Documents/book/chapters/chapter_4.pdf  — 8 pages (source pages 25-32)
  ~/Documents/book/chapters/chapter_5.pdf  — 8 pages (source pages 33-40)
  ~/Documents/book/complete_book.pdf       — 45 pages (5 dividers + 40 content)
    Structure: divider_N (1 page) followed by chapter_N (8 pages), repeated 5×

Scoring rubric (total = 1.0):

  Component 1 (0.08): ~/Documents/book/ directory exists
  Component 2 (0.08): ~/Documents/book/chapters/ directory exists
  Component 3 (0.08): Exactly 5 PDF files named chapter_1.pdf..chapter_5.pdf in chapters/

  Component 4 (0.04): chapter_1.pdf has 8 pages (source pages 1-8)
  Component 5 (0.04): chapter_2.pdf has 8 pages (source pages 9-16)
  Component 6 (0.04): chapter_3.pdf has 8 pages (source pages 17-24)
  Component 7 (0.04): chapter_4.pdf has 8 pages (source pages 25-32)
  Component 8 (0.04): chapter_5.pdf has 8 pages (source pages 33-40)

  Component 9 (0.06):  chapter_1.pdf contains correct Chapter 1 content
  Component 10 (0.06): chapter_2.pdf contains correct Chapter 2 content
  Component 11 (0.06): chapter_3.pdf contains correct Chapter 3 content
  Component 12 (0.06): chapter_4.pdf contains correct Chapter 4 content
  Component 13 (0.06): chapter_5.pdf contains correct Chapter 5 content

  Component 14 (0.10): complete_book.pdf exists
  Component 15 (0.10): complete_book.pdf has exactly 45 pages

  Component 16 (0.06): complete_book.pdf has correct interleaving structure
                       (odd pages 1,10,19,28,37 are dividers; even blocks are chapter content)
  Component 17 (0.06): complete_book.pdf chapter content pages contain correct text markers
                       (spot-check: first content page of each chapter)
  Component 18 (0.04): complete_book.pdf is a valid, openable PDF with no corruption

  Total: 1.00
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = "/home/user/Documents"
SOURCE_PDF = f"{WORKDIR}/combined_report.pdf"
BOOK_DIR = f"{WORKDIR}/book"
CHAPTERS_DIR = f"{BOOK_DIR}/chapters"
COMPLETE_BOOK = f"{BOOK_DIR}/complete_book.pdf"

# Expected page counts for each chapter file
CHAPTER_EXPECTED_PAGES = {
    "chapter_1.pdf": 8,
    "chapter_2.pdf": 8,
    "chapter_3.pdf": 8,
    "chapter_4.pdf": 8,
    "chapter_5.pdf": 8,
}

# Content markers expected to appear in each chapter file
# These are unique strings embedded in the initial_setup.py page content
CHAPTER_CONTENT_MARKERS = {
    "chapter_1.pdf": [
        "Chapter 1",
        "Introduction to Data Science",
        "CH1_P1_OVERVIEW_OF_DATA_SCIENCE",
    ],
    "chapter_2.pdf": [
        "Chapter 2",
        "Data Collection Methods",
    ],
    "chapter_3.pdf": [
        "Chapter 3",
        "Statistical Analysis",
    ],
    "chapter_4.pdf": [
        "Chapter 4",
        "Machine Learning Techniques",
    ],
    "chapter_5.pdf": [
        "Chapter 5",
        "Visualization and Reporting",
    ],
}

# In complete_book.pdf, pages are 0-indexed:
#   0     = divider 1
#   1-8   = chapter 1 (8 pages)
#   9     = divider 2
#   10-17 = chapter 2 (8 pages)
#   18    = divider 3
#   19-26 = chapter 3 (8 pages)
#   27    = divider 4
#   28-35 = chapter 4 (8 pages)
#   36    = divider 5
#   37-44 = chapter 5 (8 pages)
DIVIDER_PAGE_INDICES = [0, 9, 18, 27, 36]
CHAPTER_FIRST_CONTENT_PAGE_INDICES = [1, 10, 19, 28, 37]


def get_pdf_page_count(pdf_path: str) -> int:
    """Return page count or -1 on error."""
    try:
        doc = pymupdf.open(pdf_path)
        count = doc.page_count
        doc.close()
        return count
    except Exception:
        return -1


def get_all_text(pdf_path: str) -> str:
    """Extract all text from all pages of a PDF."""
    try:
        doc = pymupdf.open(pdf_path)
        texts = []
        for page in doc:
            texts.append(page.get_text("text"))
        doc.close()
        return "\n".join(texts)
    except Exception:
        return ""


def get_page_text(pdf_path: str, page_idx: int) -> str:
    """Extract text from a single page (0-indexed)."""
    try:
        doc = pymupdf.open(pdf_path)
        if page_idx < 0 or page_idx >= doc.page_count:
            doc.close()
            return ""
        text = doc[page_idx].get_text("text")
        doc.close()
        return text
    except Exception:
        return ""


def is_likely_divider_page(pdf_path: str, page_idx: int) -> bool:
    """
    Check if a page looks like a divider (chapter title page).
    Dividers should contain a 'CHAPTER N' heading pattern and NOT have
    typical body content markers like section body text.
    """
    text = get_page_text(pdf_path, page_idx)
    if not text:
        # Dividers may be image-based (PIL → PDF image page) with minimal extracted text
        # In that case, check that the page has images but minimal text
        try:
            doc = pymupdf.open(pdf_path)
            page = doc[page_idx]
            images = page.get_images()
            plain_text = page.get_text("text").strip()
            doc.close()
            # An image-based divider will have images and very little text
            if len(images) > 0 and len(plain_text) < 200:
                return True
        except Exception:
            pass

    # Text-based divider: should contain "CHAPTER" heading
    if "CHAPTER" in text.upper():
        return True

    return False


def verify_task() -> float:
    """Verify task completion with progressive scoring. Returns 0.0-1.0."""
    total_score = 0.0

    # ----------------------------------------------------------------
    # Component 1: ~/Documents/book/ directory exists (0.08)
    # ----------------------------------------------------------------
    if os.path.isdir(BOOK_DIR):
        print(f"PASS: Component 1 — {BOOK_DIR}/ exists (+0.08)")
        total_score += 0.08
    else:
        print(f"FAIL: Component 1 — {BOOK_DIR}/ not found")
        print(f"REWARD: {round(total_score, 2)}")
        return round(total_score, 2)

    # ----------------------------------------------------------------
    # Component 2: ~/Documents/book/chapters/ directory exists (0.08)
    # ----------------------------------------------------------------
    if os.path.isdir(CHAPTERS_DIR):
        print(f"PASS: Component 2 — {CHAPTERS_DIR}/ exists (+0.08)")
        total_score += 0.08
    else:
        print(f"FAIL: Component 2 — {CHAPTERS_DIR}/ not found")
        print(f"REWARD: {round(total_score, 2)}")
        return round(total_score, 2)

    # List PDF files in chapters/
    try:
        all_chapter_files = sorted(
            [f for f in os.listdir(CHAPTERS_DIR) if f.endswith(".pdf")]
        )
    except Exception as e:
        print(f"ERROR: Cannot list {CHAPTERS_DIR}: {e}")
        print(f"REWARD: {round(total_score, 2)}")
        return round(total_score, 2)

    # ----------------------------------------------------------------
    # Component 3: Exactly 5 files named chapter_1.pdf..chapter_5.pdf (0.08)
    # ----------------------------------------------------------------
    expected_chapter_names = [
        "chapter_1.pdf", "chapter_2.pdf", "chapter_3.pdf",
        "chapter_4.pdf", "chapter_5.pdf",
    ]
    if all_chapter_files == expected_chapter_names:
        print(f"PASS: Component 3 — Exactly 5 correctly named chapter files (+0.08)")
        total_score += 0.08
    else:
        missing = [n for n in expected_chapter_names if n not in all_chapter_files]
        extra = [f for f in all_chapter_files if f not in expected_chapter_names]
        print(f"FAIL: Component 3 — Missing: {missing}; Extra: {extra}")

    # ----------------------------------------------------------------
    # Components 4-8: Page count for each chapter file (0.04 each)
    # ----------------------------------------------------------------
    comp_num_map = {
        "chapter_1.pdf": 4,
        "chapter_2.pdf": 5,
        "chapter_3.pdf": 6,
        "chapter_4.pdf": 7,
        "chapter_5.pdf": 8,
    }
    for chapter_name, comp_num in comp_num_map.items():
        chapter_path = os.path.join(CHAPTERS_DIR, chapter_name)
        expected_pages = CHAPTER_EXPECTED_PAGES[chapter_name]
        if not os.path.exists(chapter_path):
            print(f"FAIL: Component {comp_num} — {chapter_name} not found")
            continue
        try:
            actual_pages = get_pdf_page_count(chapter_path)
            if actual_pages == expected_pages:
                print(f"PASS: Component {comp_num} — {chapter_name} has {expected_pages} pages (+0.04)")
                total_score += 0.04
            else:
                print(f"FAIL: Component {comp_num} — {chapter_name} expected {expected_pages} pages, got {actual_pages}")
        except Exception as e:
            print(f"ERROR: Component {comp_num} — {e}")

    # ----------------------------------------------------------------
    # Components 9-13: Content markers in each chapter file (0.06 each)
    # ----------------------------------------------------------------
    content_comp_map = {
        "chapter_1.pdf": (9,  "Chapter 1 content"),
        "chapter_2.pdf": (10, "Chapter 2 content"),
        "chapter_3.pdf": (11, "Chapter 3 content"),
        "chapter_4.pdf": (12, "Chapter 4 content"),
        "chapter_5.pdf": (13, "Chapter 5 content"),
    }
    for chapter_name, (comp_num, desc) in content_comp_map.items():
        chapter_path = os.path.join(CHAPTERS_DIR, chapter_name)
        if not os.path.exists(chapter_path):
            print(f"FAIL: Component {comp_num} — {chapter_name} not found")
            continue
        try:
            text = get_all_text(chapter_path)
            markers = CHAPTER_CONTENT_MARKERS[chapter_name]
            found = [m for m in markers if m in text]
            ratio = len(found) / len(markers) if markers else 0.0
            pts = round(0.06 * ratio, 4)
            if ratio >= 1.0:
                print(f"PASS: Component {comp_num} — {chapter_name} has correct {desc} (+0.06)")
            elif ratio > 0:
                print(f"PARTIAL: Component {comp_num} — {chapter_name} {len(found)}/{len(markers)} markers (+{pts:.4f})")
            else:
                print(f"FAIL: Component {comp_num} — {chapter_name} missing expected content markers")
            total_score += pts
        except Exception as e:
            print(f"ERROR: Component {comp_num} — {e}")

    # ----------------------------------------------------------------
    # Component 14: complete_book.pdf exists (0.10)
    # ----------------------------------------------------------------
    if os.path.exists(COMPLETE_BOOK):
        print(f"PASS: Component 14 — {COMPLETE_BOOK} exists (+0.10)")
        total_score += 0.10
    else:
        print(f"FAIL: Component 14 — {COMPLETE_BOOK} not found")
        print(f"REWARD: {round(total_score, 2)}")
        return round(total_score, 2)

    # Open complete_book.pdf for subsequent checks
    try:
        cb_doc = pymupdf.open(COMPLETE_BOOK)
    except Exception as e:
        print(f"CRITICAL: Cannot open complete_book.pdf: {e}")
        print(f"REWARD: {round(total_score, 2)}")
        return round(total_score, 2)

    # ----------------------------------------------------------------
    # Component 15: complete_book.pdf has 45 pages (0.10)
    # ----------------------------------------------------------------
    try:
        total_pages = cb_doc.page_count
        if total_pages == 45:
            print(f"PASS: Component 15 — complete_book.pdf has 45 pages (+0.10)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 15 — expected 45 pages, got {total_pages}")
    except Exception as e:
        print(f"ERROR: Component 15 — {e}")

    # ----------------------------------------------------------------
    # Component 16: Interleaving structure check (0.06)
    # Pages 0,9,18,27,36 should be divider pages (image-heavy or CHAPTER heading)
    # ----------------------------------------------------------------
    try:
        divider_checks_passed = 0
        for div_page_idx in DIVIDER_PAGE_INDICES:
            if div_page_idx < cb_doc.page_count:
                if is_likely_divider_page(COMPLETE_BOOK, div_page_idx):
                    divider_checks_passed += 1
                else:
                    # Check: divider pages should NOT contain source text content
                    text = get_page_text(COMPLETE_BOOK, div_page_idx)
                    # A divider has color-block background; it typically won't have
                    # the detailed body text of the chapters
                    ch_num_for_this_div = DIVIDER_PAGE_INDICES.index(div_page_idx) + 1
                    body_marker = f"CH{ch_num_for_this_div}_P"
                    if body_marker not in text:
                        # The page doesn't have chapter body markers → likely a divider
                        divider_checks_passed += 1

        div_ratio = divider_checks_passed / len(DIVIDER_PAGE_INDICES)
        pts = round(0.06 * div_ratio, 4)
        if div_ratio >= 1.0:
            print(f"PASS: Component 16 — Interleaving structure correct (+0.06)")
        elif div_ratio > 0:
            print(f"PARTIAL: Component 16 — {divider_checks_passed}/{len(DIVIDER_PAGE_INDICES)} dividers in correct position (+{pts:.4f})")
        else:
            print(f"FAIL: Component 16 — Divider pages not found at expected positions")
        total_score += pts
    except Exception as e:
        print(f"ERROR: Component 16 — {e}")

    # ----------------------------------------------------------------
    # Component 17: Content pages in complete_book.pdf have correct chapter text (0.06)
    # Check first content page of each chapter block (pages 1,10,19,28,37)
    # ----------------------------------------------------------------
    try:
        content_checks_passed = 0
        chapter_heading_markers = [
            "Chapter 1",    # page index 1
            "Chapter 2",    # page index 10
            "Chapter 3",    # page index 19
            "Chapter 4",    # page index 28
            "Chapter 5",    # page index 37
        ]
        for ch_idx, first_content_idx in enumerate(CHAPTER_FIRST_CONTENT_PAGE_INDICES):
            if first_content_idx < cb_doc.page_count:
                text = get_page_text(COMPLETE_BOOK, first_content_idx)
                expected_marker = chapter_heading_markers[ch_idx]
                if expected_marker in text:
                    content_checks_passed += 1
                else:
                    # Also accept chapter number alone
                    if f"Chapter {ch_idx + 1}" in text or f"chapter {ch_idx + 1}" in text.lower():
                        content_checks_passed += 1

        content_ratio = content_checks_passed / len(CHAPTER_FIRST_CONTENT_PAGE_INDICES)
        pts = round(0.06 * content_ratio, 4)
        if content_ratio >= 1.0:
            print(f"PASS: Component 17 — Content pages have correct chapter text (+0.06)")
        elif content_ratio > 0:
            print(f"PARTIAL: Component 17 — {content_checks_passed}/5 chapter content pages verified (+{pts:.4f})")
        else:
            print(f"FAIL: Component 17 — Content pages do not have expected chapter text")
        total_score += pts
    except Exception as e:
        print(f"ERROR: Component 17 — {e}")

    # ----------------------------------------------------------------
    # Component 18: complete_book.pdf is a valid, uncorrupted PDF (0.04)
    # ----------------------------------------------------------------
    try:
        # Attempt to iterate all pages and extract text (stress test validity)
        error_pages = 0
        for i in range(cb_doc.page_count):
            try:
                _ = cb_doc[i].get_text("text")
            except Exception:
                error_pages += 1
        cb_doc.close()

        if error_pages == 0:
            print(f"PASS: Component 18 — complete_book.pdf is valid and uncorrupted (+0.04)")
            total_score += 0.04
        else:
            print(f"FAIL: Component 18 — {error_pages} pages failed to render in complete_book.pdf")
    except Exception as e:
        print(f"ERROR: Component 18 — {e}")
        try:
            cb_doc.close()
        except Exception:
            pass

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
