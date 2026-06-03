"""
Initial Setup: Create headshot PNG files for team roster presentation task
Task ID: osworld_impress_new_presentation_images_006
Domain: libreoffice_impress

Creates three headshot PNG files in /home/user:
  - headshot_ceo.png
  - headshot_cto.png
  - headshot_cfo.png

Does NOT create team_roster.odp — that is the agent's task.
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

WORKDIR = '/home/user'
TASK_ID = 'osworld_impress_new_presentation_images_006'


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


def create_headshot(filepath: str, name: str, title: str, bg_color: tuple, text_color: tuple):
    """Create a realistic-looking headshot placeholder image."""
    width, height = 400, 500
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw a simple silhouette-style person shape as headshot placeholder
    # Background gradient-like effect with a rectangle
    draw.rectangle([0, 0, width, height], fill=bg_color)

    # Head circle
    head_cx, head_cy = width // 2, 160
    head_r = 80
    draw.ellipse(
        [head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r],
        fill=(220, 200, 185)
    )

    # Body/shoulders
    draw.ellipse([80, 320, 320, 550], fill=(200, 195, 190))
    draw.rectangle([80, 420, 320, 500], fill=(200, 195, 190))

    # Simple facial features
    # Eyes
    draw.ellipse([head_cx - 30, head_cy - 15, head_cx - 15, head_cy], fill=(60, 40, 30))
    draw.ellipse([head_cx + 15, head_cy - 15, head_cx + 30, head_cy], fill=(60, 40, 30))
    # Mouth smile
    draw.arc([head_cx - 20, head_cy + 10, head_cx + 20, head_cy + 35], 0, 180, fill=(140, 80, 60), width=3)

    # Name label at bottom
    # Use default font (PIL built-in)
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except (IOError, OSError):
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw name
    name_bbox = draw.textbbox((0, 0), name, font=font_large)
    name_w = name_bbox[2] - name_bbox[0]
    draw.text(((width - name_w) // 2, 410), name, fill=text_color, font=font_large)

    # Draw title
    title_bbox = draw.textbbox((0, 0), title, font=font_small)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, 450), title, fill=text_color, font=font_small)

    img.save(filepath, 'PNG')
    print(f'Created: {filepath}')


def create_initial():
    # Remove team_roster.odp if it exists (ensure clean initial state)
    odp_path = os.path.join(WORKDIR, 'team_roster.odp')
    if os.path.exists(odp_path):
        os.remove(odp_path)
        print(f'Removed existing: {odp_path}')

    # Also remove any pptx version
    pptx_path = os.path.join(WORKDIR, 'team_roster.pptx')
    if os.path.exists(pptx_path):
        os.remove(pptx_path)
        print(f'Removed existing: {pptx_path}')

    # Create three headshot PNG files
    headshots = [
        {
            'filename': 'headshot_ceo.png',
            'name': 'Alexandra Reid',
            'title': 'Chief Executive Officer',
            'bg_color': (45, 85, 135),
            'text_color': (255, 255, 255),
        },
        {
            'filename': 'headshot_cto.png',
            'name': 'Marcus Chen',
            'title': 'Chief Technology Officer',
            'bg_color': (35, 110, 95),
            'text_color': (255, 255, 255),
        },
        {
            'filename': 'headshot_cfo.png',
            'name': 'Priya Sharma',
            'title': 'Chief Financial Officer',
            'bg_color': (120, 60, 100),
            'text_color': (255, 255, 255),
        },
    ]

    for h in headshots:
        filepath = os.path.join(WORKDIR, h['filename'])
        create_headshot(filepath, h['name'], h['title'], h['bg_color'], h['text_color'])

    print('All headshot PNG files created successfully.')
    print(f'team_roster.odp does NOT exist — agent must create it.')

    # GUI-ready startup: Open LibreOffice Impress with a new blank presentation
    # so the agent can begin the task immediately
    launch_gui('libreoffice --impress', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Impress with DISPLAY=:0')


create_initial()
