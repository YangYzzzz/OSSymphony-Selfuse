"""
Initial Setup: Create a Writer document with 15 paragraphs in Default Paragraph Style
using Liberation Serif 12pt, single line spacing, left-aligned.
Task ID: writer_bs_052
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_052'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'


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
    doc = Document()

    # Configure the default paragraph style: Liberation Serif 12pt, single spacing, left-aligned
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Liberation Serif'
    font.size = Pt(12)
    pf = style.paragraph_format
    pf.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    pf.line_spacing = 1.0
    pf.space_after = Pt(0)
    pf.space_before = Pt(0)

    # 15 paragraphs of realistic business content
    paragraphs = [
        "Meridian Analytics released its quarterly performance report on March 15, 2025, highlighting a 12% increase in overall revenue compared to the same period last year. The growth was primarily driven by strong demand in the Asia-Pacific market, where new client acquisitions exceeded projections by a significant margin.",

        "Chief Financial Officer Elena Rodriguez presented the budget allocation for the upcoming fiscal year during the board meeting held at the company headquarters in Austin, Texas. She emphasized the importance of strategic investments in research and development to maintain competitive advantage.",

        "The human resources department announced a comprehensive restructuring of the employee benefits program, effective from the first quarter of 2026. Notable changes include an enhanced parental leave policy extending coverage to 16 weeks and the introduction of a mental health support allowance of $2,500 per employee annually.",

        "Project Lighthouse, the company's flagship digital transformation initiative, reached a critical milestone when the engineering team successfully migrated 78% of legacy infrastructure to cloud-based architecture. Senior Vice President of Technology David Park noted that the remaining migration phases are on track for completion by September 2025.",

        "The marketing division reported that the recent product launch campaign generated over 3.2 million impressions across social media platforms within the first 48 hours. Conversion rates from targeted advertising exceeded industry benchmarks by approximately 23%, according to data compiled by the analytics team.",

        "During the annual strategic planning retreat held in Boulder, Colorado, senior leadership identified three priority areas for the coming year: expanding the company's presence in emerging markets, accelerating the development of artificial intelligence capabilities, and strengthening partnerships with key enterprise clients in the healthcare sector.",

        "Internal audit findings released on February 28, 2025 confirmed that all operational processes within the supply chain management division are fully compliant with ISO 9001:2015 standards. The audit team commended the division for implementing a robust quality control framework that reduced defect rates by 34% over the past twelve months.",

        "The procurement department finalized a long-term contract with Silverstone Industrial Partners for the supply of raw materials used in manufacturing. The agreement, valued at approximately $8.7 million over three years, includes provisions for quarterly price adjustments based on prevailing market conditions.",

        "Customer satisfaction surveys conducted during the fourth quarter of 2024 revealed that the net promoter score improved from 62 to 71 points, reflecting a noticeable increase in client loyalty. Regional Manager Catherine Walsh attributed the improvement to the rollout of a dedicated account management program for mid-tier clients.",

        "The legal affairs team provided an update on the ongoing intellectual property dispute with Harmon Technologies. Lead counsel James Whitfield indicated that mediation proceedings are expected to conclude by May 2025, with a favorable outcome anticipated based on the strength of the documentary evidence presented to the arbitration panel.",

        "Facilities management completed the renovation of the second-floor conference center, which now features state-of-the-art audiovisual equipment, modular seating arrangements for up to 120 attendees, and improved acoustic insulation. The renovated space will serve as the primary venue for client presentations and internal training workshops.",

        "The data science team developed a predictive analytics model designed to identify potential supply chain disruptions before they impact production schedules. Initial testing showed that the model accurately forecasted 89% of disruption events within a 14-day window, enabling the operations team to implement contingency measures proactively.",

        "Vice President of Sales Marcus Thompson reported that the enterprise sales pipeline grew by 18% during the first quarter, driven by increased demand for the company's cybersecurity solutions among financial services firms. He projected that annual recurring revenue from enterprise accounts would surpass $45 million by year-end.",

        "The corporate social responsibility committee published its annual sustainability report, documenting a 27% reduction in carbon emissions from company operations since 2022. Key initiatives contributing to this achievement included the transition to renewable energy sources at three major manufacturing facilities and the implementation of a company-wide waste reduction program.",

        "Training and development records indicate that 92% of eligible employees completed the mandatory cybersecurity awareness certification by the December 2024 deadline. Program Director Aisha Patel recommended expanding the curriculum to include modules on data privacy regulations and secure remote work practices for the upcoming training cycle."
    ]

    for text in paragraphs:
        doc.add_paragraph(text)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Launch LibreOffice Writer with the file
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
