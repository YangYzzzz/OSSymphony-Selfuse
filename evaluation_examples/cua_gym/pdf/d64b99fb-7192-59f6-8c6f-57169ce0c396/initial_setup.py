"""
Initial Setup: Create a 20-page presentation slides PDF
Task ID: pdf_res_085
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_085'
PAPERS_DIR = f'{WORKDIR}/papers'
PDF_PATH = f'{PAPERS_DIR}/presentation_slides.pdf'


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
    os.makedirs(PAPERS_DIR, exist_ok=True)

    # Ensure /home/user/papers/slides/ does NOT exist
    slides_dir = f'{PAPERS_DIR}/slides'
    if os.path.exists(slides_dir):
        import shutil
        shutil.rmtree(slides_dir)

    doc = pymupdf.open()

    # Slide dimensions: 16:9 widescreen (10" x 5.625" at 72 dpi)
    SLIDE_W = 720
    SLIDE_H = 405

    # Presentation content for 20 slides
    slides_content = [
        {
            "title": "Q4 2025 Strategic Review",
            "subtitle": "Presented by Elena Rodriguez, Chief Strategy Officer",
            "bg_color": (0.12, 0.18, 0.33),
            "title_color": (1, 1, 1),
        },
        {
            "title": "Agenda",
            "bullets": [
                "1. Market Performance Overview",
                "2. Revenue & Growth Metrics",
                "3. Product Launch Outcomes",
                "4. Customer Acquisition Analysis",
                "5. Competitive Landscape",
                "6. Q1 2026 Projections",
            ],
            "bg_color": (1, 1, 1),
            "title_color": (0.12, 0.18, 0.33),
        },
        {
            "title": "Market Performance Summary",
            "bullets": [
                "Total addressable market grew 14.2% YoY to $8.7B",
                "Company market share increased from 12.3% to 15.1%",
                "Three new geographic markets entered: Brazil, Poland, Vietnam",
                "Customer NPS rose from 42 to 58 in Q4",
            ],
            "bg_color": (0.95, 0.95, 0.97),
            "title_color": (0.12, 0.18, 0.33),
        },
        {
            "title": "Revenue Breakdown by Segment",
            "bullets": [
                "Enterprise: $124.5M (+22% QoQ)",
                "Mid-Market: $67.3M (+15% QoQ)",
                "SMB: $41.8M (+8% QoQ)",
                "Government: $18.9M (+31% QoQ)",
                "Total Q4 Revenue: $252.5M",
            ],
            "bg_color": (1, 1, 1),
            "title_color": (0.12, 0.18, 0.33),
        },
        {
            "title": "Product Launch: Atlas Platform v3.0",
            "bullets": [
                "Launched October 15, 2025 to 2,400+ enterprise clients",
                "Adoption rate: 78% within first 60 days",
                "Average onboarding time reduced from 14 to 3 days",
                "Support ticket volume decreased 42% post-launch",
                "Featured in Gartner Magic Quadrant as Leader",
            ],
            "bg_color": (0.95, 0.97, 0.95),
            "title_color": (0.1, 0.35, 0.1),
        },
        {
            "title": "Customer Acquisition Funnel",
            "bullets": [
                "Website visitors: 4.2M (+18% QoQ)",
                "Trial signups: 128,000 (+25% QoQ)",
                "Qualified leads: 34,500 (+20% QoQ)",
                "Closed deals: 8,750 (+17% QoQ)",
                "Overall conversion rate: 6.8% (up from 5.9%)",
            ],
            "bg_color": (1, 1, 1),
            "title_color": (0.12, 0.18, 0.33),
        },
        {
            "title": "Regional Performance",
            "bullets": [
                "North America: $168.2M (67% of total)",
                "Europe: $48.7M (19% of total)",
                "Asia-Pacific: $28.4M (11% of total)",
                "Latin America: $7.2M (3% of total)",
                "EMEA growth rate leads at 34% YoY",
            ],
            "bg_color": (0.97, 0.95, 0.95),
            "title_color": (0.35, 0.1, 0.1),
        },
        {
            "title": "Engineering & Infrastructure",
            "bullets": [
                "99.97% platform uptime achieved in Q4",
                "Average API response time: 47ms (down from 82ms)",
                "Deployed 342 production releases",
                "Technical debt reduced by 28%",
                "SOC 2 Type II and ISO 27001 certifications renewed",
            ],
            "bg_color": (1, 1, 1),
            "title_color": (0.12, 0.18, 0.33),
        },
        {
            "title": "Talent & Organization",
            "bullets": [
                "Headcount grew from 1,840 to 2,150 (+17%)",
                "Engineering team: 680 (32% of company)",
                "Employee retention rate: 91%",
                "Diversity hiring: 48% from underrepresented groups",
                "Launched internal leadership academy with 120 participants",
            ],
            "bg_color": (0.95, 0.95, 0.97),
            "title_color": (0.12, 0.18, 0.33),
        },
        {
            "title": "Competitive Landscape Analysis",
            "bullets": [
                "Primary competitor Nexus Corp lost 3.2% market share",
                "New entrant CloudBridge raised $200M Series C",
                "Our win rate vs. top 3 competitors: 62% (up from 54%)",
                "Patent portfolio expanded to 127 active patents",
                "Strategic partnership with Meridian Systems announced",
            ],
            "bg_color": (1, 1, 1),
            "title_color": (0.12, 0.18, 0.33),
        },
        {
            "title": "Financial Health Indicators",
            "bullets": [
                "Gross margin: 72.4% (up from 68.9%)",
                "Operating margin: 18.7%",
                "Free cash flow: $42.3M",
                "ARR: $980M (approaching $1B milestone)",
                "Net dollar retention: 118%",
            ],
            "bg_color": (0.95, 0.97, 0.95),
            "title_color": (0.1, 0.35, 0.1),
        },
        {
            "title": "Key Customer Wins in Q4",
            "bullets": [
                "GlobalTech Industries: $4.2M 3-year contract",
                "Pacific Healthcare Network: $2.8M annual deal",
                "Nordic Financial Group: $3.5M enterprise license",
                "Sahara Logistics Corp: $1.9M platform deployment",
                "Zenith Education Partners: $1.2M SaaS subscription",
            ],
            "bg_color": (1, 1, 1),
            "title_color": (0.12, 0.18, 0.33),
        },
        {
            "title": "Product Roadmap Highlights",
            "bullets": [
                "AI-powered analytics engine (launch: Feb 2026)",
                "Mobile-first dashboard redesign (launch: Mar 2026)",
                "Advanced API gateway with rate limiting (launch: Apr 2026)",
                "Multi-tenant workspace collaboration (launch: May 2026)",
                "Real-time data streaming integration (launch: Jun 2026)",
            ],
            "bg_color": (0.97, 0.95, 0.95),
            "title_color": (0.35, 0.1, 0.1),
        },
        {
            "title": "Risk Assessment",
            "bullets": [
                "Currency fluctuation impact: -$3.1M potential exposure",
                "Regulatory changes in EU data privacy (GDPR updates)",
                "Supply chain constraints on hardware partners",
                "Talent market tightening for senior ML engineers",
                "Mitigation plans in place for all identified risks",
            ],
            "bg_color": (1, 1, 1),
            "title_color": (0.12, 0.18, 0.33),
        },
        {
            "title": "Customer Satisfaction Deep Dive",
            "bullets": [
                "Enterprise NPS: 64 (industry avg: 41)",
                "Support response time: 12 min avg (target: 15 min)",
                "Feature request fulfillment rate: 34%",
                "Customer advisory board expanded to 25 members",
                "Quarterly business reviews conducted with top 100 accounts",
            ],
            "bg_color": (0.95, 0.95, 0.97),
            "title_color": (0.12, 0.18, 0.33),
        },
        {
            "title": "Marketing & Brand",
            "bullets": [
                "Brand awareness increased 22% in target demographics",
                "Annual conference attracted 8,500 attendees (+40% YoY)",
                "Content marketing generated 45,000 MQLs",
                "Social media following grew to 2.1M across platforms",
                "Won Best Enterprise Software at TechWorld Awards",
            ],
            "bg_color": (1, 1, 1),
            "title_color": (0.12, 0.18, 0.33),
        },
        {
            "title": "Partnerships & Ecosystem",
            "bullets": [
                "Technology partner ecosystem grew to 145 integrations",
                "Launched certified partner program with 68 agencies",
                "Co-selling pipeline with Meridian: $32M",
                "Developer community reached 52,000 active members",
                "Open-source contributions: 1,200+ PRs merged",
            ],
            "bg_color": (0.95, 0.97, 0.95),
            "title_color": (0.1, 0.35, 0.1),
        },
        {
            "title": "Sustainability & ESG",
            "bullets": [
                "Carbon neutral operations achieved in Q3 2025",
                "100% renewable energy for all data centers",
                "Diversity & inclusion score: 4.2/5.0",
                "Community investment: $2.5M in STEM education programs",
                "ESG rating upgraded to AA by MSCI",
            ],
            "bg_color": (1, 1, 1),
            "title_color": (0.12, 0.18, 0.33),
        },
        {
            "title": "Q1 2026 Projections",
            "bullets": [
                "Revenue target: $275M (+9% QoQ)",
                "New customer acquisition target: 9,500",
                "Platform uptime SLA: 99.99%",
                "Planned headcount additions: 180",
                "R&D investment: $38M (14% of revenue)",
            ],
            "bg_color": (0.97, 0.95, 0.95),
            "title_color": (0.35, 0.1, 0.1),
        },
        {
            "title": "Thank You",
            "subtitle": "Questions & Discussion\n\nElena Rodriguez | elena.rodriguez@atlascorp.com",
            "bg_color": (0.12, 0.18, 0.33),
            "title_color": (1, 1, 1),
        },
    ]

    for i, slide in enumerate(slides_content):
        page = doc.new_page(width=SLIDE_W, height=SLIDE_H)

        # Draw background
        bg = slide.get("bg_color", (1, 1, 1))
        shape = page.new_shape()
        shape.draw_rect(page.rect)
        shape.finish(color=bg, fill=bg)
        shape.commit()

        tc = slide.get("title_color", (0, 0, 0))

        # Draw title
        title = slide["title"]
        if "subtitle" in slide:
            # Title slide layout
            page.insert_text(
                pymupdf.Point(60, 160),
                title,
                fontsize=28,
                fontname="hebo",
                color=tc,
            )
            sub_color = (0.7, 0.7, 0.8) if bg[0] < 0.5 else (0.4, 0.4, 0.5)
            for j, line in enumerate(slide["subtitle"].split("\n")):
                page.insert_text(
                    pymupdf.Point(60, 200 + j * 20),
                    line,
                    fontsize=14,
                    fontname="helv",
                    color=sub_color,
                )
        else:
            # Content slide layout
            # Title bar accent line
            shape2 = page.new_shape()
            shape2.draw_rect(pymupdf.Rect(0, 0, SLIDE_W, 4))
            accent = (0.2, 0.4, 0.8)
            shape2.finish(color=accent, fill=accent)
            shape2.commit()

            page.insert_text(
                pymupdf.Point(40, 45),
                title,
                fontsize=20,
                fontname="hebo",
                color=tc,
            )

            # Divider line
            shape3 = page.new_shape()
            shape3.draw_line(pymupdf.Point(40, 55), pymupdf.Point(SLIDE_W - 40, 55))
            shape3.finish(color=(0.7, 0.7, 0.7), width=0.5)
            shape3.commit()

            # Bullets
            if "bullets" in slide:
                y = 80
                for bullet in slide["bullets"]:
                    bullet_color = (0.2, 0.2, 0.2) if bg[0] > 0.5 else (0.8, 0.8, 0.8)
                    page.insert_text(
                        pymupdf.Point(55, y),
                        bullet,
                        fontsize=12,
                        fontname="helv",
                        color=bullet_color,
                    )
                    y += 28

        # Slide number (bottom right)
        num_color = (0.6, 0.6, 0.7) if bg[0] < 0.5 else (0.5, 0.5, 0.5)
        page.insert_text(
            pymupdf.Point(SLIDE_W - 40, SLIDE_H - 15),
            str(i + 1),
            fontsize=9,
            fontname="helv",
            color=num_color,
        )

    doc.set_metadata({
        "title": "Q4 2025 Strategic Review",
        "author": "Elena Rodriguez",
        "subject": "Quarterly Business Review",
        "keywords": "strategy, Q4, 2025, review, business",
        "creator": "Atlas Corp Presentations",
    })

    doc.save(PDF_PATH)
    doc.close()
    print(f'Initial file created: {PDF_PATH}')
    print(f'Page count: 20')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{PDF_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
