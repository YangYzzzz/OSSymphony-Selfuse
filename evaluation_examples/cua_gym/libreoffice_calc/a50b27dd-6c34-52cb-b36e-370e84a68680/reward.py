"""
Reward Script: Extract audio from VLC video and embed as background music in LibreOffice Impress
Task ID: osworld_multi_apps_misc_054
Domain: libreoffice_impress (multi-app: VLC + LibreOffice Impress)
Scoring:
  Component 1: concert_audio.wav exists on Desktop and is a valid non-empty WAV file (0.35 pts)
  Component 2: concert_audio.wav is embedded inside music_presentation.pptx as media (0.35 pts)
  Component 3: Slide 1 has audio relationship to concert_audio.wav with autoplay/timing configured (0.30 pts)
"""

import os
import wave
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_054'

WAV_PATH = f'{WORKDIR}/Desktop/concert_audio.wav'
PPTX_PATH = f'{WORKDIR}/Desktop/music_presentation.pptx'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition gate: PPTX must be loadable ---
    if not os.path.exists(PPTX_PATH):
        print(f"CRITICAL: PPTX not found: {PPTX_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: concert_audio.wav exists on Desktop and is a valid non-empty WAV file (0.35 pts)
    # This FAILS on initial (file doesn't exist) → PASSES on golden (file was created by audio extraction)
    try:
        if not os.path.exists(WAV_PATH):
            print(f"FAIL: Component 1 — concert_audio.wav not found at {WAV_PATH}")
        else:
            wav_size = os.path.getsize(WAV_PATH)
            if wav_size < 1000:
                print(f"FAIL: Component 1 — concert_audio.wav is too small ({wav_size} bytes), likely empty/invalid")
            else:
                # Verify it's a valid WAV file by reading its header
                try:
                    with wave.open(WAV_PATH, 'r') as wf:
                        num_frames = wf.getnframes()
                        frame_rate = wf.getframerate()
                        duration = num_frames / frame_rate if frame_rate > 0 else 0
                        if num_frames > 0 and frame_rate > 0:
                            print(f"PASS: Component 1 — concert_audio.wav is a valid WAV file "
                                  f"({wav_size} bytes, {duration:.1f}s, {frame_rate}Hz) (0.35 pts)")
                            total_score += 0.35
                        else:
                            print(f"FAIL: Component 1 — concert_audio.wav has invalid frames ({num_frames}) or rate ({frame_rate})")
                except wave.Error as we:
                    print(f"FAIL: Component 1 — concert_audio.wav is not a valid WAV: {we}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: concert_audio.wav is embedded inside music_presentation.pptx (0.35 pts)
    # This FAILS on initial (no media embedded) → PASSES on golden (audio embedded as ppt/media/concert_audio.wav)
    try:
        with zipfile.ZipFile(PPTX_PATH, 'r') as zf:
            all_names = zf.namelist()
            audio_embedded = any(
                name == 'ppt/media/concert_audio.wav' or name.endswith('/concert_audio.wav')
                for name in all_names
            )
            if audio_embedded:
                # Find the embedded audio entry
                audio_entry = next(
                    name for name in all_names
                    if 'concert_audio' in name and name.startswith('ppt/')
                )
                embedded_size = zf.getinfo(audio_entry).file_size
                if embedded_size > 1000:
                    print(f"PASS: Component 2 — concert_audio.wav embedded in PPTX as '{audio_entry}' "
                          f"({embedded_size} bytes) (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 2 — concert_audio.wav embedded but too small ({embedded_size} bytes)")
            else:
                print(f"FAIL: Component 2 — concert_audio.wav not found in PPTX media. "
                      f"Available media: {[n for n in all_names if n.startswith('ppt/media')]}")
    except zipfile.BadZipFile as e:
        print(f"FAIL: Component 2 — PPTX is not a valid zip/pptx file: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Slide 1 has an audio relationship to concert_audio.wav AND timing is configured (0.30 pts)
    # This FAILS on initial (no audio relationship) → PASSES on golden (slide1.xml.rels has audio rel, timing in slide1.xml)
    try:
        with zipfile.ZipFile(PPTX_PATH, 'r') as zf:
            # Check slide1 relationships for audio type pointing to concert_audio.wav
            rels_path = 'ppt/slides/_rels/slide1.xml.rels'
            audio_rel_id = None

            if rels_path in zf.namelist():
                rels_content = zf.read(rels_path).decode('utf-8')
                rels_root = ET.fromstring(rels_content)
                # Search all children regardless of namespace
                for rel in rels_root:
                    rel_type = rel.get('Type', '')
                    rel_target = rel.get('Target', '')
                    if 'audio' in rel_type.lower() and 'concert_audio' in rel_target:
                        audio_rel_id = rel.get('Id')
                        break

            if audio_rel_id is None:
                print(f"FAIL: Component 3 — slide1.xml.rels does not contain an audio relationship to concert_audio.wav")
            else:
                # Check slide1.xml for autoplay/background timing configuration
                slide1_path = 'ppt/slides/slide1.xml'
                slide1_has_timing = False
                slide1_has_audio_ref = False

                if slide1_path in zf.namelist():
                    slide1_content = zf.read(slide1_path).decode('utf-8')
                    # Check for timing element (background playback) or audio picture shape
                    slide1_has_timing = '<p:timing>' in slide1_content or '<p:cTn' in slide1_content
                    slide1_has_audio_ref = (
                        'concert_audio' in slide1_content
                        or audio_rel_id in slide1_content
                    )

                if slide1_has_audio_ref and slide1_has_timing:
                    print(f"PASS: Component 3 — Slide 1 has audio relationship (relId={audio_rel_id}) "
                          f"with autoplay timing configured (0.30 pts)")
                    total_score += 0.30
                elif slide1_has_audio_ref:
                    print(f"PASS (partial): Component 3 — Slide 1 references concert_audio.wav but "
                          f"timing/autoplay may not be set; awarding partial credit (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 3 — Slide 1 has audio relationship but audio shape/reference "
                          f"not found in slide XML (relId={audio_rel_id} found in rels but not in slide XML)")

    except zipfile.BadZipFile as e:
        print(f"FAIL: Component 3 — PPTX is not a valid zip/pptx file: {e}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
