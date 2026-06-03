"""
Reward Script: Extract VLC audio to film_score.wav and embed as background music in cinema_club.pptx
Task ID: osworld_multi_apps_misc_065
Domain: multi_apps (VLC + LibreOffice Impress)
Scoring:
  Component 1: film_score.wav exists on Desktop and is a valid WAV file (0.3 pts)
  Component 2: cinema_club.pptx contains an embedded WAV audio file in ppt/media/ (0.4 pts)
  Component 3: The WAV audio is linked to slide 1 via an audio relationship (0.3 pts)
  Total: 1.0
"""

import os
import zipfile
import struct

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_065'

DESKTOP = os.path.join(WORKDIR, 'Desktop')
WAV_PATH = os.path.join(DESKTOP, 'film_score.wav')
PPTX_PATH = os.path.join(WORKDIR, 'cinema_club.pptx')


def is_valid_wav(path):
    """Check if a file is a valid WAV file by inspecting the RIFF/WAVE header."""
    try:
        with open(path, 'rb') as f:
            header = f.read(12)
        if len(header) < 12:
            return False
        return header[:4] == b'RIFF' and header[8:12] == b'WAVE'
    except Exception:
        return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: cinema_club.pptx must exist
    if not os.path.exists(PPTX_PATH):
        print(f"CRITICAL: cinema_club.pptx not found at {PPTX_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: pptx must be openable as zip
    try:
        with zipfile.ZipFile(PPTX_PATH, 'r') as z:
            namelist = z.namelist()
    except Exception as e:
        print(f"CRITICAL: Cannot open cinema_club.pptx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: film_score.wav exists on Desktop and is a valid WAV file (0.3 pts)
    # This checks that the user extracted the audio from the MP4 and saved it to the Desktop.
    # In initial_env: film_score.wav does NOT exist on Desktop → FAILS
    # In golden_env: film_score.wav exists and is a valid WAV → PASSES
    try:
        wav_exists_and_valid = os.path.exists(WAV_PATH) and is_valid_wav(WAV_PATH)
        if wav_exists_and_valid:
            wav_size = os.path.getsize(WAV_PATH)
            print(f"PASS: Component 1 — film_score.wav is valid WAV (size: {wav_size} bytes) (0.3 pts)")
            total_score += 0.3
        elif os.path.exists(WAV_PATH):
            print(f"FAIL: Component 1 — file at {WAV_PATH} exists but is not a valid WAV")
        else:
            print(f"FAIL: Component 1 — film_score.wav not found at {WAV_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: cinema_club.pptx contains an embedded WAV audio file in ppt/media/ (0.4 pts)
    # This checks that the WAV audio was actually embedded inside the presentation.
    # In initial_env: pptx has no ppt/media/ entries → FAILS
    # In golden_env: pptx has ppt/media/media1.wav → PASSES
    try:
        media_wav_files = [n for n in namelist
                           if n.startswith('ppt/media/') and n.lower().endswith('.wav')]
        if media_wav_files:
            # Verify the embedded file is also a valid WAV
            with zipfile.ZipFile(PPTX_PATH, 'r') as z:
                embedded_wav_data = z.read(media_wav_files[0])
            is_valid_embedded = (
                len(embedded_wav_data) >= 12
                and embedded_wav_data[:4] == b'RIFF'
                and embedded_wav_data[8:12] == b'WAVE'
            )
            if is_valid_embedded:
                print(f"PASS: Component 2 — pptx contains embedded WAV: {media_wav_files[0]} "
                      f"({len(embedded_wav_data)} bytes) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — pptx has {media_wav_files[0]} but it is not a valid WAV")
        else:
            all_media = [n for n in namelist if n.startswith('ppt/media/')]
            print(f"FAIL: Component 2 — no WAV found in ppt/media/ of cinema_club.pptx "
                  f"(media files present: {all_media})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The audio is linked to slide 1 via an audio relationship in slide1.xml.rels (0.3 pts)
    # This checks that the audio is specifically embedded as background music on the FIRST slide.
    # In initial_env: slide1.xml.rels has no audio relationship → FAILS
    # In golden_env: slide1.xml.rels contains an audio relationship pointing to a WAV → PASSES
    try:
        slide1_rels_path = 'ppt/slides/_rels/slide1.xml.rels'
        if slide1_rels_path in namelist:
            with zipfile.ZipFile(PPTX_PATH, 'r') as z:
                rels_content = z.read(slide1_rels_path).decode('utf-8')

            # Check for audio relationship type
            audio_rel_type = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/audio'
            if audio_rel_type in rels_content:
                # Also verify the target is a WAV file
                import xml.etree.ElementTree as ET
                root = ET.fromstring(rels_content)
                ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
                audio_rels = [
                    rel for rel in root.findall('r:Relationship', ns)
                    if rel.get('Type', '') == audio_rel_type
                ]
                wav_audio_rels = [
                    rel for rel in audio_rels
                    if rel.get('Target', '').lower().endswith('.wav')
                ]
                slide1_has_wav_audio = len(wav_audio_rels) > 0
                if slide1_has_wav_audio:
                    target = wav_audio_rels[0].get('Target', '')
                    print(f"PASS: Component 3 — slide 1 audio relationship targets WAV: {target} (0.3 pts)")
                    total_score += 0.3
                elif audio_rels:
                    target = audio_rels[0].get('Target', '')
                    print(f"FAIL: Component 3 — slide 1 has audio relationship but target is not WAV: {target}")
                else:
                    print(f"FAIL: Component 3 — slide1.xml.rels contains audio type string but no matching relationship element")
            else:
                print(f"FAIL: Component 3 — slide1.xml.rels has no audio relationship "
                      f"(type '{audio_rel_type}' not found)")
        else:
            print(f"FAIL: Component 3 — {slide1_rels_path} not found in pptx archive")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
