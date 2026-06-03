"""
Initial Setup: Convert AVI files to MP4 using ffmpeg
Task ID: vlcconv_014
Domain: vlc

Creates 5 AVI source files in ~/Videos/Old_Recordings/ using ffmpeg.
Opens a terminal window for the GUI agent to use.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
SRC_DIR = os.path.join(WORKDIR, 'Videos', 'Old_Recordings')

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
    # Create source directory
    os.makedirs(SRC_DIR, exist_ok=True)

    # Define 5 AVI clips with different durations and color patterns
    clips = [
        ("clip_01.avi", 5,  "testsrc=duration=5:size=640x480:rate=25"),
        ("clip_02.avi", 8,  "smptebars=duration=8:size=640x480:rate=25"),
        ("clip_03.avi", 3,  "color=c=red:duration=3:size=640x480:rate=25"),
        ("clip_04.avi", 6,  "mandelbrot=size=640x480:rate=25"),
        ("clip_05.avi", 4,  "life=size=640x480:rate=25"),
    ]

    for filename, duration, video_src in clips:
        output_path = os.path.join(SRC_DIR, filename)
        if os.path.exists(output_path):
            print(f"Already exists, skipping: {output_path}")
            continue

        # Generate AVI with MPEG-4 video + PCM audio
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", video_src,
            "-f", "lavfi", "-i", f"sine=frequency=440:duration={duration}",
            "-t", str(duration),
            "-c:v", "mpeg4",
            "-c:a", "pcm_s16le",
            "-pix_fmt", "yuv420p",
            output_path
        ]
        # For mandelbrot and life sources, limit duration via -t
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"ERROR creating {filename}: {result.stderr}")
        else:
            print(f"Created: {output_path}")

    # Verify files
    for filename, _, _ in clips:
        path = os.path.join(SRC_DIR, filename)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  {filename}: {size} bytes")
        else:
            print(f"  {filename}: MISSING!")

    # Open a terminal window for the GUI agent
    # Try multiple terminal emulators for compatibility
    terminals = ['gnome-terminal', 'xterm', 'xfce4-terminal', 'lxterminal']
    launched = False
    for term in terminals:
        try:
            env = os.environ.copy()
            env["DISPLAY"] = ":0"
            subprocess.Popen(
                [term],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env,
            )
            time.sleep(1.0)
            launched = True
            print(f'GUI_READY: launched {term} with DISPLAY=:0')
            break
        except FileNotFoundError:
            continue
    if not launched:
        print('WARNING: Could not find any terminal emulator')


create_initial()
