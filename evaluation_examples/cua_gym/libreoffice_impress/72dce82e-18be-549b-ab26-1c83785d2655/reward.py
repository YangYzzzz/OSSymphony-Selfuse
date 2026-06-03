"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm putting together a presentation and need some help. I've got this image of a logo called 'logo.png' on my slides, and I want to make it so clicking on it during the talk sends me back to the very first slide. How do I set that up in Impress?
Generated: 2025-08-07 11:10:05
Status: success
Model: o4-mini
Total Steps: 4
"""

import os, zipfile
from lxml import etree

def verify_logo_hyperlink(file_path):
    print(f"Verifying presentation file: {file_path}")
    score = 0.0
    max_score = 1.0

    # 1. Check file existence
    if os.path.exists(file_path):
        print("✓ File exists (0.2)")
        score += 0.2
    else:
        print("✗ File not found")
        print(f"REWARD: {score:.1f}")
        return score

    # 2. Open as zip to inspect PPTX internals
    try:
        pptx_zip = zipfile.ZipFile(file_path, 'r')
        print("✓ Opened pptx file (0.1)")
        score += 0.1
    except Exception as e:
        print(f"✗ Failed to open pptx: {e}")
        print(f"REWARD: {score:.1f}")
        return score

    # 3. Find slide XML files
    slide_files = [f for f in pptx_zip.namelist()
                   if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
    if slide_files:
        print(f"✓ Found {len(slide_files)} slide XMLs (0.1)")
        score += 0.1
    else:
        print("✗ No slide XMLs found")
        print(f"REWARD: {score:.1f}")
        return score

    # XML namespaces for parsing
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }

    found_image = False
    found_hyperlink = False
    correct_action = False

    # 4. Search each slide for the logo image with hyperlink
    for slide_file in slide_files:
        slide_xml = pptx_zip.read(slide_file)
        try:
            root = etree.fromstring(slide_xml)
        except Exception as e:
            print(f"✗ Error parsing {slide_file}: {e}")
            continue

        # Locate picture shapes
        pics = root.xpath('.//p:pic', namespaces=ns)
        for pic in pics:
            cNvPr = pic.find('.//p:cNvPr', ns)
            # Identify by description attribute matching 'logo.png'
            if cNvPr is not None and cNvPr.get('descr') == 'logo.png':
                print(f"✓ Found picture with descr='logo.png' in {slide_file} (0.3)")
                found_image = True

                # Check for hyperlink element
                hlink = pic.find('.//a:hlinkClick', ns)
                if hlink is not None:
                    print(f"✓ Found hyperlink element on logo (0.2)")
                    found_hyperlink = True

                    # Verify the action attribute for slide jump
                    action = hlink.get('action')
                    print(f"  action attribute: {action}")
                    # Expected action for jumping to first slide
                    if action == 'ppaction://hlinksldjump':
                        print(f"✓ Hyperlink action is correct for jumping to first slide (0.1)")
                        correct_action = True
                    else:
                        print(f"✗ Hyperlink action incorrect")
                else:
                    print(f"✗ No hyperlink on logo.png")
                break
        if found_image:
            break

    # 5. Scoring logic
    if found_image:
        score += 0.3
    else:
        print("✗ logo.png image not found (0)")
        print(f"REWARD: {score:.1f}")
        return min(score, max_score)

    if found_hyperlink:
        score += 0.2
    else:
        print("✗ Hyperlink not found on image (0)")
        print(f"REWARD: {score:.1f}")
        return min(score, max_score)

    if correct_action:
        score += 0.1
    else:
        print("✗ Hyperlink action not correct (0)")
        print(f"REWARD: {score:.1f}")
        return min(score, max_score)

    # 6. Final score cap and output
    final_score = min(score, max_score)
    print(f"Total score: {final_score:.1f}")
    return final_score

if __name__ == '__main__':
    path = '/home/user/im_putting_together_a_presentation_and_need_some_help_ive_got_this_image_of_a_logo_called_logopng_on.pptx'
    sc = verify_logo_hyperlink(path)
    print(f"REWARD: {sc:.1f}")
