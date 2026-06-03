"""
Initial Setup: Create a legal proof of service form with interactive form fields
Task ID: pdf_legal_058
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_058'
FORM_DIR = f'{WORKDIR}/legal/forms'
OUTPUT = f'{FORM_DIR}/proof_of_service.pdf'


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
    # Ensure directory exists
    os.makedirs(FORM_DIR, exist_ok=True)

    doc = pymupdf.open()
    # -- Page 1: Proof of Service Form --
    page = doc.new_page(width=612, height=792)  # US Letter

    # Header
    page.insert_text(
        pymupdf.Point(72, 50),
        "SUPERIOR COURT OF CALIFORNIA",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(72, 68),
        "COUNTY OF SAN FRANCISCO",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0, 0), width=1.5)
    shape.commit()

    # Title
    page.insert_text(
        pymupdf.Point(200, 110),
        "PROOF OF SERVICE",
        fontsize=16,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Case info (static)
    page.insert_text(pymupdf.Point(72, 140), "Case No.: 2024-CV-03891", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 156), "Filed in connection with: Motion for Summary Judgment", fontsize=11, fontname="helv", color=(0, 0, 0))

    # Separator
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(72, 170), pymupdf.Point(540, 170))
    shape2.finish(color=(0.5, 0.5, 0.5), width=0.5)
    shape2.commit()

    # Instructions
    page.insert_textbox(
        pymupdf.Rect(72, 180, 540, 220),
        "I, the undersigned, declare under penalty of perjury that I served the "
        "documents described below on the party or parties listed, in the manner indicated.",
        fontsize=10,
        fontname="tiit",
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Form field labels and widgets ---
    y_start = 240
    field_spacing = 50
    label_x = 72
    field_x = 230
    field_width = 310
    field_height = 22

    fields = [
        ("Server Name:", "ServerName", ""),
        ("Served Party:", "ServedParty", ""),
        ("Served Person:", "ServedPerson", ""),
        ("Date of Service:", "ServiceDate", ""),
        ("Time of Service:", "ServiceTime", ""),
        ("Service Address:", "ServiceAddress", ""),
        ("Method of Service:", "ServiceMethod", ""),
    ]

    for i, (label, field_name, default_val) in enumerate(fields):
        y = y_start + i * field_spacing

        # Label
        page.insert_text(
            pymupdf.Point(label_x, y + 15),
            label,
            fontsize=11,
            fontname="hebo",
            color=(0, 0, 0),
        )

        # Form field (text widget)
        widget = pymupdf.Widget()
        widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
        widget.field_name = field_name
        widget.field_value = default_val
        widget.rect = pymupdf.Rect(field_x, y, field_x + field_width, y + field_height)
        widget.text_fontsize = 11
        widget.text_color = (0, 0, 0)
        widget.fill_color = (0.97, 0.97, 0.97)
        widget.border_color = (0.4, 0.4, 0.4)
        widget.border_width = 1
        page.add_widget(widget)

    # --- Declaration / Signature Section ---
    sig_y = y_start + len(fields) * field_spacing + 30

    page.insert_textbox(
        pymupdf.Rect(72, sig_y, 540, sig_y + 50),
        "I declare under penalty of perjury under the laws of the State of California "
        "that the foregoing is true and correct.",
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    sig_y2 = sig_y + 70

    # Signature line
    shape3 = page.new_shape()
    shape3.draw_line(pymupdf.Point(72, sig_y2), pymupdf.Point(300, sig_y2))
    shape3.finish(color=(0, 0, 0), width=0.8)
    shape3.commit()
    page.insert_text(pymupdf.Point(72, sig_y2 + 14), "Signature of Server", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

    # Date line
    shape4 = page.new_shape()
    shape4.draw_line(pymupdf.Point(350, sig_y2), pymupdf.Point(540, sig_y2))
    shape4.finish(color=(0, 0, 0), width=0.8)
    shape4.commit()
    page.insert_text(pymupdf.Point(350, sig_y2 + 14), "Date", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

    # Footer
    page.insert_text(
        pymupdf.Point(200, 750),
        "Form POS-010 (Rev. January 2024)",
        fontsize=8,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
