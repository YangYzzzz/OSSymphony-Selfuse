"""
Initial Setup: Create grant_proposal.pdf on the VM Desktop
Task ID: pdf_basic_049
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Desktop'
TASK_ID = 'grant_proposal'
OUTPUT = f'{WORKDIR}/{TASK_ID}.pdf'


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

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792

    # Helper to add a standard page
    def add_page(title, body_lines):
        page = doc.new_page(width=W, height=H)
        # Title
        page.insert_text(
            pymupdf.Point(72, 72),
            title,
            fontsize=16,
            fontname="hebo",
            color=(0, 0, 0),
        )
        # Body
        y = 110
        for line in body_lines:
            page.insert_text(
                pymupdf.Point(72, y),
                line,
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
            )
            y += 18
        return page

    # Page 1 — Cover / Title
    add_page(
        "Grant Proposal: Advancing Sustainable Urban Infrastructure",
        [
            "Submitted by: Dr. Evelyn Torres, Principal Investigator",
            "Institution: Metropolitan Research University",
            "Department: Civil Engineering and Environmental Studies",
            "Submission Date: March 15, 2026",
            "Funding Agency: National Science Foundation — Urban Systems Program",
            "",
            "Co-Investigators:",
            "  Dr. Marcus Webb, Urban Planning",
            "  Dr. Priya Nair, Environmental Science",
            "  Prof. James Alcott, Data Analytics",
            "",
            "Contact: e.torres@mru.edu | +1 (312) 555-0192",
        ],
    )

    # Page 2 — Abstract
    add_page(
        "Abstract",
        [
            "This proposal seeks funding to investigate sustainable approaches to urban",
            "infrastructure development, focusing on energy efficiency, waste reduction,",
            "and community resilience. The research integrates multidisciplinary methods",
            "from civil engineering, environmental science, and data analytics.",
            "",
            "Key objectives include: (1) characterizing current infrastructure inefficiencies",
            "in mid-sized metropolitan areas, (2) developing predictive models for resource",
            "consumption, and (3) piloting intervention strategies with measurable outcomes.",
            "",
            "The anticipated deliverables are a set of validated models, a policy brief,",
            "and an open-access dataset for use by other researchers and municipalities.",
            "",
            "Duration: 18 months    |    Funding Requested: $125,000",
        ],
    )

    # Page 3 — Introduction
    add_page(
        "1. Introduction",
        [
            "Urban infrastructure underpins modern society, yet aging systems and rapid",
            "population growth strain both environmental and financial resources. According",
            "to the American Society of Civil Engineers' 2023 Infrastructure Report Card,",
            "the United States faces a $2.6 trillion infrastructure funding gap over ten years.",
            "",
            "Sustainable infrastructure development offers a path toward resilience, but",
            "comprehensive data-driven approaches remain scarce at the municipal level.",
            "Most existing studies focus on large metropolitan areas (population > 1 million),",
            "leaving mid-sized cities (population 200,000–500,000) underserved by research.",
            "",
            "This project addresses that gap by partnering with three mid-sized cities:",
            "  - Lakewood Falls, IL (pop. 315,000)",
            "  - Bridgemont, OH (pop. 278,000)",
            "  - Riverdale Junction, TX (pop. 422,000)",
        ],
    )

    # Page 4 — Background and Literature Review
    add_page(
        "2. Background and Literature Review",
        [
            "The field of sustainable infrastructure has grown considerably in the past decade.",
            "Landmark studies by Chen et al. (2021) and Morales & Singh (2022) established",
            "baseline metrics for energy consumption in urban water systems. Building on this",
            "work, our team has previously demonstrated (Torres et al., 2024) that sensor-based",
            "monitoring can reduce maintenance costs by 18-24% in comparable municipalities.",
            "",
            "Gaps in current knowledge include:",
            "  - Lack of longitudinal data on infrastructure decay rates in mid-sized cities",
            "  - Absence of validated predictive models for resource use under climate scenarios",
            "  - Limited community engagement frameworks for infrastructure decision-making",
            "",
            "This proposal directly addresses all three gaps through empirical fieldwork,",
            "computational modeling, and structured stakeholder workshops.",
            "",
            "Key references: ASCE (2023), Chen et al. (2021), Torres et al. (2024).",
        ],
    )

    # Page 5 — Research Objectives
    add_page(
        "3. Research Objectives",
        [
            "The overarching goal is to develop evidence-based strategies for sustainable",
            "urban infrastructure management in mid-sized cities.",
            "",
            "Specific Objectives:",
            "  Objective 1: Characterize current inefficiencies in water, energy, and",
            "               transportation infrastructure across three partner cities.",
            "",
            "  Objective 2: Build and validate predictive models using machine learning",
            "               techniques applied to longitudinal infrastructure sensor data.",
            "",
            "  Objective 3: Co-design with municipal stakeholders a set of pilot",
            "               intervention strategies and measure their outcomes.",
            "",
            "  Objective 4: Disseminate findings via peer-reviewed publications,",
            "               policy briefs, and open-access datasets.",
        ],
    )

    # Page 6 — Methodology
    add_page(
        "4. Methodology",
        [
            "Phase 1 (Months 1-5): Data Collection",
            "  - Deploy IoT sensor arrays at 45 infrastructure nodes per city (135 total)",
            "  - Collect baseline data: energy use, water flow, traffic counts, waste volumes",
            "  - Conduct structured interviews with 20 municipal engineers per city",
            "",
            "Phase 2 (Months 6-12): Analysis and Modeling",
            "  - Clean and validate collected datasets using automated QA pipelines",
            "  - Train predictive models (LSTM, XGBoost, Transformer architectures)",
            "  - Validate models using 20% held-out test set; target RMSE < 5%",
            "",
            "Phase 3 (Months 13-18): Pilot Interventions and Dissemination",
            "  - Implement 3 pilot interventions per city (9 total) based on model outputs",
            "  - Measure outcomes at 3-month and 6-month intervals",
            "  - Write and submit 2 journal articles and 1 policy brief",
        ],
    )

    # Page 7 — Team and Qualifications
    add_page(
        "5. Project Team and Qualifications",
        [
            "Dr. Evelyn Torres (PI) — Professor of Civil Engineering, MRU",
            "  Ph.D., Stanford University; 15 years experience in urban infrastructure",
            "  PI on 6 prior NSF-funded projects totaling $3.2M; 48 peer-reviewed publications",
            "",
            "Dr. Marcus Webb (Co-I) — Associate Professor of Urban Planning, MRU",
            "  Ph.D., MIT; specialist in stakeholder engagement and policy design",
            "  Lead author of the Urban Resilience Framework (2023, Urban Studies Press)",
            "",
            "Dr. Priya Nair (Co-I) — Assistant Professor of Environmental Science, MRU",
            "  Ph.D., UC Berkeley; expertise in climate-infrastructure interactions",
            "  Postdoctoral Fellow, Lawrence Berkeley National Laboratory (2019-2022)",
            "",
            "Prof. James Alcott (Co-I) — Data Science Lead, MRU Computational Center",
            "  M.Sc., Carnegie Mellon University; 10 years applied ML in civil systems",
        ],
    )

    # Page 8 — Budget
    add_page(
        "6. Budget Justification",
        [
            "The project requires the following resource categories:",
            "",
            "Personnel (60% of budget):",
            "  - PI effort: 2 months summer salary ($18,000)",
            "  - Co-Investigator effort: 3 x 1.5 months ($27,000)",
            "  - Graduate Research Assistants: 2 x 12 months ($30,000)",
            "",
            "Equipment and Supplies ($12,500):",
            "  - IoT sensor units (135 units x $75 each): $10,125",
            "  - Calibration tools and consumables: $2,375",
            "",
            "Travel ($6,500):",
            "  - Site visits to 3 partner cities (4 trips each): $4,500",
            "  - Conference travel (2 national conferences): $2,000",
            "",
            "Indirect Costs ($18,000): 26% of modified total direct costs",
            "",
            "total budget: $125,000",
        ],
    )

    # Page 9 — Timeline
    add_page(
        "7. Project Timeline and Milestones",
        [
            "The research is structured as an 18-month effort with clear milestones.",
            "",
            "project timeline: 18 months",
            "",
            "Milestone Schedule:",
            "  Month 1:    Project kickoff; IRB submission; partner city MOUs signed",
            "  Month 2-3:  Sensor procurement and deployment begins",
            "  Month 5:    Baseline data collection complete (135 nodes)",
            "  Month 6:    Interim progress report submitted to NSF",
            "  Month 8:    Initial model training complete; preliminary results",
            "  Month 10:   Stakeholder workshops in all 3 cities",
            "  Month 12:   Final predictive models validated; pilot design complete",
            "  Month 13:   Pilot interventions launched",
            "  Month 15:   First journal article submitted",
            "  Month 16:   3-month pilot outcomes measured and reported",
            "  Month 18:   Project close-out; final report; dataset published",
        ],
    )

    # Page 10 — Broader Impacts
    add_page(
        "8. Broader Impacts",
        [
            "This research will produce both direct and indirect societal benefits:",
            "",
            "Direct Impacts:",
            "  - Partner cities will have actionable data to optimize infrastructure spending",
            "  - Open-access dataset will enable future research by other teams",
            "  - Policy brief will be distributed to 200+ US municipalities via ICMA network",
            "",
            "Indirect Impacts:",
            "  - Two graduate students will receive multidisciplinary research training",
            "  - Undergraduate REU participants (4 per year) will gain research experience",
            "  - Methodology is transferable to international contexts (planned follow-on work)",
            "",
            "Diversity and Inclusion:",
            "  - Active recruitment of graduate students from underrepresented groups",
            "  - Partner cities include communities with significant minority populations",
        ],
    )

    # Page 11 — Evaluation Plan
    add_page(
        "9. Evaluation Plan",
        [
            "Project success will be measured against quantitative metrics:",
            "",
            "Research Quality Metrics:",
            "  - Model RMSE for resource consumption predictions: target < 5%",
            "  - Number of peer-reviewed publications: target >= 2",
            "  - Dataset citation count at 24 months post-publication: target >= 10",
            "",
            "Implementation Metrics:",
            "  - Sensor uptime across all 135 nodes: target >= 95%",
            "  - Stakeholder workshop attendance: target >= 15 per city",
            "  - Pilot intervention adoption rate by cities: target >= 67% (2 of 3 pilots)",
            "",
            "An external evaluator, Dr. Rosa Kim (University of Michigan), will conduct",
            "annual reviews and provide independent assessment reports to NSF.",
            "",
            "Progress reports will be submitted semi-annually per NSF requirements.",
        ],
    )

    # Page 12 — Prior Work
    add_page(
        "10. Prior NSF Support",
        [
            "Dr. Torres: NSF Award #1823456 (2020-2023)",
            "  Title: Sensor-Driven Maintenance Optimization for Water Distribution Systems",
            "  Amount: $487,000 | Duration: 36 months",
            "  Outcomes: 3 journal articles, 1 patent (pending), open-source software toolkit",
            "  Intellectual Merit: Demonstrated 21% cost reduction in pilot municipalities",
            "  Broader Impacts: Software toolkit downloaded 1,200+ times; 3 grad students trained",
            "",
            "Dr. Webb: NSF Award #1956789 (2021-2024)",
            "  Title: Community Resilience Frameworks for Mid-Sized Cities",
            "  Amount: $275,000 | Duration: 36 months",
            "  Outcomes: 2 journal articles, 1 book chapter, Urban Resilience Toolkit",
            "  Intellectual Merit: New theoretical model of civic infrastructure governance",
            "  Broader Impacts: Framework adopted by 14 municipalities",
        ],
    )

    # Page 13 — Facilities and Resources
    add_page(
        "11. Facilities and Resources",
        [
            "Metropolitan Research University provides state-of-the-art facilities:",
            "",
            "Computational Resources:",
            "  - MRU High-Performance Computing cluster: 1,024 CPU cores, 4 GPU nodes",
            "  - 500 TB networked storage for large-scale sensor data",
            "  - Licensed software: MATLAB, ArcGIS, Tableau",
            "",
            "Laboratory Facilities:",
            "  - Infrastructure Testing Lab (4,500 sq ft) with calibration equipment",
            "  - Environmental Monitoring Lab with certified analytical instruments",
            "",
            "Partner City Support:",
            "  - Letters of support from public works directors in all 3 cities (attached)",
            "  - Access to existing infrastructure management systems and GIS databases",
            "  - Dedicated point-of-contact staff (0.25 FTE per city)",
        ],
    )

    # Page 14 — Data Management Plan
    add_page(
        "12. Data Management Plan",
        [
            "All data collected in this project will be managed in accordance with NSF",
            "data sharing policies and FAIR principles (Findable, Accessible, Interoperable,",
            "Reusable).",
            "",
            "Data Types and Volumes:",
            "  - Continuous sensor time-series: ~2 TB/year per city (6 TB total)",
            "  - Interview transcripts and qualitative data: ~50 GB",
            "  - Processed model outputs and derived datasets: ~100 GB",
            "",
            "Storage and Backup:",
            "  - Primary storage on MRU HPC cluster with nightly automated backups",
            "  - Secondary backup on university cloud (Microsoft Azure, encrypted at rest)",
            "",
            "Sharing and Archival:",
            "  - Raw sensor data archived in NSF-compliant repository (Zenodo) at project end",
            "  - Processed datasets released under CC BY 4.0 license",
            "  - Code released on GitHub under MIT license",
        ],
    )

    # Page 15 — References
    add_page(
        "References",
        [
            "ASCE (2023). 2023 Report Card for America's Infrastructure.",
            "  American Society of Civil Engineers, Reston, VA.",
            "",
            "Chen, L., Park, J., & Hernandez, M. (2021). Energy efficiency benchmarks for",
            "  urban water distribution systems. Water Resources Research, 57(4), e2020WR029012.",
            "",
            "Morales, R., & Singh, K. (2022). Predictive maintenance in aging urban",
            "  infrastructure: A systematic review. Urban Engineering, 14(2), 88-104.",
            "",
            "Torres, E., Webb, M., & Nair, P. (2024). Sensor-based infrastructure monitoring",
            "  in mid-sized cities: Lessons from three case studies.",
            "  Journal of Infrastructure Systems, 30(1), 04023045.",
            "",
            "National Science Foundation (2025). Urban Systems Research Program Guidelines.",
            "  NSF Publication 25-012, Alexandria, VA.",
        ],
    )

    # Save
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
