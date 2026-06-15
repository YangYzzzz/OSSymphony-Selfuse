"""
Initial Setup: Image Batch Processor with PIL UnidentifiedImageError crash bug
Task ID: osworld_multi_apps_vscode_debug_crash_008
Domain: vscode / multi_apps
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_debug_crash_008'
PROJECT_DIR = f'{WORKDIR}/Desktop/img_processor'
INPUT_DIR = f'{PROJECT_DIR}/input'
OUTPUT_DIR = f'{PROJECT_DIR}/output'


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


def create_initial():
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/logs', exist_ok=True)

    # --- logger.py ---
    logger_content = '''"""
Logger module for img_processor project.
Provides logging utilities for the batch image processor.
"""

import logging
import os
from datetime import datetime


def setup_logger(name: str, log_file: str = None, level=logging.INFO) -> logging.Logger:
    """Set up a logger with optional file handler."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Default application logger
app_logger = setup_logger('img_processor', log_file='/home/user/Desktop/img_processor/logs/app.log')
'''

    # --- utils.py ---
    utils_content = '''"""
Utility functions for image batch processor.
"""

import os
from pathlib import Path


SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}


def get_files_in_directory(directory: str) -> list:
    """Return a list of all files in the given directory (non-recursive)."""
    if not os.path.isdir(directory):
        raise ValueError(f"Directory does not exist: {directory}")
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]


def has_image_extension(filepath: str) -> bool:
    """Check if a file has a recognized image extension."""
    ext = Path(filepath).suffix.lower()
    return ext in SUPPORTED_EXTENSIONS


def ensure_output_dir(output_dir: str) -> None:
    """Create the output directory if it does not exist."""
    os.makedirs(output_dir, exist_ok=True)


def get_output_path(input_path: str, output_dir: str, suffix: str = '_processed') -> str:
    """Generate an output file path based on input path."""
    stem = Path(input_path).stem
    ext = Path(input_path).suffix
    return os.path.join(output_dir, f'{stem}{suffix}{ext}')
'''

    # --- processor.py (BUGGY VERSION - no error handling for non-image files) ---
    processor_content = '''"""
Image Batch Processor - Core processing module.
Processes all files in the input directory and saves results to output directory.
"""

import os
from PIL import Image
from utils import get_files_in_directory, get_output_path, ensure_output_dir
from logger import app_logger


def apply_grayscale(img: Image.Image) -> Image.Image:
    """Convert image to grayscale."""
    return img.convert('L').convert('RGB')


def apply_resize(img: Image.Image, width: int = 800, height: int = 600) -> Image.Image:
    """Resize image to given dimensions while preserving aspect ratio."""
    img.thumbnail((width, height), Image.LANCZOS)
    return img


def process_image(input_path: str, output_path: str) -> bool:
    """
    Process a single image: resize and convert to grayscale.
    Returns True if successful, False otherwise.
    """
    try:
        img = Image.open(input_path)
        img = apply_resize(img)
        img = apply_grayscale(img)
        img.save(output_path)
        app_logger.info(f"Processed: {input_path} -> {output_path}")
        return True
    except Exception as e:
        app_logger.error(f"Failed to process {input_path}: {e}")
        return False


def run_batch(input_dir: str, output_dir: str) -> dict:
    """
    Process all files in the input directory.
    Returns a summary dict with counts of processed and failed files.
    """
    ensure_output_dir(output_dir)
    files = get_files_in_directory(input_dir)

    processed = 0
    failed = 0

    app_logger.info(f"Starting batch processing of {len(files)} files from {input_dir}")

    for filepath in sorted(files):
        output_path = get_output_path(filepath, output_dir)
        # BUG: No check for non-image files; PIL.Image.open() will raise
        # PIL.UnidentifiedImageError for .txt, .csv, and other non-image files.
        img = Image.open(filepath)
        img = apply_resize(img)
        img = apply_grayscale(img)
        img.save(output_path)
        app_logger.info(f"Processed: {filepath}")
        processed += 1

    summary = {
        'total': len(files),
        'processed': processed,
        'failed': failed,
    }
    app_logger.info(f"Batch complete: {summary}")
    return summary
