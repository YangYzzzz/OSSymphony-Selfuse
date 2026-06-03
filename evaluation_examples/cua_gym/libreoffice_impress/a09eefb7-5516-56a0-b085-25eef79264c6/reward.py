"""
Reward Script: Embed 3 audio clips as background music for specific slide ranges
Task ID: impress_gf5_028
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.20): intro.mp3 embedded on slide 1
  - Component 2 (0.15): slide 1 audio configured to play across 3 slides
  - Component 3 (0.20): main.mp3 embedded on slide 4
  - Component 4 (0.15): slide 4 audio configured to play across 7 slides
  - Component 5 (0.15): outro.mp3 embedded on slide 11
  - Component 6 (0.10): slide 11 audio configured to play across 2 slides
  - Component 7 (0.05): no spurious audio on non-target slides
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf5_028'

# Expected audio source file sizes for identity matching
INTRO_SIZE = 475390   # /home/user/audio/intro.mp3
MAIN_SIZE = 950770    # /home/user/audio/main.mp3
OUTRO_SIZE = 316930   # /home/user/audio/outro.mp3


def get_slide_audio_info(zf, slide_num):
    """
    For a given slide, return a list of dicts with audio info:
      - media_target: the path to the media file in the zip (e.g. ppt/media/audio1.mp3)
      - media_size: size of that media file in the zip
      - num_sld: the numSld attribute from cMediaNode (how many slides it spans)
    Returns empty list if no audio found on this slide.
    """
    results = []
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    ns_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

    slide_xml_path = f'ppt/slides/slide{slide_num}.xml'
    rels_path = f'ppt/slides/_rels/slide{slide_num}.xml.rels'

    try:
        slide_data = zf.read(slide_xml_path).decode()
    except KeyError:
        return results

    # Parse relationships to build rId -> target mapping
    rid_to_target = {}
    try:
        rels_data = zf.read(rels_path).decode()
        rels_root = ET.fromstring(rels_data)
        for rel in rels_root:
            rid = rel.get('Id', '')
            target = rel.get('Target', '')
            rel_type = rel.get('Type', '')
            if 'audio' in rel_type.lower():
                # Resolve relative path: ../media/audio1.mp3 -> ppt/media/audio1.mp3
                resolved = target.replace('../', 'ppt/')
                rid_to_target[rid] = resolved
    except KeyError:
        pass

    # Parse the slide XML for audioFile elements
    root = ET.fromstring(slide_data)

    # Find audioFile elements (in a:audioFile namespace)
    audio_files_found = []
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'audioFile':
            link_rid = elem.get(f'{{{ns_r}}}link', '')
            if link_rid and link_rid in rid_to_target:
                audio_files_found.append(rid_to_target[link_rid])

    # Find numSld from cMediaNode elements
    num_sld_values = []
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'cMediaNode':
            ns_val = elem.get('numSld', None)
            if ns_val is not None:
                num_sld_values.append(ns_val)

    # Match audio files with numSld values
    for i, media_path in enumerate(audio_files_found):
        media_size = None
        try:
            info = zf.getinfo(media_path)
            media_size = info.file_size
        except KeyError:
            pass

        num_sld = num_sld_values[i] if i < len(num_sld_values) else None

        results.append({
            'media_target': media_path,
            'media_size': media_size,
            'num_sld': num_sld,
        })

    return results


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gather audio info for all slides
    slide_audio = {}
    for s in range(1, 13):
        info = get_slide_audio_info(zf, s)
        slide_audio[s] = info

    # Component 1: intro.mp3 embedded on slide 1 (0.20 points)
    try:
        s1_audios = slide_audio.get(1, [])
        intro_found = False
        for a in s1_audios:
            if a['media_size'] == INTRO_SIZE:
                intro_found = True
                break
        if intro_found:
            print(f"PASS: Component 1 - intro.mp3 ({INTRO_SIZE} bytes) embedded on slide 1 (0.20 pts)")
            total_score += 0.20
        else:
            sizes = [a['media_size'] for a in s1_audios]
            print(f"FAIL: Component 1 - intro.mp3 not found on slide 1. Found audio sizes: {sizes}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: slide 1 audio numSld=3 (plays across slides 1-3) (0.15 points)
    try:
        s1_audios = slide_audio.get(1, [])
        num_sld_correct = False
        for a in s1_audios:
            if a['media_size'] == INTRO_SIZE and a['num_sld'] == '3':
                num_sld_correct = True
                break
        if num_sld_correct:
            print(f"PASS: Component 2 - slide 1 audio numSld=3 (spans slides 1-3) (0.15 pts)")
            total_score += 0.15
        else:
            num_slds = [a['num_sld'] for a in s1_audios]
            print(f"FAIL: Component 2 - slide 1 audio numSld should be 3, found: {num_slds}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: main.mp3 embedded on slide 4 (0.20 points)
    try:
        s4_audios = slide_audio.get(4, [])
        main_found = False
        for a in s4_audios:
            if a['media_size'] == MAIN_SIZE:
                main_found = True
                break
        if main_found:
            print(f"PASS: Component 3 - main.mp3 ({MAIN_SIZE} bytes) embedded on slide 4 (0.20 pts)")
            total_score += 0.20
        else:
            sizes = [a['media_size'] for a in s4_audios]
            print(f"FAIL: Component 3 - main.mp3 not found on slide 4. Found audio sizes: {sizes}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: slide 4 audio numSld=7 (plays across slides 4-10) (0.15 points)
    try:
        s4_audios = slide_audio.get(4, [])
        num_sld_correct = False
        for a in s4_audios:
            if a['media_size'] == MAIN_SIZE and a['num_sld'] == '7':
                num_sld_correct = True
                break
        if num_sld_correct:
            print(f"PASS: Component 4 - slide 4 audio numSld=7 (spans slides 4-10) (0.15 pts)")
            total_score += 0.15
        else:
            num_slds = [a['num_sld'] for a in s4_audios]
            print(f"FAIL: Component 4 - slide 4 audio numSld should be 7, found: {num_slds}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: outro.mp3 embedded on slide 11 (0.15 points)
    try:
        s11_audios = slide_audio.get(11, [])
        outro_found = False
        for a in s11_audios:
            if a['media_size'] == OUTRO_SIZE:
                outro_found = True
                break
        if outro_found:
            print(f"PASS: Component 5 - outro.mp3 ({OUTRO_SIZE} bytes) embedded on slide 11 (0.15 pts)")
            total_score += 0.15
        else:
            sizes = [a['media_size'] for a in s11_audios]
            print(f"FAIL: Component 5 - outro.mp3 not found on slide 11. Found audio sizes: {sizes}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: slide 11 audio numSld=2 (plays across slides 11-12) (0.10 points)
    try:
        s11_audios = slide_audio.get(11, [])
        num_sld_correct = False
        for a in s11_audios:
            if a['media_size'] == OUTRO_SIZE and a['num_sld'] == '2':
                num_sld_correct = True
                break
        if num_sld_correct:
            print(f"PASS: Component 6 - slide 11 audio numSld=2 (spans slides 11-12) (0.10 pts)")
            total_score += 0.10
        else:
            num_slds = [a['num_sld'] for a in s11_audios]
            print(f"FAIL: Component 6 - slide 11 audio numSld should be 2, found: {num_slds}")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: no spurious audio on non-target slides AND at least one target has audio (0.05 points)
    # This compound check ensures it only passes when audio exists on target slides but NOT elsewhere
    try:
        target_slides = {1, 4, 11}
        spurious_slides = []
        target_audio_count = 0
        for s in range(1, 13):
            audio_count = len(slide_audio.get(s, []))
            if s in target_slides:
                target_audio_count += audio_count
            elif audio_count > 0:
                spurious_slides.append(s)
        if len(spurious_slides) == 0 and target_audio_count >= 3:
            print(f"PASS: Component 7 - audio only on target slides 1,4,11 (0.05 pts)")
            total_score += 0.05
        elif target_audio_count < 3:
            print(f"FAIL: Component 7 - not all 3 target slides have audio ({target_audio_count}/3)")
        else:
            print(f"FAIL: Component 7 - unexpected audio found on slides: {spurious_slides}")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
