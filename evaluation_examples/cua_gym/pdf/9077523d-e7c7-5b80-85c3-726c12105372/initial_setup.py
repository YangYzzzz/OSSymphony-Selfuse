"""
Initial Setup: Compare TOC bookmarks between two PDFs and write differences to a text file.
Task ID: pdf_cr_056
Domain: pdf

Creates v1.pdf and v2.pdf on the Desktop with different TOC (bookmark) entries.
The agent must compare them and produce toc_diff.txt.
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
DESKTOP = f'{WORKDIR}/Desktop'
V1_PATH = f'{DESKTOP}/v1.pdf'
V2_PATH = f'{DESKTOP}/v2.pdf'


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


def create_research_pdf(path, title, sections, toc_entries):
    """Create a realistic multi-page research-style PDF with given sections and TOC."""
    doc = pymupdf.open()

    for section_title, page_num, content_lines in sections:
        # Create pages up to the required page number
        while doc.page_count < page_num:
            page = doc.new_page(width=595, height=842)
            # Add a light footer with page number
            page.insert_text(
                pymupdf.Point(280, 810),
                f"- {doc.page_count} -",
                fontsize=9,
                fontname="tiro",
                color=(0.5, 0.5, 0.5),
            )

        # The section starts on this page (1-indexed, so page_num-1 is the index)
        page = doc[page_num - 1]

        # Section heading
        page.insert_text(
            pymupdf.Point(72, 80),
            section_title,
            fontsize=18,
            fontname="hebo",
            color=(0.1, 0.1, 0.4),
        )

        # Underline below heading
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 88), pymupdf.Point(523, 88))
        shape.finish(color=(0.2, 0.2, 0.6), width=1)
        shape.commit()

        # Body text
        y_pos = 110
        for line in content_lines:
            if y_pos > 780:
                break
            page.insert_text(
                pymupdf.Point(72, y_pos),
                line,
                fontsize=11,
                fontname="tiro",
                color=(0, 0, 0),
            )
            y_pos += 16

    # Add page footers on any pages that don't yet have them
    for i in range(doc.page_count):
        pass  # footers were added during creation

    # Set the document title
    doc.set_metadata({"title": title, "author": "Research Group Alpha"})

    # Set TOC (bookmarks)
    doc.set_toc(toc_entries)

    doc.save(path)
    doc.close()
    print(f"Created: {path} ({doc.page_count if False else 'done'})")


def create_initial():
    os.makedirs(DESKTOP, exist_ok=True)

    # --- v1.pdf: Original research paper ---
    v1_sections = [
        ("Introduction", 1, [
            "This study investigates the impact of renewable energy adoption on regional",
            "economic growth patterns across Southeast Asian countries from 2015 to 2024.",
            "",
            "The global transition toward sustainable energy sources has accelerated in",
            "recent years, driven by climate policy commitments and falling technology costs.",
            "Solar photovoltaic installations have grown at a compound annual rate of 22%,",
            "while wind energy capacity has expanded by 15% annually.",
            "",
            "Our research contributes to the existing literature by providing a comprehensive",
            "analysis of the employment multiplier effects associated with green energy",
            "investment in developing economies. We employ a panel data approach covering",
            "six countries over a ten-year period.",
            "",
            "The remainder of this paper is organized as follows. Section 2 describes our",
            "methodology and data sources. Section 3 presents the empirical results.",
        ]),
        ("Methods", 3, [
            "We utilize a fixed-effects panel regression model to estimate the relationship",
            "between renewable energy capacity additions and GDP growth at the provincial level.",
            "",
            "Data Sources:",
            "  - IRENA Renewable Energy Statistics (2015-2024)",
            "  - World Bank Development Indicators",
            "  - National statistical bureau employment surveys",
            "  - Bloomberg New Energy Finance investment data",
            "",
            "Our primary specification takes the form:",
            "",
            "  GDP_growth(i,t) = alpha + beta * RE_capacity(i,t) + gamma * X(i,t) + u(i) + e(i,t)",
            "",
            "where RE_capacity represents installed renewable capacity in megawatts,",
            "X is a vector of control variables including trade openness, human capital",
            "indices, and infrastructure quality scores.",
            "",
            "We address potential endogeneity through instrumental variable estimation,",
            "using solar irradiance and average wind speed as instruments for renewable",
            "energy capacity.",
        ]),
        ("Results", 5, [
            "Table 1 presents the baseline regression results. The coefficient on renewable",
            "energy capacity is positive and statistically significant at the 1% level.",
            "",
            "Key Findings:",
            "  1. Each additional gigawatt of solar capacity is associated with a 0.34",
            "     percentage point increase in provincial GDP growth.",
            "  2. Wind energy investments show a slightly larger effect (0.41 pp) but",
            "     with wider confidence intervals.",
            "  3. The employment multiplier for renewable energy is 2.7x, compared to",
            "     1.4x for fossil fuel investments.",
            "",
            "Robustness checks using alternative specifications and sample restrictions",
            "confirm the stability of our main estimates. The instrumental variable",
            "results yield point estimates that are 15-20% larger than OLS, suggesting",
            "modest downward bias in the baseline specification.",
            "",
            "Regional heterogeneity analysis reveals that the economic benefits are",
            "concentrated in provinces with pre-existing manufacturing capacity and",
            "higher levels of workforce education.",
        ]),
    ]
    v1_toc = [
        [1, "Introduction", 1],
        [1, "Methods", 3],
        [1, "Results", 5],
    ]
    create_research_pdf(V1_PATH, "Renewable Energy and Regional Growth v1", v1_sections, v1_toc)

    # --- v2.pdf: Revised version with additional sections and page shifts ---
    v2_sections = [
        ("Introduction", 1, [
            "This study investigates the impact of renewable energy adoption on regional",
            "economic growth patterns across Southeast Asian countries from 2015 to 2024.",
            "",
            "The global transition toward sustainable energy sources has accelerated in",
            "recent years, driven by climate policy commitments and falling technology costs.",
            "Solar photovoltaic installations have grown at a compound annual rate of 22%,",
            "while wind energy capacity has expanded by 15% annually.",
            "",
            "Our research contributes to the existing literature by providing a comprehensive",
            "analysis of the employment multiplier effects associated with green energy",
            "investment in developing economies.",
        ]),
        ("Background", 2, [
            "The theoretical framework for understanding renewable energy's economic impact",
            "draws on several strands of the development economics literature.",
            "",
            "Endogenous growth theory suggests that technological change in the energy sector",
            "can generate sustained increases in total factor productivity. The seminal work",
            "of Romer (1990) and Aghion & Howitt (1992) provides the foundation for models",
            "in which clean energy innovation drives long-run growth.",
            "",
            "Empirical studies by Apergis & Payne (2010) established a positive relationship",
            "between renewable energy consumption and economic output for a panel of OECD",
            "countries. More recent work by Bhattacharya et al. (2016) extended this finding",
            "to developing economies, though with smaller effect sizes.",
            "",
            "Regional innovation systems theory (Cooke, 2001) highlights the importance of",
            "institutional capacity and knowledge networks in translating energy investments",
            "into broader economic benefits.",
        ]),
        ("Methods", 4, [
            "We utilize a fixed-effects panel regression model to estimate the relationship",
            "between renewable energy capacity additions and GDP growth at the provincial level.",
            "",
            "Data Sources:",
            "  - IRENA Renewable Energy Statistics (2015-2024)",
            "  - World Bank Development Indicators",
            "  - National statistical bureau employment surveys",
            "  - Bloomberg New Energy Finance investment data",
            "",
            "Our primary specification takes the form:",
            "",
            "  GDP_growth(i,t) = alpha + beta * RE_capacity(i,t) + gamma * X(i,t) + u(i) + e(i,t)",
            "",
            "We address potential endogeneity through instrumental variable estimation,",
            "using solar irradiance and average wind speed as instruments.",
        ]),
        ("Results", 6, [
            "Table 1 presents the baseline regression results. The coefficient on renewable",
            "energy capacity is positive and statistically significant at the 1% level.",
            "",
            "Key Findings:",
            "  1. Each additional gigawatt of solar capacity is associated with a 0.34",
            "     percentage point increase in provincial GDP growth.",
            "  2. Wind energy investments show a slightly larger effect (0.41 pp).",
            "  3. The employment multiplier for renewable energy is 2.7x.",
            "",
            "Robustness checks confirm the stability of our main estimates.",
        ]),
        ("Discussion", 8, [
            "Our findings have important implications for energy policy in developing",
            "economies. The positive growth effects of renewable energy investment suggest",
            "that the energy transition need not come at the cost of economic development.",
            "",
            "The heterogeneity in our results points to the importance of complementary",
            "investments in human capital and infrastructure. Provinces that lack a skilled",
            "manufacturing workforce may not fully benefit from renewable energy deployment.",
            "",
            "Policy Recommendations:",
            "  1. Integrate workforce development programs with renewable energy targets.",
            "  2. Prioritize grid infrastructure upgrades in regions with high solar/wind",
            "     potential but limited connectivity.",
            "  3. Establish regional innovation hubs to facilitate technology transfer and",
            "     knowledge spillovers from the clean energy sector.",
            "",
            "Limitations of this study include the relatively short time horizon and the",
            "challenge of fully controlling for unobserved provincial characteristics.",
            "Future research should incorporate longer time series as additional data",
            "becomes available.",
        ]),
    ]
    v2_toc = [
        [1, "Introduction", 1],
        [1, "Background", 2],
        [1, "Methods", 4],
        [1, "Results", 6],
        [1, "Discussion", 8],
    ]
    create_research_pdf(V2_PATH, "Renewable Energy and Regional Growth v2", v2_sections, v2_toc)

    print(f"Initial file created: {V1_PATH}")
    print(f"Initial file created: {V2_PATH}")

    # Verify toc_diff.txt does NOT exist (negative constraint)
    diff_path = f'{DESKTOP}/toc_diff.txt'
    if os.path.exists(diff_path):
        os.remove(diff_path)
        print(f"Removed pre-existing {diff_path}")

    # GUI-ready startup: open both PDFs in Evince
    launch_gui(f'evince "{V1_PATH}"', delay_sec=2.0)
    launch_gui(f'evince "{V2_PATH}"', delay_sec=2.0)
    print("GUI_READY: launched Evince for both PDFs with DISPLAY=:0")


create_initial()
