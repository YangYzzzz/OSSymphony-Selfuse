"""
Reward Script: Extract audio from VLC video and insert as background music in LibreOffice Impress
Task ID: osworld_multi_apps_misc_057
Domain: multi_apps (LibreOffice Impress + VLC)
Scoring:
  Component 1: portfolio_music.wav exists on Desktop as a valid WAV file (0.3 points)
  Component 2: portfolio.pptx contains embedded audio file (portfolio_music.wav in media folder) (0.4 points)
  Component 3: Embedded audio is linked via audioFile relationship in slide1 rels (0.3 points)
Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_misc_057'

PPTX_PATH = f'{WORKDIR}/portfolio.pptx'
WAV_PATH = f'{WORKDIR}/portfolio_music.wav'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Extract audio from 'reel.mp4' (VLC), save as 'portfolio_music.wav' on Desktop,
    and embed it as background music in 'portfolio.pptx' configured to play across all slides.
    """
    total_score = 0.0

    # Precondition: pptx must exist; if not, nothing can be verified
    if not os.path.exists(PPTX_PATH):
        print(f"CRITICAL: portfolio.pptx not found at {PPTX_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: portfolio_music.wav exists on Desktop as a valid WAV file (0.3 points)
    # This is a task-introduced change: initial_env has no portfolio_music.wav
    try:
        wav_exists = os.path.exists(WAV_PATH)
        if wav_exists:
            # Verify it is a real WAV file (RIFF header)
            with open(WAV_PATH, 'rb') as f:
                header = f.read(4)
            is_valid_wav = (header == b'RIFF')
            wav_size = os.path.getsize(WAV_PATH)
            if is_valid_wav and wav_size > 1000:
                print(f"PASS: Component 1 — portfolio_music.wav exists on Desktop as valid WAV (size: {wav_size} bytes) (0.3 pts)")
                total_score += 0.3
            elif not is_valid_wav:
                print(f"FAIL: Component 1 — portfolio_music.wav exists but is not a valid WAV (header: {header})")
            else:
                print(f"FAIL: Component 1 — portfolio_music.wav exists but is too small ({wav_size} bytes)")
        else:
            print(f"FAIL: Component 1 — portfolio_music.wav not found at {WAV_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: portfolio.pptx contains embedded audio 'portfolio_music.wav' in ppt/media/ (0.4 points)
    # This is a task-introduced change: initial_env pptx has no media folder / audio files
    try:
        with zipfile.ZipFile(PPTX_PATH, 'r') as zf:
            all_files = zf.namelist()
            # Look for any .wav file in the ppt/media/ directory
            media_wavs = [f for f in all_files if f.startswith('ppt/media/') and f.lower().endswith('.wav')]
            if media_wavs:
                # Verify that the WAV is named portfolio_music.wav (or contains the audio)
                wav_in_pptx = any('portfolio_music.wav' in f for f in media_wavs)
                if wav_in_pptx:
                    # Also check the embedded size is substantial (actual audio content)
                    wav_info = zf.getinfo('ppt/media/portfolio_music.wav')
                    if wav_info.file_size > 1000:
                        print(f"PASS: Component 2 — ppt/media/portfolio_music.wav embedded in pptx (size: {wav_info.file_size} bytes) (0.4 pts)")
                        total_score += 0.4
                    else:
                        print(f"FAIL: Component 2 — portfolio_music.wav in pptx but too small ({wav_info.file_size} bytes)")
                else:
                    print(f"FAIL: Component 2 — WAV file(s) found in media but not named portfolio_music.wav: {media_wavs}")
            else:
                print(f"FAIL: Component 2 — No .wav files found in ppt/media/ in portfolio.pptx")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Embedded audio is linked via p:audioFile relationship in at least one slide (0.3 points)
    # Verifies the audio is actually configured to play in the presentation (not just embedded as dead media)
    try:
        with zipfile.ZipFile(PPTX_PATH, 'r') as zf:
            all_names = zf.namelist()

            # Count slides that have audio relationship to portfolio_music.wav in their rels file
            slides_with_audio_rel = 0
            for i in range(1, 9):
                rels_path = f'ppt/slides/_rels/slide{i}.xml.rels'
                if rels_path in all_names:
                    with zf.open(rels_path) as rf:
                        rels_content = rf.read().decode('utf-8')
                    if 'relationships/audio' in rels_content and 'portfolio_music.wav' in rels_content:
                        slides_with_audio_rel += 1
                        print(f"  INFO: Audio relationship to portfolio_music.wav found in slide{i} rels")

            # Count slides that have audioFile XML element in the slide body
            slides_with_audio_element = 0
            for i in range(1, 9):
                slide_path = f'ppt/slides/slide{i}.xml'
                if slide_path in all_names:
                    with zf.open(slide_path) as sf:
                        slide_content = sf.read().decode('utf-8')
                    if 'audioFile' in slide_content:
                        slides_with_audio_element += 1
                        print(f"  INFO: audioFile element found in slide{i}.xml")

            if slides_with_audio_rel >= 1 and slides_with_audio_element >= 1:
                print(f"PASS: Component 3 — Audio linked via audioFile relationship and element present in slideshow (0.3 pts)")
                total_score += 0.3
            elif slides_with_audio_rel >= 1:
                print(f"FAIL: Component 3 — Audio relationship found in rels but audioFile element missing from slide XML")
            elif slides_with_audio_element >= 1:
                print(f"FAIL: Component 3 — audioFile element found but no audio relationship in rels")
            else:
                print(f"FAIL: Component 3 — No audio relationship or audioFile element found in any slide")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
