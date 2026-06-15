"""
Initial Setup: Create product_photo.png (headphones on white studio background) on Desktop
Task ID: osworld_multi_apps_gimp_vscode_011
Domain: gimp + vscode
"""

import os
import shlex
import subprocess
import time
from PIL import Image, ImageDraw, ImageFilter

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_011'
OUTPUT = f'{WORKDIR}/product_photo.png'


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


def create_headphones_image():
    """Create a realistic-looking headphones image on a white background."""
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Center of the image
    cx, cy = width // 2, height // 2

    # === Headphone Arc (headband) ===
    # Draw headband as a thick arc at the top
    headband_color = (30, 30, 35)        # near-black
    headband_highlight = (70, 70, 80)    # lighter part
    cushion_color = (40, 40, 50)
    ear_cup_outer = (25, 25, 30)
    ear_cup_inner = (50, 50, 60)
    speaker_mesh = (15, 15, 20)
    metal_silver = (160, 165, 175)
    padding_color = (55, 50, 65)

    # Headband arc (half-circle at top)
    band_left = cx - 170
    band_right = cx + 170
    band_top = cy - 200
    band_bottom = cy - 30

    # Draw thick headband
    for thickness in range(22, 0, -1):
        t_color = headband_color if thickness > 10 else headband_highlight
        draw.arc(
            [band_left + thickness, band_top + thickness,
             band_right - thickness, band_bottom - thickness],
            start=180, end=360,
            fill=t_color, width=3
        )

    # Headband padding (underside cushion)
    pad_left = cx - 75
    pad_right = cx + 75
    pad_top = cy - 95
    pad_bottom = cy - 65
    draw.ellipse([pad_left, pad_top, pad_right, pad_bottom], fill=padding_color)
    # Padding stitching detail
    draw.ellipse([pad_left + 5, pad_top + 4, pad_right - 5, pad_bottom - 4],
                 outline=(80, 70, 90), width=2)

    # === Left Ear Cup ===
    lec_cx = cx - 170
    lec_cy = cy + 30

    # Outer shell
    draw.ellipse([lec_cx - 58, lec_cy - 80, lec_cx + 58, lec_cy + 80],
                 fill=ear_cup_outer)
    # Inner ring
    draw.ellipse([lec_cx - 48, lec_cy - 68, lec_cx + 48, lec_cy + 68],
                 fill=ear_cup_inner)
    # Speaker mesh area
    draw.ellipse([lec_cx - 34, lec_cy - 50, lec_cx + 34, lec_cy + 50],
                 fill=speaker_mesh)
    # Speaker mesh grid (vertical lines)
    for dx in range(-28, 32, 8):
        x = lec_cx + dx
        draw.line([(x, lec_cy - 46), (x, lec_cy + 46)], fill=(35, 35, 45), width=1)
    # Speaker mesh grid (horizontal lines)
    for dy in range(-44, 48, 8):
        y = lec_cy + dy
        draw.line([(lec_cx - 30, y), (lec_cx + 30, y)], fill=(35, 35, 45), width=1)
    # Center speaker dome
    draw.ellipse([lec_cx - 14, lec_cy - 18, lec_cx + 14, lec_cy + 18],
                 fill=(60, 60, 75))
    draw.ellipse([lec_cx - 7, lec_cy - 9, lec_cx + 7, lec_cy + 9],
                 fill=(80, 80, 95))
    # Ear cushion ring
    draw.ellipse([lec_cx - 55, lec_cy - 77, lec_cx + 55, lec_cy + 77],
                 outline=cushion_color, width=7)
    # Slider arm left
    draw.rectangle([lec_cx - 6, lec_cy - 135, lec_cx + 6, lec_cy - 75],
                   fill=metal_silver)
    draw.rectangle([lec_cx - 4, lec_cy - 133, lec_cx + 4, lec_cy - 77],
                   fill=(190, 195, 205))
    # Brand logo left
    draw.ellipse([lec_cx - 8, lec_cy + 52, lec_cx + 8, lec_cy + 68],
                 fill=(100, 100, 115))

    # === Right Ear Cup ===
    rec_cx = cx + 170
    rec_cy = cy + 30

    # Outer shell
    draw.ellipse([rec_cx - 58, rec_cy - 80, rec_cx + 58, rec_cy + 80],
                 fill=ear_cup_outer)
    # Inner ring
    draw.ellipse([rec_cx - 48, rec_cy - 68, rec_cx + 48, rec_cy + 68],
                 fill=ear_cup_inner)
    # Speaker mesh area
    draw.ellipse([rec_cx - 34, rec_cy - 50, rec_cx + 34, rec_cy + 50],
                 fill=speaker_mesh)
    # Speaker mesh grid (vertical lines)
    for dx in range(-28, 32, 8):
        x = rec_cx + dx
        draw.line([(x, rec_cy - 46), (x, rec_cy + 46)], fill=(35, 35, 45), width=1)
    # Speaker mesh grid (horizontal lines)
    for dy in range(-44, 48, 8):
        y = rec_cy + dy
        draw.line([(rec_cx - 30, y), (rec_cx + 30, y)], fill=(35, 35, 45), width=1)
    # Center speaker dome
    draw.ellipse([rec_cx - 14, rec_cy - 18, rec_cx + 14, rec_cy + 18],
                 fill=(60, 60, 75))
    draw.ellipse([rec_cx - 7, rec_cy - 9, rec_cx + 7, rec_cy + 9],
                 fill=(80, 80, 95))
    # Ear cushion ring
    draw.ellipse([rec_cx - 55, rec_cy - 77, rec_cx + 55, rec_cy + 77],
                 outline=cushion_color, width=7)
    # Slider arm right
    draw.rectangle([rec_cx - 6, rec_cy - 135, rec_cx + 6, rec_cy - 75],
                   fill=metal_silver)
    draw.rectangle([rec_cx - 4, rec_cy - 133, rec_cx + 4, rec_cy - 77],
                   fill=(190, 195, 205))
    # Brand logo right
    draw.ellipse([rec_cx - 8, rec_cy + 52, rec_cx + 8, rec_cy + 68],
                 fill=(100, 100, 115))

    # === Cable (left side) ===
    cable_color = (20, 20, 25)
    # Bezier-like cable from left ear cup going down
    cable_points = []
    for t in range(0, 101, 2):
        t_norm = t / 100.0
        # Quadratic bezier: start at ear cup, end at bottom
        x = int((1 - t_norm)**2 * (lec_cx - 5) + 2*(1 - t_norm)*t_norm * (lec_cx - 50) + t_norm**2 * (lec_cx - 30))
        y = int((1 - t_norm)**2 * (lec_cy + 85) + 2*(1 - t_norm)*t_norm * (cy + 200) + t_norm**2 * (cy + 250))
        cable_points.append((x, y))
    for i in range(len(cable_points) - 1):
        draw.line([cable_points[i], cable_points[i+1]], fill=cable_color, width=3)

    # === Product label/brand text area ===
    # Subtle text on headband
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        draw.text((cx - 22, cy - 88), "SOUND", fill=(100, 95, 115), font=font)
    except Exception:
        pass

    # Apply very slight blur to smooth out jagged lines
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

    os.makedirs(WORKDIR, exist_ok=True)
    img.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'Image size: {img.size}')


def main():
    create_headphones_image()

    # GUI-ready startup: open GIMP with the product photo
    launch_gui(f'gimp "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched GIMP with product_photo.png using DISPLAY=:0')


main()
