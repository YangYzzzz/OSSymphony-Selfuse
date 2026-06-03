"""
Reward Script: Create photo essay document from video
Task ID: osworld_multi_apps_media_image_009
Domain: multi_apps (ffmpeg + GIMP + LibreOffice Writer)

Task: Extract 8 frames from travel_vlog.mp4 at evenly spaced intervals (4 min video / 8 = 30s spacing),
resize to 640x360, apply warm color treatment in GIMP (increase red by 20, yellow by 10 via Curves),
save as JPEG, create LibreOffice Writer document at /home/user/documents/travel_essay.odt with title
'Travel Highlights', insert all 8 images in 2-column layout with captions 'Frame at [timestamp]',
and export the document as PDF.

Scoring Rubric:
  Component 1: 8 frame JPEG files at /home/user/videos/frames/ each 640x360        (0.30)
  Component 2: Warm color treatment applied (R/B ratio indicates warmth shift)      (0.20)
  Component 3: ODT document with title, 8 images in 2-column table, captions       (0.30)
  Component 4: PDF exported at /home/user/documents/travel_essay.pdf               (0.20)
  Total: 1.00

Warm treatment discriminator rationale:
  Raw frames from travel_vlog.mp4 (4-min video) have a cool/blue cast (R_mean ~75, B_mean ~217,
  R/B ratio ~0.35). After GIMP warm treatment (R+20, Yellow/R+G +10 via Curves), the expected
  result is R_mean > 120, B_mean < 200, R/B > 0.65. This threshold cleanly separates
  untreated (R/B ~0.35) from warm-treated (R/B ~0.73) frames.
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_media_image_009'
FRAMES_DIR = '/home/user/videos/frames'
ODT_PATH = '/home/user/documents/travel_essay.odt'
PDF_PATH = '/home/user/documents/travel_essay.pdf'
VIDEO_PATH = '/home/user/videos/travel_vlog.mp4'
EXPECTED_FRAME_COUNT = 8
EXPECTED_WIDTH = 640
EXPECTED_HEIGHT = 360

# Warm color treatment thresholds (derived from video analysis):
# Raw frames: R_mean ~75, B_mean ~217, R/B ~0.35 (cool/blue cast)
# Warm-treated frames: R_mean ~136, B_mean ~186, R/B ~0.73
# Threshold: R/B ratio > 0.65 indicates warm treatment was applied
WARM_RB_RATIO_THRESHOLD = 0.65
WARM_R_MEAN_THRESHOLD = 120.0


def verify_task():
    """
    Verify photo essay creation task with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -----------------------------------------------------------------------
    # Component 1: 8 JPEG frames exist at /home/user/videos/frames/ with
    #              correct dimensions 640x360 (0.30 points)
    # FAILS on initial (no frames dir), PASSES on golden (8 frames 640x360)
    # -----------------------------------------------------------------------
    try:
        from PIL import Image

        if not os.path.isdir(FRAMES_DIR):
            print(f"FAIL: Component 1 — frames directory does not exist: {FRAMES_DIR}")
        else:
            frame_files = sorted([
                f for f in os.listdir(FRAMES_DIR)
                if f.lower().endswith('.jpg') or f.lower().endswith('.jpeg')
            ])
            if len(frame_files) != EXPECTED_FRAME_COUNT:
                print(f"FAIL: Component 1 — expected {EXPECTED_FRAME_COUNT} JPEG frames, "
                      f"found {len(frame_files)}: {frame_files}")
            else:
                # Verify all frames are 640x360
                bad_frame = None
                for fname in frame_files:
                    path = os.path.join(FRAMES_DIR, fname)
                    try:
                        img = Image.open(path)
                        w, h = img.size
                        if w != EXPECTED_WIDTH or h != EXPECTED_HEIGHT:
                            bad_frame = f"{fname} has size {w}x{h}"
                            break
                    except Exception as e:
                        bad_frame = f"{fname} cannot open: {e}"
                        break

                if bad_frame is None:
                    print(f"PASS: Component 1 — {EXPECTED_FRAME_COUNT} JPEG frames found at "
                          f"{FRAMES_DIR}, all {EXPECTED_WIDTH}x{EXPECTED_HEIGHT} (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 1 — {bad_frame}, "
                          f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Warm color treatment applied to frames (0.20 points)
    #   The task says: increase red by 20, yellow by 10 via GIMP Curves.
    #   Yellow = R+G, so: R increases by ~20+10=30, G increases by ~10, B unchanged.
    #   The source video (travel_vlog.mp4) has a cool/blue cast (R/B ratio ~0.35).
    #   After warm treatment, R/B ratio rises to ~0.73.
    #   We verify: R_mean > WARM_R_MEAN_THRESHOLD AND R/B > WARM_RB_RATIO_THRESHOLD
    #   on ALL 8 frames.
    # FAILS on initial (no frames dir), PASSES on golden (warm-treated frames)
    # -----------------------------------------------------------------------
    try:
        import numpy as np
        from PIL import Image

        if not os.path.isdir(FRAMES_DIR):
            print(f"FAIL: Component 2 — frames directory does not exist, skipping warm check")
        else:
            frame_files = sorted([
                f for f in os.listdir(FRAMES_DIR)
                if f.lower().endswith('.jpg') or f.lower().endswith('.jpeg')
            ])

            if len(frame_files) == 0:
                print("FAIL: Component 2 — no frames to check warm treatment")
            else:
                frames_passing_warm = 0
                frames_failing_warm = []
                for fname in frame_files:
                    path = os.path.join(FRAMES_DIR, fname)
                    try:
                        arr = np.array(Image.open(path).convert('RGB'))
                        r_mean = float(arr[:, :, 0].mean())
                        b_mean = float(arr[:, :, 2].mean())
                        rb_ratio = r_mean / b_mean if b_mean > 0 else 0.0
                        if r_mean > WARM_R_MEAN_THRESHOLD and rb_ratio > WARM_RB_RATIO_THRESHOLD:
                            frames_passing_warm += 1
                        else:
                            frames_failing_warm.append(
                                f"{fname}: R_mean={r_mean:.1f}, B_mean={b_mean:.1f}, "
                                f"R/B={rb_ratio:.2f} (need R>{WARM_R_MEAN_THRESHOLD}, "
                                f"R/B>{WARM_RB_RATIO_THRESHOLD})"
                            )
                    except Exception as e:
                        frames_failing_warm.append(f"{fname}: error={e}")

                if frames_passing_warm == EXPECTED_FRAME_COUNT:
                    print(f"PASS: Component 2 — warm color treatment verified on all "
                          f"{EXPECTED_FRAME_COUNT} frames (R/B ratio > {WARM_RB_RATIO_THRESHOLD}, "
                          f"R_mean > {WARM_R_MEAN_THRESHOLD}) (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 2 — warm treatment not detected on "
                          f"{len(frames_failing_warm)}/{EXPECTED_FRAME_COUNT} frames. "
                          f"Failing: {frames_failing_warm[:2]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: ODT document at /home/user/documents/travel_essay.odt with:
    #   - Title "Travel Highlights" present
    #   - 8 embedded images in a 2-column table layout
    #   - Captions containing "Frame at" timestamps
    #   (0.30 points — 0.10 title, 0.10 images/table, 0.10 captions)
    # FAILS on initial (no ODT file), PASSES on golden (full document)
    # -----------------------------------------------------------------------
    try:
        if not os.path.isfile(ODT_PATH):
            print(f"FAIL: Component 3 — ODT file does not exist: {ODT_PATH}")
        else:
            with zipfile.ZipFile(ODT_PATH, 'r') as z:
                content = z.read('content.xml').decode('utf-8')

            root = ET.fromstring(content)
            ns_text = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
            ns_table = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
            ns_draw = 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0'

            comp3_score = 0.0

            # Sub-check 3a: Title "Travel Highlights" exists as paragraph or heading
            all_text_elements = (
                root.findall(f'.//{{{ns_text}}}h') +
                root.findall(f'.//{{{ns_text}}}p')
            )
            title_found = False
            for elem in all_text_elements:
                txt = ''.join(elem.itertext()).strip()
                if 'Travel Highlights' in txt:
                    title_found = True
                    break

            if title_found:
                print("PASS: Component 3a — title 'Travel Highlights' found in document (0.10 pts)")
                comp3_score += 0.10
            else:
                print("FAIL: Component 3a — title 'Travel Highlights' not found in document")

            # Sub-check 3b: 8 images embedded in 2-column table
            tables = root.findall(f'.//{{{ns_table}}}table')
            images = root.findall(f'.//{{{ns_draw}}}image')

            if len(tables) >= 1:
                table = tables[0]
                cols = table.findall(f'{{{ns_table}}}table-column')
                table_images = table.findall(f'.//{{{ns_draw}}}image')
                if len(cols) == 2 and len(table_images) == 8:
                    print(f"PASS: Component 3b — 8 images in 2-column table found (0.10 pts)")
                    comp3_score += 0.10
                elif len(cols) != 2:
                    print(f"FAIL: Component 3b — table has {len(cols)} columns, expected 2")
                else:
                    print(f"FAIL: Component 3b — table has {len(table_images)} images, expected 8")
            elif len(images) == 8:
                # Accept 8 images even outside a table
                print(f"PASS: Component 3b — 8 images found in document (no table structure) (0.10 pts)")
                comp3_score += 0.10
            else:
                print(f"FAIL: Component 3b — expected 8 images, found {len(images)}")

            # Sub-check 3c: Captions contain "Frame at" with timestamps
            all_paras = root.findall(f'.//{{{ns_text}}}p')
            caption_texts = []
            for p in all_paras:
                txt = ''.join(p.itertext()).strip()
                if txt.startswith('Frame at ') and ':' in txt:
                    caption_texts.append(txt)

            if len(caption_texts) == 8:
                print(f"PASS: Component 3c — 8 captions with 'Frame at [timestamp]' found: "
                      f"{caption_texts[:2]}... (0.10 pts)")
                comp3_score += 0.10
            elif len(caption_texts) >= 4:
                print(f"PARTIAL: Component 3c — {len(caption_texts)} captions with 'Frame at' found "
                      f"(need 8), partial credit (0.05 pts)")
                comp3_score += 0.05
            else:
                print(f"FAIL: Component 3c — found {len(caption_texts)} captions with 'Frame at', "
                      f"need 8. Found: {caption_texts}")

            total_score += comp3_score
            print(f"Component 3 total: {comp3_score:.2f}/0.30")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: PDF exported at /home/user/documents/travel_essay.pdf
    #   Must be a valid PDF file with non-trivial content (> 10KB)
    #   (0.20 points)
    # FAILS on initial (no PDF), PASSES on golden (PDF exists)
    # -----------------------------------------------------------------------
    try:
        if not os.path.isfile(PDF_PATH):
            print(f"FAIL: Component 4 — PDF not found: {PDF_PATH}")
        else:
            pdf_size = os.path.getsize(PDF_PATH)
            # Check it's a valid PDF by reading magic bytes
            with open(PDF_PATH, 'rb') as f:
                magic = f.read(4)

            if magic == b'%PDF' and pdf_size > 10000:
                print(f"PASS: Component 4 — PDF exported at {PDF_PATH} "
                      f"(size={pdf_size} bytes, valid PDF header) (0.20 pts)")
                total_score += 0.20
            elif magic != b'%PDF':
                print(f"FAIL: Component 4 — File at {PDF_PATH} is not a valid PDF "
                      f"(magic bytes: {magic})")
            else:
                print(f"FAIL: Component 4 — PDF too small ({pdf_size} bytes), "
                      f"expected > 10000 bytes")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


verify_task()
