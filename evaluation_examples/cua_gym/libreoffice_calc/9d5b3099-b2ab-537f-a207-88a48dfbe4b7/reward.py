"""
Reward Script: Sort images into subfolders by aspect ratio using ImageMagick and shell script
Task ID: osworld_multi_apps_media_image_007
Domain: os / multi-app (ImageMagick, GIMP, shell scripting)

Scoring Rubric:
  Component 1: Shell script (sort_images.sh) exists at /home/user/ and is executable — 0.20 pts
  Component 2: Target directories (wide/, tall/, square/) exist inside /home/user/pictures/ — 0.20 pts
  Component 3: Exactly 5 wide images in /home/user/pictures/wide/ (with correct files) — 0.20 pts
  Component 4: Exactly 4 tall images in /home/user/pictures/tall/ (with correct files) — 0.20 pts
  Component 5: Exactly 3 square images in /home/user/pictures/square/ (with correct files) — 0.20 pts
Total: 1.0

Ground truth (from task context):
  - 12 images total: 5 wide, 4 tall, 3 square
  - wide: banner_sunset.png, desktop_wallpaper.png, landscape_meadow.png, panorama_cityview.png, wide_ocean_scene.png
  - tall: infographic_chart.png, phone_screenshot.png, portrait_person.png, tall_building.png
  - square: album_cover.png, instagram_post.png, profile_avatar.png
"""

import os
import stat

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_media_image_007'

# Ground truth: expected files in each category
EXPECTED_WIDE = {
    'banner_sunset.png',
    'desktop_wallpaper.png',
    'landscape_meadow.png',
    'panorama_cityview.png',
    'wide_ocean_scene.png',
}

EXPECTED_TALL = {
    'infographic_chart.png',
    'phone_screenshot.png',
    'portrait_person.png',
    'tall_building.png',
}

EXPECTED_SQUARE = {
    'album_cover.png',
    'instagram_post.png',
    'profile_avatar.png',
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Shell script exists at /home/user/sort_images.sh and is executable (0.20 points)
    # This FAILS on initial (no script) → PASSES on golden (script created and executable)
    try:
        script_path = os.path.join(WORKDIR, 'sort_images.sh')
        if os.path.isfile(script_path):
            file_stat = os.stat(script_path)
            is_executable = bool(file_stat.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
            if is_executable:
                print(f"PASS: Component 1 — sort_images.sh exists and is executable (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — sort_images.sh exists but is NOT executable (mode: {oct(stat.S_IMODE(file_stat.st_mode))})")
        else:
            print(f"FAIL: Component 1 — sort_images.sh NOT found at {script_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — could not check sort_images.sh: {e}")

    # Component 2: Target directories wide/, tall/, square/ all exist (0.20 points)
    # This FAILS on initial (directories don't exist) → PASSES on golden (directories created)
    try:
        wide_dir = os.path.join(WORKDIR, 'pictures', 'wide')
        tall_dir = os.path.join(WORKDIR, 'pictures', 'tall')
        square_dir = os.path.join(WORKDIR, 'pictures', 'square')

        wide_exists = os.path.isdir(wide_dir)
        tall_exists = os.path.isdir(tall_dir)
        square_exists = os.path.isdir(square_dir)

        if wide_exists and tall_exists and square_exists:
            print(f"PASS: Component 2 — all 3 target directories exist (wide/, tall/, square/) (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not wide_exists:
                missing.append('wide/')
            if not tall_exists:
                missing.append('tall/')
            if not square_exists:
                missing.append('square/')
            print(f"FAIL: Component 2 — missing directories: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — could not check target directories: {e}")

    # Component 3: Exactly 5 wide images correctly sorted into /home/user/pictures/wide/ (0.20 points)
    # This FAILS on initial (directory doesn't exist) → PASSES on golden (5 images sorted)
    try:
        wide_dir = os.path.join(WORKDIR, 'pictures', 'wide')
        if os.path.isdir(wide_dir):
            actual_wide = set(f for f in os.listdir(wide_dir) if os.path.isfile(os.path.join(wide_dir, f)))
            if actual_wide == EXPECTED_WIDE:
                print(f"PASS: Component 3 — wide/ contains exactly 5 correct images: {sorted(actual_wide)} (0.20 pts)")
                total_score += 0.20
            else:
                missing = EXPECTED_WIDE - actual_wide
                extra = actual_wide - EXPECTED_WIDE
                print(f"FAIL: Component 3 — wide/ mismatch. Missing: {missing}, Extra: {extra}, Found: {actual_wide}")
        else:
            print(f"FAIL: Component 3 — wide/ directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — could not check wide/ images: {e}")

    # Component 4: Exactly 4 tall images correctly sorted into /home/user/pictures/tall/ (0.20 points)
    # This FAILS on initial (directory doesn't exist) → PASSES on golden (4 images sorted)
    try:
        tall_dir = os.path.join(WORKDIR, 'pictures', 'tall')
        if os.path.isdir(tall_dir):
            actual_tall = set(f for f in os.listdir(tall_dir) if os.path.isfile(os.path.join(tall_dir, f)))
            if actual_tall == EXPECTED_TALL:
                print(f"PASS: Component 4 — tall/ contains exactly 4 correct images: {sorted(actual_tall)} (0.20 pts)")
                total_score += 0.20
            else:
                missing = EXPECTED_TALL - actual_tall
                extra = actual_tall - EXPECTED_TALL
                print(f"FAIL: Component 4 — tall/ mismatch. Missing: {missing}, Extra: {extra}, Found: {actual_tall}")
        else:
            print(f"FAIL: Component 4 — tall/ directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 — could not check tall/ images: {e}")

    # Component 5: Exactly 3 square images correctly sorted into /home/user/pictures/square/ (0.20 points)
    # This FAILS on initial (directory doesn't exist) → PASSES on golden (3 images sorted)
    try:
        square_dir = os.path.join(WORKDIR, 'pictures', 'square')
        if os.path.isdir(square_dir):
            actual_square = set(f for f in os.listdir(square_dir) if os.path.isfile(os.path.join(square_dir, f)))
            if actual_square == EXPECTED_SQUARE:
                print(f"PASS: Component 5 — square/ contains exactly 3 correct images: {sorted(actual_square)} (0.20 pts)")
                total_score += 0.20
            else:
                missing = EXPECTED_SQUARE - actual_square
                extra = actual_square - EXPECTED_SQUARE
                print(f"FAIL: Component 5 — square/ mismatch. Missing: {missing}, Extra: {extra}, Found: {actual_square}")
        else:
            print(f"FAIL: Component 5 — square/ directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 5 — could not check square/ images: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Run verification
verify_task()
