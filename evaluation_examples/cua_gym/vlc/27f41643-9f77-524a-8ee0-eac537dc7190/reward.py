"""
Reward Script: VLC snapshot at 1:45 inserted into LibreOffice Writer document
Task ID: vlcplay_013
Domain: vlc (cross-app: VLC + LibreOffice Writer)
Scoring:
  Component 1 (0.30): Snapshot PNG file exists in ~/Pictures/
  Component 2 (0.20): Snapshot is a valid image with video-frame-like dimensions
  Component 3 (0.30): notes.docx contains at least one inline image
  Component 4 (0.20): The embedded image in notes.docx matches the snapshot file in ~/Pictures/
"""

import os
import glob
import hashlib
import zipfile
import io

WORKDIR = '/home/user'
TASK_ID = 'vlcplay_013'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice Writer edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.5)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def find_snapshot_files(pictures_dir):
    """Find PNG files in Pictures directory that look like VLC snapshots."""
    png_files = glob.glob(os.path.join(pictures_dir, "*.png"))
    return png_files


def get_file_hash(filepath):
    """Get MD5 hash of a file."""
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def get_docx_embedded_image_hashes(docx_path):
    """Extract MD5 hashes of all embedded images in a docx file."""
    hashes = []
    try:
        with zipfile.ZipFile(docx_path, 'r') as z:
            for name in z.namelist():
                if name.startswith('word/media/') and name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    data = z.read(name)
                    h = hashlib.md5(data).hexdigest()
                    hashes.append((name, h, len(data)))
    except Exception as e:
        print(f"ERROR: Could not read docx zip: {e}")
    return hashes


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    pictures_dir = os.path.join(WORKDIR, 'Pictures')
    docx_path = os.path.join(WORKDIR, 'Documents', 'notes.docx')

    # Precondition: notes.docx must exist
    if not os.path.exists(docx_path):
        print(f"CRITICAL: notes.docx not found at {docx_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Snapshot PNG file exists in ~/Pictures/ (0.30 points)
    # Initial env has EMPTY Pictures dir, so any PNG there is task-introduced
    snapshot_files = []
    try:
        snapshot_files = find_snapshot_files(pictures_dir)
        if len(snapshot_files) > 0:
            print(f"PASS: Component 1 — Found {len(snapshot_files)} PNG file(s) in Pictures/: {[os.path.basename(f) for f in snapshot_files]} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — No PNG files found in {pictures_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Snapshot is a valid image with video-frame-like dimensions (0.20 points)
    # A VLC snapshot from tutorial.avi should be a reasonable resolution image
    try:
        if snapshot_files:
            from PIL import Image
            snapshot_path = snapshot_files[0]
            img = Image.open(snapshot_path)
            w, h = img.size
            # Valid video frame should be at least 320x240 and have reasonable aspect ratio
            if w >= 320 and h >= 240 and 0.5 < (w / h) < 3.0:
                print(f"PASS: Component 2 — Snapshot is valid image ({w}x{h}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — Snapshot dimensions unexpected: {w}x{h}")
        else:
            print(f"FAIL: Component 2 — No snapshot file to validate")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: notes.docx contains at least one inline image (0.30 points)
    # Initial env has 0 images in the docx; golden should have >= 1
    docx_image_hashes = []
    try:
        from docx import Document
        doc = Document(docx_path)
        num_inline_shapes = len(doc.inline_shapes)
        docx_image_hashes = get_docx_embedded_image_hashes(docx_path)

        if num_inline_shapes > 0 and len(docx_image_hashes) > 0:
            print(f"PASS: Component 3 — notes.docx has {num_inline_shapes} inline shape(s) and {len(docx_image_hashes)} embedded image(s) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — notes.docx has {num_inline_shapes} inline shapes and {len(docx_image_hashes)} embedded images")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Embedded image matches snapshot file from Pictures/ (0.20 points)
    # This verifies the agent actually inserted the VLC snapshot (not some random image)
    try:
        if snapshot_files and docx_image_hashes:
            snapshot_hash = get_file_hash(snapshot_files[0])
            embedded_hashes = [h for _, h, _ in docx_image_hashes]
            if snapshot_hash in embedded_hashes:
                print(f"PASS: Component 4 — Embedded image matches snapshot file (hash: {snapshot_hash[:12]}...) (0.20 pts)")
                total_score += 0.20
            else:
                # Fallback: compare file sizes (images may be re-encoded)
                snapshot_size = os.path.getsize(snapshot_files[0])
                embedded_sizes = [s for _, _, s in docx_image_hashes]
                size_match = any(abs(snapshot_size - es) < 100 for es in embedded_sizes)
                if size_match:
                    print(f"PASS: Component 4 — Embedded image size matches snapshot ({snapshot_size} bytes) (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 4 — Snapshot hash {snapshot_hash[:12]} not in embedded hashes {[h[:12] for h in embedded_hashes]}, sizes also differ: snap={snapshot_size} vs embedded={embedded_sizes}")
        else:
            print(f"FAIL: Component 4 — Missing snapshot ({len(snapshot_files)}) or docx images ({len(docx_image_hashes)})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")
verify_task()
