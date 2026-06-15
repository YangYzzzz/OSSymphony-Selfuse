"""
Initial Setup: Design Portfolio Presentation with Image Galleries
Task ID: impress_wf_024
Domain: libreoffice_impress

Creates Desktop folders with placeholder images and opens LibreOffice Impress.
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'

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

def create_placeholder_image(path, width, height, color, label=""):
    """Create a placeholder image with a colored background and optional label."""
    img = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(img)
    # Add a subtle grid pattern
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=(200, 200, 200), width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(200, 200, 200), width=1)
    # Draw label text in center
    if label:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), label, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((width - tw) // 2, (height - th) // 2), label, fill=(80, 80, 80), font=font)
    img.save(path, "JPEG", quality=85)

def create_initial():
    # Create directory structure on Desktop
    folders = {
        'WebDesign': [
            ('screenshot_homepage.jpg', (800, 600), (245, 248, 252), 'Homepage Design'),
            ('screenshot_about.jpg', (800, 600), (240, 245, 250), 'About Page'),
            ('screenshot_portfolio.jpg', (800, 600), (235, 240, 248), 'Portfolio Page'),
            ('screenshot_blog.jpg', (800, 600), (248, 242, 238), 'Blog Layout'),
            ('screenshot_contact.jpg', (800, 600), (238, 245, 240), 'Contact Form'),
            ('screenshot_dashboard.jpg', (800, 600), (242, 238, 248), 'Dashboard UI'),
        ],
        'Branding': [
            ('logo_techstart.jpg', (600, 600), (52, 73, 94), 'TechStart Logo'),
            ('logo_greenleaf.jpg', (600, 600), (39, 174, 96), 'GreenLeaf Logo'),
            ('logo_skyline.jpg', (600, 600), (41, 128, 185), 'Skyline Logo'),
            ('brand_colors_techstart.jpg', (800, 400), (236, 240, 241), 'TechStart Palette'),
            ('brand_colors_greenleaf.jpg', (800, 400), (232, 245, 233), 'GreenLeaf Palette'),
            ('brand_colors_skyline.jpg', (800, 400), (227, 242, 253), 'Skyline Palette'),
        ],
        'Illustrations': [
            ('illus_cityscape.jpg', (600, 600), (255, 183, 77), 'Cityscape'),
            ('illus_forest.jpg', (600, 600), (129, 199, 132), 'Forest Scene'),
            ('illus_ocean.jpg', (600, 600), (100, 181, 246), 'Ocean Waves'),
            ('illus_mountain.jpg', (600, 600), (161, 136, 127), 'Mountain Peak'),
            ('illus_abstract1.jpg', (600, 600), (206, 147, 216), 'Abstract Flow'),
            ('illus_abstract2.jpg', (600, 600), (255, 138, 128), 'Abstract Shapes'),
            ('illus_portrait1.jpg', (600, 600), (255, 204, 128), 'Portrait Study'),
            ('illus_portrait2.jpg', (600, 600), (128, 203, 196), 'Character Design'),
            ('illus_botanical1.jpg', (600, 600), (165, 214, 167), 'Botanical Art'),
            ('illus_botanical2.jpg', (600, 600), (144, 202, 249), 'Floral Pattern'),
            ('illus_geometric1.jpg', (600, 600), (239, 154, 154), 'Geometric Study'),
            ('illus_geometric2.jpg', (600, 600), (179, 157, 219), 'Pattern Design'),
        ],
    }

    for folder_name, files in folders.items():
        folder_path = os.path.join(DESKTOP, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        for fname, size, color, label in files:
            fpath = os.path.join(folder_path, fname)
            create_placeholder_image(fpath, size[0], size[1], color, label)
            print(f'  Created: {fpath}')

    # Create headshot.jpg on Desktop
    headshot_path = os.path.join(DESKTOP, 'headshot.jpg')
    img = Image.new('RGB', (500, 500), (220, 210, 200))
    draw = ImageDraw.Draw(img)
    # Draw a simple face-like shape for headshot placeholder
    draw.ellipse([100, 50, 400, 350], fill=(240, 220, 200))  # face
    draw.ellipse([175, 150, 225, 200], fill=(100, 80, 60))   # left eye
    draw.ellipse([275, 150, 325, 200], fill=(100, 80, 60))   # right eye
    draw.arc([175, 200, 325, 300], 0, 180, fill=(150, 100, 80), width=3)  # smile
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font = ImageFont.load_default()
    draw.text((160, 400), "Jane Smith", fill=(80, 80, 80), font=font)
    img.save(headshot_path, "JPEG", quality=90)
    print(f'  Created: {headshot_path}')

    print('Initial file structure created on Desktop.')

    # Open LibreOffice Impress with a new blank presentation
    launch_gui('libreoffice --impress', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Impress with DISPLAY=:0')

create_initial()
