"""
Initial Setup: Split sunset.png into three vertical columns with progressive warm filter
Task ID: osworld_multi_apps_gimp_os_029
Domain: multi_apps (GIMP + OS/terminal)
"""

import os
import shlex
import subprocess
import time
import numpy as np

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_gimp_os_029'
OUTPUT = f'{DESKTOP}/sunset.png'


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


def create_sunset_image():
    """
    Create a realistic 1200x800 sunset photograph using Pillow/numpy.
    The image features warm sunset colors: orange/red sky, horizon glow,
    silhouetted landscape at the bottom, and golden-hour lighting.
    """
    from PIL import Image
    width, height = 1200, 800

    img_array = np.zeros((height, width, 3), dtype=np.uint8)

    # Sky gradient: deep blue-purple at top → orange-red near horizon
    for y in range(height):
        t = y / height  # 0 at top, 1 at bottom

        if t < 0.5:
            # Upper sky: deep indigo/purple to warm orange
            sky_top = np.array([40, 10, 80])      # deep indigo
            horizon = np.array([255, 120, 30])     # bright orange
            blend = t / 0.5
            r = int(sky_top[0] + blend * (horizon[0] - sky_top[0]))
            g = int(sky_top[1] + blend * (horizon[1] - sky_top[1]))
            b = int(sky_top[2] + blend * (horizon[2] - sky_top[2]))
        else:
            # Lower sky: orange to warm golden/red near ground
            horizon = np.array([255, 120, 30])     # bright orange
            ground_sky = np.array([220, 80, 20])   # deep reddish-orange
            blend = (t - 0.5) / 0.5
            r = int(horizon[0] + blend * (ground_sky[0] - horizon[0]))
            g = int(horizon[1] + blend * (ground_sky[1] - horizon[1]))
            b = int(horizon[2] + blend * (ground_sky[2] - horizon[2]))

        img_array[y, :, 0] = np.clip(r, 0, 255)
        img_array[y, :, 1] = np.clip(g, 0, 255)
        img_array[y, :, 2] = np.clip(b, 0, 255)

    # Add sun glow: a large bright circular glow near the horizon
    sun_x, sun_y = 600, 440  # near horizon center
    sun_radius = 120
    for y in range(height):
        for x in range(0, width, 2):  # every other pixel for speed, fill after
            dist = np.sqrt((x - sun_x) ** 2 + (y - sun_y) ** 2)
            if dist < sun_radius:
                intensity = (1 - dist / sun_radius) ** 2
                # Bright yellow-white sun core
                img_array[y, x, 0] = np.clip(img_array[y, x, 0] + int(100 * intensity), 0, 255)
                img_array[y, x, 1] = np.clip(img_array[y, x, 1] + int(80 * intensity), 0, 255)
                img_array[y, x, 2] = np.clip(img_array[y, x, 2] + int(20 * intensity), 0, 255)

    # Fill alternating pixels (mirror from adjacent)
    img_array[:, 1::2, :] = img_array[:, ::2, :][:, :width // 2, :][:, :width // 2, :]

    # Use numpy broadcasting to fill missing columns properly
    for x in range(1, width, 2):
        if x < width:
            img_array[:, x, :] = img_array[:, x - 1, :]

    # Add silhouette landscape (hills/trees) at bottom 15%
    ground_level = int(height * 0.82)
    # Rolling hill profile using sine waves
    for x in range(width):
        hill_height = int(
            ground_level
            + 30 * np.sin(x * 0.008)
            + 20 * np.sin(x * 0.015 + 1.2)
            + 15 * np.sin(x * 0.025 + 0.7)
        )
        hill_height = max(ground_level - 20, min(ground_level + 50, hill_height))

        # Tree silhouettes: irregular spiky tops
        tree_offset = 0
        if (x % 80) < 15:
            tree_offset = -50 - (x % 80) * 2
        elif (x % 80) < 30:
            tree_offset = -60 - ((x % 80) - 15) * 2

        fill_from = hill_height + tree_offset
        fill_from = max(0, fill_from)

        # Fill with near-black silhouette
        img_array[fill_from:, x, 0] = np.clip(img_array[fill_from:, x, 0] * 0.08, 0, 30).astype(np.uint8)
        img_array[fill_from:, x, 1] = np.clip(img_array[fill_from:, x, 1] * 0.06, 0, 20).astype(np.uint8)
        img_array[fill_from:, x, 2] = np.clip(img_array[fill_from:, x, 2] * 0.05, 0, 15).astype(np.uint8)

    # Add subtle clouds: horizontal streaks of lighter color in upper sky
    cloud_y_positions = [80, 130, 170, 220]
    np.random.seed(42)  # deterministic for reproducibility
    for cy in cloud_y_positions:
        cloud_width = np.random.randint(150, 350)
        cloud_x = np.random.randint(50, width - cloud_width - 50)
        cloud_height = np.random.randint(8, 20)
        for y in range(cy, min(cy + cloud_height, height)):
            for x in range(cloud_x, cloud_x + cloud_width):
                alpha = 0.3 * (1 - abs(y - cy - cloud_height // 2) / (cloud_height // 2))
                alpha *= (1 - abs(x - cloud_x - cloud_width // 2) / (cloud_width // 2))
                img_array[y, x, 0] = np.clip(
                    int(img_array[y, x, 0] * (1 - alpha) + 255 * alpha), 0, 255)
                img_array[y, x, 1] = np.clip(
                    int(img_array[y, x, 1] * (1 - alpha) + 200 * alpha), 0, 255)
                img_array[y, x, 2] = np.clip(
                    int(img_array[y, x, 2] * (1 - alpha) + 160 * alpha), 0, 255)

    # Add horizon reflection glow: subtle warm band
    glow_center = 460
    glow_range = 60
    for y in range(max(0, glow_center - glow_range), min(height, glow_center + glow_range)):
        intensity = (1 - abs(y - glow_center) / glow_range) * 0.4
        img_array[y, :, 0] = np.clip(
            (img_array[y, :, 0] * (1 - intensity * 0.3) + 255 * intensity * 0.3).astype(int),
            0, 255)
        img_array[y, :, 1] = np.clip(
            (img_array[y, :, 1] * (1 - intensity * 0.2) + 160 * intensity * 0.2).astype(int),
            0, 255)

    img = Image.fromarray(img_array.astype(np.uint8), 'RGB')

    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    img.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'Image size: {img.size}')


def create_initial():
    create_sunset_image()

    # Verify file was created
    if not os.path.isfile(OUTPUT):
        raise RuntimeError(f'Failed to create {OUTPUT}')

    # GUI-ready startup: open terminal (the agent needs to use command line)
    # Also open file manager to show Desktop context
    launch_gui('bash -c "DISPLAY=:0 gnome-terminal -- bash"', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')


create_initial()
