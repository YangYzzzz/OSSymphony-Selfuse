"""
Initial Setup: Create a 20-page official report PDF and a university logo PNG.
Task ID: pdf_res_065
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_065'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT_PDF = f'{PAPERS_DIR}/official_report.pdf'
OUTPUT_LOGO = f'{PAPERS_DIR}/university_logo.png'


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


def create_logo():
    """Create a 200x200 pixel university logo PNG."""
    from PIL import Image, ImageDraw, ImageFont

    size = 200
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Draw a shield shape background
    # Outer shield - dark blue
    shield_points = [
        (100, 10),   # top center
        (180, 30),   # top right
        (185, 120),  # mid right
        (100, 190),  # bottom center
        (15, 120),   # mid left
        (20, 30),    # top left
    ]
    draw.polygon(shield_points, fill=(0, 51, 102, 255))

    # Inner shield - lighter blue
    inner_points = [
        (100, 22),
        (170, 40),
        (174, 115),
        (100, 178),
        (26, 115),
        (30, 40),
    ]
    draw.polygon(inner_points, fill=(0, 76, 153, 255))

    # Draw a book icon in the center
    draw.rectangle([65, 70, 95, 130], fill=(255, 215, 0, 255))   # left page
    draw.rectangle([105, 70, 135, 130], fill=(255, 215, 0, 255))  # right page
    draw.rectangle([95, 65, 105, 135], fill=(139, 101, 8, 255))   # spine

    # Add horizontal lines on book pages
    for y in range(80, 125, 10):
        draw.line([(70, y), (90, y)], fill=(0, 51, 102, 200), width=1)
        draw.line([(110, y), (130, y)], fill=(0, 51, 102, 200), width=1)

    # Add "UNI" text at top
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except (IOError, OSError):
        font = ImageFont.load_default()
    draw.text((72, 38), "UNI", fill=(255, 215, 0, 255), font=font)

    # Add "EST. 1892" at bottom
    try:
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except (IOError, OSError):
        small_font = ImageFont.load_default()
    draw.text((60, 142), "EST. 1892", fill=(255, 215, 0, 255), font=small_font)

    img.save(OUTPUT_LOGO)
    print(f'Logo created: {OUTPUT_LOGO}')


def create_report():
    """Create a 20-page official report PDF with realistic content."""
    import pymupdf

    doc = pymupdf.open()

    # Report content organized by sections
    sections = [
        {
            "title": "Annual Research Performance Report",
            "subtitle": "Westfield University - Academic Year 2024-2025",
            "type": "cover"
        },
        {
            "title": "Table of Contents",
            "type": "toc"
        },
        {
            "title": "1. Executive Summary",
            "body": (
                "This report presents the annual research performance metrics for Westfield University "
                "for the academic year 2024-2025. The university has demonstrated significant growth across "
                "all key performance indicators, with total research funding increasing by 18.3% compared to "
                "the previous year. A total of 2,847 peer-reviewed publications were produced across our "
                "seven research colleges, with the College of Engineering and Applied Sciences leading with "
                "612 publications. Our strategic partnerships with industry have expanded to include 43 new "
                "collaborative agreements, bringing the total active partnerships to 187. Graduate student "
                "enrollment in research programs grew by 12.1%, with 1,456 students currently pursuing "
                "doctoral degrees. The university's global ranking improved from 156th to 142nd in the "
                "Times Higher Education World University Rankings."
            )
        },
        {
            "title": "2. Research Funding Overview",
            "body": (
                "Total research expenditures for FY2024-2025 reached $342.7 million, representing an "
                "increase of $53.1 million over the prior year. Federal funding accounted for 62.4% of "
                "total research revenue ($213.8M), with the National Science Foundation ($78.2M), National "
                "Institutes of Health ($64.5M), and Department of Defense ($38.9M) as the three largest "
                "sources. State funding contributed $41.2M (12.0%), while industry partnerships provided "
                "$52.8M (15.4%). Foundation and private donor contributions totaled $34.9M (10.2%). "
                "The College of Medicine secured the largest share at $94.3M, followed by Engineering at "
                "$72.1M, and Natural Sciences at $58.6M. Notably, the College of Social Sciences achieved "
                "a 34.7% year-over-year increase in external funding, reaching $28.4M."
            )
        },
        {
            "title": "3. Publication Metrics",
            "body": (
                "Westfield University researchers published 2,847 peer-reviewed articles in FY2024-2025, "
                "a 9.2% increase from 2,607 in the prior year. Of these, 1,234 appeared in journals ranked "
                "in the top quartile (Q1) of their respective fields. The university's h-index rose to 284, "
                "and the average citation impact reached 1.42, exceeding the global mean of 1.00. "
                "The most prolific departments included Biomedical Engineering (312 publications), "
                "Computer Science (287 publications), Molecular Biology (264 publications), and "
                "Chemical Engineering (198 publications). Open access publications constituted 47.3% "
                "of total output, reflecting the university's commitment to knowledge dissemination. "
                "Three researchers were recognized in the Highly Cited Researchers list by Clarivate: "
                "Dr. Elena Vasquez (Immunology), Dr. Rajesh Patel (Materials Science), and "
                "Dr. Sarah O'Brien (Artificial Intelligence)."
            )
        },
        {
            "title": "4. Graduate Research Programs",
            "body": (
                "Graduate enrollment in research-intensive programs reached 3,218 students, including "
                "1,456 doctoral candidates and 1,762 research master's students. The doctoral completion "
                "rate improved to 71.4%, up from 68.2% in the previous year. Average time-to-degree for "
                "doctoral students was 5.2 years, consistent with national benchmarks. A total of 298 "
                "doctoral dissertations were defended successfully during the reporting period. "
                "International graduate students comprised 38.6% of the research student population, "
                "representing 72 countries. The Graduate Research Fellowship program awarded 145 fellowships "
                "totaling $8.7M, while external fellowships (NSF GRFP, DOE CSGF, NIH F31) supported an "
                "additional 89 students. The new Interdisciplinary Research Training Program, launched in "
                "Fall 2024, enrolled its inaugural cohort of 34 students across six thematic clusters."
            )
        },
        {
            "title": "5. Intellectual Property and Technology Transfer",
            "body": (
                "The Office of Technology Transfer processed 187 invention disclosures in FY2024-2025, "
                "resulting in 94 patent applications filed and 52 patents granted. Licensing revenue "
                "reached $18.4M, a 22.6% increase over the prior year. Twelve new startup companies were "
                "launched based on university research, bringing the cumulative total of active spinoffs to "
                "67. Notable technology transfers included a novel mRNA delivery platform licensed to "
                "Meridian Therapeutics ($4.2M upfront), a carbon capture membrane technology licensed to "
                "GreenAir Solutions ($2.8M plus royalties), and an AI-driven diagnostic tool for early "
                "cancer detection licensed to HealthScan Inc. ($1.9M). The University Innovation Hub "
                "provided mentorship and seed funding to 28 faculty-led ventures through its accelerator "
                "program, distributing $3.4M in proof-of-concept grants."
            )
        },
        {
            "title": "6. Research Infrastructure and Facilities",
            "body": (
                "Significant investments were made in research infrastructure during FY2024-2025. "
                "The new Advanced Materials Characterization Center ($42M) opened in January 2025, housing "
                "state-of-the-art electron microscopy, X-ray diffraction, and spectroscopy equipment. "
                "The High-Performance Computing Center received a $12M upgrade, increasing computational "
                "capacity to 4.8 petaflops. The Biomedical Research Building expansion ($67M) added "
                "85,000 sq ft of BSL-2 and BSL-3 laboratory space. The university's research core "
                "facilities served 1,847 unique users across 23 shared instrument platforms, generating "
                "$6.2M in user fees. Equipment investments totaling $28.3M were made through a combination "
                "of institutional funds ($14.1M), federal grants ($9.8M), and donor contributions ($4.4M). "
                "The campus research network was upgraded to 400Gbps backbone connectivity."
            )
        },
        {
            "title": "7. Industry Partnerships and Collaborative Research",
            "body": (
                "Strategic industry partnerships continued to grow, with 43 new collaborative agreements "
                "signed during the reporting period. Total industry-sponsored research reached $52.8M "
                "across 312 active projects. Key partnerships included a $15M five-year agreement with "
                "Quantum Dynamics Corp for quantum computing research, a $8.5M collaboration with "
                "BioGenesis Pharma for drug discovery, and a $6.2M joint research program with "
                "TerraEnergy Systems for renewable energy storage. The Corporate Affiliates Program "
                "engaged 94 member companies, providing $4.1M in unrestricted research support. "
                "Faculty consulting agreements numbered 234, generating $3.8M in additional revenue. "
                "The university hosted the 3rd Annual Industry-Academia Innovation Summit in April 2025, "
                "attracting 450 attendees from 128 organizations."
            )
        },
        {
            "title": "8. International Research Collaborations",
            "body": (
                "Westfield University maintained active research collaborations with 213 institutions "
                "across 48 countries. International co-authored publications accounted for 31.4% of total "
                "output, with the strongest collaboration networks in the United Kingdom (187 co-authored "
                "papers), Germany (143), China (128), Japan (96), and Australia (84). The Global Research "
                "Exchange Program supported 67 visiting scholars and 42 outgoing faculty research stays. "
                "Joint degree programs with partner institutions enrolled 28 doctoral students in "
                "co-supervised arrangements. Major international grants included a $3.2M EU Horizon "
                "Europe grant for climate modeling, a $2.1M JSPS grant for materials science research, "
                "and a $1.8M DFG grant for computational neuroscience. The university's international "
                "research offices in London, Singapore, and Sao Paulo facilitated 34 new partnerships."
            )
        },
        {
            "title": "9. Research Centers and Institutes",
            "body": (
                "The university operates 18 interdisciplinary research centers and institutes, which "
                "collectively secured $87.4M in external funding. The Center for Artificial Intelligence "
                "and Machine Learning (CAIML) led with $18.7M in grants and 156 publications. The "
                "Institute for Climate and Environmental Science (ICES) secured a landmark $12.5M NSF "
                "grant for a decade-long environmental monitoring program. The Quantum Information Science "
                "Center (QISC), established in September 2024, rapidly grew to 23 affiliated faculty "
                "members and $9.3M in first-year funding. Other notable centers include the Biomedical "
                "Innovation Institute ($14.2M), the Center for Advanced Energy Systems ($11.8M), and "
                "the Institute for Social Policy Research ($7.6M). Two new centers were approved by the "
                "Board of Trustees: the Center for Space Technology and the Digital Humanities Lab."
            )
        },
        {
            "title": "10. Faculty Research Awards and Recognition",
            "body": (
                "Westfield faculty received numerous prestigious awards during FY2024-2025. Dr. Michael "
                "Torres (Physics) was elected to the National Academy of Sciences, and Dr. Ananya Sharma "
                "(Computer Science) received the ACM A.M. Turing Award for contributions to distributed "
                "systems. Seven faculty members received NSF CAREER Awards: Dr. James Liu (Mechanical "
                "Engineering), Dr. Maria Gonzalez (Chemistry), Dr. David Kim (Electrical Engineering), "
                "Dr. Lisa Wang (Biostatistics), Dr. Robert Okafor (Civil Engineering), Dr. Emily Fischer "
                "(Environmental Science), and Dr. Ahmed Hassan (Computer Science). Three NIH Director's "
                "New Innovator Awards were secured by Dr. Priya Mehta (Neuroscience), Dr. Jonathan Blake "
                "(Genomics), and Dr. Rachel Torres (Immunology). Total faculty honors and awards numbered "
                "184, including 12 international distinctions."
            )
        },
        {
            "title": "11. Research Ethics and Compliance",
            "body": (
                "The Office of Research Integrity processed 4,231 protocol reviews during FY2024-2025, "
                "including 1,847 IRB applications, 1,523 IACUC protocols, and 861 IBC registrations. "
                "The average IRB review turnaround time was reduced to 12.3 business days from 16.7 in "
                "the prior year through process improvements and the deployment of the new electronic "
                "submission system. Export control reviews numbered 342, with 28 Technology Control Plans "
                "established. The Responsible Conduct of Research training program was completed by 2,847 "
                "researchers, achieving a 98.2% compliance rate. Three research misconduct allegations "
                "were investigated; one was substantiated, resulting in a three-year debarment. The office "
                "conducted 156 random compliance audits across active grants with a 94.7% compliance rate."
            )
        },
        {
            "title": "12. Research Computing and Data Science",
            "body": (
                "The Research Computing Division supported 2,134 active users across campus. The Pegasus "
                "HPC cluster processed 8.7 million compute jobs consuming 142 million core-hours, a 23% "
                "increase over the prior year. Cloud computing expenditures reached $4.3M, primarily on "
                "AWS ($2.1M) and Google Cloud ($1.4M). The university's research data repository ingested "
                "847 TB of new data, bringing total managed research data to 4.2 PB. The Data Science "
                "Institute launched three new certificate programs and graduated its first cohort of 28 "
                "students in the MS in Applied Data Science program. Research software engineering support "
                "was provided to 67 projects, with the team contributing to 34 open-source software "
                "releases. The annual Research Computing Symposium attracted 312 participants."
            )
        },
        {
            "title": "13. Community Engagement and Broader Impacts",
            "body": (
                "Research-driven community engagement initiatives reached an estimated 145,000 community "
                "members during FY2024-2025. The Science Outreach Program conducted 234 events at local "
                "schools, engaging 18,700 K-12 students. The Community Health Research Partnership "
                "completed its third year, providing health screenings and wellness programs to 12,400 "
                "residents in underserved neighborhoods. The Environmental Monitoring Citizen Science "
                "project enrolled 3,200 volunteer participants across the tri-county region. Faculty "
                "researchers contributed 847 media appearances (interviews, op-eds, expert commentary), "
                "enhancing public understanding of scientific issues. The annual Science Festival drew "
                "23,000 attendees over three days. Grant proposals including broader impact activities "
                "constituted 82.3% of all submissions, up from 76.1% in the prior year."
            )
        },
        {
            "title": "14. Financial Summary and Budget Outlook",
            "body": (
                "Total research-related revenue for FY2024-2025 was $342.7M, against expenditures of "
                "$328.4M, yielding a net positive balance of $14.3M. Indirect cost recovery (F&A) "
                "totaled $89.2M at the negotiated rate of 56.5% (on-campus) and 26.0% (off-campus). "
                "Research-related capital expenditures were $28.3M, funded through institutional reserves "
                "($14.1M), federal equipment grants ($9.8M), and philanthropic gifts ($4.4M). The "
                "projected budget for FY2025-2026 anticipates a 7.2% increase in total research revenue "
                "to $367.4M, driven by anticipated growth in federal appropriations and expanding industry "
                "partnerships. Key investment priorities for the coming year include the renovation of "
                "the Chemistry Research Wing ($18M), establishment of the Space Technology Center ($8M), "
                "and deployment of a next-generation research data management platform ($3.2M)."
            )
        },
        {
            "title": "15. Strategic Priorities for FY2025-2026",
            "body": (
                "Based on the performance analysis presented in this report, the following strategic "
                "priorities have been identified for the coming academic year: (1) Expand interdisciplinary "
                "research clusters in AI/ML, quantum science, and climate resilience with targeted seed "
                "funding of $5M. (2) Increase industry partnership revenue by 15% through dedicated "
                "business development staffing and a new corporate engagement model. (3) Enhance graduate "
                "student support through a 10% increase in fellowship stipends and new professional "
                "development programming. (4) Achieve 55% open access publication rate through expanded "
                "institutional agreements with major publishers. (5) Launch the Digital Research Commons "
                "platform to improve research data sharing and reproducibility. (6) Strengthen research "
                "security protocols in alignment with NSPM-33 requirements. (7) Establish two new "
                "interdisciplinary research centers as approved by the Board of Trustees."
            )
        },
        {
            "title": "Appendix A: Research Expenditures by College",
            "type": "table",
            "headers": ["College", "Federal ($M)", "State ($M)", "Industry ($M)", "Other ($M)", "Total ($M)"],
            "rows": [
                ["Medicine", "58.4", "11.2", "14.8", "9.9", "94.3"],
                ["Engineering", "42.3", "8.1", "15.2", "6.5", "72.1"],
                ["Natural Sciences", "38.7", "6.4", "7.8", "5.7", "58.6"],
                ["Computing & Info Sci", "28.9", "4.2", "8.3", "3.1", "44.5"],
                ["Social Sciences", "18.1", "3.8", "2.7", "3.8", "28.4"],
                ["Agriculture & Life Sci", "15.6", "4.8", "2.4", "2.7", "25.5"],
                ["Arts & Humanities", "11.8", "2.7", "1.6", "3.2", "19.3"],
            ]
        },
        {
            "title": "Appendix B: Key Performance Indicators Summary",
            "type": "kpi_table",
            "headers": ["Metric", "FY2023-24", "FY2024-25", "Change (%)"],
            "rows": [
                ["Total Research Expenditures ($M)", "289.6", "342.7", "+18.3"],
                ["Peer-Reviewed Publications", "2,607", "2,847", "+9.2"],
                ["Patent Applications Filed", "81", "94", "+16.0"],
                ["Licensing Revenue ($M)", "15.0", "18.4", "+22.6"],
                ["Startup Companies Launched", "9", "12", "+33.3"],
                ["Doctoral Degrees Awarded", "267", "298", "+11.6"],
                ["Industry Partnerships (active)", "144", "187", "+29.9"],
                ["International Collaborations", "189", "213", "+12.7"],
                ["H-Index", "271", "284", "+4.8"],
                ["Global Ranking (THE)", "156", "142", "+9.0"],
            ]
        },
    ]

    page_width = 595   # A4
    page_height = 842

    for i in range(20):
        page = doc.new_page(width=page_width, height=page_height)

        if i < len(sections):
            section = sections[i]
        else:
            section = sections[-1]  # repeat last if needed

        section_type = section.get("type", "body")

        if section_type == "cover":
            # Cover page
            # Title background band
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(0, 250, page_width, 420))
            shape.finish(fill=(0, 0.2, 0.4))
            shape.commit()

            page.insert_text(
                pymupdf.Point(72, 310),
                section["title"],
                fontsize=26,
                fontname="hebo",
                color=(1, 1, 1),
            )
            page.insert_text(
                pymupdf.Point(72, 360),
                section["subtitle"],
                fontsize=16,
                fontname="helv",
                color=(0.9, 0.9, 0.9),
            )
            page.insert_text(
                pymupdf.Point(72, 500),
                "Office of the Vice Provost for Research",
                fontsize=14,
                fontname="helv",
                color=(0, 0.2, 0.4),
            )
            page.insert_text(
                pymupdf.Point(72, 525),
                "Published: March 2025",
                fontsize=12,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )
            page.insert_text(
                pymupdf.Point(72, 550),
                "Classification: Internal Use Only",
                fontsize=12,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )

        elif section_type == "toc":
            # Table of contents page
            page.insert_text(
                pymupdf.Point(72, 72),
                section["title"],
                fontsize=22,
                fontname="hebo",
                color=(0, 0.2, 0.4),
            )
            # Draw line under title
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
            shape.finish(color=(0, 0.2, 0.4), width=1.5)
            shape.commit()

            toc_entries = [
                ("1. Executive Summary", "3"),
                ("2. Research Funding Overview", "4"),
                ("3. Publication Metrics", "5"),
                ("4. Graduate Research Programs", "6"),
                ("5. Intellectual Property and Technology Transfer", "7"),
                ("6. Research Infrastructure and Facilities", "8"),
                ("7. Industry Partnerships and Collaborative Research", "9"),
                ("8. International Research Collaborations", "10"),
                ("9. Research Centers and Institutes", "11"),
                ("10. Faculty Research Awards and Recognition", "12"),
                ("11. Research Ethics and Compliance", "13"),
                ("12. Research Computing and Data Science", "14"),
                ("13. Community Engagement and Broader Impacts", "15"),
                ("14. Financial Summary and Budget Outlook", "16"),
                ("15. Strategic Priorities for FY2025-2026", "17"),
                ("Appendix A: Research Expenditures by College", "18"),
                ("Appendix B: Key Performance Indicators Summary", "19"),
            ]
            y = 110
            for entry_title, entry_page in toc_entries:
                page.insert_text(
                    pymupdf.Point(72, y),
                    entry_title,
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                )
                page.insert_text(
                    pymupdf.Point(500, y),
                    entry_page,
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                )
                y += 22

        elif section_type in ("table", "kpi_table"):
            # Table pages
            page.insert_text(
                pymupdf.Point(72, 72),
                section["title"],
                fontsize=18,
                fontname="hebo",
                color=(0, 0.2, 0.4),
            )
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
            shape.finish(color=(0, 0.2, 0.4), width=1.5)
            shape.commit()

            headers = section["headers"]
            rows = section["rows"]
            num_cols = len(headers)
            table_x = 72
            table_w = 451
            col_w = table_w / num_cols
            y_start = 110

            # Header row background
            shape2 = page.new_shape()
            shape2.draw_rect(pymupdf.Rect(table_x, y_start - 14, table_x + table_w, y_start + 6))
            shape2.finish(fill=(0, 0.2, 0.4))
            shape2.commit()

            for ci, h in enumerate(headers):
                page.insert_text(
                    pymupdf.Point(table_x + ci * col_w + 4, y_start),
                    h,
                    fontsize=9,
                    fontname="hebo",
                    color=(1, 1, 1),
                )

            y = y_start + 24
            for ri, row in enumerate(rows):
                if ri % 2 == 1:
                    shape3 = page.new_shape()
                    shape3.draw_rect(pymupdf.Rect(table_x, y - 14, table_x + table_w, y + 6))
                    shape3.finish(fill=(0.93, 0.93, 0.97))
                    shape3.commit()
                for ci, cell in enumerate(row):
                    page.insert_text(
                        pymupdf.Point(table_x + ci * col_w + 4, y),
                        cell,
                        fontsize=9,
                        fontname="helv",
                        color=(0, 0, 0),
                    )
                y += 22

        else:
            # Regular body page
            page.insert_text(
                pymupdf.Point(72, 72),
                section["title"],
                fontsize=18,
                fontname="hebo",
                color=(0, 0.2, 0.4),
            )
            # Underline
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
            shape.finish(color=(0, 0.2, 0.4), width=1.5)
            shape.commit()

            # Body text
            body_rect = pymupdf.Rect(72, 100, 523, 770)
            page.insert_textbox(
                body_rect,
                section.get("body", ""),
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

        # Footer on every page (except cover)
        if i > 0:
            page.insert_text(
                pymupdf.Point(72, page_height - 30),
                "Westfield University - Annual Research Performance Report 2024-2025",
                fontsize=8,
                fontname="heit",
                color=(0.5, 0.5, 0.5),
            )
            page.insert_text(
                pymupdf.Point(500, page_height - 30),
                f"Page {i + 1}",
                fontsize=8,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )

    doc.save(OUTPUT_PDF)
    doc.close()
    print(f'Report created: {OUTPUT_PDF} (20 pages)')


def main():
    os.makedirs(PAPERS_DIR, exist_ok=True)
    create_logo()
    create_report()

    # Open the PDF in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT_PDF}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


if __name__ == '__main__':
    import pymupdf
    main()
