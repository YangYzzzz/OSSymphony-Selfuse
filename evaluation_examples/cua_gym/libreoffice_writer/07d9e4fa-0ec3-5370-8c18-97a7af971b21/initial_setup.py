"""
Initial Setup: Writer document with Chapter 3 content in single-column layout (no named sections).
Task ID: writer_fs_077
Domain: libreoffice_writer

The document contains Chapter 3 with two subsections of realistic text,
all in a plain single-column layout. No named sections are defined --
that is the task for the agent to create.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_077'
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
    # Install odfpy if needed
    subprocess.run(['pip3', 'install', 'odfpy'], capture_output=True)

    from odf.opendocument import OpenDocumentText
    from odf.text import P, H
    from odf.style import Style, TextProperties, ParagraphProperties

    doc = OpenDocumentText()

    # --- Define styles ---
    # Heading 1 style for Chapter title
    h1_style = Style(name='ChapterHeading', family='paragraph')
    h1_style.addElement(TextProperties(fontsize='18pt', fontweight='bold', color='#1a3c5e'))
    h1_style.addElement(ParagraphProperties(marginbottom='0.3cm'))
    doc.automaticstyles.addElement(h1_style)

    # Heading 2 style for subsection titles
    h2_style = Style(name='SubsectionHeading', family='paragraph')
    h2_style.addElement(TextProperties(fontsize='14pt', fontweight='bold', color='#2e5984'))
    h2_style.addElement(ParagraphProperties(margintop='0.4cm', marginbottom='0.2cm'))
    doc.automaticstyles.addElement(h2_style)

    # Body text style
    body_style = Style(name='BodyText', family='paragraph')
    body_style.addElement(TextProperties(fontsize='11pt'))
    body_style.addElement(ParagraphProperties(marginbottom='0.2cm', textalign='justify'))
    doc.automaticstyles.addElement(body_style)

    # --- Chapter 3 heading ---
    doc.text.addElement(H(outlinelevel='1', stylename=h1_style, text='Chapter 3: Market Analysis and Strategic Positioning'))

    # --- Subsection 3A: Market Overview ---
    doc.text.addElement(H(outlinelevel='2', stylename=h2_style, text='3.A  Market Overview and Competitive Landscape'))

    doc.text.addElement(P(stylename=body_style, text=(
        'The global enterprise software market reached $685 billion in 2025, '
        'driven by accelerating digital transformation across industries. '
        'Key players including Meridian Technologies, Apex Solutions Group, '
        'and NovaStar Systems continue to dominate the cloud infrastructure '
        'segment, collectively holding approximately 62% of market share.'
    )))

    doc.text.addElement(P(stylename=body_style, text=(
        'Regional analysis reveals significant growth in Asia-Pacific markets, '
        'particularly in Singapore, South Korea, and Japan. The APAC region '
        'recorded a compound annual growth rate of 14.3% between 2022 and 2025, '
        'outpacing both North American (8.7%) and European (7.1%) markets. '
        'Emerging segments such as AI-driven analytics and edge computing '
        'contributed disproportionately to this growth trajectory.'
    )))

    doc.text.addElement(P(stylename=body_style, text=(
        'Customer acquisition costs in the mid-market segment averaged $18,400 '
        'per account during Q3 2025, representing a 12% decrease from the '
        'previous fiscal year. This improvement is attributed to enhanced '
        'inbound marketing strategies and the introduction of self-service '
        'onboarding platforms by several leading vendors.'
    )))

    doc.text.addElement(P(stylename=body_style, text=(
        'Industry analysts at Forrester and Gartner project continued '
        'consolidation among mid-tier providers, with an estimated 15 to 20 '
        'mergers and acquisitions expected in the next 18 months. Strategic '
        'partnerships between cloud-native startups and established enterprise '
        'vendors are reshaping competitive dynamics across all major verticals.'
    )))

    # --- Subsection 3B: Strategic Positioning ---
    doc.text.addElement(H(outlinelevel='2', stylename=h2_style, text='3.B  Strategic Positioning and Growth Roadmap'))

    doc.text.addElement(P(stylename=body_style, text=(
        'Our strategic positioning framework centers on three pillars: '
        'technological differentiation through proprietary machine learning '
        'models, geographic expansion into underserved markets, and deepening '
        'customer engagement via integrated service offerings. Each pillar '
        'is supported by measurable key performance indicators and quarterly '
        'review milestones established by the executive leadership team.'
    )))

    doc.text.addElement(P(stylename=body_style, text=(
        'The product roadmap for fiscal year 2026 prioritizes the launch of '
        'DataStream Pro, an advanced real-time analytics platform targeting '
        'financial services and healthcare verticals. Beta testing with '
        'twelve enterprise clients, including Hargrove Financial and Pinnacle '
        'Health Systems, yielded a net promoter score of 74, significantly '
        'above the industry benchmark of 51.'
    )))

    doc.text.addElement(P(stylename=body_style, text=(
        'Revenue diversification remains a priority. Subscription-based '
        'recurring revenue currently accounts for 71% of total revenue, '
        'with professional services and training contributing the remaining '
        '29%. The target for 2026 is to shift the ratio to 78/22 by '
        'converting existing on-premise clients to cloud subscriptions and '
        'expanding the self-service support portal.'
    )))

    doc.text.addElement(P(stylename=body_style, text=(
        'Talent acquisition and retention efforts focus on expanding the '
        'engineering team by 35% to support product development timelines. '
        'Partnerships with three leading universities \u2014 Caltech, ETH Z\u00fcrich, '
        'and Tsinghua University \u2014 provide a pipeline of specialized talent '
        'in distributed systems and applied machine learning.'
    )))

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Launch in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
