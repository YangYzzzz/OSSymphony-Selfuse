"""
Reward Script: Apply image bullets (star icon) to six list items in achievements.docx
Task ID: writer_list_033
Domain: libreoffice_writer
Scoring:
  Component 1: numPicBullet definition exists in numbering.xml (image bullet type defined) — 0.35 pts
  Component 2: All six list paragraphs reference a numId that maps to an image-bullet abstractNum — 0.45 pts
  Component 3: The image file (star_bullet.gif) is embedded in the docx media — 0.20 pts
  Total: 1.0
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_list_033'
FILE_PATH = '/home/user/Desktop/achievements.docx'

EXPECTED_TEXTS = [
    'Completed ISO 9001 certification',
    'Won Best Workplace Award',
    'Achieved zero workplace incidents for 365 days',
    'Launched three new product lines',
    'Expanded to five international markets',
    'Published ten industry white papers',
]


def verify_task(file_path):
    """
    Verify that image bullets using star_bullet.gif are applied to all six list items.
    Returns: float between 0.0 and 1.0

    Verification strategy:
    1. Parse numbering.xml to detect w:numPicBullet element (proves image bullet was defined).
    2. Walk document paragraphs to confirm all 6 list items use a numId whose abstractNum
       has w:lvlPicBulletId at level 0 (proves image bullet is actually applied).
    3. Check that an embedded GIF image file exists in word/media/ (proves the star image
       was embedded, not just referenced externally).
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open docx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    with zf:
        namelist = zf.namelist()

        # ----------------------------------------------------------------
        # Component 1: w:numPicBullet exists in numbering.xml (0.35 pts)
        # This element is ONLY present when an image bullet type is defined.
        # It is absent in the initial document which uses standard round bullets.
        # ----------------------------------------------------------------
        try:
            if 'word/numbering.xml' not in namelist:
                print("FAIL: Component 1 — numbering.xml not found in docx")
            else:
                num_xml = zf.read('word/numbering.xml').decode('utf-8')
                if 'numPicBullet' in num_xml and 'lvlPicBulletId' in num_xml:
                    # Confirm a star_bullet.gif or GIF reference exists in numbering.xml
                    has_gif_ref = '.gif' in num_xml.lower() or 'star_bullet' in num_xml.lower()
                    if has_gif_ref:
                        print("PASS: Component 1 — numPicBullet with GIF reference found in numbering.xml (0.35 pts)")
                        total_score += 0.35
                    else:
                        # Image bullet defined but not with the star GIF — partial only if lvlPicBulletId exists
                        print("PARTIAL: Component 1 — numPicBullet found but no star_bullet.gif reference; checking embedded image")
                        # Still award points if lvlPicBulletId is referenced
                        total_score += 0.15
                else:
                    print(f"FAIL: Component 1 — numPicBullet not found in numbering.xml (image bullet not defined)")
        except Exception as e:
            print(f"ERROR: Component 1 — {e}")

        # ----------------------------------------------------------------
        # Component 2: All 6 list paragraphs use image-bullet numId (0.45 pts)
        # We trace each paragraph's numId → abstractNum → check lvlPicBulletId at ilvl=0
        # ----------------------------------------------------------------
        try:
            if 'word/numbering.xml' not in namelist or 'word/document.xml' not in namelist:
                print("FAIL: Component 2 — required XML parts missing")
            else:
                num_xml = zf.read('word/numbering.xml').decode('utf-8')
                doc_xml = zf.read('word/document.xml').decode('utf-8')

                # Build map: numId -> abstractNumId
                num_to_abstract = {}
                for m in re.finditer(
                    r'<w:num\s+w:numId="(\d+)"[^>]*>.*?<w:abstractNumId\s+w:val="(\d+)"',
                    num_xml, re.DOTALL
                ):
                    num_to_abstract[m.group(1)] = m.group(2)

                # Build set of abstractNumIds that have lvlPicBulletId at ilvl=0
                pic_bullet_abstract_ids = set()
                # Find all abstractNum blocks
                for ab_match in re.finditer(
                    r'<w:abstractNum\s+w:abstractNumId="(\d+)".*?</w:abstractNum>',
                    num_xml, re.DOTALL
                ):
                    ab_id = ab_match.group(1)
                    ab_content = ab_match.group(0)
                    # Find the ilvl=0 level block
                    lvl0_match = re.search(
                        r'<w:lvl\s+w:ilvl="0".*?</w:lvl>',
                        ab_content, re.DOTALL
                    )
                    if lvl0_match:
                        lvl0_content = lvl0_match.group(0)
                        if 'lvlPicBulletId' in lvl0_content:
                            pic_bullet_abstract_ids.add(ab_id)

                # Build set of numIds that map to image-bullet abstractNums
                pic_bullet_num_ids = set()
                for nid, abid in num_to_abstract.items():
                    if abid in pic_bullet_abstract_ids:
                        pic_bullet_num_ids.add(nid)

                # Extract paragraphs with numPr from document.xml
                # Find paragraphs that contain the expected text AND have numPr
                para_blocks = re.findall(
                    r'<w:p[ >].*?</w:p>',
                    doc_xml, re.DOTALL
                )

                # For each expected text, verify it uses a pic-bullet numId
                matched_with_pic_bullet = 0
                matched_total = 0

                for para_block in para_blocks:
                    # Extract text from this paragraph
                    runs_text = ''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', para_block, re.DOTALL))
                    if not any(expected in runs_text for expected in EXPECTED_TEXTS):
                        continue

                    matched_total += 1
                    # Check numId within this paragraph
                    num_id_match = re.search(r'<w:numId\s+w:val="(\d+)"', para_block)
                    ilvl_match = re.search(r'<w:ilvl\s+w:val="(\d+)"', para_block)
                    if num_id_match:
                        num_id_val = num_id_match.group(1)
                        ilvl_val = ilvl_match.group(1) if ilvl_match else '0'
                        if num_id_val in pic_bullet_num_ids and ilvl_val == '0':
                            matched_with_pic_bullet += 1
                        else:
                            print(f"FAIL: Paragraph '{runs_text[:40]}...' uses numId={num_id_val} "
                                  f"(not an image-bullet numId; pic_bullet_num_ids={pic_bullet_num_ids})")
                    else:
                        print(f"FAIL: Paragraph '{runs_text[:40]}...' has no numPr/numId")

                print(f"INFO: Component 2 — {matched_with_pic_bullet}/{len(EXPECTED_TEXTS)} list items use image bullet numId")
                print(f"INFO: Paragraphs matched by text: {matched_total}/{len(EXPECTED_TEXTS)}")

                if matched_with_pic_bullet == len(EXPECTED_TEXTS):
                    print(f"PASS: Component 2 — All 6 list items use image-bullet numId (0.45 pts)")
                    total_score += 0.45
                elif matched_with_pic_bullet >= 4:
                    pts = round(0.45 * matched_with_pic_bullet / len(EXPECTED_TEXTS), 3)
                    print(f"PARTIAL: Component 2 — {matched_with_pic_bullet}/6 items use image bullet ({pts} pts)")
                    total_score += pts
                elif matched_with_pic_bullet > 0:
                    pts = round(0.45 * matched_with_pic_bullet / len(EXPECTED_TEXTS), 3)
                    print(f"PARTIAL: Component 2 — only {matched_with_pic_bullet}/6 items use image bullet ({pts} pts)")
                    total_score += pts
                else:
                    print("FAIL: Component 2 — No list items use image-bullet numId")

        except Exception as e:
            print(f"ERROR: Component 2 — {e}")
            import traceback
            traceback.print_exc()

        # ----------------------------------------------------------------
        # Component 3: star_bullet.gif is embedded in word/media/ (0.20 pts)
        # The initial file does not have any embedded GIF in word/media/.
        # A properly implemented image bullet embeds the GIF inside the docx.
        # ----------------------------------------------------------------
        try:
            media_gifs = [f for f in namelist if f.startswith('word/media/') and f.lower().endswith('.gif')]
            gif_embedded = len(media_gifs) > 0
            if gif_embedded:
                gif_info = zf.getinfo(media_gifs[0])
                print(f"PASS: Component 3 — GIF embedded in word/media/: {media_gifs[0]} (size={gif_info.file_size} bytes) (0.20 pts)")
                total_score += 0.20
            else:
                print("FAIL: Component 3 — No GIF found in word/media/ (star_bullet.gif not embedded)")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 3)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task(FILE_PATH)
