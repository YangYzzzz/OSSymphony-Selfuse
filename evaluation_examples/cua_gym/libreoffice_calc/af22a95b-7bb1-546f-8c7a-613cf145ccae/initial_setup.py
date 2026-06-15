"""
Initial Setup: Create a multi-page accessible PDF for accessibility audit task
Task ID: pdf_cr_060
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TASK_ID = 'pdf_cr_060'
OUTPUT = f'{DESKTOP}/accessible.pdf'


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
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    os.makedirs(DESKTOP, exist_ok=True)

    doc = pymupdf.open()

    # ---- Page 1: Title / Introduction ----
    page1 = doc.new_page(width=595, height=842)
    page1.insert_text(
        pymupdf.Point(72, 80),
        "Greenfield Sustainability Initiative",
        fontsize=26,
        fontname="hebo",
        color=(0.0, 0.2, 0.4),
    )
    page1.insert_text(
        pymupdf.Point(72, 115),
        "Annual Progress Report  |  Fiscal Year 2025",
        fontsize=13,
        fontname="heit",
        color=(0.3, 0.3, 0.3),
    )
    # Divider line
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 130), pymupdf.Point(523, 130))
    shape.finish(color=(0.0, 0.4, 0.2), width=1.5)
    shape.commit()

    intro_text = (
        "This report summarizes the progress made by the Greenfield Sustainability "
        "Initiative during Fiscal Year 2025. The initiative was launched in 2021 to "
        "reduce the environmental footprint of our operations across all regional "
        "offices. Over the past twelve months, the program has expanded to cover "
        "energy efficiency, waste reduction, water conservation, and carbon offset "
        "strategies.\n\n"
        "Key stakeholders include the Office of Environmental Affairs, Regional "
        "Operations Directors, the Facilities Management Division, and external "
        "partners such as EcoMetrics Consulting and the National Green Standards "
        "Board. The report is structured into five chapters covering objectives, "
        "methodology, results, financial impact, and future recommendations."
    )
    rect1 = pymupdf.Rect(72, 155, 523, 500)
    page1.insert_textbox(rect1, intro_text, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=0)

    page1.insert_text(
        pymupdf.Point(72, 530),
        "Prepared by: Dr. Elena Marchetti, Director of Sustainability Programs",
        fontsize=10,
        fontname="heit",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(72, 550),
        "Date: March 15, 2025",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # ---- Page 2: Objectives & Methodology ----
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text(
        pymupdf.Point(72, 72),
        "Chapter 1: Objectives",
        fontsize=20,
        fontname="hebo",
        color=(0.0, 0.2, 0.4),
    )
    obj_text = (
        "The primary objectives for FY2025 were established during the Q4 2024 "
        "strategic planning session. They include:\n\n"
        "1. Reduce total energy consumption by 15% compared to the FY2024 baseline.\n"
        "2. Divert at least 70% of office waste from landfills through recycling "
        "and composting programs.\n"
        "3. Achieve a 20% reduction in single-use plastics across cafeteria and "
        "supply operations.\n"
        "4. Install solar panel arrays at the Denver and Portland regional offices.\n"
        "5. Launch a pilot carbon offset program targeting 5,000 metric tons of CO2 "
        "equivalent.\n\n"
        "Each objective was assigned a dedicated project lead and quarterly milestones "
        "to track progress against targets."
    )
    rect2 = pymupdf.Rect(72, 100, 523, 400)
    page2.insert_textbox(rect2, obj_text, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=0)

    page2.insert_text(
        pymupdf.Point(72, 430),
        "Chapter 2: Methodology",
        fontsize=20,
        fontname="hebo",
        color=(0.0, 0.2, 0.4),
    )
    meth_text = (
        "Data collection followed the GreenMetrics Framework (v3.2), which defines "
        "standardized measurement protocols for energy, waste, water, and emissions. "
        "Utility billing records were aggregated monthly from all 14 regional offices. "
        "Waste audits were conducted quarterly by certified environmental auditors. "
        "Solar generation data was collected via IoT-enabled inverter monitoring systems "
        "providing real-time output readings.\n\n"
        "Statistical analysis used a combination of year-over-year trend comparison "
        "and regression modeling to account for weather variability, occupancy changes, "
        "and regional economic factors."
    )
    rect2b = pymupdf.Rect(72, 458, 523, 700)
    page2.insert_textbox(rect2b, meth_text, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=0)

    # ---- Page 3: Results ----
    page3 = doc.new_page(width=595, height=842)
    page3.insert_text(
        pymupdf.Point(72, 72),
        "Chapter 3: Results",
        fontsize=20,
        fontname="hebo",
        color=(0.0, 0.2, 0.4),
    )
    results_text = (
        "Energy Consumption: Total energy usage across all offices decreased by 17.3% "
        "relative to the FY2024 baseline, exceeding the 15% target. The Denver office "
        "achieved the highest reduction at 24.1%, largely attributable to the HVAC "
        "retrofit completed in November 2024.\n\n"
        "Waste Diversion: The overall waste diversion rate reached 73.8%, surpassing "
        "the 70% goal. Composting programs introduced at five new offices contributed "
        "an additional 890 metric tons of organic waste diverted from landfills.\n\n"
        "Single-Use Plastics: A 22.6% reduction in single-use plastics was documented, "
        "driven primarily by the adoption of reusable container programs in 9 of 14 "
        "office cafeterias.\n\n"
        "Solar Installation: The Denver array (capacity 150 kW) became operational in "
        "February 2025, while the Portland array (capacity 120 kW) is on track for "
        "completion by June 2025. Combined, these installations are projected to "
        "generate approximately 380 MWh annually.\n\n"
        "Carbon Offsets: The pilot program successfully retired 4,720 metric tons of "
        "verified carbon credits through reforestation projects in the Pacific Northwest "
        "and methane capture initiatives in the Midwest."
    )
    rect3 = pymupdf.Rect(72, 100, 523, 650)
    page3.insert_textbox(rect3, results_text, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=0)

    # ---- Page 4: Financial Impact ----
    page4 = doc.new_page(width=595, height=842)
    page4.insert_text(
        pymupdf.Point(72, 72),
        "Chapter 4: Financial Impact",
        fontsize=20,
        fontname="hebo",
        color=(0.0, 0.2, 0.4),
    )
    finance_text = (
        "The sustainability initiatives generated measurable financial benefits during "
        "FY2025. Total operational savings attributable to energy efficiency measures "
        "reached $1,245,000, compared to a program investment of $890,000 for the "
        "fiscal year. Key financial highlights include:\n\n"
        "Energy Cost Savings: $782,000 (reduction in electricity and natural gas bills)\n"
        "Waste Disposal Savings: $198,000 (lower landfill tipping fees)\n"
        "Water Conservation Savings: $67,000 (reduced municipal water charges)\n"
        "Carbon Credit Revenue: $198,000 (sale of excess verified offsets)\n\n"
        "The return on investment for FY2025 was 1.40x, and the cumulative ROI since "
        "program inception in 2021 stands at 2.15x. Capital expenditures for solar "
        "arrays ($2.1 million) are expected to achieve payback within 6.8 years based "
        "on current utility rates and projected generation.\n\n"
        "Budget allocation for FY2026 has been approved at $1,150,000, reflecting a "
        "29% increase to fund expanded initiatives including electric vehicle fleet "
        "conversion and green building certification for the new Seattle office."
    )
    rect4 = pymupdf.Rect(72, 100, 523, 600)
    page4.insert_textbox(rect4, finance_text, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=0)

    # ---- Page 5: Recommendations ----
    page5 = doc.new_page(width=595, height=842)
    page5.insert_text(
        pymupdf.Point(72, 72),
        "Chapter 5: Future Recommendations",
        fontsize=20,
        fontname="hebo",
        color=(0.0, 0.2, 0.4),
    )
    rec_text = (
        "Based on the achievements and lessons learned during FY2025, the Sustainability "
        "Committee recommends the following priorities for the coming fiscal year:\n\n"
        "1. Expand the solar panel program to at least three additional offices "
        "(Chicago, Atlanta, and Miami) to increase renewable generation capacity "
        "by 400 kW.\n\n"
        "2. Transition 30% of the corporate vehicle fleet to electric or hybrid "
        "models by Q2 FY2026.\n\n"
        "3. Implement smart building management systems at all offices with more "
        "than 200 employees to optimize HVAC and lighting schedules.\n\n"
        "4. Establish partnerships with at least two additional carbon offset providers "
        "to diversify the offset portfolio and reduce counterparty risk.\n\n"
        "5. Pursue LEED Gold certification for the new Seattle office, incorporating "
        "lessons from the Denver retrofit.\n\n"
        "6. Develop an employee engagement scorecard that tracks individual and team "
        "contributions to sustainability goals, integrated into the annual performance "
        "review process.\n\n"
        "The committee will present a detailed implementation plan at the Q1 FY2026 "
        "leadership retreat scheduled for October 2025."
    )
    rect5 = pymupdf.Rect(72, 100, 523, 700)
    page5.insert_textbox(rect5, rec_text, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=0)

    # ---- Set Metadata ----
    doc.set_metadata({
        "title": "Greenfield Sustainability Initiative - Annual Progress Report FY2025",
        "author": "Dr. Elena Marchetti",
        "subject": "Sustainability Progress Report",
        "keywords": "sustainability, environment, energy, carbon offset, green initiative",
        "creator": "Greenfield Corp Sustainability Office",
        "producer": "PyMuPDF",
    })

    # ---- Set Language ----
    # Set the document language via the catalog
    cat = doc.pdf_catalog()
    # Use xref-based approach to set /Lang
    xref = cat
    doc.xref_set_key(xref, "Lang", "(en-US)")

    # ---- Set Table of Contents (Bookmarks) ----
    toc = [
        [1, "Introduction", 1],
        [1, "Chapter 1: Objectives", 2],
        [1, "Chapter 2: Methodology", 2],
        [1, "Chapter 3: Results", 3],
        [1, "Chapter 4: Financial Impact", 4],
        [1, "Chapter 5: Future Recommendations", 5],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open PDF in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
