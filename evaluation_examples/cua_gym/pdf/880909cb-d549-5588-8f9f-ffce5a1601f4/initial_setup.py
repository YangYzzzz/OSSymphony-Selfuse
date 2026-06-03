"""
Initial Setup: Create a 5-page architectural blueprint PDF with 'Emergency Exit' label on page 2.
Task ID: pdf_fm_027
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_027'
DOCDIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCDIR}/blueprint.pdf'

# Page dimensions (Letter size)
W, H = 612, 792

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


def draw_room(shape, x, y, w, h, label):
    """Draw a room rectangle with label."""
    rect = pymupdf.Rect(x, y, x + w, y + h)
    shape.draw_rect(rect)
    shape.finish(color=(0, 0, 0), width=1)
    # Label inside the room
    cx = x + w / 2 - len(label) * 2.5
    cy = y + h / 2 + 4
    return (cx, cy, label)


def create_initial():
    os.makedirs(DOCDIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Title Page ---
    page1 = doc.new_page(width=W, height=H)
    page1.insert_text(pymupdf.Point(120, 200), "RIVERSIDE OFFICE COMPLEX",
                      fontsize=24, fontname="hebo", color=(0, 0, 0.4))
    page1.insert_text(pymupdf.Point(160, 250), "Architectural Floor Plans",
                      fontsize=18, fontname="helv", color=(0.2, 0.2, 0.2))
    page1.insert_text(pymupdf.Point(180, 310), "Prepared by: Hartwell & Associates",
                      fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page1.insert_text(pymupdf.Point(200, 340), "Project No: ROC-2025-0412",
                      fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page1.insert_text(pymupdf.Point(215, 370), "Date: March 15, 2025",
                      fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page1.insert_text(pymupdf.Point(150, 440), "Sheet Index:",
                      fontsize=14, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(160, 465), "A-101  Ground Floor Plan",
                      fontsize=11, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(160, 485), "A-102  Second Floor Plan",
                      fontsize=11, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(160, 505), "E-201  Electrical Layout",
                      fontsize=11, fontname="helv", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(160, 525), "P-301  Plumbing Layout",
                      fontsize=11, fontname="helv", color=(0, 0, 0))

    # Title page border
    shape1 = page1.new_shape()
    shape1.draw_rect(pymupdf.Rect(36, 36, W - 36, H - 36))
    shape1.finish(color=(0, 0, 0.4), width=2)
    shape1.commit()

    # --- Page 2: Ground Floor Plan (A-101) with "Emergency Exit" label ---
    page2 = doc.new_page(width=W, height=H)
    page2.insert_text(pymupdf.Point(36, 50), "A-101  GROUND FLOOR PLAN",
                      fontsize=16, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(36, 68), "Scale: 1/4\" = 1'-0\"",
                      fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    shape2 = page2.new_shape()

    # Outer building boundary
    shape2.draw_rect(pymupdf.Rect(50, 90, 562, 700))
    shape2.finish(color=(0, 0, 0), width=2)

    # Rooms layout
    room_labels = []

    # Main Lobby
    room_labels.append(draw_room(shape2, 50, 90, 250, 150, "Main Lobby"))
    # Reception
    room_labels.append(draw_room(shape2, 300, 90, 130, 150, "Reception"))
    # Security Office
    room_labels.append(draw_room(shape2, 430, 90, 132, 150, "Security"))
    # Corridor
    room_labels.append(draw_room(shape2, 50, 240, 512, 50, "Corridor A"))
    # Conference Room A
    room_labels.append(draw_room(shape2, 50, 290, 200, 130, "Conference Room A"))
    # Office Suite 101
    room_labels.append(draw_room(shape2, 250, 290, 160, 130, "Office Suite 101"))
    # Office Suite 102
    room_labels.append(draw_room(shape2, 410, 290, 152, 130, "Office Suite 102"))
    # Corridor B
    room_labels.append(draw_room(shape2, 50, 420, 512, 50, "Corridor B"))
    # Break Room
    room_labels.append(draw_room(shape2, 50, 470, 170, 120, "Break Room"))
    # Server Room
    room_labels.append(draw_room(shape2, 220, 470, 140, 120, "Server Room"))
    # Storage
    room_labels.append(draw_room(shape2, 360, 470, 100, 120, "Storage"))

    # Emergency Exit area (right side, lower)
    room_labels.append(draw_room(shape2, 460, 470, 102, 120, ""))

    # Stairwell
    room_labels.append(draw_room(shape2, 50, 590, 120, 110, "Stairwell A"))
    # Restrooms
    room_labels.append(draw_room(shape2, 170, 590, 120, 110, "Restrooms"))
    # Mechanical
    room_labels.append(draw_room(shape2, 290, 590, 130, 110, "Mechanical"))
    # Stairwell B
    room_labels.append(draw_room(shape2, 420, 590, 142, 110, "Stairwell B"))

    shape2.commit()

    # Add room labels as text
    for cx, cy, label in room_labels:
        if label:
            page2.insert_text(pymupdf.Point(cx, cy), label,
                              fontsize=8, fontname="helv", color=(0.2, 0.2, 0.2))

    # Add the "Emergency Exit" label prominently in the right-lower room area
    page2.insert_text(pymupdf.Point(472, 520), "Emergency",
                      fontsize=11, fontname="hebo", color=(0.7, 0, 0))
    page2.insert_text(pymupdf.Point(487, 536), "Exit",
                      fontsize=11, fontname="hebo", color=(0.7, 0, 0))

    # Door indicators (small gaps in walls represented by lines)
    shape2b = page2.new_shape()
    # Main entrance door
    shape2b.draw_line(pymupdf.Point(150, 90), pymupdf.Point(190, 90))
    shape2b.finish(color=(1, 1, 1), width=4)
    shape2b.draw_line(pymupdf.Point(150, 88), pymupdf.Point(190, 88))
    shape2b.finish(color=(0, 0.5, 0), width=1)
    # Emergency exit door
    shape2b.draw_line(pymupdf.Point(562, 510), pymupdf.Point(562, 550))
    shape2b.finish(color=(1, 1, 1), width=4)
    shape2b.draw_line(pymupdf.Point(564, 510), pymupdf.Point(564, 550))
    shape2b.finish(color=(0.7, 0, 0), width=1.5)
    shape2b.commit()

    # Page 2 border
    shape2c = page2.new_shape()
    shape2c.draw_rect(pymupdf.Rect(30, 30, W - 30, H - 30))
    shape2c.finish(color=(0, 0, 0), width=1)
    shape2c.commit()

    # North arrow indicator
    page2.insert_text(pymupdf.Point(540, 760), "N",
                      fontsize=14, fontname="hebo", color=(0, 0, 0))
    shape2d = page2.new_shape()
    shape2d.draw_line(pymupdf.Point(546, 740), pymupdf.Point(546, 762))
    shape2d.finish(color=(0, 0, 0), width=1.5)
    shape2d.draw_line(pymupdf.Point(546, 740), pymupdf.Point(542, 748))
    shape2d.finish(color=(0, 0, 0), width=1.5)
    shape2d.draw_line(pymupdf.Point(546, 740), pymupdf.Point(550, 748))
    shape2d.finish(color=(0, 0, 0), width=1.5)
    shape2d.commit()

    # --- Page 3: Second Floor Plan (A-102) ---
    page3 = doc.new_page(width=W, height=H)
    page3.insert_text(pymupdf.Point(36, 50), "A-102  SECOND FLOOR PLAN",
                      fontsize=16, fontname="hebo", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(36, 68), "Scale: 1/4\" = 1'-0\"",
                      fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    shape3 = page3.new_shape()
    shape3.draw_rect(pymupdf.Rect(50, 90, 562, 700))
    shape3.finish(color=(0, 0, 0), width=2)

    room_labels3 = []
    room_labels3.append(draw_room(shape3, 50, 90, 250, 150, "Open Office Area"))
    room_labels3.append(draw_room(shape3, 300, 90, 262, 150, "Executive Suite"))
    room_labels3.append(draw_room(shape3, 50, 240, 512, 50, "Corridor C"))
    room_labels3.append(draw_room(shape3, 50, 290, 170, 130, "Meeting Room 201"))
    room_labels3.append(draw_room(shape3, 220, 290, 170, 130, "Meeting Room 202"))
    room_labels3.append(draw_room(shape3, 390, 290, 172, 130, "IT Department"))
    room_labels3.append(draw_room(shape3, 50, 420, 512, 50, "Corridor D"))
    room_labels3.append(draw_room(shape3, 50, 470, 200, 120, "Training Room"))
    room_labels3.append(draw_room(shape3, 250, 470, 160, 120, "Kitchen"))
    room_labels3.append(draw_room(shape3, 410, 470, 152, 120, "Lounge"))
    room_labels3.append(draw_room(shape3, 50, 590, 120, 110, "Stairwell A"))
    room_labels3.append(draw_room(shape3, 170, 590, 120, 110, "Restrooms"))
    room_labels3.append(draw_room(shape3, 290, 590, 130, 110, "Storage"))
    room_labels3.append(draw_room(shape3, 420, 590, 142, 110, "Stairwell B"))
    shape3.commit()

    for cx, cy, label in room_labels3:
        if label:
            page3.insert_text(pymupdf.Point(cx, cy), label,
                              fontsize=8, fontname="helv", color=(0.2, 0.2, 0.2))

    shape3b = page3.new_shape()
    shape3b.draw_rect(pymupdf.Rect(30, 30, W - 30, H - 30))
    shape3b.finish(color=(0, 0, 0), width=1)
    shape3b.commit()

    # --- Page 4: Electrical Layout (E-201) ---
    page4 = doc.new_page(width=W, height=H)
    page4.insert_text(pymupdf.Point(36, 50), "E-201  ELECTRICAL LAYOUT",
                      fontsize=16, fontname="hebo", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(36, 68), "Scale: 1/4\" = 1'-0\"",
                      fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    shape4 = page4.new_shape()
    shape4.draw_rect(pymupdf.Rect(50, 90, 562, 700))
    shape4.finish(color=(0, 0, 0), width=2)

    # Electrical symbols - outlets
    for x in [100, 200, 300, 400, 500]:
        for y in [150, 300, 450, 600]:
            shape4.draw_circle(pymupdf.Point(x, y), 5)
            shape4.finish(color=(0, 0, 0.7), width=1)

    # Wiring runs
    shape4.draw_line(pymupdf.Point(100, 150), pymupdf.Point(500, 150))
    shape4.finish(color=(0, 0, 0.7), width=0.5, dashes="[4 2]")
    shape4.draw_line(pymupdf.Point(100, 300), pymupdf.Point(500, 300))
    shape4.finish(color=(0, 0, 0.7), width=0.5, dashes="[4 2]")
    shape4.draw_line(pymupdf.Point(100, 450), pymupdf.Point(500, 450))
    shape4.finish(color=(0, 0, 0.7), width=0.5, dashes="[4 2]")
    shape4.draw_line(pymupdf.Point(100, 600), pymupdf.Point(500, 600))
    shape4.finish(color=(0, 0, 0.7), width=0.5, dashes="[4 2]")

    # Main panel
    shape4.draw_rect(pymupdf.Rect(80, 650, 160, 690))
    shape4.finish(color=(0, 0, 0.7), fill=(0.85, 0.85, 1), width=1.5)
    shape4.commit()

    page4.insert_text(pymupdf.Point(85, 675), "Main Panel",
                      fontsize=8, fontname="helv", color=(0, 0, 0.7))

    # Legend
    page4.insert_text(pymupdf.Point(380, 660), "LEGEND:",
                      fontsize=9, fontname="hebo", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(380, 675), "O = Outlet   --- = Wiring Run",
                      fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))

    shape4b = page4.new_shape()
    shape4b.draw_rect(pymupdf.Rect(30, 30, W - 30, H - 30))
    shape4b.finish(color=(0, 0, 0), width=1)
    shape4b.commit()

    # --- Page 5: Plumbing Layout (P-301) ---
    page5 = doc.new_page(width=W, height=H)
    page5.insert_text(pymupdf.Point(36, 50), "P-301  PLUMBING LAYOUT",
                      fontsize=16, fontname="hebo", color=(0, 0, 0))
    page5.insert_text(pymupdf.Point(36, 68), "Scale: 1/4\" = 1'-0\"",
                      fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    shape5 = page5.new_shape()
    shape5.draw_rect(pymupdf.Rect(50, 90, 562, 700))
    shape5.finish(color=(0, 0, 0), width=2)

    # Water supply lines (blue)
    shape5.draw_line(pymupdf.Point(100, 120), pymupdf.Point(100, 680))
    shape5.finish(color=(0, 0, 0.8), width=1.5)
    shape5.draw_line(pymupdf.Point(100, 200), pymupdf.Point(400, 200))
    shape5.finish(color=(0, 0, 0.8), width=1.5)
    shape5.draw_line(pymupdf.Point(100, 400), pymupdf.Point(400, 400))
    shape5.finish(color=(0, 0, 0.8), width=1.5)
    shape5.draw_line(pymupdf.Point(100, 600), pymupdf.Point(400, 600))
    shape5.finish(color=(0, 0, 0.8), width=1.5)

    # Drain lines (green)
    shape5.draw_line(pymupdf.Point(500, 120), pymupdf.Point(500, 680))
    shape5.finish(color=(0, 0.5, 0), width=1.5)
    shape5.draw_line(pymupdf.Point(400, 200), pymupdf.Point(500, 200))
    shape5.finish(color=(0, 0.5, 0), width=1.5)
    shape5.draw_line(pymupdf.Point(400, 400), pymupdf.Point(500, 400))
    shape5.finish(color=(0, 0.5, 0), width=1.5)
    shape5.draw_line(pymupdf.Point(400, 600), pymupdf.Point(500, 600))
    shape5.finish(color=(0, 0.5, 0), width=1.5)

    # Fixtures
    for y in [200, 400, 600]:
        shape5.draw_rect(pymupdf.Rect(380, y - 10, 420, y + 10))
        shape5.finish(color=(0.3, 0.3, 0.3), fill=(0.9, 0.9, 0.9), width=1)

    shape5.commit()

    # Legend
    page5.insert_text(pymupdf.Point(380, 660), "LEGEND:",
                      fontsize=9, fontname="hebo", color=(0, 0, 0))
    page5.insert_text(pymupdf.Point(380, 675), "Blue = Supply   Green = Drain",
                      fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))

    shape5b = page5.new_shape()
    shape5b.draw_rect(pymupdf.Rect(30, 30, W - 30, H - 30))
    shape5b.finish(color=(0, 0, 0), width=1)
    shape5b.commit()

    # Save
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready: open in Evince at page 2
    launch_gui(f'evince --page-index=2 "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
