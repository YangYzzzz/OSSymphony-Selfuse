"""
Initial Setup: Organize research paper PDFs on Desktop
Task ID: osworld_multi_apps_doc_desktop_organize_006
Domain: libreoffice_calc (+ OS file operations)

Creates 15 PDF placeholder files on the Desktop with author-year-title filenames.
No year folders and no catalog file exist initially.
Opens a file manager (Nautilus) showing the Desktop so the agent can see the files.
"""

import os
import shlex
import subprocess
import time

DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_doc_desktop_organize_006'

# 15 research PDFs spanning years 2020–2024 (3 per year)
PDF_FILES = [
    # 2020
    'brown2020language.pdf',
    'raffel2020exploring.pdf',
    'dosovitskiy2020image.pdf',
    # 2021
    'jones2021transformer.pdf',
    'loshchilov2021decoupled.pdf',
    'radford2021learning.pdf',
    # 2022
    'smith2022attention.pdf',
    'wei2022chain.pdf',
    'ouyang2022training.pdf',
    # 2023
    'wang2023llm.pdf',
    'touvron2023llama.pdf',
    'achiam2023gpt.pdf',
    # 2024
    'dubey2024llama.pdf',
    'yang2024qwen.pdf',
    'bai2024longalign.pdf',
]


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch a GUI app on the VM display without blocking script exit."""
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
    # Ensure Desktop exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any existing year folders to ensure clean initial state
    for year in ['2020', '2021', '2022', '2023', '2024']:
        year_dir = os.path.join(DESKTOP, year)
        if os.path.isdir(year_dir):
            import shutil
            shutil.rmtree(year_dir)

    # Remove catalog file if it exists from a prior run
    catalog_path = os.path.join(DESKTOP, 'papers_catalog.ods')
    if os.path.isfile(catalog_path):
        os.remove(catalog_path)

    # Create placeholder PDF files on the Desktop
    for filename in PDF_FILES:
        filepath = os.path.join(DESKTOP, filename)
        if not os.path.isfile(filepath):
            # Create a minimal but valid-looking placeholder text file with .pdf extension
            with open(filepath, 'w') as f:
                f.write(f'%PDF-1.4\n% Placeholder PDF: {filename}\n')
        print(f'  Created: {filepath}')

    print(f'Initial state: {len(PDF_FILES)} PDF files on Desktop')
    print(f'Desktop path: {DESKTOP}')

    # GUI-ready startup: open Nautilus showing the Desktop
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus on Desktop with DISPLAY=:0')


create_initial()
