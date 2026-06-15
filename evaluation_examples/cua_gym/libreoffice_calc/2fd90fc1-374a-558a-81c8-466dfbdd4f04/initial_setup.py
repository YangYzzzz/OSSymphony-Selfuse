"""
Initial Setup: Write a shell script to resize images with ImageMagick, log sizes to CSV
Task ID: osworld_multi_apps_code_batch_terminal_010
Domain: libreoffice_calc (multi-app: terminal + LibreOffice Calc)

Initial state: /home/user/media/ has 15 images of varying sizes.
ImageMagick is installed. /home/user/media/resized/ does NOT exist.
No shell script exists. No CSV file exists.
"""

import os
import shlex
import subprocess
import time
import sys
from pathlib import Path

# Ensure required packages are installed
subprocess.run([sys.executable, '-m', 'pip', 'install', 'Pillow', '-q'], check=True)

from PIL import Image

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_batch_terminal_010'
MEDIA_DIR = f'{WORKDIR}/media'
SCRIPTS_DIR = f'{WORKDIR}/scripts'


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


def ensure_imagemagick():
    """Ensure ImageMagick is installed (task context says it should be)."""
    result = subprocess.run(['which', 'convert'], capture_output=True, text=True)
    if result.returncode != 0:
        print('Installing ImageMagick...')
        subprocess.run(
            'echo "password" | sudo -S apt-get install -y imagemagick',
            shell=True,
            check=True
        )
        print('ImageMagick installed.')
    else:
        print(f'ImageMagick found at: {result.stdout.strip()}')


def create_initial():
    # Ensure ImageMagick is installed
    ensure_imagemagick()

    # Create media directory (resized dir must NOT exist)
    os.makedirs(MEDIA_DIR, exist_ok=True)

    # Create scripts directory (but no script inside yet)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # Make sure resized dir does NOT exist
    resized_dir = f'{MEDIA_DIR}/resized'
    if os.path.exists(resized_dir):
        import shutil
        shutil.rmtree(resized_dir)

    # Remove any existing CSV log
    csv_path = f'{MEDIA_DIR}/resize_log.csv'
    if os.path.exists(csv_path):
        os.remove(csv_path)

    # Remove any existing shell script
    script_path = f'{SCRIPTS_DIR}/media_processor.sh'
    if os.path.exists(script_path):
        os.remove(script_path)

    # Image filenames and their approximate dimensions (varied sizes)
    images_spec = [
        ('vacation_beach.jpg',    (3840, 2160), 'JPEG'),  # 4K landscape
        ('portrait_family.jpg',   (2448, 3264), 'JPEG'),  # portrait photo
        ('city_skyline.png',      (2560, 1440), 'PNG'),   # 2K panoramic
        ('product_photo_01.jpg',  (1920, 1080), 'JPEG'),  # full HD
        ('product_photo_02.jpg',  (1600, 1200), 'JPEG'),  # 4:3 ratio
        ('logo_design.png',       (1200, 800),  'PNG'),   # logo
        ('team_photo.jpg',        (4032, 3024), 'JPEG'),  # smartphone photo
        ('diagram_flow.png',      (2200, 1700), 'PNG'),   # diagram
        ('event_banner.jpg',      (3000, 1500), 'JPEG'),  # banner
        ('thumbnail_video.jpg',   (1280, 720),  'JPEG'),  # HD thumbnail
        ('archive_scan_01.png',   (2480, 3508), 'PNG'),   # A4 scan
        ('archive_scan_02.png',   (2480, 3508), 'PNG'),   # A4 scan
        ('screenshot_desktop.png',(1366, 768),  'PNG'),   # screenshot
        ('infographic_data.png',  (1800, 2400), 'PNG'),   # tall infographic
        ('group_workshop.jpg',    (5184, 3456), 'JPEG'),  # DSLR photo
    ]

    for filename, (width, height), fmt in images_spec:
        filepath = f'{MEDIA_DIR}/{filename}'
        if not os.path.exists(filepath):
            # Create a realistic test image with varied content
            img = Image.new('RGB', (width, height))
            # Add some pixel variation to make file sizes realistic
            pixels = img.load()
            import random
            random.seed(hash(filename))
            # Fill with random-ish colors in blocks for compression realism
            block_size = max(width, height) // 20
            for by in range(0, height, block_size):
                for bx in range(0, width, block_size):
                    r = random.randint(50, 220)
                    g = random.randint(50, 220)
                    b = random.randint(50, 220)
                    for py in range(by, min(by + block_size, height)):
                        for px in range(bx, min(bx + block_size, width)):
                            pixels[px, py] = (r, g, b)
            if fmt == 'JPEG':
                img.save(filepath, 'JPEG', quality=85)
            else:
                img.save(filepath, 'PNG')

    # Verify images created
    created = [f for f in os.listdir(MEDIA_DIR) if f.endswith(('.jpg', '.png'))]
    print(f'Created {len(created)} images in {MEDIA_DIR}')
    assert len(created) == 15, f"Expected 15 images, got {len(created)}"

    # Verify no resized directory
    assert not os.path.exists(resized_dir), f"{resized_dir} should not exist"
    # Verify no CSV
    assert not os.path.exists(csv_path), f"{csv_path} should not exist"
    # Verify no script
    assert not os.path.exists(script_path), f"{script_path} should not exist"

    print(f'Initial state ready:')
    print(f'  - {MEDIA_DIR}: {len(created)} images')
    print(f'  - {resized_dir}: does not exist')
    print(f'  - {SCRIPTS_DIR}: exists but empty')
    print(f'  - {csv_path}: does not exist')

    # GUI-ready: open a terminal so agent can write the script
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched gnome-terminal with DISPLAY=:0')


create_initial()
