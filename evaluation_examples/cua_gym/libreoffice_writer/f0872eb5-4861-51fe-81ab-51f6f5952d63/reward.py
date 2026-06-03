"""
Reward Script: Sidebar column effect with text frame
Task ID: writer_rd_072
Domain: libreoffice_writer
Scoring:
  Component 1: Frame paragraphs exist with framePr (0.20)
  Component 2: Frame width approximately 4 cm (0.15)
  Component 3: Frame contains chapter navigation labels (0.15)
  Component 4: Frame has light gray background #F2F2F2 (0.15)
  Component 5: Frame has right border, single, gray (0.15)
  Component 6: Body paragraphs have left indent (0.20)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_072'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.oxml.ns import qn
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    # Collect frame paragraphs and non-frame paragraphs
    frame_paras = []
    body_paras = []
    for i, p in enumerate(doc.paragraphs):
        pPr = p._element.find("w:pPr", ns)
        has_frame = False
        if pPr is not None:
            framePr = pPr.find("w:framePr", ns)
            if framePr is not None:
                has_frame = True
                frame_paras.append((i, p, framePr, pPr))
        if not has_frame:
            body_paras.append((i, p))

    # Component 1: Frame paragraphs exist (0.20 points)
    # Initial has 0 frame paragraphs; golden has 9
    try:
        if len(frame_paras) >= 2:
            print(f"PASS: Component 1 - Found {len(frame_paras)} frame paragraphs (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - Expected >=2 frame paragraphs, found {len(frame_paras)}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Frame width approximately 4 cm = 2268 twips (tolerance: 1800-2700) (0.15 points)
    # Initial has no frames so this scores 0
    try:
        if len(frame_paras) > 0:
            # Check the first frame paragraph's width
            first_framePr = frame_paras[0][2]
            w_str = first_framePr.get(qn("w:w"))
            if w_str is not None:
                w_val = int(w_str)
                # 4 cm = 2268 twips. Allow 1800-2700 (approx 3.2-4.8 cm)
                if 1800 <= w_val <= 2700:
                    print(f"PASS: Component 2 - Frame width={w_val} twips (~{w_val/567:.1f} cm), within tolerance (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 2 - Frame width={w_val} twips (~{w_val/567:.1f} cm), expected ~2268 (4.0 cm)")
            else:
                print(f"FAIL: Component 2 - Frame has no width attribute")
        else:
            print(f"FAIL: Component 2 - No frame paragraphs to check width")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Frame contains chapter navigation labels (0.15 points)
    # Initial has no frames, so frame text is empty -> FAIL
    try:
        if len(frame_paras) > 0:
            frame_texts = [p.text.strip().lower() for _, p, _, _ in frame_paras]
            chapter_count = sum(1 for t in frame_texts if 'chapter' in t)
            if chapter_count >= 2:
                print(f"PASS: Component 3 - Frame has {chapter_count} chapter labels (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 - Expected >=2 chapter labels in frame, found {chapter_count}")
                print(f"  Frame texts: {frame_texts[:10]}")
        else:
            print(f"FAIL: Component 3 - No frame paragraphs for navigation labels")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Frame has light gray background (#F2F2F2) (0.15 points)
    # Initial has no frames, so no shading -> FAIL
    try:
        if len(frame_paras) > 0:
            shading_found = False
            for _, p, _, pPr in frame_paras:
                shd = pPr.find("w:shd", ns)
                if shd is not None:
                    fill = shd.get(qn("w:fill"))
                    if fill is not None:
                        fill_upper = fill.upper().lstrip('#')
                        # Accept F2F2F2 or close grays (E0E0E0 to FFFFFF range)
                        if fill_upper == "F2F2F2":
                            shading_found = True
                            break
                        else:
                            # Accept any light gray (R=G=B, value >= 0xD0)
                            try:
                                r = int(fill_upper[0:2], 16)
                                g = int(fill_upper[2:4], 16)
                                b = int(fill_upper[4:6], 16)
                                if r == g == b and r >= 0xD0:
                                    shading_found = True
                                    break
                            except (ValueError, IndexError):
                                pass
            if shading_found:
                print(f"PASS: Component 4 - Frame has light gray background (0.15 pts)")
                total_score += 0.15
            else:
                fills = []
                for _, p, _, pPr in frame_paras[:3]:
                    shd = pPr.find("w:shd", ns)
                    if shd is not None:
                        fills.append(shd.get(qn("w:fill")))
                print(f"FAIL: Component 4 - Expected light gray (#F2F2F2) background, found fills: {fills}")
        else:
            print(f"FAIL: Component 4 - No frame paragraphs for background check")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Frame has right border (single, gray ~CCCCCC) (0.15 points)
    # Initial has no frames -> FAIL
    try:
        if len(frame_paras) > 0:
            border_found = False
            for _, p, _, pPr in frame_paras:
                pBdr = pPr.find("w:pBdr", ns)
                if pBdr is not None:
                    right_bdr = pBdr.find("w:right", ns)
                    if right_bdr is not None:
                        bval = right_bdr.get(qn("w:val"))
                        bcolor = right_bdr.get(qn("w:color"))
                        if bval == "single":
                            border_found = True
                            print(f"  Right border: val={bval}, color={bcolor}")
                            break
            if border_found:
                print(f"PASS: Component 5 - Frame has right border (single) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 - No right border found on frame paragraphs")
        else:
            print(f"FAIL: Component 5 - No frame paragraphs for border check")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Body paragraphs (non-frame, after frame section) have left indent (0.20 points)
    # In golden, body content paragraphs (Heading 1 and Normal after TOC) have left_indent=1619885 EMU
    # In initial, all paragraphs have indent_emu=None -> FAIL
    try:
        # Find body content paragraphs (headings and normal text after TOC section)
        indented_body_count = 0
        total_body_content = 0
        for idx, p in body_paras:
            # Skip empty paragraphs and TOC-like short lines
            text = p.text.strip()
            if not text:
                continue
            style = p.style.name if p.style else "Normal"
            # Consider content paragraphs: Heading 1 or Normal with substantial text
            if style in ("Heading 1",) or (style == "Normal" and len(text) > 60):
                total_body_content += 1
                indent = p.paragraph_format.left_indent
                if indent is not None and indent > 0:
                    indented_body_count += 1

        if total_body_content > 0 and indented_body_count > 0:
            ratio = indented_body_count / total_body_content
            if ratio >= 0.5:
                print(f"PASS: Component 6 - {indented_body_count}/{total_body_content} body content paragraphs have left indent (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 6 - Only {indented_body_count}/{total_body_content} body content paragraphs have left indent (ratio={ratio:.2f})")
        elif total_body_content == 0:
            print(f"FAIL: Component 6 - No body content paragraphs found to check indent")
        else:
            print(f"FAIL: Component 6 - 0/{total_body_content} body content paragraphs have left indent")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
