"""
Initial Setup: Company Picnic photo folder for HR Director identification task
Task ID: osworld_multi_apps_photo_zip_054
Domain: os (file management with photos)

Creates:
  - /home/user/Desktop/Company Picnic/ with 12 JPG photos
  - Each photo shows labeled attendees; 4 photos include Janet Brooks (HR Director)
  - Labeled photos: picnic_01 through picnic_12
  - Photos with Janet Brooks: picnic_02, picnic_05, picnic_08, picnic_11
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
PICNIC_DIR = f'{DESKTOP}/Company Picnic'

# Photos that contain Janet Brooks
JANET_PHOTOS = ['picnic_02.jpg', 'picnic_05.jpg', 'picnic_08.jpg', 'picnic_11.jpg']

# All 12 photos with their attendees
PHOTO_DATA = [
    ('picnic_01.jpg', ['Tom Nguyen', 'Lisa Park', 'David Kim'],
     (210, 240, 180), 'Outdoor BBQ Area'),
    ('picnic_02.jpg', ['Janet Brooks', 'Sarah Chen', 'Mike Torres'],
     (180, 220, 255), 'Main Picnic Tables'),
    ('picnic_03.jpg', ['James Wilson', 'Rachel Green', 'Olivia Brown'],
     (255, 230, 180), 'Volleyball Court'),
    ('picnic_04.jpg', ['Kevin Lee', 'Emma Davis', 'Chris Martinez'],
     (200, 255, 200), 'Food Stations'),
    ('picnic_05.jpg', ['Janet Brooks', 'Henry Adams', 'Nina Patel'],
     (255, 200, 200), 'Game Area'),
    ('picnic_06.jpg', ['Bob Johnson', 'Amy White', 'Carlos Reyes'],
     (230, 210, 255), 'Lawn Games'),
    ('picnic_07.jpg', ['Stephanie Clark', 'Daniel Miller', 'Grace Hall'],
     (255, 240, 200), 'Seating Canopy'),
    ('picnic_08.jpg', ['Janet Brooks', 'Frank Lewis', 'Mia Robinson'],
     (190, 240, 230), 'Awards Ceremony'),
    ('picnic_09.jpg', ['Tyler Scott', 'Lauren Turner', 'Sean Walker'],
     (240, 215, 190), 'Team Relay Race'),
    ('picnic_10.jpg', ['Patricia Young', 'Joshua Allen', 'Christine Hill'],
     (215, 235, 255), 'Dessert Table'),
    ('picnic_11.jpg', ['Janet Brooks', 'Marcus Johnson', 'Diana Wright'],
     (250, 230, 210), 'Group Photo Spot'),
    ('picnic_12.jpg', ['Robert King', 'Amber Baker', 'Anthony Carter'],
     (200, 225, 200), 'Closing Bonfire'),
]


def make_photo(path: str, attendees: list, bg_color: tuple, location: str):
    """Create a realistic-looking company picnic photo as a JPG."""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Sky gradient (top portion)
    sky_r, sky_g, sky_b = min(bg_color[0] + 40, 255), min(bg_color[1] + 30, 255), min(bg_color[2] + 50, 255)
    for y in range(200):
        ratio = y / 200
        r = int(sky_r * (1 - ratio) + bg_color[0] * ratio)
        g = int(sky_g * (1 - ratio) + bg_color[1] * ratio)
        b = int(sky_b * (1 - ratio) + bg_color[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Ground area (bottom portion)
    ground_color = (100, 160, 80)
    for y in range(400, height):
        ratio = (y - 400) / 200
        r = int(bg_color[0] * (1 - ratio) + ground_color[0] * ratio)
        g = int(bg_color[1] * (1 - ratio) + ground_color[1] * ratio)
        b = int(bg_color[2] * (1 - ratio) + ground_color[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Draw simple tree shapes
    tree_positions = [50, 150, 650, 750]
    for tx in tree_positions:
        # Trunk
        draw.rectangle([tx - 8, 300, tx + 8, 420], fill=(120, 80, 40))
        # Canopy
        draw.ellipse([tx - 55, 200, tx + 55, 320], fill=(60, 140, 60))
        draw.ellipse([tx - 40, 185, tx + 40, 305], fill=(70, 160, 70))

    # Draw simple people silhouettes
    person_positions = [250, 380, 520]
    for i, px in enumerate(person_positions):
        py = 360
        color = (80, 80, 200) if i % 2 == 0 else (200, 80, 80)
        # Body
        draw.ellipse([px - 18, py - 80, px + 18, py - 44], fill=(220, 180, 140))  # head
        draw.rectangle([px - 16, py - 44, px + 16, py + 20], fill=color)  # torso
        # Legs
        draw.rectangle([px - 14, py + 20, px - 4, py + 70], fill=(100, 100, 100))
        draw.rectangle([px + 4, py + 20, px + 14, py + 70], fill=(100, 100, 100))

    # Draw location label box
    draw.rectangle([20, 20, 400, 65], fill=(0, 0, 0, 180))
    try:
        font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
        font_medium = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    except (IOError, OSError):
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((30, 25), f'Company Picnic 2025 — {location}', fill='white', font=font_large)

    # Draw attendee name tags at the bottom
    tag_y = height - 120
    draw.rectangle([0, tag_y - 5, width, height], fill=(0, 0, 0, 160))
    draw.text((20, tag_y), 'Attendees in this photo:', fill=(255, 220, 100), font=font_medium)

    for idx, name in enumerate(attendees):
        col = idx % 3
        row = idx // 3
        x = 20 + col * 260
        y = tag_y + 25 + row * 22
        # Highlight Janet Brooks in a special color
        color = (255, 255, 100) if name == 'Janet Brooks' else (200, 230, 255)
        draw.text((x, y), f'• {name}', fill=color, font=font_small)

    # Add HR Director badge if Janet Brooks is in the photo
    if 'Janet Brooks' in attendees:
        badge_x, badge_y = width - 210, 20
        draw.rectangle([badge_x, badge_y, badge_x + 190, badge_y + 50],
                       fill=(180, 30, 30), outline=(255, 200, 0), width=2)
        draw.text((badge_x + 10, badge_y + 6), 'HR Director Present', fill='white', font=font_medium)
        draw.text((badge_x + 30, badge_y + 28), 'Janet Brooks', fill=(255, 255, 100), font=font_medium)

    img.save(path, 'JPEG', quality=88)


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Create the Company Picnic directory on Desktop
    os.makedirs(PICNIC_DIR, exist_ok=True)

    # Generate all 12 photos
    for filename, attendees, bg_color, location in PHOTO_DATA:
        photo_path = os.path.join(PICNIC_DIR, filename)
        make_photo(photo_path, attendees, bg_color, location)
        print(f'Created: {photo_path}')

    print(f'\nInitial state created: {PICNIC_DIR}')
    print(f'Total photos: {len(PHOTO_DATA)}')
    print(f'Photos with Janet Brooks: {JANET_PHOTOS}')

    # Verify the janet_brooks folder and zip do NOT exist in initial state
    janet_dir = os.path.join(DESKTOP, 'janet_brooks')
    janet_zip = os.path.join(DESKTOP, 'janet_brooks.zip')
    if os.path.exists(janet_dir):
        import shutil
        shutil.rmtree(janet_dir)
        print('Removed pre-existing janet_brooks folder to ensure clean initial state')
    if os.path.exists(janet_zip):
        os.remove(janet_zip)
        print('Removed pre-existing janet_brooks.zip to ensure clean initial state')

    # GUI-ready startup: open Nautilus file manager showing the Desktop
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager showing Desktop with DISPLAY=:0')


create_initial()
