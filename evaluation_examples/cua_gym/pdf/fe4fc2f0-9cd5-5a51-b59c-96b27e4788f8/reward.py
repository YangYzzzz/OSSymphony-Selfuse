"""
Reward Script: PDF Thumbnail Generator Service
Task ID: pdf_gf3_034
Domain: pdf
Scoring:
  Component 1: thumbnail_service.py exists and is valid Python (0.10)
  Component 2: thumbnails/ dir has 25 JPEG files (0.25)
  Component 3: Each thumbnail is 200x200 px (0.25)
  Component 4: Thumbnail names match PDF source names (0.15)
  Component 5: index.html exists with HTML5 + grid layout (0.10)
  Component 6: HTML has 25 thumbnail <img> refs and 25 PDF <a> links (0.15)
"""

import os
import re
import glob

WORKDIR = '/home/user'
LIBRARY = os.path.join(WORKDIR, 'library')
THUMBDIR = os.path.join(LIBRARY, 'thumbnails')
SCRIPT_PATH = os.path.join(WORKDIR, 'scripts', 'thumbnail_service.py')
HTML_PATH = os.path.join(LIBRARY, 'index.html')


def verify_task():
    total_score = 0.0

    # Gather expected PDF basenames from /home/user/library/
    pdf_files = sorted([f for f in os.listdir(LIBRARY) if f.lower().endswith('.pdf')])
    pdf_basenames = [os.path.splitext(f)[0] for f in pdf_files]

    # Component 1: thumbnail_service.py exists and is valid Python (0.10 pts)
    try:
        if os.path.isfile(SCRIPT_PATH):
            with open(SCRIPT_PATH, 'r') as f:
                source = f.read()
            # Verify it's valid Python by compiling
            compile(source, SCRIPT_PATH, 'exec')
            if len(source.strip()) > 50:
                print(f"PASS: Component 1 — thumbnail_service.py exists and is valid Python ({len(source)} chars) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — thumbnail_service.py too short ({len(source)} chars)")
        else:
            print(f"FAIL: Component 1 — {SCRIPT_PATH} not found")
    except SyntaxError as e:
        print(f"FAIL: Component 1 — thumbnail_service.py has syntax error: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: thumbnails/ directory has 25 JPEG files (0.25 pts)
    try:
        if os.path.isdir(THUMBDIR):
            jpg_files = sorted([f for f in os.listdir(THUMBDIR)
                               if f.lower().endswith(('.jpg', '.jpeg'))])
            if len(jpg_files) == 25:
                print(f"PASS: Component 2 — thumbnails/ has exactly 25 JPEG files (0.25 pts)")
                total_score += 0.25
            elif len(jpg_files) >= 20:
                partial = 0.25 * (len(jpg_files) / 25)
                print(f"PARTIAL: Component 2 — thumbnails/ has {len(jpg_files)}/25 JPEG files ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — thumbnails/ has {len(jpg_files)}/25 JPEG files")
        else:
            print(f"FAIL: Component 2 — {THUMBDIR} directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each thumbnail is exactly 200x200 px (0.25 pts)
    try:
        from PIL import Image
        if os.path.isdir(THUMBDIR):
            jpg_files = sorted([f for f in os.listdir(THUMBDIR)
                               if f.lower().endswith(('.jpg', '.jpeg'))])
            if len(jpg_files) > 0:
                correct_size_count = 0
                for jf in jpg_files:
                    img = Image.open(os.path.join(THUMBDIR, jf))
                    w, h = img.size
                    if w == 200 and h == 200:
                        correct_size_count += 1
                    img.close()
                if correct_size_count == len(jpg_files) and len(jpg_files) == 25:
                    print(f"PASS: Component 3 — all 25 thumbnails are 200x200 px (0.25 pts)")
                    total_score += 0.25
                elif correct_size_count > 0:
                    partial = 0.25 * (correct_size_count / 25)
                    print(f"PARTIAL: Component 3 — {correct_size_count}/25 thumbnails are 200x200 ({partial:.2f} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 3 — no thumbnails are 200x200 px")
            else:
                print(f"FAIL: Component 3 — no JPEG files in thumbnails/")
        else:
            print(f"FAIL: Component 3 — thumbnails/ directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Thumbnail names match PDF source names (0.15 pts)
    # e.g. report.pdf -> report.jpg
    try:
        if os.path.isdir(THUMBDIR):
            jpg_files = sorted([f for f in os.listdir(THUMBDIR)
                               if f.lower().endswith(('.jpg', '.jpeg'))])
            expected_names = set()
            for bn in pdf_basenames:
                expected_names.add(bn + '.jpg')
                expected_names.add(bn + '.jpeg')
            matched = 0
            for jf in jpg_files:
                if jf in expected_names:
                    matched += 1
            if matched == 25:
                print(f"PASS: Component 4 — all 25 thumbnails correctly named from PDFs (0.15 pts)")
                total_score += 0.15
            elif matched >= 20:
                partial = 0.15 * (matched / 25)
                print(f"PARTIAL: Component 4 — {matched}/25 thumbnails correctly named ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — only {matched}/25 thumbnails have correct names")
        else:
            print(f"FAIL: Component 4 — thumbnails/ directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: index.html exists with valid HTML5 + CSS grid layout (0.10 pts)
    try:
        if os.path.isfile(HTML_PATH):
            with open(HTML_PATH, 'r') as f:
                html = f.read()
            has_doctype = html.strip().lower().startswith('<!doctype html')
            has_grid = 'grid' in html.lower()
            has_html_tag = '<html' in html.lower()
            has_head = '<head' in html.lower()
            has_body = '<body' in html.lower()

            if has_doctype and has_grid and has_html_tag and has_head and has_body:
                print(f"PASS: Component 5 — index.html has valid HTML5 structure with CSS grid (0.10 pts)")
                total_score += 0.10
            elif has_html_tag and has_body:
                # Partial: valid HTML but missing grid or doctype
                partial = 0.05
                print(f"PARTIAL: Component 5 — HTML present but missing {'DOCTYPE' if not has_doctype else ''} {'grid' if not has_grid else ''} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — index.html missing basic HTML structure")
        else:
            print(f"FAIL: Component 5 — {HTML_PATH} not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: HTML contains 25 thumbnail <img> refs and 25 PDF <a> links (0.15 pts)
    try:
        if os.path.isfile(HTML_PATH):
            with open(HTML_PATH, 'r') as f:
                html = f.read()
            # Count img tags referencing thumbnails (jpg/jpeg)
            img_refs = re.findall(r'<img[^>]+src=["\']([^"\']*\.jpe?g)["\']', html, re.IGNORECASE)
            # Count links to PDF files
            pdf_links = re.findall(r'<a[^>]+href=["\']([^"\']*\.pdf)["\']', html, re.IGNORECASE)

            img_ok = len(img_refs) == 25
            pdf_ok = len(pdf_links) == 25

            if img_ok and pdf_ok:
                print(f"PASS: Component 6 — HTML has 25 thumbnail images and 25 PDF links (0.15 pts)")
                total_score += 0.15
            elif len(img_refs) >= 20 and len(pdf_links) >= 20:
                ratio = min(len(img_refs), len(pdf_links)) / 25
                partial = 0.15 * ratio
                print(f"PARTIAL: Component 6 — {len(img_refs)} images, {len(pdf_links)} PDF links ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 6 — {len(img_refs)} images, {len(pdf_links)} PDF links (expected 25 each)")
        else:
            print(f"FAIL: Component 6 — index.html not found, cannot check references")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
