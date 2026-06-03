"""
Initial Setup: VLC extract + GIMP crop to GIF task
Task ID: osworld_multi_apps_vlc_gimp_037
Domain: multi_apps (VLC + GIMP)

Creates a synthetic interview.mp4 (3+ minutes) on the Desktop.
Does NOT create interview_clip.gif — that is the expected task output.
Opens VLC with the video file so the agent can start working.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TASK_ID = 'osworld_multi_apps_vlc_gimp_037'
VIDEO_FILE = f'{DESKTOP}/interview.mp4'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any leftover output gif from previous runs
    gif_output = f'{DESKTOP}/interview_clip.gif'
    if os.path.exists(gif_output):
        os.remove(gif_output)
        print(f'Removed existing: {gif_output}')

    # Generate a synthetic interview-style video using ffmpeg
    # 3.5 minutes (210 seconds), 1280x720, 30fps, with color bars + overlaid text
    # The video uses a drawtext overlay to simulate an interview setting
    if not os.path.exists(VIDEO_FILE):
        print(f'Generating interview.mp4 (this may take ~30 seconds)...')
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            # Video: gradient color background simulating a studio interview set
            '-f', 'lavfi',
            '-i', (
                'color=c=0x3a5a8c:size=1280x720:rate=24,'
                'drawtext=text=\'Interview Session\':'
                'fontcolor=white:fontsize=48:x=(w-text_w)/2:y=h/4,'
                'drawtext=text=\'Guest Speaker - Dr. Elena Martinez\':'
                'fontcolor=yellow:fontsize=28:x=(w-text_w)/2:y=h/4+70,'
                'drawtext=text=\'%{pts\\:hms}\':'
                'fontcolor=white:fontsize=20:x=20:y=20'
            ),
            # Audio: soft tone to simulate background
            '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=44100',
            '-t', '210',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-crf', '28',
            '-c:a', 'aac',
            '-b:a', '64k',
            '-shortest',
            VIDEO_FILE
        ]
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # Fallback: simpler ffmpeg command without drawtext (if fonts missing)
            print('Trying simpler ffmpeg fallback (no drawtext)...')
            ffmpeg_cmd_simple = [
                'ffmpeg', '-y',
                '-f', 'lavfi',
                '-i', 'color=c=0x3a5a8c:size=1280x720:rate=24',
                '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=44100',
                '-t', '210',
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-crf', '28',
                '-c:a', 'aac',
                '-b:a', '64k',
                '-shortest',
                VIDEO_FILE
            ]
            result2 = subprocess.run(ffmpeg_cmd_simple, capture_output=True, text=True)
            if result2.returncode != 0:
                print(f'ffmpeg error: {result2.stderr[-500:]}')
                raise RuntimeError('Failed to create interview.mp4')
        print(f'Created: {VIDEO_FILE}')
    else:
        print(f'Video already exists: {VIDEO_FILE}')

    # Verify file exists and is non-trivial
    size = os.path.getsize(VIDEO_FILE)
    print(f'Video file size: {size} bytes')
    assert size > 100_000, f'Video file too small: {size}'

    # GUI-ready startup: open VLC with the interview video
    launch_gui(f'vlc "{VIDEO_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VLC with interview.mp4 (DISPLAY=:0)')


create_initial()
