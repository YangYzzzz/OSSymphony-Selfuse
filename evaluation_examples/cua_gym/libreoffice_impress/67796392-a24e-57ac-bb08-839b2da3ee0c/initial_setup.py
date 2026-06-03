"""
Initial Setup: Build a photo slideshow with transitions and music timing
Task ID: impress_wf_017
Domain: libreoffice_impress

Creates:
  - ~/Slideshow/img01.jpg through img10.jpg (1920x1080 placeholder images)
  - ~/Desktop/background_music.mp3 (placeholder audio file)
  - Opens LibreOffice Impress with a blank presentation
"""

import os
import shlex
import struct
import subprocess
import time

from PIL import Image, ImageDraw, ImageFont

WORKDIR = '/home/user'
TASK_ID = 'impress_wf_017'
SLIDESHOW_DIR = f'{WORKDIR}/Slideshow'
DESKTOP_DIR = f'{WORKDIR}/Desktop'


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


def create_placeholder_image(path, index, width=1920, height=1080):
    """Create a colorful placeholder image with label text."""
    # Different colors for each image
    colors = [
        (45, 85, 130),   # deep blue
        (130, 50, 50),   # dark red
        (50, 120, 60),   # forest green
        (140, 100, 40),  # golden brown
        (80, 50, 120),   # purple
        (40, 110, 110),  # teal
        (150, 80, 30),   # orange-brown
        (60, 60, 100),   # slate blue
        (100, 40, 80),   # plum
        (35, 90, 90),    # dark cyan
    ]
    color = colors[index % len(colors)]
    img = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(img)

    # Add label text
    label = f"Photo {index + 1:02d}"
    # Use default font with larger size
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    except (IOError, OSError):
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (width - tw) // 2
    y = (height - th) // 2
    draw.text((x, y), label, fill=(255, 255, 255), font=font)

    # Add some visual interest - a subtle gradient bar at bottom
    for yy in range(height - 60, height):
        alpha = (yy - (height - 60)) / 60.0
        r = int(color[0] * (1 - alpha) + 20 * alpha)
        g = int(color[1] * (1 - alpha) + 20 * alpha)
        b = int(color[2] * (1 - alpha) + 20 * alpha)
        draw.line([(0, yy), (width, yy)], fill=(r, g, b))

    img.save(path, 'JPEG', quality=90)


def create_placeholder_mp3(path):
    """Create a minimal valid MP3 file (~2 minutes of silence).
    Uses a simple MP3 frame header for a valid file."""
    # Minimal MP3: ID3 tag + silent MPEG frames
    # MPEG1, Layer3, 128kbps, 44100Hz, stereo
    # Frame size = 144 * bitrate / sample_rate + padding
    # = 144 * 128000 / 44100 = ~417 bytes per frame
    # For ~2 minutes: 120s * 44100/1152 frames/sec ~ 4594 frames
    # But we'll just create enough to be recognized as MP3

    frame_header = bytes([0xFF, 0xFB, 0x90, 0x00])  # MPEG1, Layer3, 128kbps, 44100Hz, stereo
    frame_data = bytes(413)  # rest of frame is silence (zeros)
    frame = frame_header + frame_data

    # ~2 minutes worth of frames (approximate)
    num_frames = 4600  # ~120 seconds
    with open(path, 'wb') as f:
        # ID3v2 header (minimal)
        f.write(b'ID3')
        f.write(bytes([3, 0, 0]))  # version 2.3, no flags
        f.write(bytes([0, 0, 0, 0]))  # size = 0
        # Write frames
        for _ in range(num_frames):
            f.write(frame)


def create_initial():
    # Create directories
    os.makedirs(SLIDESHOW_DIR, exist_ok=True)
    os.makedirs(DESKTOP_DIR, exist_ok=True)

    # Create 10 placeholder images
    for i in range(10):
        img_path = os.path.join(SLIDESHOW_DIR, f'img{i+1:02d}.jpg')
        create_placeholder_image(img_path, i)
        print(f'Created: {img_path}')

    # Create placeholder MP3
    mp3_path = os.path.join(DESKTOP_DIR, 'background_music.mp3')
    create_placeholder_mp3(mp3_path)
    print(f'Created: {mp3_path}')

    # Kill any existing LibreOffice instances for clean start
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(1)

    # Open LibreOffice Impress with a blank presentation
    launch_gui('libreoffice --impress', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Impress with blank presentation on DISPLAY=:0')


create_initial()
