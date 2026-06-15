"""
Reward Script: Replace logo on page 1 of financial report PDF
Task ID: pdf_fin_091
Domain: pdf
Scoring:
  Component 1 (0.5): Page 1 image matches new_logo.png (pixel similarity)
  Component 2 (0.2): Page 1 image differs from old logo (old logo removed)
  Component 3 (0.3): Text content on all pages preserved from original
"""

import os
import numpy as np

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_091'

# Paths
OUTPUT_PDF = os.path.join(WORKDIR, 'finance', 'report_new_logo.pdf')
ORIGINAL_PDF = os.path.join(WORKDIR, 'finance', 'report_old_logo.pdf')
NEW_LOGO_PATH = os.path.join(WORKDIR, 'finance', 'assets', 'new_logo.png')


def extract_page_image_data(pdf_path, page_num=0):
    """Extract the first image from a given page as a numpy array."""
    import pymupdf
    from PIL import Image
    import io
    doc = pymupdf.open(pdf_path)
    page = doc[page_num]
    images = page.get_images()
    if not images:
        doc.close()
        return None
    xref = images[0][0]
    img_data = doc.extract_image(xref)
    doc.close()
    img = Image.open(io.BytesIO(img_data['image'])).convert('RGB')
    return np.array(img)


def get_all_text(pdf_path):
    """Get concatenated text from all pages."""
    import pymupdf
    doc = pymupdf.open(pdf_path)
    texts = []
    for page in doc:
        texts.append(page.get_text())
    doc.close()
    return texts


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_PDF):
        print("CRITICAL: Output file not found: %s" % OUTPUT_PDF)
        print("REWARD: 0.0")
        return 0.0

    # Precondition: new_logo.png must exist for comparison
    if not os.path.exists(NEW_LOGO_PATH):
        print("CRITICAL: Reference new_logo.png not found: %s" % NEW_LOGO_PATH)
        print("REWARD: 0.0")
        return 0.0

    # Precondition: output PDF must be loadable
    try:
        import pymupdf
        doc = pymupdf.open(OUTPUT_PDF)
        page_count = len(doc)
        doc.close()
        if page_count == 0:
            print("CRITICAL: Output PDF has 0 pages")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print("CRITICAL: Cannot load output PDF: %s" % e)
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page 1 image matches new_logo.png (0.5 points)
    # This checks the core task: replacing the logo with the new one
    try:
        from PIL import Image
        output_img = extract_page_image_data(OUTPUT_PDF, page_num=0)
        ref_img = np.array(Image.open(NEW_LOGO_PATH).convert('RGB'))

        if output_img is None:
            print("FAIL: Component 1 — No image found on page 1 of output PDF")
        else:
            # Resize reference if shapes differ
            if output_img.shape != ref_img.shape:
                ref_img = np.array(
                    Image.open(NEW_LOGO_PATH).convert('RGB').resize(
                        (output_img.shape[1], output_img.shape[0]),
                        Image.Resampling.LANCZOS
                    )
                )

            # Compute mean absolute pixel difference (0 = identical)
            mean_diff = np.mean(np.abs(output_img.astype(float) - ref_img.astype(float)))
            print("INFO: Component 1 — Mean pixel diff (output vs new_logo): %.4f" % mean_diff)

            if mean_diff < 5.0:
                # Near-perfect match (allows minor compression artifacts)
                print("PASS: Component 1 — Page 1 image matches new_logo.png (diff=%.4f) (0.5 pts)" % mean_diff)
                total_score += 0.5
            elif mean_diff < 20.0:
                # Partial match — image is similar but not exact
                partial = 0.25
                print("PARTIAL: Component 1 — Page 1 image similar to new_logo (diff=%.4f) (%.2f pts)" % (mean_diff, partial))
                total_score += partial
            else:
                print("FAIL: Component 1 — Page 1 image does NOT match new_logo (diff=%.4f)" % mean_diff)
    except Exception as e:
        print("ERROR: Component 1 — %s" % e)

    # Component 2: Page 1 image differs from old logo pattern (0.2 points)
    # Verifies the old logo was actually replaced, not just kept
    try:
        output_img = extract_page_image_data(OUTPUT_PDF, page_num=0)

        if output_img is None:
            print("FAIL: Component 2 — No image found on page 1")
        elif os.path.exists(ORIGINAL_PDF):
            old_img = extract_page_image_data(ORIGINAL_PDF, page_num=0)
            if old_img is not None:
                # Resize if needed
                if output_img.shape != old_img.shape:
                    from PIL import Image
                    old_img = np.array(
                        Image.fromarray(old_img).resize(
                            (output_img.shape[1], output_img.shape[0]),
                            Image.Resampling.LANCZOS
                        )
                    )
                old_diff = np.mean(np.abs(output_img.astype(float) - old_img.astype(float)))
                print("INFO: Component 2 — Mean pixel diff (output vs old logo): %.4f" % old_diff)

                if old_diff > 10.0:
                    print("PASS: Component 2 — Old logo successfully replaced (diff=%.4f) (0.2 pts)" % old_diff)
                    total_score += 0.2
                else:
                    print("FAIL: Component 2 — Output image still matches old logo (diff=%.4f)" % old_diff)
            else:
                print("WARN: Component 2 — Cannot extract old logo for comparison, skipping")
        else:
            print("WARN: Component 2 — Original PDF not found for comparison, skipping")
    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    # Component 3: Text content preserved across all pages (0.3 points)
    # The task requires all other content to be preserved
    try:
        if os.path.exists(ORIGINAL_PDF):
            orig_texts = get_all_text(ORIGINAL_PDF)
            out_texts = get_all_text(OUTPUT_PDF)

            if len(out_texts) != len(orig_texts):
                print("FAIL: Component 3 — Page count mismatch: original=%d, output=%d" % (len(orig_texts), len(out_texts)))
            else:
                pages_matching = 0
                total_pages = len(orig_texts)
                for i in range(total_pages):
                    orig_stripped = orig_texts[i].strip()
                    out_stripped = out_texts[i].strip()
                    if orig_stripped == out_stripped:
                        pages_matching += 1
                    else:
                        # Check similarity ratio for partial match
                        common_len = min(len(orig_stripped), len(out_stripped))
                        if common_len > 0:
                            matching_chars = sum(1 for a, b in zip(orig_stripped[:common_len], out_stripped[:common_len]) if a == b)
                            ratio = matching_chars / max(len(orig_stripped), len(out_stripped))
                            if ratio > 0.95:
                                pages_matching += 1
                                print("INFO: Component 3 — Page %d text ~%.1f%% similar" % (i, ratio * 100))
                            else:
                                print("FAIL: Component 3 — Page %d text differs (similarity=%.1f%%)" % (i, ratio * 100))
                        else:
                            print("FAIL: Component 3 — Page %d text empty or differs significantly" % i)

                if pages_matching == total_pages:
                    print("PASS: Component 3 — All %d pages text content preserved (0.3 pts)" % total_pages)
                    total_score += 0.3
                elif pages_matching > 0:
                    partial = 0.3 * (pages_matching / total_pages)
                    print("PARTIAL: Component 3 — %d/%d pages text preserved (%.2f pts)" % (pages_matching, total_pages, partial))
                    total_score += partial
                else:
                    print("FAIL: Component 3 — No pages have matching text content")
        else:
            print("WARN: Component 3 — Original PDF not found, cannot verify text preservation")
    except Exception as e:
        print("ERROR: Component 3 — %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
verify_task()
