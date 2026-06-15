"""
Initial Setup: Create an ODT document without version-on-close enabled.
Task ID: writer_lec_081
Domain: libreoffice_writer

Creates a realistic Writer document (.odt) with content but without
the 'Always save a version on close' setting enabled.
"""

import os
import shlex
import subprocess
import time
import zipfile
import tempfile
import shutil
from odf.opendocument import OpenDocumentText
from odf.text import P, H, Span, List, ListItem
from odf.style import (
    Style, TextProperties, ParagraphProperties, ListLevelProperties
)

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_081'
OUTPUT = f'{WORKDIR}/{TASK_ID}.odt'


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
    doc = OpenDocumentText()

    # --- Define styles ---
    # Title style
    title_style = Style(name="DocTitle", family="paragraph")
    title_style.addElement(TextProperties(
        fontsize="18pt", fontweight="bold", color="#1a3c5e"
    ))
    title_style.addElement(ParagraphProperties(
        textalign="center", marginbottom="0.3in"
    ))
    doc.automaticstyles.addElement(title_style)

    # Heading style
    heading_style = Style(name="SectionHead", family="paragraph")
    heading_style.addElement(TextProperties(
        fontsize="14pt", fontweight="bold", color="#2d5f8a"
    ))
    heading_style.addElement(ParagraphProperties(
        margintop="0.2in", marginbottom="0.1in"
    ))
    doc.automaticstyles.addElement(heading_style)

    # Body style
    body_style = Style(name="BodyText", family="paragraph")
    body_style.addElement(TextProperties(fontsize="11pt"))
    body_style.addElement(ParagraphProperties(
        marginbottom="0.08in", textalign="justify"
    ))
    doc.automaticstyles.addElement(body_style)

    # Bold inline style
    bold_style = Style(name="BoldInline", family="text")
    bold_style.addElement(TextProperties(fontweight="bold"))
    doc.automaticstyles.addElement(bold_style)

    # --- Title ---
    p_title = P(stylename=title_style)
    p_title.addText("Quarterly Marketing Strategy Report")
    doc.text.addElement(p_title)

    p_subtitle = P(stylename=body_style)
    p_subtitle.addText("Prepared by: Elena Rodriguez, Marketing Director")
    doc.text.addElement(p_subtitle)

    p_date = P(stylename=body_style)
    p_date.addText("Date: March 28, 2026")
    doc.text.addElement(p_date)

    # Blank line
    doc.text.addElement(P())

    # --- Section 1: Executive Summary ---
    h1 = P(stylename=heading_style)
    h1.addText("1. Executive Summary")
    doc.text.addElement(h1)

    p1 = P(stylename=body_style)
    p1.addText(
        "This report outlines the marketing strategy for Q2 2026, focusing on "
        "digital channel expansion and customer retention initiatives. Our analysis "
        "of Q1 performance indicates a 12% increase in brand awareness metrics "
        "and a 7.3% improvement in customer acquisition cost (CAC) compared to "
        "the previous quarter."
    )
    doc.text.addElement(p1)

    p2 = P(stylename=body_style)
    p2.addText(
        "Key highlights include the successful launch of our social media campaign "
        "across three new platforms, resulting in 45,000 new followers and a 15% "
        "increase in engagement rates. The email marketing program delivered an "
        "average open rate of 24.8%, exceeding the industry benchmark of 21.3%."
    )
    doc.text.addElement(p2)

    # --- Section 2: Budget Overview ---
    h2 = P(stylename=heading_style)
    h2.addText("2. Budget Overview")
    doc.text.addElement(h2)

    p3 = P(stylename=body_style)
    p3.addText(
        "The total marketing budget for Q2 2026 is allocated at $487,500, "
        "representing a 5% increase from Q1. The distribution across channels "
        "reflects our strategic shift toward digital-first engagement:"
    )
    doc.text.addElement(p3)

    budget_items = [
        "Digital Advertising (Google, Meta, LinkedIn): $175,000 (35.9%)",
        "Content Marketing and SEO: $92,500 (19.0%)",
        "Email Campaigns and Automation: $58,200 (11.9%)",
        "Event Sponsorships and Webinars: $72,800 (14.9%)",
        "Market Research and Analytics: $48,000 (9.8%)",
        "Creative Services and Design: $41,000 (8.4%)",
    ]
    for item in budget_items:
        bp = P(stylename=body_style)
        bp.addText(f"  \u2022  {item}")
        doc.text.addElement(bp)

    # --- Section 3: Target Audience ---
    h3 = P(stylename=heading_style)
    h3.addText("3. Target Audience Segmentation")
    doc.text.addElement(h3)

    p4 = P(stylename=body_style)
    p4.addText(
        "Our revised audience segmentation identifies four primary cohorts "
        "based on purchasing behavior, demographic analysis, and digital "
        "engagement patterns collected during the past two quarters:"
    )
    doc.text.addElement(p4)

    segments = [
        ("Tech Professionals (25-40)", "High digital engagement, preference for "
         "webinar content and LinkedIn outreach. Average deal value: $12,400."),
        ("Small Business Owners (30-55)", "Value-driven, responsive to case studies "
         "and ROI-focused messaging. Average deal value: $8,750."),
        ("Enterprise Decision Makers (35-55)", "Require multi-touch campaigns with "
         "white papers and industry reports. Average deal value: $45,200."),
        ("Startup Founders (22-40)", "Early adopters, active on Twitter/X and "
         "Product Hunt. Average deal value: $5,800."),
    ]
    for name, desc in segments:
        sp = P(stylename=body_style)
        bold_span = Span(stylename=bold_style)
        bold_span.addText(name)
        sp.addElement(bold_span)
        sp.addText(f" \u2014 {desc}")
        doc.text.addElement(sp)

    # --- Section 4: Campaign Timeline ---
    h4 = P(stylename=heading_style)
    h4.addText("4. Campaign Timeline")
    doc.text.addElement(h4)

    p5 = P(stylename=body_style)
    p5.addText(
        "The Q2 campaign schedule is organized into three phases to maximize "
        "impact while maintaining consistent brand messaging across all channels."
    )
    doc.text.addElement(p5)

    phases = [
        ("Phase 1 (April 1-30): Awareness", "Launch refreshed brand assets, "
         "begin paid social campaigns, publish three thought leadership articles."),
        ("Phase 2 (May 1-31): Engagement", "Host two webinars, activate email "
         "nurture sequences, launch interactive product demos on website."),
        ("Phase 3 (June 1-30): Conversion", "Deploy retargeting campaigns, "
         "offer limited-time promotions, conduct personalized outreach to "
         "high-intent leads identified in Phases 1 and 2."),
    ]
    for phase_name, phase_desc in phases:
        pp = P(stylename=body_style)
        bold_span = Span(stylename=bold_style)
        bold_span.addText(phase_name)
        pp.addElement(bold_span)
        pp.addText(f" \u2014 {phase_desc}")
        doc.text.addElement(pp)

    # --- Section 5: KPIs ---
    h5 = P(stylename=heading_style)
    h5.addText("5. Key Performance Indicators")
    doc.text.addElement(h5)

    p6 = P(stylename=body_style)
    p6.addText(
        "Progress will be measured against the following KPIs, with monthly "
        "reviews scheduled for the last Friday of each month:"
    )
    doc.text.addElement(p6)

    kpis = [
        "Website traffic growth: target 20% increase quarter-over-quarter",
        "Marketing Qualified Leads (MQLs): target 850 per month",
        "Customer Acquisition Cost: target reduction to $128 per customer",
        "Email open rate: maintain above 23%",
        "Social media engagement rate: target 4.5% across platforms",
        "Content downloads: target 2,400 white paper downloads",
    ]
    for kpi in kpis:
        kp = P(stylename=body_style)
        kp.addText(f"  \u2022  {kpi}")
        doc.text.addElement(kp)

    # --- Save the document ---
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # --- Open in LibreOffice Writer ---
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
