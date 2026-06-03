"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Impress, what’s the quickest way to export my entire deck so that each slide becomes its own PNG file? And while we’re at it, I also need slide 1 saved separately as exactly “~/Desktop/res.png”.
Generated: 2025-09-10 13:01:24
Status: success
Model: azure-o3
Total Steps: 19
"""

import os
import re
import hashlib
from collections import defaultdict
from pptx import Presentation
from PIL import Image

# -----------------------------------------------------------------------------
# Reward script for the task:
#  In LibreOffice Impress, export every slide as its own PNG and save slide 1 as
#  exactly "~/Desktop/res.png".
# -----------------------------------------------------------------------------
# The script awards up to 1.0 points:
#   • 0 – 0.6  : proportion of deck successfully exported to separate PNG files
#   • 0.2      : res.png exists on the Desktop with reasonable dimensions
#   • 0.2      : res.png’s content matches one of the exported slide PNGs
# -----------------------------------------------------------------------------
# Scoring is progressive and based ONLY on verifiable evidence – no natural
# conditions are rewarded.  A score of exactly 1.0 means the task is completed
# perfectly.
# -----------------------------------------------------------------------------

# ------------------------------ Configuration --------------------------------
DECK_PATH = (
    "/home/user/"
    "in_libreoffice_impress_whats_the_quickest_way_to_export_my_entire_deck_"
    "so_that_each_slide_becomes_it_golden.pptx"
)
RES_PATH = os.path.expanduser("~/Desktop/res.png")
VISIBLE_ROOT = "/home/user"  # top-level directory to search for exported PNGs

# ------------------------------ Helper Utils ---------------------------------

def _is_hidden(path: str) -> bool:
    """Return True if any component of *path* is hidden (starts with '.')"""
    parts = path.split(os.sep)
    return any(part.startswith(".") and part not in ("", ".") for part in parts)


def _get_png_dim(path: str):
    """Return (width, height) for a PNG or None if unreadable."""
    try:
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def _aspect_ratio(dim):
    if not dim or dim[1] == 0:
        return None
    return dim[0] / dim[1]


def _sha1_first_mb(path: str, size: int = 1024 * 1024) -> str:
    """SHA-1 of first *size* bytes (defaults to 1 MB) – fast similarity check."""
    h = hashlib.sha1()
    with open(path, "rb") as fh:
        h.update(fh.read(size))
    return h.hexdigest()


# --------------------------- Filesystem Scanning -----------------------------

def _discover_large_pngs(root: str, min_side: int = 300):
    """Yield (path, dim) for visible PNGs whose smaller side ≥ *min_side*."""
    for cur_root, dirs, files in os.walk(root):
        # prune hidden directories from the walk
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        if _is_hidden(cur_root):
            continue
        for fname in files:
            if not fname.lower().endswith(".png"):
                continue
            full = os.path.join(cur_root, fname)
            dim = _get_png_dim(full)
            if dim and min(dim) >= min_side:
                yield full, dim


def _find_slide_cluster(png_items, expected_count: int, target_ratio: float, ratio_tol: float = 0.05):
    """Return (directory, paths) that best match the exported-slide cluster."""
    best_score, best_dir, best_paths = -1, None, []

    # Group candidates by directory
    directory_map = defaultdict(list)
    for path, dim in png_items:
        directory_map[os.path.dirname(path)].append((path, dim))

    for directory, items in directory_map.items():
        # Group images in this directory by identical dimensions within ratio tolerance
        dim_groups = defaultdict(list)
        for path, dim in items:
            if _aspect_ratio(dim) is None:
                continue
            if abs(_aspect_ratio(dim) - target_ratio) / target_ratio > ratio_tol:
                continue
            dim_groups[dim].append(path)

        # Evaluate each dimension group separately
        for dim, paths in dim_groups.items():
            count = len(paths)
            if not count:
                continue
            # Scoring components
            closeness = min(count, expected_count) / expected_count  # 1.0 when count ≥ expected
            name_hits = sum(
                bool(re.search(r"(slide|page).*?\d", os.path.basename(p), re.I))
                for p in paths
            )
            name_score = name_hits / count if count else 0.0
            score = closeness * 0.7 + name_score * 0.3  # weights sum to 1.0
            if score > best_score:
                best_score, best_dir, best_paths = score, directory, sorted(paths)

    # Require a modest score to treat as a real cluster (avoids random icons)
    return best_dir, best_paths if best_score >= 0.3 else (None, [])


# --------------------------- Main Verification ------------------------------

def verify_task(deck_path: str = DECK_PATH, res_path: str = RES_PATH):
    print(f"Verifying task for deck: {deck_path}")
    total_score = 0.0  # progressive score accumulator

    # 1. Load the deck to obtain slide count and expected aspect ratio
    if not os.path.exists(deck_path):
        print("✗ Deck file not found – task failed")
        print("REWARD: 0.0")
        return 0.0
    try:
        prs = Presentation(deck_path)
        slide_count = len(prs.slides)
        slide_ratio = prs.slide_width / prs.slide_height if prs.slide_height else 1.33
        print(f"✓ Deck loaded – {slide_count} slides (ratio≈{slide_ratio:.2f})")
    except Exception as e:
        print(f"✗ Unable to open deck: {e}")
        print("REWARD: 0.0")
        return 0.0

    # 2. Search filesystem for large PNGs
    print("Scanning filesystem for PNG images… (may take a moment)")
    png_items = list(_discover_large_pngs(VISIBLE_ROOT, min_side=300))
    print(f"  Large visible PNGs discovered: {len(png_items)}")

    # 3. Identify the cluster that represents exported slides
    export_dir, slide_pngs = _find_slide_cluster(png_items, slide_count, slide_ratio)
    if slide_pngs:
        exported_n = len(slide_pngs)
        export_score = min(exported_n, slide_count) / slide_count * 0.6  # max 0.6
        total_score += export_score
        print(
            f"✓ Detected slide export directory: {export_dir}\n"
            f"  Slide images detected: {exported_n} – score {export_score:.2f}/0.6"
        )
    else:
        print("✗ No suitable slide-export images found – 0 points for deck export")

    # 4. Validate res.png on Desktop
    if os.path.exists(res_path):
        res_dim = _get_png_dim(res_path)
        if res_dim and min(res_dim) >= 300:
            print(f"✓ res.png exists with dimension {res_dim}")
            total_score += 0.2  # res.png basic requirement met
            # Bonus if res.png matches one of the slide PNGs exactly
            matched = False
            for spath in slide_pngs:
                if res_dim == _get_png_dim(spath):
                    # Compare file sizes within 5 % as quick heuristic
                    sz_res, sz_sp = os.path.getsize(res_path), os.path.getsize(spath)
                    if abs(sz_res - sz_sp) / max(sz_sp, 1) <= 0.05:
                        # SHA-1 hash of first MB for stronger confirmation
                        if _sha1_first_mb(res_path) == _sha1_first_mb(spath):
                            matched = True
                            break
            if matched:
                total_score += 0.2
                print("✓ res.png content matches one of the slide images (+0.2)")
            else:
                print("⚠️ res.png does not exactly match detected slide images – no bonus")
        else:
            print("⚠️ res.png present but dimensions too small/unreadable – no points")
    else:
        print("✗ res.png not found on Desktop – 0 points for this requirement")

    # 5. Final score and output
    final_score = round(min(total_score, 1.0), 2)
    print(f"Total score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


# ----------------------------- Script Entry ----------------------------------
if __name__ == "__main__":
    verify_task()

