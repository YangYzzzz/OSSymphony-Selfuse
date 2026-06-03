"""
Initial Setup: Create a 30-page group project PDF with mixed annotations
Task ID: pdf_fm_041
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_041'
DOC_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOC_DIR}/group_project.pdf'


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
    os.makedirs(DOC_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Create 30 pages of realistic group project content ---
    chapters = [
        ("Chapter 1: Introduction", [
            "This group project investigates the impact of renewable energy adoption on urban infrastructure development across major metropolitan areas in the Pacific Northwest region.",
            "The research team consists of four members: Dr. Amelia Rodriguez (Project Lead), James Whitfield (Data Analysis), Priya Sharma (Field Research), and Tobias Mller (Technical Writing).",
            "Our primary objective is to evaluate how cities with populations exceeding 250,000 have integrated solar and wind energy systems into their existing power grids between 2018 and 2024.",
            "Secondary objectives include assessing cost-benefit ratios for residential solar panel installations and documenting regulatory frameworks that either facilitate or hinder renewable energy adoption.",
            "The significance of this research lies in providing actionable policy recommendations for mid-sized cities considering large-scale renewable energy transitions.",
        ]),
        ("Chapter 2: Literature Review", [
            "Anderson et al. (2021) conducted a comprehensive meta-analysis of 47 studies examining renewable energy integration in North American cities, finding an average cost reduction of 23% over five years.",
            "Chen and Nakamura (2022) provided a critical examination of policy frameworks, noting that cities with dedicated renewable energy offices achieved 40% faster adoption rates.",
            "The Brookings Institution report (2023) highlighted that federal tax incentives accounted for approximately 35% of new residential solar installations in 2022.",
            "A contrasting perspective from Volkov (2020) argued that grid infrastructure limitations remain the primary bottleneck, with upgrade costs often underestimated by 15-30%.",
            "Recent work by Okonkwo and Larsson (2024) introduced a novel cost modeling framework that accounts for supply chain volatility, seasonal demand fluctuations, and labor market constraints.",
        ]),
        ("Chapter 3: Methodology", [
            "This study employs a mixed-methods research design combining quantitative analysis of energy production data with qualitative interviews of municipal energy directors.",
            "Quantitative data was collected from 12 cities across Washington, Oregon, and British Columbia, covering energy production records from January 2018 through December 2024.",
            "Semi-structured interviews were conducted with 36 municipal officials, energy company representatives, and community organizers between March and August 2024.",
            "Statistical analysis utilized multiple regression models controlling for population density, median household income, existing infrastructure age, and climate zone classification.",
            "Interview transcripts were analyzed using thematic coding with NVivo 14, with inter-rater reliability assessed through Cohen's kappa (achieving k = 0.83 across all categories).",
        ]),
        ("Chapter 4: Data Collection", [
            "Primary data sources included the U.S. Energy Information Administration (EIA), BC Hydro annual reports, and municipal energy department databases.",
            "Portland reported 847 MW of installed solar capacity by Q4 2024, representing a 156% increase from 2018 baseline measurements of 331 MW.",
            "Seattle's wind energy contribution reached 12.4% of total grid capacity, with the Cedar Falls wind farm producing 2,340 GWh annually.",
            "Vancouver's district energy system expansion covered 14 new neighborhoods between 2020-2024, serving approximately 45,000 residential units.",
            "Data quality assurance involved cross-referencing EIA reports with state-level utility filings, resolving 23 discrepancies across the dataset.",
        ]),
        ("Chapter 5: Quantitative Results", [
            "Regression analysis reveals a statistically significant positive relationship between dedicated renewable energy policy offices and adoption rates (beta = 0.42, p < 0.001).",
            "Cities with streamlined permitting processes showed 28% faster installation timelines, with average residential solar deployment dropping from 47 to 34 days.",
            "The cost per kilowatt-hour for solar energy decreased from $0.089 in 2018 to $0.052 in 2024 across the study region, a 41.6% reduction.",
            "Wind energy capacity utilization averaged 31.7% across all monitored installations, with coastal facilities achieving 38.2% compared to 26.1% for inland sites.",
            "Total renewable energy investment in the 12 study cities reached $4.7 billion over the study period, generating an estimated 23,400 direct jobs.",
        ]),
        ("Chapter 6: Qualitative Findings", [
            "Interview analysis identified five primary themes: political leadership, community engagement, workforce development, infrastructure readiness, and financial accessibility.",
            "Director Sarah Blackwell (Portland Energy Office) emphasized that 'consistent political championing across election cycles was the single most critical factor in our success.'",
            "Community opposition was reported as a significant barrier in 4 of 12 cities, primarily related to visual impact of wind turbines and concerns about property values.",
            "Workforce development emerged as an unexpected challenge, with 8 of 12 cities reporting skilled labor shortages in solar panel installation and grid integration.",
            "Financial accessibility programs targeting low-income households increased adoption by 67% in participating neighborhoods compared to city-wide averages.",
        ]),
        ("Chapter 7: Case Study - Portland", [
            "Portland serves as the study's primary success case, having achieved 45% renewable energy grid contribution by December 2024.",
            "The Portland Clean Energy Fund, approved by voters in 2018, generated $61 million annually for clean energy projects in underserved communities.",
            "Key infrastructure investments included the $180 million Southeast Grid Modernization project, completed in 2023, which reduced transmission losses by 8.3%.",
            "Residential solar adoption reached 34,200 installations by end of 2024, supported by a tiered rebate program offering $2,500-$7,500 per household.",
            "Portland's experience demonstrates that combining voter-approved funding, streamlined permitting, and targeted community programs creates a self-reinforcing adoption cycle.",
        ]),
        ("Chapter 8: Case Study - Seattle", [
            "Seattle's approach focused primarily on wind energy and hydroelectric modernization rather than solar, reflecting its unique geographic and climatic conditions.",
            "The City Light utility company invested $340 million in grid modernization between 2019-2024, achieving 89% renewable energy sourcing.",
            "The South Park Community Solar project provided 2,400 low-income households with access to solar energy without requiring rooftop installation.",
            "Seattle's Green Building Standard, updated in 2022, requires all new commercial construction over 50,000 sq ft to incorporate on-site renewable energy generation.",
            "Challenge areas included aging hydroelectric infrastructure, with the Boundary Dam requiring $95 million in upgrades to maintain efficiency above 85%.",
        ]),
        ("Chapter 9: Comparative Analysis", [
            "Cross-city comparison reveals three distinct adoption models: policy-driven (Portland, Eugene), market-driven (Bellevue, Boise), and hybrid (Vancouver, Tacoma).",
            "Policy-driven cities achieved higher adoption rates (avg. 38% renewable grid share) but at higher per-capita public investment ($847 vs $312 for market-driven).",
            "Market-driven cities showed faster private sector innovation but greater inequality in access, with affluent neighborhoods adopting at 4.2x the rate of lower-income areas.",
            "The hybrid model, exemplified by Vancouver, balanced public investment with private incentives, achieving 33% grid share with the lowest reported community opposition.",
            "Infrastructure age proved the strongest predictor of implementation cost, with cities possessing grid infrastructure older than 40 years spending 2.1x more on integration.",
        ]),
        ("Chapter 10: Discussion", [
            "Our findings largely align with Anderson et al. (2021) regarding cost reductions, though we observed faster decreases in the Pacific Northwest than their national average.",
            "The workforce development challenge identified in our qualitative analysis represents a critical gap in existing literature, which has focused primarily on policy and technology.",
            "We propose a four-pillar framework for renewable energy transition: Political Commitment, Community Inclusion, Workforce Readiness, and Infrastructure Modernization.",
            "The framework acknowledges that success requires simultaneous progress across all four pillars; cities that excelled in policy but neglected workforce saw diminishing returns.",
            "Limitations include the geographic concentration in the Pacific Northwest, which may limit generalizability to regions with different climatic and political contexts.",
        ]),
    ]

    page_idx = 0
    for ch_idx, (title, paragraphs) in enumerate(chapters):
        # Each chapter gets 3 pages
        for sub_page in range(3):
            page = doc.new_page(width=595, height=842)  # A4

            # Header
            page.insert_text(
                pymupdf.Point(72, 50),
                title,
                fontsize=14 if sub_page == 0 else 10,
                fontname="hebo" if sub_page == 0 else "helv",
                color=(0, 0, 0.4),
            )

            # Horizontal rule
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 60), pymupdf.Point(523, 60))
            shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
            shape.commit()

            # Body text
            y_pos = 85
            if sub_page == 0:
                for para in paragraphs:
                    rect = pymupdf.Rect(72, y_pos, 523, y_pos + 80)
                    page.insert_textbox(
                        rect,
                        para,
                        fontsize=11,
                        fontname="tiro",
                        color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY,
                    )
                    y_pos += 85
            elif sub_page == 1:
                continuation_texts = [
                    f"Continuing the analysis from the previous section, we examine additional data points relevant to {title.split(': ')[1] if ': ' in title else title}.",
                    f"Table {ch_idx + 1}.{sub_page}: Summary statistics for the metrics discussed in this chapter show consistent trends across all twelve study cities.",
                    "The data reveals several important patterns that merit further investigation in subsequent phases of this research project.",
                    "Cross-referencing these findings with external validation datasets confirms the robustness of our analytical framework and methodology.",
                    f"Additional supporting materials and raw data tables are provided in Appendix {chr(65 + ch_idx)}.",
                ]
                for text in continuation_texts:
                    rect = pymupdf.Rect(72, y_pos, 523, y_pos + 65)
                    page.insert_textbox(rect, text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
                    y_pos += 70
            else:
                summary_texts = [
                    f"Section {ch_idx + 1} Summary: The key findings presented in this chapter provide critical evidence for the project's overall thesis.",
                    "The methodological approach employed ensures reproducibility and allows for future longitudinal studies to build upon this foundation.",
                    "Peer review feedback from Dr. Katherine Wells (University of Washington) and Dr. Raj Patel (Simon Fraser University) has been incorporated into this revision.",
                    f"References specific to this chapter are listed in the bibliography section under category {chr(65 + ch_idx)}.",
                ]
                for text in summary_texts:
                    rect = pymupdf.Rect(72, y_pos, 523, y_pos + 65)
                    page.insert_textbox(rect, text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
                    y_pos += 70

            # Footer
            page.insert_text(
                pymupdf.Point(280, 820),
                str(page_idx + 1),
                fontsize=9,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )

            page_idx += 1

    # --- Add Annotations ---
    # 15 highlights spread across pages
    highlight_specs = [
        (0, "renewable energy adoption"),
        (1, "Amelia Rodriguez"),
        (3, "meta-analysis"),
        (5, "mixed-methods"),
        (7, "Energy Information Administration"),
        (9, "statistically significant"),
        (11, "political leadership"),
        (13, "Portland Clean Energy Fund"),
        (15, "grid modernization"),
        (17, "South Park Community Solar"),
        (19, "Green Building Standard"),
        (21, "Cross-city comparison"),
        (23, "four-pillar framework"),
        (25, "Political Commitment"),
        (27, "bibliography"),
    ]

    for page_num, search_text in highlight_specs:
        if page_num < doc.page_count:
            page = doc[page_num]
            instances = page.search_for(search_text)
            if instances:
                annot = page.add_highlight_annot(instances[0])
                annot.set_colors(stroke=(1, 1, 0))  # yellow highlight
                annot.update()
            else:
                # Fallback: create highlight at a fixed position
                rect = pymupdf.Rect(72, 100, 300, 115)
                annot = page.add_highlight_annot(rect)
                annot.set_colors(stroke=(1, 1, 0))
                annot.update()

    # 8 sticky notes spread across pages
    sticky_specs = [
        (0, pymupdf.Point(520, 80), "Review introduction scope with team"),
        (2, pymupdf.Point(520, 150), "Check Anderson et al. citation format"),
        (6, pymupdf.Point(520, 200), "Verify NVivo coding categories"),
        (10, pymupdf.Point(520, 120), "Add confidence intervals to table"),
        (14, pymupdf.Point(520, 180), "Cross-reference with census data"),
        (18, pymupdf.Point(520, 100), "Update Seattle population figures"),
        (22, pymupdf.Point(520, 250), "Discuss framework limitations"),
        (28, pymupdf.Point(520, 150), "Final proofreading needed"),
    ]

    for page_num, point, content in sticky_specs:
        if page_num < doc.page_count:
            page = doc[page_num]
            annot = page.add_text_annot(point, content, icon="Note")
            annot.set_colors(stroke=(1, 0.8, 0))  # orange
            annot.update()

    # 5 underlines spread across pages
    underline_specs = [
        (4, "Primary data sources"),
        (8, "cost per kilowatt-hour"),
        (12, "Portland serves as the study"),
        (20, "policy-driven"),
        (26, "Limitations include"),
    ]

    for page_num, search_text in underline_specs:
        if page_num < doc.page_count:
            page = doc[page_num]
            instances = page.search_for(search_text)
            if instances:
                annot = page.add_underline_annot(instances[0])
                annot.set_colors(stroke=(0, 0, 1))  # blue underline
                annot.update()
            else:
                rect = pymupdf.Rect(72, 100, 350, 115)
                annot = page.add_underline_annot(rect)
                annot.set_colors(stroke=(0, 0, 1))
                annot.update()

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify annotation counts
    doc = pymupdf.open(OUTPUT)
    h_count, s_count, u_count = 0, 0, 0
    for page in doc:
        for annot in page.annots():
            atype = annot.type[1]
            if atype == "Highlight":
                h_count += 1
            elif atype == "Text":
                s_count += 1
            elif atype == "Underline":
                u_count += 1
    doc.close()
    print(f'Annotations: {h_count} highlights, {s_count} sticky notes, {u_count} underlines')
    print(f'Total: {h_count + s_count + u_count}')

    # GUI-ready startup: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
