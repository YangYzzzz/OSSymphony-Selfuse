"""
Initial Setup: Create chapter data JSON and reports directory for multi-chapter PDF task
Task ID: pdf_aw_026
Domain: pdf
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_026'
DATA_DIR = f'{WORKDIR}/data'
REPORTS_DIR = f'{WORKDIR}/reports'
CHAPTERS_JSON = f'{DATA_DIR}/chapters.json'


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
    # Create directories
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Create chapters.json with 4 chapters, each with title and 3 paragraphs
    chapters = [
        {
            "title": "Executive Summary",
            "paragraphs": [
                "The first quarter of 2026 demonstrated strong performance across all major business segments. Revenue grew by 12.3% year-over-year, reaching $48.7 million, driven primarily by expansion in the enterprise software division and increased adoption of our cloud-based analytics platform. Operating margins improved to 24.1%, reflecting the benefits of our ongoing cost optimization initiatives and favorable product mix shift toward higher-margin recurring revenue streams.",
                "Customer acquisition accelerated significantly during the quarter, with 847 new enterprise accounts added compared to 612 in the prior quarter. The net revenue retention rate remained above 115%, indicating robust expansion within existing accounts. Our strategic partnership with Meridian Technologies, announced in February, has already contributed 23 new joint enterprise deals worth an estimated $6.2 million in annual contract value.",
                "Looking ahead, the management team maintains a cautiously optimistic outlook for Q2 2026. The pipeline of qualified opportunities has grown to $127 million, representing a 31% increase from the beginning of the fiscal year. Key initiatives for the upcoming quarter include the launch of our next-generation predictive analytics module, expansion into the Southeast Asian market, and continued investment in our AI-powered customer success platform."
            ]
        },
        {
            "title": "Financial Performance",
            "paragraphs": [
                "Total revenue for Q1 2026 reached $48.7 million, representing a 12.3% increase from $43.4 million in Q1 2025. Subscription revenue, which now accounts for 73% of total revenue, grew 18.6% to $35.6 million. Professional services revenue was $8.4 million, down slightly from $8.9 million in the prior year as the company continues its strategic shift toward self-service implementation tools. Hardware and licensing revenue contributed the remaining $4.7 million.",
                "Gross profit for the quarter was $33.1 million, yielding a gross margin of 67.9%, up from 65.2% in Q1 2025. The improvement was driven by economies of scale in cloud infrastructure costs, which decreased from 22.4% to 19.8% of subscription revenue. Research and development expenses were $11.2 million (23.0% of revenue), reflecting increased investment in the AI and machine learning capabilities of our product suite. Sales and marketing expenses of $9.8 million (20.1% of revenue) decreased as a percentage of revenue due to improved sales productivity.",
                "Net income for Q1 2026 was $5.9 million, or $0.42 per diluted share, compared to $3.8 million, or $0.28 per diluted share, in Q1 2025. Adjusted EBITDA was $11.7 million, representing a margin of 24.1%, up from 20.3% in the year-ago period. Free cash flow was $8.3 million, and the company ended the quarter with $92.4 million in cash and short-term investments, providing ample liquidity for planned growth initiatives."
            ]
        },
        {
            "title": "Product Development and Innovation",
            "paragraphs": [
                "The engineering team made significant progress on several key product initiatives during Q1 2026. The beta release of our Predictive Analytics 3.0 module received overwhelmingly positive feedback from the 45 enterprise customers participating in the early access program. Key enhancements include real-time anomaly detection powered by our proprietary neural network architecture, natural language querying capabilities that allow non-technical users to generate complex analytical reports, and seamless integration with over 200 third-party data sources including Salesforce, SAP, and Oracle Cloud.",
                "Our mobile platform underwent a major redesign during the quarter, with the new responsive interface launching in March 2026. Initial metrics show a 34% increase in mobile engagement and a 28% reduction in average time-to-insight for mobile users. The redesign also introduced offline analytics capabilities, allowing field teams to access critical dashboards and reports without an internet connection. This feature has been particularly well-received by customers in the manufacturing and logistics sectors.",
                "Investment in artificial intelligence continued to be a strategic priority, with the AI research team growing from 28 to 41 engineers during the quarter. Notable achievements include the development of our AutoML pipeline, which reduces model training time by 60% compared to previous approaches, and the launch of an AI-powered data quality assessment tool that automatically identifies and flags data integrity issues across connected data sources. Patent applications for three novel machine learning techniques were filed during the quarter."
            ]
        },
        {
            "title": "Market Expansion and Strategic Outlook",
            "paragraphs": [
                "Geographic expansion remained a key growth driver in Q1 2026, with international revenue increasing 22.7% year-over-year to $14.6 million, now representing 30% of total revenue. The opening of our Singapore regional headquarters in January has accelerated market penetration in Southeast Asia, with 12 new enterprise customers signed in the region during the quarter. The European business continued its strong trajectory, with particular strength in the DACH region where revenue grew 31% year-over-year driven by demand from automotive and financial services verticals.",
                "The competitive landscape evolved meaningfully during Q1, with two significant acquisitions among our peer group. Our differentiated position as the only independent, pure-play analytics platform with native AI capabilities has resonated strongly with customers concerned about vendor lock-in. Win rates against our top three competitors improved from 42% to 49% during the quarter, and average deal sizes increased 15% as customers increasingly chose our comprehensive platform over point solutions from multiple vendors.",
                "For the remainder of fiscal year 2026, management is focused on three strategic priorities. First, accelerating the transition to consumption-based pricing, which early pilots indicate can increase customer lifetime value by 25-35%. Second, deepening vertical expertise through the launch of industry-specific solution packages for healthcare, financial services, and manufacturing sectors. Third, building out our partner ecosystem to include 50 certified implementation partners by year-end, up from the current 23, to support scalable growth without proportional increases in professional services headcount."
            ]
        }
    ]

    with open(CHAPTERS_JSON, 'w') as f:
        json.dump(chapters, f, indent=2)

    print(f'Created chapters JSON: {CHAPTERS_JSON}')
    print(f'Created reports directory: {REPORTS_DIR}')

    # Open file manager to show the data directory
    launch_gui(f'nautilus "{DATA_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
