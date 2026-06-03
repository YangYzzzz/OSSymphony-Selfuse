"""
Initial Setup: Create a 10-page team review PDF with a sticky note on page 6
Task ID: pdf_fm_025
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_025'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS_DIR}/team_review.pdf'


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

    doc = pymupdf.open()

    # --- Page dimensions ---
    W, H = 595, 842  # A4

    # --- Page 1: Title Page ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 120), "Q3 2025 Team Performance Review",
                     fontsize=24, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 170), "Prepared by: Human Resources Department",
                     fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 200), "Date: August 10, 2025",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 230), "Confidential - Internal Use Only",
                     fontsize=11, fontname="heit", color=(0.6, 0.0, 0.0))
    # Decorative line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 260), pymupdf.Point(523, 260))
    shape.finish(color=(0.1, 0.1, 0.4), width=2)
    shape.commit()
    page.insert_textbox(
        pymupdf.Rect(72, 290, 523, 500),
        "This document contains the quarterly performance review for all departments "
        "within the Engineering, Marketing, Sales, and Operations divisions. "
        "The review covers key metrics, individual contributions, and strategic "
        "recommendations for Q4 2025 planning.\n\n"
        "Distribution: VP Engineering, VP Marketing, VP Sales, VP Operations, "
        "Chief People Officer, CEO",
        fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Page 2: Executive Summary ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "Executive Summary",
                     fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 75), pymupdf.Point(300, 75))
    shape.finish(color=(0.1, 0.1, 0.4), width=1)
    shape.commit()
    page.insert_textbox(
        pymupdf.Rect(72, 90, 523, 780),
        "Overall Performance: The team delivered 94% of planned objectives for Q3 2025, "
        "a 7% improvement over Q2. Revenue targets were exceeded by 12%, with notable "
        "contributions from the Enterprise Sales team and the Platform Engineering group.\n\n"
        "Headcount: The organization grew from 187 to 203 employees, with key hires in "
        "the AI/ML division (8 engineers) and Customer Success (4 specialists). Attrition "
        "remained low at 3.2%, well below the industry average of 8.5%.\n\n"
        "Key Highlights:\n"
        "- Launched the Meridian Platform v3.0 ahead of schedule\n"
        "- Closed 14 enterprise deals totaling $4.2M ARR\n"
        "- Customer NPS score improved from 62 to 71\n"
        "- Reduced infrastructure costs by 18% through cloud optimization\n"
        "- Filed 3 patent applications for proprietary ML algorithms\n\n"
        "Areas for Improvement:\n"
        "- Cross-team communication needs strengthening\n"
        "- Documentation practices remain inconsistent\n"
        "- QA cycle times are 20% above target\n"
        "- On-call rotation burnout reported in SRE team",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Page 3: Engineering Department ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "Engineering Department",
                     fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 75), pymupdf.Point(350, 75))
    shape.finish(color=(0.1, 0.1, 0.4), width=1)
    shape.commit()
    page.insert_textbox(
        pymupdf.Rect(72, 90, 523, 780),
        "Department Head: Sarah Chen, VP Engineering\n"
        "Team Size: 78 engineers (up from 72 in Q2)\n\n"
        "Sprint Velocity: Average 142 story points per sprint (target: 130)\n"
        "Bug Resolution Rate: 89% within SLA (target: 85%)\n"
        "Code Review Turnaround: 4.2 hours average (target: 6 hours)\n"
        "Deployment Frequency: 18 deployments per week (up from 12)\n\n"
        "Top Performers:\n"
        "- Marcus Johnson (Staff Engineer): Led the database migration project, "
        "reducing query latency by 40%. Mentored 3 junior engineers.\n"
        "- Aisha Patel (Senior Engineer): Architected the new event streaming "
        "pipeline. Presented at KubeCon 2025.\n"
        "- David Kim (Engineering Manager): Successfully transitioned Platform "
        "team to trunk-based development, improving merge frequency by 3x.\n\n"
        "Projects Delivered:\n"
        "1. Meridian Platform v3.0 - Real-time analytics dashboard\n"
        "2. API Gateway v2 - OAuth 2.1 support, rate limiting overhaul\n"
        "3. ML Pipeline Infrastructure - Automated model training and deployment\n"
        "4. Observability Stack Migration - Moved to OpenTelemetry\n\n"
        "Challenges:\n"
        "- Technical debt in the legacy billing module needs addressing\n"
        "- CI/CD pipeline reliability at 97.8% (target: 99.5%)\n"
        "- Inter-service latency spikes during peak traffic",
        fontsize=10.5, fontname="helv", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Page 4: Marketing Department ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "Marketing Department",
                     fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 75), pymupdf.Point(330, 75))
    shape.finish(color=(0.1, 0.1, 0.4), width=1)
    shape.commit()
    page.insert_textbox(
        pymupdf.Rect(72, 90, 523, 780),
        "Department Head: Lisa Rodriguez, VP Marketing\n"
        "Team Size: 24 (up from 21 in Q2)\n\n"
        "Campaign Performance:\n"
        "- Generated 2,847 MQLs (target: 2,200) - 129% of goal\n"
        "- Website traffic increased 34% YoY to 1.2M unique visitors\n"
        "- Social media engagement up 28% across all channels\n"
        "- Email open rate: 24.6% (industry avg: 18.2%)\n"
        "- Content published: 42 blog posts, 8 whitepapers, 3 case studies\n\n"
        "Top Performers:\n"
        "- James Wright (Content Lead): Wrote the viral thought leadership piece "
        "'The Future of Enterprise AI' - 45K shares\n"
        "- Priya Sharma (Demand Gen Manager): Redesigned the lead scoring model, "
        "improving SQL conversion by 22%\n"
        "- Tom Nakamura (Brand Designer): Completed full brand refresh ahead of schedule\n\n"
        "Key Initiatives:\n"
        "1. Product-led growth motion launched for Meridian Starter\n"
        "2. Partner co-marketing program with 6 ISV partners\n"
        "3. Annual user conference 'Meridian Summit' planning (Nov 2025)\n"
        "4. New customer advocacy program with 12 reference accounts\n\n"
        "Budget: $1.8M spent of $2.1M allocated (86% utilization)\n"
        "CAC: $342 (down from $410 in Q2, target: $350)",
        fontsize=10.5, fontname="helv", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Page 5: Sales Department ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "Sales Department",
                     fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 75), pymupdf.Point(280, 75))
    shape.finish(color=(0.1, 0.1, 0.4), width=1)
    shape.commit()
    page.insert_textbox(
        pymupdf.Rect(72, 90, 523, 780),
        "Department Head: Robert Yang, VP Sales\n"
        "Team Size: 32 (unchanged from Q2)\n\n"
        "Revenue Metrics:\n"
        "- New ARR: $4.2M (target: $3.8M) - 110% attainment\n"
        "- Total Pipeline: $18.7M (3.2x coverage)\n"
        "- Average Deal Size: $145K (up from $118K in Q2)\n"
        "- Win Rate: 34% (up from 28%)\n"
        "- Average Sales Cycle: 62 days (down from 78 days)\n\n"
        "Top Performers:\n"
        "- Nicole Anderson (Enterprise AE): Closed 3 deals totaling $1.1M, "
        "including the Apex Financial account\n"
        "- Raj Krishnan (Mid-Market AE): 156% quota attainment, fastest ramp "
        "for a new hire in company history\n"
        "- Elena Torres (SE Lead): Supported 28 technical evaluations with "
        "92% close rate on supported deals\n\n"
        "Notable Deals:\n"
        "1. Apex Financial Services - $480K ARR (3-year contract)\n"
        "2. Northern Healthcare Group - $320K ARR\n"
        "3. Pacific Logistics Corp - $285K ARR\n"
        "4. Atlas Manufacturing - $210K ARR (expansion)\n\n"
        "Pipeline Analysis: Q4 pipeline is strong at $14.2M with 45% in "
        "stages 3+. Risk: 3 large deals ($800K combined) in legal review.",
        fontsize=10.5, fontname="helv", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Page 6: Operations & Finance (0-indexed page 5 - the one with the sticky note) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "Operations & Finance",
                     fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 75), pymupdf.Point(330, 75))
    shape.finish(color=(0.1, 0.1, 0.4), width=1)
    shape.commit()
    page.insert_textbox(
        pymupdf.Rect(72, 90, 523, 780),
        "Department Head: Karen Mitchell, VP Operations\n"
        "Finance Lead: Thomas Park, Controller\n"
        "Combined Team Size: 28\n\n"
        "Financial Highlights:\n"
        "- Total Revenue: $8.4M (target: $7.8M)\n"
        "- Gross Margin: 78.2% (target: 75%)\n"
        "- Operating Expenses: $6.1M (under budget by $340K)\n"
        "- EBITDA: $1.9M (22.6% margin)\n"
        "- Cash Runway: 24 months at current burn rate\n\n"
        "Operational Metrics:\n"
        "- System Uptime: 99.97% (target: 99.95%)\n"
        "- Support Ticket Resolution: 4.1 hours avg (target: 6 hours)\n"
        "- Customer Churn Rate: 1.8% monthly (target: 2.5%)\n"
        "- Infrastructure Cost per User: $12.40 (down 18% from $15.10)\n\n"
        "Key Achievements:\n"
        "1. Completed SOC 2 Type II audit with zero findings\n"
        "2. Migrated 60% of workloads to spot instances\n"
        "3. Implemented automated invoice processing (saving 120 hrs/month)\n"
        "4. Reduced vendor costs by $280K through contract renegotiation\n\n"
        "Figure 6.1: Q3 Cost Breakdown by Department\n"
        "Engineering: $3.2M | Marketing: $1.8M | Sales: $2.4M | Ops: $0.7M\n\n"
        "Budget Forecast for Q4:\n"
        "Projected Revenue: $9.1M | Projected OpEx: $6.5M | Target EBITDA: $2.2M",
        fontsize=10.5, fontname="helv", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Add the sticky note annotation on page 6 (0-indexed: 5)
    annot = page.add_text_annot(
        pymupdf.Point(400, 400),
        "Is this figure correct?",
        icon="Note"
    )
    annot.set_colors(stroke=(1, 0.8, 0))  # orange
    annot.update()

    # --- Page 7: Customer Success ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "Customer Success",
                     fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 75), pymupdf.Point(290, 75))
    shape.finish(color=(0.1, 0.1, 0.4), width=1)
    shape.commit()
    page.insert_textbox(
        pymupdf.Rect(72, 90, 523, 780),
        "Department Head: Amanda Foster, Director of Customer Success\n"
        "Team Size: 18 (up from 14 in Q2)\n\n"
        "Customer Health Metrics:\n"
        "- Net Promoter Score: 71 (up from 62 in Q2)\n"
        "- Customer Health Score: 82/100 average\n"
        "- Expansion Revenue: $1.4M (target: $1.1M)\n"
        "- Renewal Rate: 94.5% (target: 92%)\n"
        "- Time to Value: 21 days average (down from 34 days)\n\n"
        "Top Performers:\n"
        "- Maria Gonzalez (Senior CSM): Managed 32 accounts with zero churn, "
        "drove $420K in expansion revenue\n"
        "- Ben Cooper (Implementation Lead): Reduced average onboarding time "
        "from 6 weeks to 3 weeks\n"
        "- Sarah Liu (Support Engineer): Achieved 98.7% customer satisfaction "
        "rating on technical escalations\n\n"
        "Key Programs:\n"
        "1. Launched Customer Advisory Board with 8 strategic accounts\n"
        "2. Created self-service knowledge base (500+ articles)\n"
        "3. Implemented proactive health monitoring alerts\n"
        "4. Started quarterly business review cadence for top 50 accounts",
        fontsize=10.5, fontname="helv", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Page 8: People & Culture ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "People & Culture",
                     fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 75), pymupdf.Point(280, 75))
    shape.finish(color=(0.1, 0.1, 0.4), width=1)
    shape.commit()
    page.insert_textbox(
        pymupdf.Rect(72, 90, 523, 780),
        "Department Head: Jennifer Walsh, Chief People Officer\n"
        "Team Size: 8\n\n"
        "Talent Metrics:\n"
        "- Total Headcount: 203 (up from 187)\n"
        "- New Hires: 22 (16 backfills + 6 new positions)\n"
        "- Voluntary Attrition: 3.2% annualized (industry: 8.5%)\n"
        "- Offer Acceptance Rate: 88% (target: 85%)\n"
        "- Average Time to Fill: 38 days (target: 45 days)\n"
        "- Employee Engagement Score: 4.3/5.0\n\n"
        "Diversity & Inclusion:\n"
        "- Gender diversity: 41% women (up from 38%)\n"
        "- Underrepresented minorities: 28% (up from 24%)\n"
        "- Pay equity audit completed - 98.5% compliance\n\n"
        "Learning & Development:\n"
        "- 92% of employees completed required training\n"
        "- 45 employees participated in leadership development\n"
        "- Average L&D spend: $2,400 per employee\n"
        "- Internal promotion rate: 22% (target: 20%)\n\n"
        "Culture Initiatives:\n"
        "1. Launched flexible hybrid work policy (3 days in-office)\n"
        "2. Mental health support program expanded\n"
        "3. Quarterly hackathon events (avg 60% participation)\n"
        "4. ERG budget increased by 40%",
        fontsize=10.5, fontname="helv", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Page 9: Strategic Initiatives ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "Strategic Initiatives for Q4",
                     fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 75), pymupdf.Point(380, 75))
    shape.finish(color=(0.1, 0.1, 0.4), width=1)
    shape.commit()
    page.insert_textbox(
        pymupdf.Rect(72, 90, 523, 780),
        "Based on Q3 performance and market conditions, the following strategic "
        "initiatives are prioritized for Q4 2025:\n\n"
        "1. AI-Powered Analytics Module (Priority: Critical)\n"
        "   Lead: Sarah Chen | Budget: $1.2M | Timeline: Oct-Dec 2025\n"
        "   Integrate generative AI capabilities into Meridian Platform for "
        "   automated insight generation and natural language queries.\n\n"
        "2. Enterprise Security Enhancements (Priority: High)\n"
        "   Lead: David Kim | Budget: $450K | Timeline: Oct-Nov 2025\n"
        "   Implement SSO/SAML federation, advanced audit logging, and "
        "   data residency controls for EU market expansion.\n\n"
        "3. Partner Ecosystem Expansion (Priority: High)\n"
        "   Lead: Lisa Rodriguez & Robert Yang | Budget: $600K\n"
        "   Launch marketplace for third-party integrations. Target: 20 "
        "   certified partner integrations by end of Q4.\n\n"
        "4. Customer-Led Growth Program (Priority: Medium)\n"
        "   Lead: Amanda Foster | Budget: $200K\n"
        "   Expand advocacy program, launch referral incentive system, "
        "   produce 10 video testimonials from key accounts.\n\n"
        "5. Operational Excellence (Priority: Medium)\n"
        "   Lead: Karen Mitchell | Budget: $300K\n"
        "   Achieve FedRAMP Moderate certification, implement FinOps "
        "   practices, reduce P1 incident MTTR to under 30 minutes.",
        fontsize=10.5, fontname="helv", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # --- Page 10: Appendix ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "Appendix: Key Metrics Dashboard",
                     fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 75), pymupdf.Point(420, 75))
    shape.finish(color=(0.1, 0.1, 0.4), width=1)
    shape.commit()
    page.insert_textbox(
        pymupdf.Rect(72, 90, 523, 780),
        "Quarterly Comparison Table\n\n"
        "Metric                    Q1 2025    Q2 2025    Q3 2025\n"
        "------                    -------    -------    -------\n"
        "Revenue ($M)                6.8        7.4        8.4\n"
        "ARR Growth (%)              22         26         31\n"
        "Customer Count             412        438        467\n"
        "Headcount                  178        187        203\n"
        "NPS Score                   58         62         71\n"
        "Uptime (%)                99.94      99.96      99.97\n"
        "Sprint Velocity            128        135        142\n"
        "Bug Resolution (%)          82         86         89\n"
        "MQLs Generated           1,840      2,120      2,847\n"
        "Win Rate (%)                24         28         34\n"
        "Churn Rate (%)             2.8        2.2        1.8\n"
        "Employee Engagement       4.0        4.1        4.3\n\n"
        "Notes:\n"
        "- All financial figures are unaudited\n"
        "- NPS measured via quarterly customer survey (n=280)\n"
        "- Sprint velocity is team average across 12 scrum teams\n"
        "- Win rate calculated on opportunities > $50K\n\n"
        "Next Review: November 15, 2025\n"
        "Prepared by: HR Analytics Team\n"
        "Approved by: Executive Leadership Team",
        fontsize=10.5, fontname="cour", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 10')

    # Open in Evince at page 6
    launch_gui(f'evince --page-index=5 "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
