"""
Initial Setup: AutoCorrect 'dept' -> 'Department' in LibreOffice Writer
Task ID: writer_frd_061
Domain: libreoffice_writer

Initial state: LibreOffice Writer open with a blank document.
No AutoCorrect entry for 'dept' -> 'Department' exists.
"""

import os
import shlex
import subprocess
import time
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_061'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'
AUTOCORR_DIR = f'{WORKDIR}/.config/libreoffice/4/user/autocorr'
AUTOCORR_FILE = f'{AUTOCORR_DIR}/acor_en-US.dat'


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


def ensure_no_dept_autocorrect():
    """Make sure there is no user-level 'dept' -> 'Department' autocorrect entry."""
    if os.path.exists(AUTOCORR_FILE):
        # If a user-level autocorrect file exists, check and remove any 'dept' entry
        import tempfile
        import shutil

        with zipfile.ZipFile(AUTOCORR_FILE, 'r') as z:
            content = z.read('DocumentList.xml').decode('utf-8')

        if 'abbreviated-name="dept"' in content:
            # Remove the dept entry
            import re
            content = re.sub(
                r'<block-list:block\s+block-list:abbreviated-name="dept"\s+block-list:name="[^"]*"\s*/>\s*',
                '',
                content
            )
            # Rewrite the dat file
            tmp = AUTOCORR_FILE + '.tmp'
            with zipfile.ZipFile(AUTOCORR_FILE, 'r') as zin:
                with zipfile.ZipFile(tmp, 'w') as zout:
                    for item in zin.namelist():
                        if item == 'DocumentList.xml':
                            zout.writestr(item, content)
                        else:
                            zout.writestr(item, zin.read(item))
            shutil.move(tmp, AUTOCORR_FILE)
            print('Removed existing dept autocorrect entry from user file')
        else:
            print('No dept entry in user autocorrect file')
    else:
        print('No user-level autocorrect file exists (good - clean state)')


def create_blank_document():
    """Create a simple blank document for Writer to open."""
    from docx import Document

    doc = Document()
    doc.add_paragraph('')
    doc.save(OUTPUT)
    print(f'Blank document created: {OUTPUT}')


def main():
    ensure_no_dept_autocorrect()
    create_blank_document()

    # Open LibreOffice Writer with the blank document
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


main()
