"""
Reward Script: Consolidated index PDF with thumbnails, labels, and bookmarks
Task ID: pdf_pw_050
Domain: pdf
Scoring:
  Component 1: master_index.pdf exists (precondition gate, 0 pts)
  Component 2: Contains 5 thumbnail images from source docs (0.35 pts)
  Component 3: Contains text labels matching source doc titles (0.30 pts)
  Component 4: Has 5 bookmarks matching source doc titles (0.35 pts)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_050'
INDEX_PATH = os.path.join(WORKDIR, 'archive', 'master_index.pdf')
DOCS_DIR = os.path.join(WORKDIR, 'archive', 'docs')

# Expected source files
SOURCE_FILES = ['report_a.pdf', 'report_b.pdf', 'report_c.pdf', 'report_d.pdf', 'report_e.pdf']


def get_source_titles():
    """Read metadata titles from source PDFs."""
    titles = []
    for fn in sorted(SOURCE_FILES):
        path = os.path.join(DOCS_DIR, fn)
        try:
            doc = pymupdf.open(path)
            t = doc.metadata.get('title', '') or ''
            titles.append(t.strip())
            doc.close()
        except Exception as e:
            print(f"WARN: Could not read title from {fn}: {e}")
            titles.append('')
    return titles


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: master_index.pdf must exist
    if not os.path.exists(INDEX_PATH):
        print(f"CRITICAL: master_index.pdf not found at {INDEX_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(INDEX_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open master_index.pdf: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Read source doc titles for comparison
    source_titles = get_source_titles()
    print(f"Source titles: {source_titles}")

    # Component 1: Contains thumbnail images — at least 5 images across all pages (0.35 pts)
    try:
        total_images = 0
        for page_idx in range(doc.page_count):
            page = doc[page_idx]
            images = page.get_images(full=True)
            total_images += len(images)
        print(f"Total images in master_index.pdf: {total_images}")
        if total_images >= 5:
            print(f"PASS: Component 1 — Found {total_images} images (>= 5 expected) (0.35 pts)")
            total_score += 0.35
        elif total_images >= 3:
            partial = 0.35 * (total_images / 5.0)
            print(f"PARTIAL: Component 1 — Found {total_images}/5 images ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Found only {total_images} images, expected >= 5")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Text labels contain document titles (0.30 pts)
    try:
        # Extract all text from the document
        all_text = ""
        for page_idx in range(doc.page_count):
            page = doc[page_idx]
            all_text += page.get_text()

        titles_found = 0
        for title in source_titles:
            if not title:
                continue
            # Check if the title (or a truncated version) appears in the text
            # Titles may be truncated in the grid layout, so check for significant prefix
            if title in all_text:
                titles_found += 1
                print(f"  Found title: {repr(title)}")
            elif len(title) > 20 and title[:20] in all_text:
                # Allow truncated titles (common in grid layouts)
                titles_found += 1
                print(f"  Found truncated title: {repr(title[:20])}...")
            else:
                print(f"  Missing title: {repr(title)}")

        if titles_found >= 5:
            print(f"PASS: Component 2 — All {titles_found}/5 title labels found (0.30 pts)")
            total_score += 0.30
        elif titles_found > 0:
            partial = 0.30 * (titles_found / 5.0)
            print(f"PARTIAL: Component 2 — {titles_found}/5 title labels found ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No title labels found in document text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Has 5 bookmarks matching source doc titles (0.35 pts)
    try:
        toc = doc.get_toc()
        print(f"TOC entries: {len(toc)}")
        for entry in toc:
            print(f"  Bookmark: level={entry[0]}, title={repr(entry[1])}, page={entry[2]}")

        if len(toc) >= 5:
            # Check how many TOC titles match source document titles
            toc_titles = [entry[1].strip() for entry in toc]
            matches = 0
            for src_title in source_titles:
                if not src_title:
                    continue
                for toc_title in toc_titles:
                    if src_title == toc_title or src_title in toc_title or toc_title in src_title:
                        matches += 1
                        break

            if matches >= 5:
                print(f"PASS: Component 3 — {matches}/5 bookmarks match source titles (0.35 pts)")
                total_score += 0.35
            elif matches > 0:
                partial = 0.35 * (matches / 5.0)
                print(f"PARTIAL: Component 3 — {matches}/5 bookmarks match ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No bookmarks match source titles")
        elif len(toc) > 0:
            # Some bookmarks exist but fewer than 5
            partial = 0.35 * (len(toc) / 5.0)
            print(f"PARTIAL: Component 3 — Only {len(toc)}/5 bookmarks found ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No bookmarks/TOC entries found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
