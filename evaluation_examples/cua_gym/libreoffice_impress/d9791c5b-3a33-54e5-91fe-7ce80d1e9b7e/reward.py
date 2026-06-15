"""
Reward Script: Export slides as PNG images with transparent background
Task ID: impress_el_042
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): All 5 PNG files exist
  Component 2 (0.30): All PNGs have RGBA mode (alpha channel)
  Component 3 (0.25): All PNGs have significant transparency (>20% transparent pixels)
  Component 4 (0.20): All PNGs contain visible content (non-transparent pixels with actual shapes)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'impress_el_042'
NUM_SLIDES = 5


def find_exported_pngs():
    """
    Search for exported PNG files. They may use various naming conventions.
    Returns a list of found PNG file paths.
    """
    found = []

    # Pattern 1: exact naming from golden (impress_el_042_slide1.png ... slide5.png)
    for i in range(1, NUM_SLIDES + 1):
        path = os.path.join(WORKDIR, f'{TASK_ID}_slide{i}.png')
        if os.path.exists(path):
            found.append(path)

    if len(found) == NUM_SLIDES:
        return found

    # Pattern 2: generic slide export names (Slide1.png, slide1.png, etc.)
    found = []
    for i in range(1, NUM_SLIDES + 1):
        for pattern in [f'Slide{i}.png', f'slide{i}.png', f'Slide {i}.png',
                        f'slide_{i}.png', f'Slide_{i}.png']:
            path = os.path.join(WORKDIR, pattern)
            if os.path.exists(path):
                found.append(path)
                break

    if len(found) == NUM_SLIDES:
        return found

    # Pattern 3: look for any PNG files in /home/user that could be slide exports
    # (exclude known non-slide PNGs)
    found = []
    all_pngs = sorted([f for f in os.listdir(WORKDIR)
                        if f.lower().endswith('.png') and os.path.isfile(os.path.join(WORKDIR, f))])
    if len(all_pngs) >= NUM_SLIDES:
        # Take the first NUM_SLIDES PNGs (sorted alphabetically)
        found = [os.path.join(WORKDIR, f) for f in all_pngs[:NUM_SLIDES]]

    # Pattern 4: check common export subdirectories
    if len(found) < NUM_SLIDES:
        for subdir in ['export', 'slides', 'png', 'output', 'images']:
            dirpath = os.path.join(WORKDIR, subdir)
            if os.path.isdir(dirpath):
                pngs = sorted([f for f in os.listdir(dirpath)
                                if f.lower().endswith('.png')])
                if len(pngs) >= NUM_SLIDES:
                    found = [os.path.join(dirpath, f) for f in pngs[:NUM_SLIDES]]
                    break

    return found


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find PNG files
    png_files = find_exported_pngs()
    found_count = len(png_files)

    # Component 1: All 5 PNG files exist (0.25 points)
    try:
        if found_count == NUM_SLIDES:
            total_score += 0.25
            print(f"PASS: Component 1 — All {NUM_SLIDES} PNG files found (0.25 pts)")
            for p in png_files:
                print(f"  Found: {p}")
        elif found_count > 0:
            partial = round(0.25 * found_count / NUM_SLIDES, 3)
            total_score += partial
            print(f"PARTIAL: Component 1 — {found_count}/{NUM_SLIDES} PNG files found ({partial} pts)")
            for p in png_files:
                print(f"  Found: {p}")
        else:
            print(f"FAIL: Component 1 — No PNG files found in {WORKDIR}")
            # No files = no further checks possible
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Need PIL for remaining checks
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: PIL/Pillow not available, cannot verify image properties")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: All PNGs have RGBA mode — alpha channel present (0.30 points)
    try:
        rgba_count = 0
        for path in png_files:
            img = Image.open(path)
            if img.mode == 'RGBA':
                rgba_count += 1
                print(f"  {os.path.basename(path)}: RGBA mode confirmed")
            else:
                print(f"  {os.path.basename(path)}: mode={img.mode} (NOT RGBA)")
            img.close()

        if rgba_count == found_count and found_count > 0:
            print(f"PASS: Component 2 — All {rgba_count} PNGs have RGBA mode (0.30 pts)")
            total_score += 0.30
        elif rgba_count > 0:
            partial = round(0.30 * rgba_count / found_count, 3)
            print(f"PARTIAL: Component 2 — {rgba_count}/{found_count} PNGs have RGBA ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No PNGs have RGBA mode (no alpha channel)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PNGs have significant transparency — >20% transparent pixels (0.25 points)
    # This verifies background was actually removed, not just mode set to RGBA
    try:
        transparent_count = 0
        for path in png_files:
            img = Image.open(path)
            if img.mode != 'RGBA':
                print(f"  {os.path.basename(path)}: skipped (not RGBA)")
                continue
            alpha = img.split()[-1]
            total_pixels = img.size[0] * img.size[1]
            fully_transparent = sum(1 for a in alpha.getdata() if a == 0)
            pct = 100.0 * fully_transparent / total_pixels
            if pct > 20.0:
                transparent_count += 1
                print(f"  {os.path.basename(path)}: {pct:.1f}% transparent pixels — significant transparency")
            else:
                print(f"  {os.path.basename(path)}: {pct:.1f}% transparent pixels — insufficient transparency")
            img.close()

        if transparent_count == found_count and found_count > 0:
            print(f"PASS: Component 3 — All {transparent_count} PNGs have >20% transparency (0.25 pts)")
            total_score += 0.25
        elif transparent_count > 0:
            partial = round(0.25 * transparent_count / found_count, 3)
            print(f"PARTIAL: Component 3 — {transparent_count}/{found_count} PNGs have significant transparency ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No PNGs have significant transparency (background not removed)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: PNGs contain visible content — non-transparent pixels exist (0.20 points)
    # This verifies shapes/text were preserved, not just blank transparent images
    try:
        content_count = 0
        for path in png_files:
            img = Image.open(path)
            if img.mode != 'RGBA':
                # For non-RGBA, any pixel is "visible"
                content_count += 1
                continue
            alpha = img.split()[-1]
            total_pixels = img.size[0] * img.size[1]
            visible = sum(1 for a in alpha.getdata() if a > 0)
            visible_pct = 100.0 * visible / total_pixels
            # Need at least 1% visible content (shapes/text)
            if visible_pct > 1.0:
                content_count += 1
                print(f"  {os.path.basename(path)}: {visible_pct:.1f}% visible content — shapes/text preserved")
            else:
                print(f"  {os.path.basename(path)}: {visible_pct:.1f}% visible — too little content")
            img.close()

        if content_count == found_count and found_count > 0:
            print(f"PASS: Component 4 — All {content_count} PNGs contain visible content (0.20 pts)")
            total_score += 0.20
        elif content_count > 0:
            partial = round(0.20 * content_count / found_count, 3)
            print(f"PARTIAL: Component 4 — {content_count}/{found_count} PNGs have visible content ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — PNGs appear to be fully transparent (no content preserved)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
