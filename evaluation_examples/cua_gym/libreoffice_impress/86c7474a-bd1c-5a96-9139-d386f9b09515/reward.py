"""
FINAL REWARD SCRIPT - SUCCESS
Task: Working on my slide deck, and I’d like slide 2 to have a bit of flair. How can I add just a 'Fade Smoothly' transition effect to this specific slide?
Generated: 2025-08-07 11:20:06
Status: success
Model: o4-mini
Total Steps: 7
"""

import os
import zipfile
from lxml import etree

def verify_fade_transition(file_path):
    print(f"Checking file: {file_path}")
    total_score = 0.0

    # Requirement 1: File existence (0.2 points)
    print("Checking file existence...")
    if os.path.exists(file_path):
        print("✓ File exists (0.2 points)")
        total_score += 0.2
    else:
        print("✗ File not found (0.0 points)")
        return total_score

    # Requirement 2: Can open as PPTX ZIP (0.1 points)
    try:
        z = zipfile.ZipFile(file_path, 'r')
        print("✓ Opened PPTX as ZIP (0.1 points)")
        total_score += 0.1
    except Exception as e:
        print(f"✗ Cannot open PPTX as ZIP: {e} (0.0 points)")
        return total_score

    # Requirement 3: At least two slides (0.2 points)
    slide_files = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
    print(f"Found slide files: {slide_files}")
    if len(slide_files) >= 2:
        print("✓ Found at least 2 slides (0.2 points)")
        total_score += 0.2
    else:
        print("✗ Less than 2 slides (0.0 points)")
        z.close()
        return total_score

    # Requirement 4: Transition element on slide2 (0.2 points) and fade transition (0.3 points)
    slide2_path = 'ppt/slides/slide2.xml'
    if slide2_path in slide_files:
        xml = z.read(slide2_path)
        root = etree.fromstring(xml)
        ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
        transition_elem = root.find('.//p:transition', ns)
        if transition_elem is not None:
            print("✓ Transition element found on slide2 (0.2 points)")
            total_score += 0.2
            fade_elem = transition_elem.find('.//p:fade', ns)
            if fade_elem is not None:
                print("✓ Fade transition found on slide2 (0.3 points)")
                total_score += 0.3
            else:
                print("✗ Fade transition not found on slide2 (0.0 points)")
        else:
            print("✗ No transition element on slide2 (0.0 points)")
    else:
        print("✗ slide2.xml not found (0.0 points)")

    z.close()
    final_score = min(total_score, 1.0)
    print(f"Total score: {final_score}")
    return final_score

if __name__ == '__main__':
    # Path to the slide deck to verify
    file_path = '/home/user/working_on_my_slide_deck_and_id_like_slide_2_to_have_a_bit_of_flair_how_can_i_add_just_a_fade_smooth.pptx'
    reward = verify_fade_transition(file_path)
    print(f"REWARD: {reward}")
