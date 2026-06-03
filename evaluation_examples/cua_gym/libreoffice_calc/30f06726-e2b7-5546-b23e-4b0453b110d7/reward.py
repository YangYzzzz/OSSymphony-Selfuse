"""
Reward Script: Download foundational paper PDF and identify citing paper
Task ID: osworld_multi_apps_pdf_download_cite_004
Domain: multi_apps (libreoffice_calc + os + browser + libreoffice_writer)
Scoring:
  - Component 1: /home/user/papers/ directory exists and contains foundational_paper.pdf  (0.4 pts)
  - Component 2: foundational_paper.pdf is a valid PDF with size > 100KB                  (0.2 pts)
  - Component 3: /home/user/citing_paper.docx exists with a recognized citing paper title (0.4 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_download_cite_004'

# Papers from spreadsheet that cite ResNet (He et al., 2016 - "Deep Residual Learning for Image Recognition")
# Based on the papers_by_topic.xlsx spreadsheet context, these are recognized titles that cite ResNet
VALID_CITING_TITLES = [
    "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks",
    "Feature Pyramid Networks for Object Detection",
    "Mask R-CNN",
    "You Only Look Once: Unified, Real-Time Object Detection",
    "SSD: Single Shot MultiBox Detector",
    "Densely Connected Convolutional Networks",
    "Fully Convolutional Networks for Semantic Segmentation",
    "Very Deep Convolutional Networks for Large-Scale Image Recognition",
]

# Key identifying terms from the valid titles (for partial matching)
VALID_KEY_TERMS = [
    "faster r-cnn",
    "feature pyramid",
    "mask r-cnn",
    "you only look once",
    "ssd: single shot",
    "densely connected",
    "fully convolutional",
    "very deep convolutional",
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    papers_dir = os.path.join(WORKDIR, 'papers')
    pdf_path = os.path.join(papers_dir, 'foundational_paper.pdf')
    docx_path = os.path.join(WORKDIR, 'citing_paper.docx')

    # Component 1: papers/ directory exists and contains foundational_paper.pdf (0.4 points)
    # This FAILS on initial_env (no papers/ dir) and PASSES on golden_env
    try:
        dir_exists = os.path.isdir(papers_dir)
        if dir_exists:
            pdf_exists = os.path.isfile(pdf_path)
        else:
            pdf_exists = False

        if dir_exists and pdf_exists:
            print(f"PASS: Component 1 — papers/ directory exists and contains foundational_paper.pdf (0.4 pts)")
            total_score += 0.4
        elif not dir_exists:
            print(f"FAIL: Component 1 — /home/user/papers/ directory does not exist")
        else:
            print(f"FAIL: Component 1 — foundational_paper.pdf not found in /home/user/papers/")
            print(f"  Files in papers/: {os.listdir(papers_dir)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: foundational_paper.pdf is a valid PDF with size > 100KB (0.2 points)
    # A valid non-trivial PDF confirms it's actually the downloaded paper content
    # This FAILS on initial_env (no pdf) and PASSES on golden_env
    try:
        pdf_exists_now = os.path.isfile(pdf_path)
        if pdf_exists_now:
            file_size = os.path.getsize(pdf_path)
            with open(pdf_path, 'rb') as f:
                header = f.read(5)
            is_valid_pdf = header.startswith(b'%PDF')
            is_substantial = file_size > 100 * 1024  # > 100KB (actual ResNet PDF is ~800KB)

            if is_valid_pdf and is_substantial:
                print(f"PASS: Component 2 — foundational_paper.pdf is a valid PDF ({file_size} bytes) (0.2 pts)")
                total_score += 0.2
            elif not is_valid_pdf:
                print(f"FAIL: Component 2 — file does not start with PDF header (got: {header})")
            else:
                print(f"FAIL: Component 2 — PDF is too small ({file_size} bytes, expected > 100KB)")
        else:
            print(f"FAIL: Component 2 — foundational_paper.pdf does not exist (cannot check validity)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: citing_paper.docx exists and contains a valid citing paper title (0.4 points)
    # The task requires identifying which paper in the list cites the foundational (ResNet) paper
    # and writing its title in citing_paper.docx
    # This FAILS on initial_env (no docx) and PASSES on golden_env
    try:
        docx_exists = os.path.isfile(docx_path)
        if not docx_exists:
            print(f"FAIL: Component 3 — /home/user/citing_paper.docx does not exist")
        else:
            from docx import Document
            doc = Document(docx_path)
            # Get all text from the document
            all_text = ' '.join(p.text.strip() for p in doc.paragraphs if p.text.strip())
            print(f"  citing_paper.docx content: {repr(all_text)}")

            if not all_text:
                print(f"FAIL: Component 3 — citing_paper.docx is empty")
            else:
                all_text_lower = all_text.lower()
                # Check if document contains a valid citing paper title (full match)
                title_match = any(
                    title.lower() in all_text_lower or all_text_lower in title.lower()
                    for title in VALID_CITING_TITLES
                )
                # Also check for key identifying terms
                term_match = any(term in all_text_lower for term in VALID_KEY_TERMS)

                if title_match or term_match:
                    print(f"PASS: Component 3 — citing_paper.docx contains recognized citing paper title (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 3 — content '{all_text}' does not match any recognized citing paper title")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
