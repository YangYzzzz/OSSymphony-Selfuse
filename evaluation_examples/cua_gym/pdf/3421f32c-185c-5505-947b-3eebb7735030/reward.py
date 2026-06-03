"""
Reward Script: Insert blank signature page after page 5 in contract_draft.pdf
Task ID: pdf_gf2_020
Domain: pdf
Scoring:
  Component 1 (0.25): Output file exists with correct page count (11 pages)
  Component 2 (0.25): New page 6 (0-indexed: 5) contains 'SIGNATURE PAGE' text
  Component 3 (0.25): New page dimensions match original (612x792) and text is horizontally centered
  Component 4 (0.25): Content preservation — original pages correctly shifted
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_020'

ORIGINAL_PATH = os.path.join(WORKDIR, 'Documents', 'contract_draft.pdf')
OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'contract_draft_sig.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open output file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has 11 pages (0.25 points)
    try:
        page_count = doc.page_count
        if page_count == 11:
            print(f"PASS: Component 1 — Output has 11 pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 11 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page 5 (0-indexed) contains 'SIGNATURE PAGE' text and is mostly blank (0.25 points)
    try:
        if doc.page_count > 5:
            sig_page = doc[5]
            sig_text = sig_page.get_text("text").strip()
            if "SIGNATURE PAGE" in sig_text:
                # Check that the page is mostly just the signature text (no other substantial content)
                cleaned = sig_text.replace("SIGNATURE PAGE", "").strip()
                if len(cleaned) < 20:
                    print(f"PASS: Component 2 — Page 5 contains 'SIGNATURE PAGE' with minimal other content (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 — Page 5 has 'SIGNATURE PAGE' but also extra content: {repr(cleaned[:80])}")
            else:
                print(f"FAIL: Component 2 — Page 5 text is: {repr(sig_text[:100])}, expected 'SIGNATURE PAGE'")
        else:
            print(f"FAIL: Component 2 — Document has fewer than 6 pages")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: New page dimensions match original (612x792) and text is horizontally centered (0.25 points)
    try:
        if doc.page_count > 5:
            sig_page = doc[5]
            w, h = sig_page.rect.width, sig_page.rect.height

            # Check dimensions match Letter size (612x792)
            dims_ok = abs(w - 612.0) < 2.0 and abs(h - 792.0) < 2.0

            # Check horizontal centering of SIGNATURE PAGE text
            instances = sig_page.search_for("SIGNATURE PAGE")
            centered = False
            if instances:
                r = instances[0]
                text_cx = (r.x0 + r.x1) / 2
                page_cx = w / 2
                # Allow 20pt tolerance for centering
                centered = abs(text_cx - page_cx) < 20.0

            if dims_ok and centered:
                print(f"PASS: Component 3 — Page dims {w}x{h}, text centered (diff={abs(text_cx - page_cx):.1f}pt) (0.25 pts)")
                total_score += 0.25
            elif dims_ok and not centered:
                print(f"FAIL: Component 3 — Dims OK ({w}x{h}) but text not centered")
            elif not dims_ok:
                print(f"FAIL: Component 3 — Page dims {w}x{h}, expected ~612x792")
        else:
            print(f"FAIL: Component 3 — Not enough pages")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Content preservation — original pages are correctly shifted (0.25 points)
    try:
        if os.path.exists(ORIGINAL_PATH) and doc.page_count == 11:
            orig = pymupdf.open(ORIGINAL_PATH)
            matches = 0
            total_checks = 0

            # Pages 0-4 of output should match pages 0-4 of original
            for i in range(min(5, orig.page_count)):
                total_checks += 1
                out_text = doc[i].get_text("text")[:200].strip()
                orig_text = orig[i].get_text("text")[:200].strip()
                if out_text == orig_text:
                    matches += 1
                else:
                    print(f"  INFO: Page {i} text mismatch")

            # Pages 6-10 of output should match pages 5-9 of original
            for out_i, orig_i in zip(range(6, 11), range(5, 10)):
                if orig_i < orig.page_count and out_i < doc.page_count:
                    total_checks += 1
                    out_text = doc[out_i].get_text("text")[:200].strip()
                    orig_text = orig[orig_i].get_text("text")[:200].strip()
                    if out_text == orig_text:
                        matches += 1
                    else:
                        print(f"  INFO: Output page {out_i} != Original page {orig_i}")

            orig.close()

            if total_checks > 0 and matches == total_checks:
                print(f"PASS: Component 4 — All {matches}/{total_checks} page content checks passed (0.25 pts)")
                total_score += 0.25
            elif total_checks > 0:
                ratio = matches / total_checks
                partial = round(0.25 * ratio, 2)
                print(f"FAIL: Component 4 — {matches}/{total_checks} pages matched (partial: {partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — No checks performed")
        else:
            print(f"FAIL: Component 4 — Original file missing or wrong page count")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
