"""
FINAL REWARD SCRIPT - SUCCESS
Task: Extract audio from video and save as /home/user/Desktop/lecture_audio.wav.
Generated: 2025-09-13 08:37:14
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import wave
import contextlib
import struct

def verify_audio_extraction():
    """Reward verification for: Extract audio from video and save as
    /home/user/Desktop/lecture_audio.wav.

    Progressive scoring (max 1.0):
      • 0.3  – File exists AND >1 KiB (evidence of extraction)
      • 0.5  – Valid WAV with >1 s of audio (frames > sample-rate)
      • 0.2  – Audio is not all silence (non-zero amplitude in first 10 ms)
    """

    expected_path = "/home/user/Desktop/lecture_audio.wav"
    total_score   = 0.0
    max_score     = 1.0

    print(f"Checking for extracted audio at: {expected_path}")

    # ------------------------------------------------------------------
    # 1) File existence & reasonable size (>1 KiB)
    # ------------------------------------------------------------------
    if os.path.isfile(expected_path):
        file_size = os.path.getsize(expected_path)
        print(f"✓ File exists. Size: {file_size} bytes")

        if file_size > 1024:  # minimal threshold for real audio data
            total_score += 0.3
            print("✓ File size > 1 KiB – awarding 0.3 points")
        else:
            print("✗ File size too small (<1 KiB) – likely not valid audio")
    else:
        print("✗ Expected audio file does not exist – task incomplete")
        return 0.0  # Cannot proceed further without the file

    # ------------------------------------------------------------------
    # 2) WAV structure & duration check
    # ------------------------------------------------------------------
    try:
        with contextlib.closing(wave.open(expected_path, "rb")) as wf:
            n_channels = wf.getnchannels()
            n_frames   = wf.getnframes()
            framerate  = wf.getframerate()
            sampwidth  = wf.getsampwidth()

            print(
                f"WAV details – Channels: {n_channels}, Frames: {n_frames}, "
                f"SampleRate: {framerate}, SampleWidth: {sampwidth} bytes"
            )

            # Require >1 s of audio to be confident extraction succeeded
            if n_frames > framerate:
                total_score += 0.5
                print("✓ Contains more than 1 second of audio – +0.5 points")
            elif n_frames > 0:
                total_score += 0.3  # partial credit if some audio present
                print("✓ Contains audio frames (<1 s) – +0.3 points")
            else:
                print("✗ No audio frames present – 0 points for duration check")
    except wave.Error as err:
        print(f"✗ wave.Error while parsing WAV: {err}")
    except Exception as exc:
        print(f"✗ Unexpected error while reading WAV: {exc}")

    # ------------------------------------------------------------------
    # 3) Non-silence check – inspect first 10 ms
    # ------------------------------------------------------------------
    if total_score > 0.3:  # Only attempt if WAV header looked reasonable
        try:
            with contextlib.closing(wave.open(expected_path, "rb")) as wf:
                sample_rate = wf.getframerate()
                num_samples = int(sample_rate * 0.01)  # 10 ms worth
                raw_bytes   = wf.readframes(num_samples)

                if len(raw_bytes) >= wf.getsampwidth() * num_samples:
                    fmt_char = {1: "b", 2: "h", 4: "i"}.get(wf.getsampwidth())
                    if fmt_char:
                        unpack_fmt = "<" + fmt_char * num_samples
                        samples = struct.unpack(unpack_fmt, raw_bytes[: struct.calcsize(unpack_fmt)])
                        if max(abs(s) for s in samples) > 0:
                            total_score += 0.2
                            print("✓ Detected non-silent samples – +0.2 points")
                        else:
                            print("✗ First 10 ms are silent – no extra points")
        except Exception as ex:
            print(f"! Warning: Could not perform silence check: {ex}")

    # ------------------------------------------------------------------
    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    return final_score


if __name__ == "__main__":
    reward = verify_audio_extraction()
    print(f"REWARD: {reward}")
