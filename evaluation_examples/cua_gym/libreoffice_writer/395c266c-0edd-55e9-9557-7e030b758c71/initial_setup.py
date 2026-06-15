"""
initial_setup.py - Create a blank Writer document and launch it in LibreOffice Writer.
Task: writer_hr_066 - Employee Onboarding Packet
"""

import subprocess
import os
import time

WORKDIR = '/home/user'
FILEPATH = os.path.join(WORKDIR, 'writer_hr_066.docx')

# Create a blank document
from docx import Document

doc = Document()
doc.save(FILEPATH)
print(f"Blank document created at {FILEPATH}")

# Launch in LibreOffice Writer GUI
env = os.environ.copy()
env["DISPLAY"] = ":0"
subprocess.Popen(
    ["libreoffice", "--writer", FILEPATH],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    env=env
)
time.sleep(2)
print("LibreOffice Writer launched.")
