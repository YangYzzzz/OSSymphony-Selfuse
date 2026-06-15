"""
Initial Setup: Create a 5-page meeting notes PDF for highlight annotation task
Task ID: pdf_fm_010
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_010'
OUTPUT_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{OUTPUT_DIR}/meeting_notes.pdf'


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
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Q1 2025 All-Hands Meeting ---
    page = doc.new_page(width=595, height=842)

    # Title
    page.insert_text(
        pymupdf.Point(72, 60),
        "Quarterly All-Hands Meeting Notes",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    # Date and attendees line
    page.insert_text(
        pymupdf.Point(72, 85),
        "Date: March 15, 2025  |  Location: Conference Room A  |  Facilitator: Rachel Kim",
        fontsize=9,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # First paragraph - this is the target for the highlight annotation
    # Spanning roughly (72, 100, 540, 160) as specified in context
    first_para = (
        "The Q1 2025 all-hands meeting was called to order at 10:00 AM by Rachel Kim, VP of Operations. "
        "All department heads were present including James Park (Engineering), Sarah Chen (Marketing), "
        "David Okafor (Finance), and Lisa Tanaka (Human Resources). The agenda covered quarterly "
        "performance review, upcoming product launches, and organizational restructuring plans."
    )
    rect = pymupdf.Rect(72, 100, 540, 180)
    page.insert_textbox(rect, first_para, fontsize=10, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_LEFT)

    # Section: Performance Review
    page.insert_text(pymupdf.Point(72, 200), "1. Quarterly Performance Review",
                     fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.4))

    perf_text = (
        "James Park presented the engineering team's Q1 deliverables. The platform migration project "
        "is 85% complete, with final deployment scheduled for April 7th. Three critical bugs in the "
        "authentication module were resolved, reducing login failures by 62%. The team shipped 14 "
        "features against a target of 12, achieving 117% of the sprint commitment.\n\n"
        "Sarah Chen reported that marketing campaigns generated 4,200 qualified leads in Q1, "
        "exceeding the 3,500 target by 20%. The brand awareness survey showed a 15-point increase "
        "in unaided recall among the 25-34 demographic. Social media engagement grew 38% quarter-over-quarter, "
        "driven primarily by the new video content strategy launched in February."
    )
    rect2 = pymupdf.Rect(72, 220, 540, 450)
    page.insert_textbox(rect2, perf_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_LEFT)

    # Section: Financial Update
    page.insert_text(pymupdf.Point(72, 470), "2. Financial Update",
                     fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.4))

    fin_text = (
        "David Okafor shared the Q1 financial results. Total revenue reached $4.87M, representing "
        "a 23% year-over-year increase. Operating expenses were $3.12M, below the $3.25M budget. "
        "The EBITDA margin improved to 18.4%, up from 14.2% in Q1 2024. Cash reserves stand at "
        "$12.3M with a 14-month runway at current burn rate.\n\n"
        "Key cost savings came from the cloud infrastructure optimization project led by Marcus "
        "Rodriguez, which reduced monthly AWS spend by $45,000 through right-sizing instances and "
        "implementing reserved capacity agreements."
    )
    rect3 = pymupdf.Rect(72, 490, 540, 720)
    page.insert_textbox(rect3, fin_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_LEFT)

    # Footer
    page.insert_text(pymupdf.Point(72, 800), "Confidential - Internal Use Only",
                     fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
    page.insert_text(pymupdf.Point(500, 800), "Page 1 of 5",
                     fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 2: Product Launches ---
    page2 = doc.new_page(width=595, height=842)

    page2.insert_text(pymupdf.Point(72, 60), "3. Upcoming Product Launches",
                      fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.4))

    prod_text = (
        "The product team outlined three major launches planned for Q2 2025:\n\n"
        "a) Project Atlas (April 21): A complete redesign of the customer dashboard featuring "
        "real-time analytics, customizable widgets, and an AI-powered insights panel. Beta testing "
        "with 200 enterprise customers showed a 92% satisfaction rate. The rollout will be phased "
        "over two weeks starting with Tier 1 accounts.\n\n"
        "b) Mobile App v3.0 (May 5): Includes offline mode, biometric authentication, and push "
        "notification improvements. Performance benchmarks show 40% faster load times compared to "
        "v2.8. The QA team has completed 1,847 test cases with a 99.2% pass rate.\n\n"
        "c) Integration Hub (June 2): A new marketplace for third-party integrations including "
        "Salesforce, HubSpot, Slack, and 15 additional connectors. Partner onboarding is underway "
        "with 8 launch partners confirmed. Revenue projections estimate $180K ARR from integration "
        "licensing fees in the first year."
    )
    rect_p2 = pymupdf.Rect(72, 80, 540, 380)
    page2.insert_textbox(rect_p2, prod_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_LEFT)

    page2.insert_text(pymupdf.Point(72, 400), "4. Customer Success Highlights",
                      fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.4))

    cust_text = (
        "Lisa Tanaka presented key customer success metrics:\n\n"
        "- Net Promoter Score (NPS) increased from 42 to 58 in Q1\n"
        "- Customer churn rate decreased to 2.1%, down from 3.8% in Q4 2024\n"
        "- Average onboarding time reduced from 14 days to 8 days\n"
        "- Support ticket resolution time improved by 35% with the new AI chatbot\n\n"
        "Notable enterprise wins include Meridian Healthcare ($420K ACV), TechNova Solutions "
        "($285K ACV), and Pacific Coast Financial ($195K ACV). The total pipeline for Q2 stands "
        "at $2.1M with a 45% weighted close probability."
    )
    rect_p2b = pymupdf.Rect(72, 420, 540, 680)
    page2.insert_textbox(rect_p2b, cust_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_LEFT)

    page2.insert_text(pymupdf.Point(500, 800), "Page 2 of 5",
                      fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 3: Organizational Updates ---
    page3 = doc.new_page(width=595, height=842)

    page3.insert_text(pymupdf.Point(72, 60), "5. Organizational Restructuring",
                      fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.4))

    org_text = (
        "Rachel Kim announced several organizational changes effective April 1, 2025:\n\n"
        "The Engineering department will split into two divisions: Platform Engineering (led by "
        "James Park) and Product Engineering (led by newly promoted Anika Patel). This change "
        "reflects the growing complexity of our technical infrastructure and the need for dedicated "
        "leadership across both domains.\n\n"
        "A new Data Science team of 6 members will be formed under Carlos Mendez, reporting to "
        "the CTO. Initial focus areas include predictive churn modeling, usage pattern analysis, "
        "and automated feature recommendation algorithms.\n\n"
        "The Customer Success team will expand by 4 positions: 2 Enterprise Account Managers, "
        "1 Technical Solutions Architect, and 1 Onboarding Specialist. Hiring is expected to "
        "complete by end of April."
    )
    rect_p3 = pymupdf.Rect(72, 80, 540, 380)
    page3.insert_textbox(rect_p3, org_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_LEFT)

    page3.insert_text(pymupdf.Point(72, 400), "6. Office and Facilities",
                      fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.4))

    office_text = (
        "The office renovation project for the 3rd floor is on track for completion by May 15th. "
        "New amenities include a wellness room, expanded kitchen facilities, and 4 additional "
        "phone booths for private calls. The hybrid work policy remains unchanged: minimum 3 days "
        "in-office per week with flexibility for Tuesday and Thursday remote work.\n\n"
        "IT infrastructure upgrades include new 10Gbps network switches, upgraded Wi-Fi 6E access "
        "points throughout the building, and a refreshed conference room AV system supporting "
        "seamless hybrid meetings with Zoom Rooms integration."
    )
    rect_p3b = pymupdf.Rect(72, 420, 540, 640)
    page3.insert_textbox(rect_p3b, office_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_LEFT)

    page3.insert_text(pymupdf.Point(500, 800), "Page 3 of 5",
                      fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 4: Action Items ---
    page4 = doc.new_page(width=595, height=842)

    page4.insert_text(pymupdf.Point(72, 60), "7. Action Items",
                      fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.4))

    action_text = (
        "The following action items were assigned during the meeting:\n\n"
        "1. James Park - Finalize platform migration timeline and communicate go-live plan to "
        "all stakeholders by March 22.\n\n"
        "2. Sarah Chen - Prepare Q2 marketing budget proposal with emphasis on video content "
        "expansion and influencer partnership program. Due: March 28.\n\n"
        "3. David Okafor - Complete board-ready financial deck with updated projections "
        "incorporating the new pricing model. Due: April 3.\n\n"
        "4. Anika Patel - Draft Product Engineering team charter and propose initial sprint "
        "structure for the new division. Due: March 25.\n\n"
        "5. Carlos Mendez - Present Data Science team hiring plan with role descriptions and "
        "compensation benchmarks. Due: March 30.\n\n"
        "6. Lisa Tanaka - Coordinate with IT on office renovation punch list and confirm "
        "furniture delivery schedule. Due: March 20.\n\n"
        "7. All Department Heads - Submit Q2 OKRs to Rachel Kim for alignment review. "
        "Due: April 5."
    )
    rect_p4 = pymupdf.Rect(72, 80, 540, 520)
    page4.insert_textbox(rect_p4, action_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_LEFT)

    page4.insert_text(pymupdf.Point(72, 540), "8. Budget Approvals",
                      fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.4))

    budget_text = (
        "The following budget requests were approved:\n\n"
        "- Engineering cloud optimization tools: $35,000 (annual)\n"
        "- Marketing video production equipment: $22,500 (one-time)\n"
        "- HR recruiting platform upgrade: $18,000 (annual)\n"
        "- Office renovation contingency fund: $50,000\n"
        "- Data Science team hardware (GPU workstations): $67,000 (one-time)"
    )
    rect_p4b = pymupdf.Rect(72, 560, 540, 750)
    page4.insert_textbox(rect_p4b, budget_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_LEFT)

    page4.insert_text(pymupdf.Point(500, 800), "Page 4 of 5",
                      fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # --- Page 5: Next Meeting & Closing ---
    page5 = doc.new_page(width=595, height=842)

    page5.insert_text(pymupdf.Point(72, 60), "9. Upcoming Events",
                      fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.4))

    events_text = (
        "Key dates for the coming quarter:\n\n"
        "- April 7: Platform migration go-live\n"
        "- April 10-11: Company offsite at Redwood Retreat Center\n"
        "- April 21: Project Atlas customer dashboard launch\n"
        "- May 1: Q2 OKR kick-off meeting\n"
        "- May 5: Mobile App v3.0 release\n"
        "- May 15: Office 3rd floor renovation completion\n"
        "- June 2: Integration Hub marketplace launch\n"
        "- June 15: Mid-year performance review cycle begins\n"
        "- June 30: Q2 All-Hands Meeting"
    )
    rect_p5 = pymupdf.Rect(72, 80, 540, 320)
    page5.insert_textbox(rect_p5, events_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_LEFT)

    page5.insert_text(pymupdf.Point(72, 340), "10. Meeting Adjournment",
                      fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.4))

    closing_text = (
        "The meeting was adjourned at 11:45 AM. Rachel Kim thanked all participants for their "
        "thorough preparation and encouraged teams to begin executing on the Q2 initiatives "
        "immediately. Department heads were reminded to schedule their team debriefs within "
        "the next 48 hours to cascade key decisions.\n\n"
        "Minutes recorded by: Emily Watson, Executive Assistant\n"
        "Reviewed by: Rachel Kim, VP of Operations\n"
        "Distribution: All employees (via company intranet)"
    )
    rect_p5b = pymupdf.Rect(72, 360, 540, 550)
    page5.insert_textbox(rect_p5b, closing_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_LEFT)

    # Signature line
    shape = page5.new_shape()
    shape.draw_line(pymupdf.Point(72, 600), pymupdf.Point(280, 600))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page5.insert_text(pymupdf.Point(72, 615), "Rachel Kim, VP of Operations",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page5.insert_text(pymupdf.Point(72, 630), "Date: March 15, 2025",
                      fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

    page5.insert_text(pymupdf.Point(500, 800), "Page 5 of 5",
                      fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
