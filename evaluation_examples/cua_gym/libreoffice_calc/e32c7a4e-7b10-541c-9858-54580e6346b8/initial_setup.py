"""
Initial Setup: Create coin_sprite.png (golden coin on black background) on Desktop.
Task ID: osworld_multi_apps_gimp_vscode_005
Domain: gimp + vscode
"""

import os
import shlex
import subprocess
import time

try:
    from PIL import Image, ImageDraw
    import numpy as np
except ImportError:
    subprocess.run(["pip3", "install", "Pillow", "numpy"], check=True)
    from PIL import Image, ImageDraw
    import numpy as np

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_vscode_005'
OUTPUT = f'{WORKDIR}/coin_sprite.png'


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


def create_coin_sprite():
    """Create a golden coin sprite on a pure black background."""
    width, height = 128, 128

    # Start with pure black background
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Center and radius for the coin
    cx, cy = width // 2, height // 2
    coin_radius = 48
    inner_radius = 38
    rim_radius = 44

    # Outer coin body - dark gold rim
    draw.ellipse(
        [cx - coin_radius, cy - coin_radius, cx + coin_radius, cy + coin_radius],
        fill=(184, 134, 11),
        outline=(140, 100, 5),
        width=2,
    )

    # Rim highlight
    draw.ellipse(
        [cx - rim_radius, cy - rim_radius, cx + rim_radius, cy + rim_radius],
        fill=(212, 175, 55),
        outline=(184, 134, 11),
        width=2,
    )

    # Inner coin face - bright gold
    draw.ellipse(
        [cx - inner_radius, cy - inner_radius, cx + inner_radius, cy + inner_radius],
        fill=(255, 215, 0),
        outline=(184, 134, 11),
        width=1,
    )

    # Highlight sheen on upper-left
    highlight_data = np.array(img)
    # Create a subtle radial highlight
    for py in range(height):
        for px in range(width):
            dist = ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5
            if dist <= inner_radius:
                # Add highlight in upper-left quadrant
                if px < cx and py < cy:
                    fade = 1.0 - (dist / inner_radius)
                    r, g, b = highlight_data[py, px]
                    highlight_data[py, px] = [
                        min(255, int(r + 40 * fade)),
                        min(255, int(g + 30 * fade)),
                        min(255, int(b)),
                    ]

    img = Image.fromarray(highlight_data.astype("uint8"), "RGB")
    draw = ImageDraw.Draw(img)

    # Draw a dollar sign "$" on the coin face
    # Simplified: draw two vertical lines and three horizontal curves suggestion
    # Use a polygon-based "C" shape to represent a coin letter
    # Center text-like mark: a simple "G" shape using arcs
    # Draw inner circle detail
    draw.ellipse(
        [cx - 15, cy - 15, cx + 15, cy + 15],
        fill=(255, 200, 0),
        outline=(184, 134, 11),
        width=1,
    )

    # Draw a cross/star detail to make it look like a coin face
    # Vertical bar
    draw.rectangle([cx - 3, cy - 12, cx + 3, cy + 12], fill=(184, 134, 11))
    # Horizontal bar
    draw.rectangle([cx - 12, cy - 3, cx + 12, cy + 3], fill=(184, 134, 11))

    # Small dots around inner circle
    for angle_deg in [0, 45, 90, 135, 180, 225, 270, 315]:
        angle_rad = angle_deg * 3.14159 / 180
        dx = int(22 * np.cos(angle_rad))
        dy = int(22 * np.sin(angle_rad))
        draw.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2],
                     fill=(184, 134, 11))

    # Ensure no artifacts - make all pixels truly black or coin-colored
    # Any near-black pixel outside coin radius becomes pure black
    final_data = np.array(img)
    for py in range(height):
        for px in range(width):
            dist = ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5
            if dist > coin_radius:
                final_data[py, px] = [0, 0, 0]

    img = Image.fromarray(final_data.astype("uint8"), "RGB")

    # Ensure Desktop directory exists
    os.makedirs(WORKDIR, exist_ok=True)
    img.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    return img


def create_initial():
    create_coin_sprite()

    # Open GIMP with the coin sprite
    launch_gui(f'gimp "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched GIMP with coin_sprite.png and DISPLAY=:0')


create_initial()
