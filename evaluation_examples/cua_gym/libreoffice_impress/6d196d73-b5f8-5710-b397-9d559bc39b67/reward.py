"""
Reward Script: Create a 4-slide blank presentation named 'team_roster.odp'
               and insert headshot images on designated slides.
Task ID: osworld_impress_new_presentation_images_006
Domain: libreoffice_impress
Scoring:
  Component 1: team_roster.odp exists and is a valid ODP with exactly 4 slides (0.30 pts)
  Component 2: Slide 2 contains headshot_ceo.png image blob (0.25 pts)
  Component 3: Slide 3 contains headshot_cto.png image blob (0.25 pts)
  Component 4: Slide 4 contains headshot_cfo.png image blob (0.20 pts)
  Total: 1.0
"""

import os
import zipfile
import hashlib
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_impress_new_presentation_images_006'
ODP_PATH = os.path.join(WORKDIR, 'team_roster.odp')

# Namespaces used in ODP XML
DRAW_NS = 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0'
PRES_NS = 'urn:oasis:names:tc:opendocument:xmlns:presentation:1.0'
XLINK_NS = 'http://www.w3.org/1999/xlink'


def get_file_md5(filepath):
    """Compute MD5 hash of a file."""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def get_blob_md5(data):
    """Compute MD5 hash of bytes."""
    return hashlib.md5(data).hexdigest()


def verify_task(odp_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition gate: file must exist and be a valid ZIP/ODP ---
    if not os.path.exists(odp_path):
        print("FAIL: team_roster.odp does not exist at", odp_path)
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf_test = zipfile.ZipFile(odp_path, 'r')
        zf_test.close()
    except Exception as e:
        print("FAIL: team_roster.odp is not a valid ODP/ZIP file:", e)
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # --- Load and parse content.xml ---
    try:
        with zipfile.ZipFile(odp_path, 'r') as zf:
            content_xml = zf.read('content.xml').decode('utf-8')
    except Exception as e:
        print("FAIL: Cannot read content.xml from ODP:", e)
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    try:
        root = ET.fromstring(content_xml)
    except Exception as e:
        print("FAIL: Cannot parse content.xml XML:", e)
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Find all slides (draw:page elements)
    pages = root.findall('.//{%s}page' % DRAW_NS)

    # --- Component 1: Valid ODP with exactly 4 slides (0.30 points) ---
    try:
        num_slides = len(pages)
        if num_slides == 4:
            print("PASS: Component 1 — team_roster.odp exists and has exactly 4 slides (0.30 pts)")
            total_score += 0.30
        else:
            print("FAIL: Component 1 — expected 4 slides, found:", num_slides)
    except Exception as e:
        print("ERROR: Component 1 — could not count slides:", e)

    # --- Build a map from picture href -> MD5 of blob in ODP ---
    odp_picture_md5 = {}
    try:
        with zipfile.ZipFile(odp_path, 'r') as zf:
            for name in zf.namelist():
                if name.startswith('Pictures/'):
                    data = zf.read(name)
                    odp_picture_md5[name] = get_blob_md5(data)
    except Exception as e:
        print("ERROR: Could not read Pictures from ODP:", e)

    # --- Map slide index -> image hrefs on that slide ---
    def get_image_hrefs_on_slide(page_element):
        hrefs = []
        for frame in page_element.findall('.//{%s}frame' % DRAW_NS):
            for img in frame.findall('{%s}image' % DRAW_NS):
                href = img.get('{%s}href' % XLINK_NS, '')
                if href:
                    hrefs.append(href)
        return hrefs

    # --- Expected MD5s from source PNG files ---
    expected_md5 = {}
    for png_name in ['headshot_ceo.png', 'headshot_cto.png', 'headshot_cfo.png']:
        png_path = os.path.join(WORKDIR, png_name)
        if os.path.exists(png_path):
            expected_md5[png_name] = get_file_md5(png_path)
        else:
            print("WARN: Source PNG not found:", png_path)
            expected_md5[png_name] = None

    def slide_contains_image_with_md5(slide_idx, expected_png_name):
        """Check if the slide at slide_idx (0-based) contains the expected image."""
        if slide_idx >= len(pages):
            return False
        page = pages[slide_idx]
        hrefs = get_image_hrefs_on_slide(page)
        if not hrefs:
            return False
        target_md5 = expected_md5.get(expected_png_name)
        if target_md5 is None:
            return False
        for href in hrefs:
            odp_md5 = odp_picture_md5.get(href)
            if odp_md5 == target_md5:
                return True
        return False

    # --- Component 2: Slide 2 contains headshot_ceo.png (0.25 points) ---
    try:
        if slide_contains_image_with_md5(1, 'headshot_ceo.png'):
            print("PASS: Component 2 — slide 2 contains headshot_ceo.png image blob (0.25 pts)")
            total_score += 0.25
        else:
            slide2_hrefs = get_image_hrefs_on_slide(pages[1]) if len(pages) > 1 else []
            slide2_md5s = [odp_picture_md5.get(h, 'N/A') for h in slide2_hrefs]
            print("FAIL: Component 2 — slide 2 does not contain headshot_ceo.png;",
                  "found hrefs:", slide2_hrefs, "MD5s:", slide2_md5s,
                  "expected MD5:", expected_md5.get('headshot_ceo.png'))
    except Exception as e:
        print("ERROR: Component 2 — could not verify slide 2:", e)

    # --- Component 3: Slide 3 contains headshot_cto.png (0.25 points) ---
    try:
        if slide_contains_image_with_md5(2, 'headshot_cto.png'):
            print("PASS: Component 3 — slide 3 contains headshot_cto.png image blob (0.25 pts)")
            total_score += 0.25
        else:
            slide3_hrefs = get_image_hrefs_on_slide(pages[2]) if len(pages) > 2 else []
            slide3_md5s = [odp_picture_md5.get(h, 'N/A') for h in slide3_hrefs]
            print("FAIL: Component 3 — slide 3 does not contain headshot_cto.png;",
                  "found hrefs:", slide3_hrefs, "MD5s:", slide3_md5s,
                  "expected MD5:", expected_md5.get('headshot_cto.png'))
    except Exception as e:
        print("ERROR: Component 3 — could not verify slide 3:", e)

    # --- Component 4: Slide 4 contains headshot_cfo.png (0.20 points) ---
    try:
        if slide_contains_image_with_md5(3, 'headshot_cfo.png'):
            print("PASS: Component 4 — slide 4 contains headshot_cfo.png image blob (0.20 pts)")
            total_score += 0.20
        else:
            slide4_hrefs = get_image_hrefs_on_slide(pages[3]) if len(pages) > 3 else []
            slide4_md5s = [odp_picture_md5.get(h, 'N/A') for h in slide4_hrefs]
            print("FAIL: Component 4 — slide 4 does not contain headshot_cfo.png;",
                  "found hrefs:", slide4_hrefs, "MD5s:", slide4_md5s,
                  "expected MD5:", expected_md5.get('headshot_cfo.png'))
    except Exception as e:
        print("ERROR: Component 4 — could not verify slide 4:", e)

    final_score = min(total_score, 1.0)
    print("\nScore:", round(total_score, 4), "/1.0")
    print("REWARD:", round(final_score, 4))
    return final_score


# Entrypoint — runs on the VM
verify_task(ODP_PATH)
