"""
Initial Setup: Create Q1 and Q2 report PDFs for merge task
Task ID: pdf_pw_030
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_030'
REPORTS_DIR = f'{WORKDIR}/reports'

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


def create_q1_report():
    """Create a 15-page Q1 financial report."""
    doc = pymupdf.open()

    # Page dimensions
    W, H = 595, 842  # A4

    # --- Page 1: Title Page ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(W/2 - 120, 200), "Q1 Financial Report",
                     fontsize=28, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_text(pymupdf.Point(W/2 - 80, 250), "January - March 2025",
                     fontsize=16, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(W/2 - 70, 300), "Meridian Corp.",
                     fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(100, 320), pymupdf.Point(495, 320))
    shape.finish(color=(0.1, 0.15, 0.35), width=2)
    shape.commit()

    # --- Page 2: Executive Summary ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Executive Summary",
                     fontsize=22, fontname="hebo", color=(0.1, 0.15, 0.35))
    summary_text = (
        "Meridian Corp. delivered strong results in Q1 2025 with total revenue of $48.7M, "
        "representing a 12% year-over-year increase. Operating margins improved to 23.4%, "
        "driven by cost optimization initiatives and robust demand across our enterprise "
        "software division. The customer acquisition rate rose by 18%, adding 2,340 new "
        "enterprise accounts. Our SaaS recurring revenue grew to $32.1M, now comprising "
        "66% of total revenue. Key investments in AI-driven analytics and cloud "
        "infrastructure modernization remain on track with Q2 milestones."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 400), summary_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 3: Revenue Breakdown ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Revenue Breakdown",
                     fontsize=22, fontname="hebo", color=(0.1, 0.15, 0.35))
    revenue_data = [
        ("Product Line", "Jan ($K)", "Feb ($K)", "Mar ($K)", "Total ($K)"),
        ("Enterprise SaaS", "9,450", "9,820", "10,130", "29,400"),
        ("Professional Services", "2,100", "2,340", "2,560", "7,000"),
        ("Data Analytics Suite", "1,800", "1,950", "2,050", "5,800"),
        ("Cloud Infrastructure", "1,200", "1,350", "1,450", "4,000"),
        ("Support & Maintenance", "850", "830", "820", "2,500"),
    ]
    y = 110
    for i, row in enumerate(revenue_data):
        x = 72
        fname = "hebo" if i == 0 else "helv"
        for val in row:
            page.insert_text(pymupdf.Point(x, y), val, fontsize=10, fontname=fname, color=(0, 0, 0))
            x += 95
        y += 22

    # --- Pages 4-5: Monthly Financials ---
    for month_name in ["January 2025", "February 2025"]:
        page = doc.new_page(width=W, height=H)
        page.insert_text(pymupdf.Point(72, 72), f"Financial Details - {month_name}",
                         fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
        details = (
            f"Total Revenue: $16.4M\n"
            f"Cost of Goods Sold: $6.2M\n"
            f"Gross Profit: $10.2M\n"
            f"Operating Expenses: $4.8M\n"
            f"EBITDA: $5.4M\n"
            f"Net Income: $3.8M\n\n"
            f"Headcount: 1,245 FTE\n"
            f"Customer Churn Rate: 2.1%\n"
            f"Net Promoter Score: 72\n"
        )
        page.insert_textbox(pymupdf.Rect(72, 100, 523, 500), details,
                            fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 6: March Financials ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Financial Details - March 2025",
                     fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 500),
                        "Total Revenue: $17.0M\nCost of Goods Sold: $6.4M\n"
                        "Gross Profit: $10.6M\nOperating Expenses: $4.9M\n"
                        "EBITDA: $5.7M\nNet Income: $4.0M\n\n"
                        "Headcount: 1,278 FTE\nCustomer Churn Rate: 1.9%\n"
                        "Net Promoter Score: 74",
                        fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Pages 7-9: Department Reports ---
    departments = [
        ("Engineering Division", "The engineering team completed 47 sprint cycles with a "
         "97.2% on-time delivery rate. Major milestones included the release of v4.2 of "
         "the Analytics Platform and the beta launch of the AI Copilot feature. Infrastructure "
         "uptime remained at 99.97%. The team expanded from 380 to 412 engineers."),
        ("Sales & Marketing", "New enterprise deals closed: 187 (target: 160). Average deal "
         "size increased to $142K from $128K in Q4 2024. Marketing qualified leads grew 24% "
         "through targeted ABM campaigns. The North America region contributed 62% of new "
         "bookings, EMEA 28%, and APAC 10%."),
        ("Customer Success", "Renewal rate: 94.3% (up from 92.1% in Q4). Expansion revenue "
         "from existing accounts: $4.2M. Support ticket resolution time averaged 4.2 hours "
         "(SLA target: 8 hours). The team onboarded 312 new enterprise customers with an "
         "average time-to-value of 21 days."),
    ]
    for dept_name, dept_text in departments:
        page = doc.new_page(width=W, height=H)
        page.insert_text(pymupdf.Point(72, 72), dept_name,
                         fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
        page.insert_textbox(pymupdf.Rect(72, 100, 523, 500), dept_text,
                            fontsize=11, fontname="helv", color=(0, 0, 0),
                            align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Pages 10-12: Regional Performance ---
    regions = [
        ("North America Region", "Revenue: $30.2M | Growth: 14% YoY | Key accounts: Microsoft, "
         "Salesforce, JPMorgan. Expansion into Canadian market showing strong traction with "
         "12 new enterprise accounts. US federal contracts pipeline valued at $8.5M."),
        ("EMEA Region", "Revenue: $13.6M | Growth: 9% YoY | Key accounts: Siemens, Unilever, "
         "Barclays. New office opened in Berlin with 45 staff. GDPR compliance certification "
         "renewed. Partnership with SAP yielding 23% of regional leads."),
        ("APAC Region", "Revenue: $4.9M | Growth: 22% YoY | Key accounts: Toyota, Samsung, "
         "ANZ Bank. Established data center presence in Singapore. Japan market entry "
         "progressing with 3 pilot programs underway."),
    ]
    for region_name, region_text in regions:
        page = doc.new_page(width=W, height=H)
        page.insert_text(pymupdf.Point(72, 72), region_name,
                         fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
        page.insert_textbox(pymupdf.Rect(72, 100, 523, 500), region_text,
                            fontsize=11, fontname="helv", color=(0, 0, 0),
                            align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 13: Risk Assessment ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Risk Assessment",
                     fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 600),
                        "1. Market Competition: Increased pressure from emerging AI-native "
                        "competitors. Mitigation: Accelerated R&D investment and strategic "
                        "acquisitions pipeline.\n\n"
                        "2. Talent Retention: Engineering turnover at 8.2% (industry avg: 12%). "
                        "Mitigation: Enhanced equity packages and remote work flexibility.\n\n"
                        "3. Regulatory Changes: Pending EU AI Act compliance requirements. "
                        "Mitigation: Dedicated compliance team established in Q1.\n\n"
                        "4. Currency Fluctuation: USD strengthening impacting EMEA margins. "
                        "Mitigation: Hedging strategy covers 70% of projected exposure.\n\n"
                        "5. Supply Chain: Cloud infrastructure costs rising 6% QoQ. "
                        "Mitigation: Multi-cloud strategy and reserved capacity agreements.",
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 14: Key Metrics Dashboard ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Key Performance Indicators",
                     fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
    kpis = [
        ("ARR (Annual Recurring Revenue)", "$128.4M", "+15% YoY"),
        ("Monthly Active Users", "892,000", "+21% YoY"),
        ("Customer Lifetime Value", "$284,000", "+8% YoY"),
        ("CAC Payback Period", "14 months", "-2 months"),
        ("Gross Margin", "62.3%", "+1.8pp"),
        ("Rule of 40 Score", "47", "+3 points"),
        ("Employee Satisfaction", "4.3/5.0", "+0.2"),
        ("Carbon Footprint", "1,240 tCO2e", "-12% YoY"),
    ]
    y = 110
    for kpi_name, kpi_val, kpi_change in kpis:
        page.insert_text(pymupdf.Point(72, y), kpi_name, fontsize=11, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(330, y), kpi_val, fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(450, y), kpi_change, fontsize=11, fontname="helv", color=(0, 0.5, 0))
        y += 28

    # --- Page 15: Q2 Outlook ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Q2 2025 Outlook",
                     fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 500),
                        "Revenue guidance: $51-53M (8-12% sequential growth). Key initiatives: "
                        "Launch of AI Copilot GA, expansion of APAC sales team by 30%, "
                        "completion of SOC 2 Type II certification, and strategic partnership "
                        "announcement with a major cloud provider. Capital expenditure projected "
                        "at $4.2M for data center expansion and $2.8M for product development. "
                        "Board has approved a $5M share buyback program effective April 2025.",
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    q1_path = f'{REPORTS_DIR}/q1_report.pdf'
    doc.save(q1_path)
    doc.close()
    print(f'Q1 report created: {q1_path} ({15} pages)')
    return q1_path


def create_q2_report():
    """Create an 18-page Q2 financial report."""
    doc = pymupdf.open()
    W, H = 595, 842

    # --- Page 1: Title Page ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(W/2 - 120, 200), "Q2 Financial Report",
                     fontsize=28, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_text(pymupdf.Point(W/2 - 70, 250), "April - June 2025",
                     fontsize=16, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(W/2 - 70, 300), "Meridian Corp.",
                     fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(100, 320), pymupdf.Point(495, 320))
    shape.finish(color=(0.1, 0.15, 0.35), width=2)
    shape.commit()

    # --- Page 2: Executive Summary ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Executive Summary",
                     fontsize=22, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 400),
                        "Q2 2025 marked a record quarter for Meridian Corp. with revenue reaching "
                        "$53.2M, surpassing guidance. The AI Copilot product launch generated $6.8M "
                        "in new bookings within its first full quarter. Operating margins expanded to "
                        "25.1%, reflecting operational leverage and disciplined cost management. "
                        "The APAC expansion strategy gained momentum with 28 new enterprise clients.",
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 3: Revenue Breakdown ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Revenue Breakdown",
                     fontsize=22, fontname="hebo", color=(0.1, 0.15, 0.35))
    revenue_data = [
        ("Product Line", "Apr ($K)", "May ($K)", "Jun ($K)", "Total ($K)"),
        ("Enterprise SaaS", "10,500", "10,820", "11,200", "32,520"),
        ("AI Copilot", "1,800", "2,200", "2,800", "6,800"),
        ("Professional Services", "2,400", "2,500", "2,680", "7,580"),
        ("Data Analytics Suite", "1,650", "1,720", "1,830", "5,200"),
        ("Support & Maintenance", "450", "420", "430", "1,300"),
    ]
    y = 110
    for i, row in enumerate(revenue_data):
        x = 72
        fname = "hebo" if i == 0 else "helv"
        for val in row:
            page.insert_text(pymupdf.Point(x, y), val, fontsize=10, fontname=fname, color=(0, 0, 0))
            x += 95
        y += 22

    # --- Pages 4-6: Monthly Financials ---
    months = [
        ("April 2025", "$17.8M", "$6.7M", "$11.1M", "$5.0M", "$6.1M", "$4.3M", "1,310", "1.8%", "75"),
        ("May 2025", "$17.9M", "$6.8M", "$11.1M", "$5.1M", "$6.0M", "$4.2M", "1,342", "1.7%", "76"),
        ("June 2025", "$18.5M", "$6.9M", "$11.6M", "$5.2M", "$6.4M", "$4.5M", "1,380", "1.6%", "78"),
    ]
    for month_name, rev, cogs, gp, opex, ebitda, ni, hc, churn, nps in months:
        page = doc.new_page(width=W, height=H)
        page.insert_text(pymupdf.Point(72, 72), f"Financial Details - {month_name}",
                         fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
        details = (
            f"Total Revenue: {rev}\n"
            f"Cost of Goods Sold: {cogs}\n"
            f"Gross Profit: {gp}\n"
            f"Operating Expenses: {opex}\n"
            f"EBITDA: {ebitda}\n"
            f"Net Income: {ni}\n\n"
            f"Headcount: {hc} FTE\n"
            f"Customer Churn Rate: {churn}\n"
            f"Net Promoter Score: {nps}\n"
        )
        page.insert_textbox(pymupdf.Rect(72, 100, 523, 500), details,
                            fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Pages 7-9: Department Reports ---
    departments = [
        ("Engineering Division", "AI Copilot reached GA with 99.5% uptime. Platform v4.3 released "
         "with 23 new integrations. Infrastructure migration to multi-cloud architecture completed "
         "ahead of schedule. Team grew to 445 engineers with 15 senior hires from FAANG companies."),
        ("Sales & Marketing", "New enterprise deals: 214 (target: 185). Average deal size: $156K. "
         "Marketing pipeline grew 31% through AI-powered lead scoring. Partnership channel now "
         "contributes 28% of total bookings. Customer conference attracted 3,200 attendees."),
        ("Customer Success", "Renewal rate: 95.8%. Expansion revenue: $5.1M. Support resolution "
         "time: 3.8 hours. Launched premium support tier with 98% satisfaction score. "
         "Onboarded 415 new enterprise customers with 18-day average time-to-value."),
    ]
    for dept_name, dept_text in departments:
        page = doc.new_page(width=W, height=H)
        page.insert_text(pymupdf.Point(72, 72), dept_name,
                         fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
        page.insert_textbox(pymupdf.Rect(72, 100, 523, 500), dept_text,
                            fontsize=11, fontname="helv", color=(0, 0, 0),
                            align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Pages 10-12: Regional Performance ---
    regions = [
        ("North America Region", "Revenue: $33.0M | Growth: 11% QoQ | Federal contract worth "
         "$3.2M secured. Canadian operations profitable for first time. US west coast hub "
         "opened in San Francisco with 60 staff."),
        ("EMEA Region", "Revenue: $14.8M | Growth: 9% QoQ | Berlin office fully operational. "
         "UK public sector deal worth GBP 2.1M signed. EU AI Act compliance achieved ahead "
         "of regulatory deadline."),
        ("APAC Region", "Revenue: $5.4M | Growth: 10% QoQ | Japan pilot converted to full "
         "deployment at Toyota and NTT. Singapore data center capacity doubled. Australia "
         "team expanded to 25 with dedicated support center."),
    ]
    for region_name, region_text in regions:
        page = doc.new_page(width=W, height=H)
        page.insert_text(pymupdf.Point(72, 72), region_name,
                         fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
        page.insert_textbox(pymupdf.Rect(72, 100, 523, 500), region_text,
                            fontsize=11, fontname="helv", color=(0, 0, 0),
                            align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 13: Product Innovation ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Product Innovation Highlights",
                     fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 600),
                        "1. AI Copilot GA Launch: Successfully launched with 850 enterprise "
                        "customers onboarded in first 90 days. User engagement 3x higher than "
                        "projected baseline.\n\n"
                        "2. Platform v4.3: 23 new third-party integrations including Snowflake, "
                        "Databricks, and Azure Synapse. API call volume increased 45%.\n\n"
                        "3. Mobile App Redesign: Complete UX overhaul resulting in 40% increase "
                        "in mobile session duration and 4.7 App Store rating.\n\n"
                        "4. Security Enhancements: SOC 2 Type II certification achieved. "
                        "Zero-trust architecture implementation 80% complete.\n\n"
                        "5. Developer Platform: Public API program launched with 1,200 developers "
                        "registered. Marketplace features 45 certified partner integrations.",
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 14: Risk Assessment ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Risk Assessment - Q2 Update",
                     fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 600),
                        "1. AI Regulation: EU AI Act effective August 2025. Full compliance "
                        "achieved. US regulatory landscape evolving with proposed AI Safety Act.\n\n"
                        "2. Competitive Landscape: Two well-funded startups ($200M+ Series C) "
                        "entering enterprise analytics space. Differentiation through AI Copilot "
                        "and platform depth.\n\n"
                        "3. Macroeconomic: Interest rate environment stabilizing. Enterprise "
                        "IT budgets showing recovery signs. Deal cycle length decreased 15%.\n\n"
                        "4. Cybersecurity: Attempted breach detected and neutralized in May. "
                        "Bug bounty program expanded. Penetration testing frequency doubled.\n\n"
                        "5. Talent: Engineering attrition decreased to 6.8%. New university "
                        "partnership program bringing 40 interns for H2 2025.",
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 15: Key Metrics ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Key Performance Indicators",
                     fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
    kpis = [
        ("ARR", "$145.6M", "+13% QoQ"),
        ("Monthly Active Users", "1,042,000", "+17% QoQ"),
        ("Customer Lifetime Value", "$298,000", "+5% QoQ"),
        ("CAC Payback Period", "12 months", "-2 months"),
        ("Gross Margin", "64.1%", "+1.8pp"),
        ("Rule of 40 Score", "52", "+5 points"),
        ("Employee Satisfaction", "4.4/5.0", "+0.1"),
        ("Carbon Footprint", "1,180 tCO2e", "-5% QoQ"),
    ]
    y = 110
    for kpi_name, kpi_val, kpi_change in kpis:
        page.insert_text(pymupdf.Point(72, y), kpi_name, fontsize=11, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(330, y), kpi_val, fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(450, y), kpi_change, fontsize=11, fontname="helv", color=(0, 0.5, 0))
        y += 28

    # --- Page 16: Strategic Partnerships ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Strategic Partnerships",
                     fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 500),
                        "Major partnership established with Amazon Web Services as a Premier "
                        "Technology Partner. Joint go-to-market program expected to generate "
                        "$15M in pipeline over next 12 months. Additional partnerships signed "
                        "with Deloitte for system integration services and Accenture for "
                        "managed services delivery. Technology integration agreements with "
                        "Snowflake and Databricks deepened with co-developed connectors.",
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 17: ESG Report ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "ESG Report",
                     fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 500),
                        "Environmental: Achieved carbon neutrality for Scope 1 and 2 emissions. "
                        "Renewable energy procurement covers 85% of data center needs. E-waste "
                        "recycling program processed 2.4 tons of equipment.\n\n"
                        "Social: Diversity hiring increased to 42% of new hires from "
                        "underrepresented groups. Launched mentorship program with 180 pairs. "
                        "Employee volunteer program logged 4,500 hours.\n\n"
                        "Governance: Independent board members increased to 7 of 9. ESG committee "
                        "established. Whistleblower hotline received zero reports. Executive "
                        "compensation tied to ESG metrics at 15% weighting.",
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 18: Q3 Outlook ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Q3 2025 Outlook",
                     fontsize=20, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 500),
                        "Revenue guidance: $56-59M (6-11% sequential growth). Key priorities: "
                        "AI Copilot expansion to mid-market segment, launch of vertical-specific "
                        "solutions for healthcare and financial services, completion of zero-trust "
                        "security architecture, and preparation for Series F fundraise targeting "
                        "$200M at $2.5B+ valuation. Headcount planned to reach 1,500 by Q3 end "
                        "with emphasis on product engineering and APAC sales.",
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    q2_path = f'{REPORTS_DIR}/q2_report.pdf'
    doc.save(q2_path)
    doc.close()
    print(f'Q2 report created: {q2_path} ({18} pages)')
    return q2_path


def create_initial():
    os.makedirs(REPORTS_DIR, exist_ok=True)

    q1_path = create_q1_report()
    q2_path = create_q2_report()

    # GUI-ready: open q1_report in Evince
    launch_gui(f'evince "{q1_path}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with q1_report.pdf on DISPLAY=:0')


create_initial()
