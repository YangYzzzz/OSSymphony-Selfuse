"""
Reward Script: Use VLC to extract a 5-second clip from 'training_video.mp4' beginning at 00:08.
               Convert the frames to greyscale in GIMP and export as 'training_bw.gif'
               with a frame delay of 80ms per frame.
Task ID: osworld_multi_apps_vlc_gimp_041
Domain: multi_apps (VLC + GIMP)
Scoring:
    Component 1: Output GIF exists and is a valid animated GIF with greyscale frames (0.3 pts)
    Component 2: Frame delay is 80ms per frame (0.3 pts)
    Component 3: GIF temporal content starts at video t=8s and is ~5 seconds long (0.4 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vlc_gimp_041'


def count_frames_and_check_greyscale(gif_path):
    """Count all frames and verify each is greyscale. Returns (n_frames, all_grey)."""
    from PIL import Image
    import numpy as np

    img = Image.open(gif_path)
    n_frames = 0
    non_grey_count = 0
    try:
        while True:
            frame = img.copy().convert('RGB')
            arr = np.array(frame)
            # Greyscale: R == G == B for all pixels
            if not (np.all(arr[:, :, 0] == arr[:, :, 1]) and np.all(arr[:, :, 1] == arr[:, :, 2])):
                non_grey_count += 1
            n_frames += 1
            img.seek(n_frames)
    except EOFError:
        pass
    return n_frames, non_grey_count == 0


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    gif_path = f'{WORKDIR}/Desktop/training_bw.gif'
    video_path = f'{WORKDIR}/Desktop/training_video.mp4'

    # Precondition gate: file must exist and be openable
    if not os.path.exists(gif_path):
        print(f"FAIL: Output file not found at {gif_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: GIF is animated with greyscale frames (0.3 points)
    # Checks: file is a GIF format, has multiple frames (>=10 for 5s clip), all frames are greyscale
    try:
        from PIL import Image

        img = Image.open(gif_path)
        img_format = img.format

        if img_format != 'GIF':
            print(f"FAIL: Component 1 — expected GIF format, got {img_format}")
        else:
            n_frames, greyscale_ok = count_frames_and_check_greyscale(gif_path)
            # A 5-second clip at typical video frame rates should have multiple frames
            # At 10fps this is 50 frames; we require at least 10 frames
            frames_ok = n_frames >= 10
            component1_pass = frames_ok and greyscale_ok
            if component1_pass:
                print(f"PASS: Component 1 — GIF has {n_frames} frames, all greyscale (0.3 pts)")
                total_score += 0.3
            elif not frames_ok:
                print(f"FAIL: Component 1 — expected at least 10 frames for a 5s clip, got {n_frames}")
            else:
                print(f"FAIL: Component 1 — GIF frames are not all greyscale (found color pixels)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Frame delay is 80ms (0.3 points)
    # Checks: each frame has duration == 80ms
    try:
        from PIL import Image

        img = Image.open(gif_path)
        i = 0
        delays = []
        try:
            while True:
                delay = img.info.get('duration', None)
                delays.append(delay)
                i += 1
                img.seek(i)
        except EOFError:
            pass

        delays_are_80ms = len(delays) > 0 and all(d == 80 for d in delays)
        if delays_are_80ms:
            print(f"PASS: Component 2 — all {len(delays)} frames have 80ms delay (0.3 pts)")
            total_score += 0.3
        elif len(delays) == 0:
            print("FAIL: Component 2 — no frames found")
        else:
            wrong = [d for d in delays if d != 80]
            print(f"FAIL: Component 2 — expected all frames to have 80ms delay, "
                  f"found non-80ms values: {set(wrong)} (checked {len(delays)} frames)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: GIF temporal content corresponds to video segment 00:08-00:13 (0.4 points)
    # Checks: first frame of GIF closely matches the video frame at t=8 seconds
    # AND the GIF has roughly the right number of frames for a 5-second clip (10-100 frames)
    try:
        from PIL import Image
        import numpy as np

        if not os.path.exists(video_path):
            print(f"FAIL: Component 3 — source video not found at {video_path}")
        else:
            # Extract video frame at t=8s using ffmpeg (no Python library can seek video frames)
            ref_frame_path = '/tmp/reward_ref_frame_8s.png'
            os.system(f'ffmpeg -ss 8 -i "{video_path}" -vframes 1 "{ref_frame_path}" -y -loglevel quiet')

            ref_exists = os.path.exists(ref_frame_path)
            if not ref_exists:
                print("FAIL: Component 3 — could not extract reference frame from video at t=8s")
            else:
                # Convert reference frame to greyscale
                ref_img = Image.open(ref_frame_path).convert('L')

                # Get first frame of GIF converted to greyscale
                gif_img = Image.open(gif_path)
                gif_img.seek(0)
                gif_frame0 = gif_img.convert('L')

                # Resize if dimensions differ
                if ref_img.size != gif_frame0.size:
                    ref_img = ref_img.resize(gif_frame0.size, Image.LANCZOS)

                ref_arr = np.array(ref_img, dtype=float)
                gif_arr = np.array(gif_frame0, dtype=float)
                mean_diff = np.mean(np.abs(ref_arr - gif_arr))

                # Also check approximate frame count for 5-second duration
                n_frames_c3 = 0
                try:
                    while True:
                        n_frames_c3 += 1
                        gif_img.seek(n_frames_c3)
                except EOFError:
                    pass

                # At 10fps, 5 seconds = 50 frames; allow 10-100 frames for varying fps
                duration_ok = 10 <= n_frames_c3 <= 100
                # mean_diff < 5.0: pixel-accurate or near-accurate match with the 8s frame
                segment_ok = mean_diff < 5.0

                component3_pass = segment_ok and duration_ok
                if component3_pass:
                    print(f"PASS: Component 3 — GIF first frame matches video at t=8s "
                          f"(mean pixel diff: {mean_diff:.2f}), {n_frames_c3} frames for ~5s segment (0.4 pts)")
                    total_score += 0.4
                elif not segment_ok:
                    print(f"FAIL: Component 3 — GIF first frame does not match video at t=8s "
                          f"(mean pixel diff: {mean_diff:.2f}, threshold: 5.0)")
                else:
                    print(f"FAIL: Component 3 — frame count {n_frames_c3} outside expected range 10-100 "
                          f"for a 5-second clip")

                # Cleanup temp file
                try:
                    os.remove(ref_frame_path)
                except Exception:
                    pass
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
