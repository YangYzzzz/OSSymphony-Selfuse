"""
Initial Setup: Badge template PDF and employee photo
Task ID: pdf_cross_081
Domain: gimp
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_081'
BADGE_PDF = f'{WORKDIR}/badge_template.pdf'
EMPLOYEE_PHOTO = f'{WORKDIR}/employee_photo.jpg'


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
    import pymupdf  # fitz
    from PIL import Image, ImageDraw, ImageFont
    import io

    # Ensure Documents directory exists
    os.makedirs(WORKDIR, exist_ok=True)

    # ---- Create badge_template.pdf ----
    # A standard ID badge size: ~3.375in x 5.375in at 72 dpi => ~243 x 387 pt
    badge_width_pt = 243
    badge_height_pt = 387

    doc = pymupdf.open()
    page = doc.new_page(width=badge_width_pt, height=badge_height_pt)

    # White background
    page.draw_rect(pymupdf.Rect(0, 0, badge_width_pt, badge_height_pt),
                   color=(1, 1, 1), fill=(1, 1, 1))

    # Company header bar (blue)
    page.draw_rect(pymupdf.Rect(0, 0, badge_width_pt, 50),
                   color=(0.1, 0.3, 0.7), fill=(0.1, 0.3, 0.7))

    # Company name text
    page.insert_text(
        pymupdf.Point(20, 32),
        "Acme Corporation",
        fontsize=14,
        color=(1, 1, 1),
        fontname="helv",
    )

    # Photo placeholder box at (50, 80) size 150x200 pixels
    # At 300 DPI, 1 pt = 72/300 = 0.24 in; but placeholder coordinates are in pixel space
    # The task says: paste photo at position (50, 80) in the rendered-at-300dpi image
    # We store the placeholder boundary with a light gray fill and border
    page.draw_rect(
        pymupdf.Rect(35.7, 57.1, 142.9, 199.9),  # ~150x200 pixels at 300dpi -> pt coords
        color=(0.5, 0.5, 0.5),
        fill=(0.88, 0.88, 0.88),
        width=1,
    )

    # "Photo Here" label inside placeholder
    page.insert_text(
        pymupdf.Point(55, 130),
        "Photo Here",
        fontsize=9,
        color=(0.4, 0.4, 0.4),
        fontname="helv",
    )

    # Name field line
    page.draw_line(
        pymupdf.Point(20, 230), pymupdf.Point(223, 230),
        color=(0.2, 0.2, 0.2), width=0.5
    )
    page.insert_text(pymupdf.Point(20, 225), "Name:", fontsize=9, color=(0.2, 0.2, 0.2))

    # Title field line
    page.draw_line(
        pymupdf.Point(20, 260), pymupdf.Point(223, 260),
        color=(0.2, 0.2, 0.2), width=0.5
    )
    page.insert_text(pymupdf.Point(20, 255), "Title:", fontsize=9, color=(0.2, 0.2, 0.2))

    # Department field line
    page.draw_line(
        pymupdf.Point(20, 290), pymupdf.Point(223, 290),
        color=(0.2, 0.2, 0.2), width=0.5
    )
    page.insert_text(pymupdf.Point(20, 285), "Department:", fontsize=9, color=(0.2, 0.2, 0.2))

    # Footer bar
    page.draw_rect(pymupdf.Rect(0, 340, badge_width_pt, badge_height_pt),
                   color=(0.1, 0.3, 0.7), fill=(0.1, 0.3, 0.7))
    page.insert_text(pymupdf.Point(20, 365), "Employee ID Badge", fontsize=9,
                     color=(1, 1, 1), fontname="helv")

    doc.save(BADGE_PDF)
    doc.close()
    print(f'Badge template created: {BADGE_PDF}')

    # ---- Create employee_photo.jpg (1200x1600 portrait) ----
    img = Image.new("RGB", (1200, 1600), color=(210, 180, 140))  # tan background

    draw = ImageDraw.Draw(img)

    # Simple portrait: face circle
    # Face oval
    draw.ellipse([350, 200, 850, 800], fill=(255, 220, 185))
    # Hair
    draw.ellipse([330, 180, 870, 550], fill=(80, 40, 20))
    # Eyes
    draw.ellipse([450, 380, 530, 440], fill=(255, 255, 255))
    draw.ellipse([670, 380, 750, 440], fill=(255, 255, 255))
    draw.ellipse([472, 398, 508, 422], fill=(50, 30, 10))
    draw.ellipse([692, 398, 728, 422], fill=(50, 30, 10))
    # Nose
    draw.ellipse([575, 490, 625, 540], fill=(240, 195, 160))
    # Smile
    draw.arc([500, 560, 700, 660], start=0, end=180, fill=(180, 80, 80), width=8)

    # Shirt
    draw.polygon([(200, 800), (600, 750), (600, 1600), (200, 1600)], fill=(30, 60, 130))
    draw.polygon([(1000, 800), (600, 750), (600, 1600), (1000, 1600)], fill=(30, 60, 130))

    # Neck
    draw.rectangle([530, 720, 670, 800], fill=(255, 220, 185))

    # Background gradient effect
    for y in range(0, 200):
        alpha = int(y * 1.27)
        draw.rectangle([0, y, 1200, y + 1], fill=(180, 200, 220))

    img.save(EMPLOYEE_PHOTO, quality=92)
    print(f'Employee photo created: {EMPLOYEE_PHOTO}')

    # Launch GIMP with the badge template PDF
    launch_gui(f'gimp "{BADGE_PDF}"', delay_sec=3.0)
    print('GUI_READY: launched GIMP with badge_template.pdf with DISPLAY=:0')


create_initial()
