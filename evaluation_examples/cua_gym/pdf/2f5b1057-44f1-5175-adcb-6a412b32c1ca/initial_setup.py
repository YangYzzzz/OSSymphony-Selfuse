"""
Initial Setup: Create two landscape-oriented PDF pages with chart data
Task ID: pdf_ro_044
Domain: pdf

Creates:
  /home/user/Documents/left.pdf  — single-page landscape PDF with a bar chart
  /home/user/Documents/right.pdf — single-page landscape PDF with a line chart
Does NOT create combined.pdf (that is the agent's task).
"""

import os
import shlex
import subprocess
import time
import pymupdf  # PyMuPDF

WORKDIR = '/home/user'
DOCS_DIR = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_ro_044'

LEFT_PDF = f'{DOCS_DIR}/left.pdf'
RIGHT_PDF = f'{DOCS_DIR}/right.pdf'

# Landscape dimensions: 792 x 612 points (11" x 8.5")
LANDSCAPE_W = 792
LANDSCAPE_H = 612


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


def draw_bar_chart(page, title, labels, values, color):
    """Draw a simple bar chart on the page."""
    shape = page.new_shape()

    # Title
    page.insert_text(
        pymupdf.Point(LANDSCAPE_W / 2 - 120, 50),
        title,
        fontsize=22,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    # Chart area
    chart_left = 100
    chart_bottom = 520
    chart_top = 100
    chart_right = 700
    bar_width = 60
    gap = 30
    max_val = max(values)

    # Y-axis
    shape.draw_line(pymupdf.Point(chart_left, chart_top), pymupdf.Point(chart_left, chart_bottom))
    shape.finish(color=(0.3, 0.3, 0.3), width=1.5)

    # X-axis
    shape.draw_line(pymupdf.Point(chart_left, chart_bottom), pymupdf.Point(chart_right, chart_bottom))
    shape.finish(color=(0.3, 0.3, 0.3), width=1.5)

    # Gridlines
    for i in range(1, 6):
        y = chart_bottom - (chart_bottom - chart_top) * i / 5
        shape.draw_line(pymupdf.Point(chart_left, y), pymupdf.Point(chart_right, y))
        shape.finish(color=(0.85, 0.85, 0.85), width=0.5)
        # Y-axis labels
        page.insert_text(
            pymupdf.Point(chart_left - 45, y + 5),
            f"${int(max_val * i / 5):,}",
            fontsize=9,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

    # Bars
    total_bar_area = len(values) * (bar_width + gap) - gap
    start_x = chart_left + (chart_right - chart_left - total_bar_area) / 2

    for i, (label, val) in enumerate(zip(labels, values)):
        x = start_x + i * (bar_width + gap)
        bar_height = (val / max_val) * (chart_bottom - chart_top)
        y_top = chart_bottom - bar_height

        rect = pymupdf.Rect(x, y_top, x + bar_width, chart_bottom)
        shape.draw_rect(rect)
        shape.finish(color=color, fill=color, width=0)

        # Label below bar
        page.insert_text(
            pymupdf.Point(x + 5, chart_bottom + 18),
            label,
            fontsize=9,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
        )

        # Value on top of bar
        page.insert_text(
            pymupdf.Point(x + 5, y_top - 8),
            f"${val:,.0f}",
            fontsize=8,
            fontname="hebo",
            color=(0.2, 0.2, 0.2),
        )

    shape.commit()

    # Footer
    page.insert_text(
        pymupdf.Point(chart_left, chart_bottom + 55),
        "Source: Annual Financial Report FY2025 — Westbridge Analytics Group",
        fontsize=8,
        fontname="tiit",
        color=(0.5, 0.5, 0.5),
    )


def draw_line_chart(page, title, months, series):
    """Draw a simple line chart on the page."""
    shape = page.new_shape()

    # Title
    page.insert_text(
        pymupdf.Point(LANDSCAPE_W / 2 - 150, 50),
        title,
        fontsize=22,
        fontname="hebo",
        color=(0.1, 0.3, 0.1),
    )

    # Chart area
    chart_left = 100
    chart_bottom = 500
    chart_top = 100
    chart_right = 700
    max_val = max(max(s["values"]) for s in series)
    min_val = 0

    # Axes
    shape.draw_line(pymupdf.Point(chart_left, chart_top), pymupdf.Point(chart_left, chart_bottom))
    shape.finish(color=(0.3, 0.3, 0.3), width=1.5)
    shape.draw_line(pymupdf.Point(chart_left, chart_bottom), pymupdf.Point(chart_right, chart_bottom))
    shape.finish(color=(0.3, 0.3, 0.3), width=1.5)

    # Gridlines
    for i in range(1, 6):
        y = chart_bottom - (chart_bottom - chart_top) * i / 5
        shape.draw_line(pymupdf.Point(chart_left, y), pymupdf.Point(chart_right, y))
        shape.finish(color=(0.85, 0.85, 0.85), width=0.5)
        page.insert_text(
            pymupdf.Point(chart_left - 40, y + 5),
            f"{int(max_val * i / 5):,}",
            fontsize=9,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

    # X-axis labels
    n_months = len(months)
    x_step = (chart_right - chart_left) / (n_months - 1)
    for i, m in enumerate(months):
        x = chart_left + i * x_step
        page.insert_text(
            pymupdf.Point(x - 10, chart_bottom + 18),
            m,
            fontsize=9,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
        )

    # Data lines
    for s in series:
        vals = s["values"]
        color = s["color"]
        points = []
        for i, v in enumerate(vals):
            x = chart_left + i * x_step
            y = chart_bottom - (v / max_val) * (chart_bottom - chart_top)
            points.append(pymupdf.Point(x, y))

        for j in range(len(points) - 1):
            shape.draw_line(points[j], points[j + 1])
            shape.finish(color=color, width=2.0)

        # Data point circles
        for p in points:
            shape.draw_circle(p, 3)
            shape.finish(color=color, fill=color, width=0)

    shape.commit()

    # Legend
    legend_y = chart_bottom + 45
    legend_x = chart_left
    for s in series:
        rect = pymupdf.Rect(legend_x, legend_y - 6, legend_x + 12, legend_y + 2)
        sh2 = page.new_shape()
        sh2.draw_rect(rect)
        sh2.finish(color=s["color"], fill=s["color"], width=0)
        sh2.commit()
        page.insert_text(
            pymupdf.Point(legend_x + 16, legend_y + 2),
            s["name"],
            fontsize=9,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
        )
        legend_x += 140

    # Footer
    page.insert_text(
        pymupdf.Point(chart_left, chart_bottom + 75),
        "Source: Regional Performance Dashboard — Meridian Consulting Partners",
        fontsize=8,
        fontname="tiit",
        color=(0.5, 0.5, 0.5),
    )


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    # --- left.pdf: Bar chart of quarterly revenue by department ---
    doc_left = pymupdf.open()
    page_left = doc_left.new_page(width=LANDSCAPE_W, height=LANDSCAPE_H)

    departments = ["Engineering", "Sales", "Marketing", "Operations", "Support"]
    revenues = [425000, 387000, 298000, 210000, 165000]
    draw_bar_chart(
        page_left,
        "Q4 2025 Revenue by Department",
        departments,
        revenues,
        color=(0.2, 0.4, 0.75),
    )

    doc_left.save(LEFT_PDF)
    doc_left.close()
    print(f'Created: {LEFT_PDF}')

    # --- right.pdf: Line chart of monthly active users ---
    doc_right = pymupdf.open()
    page_right = doc_right.new_page(width=LANDSCAPE_W, height=LANDSCAPE_H)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    series_data = [
        {
            "name": "North America",
            "values": [1200, 1350, 1500, 1480, 1620, 1750, 1900, 2050, 2100, 2250, 2380, 2500],
            "color": (0.2, 0.55, 0.2),
        },
        {
            "name": "Europe",
            "values": [800, 850, 920, 980, 1050, 1100, 1180, 1250, 1300, 1380, 1420, 1500],
            "color": (0.75, 0.3, 0.15),
        },
        {
            "name": "Asia-Pacific",
            "values": [600, 700, 780, 850, 950, 1020, 1150, 1280, 1400, 1520, 1650, 1800],
            "color": (0.5, 0.2, 0.6),
        },
    ]
    draw_line_chart(page_right, "Monthly Active Users by Region — 2025", months, series_data)

    doc_right.save(RIGHT_PDF)
    doc_right.close()
    print(f'Created: {RIGHT_PDF}')

    # Open the files in Evince for the agent
    launch_gui(f'evince "{LEFT_PDF}"', delay_sec=1.5)
    launch_gui(f'evince "{RIGHT_PDF}"', delay_sec=1.5)
    print('GUI_READY: launched Evince with left.pdf and right.pdf on DISPLAY=:0')


create_initial()