'''

    # --- main.py ---
    main_content = '''"""
Main entry point for the image batch processor.
"""

import os
import sys
from processor import run_batch
from logger import app_logger


INPUT_DIR = os.path.join(os.path.dirname(__file__), 'input')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')


def main():
    app_logger.info("Image Batch Processor starting...")
    app_logger.info(f"Input directory:  {INPUT_DIR}")
    app_logger.info(f"Output directory: {OUTPUT_DIR}")

    if not os.path.isdir(INPUT_DIR):
        app_logger.error(f"Input directory not found: {INPUT_DIR}")
        sys.exit(1)

    summary = run_batch(INPUT_DIR, OUTPUT_DIR)
    app_logger.info(f"Done. Processed {summary[\'processed\']} / {summary[\'total\']} files.")


if __name__ == '__main__':
    main()
'''

    # Write Python source files
    with open(f'{PROJECT_DIR}/logger.py', 'w') as f:
        f.write(logger_content)

    with open(f'{PROJECT_DIR}/utils.py', 'w') as f:
        f.write(utils_content)

    with open(f'{PROJECT_DIR}/processor.py', 'w') as f:
        f.write(processor_content)

    with open(f'{PROJECT_DIR}/main.py', 'w') as f:
        f.write(main_content)

    print(f"Created project files in {PROJECT_DIR}")

    # Create sample input files: real images and non-image files
    # Create a small valid PNG using raw bytes (1x1 red pixel PNG)
    import struct
    import zlib

    def create_minimal_png(path: str, width: int = 64, height: int = 64,
                           r: int = 200, g: int = 100, b: int = 50):
        """Create a minimal valid PNG file."""
        # PNG signature
        sig = b'\x89PNG\r\n\x1a\n'

        # IHDR chunk
        ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
        ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
        ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)

        # IDAT chunk (raw pixel data: each row starts with filter byte 0)
        raw_data = b''
        for _ in range(height):
            raw_data += b'\x00'  # filter byte
            for _ in range(width):
                raw_data += bytes([r, g, b])
        compressed = zlib.compress(raw_data)
        idat_crc = zlib.crc32(b'IDAT' + compressed) & 0xffffffff
        idat = struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', idat_crc)

        # IEND chunk
        iend_crc = zlib.crc32(b'IEND') & 0xffffffff
        iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)

        with open(path, 'wb') as f:
            f.write(sig + ihdr + idat + iend)

    # Create valid image files
    create_minimal_png(f'{INPUT_DIR}/photo_landscape_001.png', 80, 60, 135, 180, 220)
    create_minimal_png(f'{INPUT_DIR}/photo_portrait_002.png', 60, 80, 220, 160, 100)
    create_minimal_png(f'{INPUT_DIR}/product_shot_003.png', 100, 100, 80, 160, 80)

    # Create non-image files (these will crash the buggy processor)
    with open(f'{INPUT_DIR}/metadata.txt', 'w') as f:
        f.write("Image batch metadata\nDate: 2025-03-01\nAuthor: Alice Nguyen\nBatch ID: IMG-2025-0301\n")

    with open(f'{INPUT_DIR}/inventory.csv', 'w') as f:
        f.write("filename,category,tags,date_taken\n")
        f.write("photo_landscape_001.png,nature,sky|clouds|blue,2025-02-14\n")
        f.write("photo_portrait_002.png,people,outdoor|casual,2025-02-15\n")
        f.write("product_shot_003.png,product,studio|white_bg,2025-02-16\n")

    with open(f'{INPUT_DIR}/notes.txt', 'w') as f:
        f.write("Processing notes:\n- Apply grayscale filter to all images\n- Resize to max 800x600\n- Check histogram after conversion\n")

    print(f"Created input files: 3 valid PNGs and 3 non-image files (metadata.txt, inventory.csv, notes.txt)")
    print(f"Output directory ready: {OUTPUT_DIR}")

    # Open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print(f'GUI_READY: VSCode launched with {PROJECT_DIR} (DISPLAY=:0)')


create_initial()
