"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Impress, how can I replace the standard bullet points on slide 128 with my custom bullet graphic? The file I want to use is exactly '~/Desktop/dot.png'.
Generated: 2025-09-10 16:25:27
Status: success
Model: azure-o3
Total Steps: 12
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO
from PIL import Image


def verify_task(pptx_path: str, target_slide: int = 128) -> float:
    """Verify that standard bullet points on the specified slide were replaced
    with a custom bullet graphic.

    Scoring (progressive):
        0.3  – Slide contains bullet paragraphs
        0.3  – At least one bullet paragraph uses an image bullet (buBlip)
        0.2  – ≥90 % of bullet paragraphs use the image bullet
        0.2  – Embedded bullet image verified as a small graphic (≤64 px square)

    Returns
    -------
    float
        Progressive score between 0.0 and 1.0 (exactly 1.0 on perfect success)
    """

    ns = {
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }

    print(f"Verifying custom bullets on slide {target_slide} in '{pptx_path}'")
    total_score = 0.0

    # ------------------------------------------------------------------
    # 1. Basic presence checks (file & slide)
    # ------------------------------------------------------------------
    if not os.path.exists(pptx_path):
        print("✗ Presentation file not found")
        return 0.0

    slide_xml = f"ppt/slides/slide{target_slide}.xml"
    rels_xml = f"ppt/slides/_rels/slide{target_slide}.xml.rels"

    try:
        with zipfile.ZipFile(pptx_path) as z:
            if slide_xml not in z.namelist():
                print(f"✗ Slide XML for slide {target_slide} not found in PPTX")
                return 0.0

            # ------------------------------------------------------------------
            # 2. Parse slide XML to inspect bullet paragraphs
            # ------------------------------------------------------------------
            root = ET.fromstring(z.read(slide_xml))
            bullet_paragraphs = 0
            image_bullet_paragraphs = 0
            embed_ids = set()

            for p_elem in root.findall(".//a:p", ns):
                pPr = p_elem.find("a:pPr", ns)
                if pPr is None:
                    continue
                if pPr.find("a:buNone", ns) is not None:
                    # Explicitly no bullet
                    continue

                bu_blip = pPr.find("a:buBlip", ns)
                bu_char = pPr.find("a:buChar", ns)
                bu_auto = pPr.find("a:buAutoNum", ns)

                # Skip paragraphs that are not bullet-style
                if bu_blip is None and bu_char is None and bu_auto is None:
                    continue

                # Count bullet paragraph
                bullet_paragraphs += 1

                # If using image bullet, gather relationship id
                if bu_blip is not None:
                    image_bullet_paragraphs += 1
                    blip = bu_blip.find("a:blip", ns)
                    if blip is not None:
                        rid = blip.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                        if rid:
                            embed_ids.add(rid)

            print(f"Total bullet paragraphs: {bullet_paragraphs}")
            print(f"Bullet paragraphs using image bullets: {image_bullet_paragraphs}")

            # ------------------------------------------------------------------
            # Scoring component 1 – bullet paragraphs exist (0.3)
            # ------------------------------------------------------------------
            if bullet_paragraphs > 0:
                total_score += 0.3
                print("✓ Bullet paragraphs detected (+0.3)")
            else:
                print("✗ No bullet paragraphs found on slide – task failed")
                return 0.0  # Cannot award further points

            # ------------------------------------------------------------------
            # Scoring component 2 – at least one image bullet used (0.3)
            # ------------------------------------------------------------------
            if image_bullet_paragraphs > 0:
                total_score += 0.3
                print("✓ Image bullets detected (+0.3)")
            else:
                print("✗ No image bullets detected – still using standard bullets")

            # ------------------------------------------------------------------
            # Scoring component 3 – ≥90 % of bullets converted (0.2)
            # ------------------------------------------------------------------
            if (
                bullet_paragraphs > 0
                and image_bullet_paragraphs / bullet_paragraphs >= 0.9
            ):
                total_score += 0.2
                print("✓ ≥90% of bullets use custom image (+0.2)")
            else:
                print("✗ Less than 90% of bullets converted to image bullets")

            # ------------------------------------------------------------------
            # Scoring component 4 – verify embedded image size (0.2)
            # ------------------------------------------------------------------
            small_dot_confirmed = False
            if embed_ids and rels_xml in z.namelist():
                rels_root = ET.fromstring(z.read(rels_xml))
                for rel in rels_root.findall("*"):
                    rid = rel.get("Id")
                    if rid in embed_ids:
                        target = rel.get("Target")
                        if not target:
                            continue
                        # Resolve relative path inside ZIP structure
                        target_path = os.path.normpath(
                            os.path.join(os.path.dirname(slide_xml), target)
                        )
                        if target_path not in z.namelist():
                            continue
                        try:
                            img = Image.open(BytesIO(z.read(target_path)))
                            w, h = img.size
                            print(
                                f"Embedded bullet image dimensions: {w}×{h} pixels"
                            )
                            # Heuristic: a small bullet graphic is typically tiny – here ≤64 px
                            if w <= 64 and h <= 64:
                                small_dot_confirmed = True
                                break
                        except Exception as img_err:
                            print(f"Error reading embedded image: {img_err}")

            if small_dot_confirmed:
                total_score += 0.2
                print("✓ Embedded image verified as small graphic (+0.2)")
            else:
                print(
                    "✗ Embedded image not verified as a small graphic (≤64 px) or not found"
                )

    except Exception as e:
        # Catch-all for unexpected issues
        print(f"✗ Unexpected error during verification: {e}")
        return 0.0

    final_score = round(min(total_score, 1.0), 3)
    print(f"Total Score: {final_score} / 1.0")
    return final_score


if __name__ == "__main__":
    PPTX_FILE = (
        "/home/user/"
        "in_libreoffice_impress_how_can_i_replace_the_standard_bullet_points_on_slide_128_with_my_custom_bull_golden.pptx"
    )

    reward = verify_task(PPTX_FILE)
    print(f"REWARD: {reward}")
