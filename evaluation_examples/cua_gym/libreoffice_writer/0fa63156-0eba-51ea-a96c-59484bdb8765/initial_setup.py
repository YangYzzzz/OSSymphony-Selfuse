#!/usr/bin/env python3
"""initial_setup.py - Create a blank .docx and open it in LibreOffice Writer."""

import subprocess
import time
import os

# Kill any existing LibreOffice processes
subprocess.run(["pkill", "-f", "soffice"], capture_output=True)
time.sleep(1)

# Create a blank document using python-docx
from docx import Document

doc = Document()
doc.save("/home/user/writer_wf_081.docx")

# Open in LibreOffice Writer
env = os.environ.copy()
env["DISPLAY"] = ":0"
subprocess.Popen(
    ["libreoffice", "--writer", "/home/user/writer_wf_081.docx"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    env=env,
)
time.sleep(3)

print("initial_setup.py completed successfully.")
