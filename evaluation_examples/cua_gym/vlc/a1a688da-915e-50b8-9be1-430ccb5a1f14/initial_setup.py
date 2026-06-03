"""
Initial Setup: Extract audio from Meditation_Guide.mp4 to FLAC
Task ID: vlcconv_006
Domain: vlc
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlcconv_006'
VIDEOS_DIR = f'{WORKDIR}/Videos'
MUSIC_DIR = f'{WORKDIR}/Music'
SOURCE_VIDEO = f'{VIDEOS_DIR}/Meditation_Guide.mp4'


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
    # Ensure directories exist
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    os.makedirs(MUSIC_DIR, exist_ok=True)

    # Create a realistic ~30-second MP4 video with stereo AAC audio
    # Using ffmpeg to generate a test video with audio that simulates
    # a meditation guide (gentle sine wave tones + color pattern video)
    subprocess.run([
        'ffmpeg', '-y',
        # Video: calming blue/green gradient pattern
        '-f', 'lavfi', '-i',
        'testsrc2=duration=30:size=1280x720:rate=24',
        # Audio: gentle stereo sine wave (meditation-like tone)
        '-f', 'lavfi', '-i',
        'sine=frequency=256:duration=30,aformat=channel_layouts=stereo',
        # Encode video as H.264, audio as AAC stereo
        '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-ac', '2',
        '-shortest',
        SOURCE_VIDEO
    ], check=True, capture_output=True)

    print(f'Source video created: {SOURCE_VIDEO}')

    # Verify the source file exists and has audio
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'a',
         '-show_entries', 'stream=codec_name,channels,sample_rate',
         '-of', 'default=noprint_wrappers=1', SOURCE_VIDEO],
        capture_output=True, text=True
    )
    print(f'Audio stream info: {result.stdout.strip()}')

    # Make sure the output file does NOT exist in initial state
    output_flac = f'{MUSIC_DIR}/Meditation_Audio.flac'
    if os.path.exists(output_flac):
        os.remove(output_flac)

    # Open a terminal for the agent to use
    launch_gui('bash -c "xfce4-terminal || gnome-terminal || xterm"', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')


create_initial()
