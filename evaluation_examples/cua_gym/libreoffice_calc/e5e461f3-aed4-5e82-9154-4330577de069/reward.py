"""
Reward Script: Create LibreOffice Impress presentation from images per ODT guide
Task ID: osworld_multi_apps_media_doc_edit_006
Domain: libreoffice_impress (ODP format)
Scoring:
  Component 1: Presentation file exists with 4 slides (0.25 pts)
  Component 2: Each slide contains one image from quarterly_review folder (0.35 pts)
  Component 3: Each slide has text matching its image filename without extension (0.25 pts)
  Component 4: Images cover approximately 80% of slide dimensions (0.15 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import hashlib

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_media_doc_edit_006'

PRESENTATION_PATH = '/home/user/presentations/quarterly_review.odp'
SOURCE_IMG_DIR = '/home/user/pictures/quarterly_review'
SLIDE_WIDTH_CM = 25.4
SLIDE_HEIGHT_CM = 19.05


def cm_to_float(cm_str):
    """Convert a string like '20.319cm' to a float value in cm."""
    if cm_str and cm_str.endswith('cm'):
        try:
            return float(cm_str[:-2])
        except ValueError:
            return None
    return None


def get_source_image_hashes(img_dir):
    """Return dict mapping md5 hash -> filename (no extension) for source images."""
    md5_to_name = {}
    if not os.path.isdir(img_dir):
        return md5_to_name
    for fname in sorted(os.listdir(img_dir)):
        fpath = os.path.join(img_dir, fname)
        if os.path.isfile(fpath):
            with open(fpath, 'rb') as f:
                data = f.read()
            md5 = hashlib.md5(data).hexdigest()
            name_no_ext = os.path.splitext(fname)[0]
            md5_to_name[md5] = name_no_ext
    return md5_to_name


def verify_task(pres_path, source_dir):
    """
    Verify that the LibreOffice Impress presentation matches task requirements.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(pres_path):
        print(f"FAIL (gate): Presentation file not found at {pres_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be valid ZIP (ODP is ZIP-based)
    try:
        with zipfile.ZipFile(pres_path, 'r') as z:
            namelist = z.namelist()
    except Exception as e:
        print(f"FAIL (gate): Cannot open ODP file as ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load content.xml for parsing
    try:
        with zipfile.ZipFile(pres_path, 'r') as z:
            content_xml = z.read('content.xml').decode('utf-8')
    except Exception as e:
        print(f"FAIL (gate): Cannot read content.xml from ODP: {e}")
        print("REWARD: 0.0")
        return 0.0

    root = ET.fromstring(content_xml)

    # Find all slides (draw:page elements)
    DRAW_NS = 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0'
    TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
    XLINK_NS = 'http://www.w3.org/1999/xlink'
    SVG_NS = 'urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0'

    pages = list(root.iter(f'{{{DRAW_NS}}}page'))

    # -------------------------------------------------------------------
    # Component 1: Presentation has exactly 4 slides (0.25 pts)
    # -------------------------------------------------------------------
    try:
        num_slides = len(pages)
        if num_slides == 4:
            print(f"PASS: Component 1 — 4 slides found ({num_slides} slides)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 4 slides, found {num_slides}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------
    # Component 2: Each slide contains one image from source folder (0.35 pts)
    # -------------------------------------------------------------------
    try:
        # Build map of ODP internal image paths to md5 hashes
        odp_img_md5 = {}
        with zipfile.ZipFile(pres_path, 'r') as z:
            for name in z.namelist():
                if name.startswith('Pictures/'):
                    with z.open(name) as f:
                        data = f.read()
                    odp_img_md5[name] = hashlib.md5(data).hexdigest()

        # Build source image md5 set
        source_md5_to_name = get_source_image_hashes(source_dir)
        source_md5_set = set(source_md5_to_name.keys())

        slides_with_valid_img = 0
        for page in pages:
            img_elems = list(page.iter(f'{{{DRAW_NS}}}image'))
            if len(img_elems) == 0:
                continue
            # Check if the first image in the slide comes from source folder
            href = img_elems[0].get(f'{{{XLINK_NS}}}href', '')
            md5 = odp_img_md5.get(href, None)
            if md5 and md5 in source_md5_set:
                slides_with_valid_img += 1

        if slides_with_valid_img == 4:
            print(f"PASS: Component 2 — All 4 slides contain source images from quarterly_review folder")
            total_score += 0.35
        elif slides_with_valid_img > 0:
            partial = round(0.35 * slides_with_valid_img / 4, 4)
            print(f"PARTIAL: Component 2 — {slides_with_valid_img}/4 slides contain valid source images")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No slides contain images from source folder")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------
    # Component 3: Each slide has text matching image filename (no extension) (0.25 pts)
    # -------------------------------------------------------------------
    try:
        slides_with_correct_title = 0
        mismatches = []

        # Re-build per-slide info
        with zipfile.ZipFile(pres_path, 'r') as z:
            odp_img_md5_2 = {}
            for name in z.namelist():
                if name.startswith('Pictures/'):
                    with z.open(name) as f:
                        data = f.read()
                    odp_img_md5_2[name] = hashlib.md5(data).hexdigest()

        for page in pages:
            # Get all text in this slide
            slide_texts = []
            for elem in page.iter(f'{{{TEXT_NS}}}p'):
                text = ''.join(elem.itertext()).strip()
                if text:
                    slide_texts.append(text)

            # Get the image for this slide and compute expected title
            img_elems = list(page.iter(f'{{{DRAW_NS}}}image'))
            if not img_elems:
                mismatches.append("Slide has no image")
                continue

            href = img_elems[0].get(f'{{{XLINK_NS}}}href', '')
            md5 = odp_img_md5_2.get(href, None)
            expected_title = source_md5_to_name.get(md5, None)

            if expected_title is None:
                mismatches.append(f"Image not found in source ({href})")
                continue

            # Check if expected title appears in slide texts
            if expected_title in slide_texts:
                slides_with_correct_title += 1
            else:
                mismatches.append(f"Expected '{expected_title}' in text, found: {slide_texts}")

        if slides_with_correct_title == 4:
            print(f"PASS: Component 3 — All 4 slides have text labels matching image filenames")
            total_score += 0.25
        elif slides_with_correct_title > 0:
            partial = round(0.25 * slides_with_correct_title / 4, 4)
            print(f"PARTIAL: Component 3 — {slides_with_correct_title}/4 slides have correct text labels")
            if mismatches:
                print(f"  Mismatches: {mismatches}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No slides have correct text labels")
            if mismatches:
                print(f"  Issues: {mismatches}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------
    # Component 4: Images cover approximately 80% of slide dimensions (0.15 pts)
    # -------------------------------------------------------------------
    try:
        slides_with_correct_size = 0
        size_issues = []

        for page in pages:
            # Find frames containing images
            frames = list(page.iter(f'{{{DRAW_NS}}}frame'))
            img_frame = None
            for frame in frames:
                img_children = list(frame.iter(f'{{{DRAW_NS}}}image'))
                if img_children:
                    img_frame = frame
                    break

            if img_frame is None:
                size_issues.append("No image frame found")
                continue

            w_str = img_frame.get(f'{{{SVG_NS}}}width', '')
            h_str = img_frame.get(f'{{{SVG_NS}}}height', '')

            w_cm = cm_to_float(w_str)
            h_cm = cm_to_float(h_str)

            if w_cm is None or h_cm is None:
                size_issues.append(f"Cannot parse frame size: w={w_str}, h={h_str}")
                continue

            w_ratio = w_cm / SLIDE_WIDTH_CM
            h_ratio = h_cm / SLIDE_HEIGHT_CM

            # Accept 80% coverage with ±5% tolerance (i.e., 75%-85%)
            if 0.75 <= w_ratio <= 0.85 and 0.75 <= h_ratio <= 0.85:
                slides_with_correct_size += 1
            else:
                size_issues.append(
                    f"Image size ratio {w_ratio:.3f} x {h_ratio:.3f} "
                    f"(expected ~0.80 x 0.80); img={w_cm}cm x {h_cm}cm"
                )

        if slides_with_correct_size == 4:
            print(f"PASS: Component 4 — All 4 slides have images at ~80% of slide size")
            total_score += 0.15
        elif slides_with_correct_size > 0:
            partial = round(0.15 * slides_with_correct_size / 4, 4)
            print(f"PARTIAL: Component 4 — {slides_with_correct_size}/4 slides have correct image size")
            if size_issues:
                print(f"  Issues: {size_issues}")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Images do not cover ~80% of slide")
            if size_issues:
                print(f"  Issues: {size_issues[:4]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task(PRESENTATION_PATH, SOURCE_IMG_DIR)
