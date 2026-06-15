"""
FINAL REWARD SCRIPT - SUCCESS
Task: Is there a quick way to swap out Times New Roman for Liberation Serif across my whole presentation? I want to make sure every slide consistently uses Liberation Serif.
Generated: 2025-08-07 08:27:43
Status: success
Model: o4-mini
Total Steps: 11
"""

import os
import zipfile
from lxml import etree

def verify_font_swap(file_path):
    print("Starting font swap verification: swap Times New Roman to Liberation Serif")
    total_score = 0.0
    max_score = 1.0

    # Requirement 1: File exists (0.2 points)
    if os.path.exists(file_path):
        print("✓ File exists (0.2 points)")
        total_score += 0.2
    else:
        print(f"✗ File not found: {file_path} (0/0.2 points)")
        print(f"REWARD: {total_score}")
        return total_score

    # Requirement 2: Open PPTX as zip (0.1 points)
    try:
        pptx_zip = zipfile.ZipFile(file_path, 'r')
        print("✓ Opened PPTX as zip (0.1 points)")
        total_score += 0.1
    except Exception as e:
        print(f"✗ Failed to open PPTX as zip: {e} (0/0.1 points)")
        print(f"REWARD: {total_score}")
        return total_score

    # Gather slide files
    slide_files = [f for f in pptx_zip.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
    if not slide_files:
        print("✗ No slide XML files found (0 points)")
        print(f"REWARD: {total_score}")
        return total_score
    print(f"Found {len(slide_files)} slide files for verification")

    # Requirement 3: No explicit Times New Roman overrides (0.3 points)
    times_overrides = 0
    ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    for slide_file in slide_files:
        try:
            data = pptx_zip.read(slide_file)
            root = etree.fromstring(data)
            for rfonts in root.xpath('//a:rPr/a:rFonts', namespaces=ns):
                for attr in ['latin', 'ascii', 'cs', 'eastAsia']:
                    tf = rfonts.get(attr)
                    if tf and tf.strip().lower() == 'times new roman':
                        times_overrides += 1
        except Exception as e:
            print(f"✗ Error parsing {slide_file}: {e}")
    if times_overrides == 0:
        print("✓ No explicit 'Times New Roman' overrides found (0.3 points)")
        total_score += 0.3
    else:
        print(f"✗ Found {times_overrides} 'Times New Roman' overrides (0/0.3 points)")

    # Requirement 4: Liberation Serif in each slide default or override (0.4 points)
    lib_slide_count = 0
    for slide_file in slide_files:
        try:
            data = pptx_zip.read(slide_file)
            root = etree.fromstring(data)
            # Check explicit rFonts overrides
            found = False
            for rfonts in root.xpath('//a:rPr/a:rFonts', namespaces=ns):
                for attr in ['latin', 'ascii', 'cs', 'eastAsia']:
                    tf = rfonts.get(attr)
                    if tf and tf.strip().lower() == 'liberation serif':
                        found = True
                        break
                if found:
                    break
            # If not found, check default paragraph properties
            if not found:
                for latin in root.xpath('//a:defRPr/a:latin', namespaces=ns):
                    tf = latin.get('typeface')
                    if tf and tf.strip().lower() == 'liberation serif':
                        found = True
                        break
            if found:
                lib_slide_count += 1
            else:
                print(f"✗ Slide {slide_file} lacks 'Liberation Serif' default or override")
        except Exception as e:
            print(f"✗ Error parsing {slide_file} for Liberation Serif: {e}")
    if lib_slide_count == len(slide_files):
        print(f"✓ 'Liberation Serif' found in all {lib_slide_count} slides (0.4 points)")
        total_score += 0.4
    else:
        print(f"✗ 'Liberation Serif' found only in {lib_slide_count}/{len(slide_files)} slides (0/0.4 points)")

    # Final score
    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score

# Execute verification
file_path = '/home/user/is_there_a_quick_way_to_swap_out_times_new_roman_for_liberation_serif_across_my_whole_presentation_i.pptx'
verify_font_swap(file_path)
