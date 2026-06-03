"""
FINAL REWARD SCRIPT - SUCCESS
Task: Convert audio to 44.1kHz 16-bit WAV format and save as /home/user/Desktop/cd_quality.wav.
Generated: 2025-09-13 13:09:38
Status: success
Model: azure-o3
Total Steps: 10
"""

import os
import wave
import contextlib


def verify_audio_conversion(target_path: str = "/home/user/Desktop/cd_quality.wav") -> float:
    """Reward script for task: convert audio to 44.1 kHz / 16-bit WAV.

    Scoring (progressive):
        • PCM (uncompressed) ......................... 0.30
        • Sample-rate 44 100 Hz ...................... 0.35
        • Sample-width 16-bit (2 bytes) ............. 0.35

    Perfect file ⇒ 1.0.  File existence or successful load
    earn **no** points (they are only prerequisites).
    """

    max_score = 1.0
    score = 0.0

    print(f"Verifying target WAV file: {target_path}")

    # ---------- prerequisite: file exists ----------
    if not os.path.isfile(target_path):
        print("✗ File does not exist – task not completed")
        print("REWARD: 0.0")
        return 0.0

    print("✓ File exists (prerequisite only – 0 points)")

    # ---------- attempt to read WAV metadata ----------
    try:
        with contextlib.closing(wave.open(target_path, "rb")) as wf:
            nchannels = wf.getnchannels()
            sampwidth_bytes = wf.getsampwidth()
            framerate = wf.getframerate()
            nframes = wf.getnframes()
            comptype = wf.getcomptype()

            print(
                f"Metadata → channels: {nchannels}, sample-width: {sampwidth_bytes * 8}-bit, "
                f"sample-rate: {framerate} Hz, frames: {nframes}, comp-type: {comptype}"
            )

            # Reject empty / header-only files
            if nframes == 0:
                print("✗ WAV contains 0 frames – conversion failed")
                print("REWARD: 0.0")
                return 0.0

            # 1. PCM / uncompressed
            if comptype == "NONE":
                score += 0.30
                print("✓ PCM encoding verified (+0.30)")
            else:
                print("✗ WAV is not PCM – 0 points for encoding")

            # 2. Sample-rate 44 100 Hz
            if framerate == 44100:
                score += 0.35
                print("✓ Sample rate is 44.1 kHz (+0.35)")
            else:
                print(f"✗ Sample rate {framerate} Hz – expected 44 100 Hz")

            # 3. Sample-width 16-bit
            if sampwidth_bytes == 2:  # 2 bytes ⇒ 16-bit
                score += 0.35
                print("✓ Sample width is 16-bit (+0.35)")
            else:
                print(f"✗ Sample width {sampwidth_bytes * 8}-bit – expected 16-bit")

    except wave.Error as err:
        print(f"✗ wave.Error while opening file: {err}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as err:
        print(f"✗ Unexpected error while reading file: {err}")
        print("REWARD: 0.0")
        return 0.0

    # ---------- final score ----------
    if abs(score - 1.0) < 1e-6:
        score = 1.0  # normalise rounding glitches
    score = min(score, max_score)

    print(f"Total score: {score}/{max_score}")
    print(f"REWARD: {score}")
    return score


if __name__ == "__main__":
    verify_audio_conversion()

