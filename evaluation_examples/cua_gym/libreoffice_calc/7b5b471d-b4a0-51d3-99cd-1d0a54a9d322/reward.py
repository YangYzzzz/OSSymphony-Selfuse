"""
Reward Script: Extract renovation data from PDF, create Impress presentation with side-by-side
comparison slides, and export as PDF.
Task ID: pdf_cross_067
Domain: pdf / libreoffice_impress
Scoring:
  - Component 1: renovation_showcase.odp exists with 6 slides (title + 5 renovation areas) — 0.35 pts
  - Component 2: ODP contains all 5 renovation area names — 0.25 pts
  - Component 3: ODP contains correct before/after satisfaction percentages for all areas — 0.20 pts
  - Component 4: renovation_showcase.pdf exists and has exactly 6 pages — 0.20 pts
Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Documents'
ODP_PATH = f'{WORKDIR}/renovation_showcase.odp'
PDF_PATH = f'{WORKDIR}/renovation_showcase.pdf'

# Ground truth: 5 renovation areas with costs and before/after satisfaction
RENOVATION_AREAS = ['Lobby', 'Cafeteria', 'Conference Rooms', 'Parking', 'Restrooms']

# Ground truth satisfaction data from task context
AREA_DATA = {
    'Lobby':            {'cost': '$50,000', 'before': '65%', 'after': '92%'},
    'Cafeteria':        {'cost': '$35,000', 'before': '58%', 'after': '88%'},
    'Conference Rooms': {'cost': '$28,000', 'before': '70%', 'after': '95%'},
    'Parking':          {'cost': '$45,000', 'before': '55%', 'after': '85%'},
    'Restrooms':        {'cost': '$22,000', 'before': '60%', 'after': '90%'},
}

ODP_NS = {
    'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'presentation': 'urn:oasis:names:tc:opendocument:xmlns:presentation:1.0',
}


def extract_odp_slide_texts(odp_path):
    """Extract text content from each slide in an ODP file.
    Returns list of lists of text strings per slide."""
    with zipfile.ZipFile(odp_path, 'r') as z:
        content = z.read('content.xml').decode('utf-8')
    root = ET.fromstring(content)
    pages = root.findall('.//draw:page', ODP_NS)
    slide_texts = []
    for page in pages:
        texts = []
        for t in page.findall('.//text:p', ODP_NS):
            text_content = ''.join(t.itertext()).strip()
            if text_content:
                texts.append(text_content)
        slide_texts.append(texts)
    return slide_texts


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ----------------------------------------------------------------
    # Component 1: renovation_showcase.odp exists with exactly 6 slides
    # (1 title slide + 5 renovation area comparison slides) — 0.35 pts
    # ----------------------------------------------------------------
    try:
        if not os.path.exists(ODP_PATH):
            print(f"FAIL: Component 1 — ODP file does not exist at {ODP_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with zipfile.ZipFile(ODP_PATH, 'r') as z:
            content = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content)
        pages = root.findall('.//draw:page', ODP_NS)
        slide_count = len(pages)

        if slide_count == 6:
            print(f"PASS: Component 1 — ODP exists with exactly 6 slides (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — ODP exists but has {slide_count} slides, expected 6")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: ODP contains all 5 renovation area names across slides — 0.25 pts
    # Each area found = 0.05 pts
    # ----------------------------------------------------------------
    try:
        slide_texts = extract_odp_slide_texts(ODP_PATH)
        # Flatten all text from slides 2-6 (area comparison slides)
        all_text = ' '.join(
            text
            for slide in slide_texts
            for text in slide
        )
        areas_found = 0
        for area in RENOVATION_AREAS:
            if area in all_text:
                areas_found += 1
                print(f"  PASS: Area '{area}' found in ODP")
            else:
                print(f"  FAIL: Area '{area}' NOT found in ODP")
        if areas_found > 0:
            area_score = areas_found * 0.05
            print(f"PASS: Component 2 — {areas_found}/5 renovation areas found ({area_score:.2f} pts)")
            total_score += area_score
        else:
            print(f"FAIL: Component 2 — No renovation areas found in ODP (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: ODP contains correct before/after satisfaction percentages
    # for all renovation areas — 0.20 pts
    # All satisfaction data present = 0.20 pts (partial: 0.04 per area)
    # ----------------------------------------------------------------
    try:
        slide_texts = extract_odp_slide_texts(ODP_PATH)
        all_text = ' '.join(
            text
            for slide in slide_texts
            for text in slide
        )
        # Check that each area's before and after percentages appear somewhere in ODP
        data_verified = 0
        for area, data in AREA_DATA.items():
            before_pct = data['before']
            after_pct = data['after']
            # The percentages must appear in the ODP text (area-agnostic check)
            # but we look holistically since percentages repeat across areas
            # Check by slide: slide index matches area order (slides 2-6)
            area_idx = RENOVATION_AREAS.index(area)
            if area_idx + 1 < len(slide_texts):
                slide_text_joined = ' '.join(slide_texts[area_idx + 1])
                # Check before% and after% appear in the correct area's slide
                has_before = before_pct in slide_text_joined
                has_after = after_pct in slide_text_joined
                if has_before and has_after:
                    data_verified += 1
                    print(f"  PASS: {area} slide has before={before_pct} and after={after_pct}")
                else:
                    print(f"  FAIL: {area} slide missing before={before_pct} ({has_before}) or after={after_pct} ({has_after})")
            else:
                print(f"  FAIL: {area} slide index {area_idx+1} out of range (only {len(slide_texts)} slides)")
        if data_verified > 0:
            data_score = data_verified * 0.04
            print(f"PASS: Component 3 — {data_verified}/5 area slides have correct before/after data ({data_score:.2f} pts)")
            total_score += data_score
        else:
            print(f"FAIL: Component 3 — No area slides have correct before/after data (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ----------------------------------------------------------------
    # Component 4: renovation_showcase.pdf exists with exactly 6 pages — 0.20 pts
    # ----------------------------------------------------------------
    try:
        if not os.path.exists(PDF_PATH):
            print(f"FAIL: Component 4 — PDF file does not exist at {PDF_PATH}")
        else:
            try:
                import pymupdf
            except ImportError:
                import fitz as pymupdf
            doc = pymupdf.open(PDF_PATH)
            page_count = doc.page_count
            doc.close()
            if page_count == 6:
                print(f"PASS: Component 4 — PDF exported with exactly 6 pages (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — PDF has {page_count} pages, expected 6")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
