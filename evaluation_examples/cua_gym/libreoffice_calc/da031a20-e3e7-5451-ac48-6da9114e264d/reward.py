"""
Reward Script: Extract audio from nature_documentary.mp4 to nature_audio.wav,
               and embed it as background music on the first slide of travel_slides.pptx.
Task ID: osworld_multi_apps_misc_051
Domain: libreoffice_impress (multi-app: VLC + LibreOffice Impress)

Scoring Rubric:
  Component 1: nature_audio.wav exists on Desktop and is a valid WAV file (0.35 pts)
  Component 2: travel_slides.pptx has nature_audio.wav embedded in ppt/media/ (0.35 pts)
  Component 3: First slide has an audio relationship referencing the embedded WAV (0.30 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

DESKTOP = '/home/user/Desktop'
WAV_PATH = os.path.join(DESKTOP, 'nature_audio.wav')
PPTX_PATH = os.path.join(DESKTOP, 'travel_slides.pptx')
TASK_ID = 'osworld_multi_apps_misc_051'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: PPTX must exist
    if not os.path.isfile(PPTX_PATH):
        print(f"CRITICAL: PPTX not found at {PPTX_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: nature_audio.wav exists on Desktop and is a valid WAV file (0.35 points)
    # This FAILS on initial (no WAV file) and PASSES on golden
    try:
        if not os.path.isfile(WAV_PATH):
            print(f"FAIL: Component 1 — nature_audio.wav not found at {WAV_PATH}")
        else:
            wav_size = os.path.getsize(WAV_PATH)
            # Verify WAV header (RIFF + WAVE markers)
            with open(WAV_PATH, 'rb') as f:
                header = f.read(12)
            riff_marker = header[0:4]
            wave_marker = header[8:12]
            if riff_marker == b'RIFF' and wave_marker == b'WAVE':
                print(f"PASS: Component 1 — nature_audio.wav exists ({wav_size} bytes) and is a valid WAV file (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — nature_audio.wav exists but is not a valid WAV file "
                      f"(RIFF={riff_marker}, WAVE={wave_marker})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: travel_slides.pptx has nature_audio.wav embedded in ppt/media/ (0.35 points)
    # This FAILS on initial (no embedded audio) and PASSES on golden
    try:
        with zipfile.ZipFile(PPTX_PATH, 'r') as z:
            namelist = z.namelist()
            # Check for embedded WAV in ppt/media/
            audio_entries = [n for n in namelist if 'ppt/media/' in n and n.endswith('.wav')]
            if not audio_entries:
                print(f"FAIL: Component 2 — no WAV file found in ppt/media/ inside PPTX "
                      f"(entries in ppt/media/: {[n for n in namelist if 'ppt/media/' in n]})")
            else:
                # Check specifically for nature_audio.wav
                has_nature_audio = any('nature_audio.wav' in entry for entry in audio_entries)
                if has_nature_audio:
                    # Verify the embedded WAV is a real WAV (RIFF header)
                    wav_entry = next(e for e in audio_entries if 'nature_audio.wav' in e)
                    with z.open(wav_entry) as wf:
                        embedded_header = wf.read(12)
                    embedded_riff = embedded_header[0:4]
                    embedded_wave = embedded_header[8:12]
                    embedded_size = z.getinfo(wav_entry).file_size
                    if embedded_riff == b'RIFF' and embedded_wave == b'WAVE':
                        print(f"PASS: Component 2 — ppt/media/nature_audio.wav embedded in PPTX "
                              f"({embedded_size} bytes, valid WAV) (0.35 pts)")
                        total_score += 0.35
                    else:
                        print(f"FAIL: Component 2 — embedded WAV is not valid "
                              f"(RIFF={embedded_riff}, WAVE={embedded_wave})")
                else:
                    print(f"FAIL: Component 2 — WAV files found ({audio_entries}) but none named 'nature_audio.wav'")
    except zipfile.BadZipFile as e:
        print(f"CRITICAL: Component 2 — PPTX file is corrupted: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: First slide has audio relationship referencing embedded WAV,
    # and the audio is linked as a transition sound or background music (0.30 points)
    # This FAILS on initial (no audio relationship) and PASSES on golden
    try:
        with zipfile.ZipFile(PPTX_PATH, 'r') as z:
            # Check slide1 relationships for audio type
            slide1_rels_path = 'ppt/slides/_rels/slide1.xml.rels'
            if slide1_rels_path not in z.namelist():
                print(f"FAIL: Component 3 — {slide1_rels_path} not found in PPTX")
            else:
                with z.open(slide1_rels_path) as f:
                    rels_content = f.read().decode()

                # Parse XML to find audio relationships
                rels_root = ET.fromstring(rels_content)
                ns_rel = 'http://schemas.openxmlformats.org/package/2006/relationships'
                audio_rel_type = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/audio'

                audio_rels = [
                    rel for rel in rels_root.findall(f'{{{ns_rel}}}Relationship')
                    if rel.get('Type') == audio_rel_type
                ]

                if not audio_rels:
                    print(f"FAIL: Component 3 — no audio relationship found in slide1 rels "
                          f"(found types: {[r.get('Type').split('/')[-1] for r in rels_root.findall(f'{{{ns_rel}}}Relationship')]})")
                else:
                    # Check that the audio rel points to nature_audio.wav
                    audio_rel = audio_rels[0]
                    target = audio_rel.get('Target', '')
                    rel_id = audio_rel.get('Id', '')

                    if 'nature_audio.wav' not in target:
                        print(f"FAIL: Component 3 — audio relationship target does not reference nature_audio.wav "
                              f"(Target={target})")
                    else:
                        # Verify the audio is referenced in slide1.xml (as transition sound or embedded)
                        with z.open('ppt/slides/slide1.xml') as sf:
                            slide1_content = sf.read().decode()

                        # Check that rel_id is actually used in slide1.xml
                        if rel_id and rel_id in slide1_content:
                            print(f"PASS: Component 3 — slide1 has audio relationship (Id={rel_id}, "
                                  f"Target={target}) and it is referenced in slide1.xml (0.30 pts)")
                            total_score += 0.30
                        else:
                            print(f"FAIL: Component 3 — audio relationship (Id={rel_id}) exists in rels "
                                  f"but is not referenced in slide1.xml content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
