"""
Reward Script: Open landscape.jpg in GIMP, apply Hue-Saturation (+40 saturation),
               export as landscape_vivid.jpg, and set it as desktop wallpaper.
Task ID: osworld_multi_apps_media_image_003
Domain: gimp + os (multi-app)
Scoring:
  Component 1: landscape_vivid.jpg file exists in /home/user/pictures/      (0.3 pts)
  Component 2: landscape_vivid.jpg has higher saturation than landscape.jpg  (0.3 pts)
  Component 3: Desktop wallpaper is set to landscape_vivid.jpg               (0.4 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_media_image_003'

ORIGINAL_IMAGE = os.path.join(WORKDIR, 'pictures', 'landscape.jpg')
VIVID_IMAGE = os.path.join(WORKDIR, 'pictures', 'landscape_vivid.jpg')
DCONF_USER_DB = os.path.join(WORKDIR, '.config', 'dconf', 'user')


def get_wallpaper_from_dconf():
    """
    Read the desktop wallpaper URI directly from the dconf binary DB.
    The dconf user DB stores settings as readable strings embedded in a binary format.
    Returns the wallpaper URI string, or None if not found.
    """
    if not os.path.isfile(DCONF_USER_DB):
        return None
    try:
        with open(DCONF_USER_DB, 'rb') as f:
            content = f.read()
        # Search for 'picture-uri' key and extract URI value
        # In the dconf binary format, the URI is stored as a readable string
        idx = content.find(b'picture-uri\x00')
        if idx == -1:
            idx = content.find(b'picture-uri')
        if idx == -1:
            return None
        # Scan forward to find the file:// URI
        search_start = idx
        uri_marker = b'file://'
        uri_idx = content.find(uri_marker, search_start)
        if uri_idx == -1 or uri_idx > search_start + 200:
            return None
        # Extract the URI until null byte or non-printable char
        end = uri_idx
        while end < len(content) and 32 <= content[end] < 127:
            end += 1
        uri = content[uri_idx:end].decode('ascii', errors='replace')
        return uri
    except Exception as e:
        print(f"WARN: Could not read dconf DB: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    vivid_exists = False

    # Gate: original image must exist to run any useful check
    if not os.path.isfile(ORIGINAL_IMAGE):
        print(f"CRITICAL: Original image not found at {ORIGINAL_IMAGE}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: landscape_vivid.jpg exists (0.3 points)
    # This FAILS on initial_env (file does not exist) and PASSES on golden_env (file created by task)
    try:
        vivid_exists = os.path.isfile(VIVID_IMAGE)
        if vivid_exists:
            print(f"PASS: Component 1 — landscape_vivid.jpg exists at {VIVID_IMAGE} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — landscape_vivid.jpg not found at {VIVID_IMAGE}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: landscape_vivid.jpg has higher saturation than landscape.jpg (0.3 points)
    # Verifies the Hue-Saturation +40 adjustment was actually applied.
    # This FAILS on initial_env (file does not exist) and PASSES on golden_env (saturation increased).
    if vivid_exists:
        try:
            from PIL import Image
            import numpy as np

            src_img = Image.open(ORIGINAL_IMAGE).convert('HSV')
            tgt_img = Image.open(VIVID_IMAGE).convert('HSV')

            # Extract S channel (index 1 in HSV)
            src_sat = float(np.mean(np.array(src_img)[:, :, 1]))
            tgt_sat = float(np.mean(np.array(tgt_img)[:, :, 1]))

            print(f"INFO: landscape.jpg avg HSV saturation: {src_sat:.4f}")
            print(f"INFO: landscape_vivid.jpg avg HSV saturation: {tgt_sat:.4f}")

            # Vivid should have notably higher saturation
            # (task asks for +40 saturation units in GIMP).
            # Threshold of 10.0 (in 0-255 scale) to account for minor compression artifacts
            # and different implementations of the saturation operation.
            sat_increase = tgt_sat - src_sat
            if sat_increase > 10.0:
                print(f"PASS: Component 2 — saturation increased by {sat_increase:.2f} (>10 threshold) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — saturation increase is {sat_increase:.2f}, expected >10 (not enough increase)")
        except Exception as e:
            print(f"ERROR: Component 2 — could not compare saturation: {e}")
    else:
        print("SKIP: Component 2 — skipped because landscape_vivid.jpg does not exist")

    # Component 3: Desktop wallpaper is set to landscape_vivid.jpg (0.4 points)
    # Verifies the system wallpaper was changed as part of the task.
    # This FAILS on initial_env (wallpaper is the default Ubuntu background) and PASSES on golden_env.
    # We read the dconf user DB directly (binary file) to avoid subprocess dependency.
    try:
        wallpaper_uri = get_wallpaper_from_dconf()
        print(f"INFO: Current wallpaper URI (from dconf): {wallpaper_uri}")

        if wallpaper_uri and 'landscape_vivid.jpg' in wallpaper_uri:
            print(f"PASS: Component 3 — wallpaper set to landscape_vivid.jpg (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 3 — wallpaper URI does not contain 'landscape_vivid.jpg': {wallpaper_uri}")
    except Exception as e:
        print(f"ERROR: Component 3 — could not check wallpaper: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
