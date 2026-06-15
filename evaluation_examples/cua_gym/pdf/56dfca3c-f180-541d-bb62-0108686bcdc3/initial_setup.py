"""
Initial Setup: Convert SVG diagram to PDF preserving vector graphics quality.
Task ID: pdf_mbc_088
Domain: pdf

Creates ~/Documents/diagram.svg - a flowchart with shapes, arrows, and text labels.
Opens the file manager showing ~/Documents/ so the agent can see the SVG file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_088'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
OUTPUT_SVG = f'{DOCUMENTS_DIR}/diagram.svg'


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
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    # Create an SVG flowchart with shapes, arrows, and text labels
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333333"/>
    </marker>
    <style>
      .title-text { font-family: Arial, Helvetica, sans-serif; font-size: 24px; font-weight: bold; fill: #1a1a2e; }
      .box-text { font-family: Arial, Helvetica, sans-serif; font-size: 14px; fill: #ffffff; }
      .diamond-text { font-family: Arial, Helvetica, sans-serif; font-size: 13px; fill: #ffffff; }
      .label-text { font-family: Arial, Helvetica, sans-serif; font-size: 11px; fill: #555555; }
    </style>
  </defs>

  <!-- Background -->
  <rect width="800" height="600" fill="#f8f9fa" rx="8"/>

  <!-- Title -->
  <text x="400" y="45" text-anchor="middle" class="title-text">Software Release Process</text>

  <!-- Start: Rounded rectangle -->
  <rect x="325" y="70" width="150" height="45" rx="22" ry="22" fill="#2ecc71" stroke="#27ae60" stroke-width="2"/>
  <text x="400" y="98" text-anchor="middle" class="box-text">Start Release</text>

  <!-- Arrow: Start -> Code Review -->
  <line x1="400" y1="115" x2="400" y2="150" stroke="#333333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Code Review: Rectangle -->
  <rect x="300" y="150" width="200" height="50" rx="6" ry="6" fill="#3498db" stroke="#2980b9" stroke-width="2"/>
  <text x="400" y="180" text-anchor="middle" class="box-text">Code Review</text>

  <!-- Arrow: Code Review -> Tests Pass? -->
  <line x1="400" y1="200" x2="400" y2="245" stroke="#333333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Decision Diamond: Tests Pass? -->
  <polygon points="400,245 480,290 400,335 320,290" fill="#e74c3c" stroke="#c0392b" stroke-width="2"/>
  <text x="400" y="295" text-anchor="middle" class="diamond-text">Tests Pass?</text>

  <!-- Arrow: Tests Pass? -> Yes -> Build Package -->
  <line x1="480" y1="290" x2="560" y2="290" stroke="#333333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="515" y="282" text-anchor="middle" class="label-text">Yes</text>

  <!-- Arrow: Tests Pass? -> No -> Fix Bugs -->
  <line x1="320" y1="290" x2="240" y2="290" stroke="#333333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="285" y="282" text-anchor="middle" class="label-text">No</text>

  <!-- Fix Bugs: Rectangle -->
  <rect x="100" y="265" width="140" height="50" rx="6" ry="6" fill="#f39c12" stroke="#e67e22" stroke-width="2"/>
  <text x="170" y="295" text-anchor="middle" class="box-text">Fix Bugs</text>

  <!-- Arrow: Fix Bugs -> Code Review (loop back) -->
  <line x1="170" y1="265" x2="170" y2="175" stroke="#333333" stroke-width="2"/>
  <line x1="170" y1="175" x2="300" y2="175" stroke="#333333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Build Package: Rectangle -->
  <rect x="560" y="265" width="160" height="50" rx="6" ry="6" fill="#3498db" stroke="#2980b9" stroke-width="2"/>
  <text x="640" y="295" text-anchor="middle" class="box-text">Build Package</text>

  <!-- Arrow: Build Package -> QA Review -->
  <line x1="640" y1="315" x2="640" y2="365" stroke="#333333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Decision Diamond: QA Approved? -->
  <polygon points="640,365 720,410 640,455 560,410" fill="#e74c3c" stroke="#c0392b" stroke-width="2"/>
  <text x="640" y="413" text-anchor="middle" class="diamond-text">QA OK?</text>

  <!-- Arrow: QA Approved? -> Yes -> Deploy -->
  <line x1="640" y1="455" x2="640" y2="495" stroke="#333333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="660" y="480" text-anchor="start" class="label-text">Yes</text>

  <!-- Arrow: QA Approved? -> No -> Fix Bugs -->
  <line x1="560" y1="410" x2="170" y2="410" stroke="#333333" stroke-width="2"/>
  <line x1="170" y1="410" x2="170" y2="315" stroke="#333333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="370" y="402" text-anchor="middle" class="label-text">No</text>

  <!-- Deploy to Production: Rectangle -->
  <rect x="555" y="495" width="170" height="50" rx="6" ry="6" fill="#9b59b6" stroke="#8e44ad" stroke-width="2"/>
  <text x="640" y="525" text-anchor="middle" class="box-text">Deploy to Prod</text>

  <!-- Arrow: Deploy -> End -->
  <line x1="640" y1="545" x2="400" y2="545" stroke="#333333" stroke-width="2"/>
  <line x1="400" y1="545" x2="400" y2="560" stroke="#333333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- End: Rounded rectangle -->
  <rect x="330" y="560" width="140" height="35" rx="17" ry="17" fill="#2ecc71" stroke="#27ae60" stroke-width="2"/>
  <text x="400" y="583" text-anchor="middle" class="box-text" style="font-size:13px;">Release Complete</text>
</svg>'''

    with open(OUTPUT_SVG, 'w') as f:
        f.write(svg_content)

    print(f'Initial SVG file created: {OUTPUT_SVG}')

    # Ensure no PDF file exists (the agent must create it)
    pdf_path = f'{DOCUMENTS_DIR}/diagram.pdf'
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    # Open file manager showing Documents directory so agent sees the SVG
    launch_gui(f'nautilus "{DOCUMENTS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
