"""
Reward Script: Extract audio from VLC video and embed as background music in LibreOffice Impress
Task ID: osworld_multi_apps_misc_052
Domain: multi_apps (VLC + LibreOffice Impress)
Scoring:
  - Component 1 (0.4): ambient.wav exists on Desktop and is a valid WAV file
  - Component 2 (0.3): project_presentation.pptx contains embedded audio (ppt/media/ambient.wav inside ZIP)
  - Component 3 (0.3): Slide 1 of pptx has an audio relationship referencing the embedded wav
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_misc_052'

WAV_PATH = f'{WORKDIR}/ambient.wav'
PPTX_PATH = f'{WORKDIR}/project_presentation.pptx'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: pptx must exist (not a scoring component — it exists in initial state too)
    if not os.path.exists(PPTX_PATH):
        print(f"CRITICAL: project_presentation.pptx not found at {PPTX_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: ambient.wav exists on Desktop and is a valid WAV file (0.4 points)
    # This FAILS on initial (no ambient.wav) and PASSES on golden (ambient.wav created by audio extraction)
    try:
        if os.path.exists(WAV_PATH):
            with open(WAV_PATH, 'rb') as f:
                header = f.read(4)
            if header == b'RIFF':
                file_size = os.path.getsize(WAV_PATH)
                print(f"PASS: Component 1 — ambient.wav exists at Desktop, valid RIFF/WAV header, size={file_size} bytes (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — ambient.wav exists but is not a valid WAV file (header: {header})")
        else:
            print(f"FAIL: Component 1 — ambient.wav not found at {WAV_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: project_presentation.pptx contains embedded audio file (ppt/media/ambient.wav inside ZIP) (0.3 points)
    # This FAILS on initial (no media in pptx) and PASSES on golden (wav embedded in pptx)
    try:
        with zipfile.ZipFile(PPTX_PATH, 'r') as z:
            namelist = z.namelist()
            audio_media_files = [f for f in namelist if f.startswith('ppt/media/') and f.lower().endswith('.wav')]
            if audio_media_files:
                # Verify the embedded audio is non-empty and is a valid WAV
                embedded_audio = audio_media_files[0]
                audio_data = z.read(embedded_audio)
                if audio_data[:4] == b'RIFF' and len(audio_data) > 1000:
                    print(f"PASS: Component 2 — pptx contains embedded WAV audio: {embedded_audio}, size={len(audio_data)} bytes (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — embedded audio {embedded_audio} invalid or too small (size={len(audio_data)}, header={audio_data[:4]})")
            else:
                print(f"FAIL: Component 2 — no WAV audio files found in ppt/media/ within pptx (media files: {[f for f in namelist if 'media' in f]})")
    except zipfile.BadZipFile as e:
        print(f"CRITICAL: Component 2 — Cannot open pptx as ZIP: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Slide 1 has an audio relationship referencing the embedded wav (0.3 points)
    # This FAILS on initial (no audio relationship) and PASSES on golden (audio linked to slide 1)
    try:
        with zipfile.ZipFile(PPTX_PATH, 'r') as z:
            rels_path = 'ppt/slides/_rels/slide1.xml.rels'
            if rels_path in z.namelist():
                rels_content = z.read(rels_path).decode('utf-8', errors='replace')
                rels_root = ET.fromstring(rels_content)
                # Look for audio relationship type
                audio_rel_type = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/audio'
                audio_rels = [
                    rel for rel in rels_root.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')
                    if rel.get('Type') == audio_rel_type
                ]
                if audio_rels:
                    rel_target = audio_rels[0].get('Target', '')
                    print(f"PASS: Component 3 — slide1 has audio relationship pointing to: {rel_target} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — slide1.xml.rels has no audio relationship (type='{audio_rel_type}')")
                    print(f"  Existing rels: {[(r.get('Type'), r.get('Target')) for r in rels_root]}")
            else:
                print(f"FAIL: Component 3 — {rels_path} not found in pptx")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
