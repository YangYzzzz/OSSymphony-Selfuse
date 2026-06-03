"""
Reward Script: Create two custom slideshows from a presentation
Task ID: impress_ndo_088
Domain: libreoffice_impress
Scoring:
  Component 1 (0.15): 'Technical Audience' custom show exists
  Component 2 (0.30): 'Technical Audience' contains correct slides in order
  Component 3 (0.15): 'Business Audience' custom show exists
  Component 4 (0.30): 'Business Audience' contains correct slides in order
  Component 5 (0.10): Original presentation still has 15 slides (unchanged)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ndo_088'

# Namespaces for OOXML
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}
R_NS = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'


def build_rid_to_slide_index(root):
    """Build mapping from rId to 1-based slide index using sldIdLst."""
    mapping = {}
    sldIdLst = root.find('.//p:sldIdLst', NS)
    if sldIdLst is not None:
        for i, sldId in enumerate(sldIdLst.findall('p:sldId', NS)):
            rid = sldId.get(f'{R_NS}id')
            if rid:
                mapping[rid] = i + 1  # 1-based
    return mapping


def get_custom_shows(pptx_path):
    """
    Parse custom slideshows from presentation.xml.
    Returns dict: {show_name: [slide_number, ...]} using 1-based slide indices.
    """
    shows = {}
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            with zf.open('ppt/presentation.xml') as f:
                root = ET.parse(f).getroot()

            rid_to_idx = build_rid_to_slide_index(root)

            custShowLst = root.find('.//p:custShowLst', NS)
            if custShowLst is None:
                return shows

            for custShow in custShowLst.findall('p:custShow', NS):
                name = custShow.get('name', '')
                slide_indices = []
                sldLst = custShow.find('p:sldLst', NS)
                if sldLst is not None:
                    for sld in sldLst.findall('p:sld', NS):
                        rid = sld.get(f'{R_NS}id')
                        if rid and rid in rid_to_idx:
                            slide_indices.append(rid_to_idx[rid])
                shows[name] = slide_indices
    except Exception as e:
        print(f"ERROR: Failed to parse custom shows: {e}")
    return shows


def get_slide_count(pptx_path):
    """Get total slide count from presentation.xml."""
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            with zf.open('ppt/presentation.xml') as f:
                root = ET.parse(f).getroot()
            sldIdLst = root.find('.//p:sldIdLst', NS)
            if sldIdLst is not None:
                return len(sldIdLst.findall('p:sldId', NS))
    except Exception as e:
        print(f"ERROR: Failed to count slides: {e}")
    return 0


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Parse custom shows from the file
    shows = get_custom_shows(file_path)
    print(f"INFO: Found {len(shows)} custom show(s): {list(shows.keys())}")

    # Expected slide lists (1-based)
    EXPECTED_TECH = [1, 4, 5, 6, 7, 12, 15]
    EXPECTED_BIZ = [1, 2, 3, 8, 9, 10, 15]

    # Component 1: 'Technical Audience' custom show exists (0.15 points)
    try:
        if 'Technical Audience' in shows:
            print(f"PASS: Component 1 - 'Technical Audience' custom show exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - 'Technical Audience' custom show not found. Shows: {list(shows.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: 'Technical Audience' contains correct slides in order (0.30 points)
    try:
        if 'Technical Audience' in shows:
            actual_tech = shows['Technical Audience']
            if actual_tech == EXPECTED_TECH:
                print(f"PASS: Component 2 - 'Technical Audience' slides match exactly: {actual_tech} (0.30 pts)")
                total_score += 0.30
            else:
                # Partial credit: check how many slides match
                matching = sum(1 for a, e in zip(actual_tech, EXPECTED_TECH) if a == e)
                total_expected = len(EXPECTED_TECH)
                if len(actual_tech) == total_expected and matching >= total_expected * 0.5:
                    partial = 0.15
                    print(f"PARTIAL: Component 2 - 'Technical Audience' has {matching}/{total_expected} correct positions. Got {actual_tech}, expected {EXPECTED_TECH} ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 2 - 'Technical Audience' slides wrong. Got {actual_tech}, expected {EXPECTED_TECH}")
        else:
            print(f"FAIL: Component 2 - 'Technical Audience' show not found, cannot check slides")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: 'Business Audience' custom show exists (0.15 points)
    try:
        if 'Business Audience' in shows:
            print(f"PASS: Component 3 - 'Business Audience' custom show exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - 'Business Audience' custom show not found. Shows: {list(shows.keys())}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: 'Business Audience' contains correct slides in order (0.30 points)
    try:
        if 'Business Audience' in shows:
            actual_biz = shows['Business Audience']
            if actual_biz == EXPECTED_BIZ:
                print(f"PASS: Component 4 - 'Business Audience' slides match exactly: {actual_biz} (0.30 pts)")
                total_score += 0.30
            else:
                # Partial credit
                matching = sum(1 for a, e in zip(actual_biz, EXPECTED_BIZ) if a == e)
                total_expected = len(EXPECTED_BIZ)
                if len(actual_biz) == total_expected and matching >= total_expected * 0.5:
                    partial = 0.15
                    print(f"PARTIAL: Component 4 - 'Business Audience' has {matching}/{total_expected} correct positions. Got {actual_biz}, expected {EXPECTED_BIZ} ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 - 'Business Audience' slides wrong. Got {actual_biz}, expected {EXPECTED_BIZ}")
        else:
            print(f"FAIL: Component 4 - 'Business Audience' show not found, cannot check slides")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Presentation still has 15 slides (not corrupted) (0.10 points)
    # This is a compound check: slide count is correct AND at least one custom show exists
    # The AND condition ensures it only passes when the task has been attempted
    try:
        slide_count = get_slide_count(file_path)
        if slide_count == 15 and len(shows) >= 1:
            print(f"PASS: Component 5 - Presentation has {slide_count} slides and custom shows exist (0.10 pts)")
            total_score += 0.10
        elif slide_count == 15 and len(shows) == 0:
            print(f"FAIL: Component 5 - Presentation has 15 slides but no custom shows (pre-task state)")
        else:
            print(f"FAIL: Component 5 - Expected 15 slides, found {slide_count}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
