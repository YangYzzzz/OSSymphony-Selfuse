"""
Initial Setup: Create ~/Documents/timesheet.pdf — an empty 2-page timesheet form.
Task ID: pdf_adv_188
Domain: pdf

The agent must create ~/Documents/timesheet.pdf with:
  Page 1: text fields 'employee_name', 'employee_id', 'department', 'week_ending'
  Page 2: text fields 'monday_hours', 'tuesday_hours', 'wednesday_hours',
           'thursday_hours', 'friday_hours', 'total_hours', and checkbox 'supervisor_approved'

Initial state: the file does NOT exist; this script creates a blank (no-form-fields) 2-page
placeholder so the GUI agent has a starting document to open.
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = "/home/user/Documents"
OUTPUT = f"{WORKDIR}/timesheet.pdf"

# A4 dimensions in points
PAGE_W, PAGE_H = 595, 842


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
    os.makedirs(WORKDIR, exist_ok=True)

    doc = pymupdf.open()

    # ── PAGE 1: Employee Information ────────────────────────────────────────
    page1 = doc.new_page(width=PAGE_W, height=PAGE_H)

    # Title
    page1.insert_text(
        pymupdf.Point(72, 60),
        "EMPLOYEE TIMESHEET",
        fontsize=20,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )
    page1.insert_text(
        pymupdf.Point(72, 85),
        "Employee Information — Page 1 of 2",
        fontsize=10,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    # Horizontal separator
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(PAGE_W - 72, 95))
    shape.finish(color=(0.3, 0.3, 0.6), width=1.5)
    shape.commit()

    # Labels and blank lines (no interactive fields — agent must add them)
    fields_info = [
        ("Employee Name:", 140),
        ("Employee ID:", 210),
        ("Department:", 280),
        ("Week Ending:", 350),
    ]
    for label, y in fields_info:
        page1.insert_text(
            pymupdf.Point(72, y),
            label,
            fontsize=11,
            fontname="hebo",
            color=(0.15, 0.15, 0.15),
        )
        # Blank line placeholder
        shape = page1.new_shape()
        shape.draw_line(pymupdf.Point(215, y + 4), pymupdf.Point(PAGE_W - 72, y + 4))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.75)
        shape.commit()

    page1.insert_text(
        pymupdf.Point(72, PAGE_H - 60),
        "Acme Corporation — Confidential",
        fontsize=8,
        fontname="tiro",
        color=(0.6, 0.6, 0.6),
    )

    # ── PAGE 2: Hours Tracking ───────────────────────────────────────────────
    page2 = doc.new_page(width=PAGE_W, height=PAGE_H)

    page2.insert_text(
        pymupdf.Point(72, 60),
        "EMPLOYEE TIMESHEET",
        fontsize=20,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )
    page2.insert_text(
        pymupdf.Point(72, 85),
        "Hours Worked — Page 2 of 2",
        fontsize=10,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    shape = page2.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(PAGE_W - 72, 95))
    shape.finish(color=(0.3, 0.3, 0.6), width=1.5)
    shape.commit()

    hours_fields = [
        ("Monday Hours:", 140),
        ("Tuesday Hours:", 210),
        ("Wednesday Hours:", 280),
        ("Thursday Hours:", 350),
        ("Friday Hours:", 420),
        ("Total Hours:", 490),
    ]
    for label, y in hours_fields:
        page2.insert_text(
            pymupdf.Point(72, y),
            label,
            fontsize=11,
            fontname="hebo",
            color=(0.15, 0.15, 0.15),
        )
        shape = page2.new_shape()
        shape.draw_line(pymupdf.Point(230, y + 4), pymupdf.Point(PAGE_W - 72, y + 4))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.75)
        shape.commit()

    # Supervisor approval section (no checkbox yet — agent must add it)
    page2.insert_text(
        pymupdf.Point(72, 570),
        "Supervisor Approval:",
        fontsize=11,
        fontname="hebo",
        color=(0.15, 0.15, 0.15),
    )
    # Empty box placeholder for checkbox
    shape = page2.new_shape()
    shape.draw_rect(pymupdf.Rect(235, 555, 255, 575))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.75)
    shape.commit()

    page2.insert_text(
        pymupdf.Point(72, PAGE_H - 60),
        "Acme Corporation — Confidential",
        fontsize=8,
        fontname="tiro",
        color=(0.6, 0.6, 0.6),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f"Created: {OUTPUT}")

    # Verify
    verify = pymupdf.open(OUTPUT)
    assert verify.page_count == 2, f"Expected 2 pages, got {verify.page_count}"
    # No interactive form fields in initial state
    field_count = sum(1 for page in verify for _ in page.widgets())
    assert field_count == 0, f"Initial file should have 0 form fields, got {field_count}"
    verify.close()
    print("Verified: timesheet.pdf has 2 pages and 0 form fields (initial state)")

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched Evince with DISPLAY=:0")


create_initial()
