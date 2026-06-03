"""
Reward Script: Extract audio from game_trailer.mp4 to game_ost.wav and embed into gaming_club.pptx
Task ID: osworld_multi_apps_misc_064
Domain: multi_apps (VLC + LibreOffice Impress + OS)
Scoring:
  - Component 1 (0.4): game_ost.wav exists on Desktop and is a valid WAV audio file
  - Component 2 (0.3): gaming_club.pptx contains an embedded audio file in ppt/media/
  - Component 3 (0.3): The embedded audio is referenced from slide 1 via audio relationship in slide1.xml.rels
Total: 1.0
"""

import os
import wave
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_064'

WAV_PATH = os.path.join(WORKDIR, 'Desktop', 'game_ost.wav')
PPTX_PATH = os.path.join(WORKDIR, 'gaming_club.pptx')


def check_wav_valid(path):
    """Returns (is_valid, channels, sample_rate, duration_sec) or (False, ...) on error."""
    try:
        with wave.open(path, 'r') as wf:
            n_frames = wf.getnframes()
            sample_rate = wf.getframerate()
            n_channels = wf.getnchannels()
        if n_frames > 0 and sample_rate > 0:
            return True, n_channels, sample_rate, n_frames / sample_rate
        return False, 0, 0, 0
    except Exception:
        return False, 0, 0, 0


def get_audio_media_files(pptx_path):
    """Returns list of WAV files under ppt/media/ in the PPTX zip."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        return [f for f in zf.namelist()
                if f.startswith('ppt/media/') and f.lower().endswith('.wav')]


def get_audio_data_size(pptx_path, audio_file_name):
    """Returns size in bytes of embedded audio file."""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        return len(zf.read(audio_file_name))


def get_slide1_audio_rels(pptx_path):
    """Returns list of audio Relationship elements from slide1.xml.rels."""
    audio_rel_type = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/audio'
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide1_rels_path = 'ppt/slides/_rels/slide1.xml.rels'
        if slide1_rels_path not in zf.namelist():
            return []
        rels_xml = zf.read(slide1_rels_path).decode('utf-8')
    root = ET.fromstring(rels_xml)
    ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
    audio_rels = [rel for rel in root.findall('r:Relationship', ns)
                  if rel.get('Type') == audio_rel_type]
    if not audio_rels:
        # Fallback: iterate all elements in case namespace varies
        audio_rels = [rel for rel in root.iter()
                      if rel.get('Type') == audio_rel_type]
    return audio_rels


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition: PPTX file must exist ---
    if not os.path.isfile(PPTX_PATH):
        print(f"CRITICAL: PPTX file not found: {PPTX_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: game_ost.wav exists on Desktop and is a valid WAV file (0.4 points)
    # This FAILS on initial (file doesn't exist) and PASSES on golden (file exists and is valid WAV)
    try:
        wav_exists = os.path.isfile(WAV_PATH)
        wav_valid, wav_ch, wav_sr, wav_dur = check_wav_valid(WAV_PATH) if wav_exists else (False, 0, 0, 0)
        if wav_exists and wav_valid:
            total_score += 0.4
            print(f"PASS: Component 1 — game_ost.wav found and valid WAV "
                  f"({wav_ch}ch, {wav_sr}Hz, {wav_dur:.1f}s) (0.4 pts)")
        elif not wav_exists:
            print(f"FAIL: Component 1 — game_ost.wav not found at {WAV_PATH}")
        else:
            print(f"FAIL: Component 1 — game_ost.wav found but is not a valid WAV")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: gaming_club.pptx contains an embedded WAV audio file in ppt/media/ (0.3 points)
    # This FAILS on initial (no ppt/media/ at all) and PASSES on golden (ppt/media/audio1.wav present)
    try:
        audio_media_files = get_audio_media_files(PPTX_PATH)
        has_audio_media = len(audio_media_files) > 0
        audio_data_size = get_audio_data_size(PPTX_PATH, audio_media_files[0]) if has_audio_media else 0
        if has_audio_media and audio_data_size > 0:
            total_score += 0.3
            print(f"PASS: Component 2 — Embedded audio found at {audio_media_files[0]} "
                  f"({audio_data_size} bytes) (0.3 pts)")
        elif not has_audio_media:
            print(f"FAIL: Component 2 — No WAV audio found in ppt/media/ of gaming_club.pptx")
        else:
            print(f"FAIL: Component 2 — Embedded audio file {audio_media_files[0]} is empty")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The embedded audio is referenced from slide 1 via audio relationship (0.3 points)
    # This FAILS on initial (no audio relationship in slide1.xml.rels) and PASSES on golden
    # Relationship type: .../officeDocument/2006/relationships/audio
    try:
        audio_rels = get_slide1_audio_rels(PPTX_PATH)
        has_audio_rel = len(audio_rels) > 0
        if has_audio_rel:
            target = audio_rels[0].get('Target', '')
            rel_id = audio_rels[0].get('Id', '')
            total_score += 0.3
            print(f"PASS: Component 3 — Audio relationship found in slide1.xml.rels "
                  f"(Id={rel_id}, Target={target}) (0.3 pts)")
        else:
            print(f"FAIL: Component 3 — No audio relationship type found in slide1.xml.rels")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
