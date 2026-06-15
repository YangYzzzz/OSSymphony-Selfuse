"""
Initial Setup: Create a multi-page PDF with mixed page sizes
Task ID: pdf_mbc_025
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_025'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/mixed_sizes.pdf'


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page 1: Letter (612x792)
    page1 = doc.new_page(width=612, height=792)
    page1.insert_text(
        pymupdf.Point(72, 60),
        "Greenfield Analytics - Monthly Performance Summary",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.15, 0.35),
    )
    page1.insert_text(
        pymupdf.Point(72, 90),
        "Prepared by: Rachel Kim, Senior Data Analyst",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(72, 110),
        "Date: March 15, 2025",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    rect1 = pymupdf.Rect(72, 140, 540, 400)
    page1.insert_textbox(
        rect1,
        "This document compiles the key performance indicators across our regional "
        "offices for the month of February 2025. Revenue across all divisions increased "
        "by 8.3% compared to the same period last year, driven primarily by strong demand "
        "in the enterprise software segment. The Western region posted the highest growth "
        "at 12.1%, while the Southern region experienced a modest decline of 1.7% due to "
        "ongoing supply chain disruptions.\n\n"
        "Customer acquisition costs remained stable at $47.20 per lead, with conversion "
        "rates improving from 3.8% to 4.5% following the launch of the redesigned onboarding "
        "workflow. Net Promoter Score rose to 72, up from 68 in January, reflecting improved "
        "customer satisfaction with our support response times.\n\n"
        "The detailed breakdowns by region, product line, and channel follow in the "
        "subsequent pages of this report.",
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 2: A4 (595x842)
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text(
        pymupdf.Point(60, 55),
        "Regional Revenue Breakdown - Q1 2025",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.15, 0.35),
    )
    # Draw a simple table header
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(60, 85), pymupdf.Point(535, 85))
    shape2.finish(color=(0.1, 0.15, 0.35), width=1.5)
    shape2.commit()

    headers = ["Region", "Jan ($K)", "Feb ($K)", "Mar ($K)", "Total ($K)"]
    x_positions = [60, 160, 250, 340, 430]
    for i, h in enumerate(headers):
        page2.insert_text(
            pymupdf.Point(x_positions[i], 102),
            h,
            fontsize=10,
            fontname="hebo",
            color=(0.1, 0.15, 0.35),
        )

    data_rows = [
        ["Northeast", "1,245", "1,310", "1,402", "3,957"],
        ["Southeast", "892", "878", "901", "2,671"],
        ["Midwest", "1,067", "1,125", "1,198", "3,390"],
        ["West Coast", "1,523", "1,640", "1,707", "4,870"],
        ["Southwest", "734", "752", "789", "2,275"],
        ["Pacific NW", "456", "481", "512", "1,449"],
    ]
    y = 122
    for row in data_rows:
        for i, val in enumerate(row):
            page2.insert_text(
                pymupdf.Point(x_positions[i], y),
                val,
                fontsize=10,
                fontname="helv",
                color=(0, 0, 0),
            )
        y += 18

    rect2 = pymupdf.Rect(60, y + 20, 535, y + 120)
    page2.insert_textbox(
        rect2,
        "The West Coast region continues to lead in absolute revenue generation, "
        "accounting for 26.2% of the company's total domestic revenue. The Pacific "
        "Northwest saw the highest month-over-month growth rate at 6.4%, indicating "
        "strong momentum from the new Portland and Seattle office expansions.",
        fontsize=10,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page 3: Legal (612x1008)
    page3 = doc.new_page(width=612, height=1008)
    page3.insert_text(
        pymupdf.Point(72, 60),
        "Product Line Performance Detail",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.15, 0.35),
    )
    products = [
        ("Enterprise Suite Pro", "$2.4M", "+12.1%", "Our flagship product maintained strong growth driven by new enterprise contracts with Meridian Health Systems and Oakridge Financial Group."),
        ("CloudSync Platform", "$1.8M", "+8.7%", "Migration services revenue increased as mid-market companies accelerated their cloud transitions. Average deal size grew to $45K."),
        ("DataVault Analytics", "$1.1M", "+15.3%", "Fastest-growing product line. The release of real-time dashboards in v3.2 attracted 47 new customers in Q1 alone."),
        ("SecureConnect VPN", "$680K", "-2.1%", "Slight decline attributed to increased competition from bundled solutions. Product team is preparing a major feature update for Q2."),
        ("MobileFirst SDK", "$420K", "+6.8%", "Developer adoption continues to climb with 1,200 new API keys issued. Partnership with TechReady Bootcamp drove awareness."),
    ]
    y = 90
    for name, rev, growth, desc in products:
        page3.insert_text(
            pymupdf.Point(72, y),
            f"{name}  |  Revenue: {rev}  |  YoY Growth: {growth}",
            fontsize=11,
            fontname="hebo",
            color=(0.15, 0.15, 0.15),
        )
        y += 18
        rect_p = pymupdf.Rect(72, y, 540, y + 60)
        page3.insert_textbox(
            rect_p,
            desc,
            fontsize=10,
            fontname="helv",
            color=(0.25, 0.25, 0.25),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )
        y += 70

    page3.insert_text(
        pymupdf.Point(72, y + 20),
        "Appendix: Detailed financial reconciliation and audit notes are available in the "
        "companion spreadsheet (Q1_2025_Financials.xlsx) shared via the internal portal.",
        fontsize=10,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )

    # Page 4: Letter landscape (792x612)
    page4 = doc.new_page(width=792, height=612)
    page4.insert_text(
        pymupdf.Point(72, 55),
        "Customer Acquisition Funnel - February 2025",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.15, 0.35),
    )

    # Draw funnel-like bars
    shape4 = page4.new_shape()
    stages = [
        ("Website Visitors", "42,380", 600, (0.2, 0.4, 0.7)),
        ("Lead Captures", "8,476", 480, (0.3, 0.5, 0.8)),
        ("Qualified Leads", "3,390", 360, (0.4, 0.6, 0.85)),
        ("Demos Scheduled", "1,017", 240, (0.5, 0.7, 0.9)),
        ("Proposals Sent", "381", 160, (0.6, 0.75, 0.92)),
        ("Closed Won", "152", 100, (0.15, 0.55, 0.3)),
    ]
    y = 90
    for label, count, bar_w, color in stages:
        x_start = (720 - bar_w) / 2
        rect_bar = pymupdf.Rect(x_start, y, x_start + bar_w, y + 30)
        shape4.draw_rect(rect_bar)
        shape4.finish(color=color, fill=color, width=0)
        page4.insert_text(
            pymupdf.Point(x_start + 10, y + 20),
            f"{label}: {count}",
            fontsize=10,
            fontname="hebo",
            color=(1, 1, 1),
        )
        y += 45

    shape4.commit()

    page4.insert_text(
        pymupdf.Point(72, y + 30),
        "Conversion Rate: 0.36%  |  CAC: $47.20  |  LTV:CAC Ratio: 4.8x",
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Make sure page_dimensions.txt does NOT exist (task output)
    txt_path = f'{DOCS_DIR}/page_dimensions.txt'
    if os.path.exists(txt_path):
        os.remove(txt_path)

    # Open PDF in evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
