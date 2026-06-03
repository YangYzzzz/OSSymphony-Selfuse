"""
Initial Setup: Create portfolio images and open blank LibreOffice Impress
Task ID: impress_wf_006
Domain: libreoffice_impress
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'impress_wf_006'
PORTFOLIO_DIR = f'{WORKDIR}/Portfolio'


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


def create_portfolio_images():
    """Create 4 sample project images (400x300) in ~/Portfolio/."""
    from PIL import Image, ImageDraw, ImageFont

    os.makedirs(PORTFOLIO_DIR, exist_ok=True)

    # Color schemes for each project image to look realistic
    projects = [
        {
            'name': 'project1.jpg',
            'bg_color': (41, 128, 185),    # blue
            'accent': (236, 240, 241),
            'label': 'Web Redesign',
        },
        {
            'name': 'project2.jpg',
            'bg_color': (39, 174, 96),     # green
            'accent': (241, 196, 15),
            'label': 'Mobile App',
        },
        {
            'name': 'project3.jpg',
            'bg_color': (142, 68, 173),    # purple
            'accent': (236, 240, 241),
            'label': 'Brand Identity',
        },
        {
            'name': 'project4.jpg',
            'bg_color': (231, 76, 60),     # red
            'accent': (241, 196, 15),
            'label': 'Dashboard UI',
        },
    ]

    for proj in projects:
        img = Image.new('RGB', (400, 300), proj['bg_color'])
        draw = ImageDraw.Draw(img)

        # Draw some decorative rectangles to make it look like a project screenshot
        draw.rectangle([20, 20, 380, 60], fill=proj['accent'])
        draw.rectangle([20, 80, 185, 280], fill=tuple(max(0, c - 30) for c in proj['bg_color']))
        draw.rectangle([200, 80, 380, 170], fill=tuple(max(0, c - 30) for c in proj['bg_color']))
        draw.rectangle([200, 185, 380, 280], fill=proj['accent'])

        # Add project label text
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        except (OSError, IOError):
            font = ImageFont.load_default()
        draw.text((30, 30), proj['label'], fill=(50, 50, 50), font=font)

        filepath = os.path.join(PORTFOLIO_DIR, proj['name'])
        img.save(filepath, 'JPEG', quality=90)
        print(f"Created: {filepath}")


def create_initial():
    create_portfolio_images()

    # Ensure Desktop directory exists
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    print(f"Portfolio images created in {PORTFOLIO_DIR}")
    print("Files: project1.jpg, project2.jpg, project3.jpg, project4.jpg (400x300)")

    # Open LibreOffice Impress with a blank presentation
    launch_gui('libreoffice --impress', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Impress with DISPLAY=:0')


create_initial()
