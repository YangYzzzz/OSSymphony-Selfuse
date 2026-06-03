"""
Initial Setup: Create a non-linearized 8-page article PDF for linearization task
Task ID: pdf_gf1_034
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_034'
DOCDIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCDIR}/article.pdf'


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
    os.makedirs(DOCDIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792
    LEFT = 72
    RIGHT = W - 72
    TEXT_W = RIGHT - LEFT

    # --- Page 1: Title Page ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(LEFT, 200), "Advances in Renewable Energy Storage:", fontsize=24, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(LEFT, 235), "A Comprehensive Review of Battery Technologies", fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(LEFT, 290), "Dr. Elena Vasquez, Prof. James Hartfield, Dr. Mei-Lin Chang", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(LEFT, 315), "Institute of Sustainable Energy Research", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(LEFT, 335), "University of Pacific Northwest", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(LEFT, 375), "Published: March 2025", fontsize=11, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(LEFT, 395), "Journal of Energy Systems, Vol. 42, Issue 3, pp. 1-47", fontsize=10, fontname="heit", color=(0.4, 0.4, 0.4))

    # --- Page 2: Abstract & Introduction ---
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT, y), "Abstract", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 30
    abstract = (
        "The rapid expansion of renewable energy generation has intensified the demand for efficient, "
        "scalable, and cost-effective energy storage solutions. This review examines the current state "
        "of battery technologies, focusing on lithium-ion, solid-state, sodium-ion, and flow battery "
        "systems. We evaluate performance metrics including energy density, cycle life, safety profiles, "
        "and manufacturing scalability. Our analysis of 247 peer-reviewed studies from 2020-2025 reveals "
        "that solid-state batteries show the most promising trajectory for grid-scale deployment, with "
        "projected cost reductions of 60% by 2030. However, sodium-ion batteries present compelling "
        "advantages for stationary storage due to raw material abundance and lower environmental impact."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 130)
    page.insert_textbox(rect, abstract, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    y = 240
    page.insert_text(pymupdf.Point(LEFT, y), "1. Introduction", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 28
    intro = (
        "Global energy consumption continues to rise at an annual rate of 2.1%, driven by population "
        "growth, industrialization in developing economies, and the electrification of transportation. "
        "The International Energy Agency (IEA) projects that renewable sources will account for 45% of "
        "global electricity generation by 2030, up from 29% in 2020. This transition creates an urgent "
        "need for energy storage systems that can manage the intermittent nature of solar and wind power.\n\n"
        "Battery energy storage systems (BESS) have emerged as the primary technology for addressing this "
        "challenge. The global BESS market reached $13.4 billion in 2024, with projections indicating growth "
        "to $42 billion by 2030 (Bloomberg New Energy Finance, 2024). This growth is fueled by declining "
        "battery costs, supportive policy frameworks, and increasing grid instability events.\n\n"
        "This review aims to provide a comprehensive assessment of the four most promising battery "
        "technologies for grid-scale energy storage: lithium-ion (Li-ion), solid-state, sodium-ion (Na-ion), "
        "and redox flow batteries. We evaluate each technology across five critical dimensions: energy density, "
        "cycle life, safety, cost, and environmental impact."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 350)
    page.insert_textbox(rect, intro, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 3: Lithium-ion Technologies ---
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT, y), "2. Lithium-Ion Battery Technologies", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 28
    page.insert_text(pymupdf.Point(LEFT, y), "2.1 Current State of the Art", fontsize=13, fontname="hebo", color=(0.2, 0.2, 0.4))
    y += 22
    liion = (
        "Lithium-ion batteries remain the dominant technology in both portable electronics and electric "
        "vehicles, with a combined market share exceeding 92% of rechargeable battery sales. The technology "
        "has benefited from decades of incremental improvements, with energy densities increasing from "
        "90 Wh/kg in 1991 to over 300 Wh/kg in current commercial cells.\n\n"
        "The most widely deployed chemistries for grid storage include lithium iron phosphate (LFP) and "
        "nickel manganese cobalt (NMC) variants. LFP offers superior thermal stability and cycle life "
        "(exceeding 6,000 cycles at 80% depth of discharge), while NMC provides higher energy density, "
        "making it preferred for space-constrained applications.\n\n"
        "Recent advances in silicon anode technology have demonstrated energy densities approaching "
        "400 Wh/kg in laboratory settings. Amprius Technologies reported a 450 Wh/kg cell in early 2024, "
        "though commercial availability at scale remains 2-3 years away. The key challenge is silicon's "
        "volumetric expansion during lithiation, which degrades cycle life."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 280)
    page.insert_textbox(rect, liion, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    y += 300
    page.insert_text(pymupdf.Point(LEFT, y), "2.2 Cost Trajectory", fontsize=13, fontname="hebo", color=(0.2, 0.2, 0.4))
    y += 22
    cost_text = (
        "The levelized cost of Li-ion storage has declined by 89% since 2010, from $1,191/kWh to "
        "approximately $131/kWh in 2024. BNEF projects costs will reach $80/kWh by 2028 for utility-scale "
        "LFP systems. This cost reduction trajectory is driven by manufacturing scale, improved cathode "
        "synthesis methods, and supply chain maturation. The price of lithium carbonate, however, remains "
        "volatile, ranging from $15,000 to $78,000 per metric ton between 2021 and 2024."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 120)
    page.insert_textbox(rect, cost_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 4: Solid-State Batteries ---
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT, y), "3. Solid-State Battery Technology", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 28
    page.insert_text(pymupdf.Point(LEFT, y), "3.1 Electrolyte Materials", fontsize=13, fontname="hebo", color=(0.2, 0.2, 0.4))
    y += 22
    solid_state = (
        "Solid-state batteries replace the liquid electrolyte found in conventional Li-ion cells with "
        "a solid ionic conductor. This fundamental change addresses two critical limitations of liquid "
        "electrolyte systems: flammability risk and the inability to use lithium metal anodes.\n\n"
        "Three main classes of solid electrolytes are under active development:\n\n"
        "Sulfide-based electrolytes (e.g., Li6PS5Cl) offer the highest ionic conductivity among solid "
        "electrolytes, approaching 10-2 S/cm at room temperature. Samsung SDI and Toyota have both "
        "demonstrated prototype cells using sulfide electrolytes with energy densities exceeding 500 Wh/kg.\n\n"
        "Oxide-based electrolytes (e.g., Li7La3Zr2O12, LLZO) provide excellent chemical stability and a "
        "wide electrochemical window. However, their ionic conductivity (10-4 to 10-3 S/cm) requires "
        "operation at elevated temperatures or thin-film architectures.\n\n"
        "Polymer electrolytes, pioneered by Blue Solutions (Bollore Group), enable flexible cell designs "
        "but typically require operating temperatures above 60C for adequate ionic conductivity."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 340)
    page.insert_textbox(rect, solid_state, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    y += 360
    page.insert_text(pymupdf.Point(LEFT, y), "3.2 Manufacturing Challenges", fontsize=13, fontname="hebo", color=(0.2, 0.2, 0.4))
    y += 22
    mfg = (
        "The primary barrier to solid-state battery commercialization remains manufacturing scalability. "
        "Current production costs are estimated at 3-5x those of conventional Li-ion cells. QuantumScape "
        "reported a projected manufacturing cost of $35/kWh at scale, contingent on successful ramp-up "
        "of their ceramic separator technology."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 80)
    page.insert_textbox(rect, mfg, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 5: Sodium-Ion Batteries ---
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT, y), "4. Sodium-Ion Battery Systems", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 28
    naion = (
        "Sodium-ion batteries have attracted renewed interest as a potential complement to Li-ion "
        "technology, particularly for stationary storage applications where volumetric energy density "
        "is less critical. The key advantage of Na-ion technology lies in the abundance and low cost "
        "of sodium precursors. Sodium carbonate costs approximately $150/ton, compared to $15,000-78,000/ton "
        "for lithium carbonate.\n\n"
        "CATL launched the first commercial Na-ion battery in 2023 with an energy density of 160 Wh/kg "
        "and a cycle life of 3,000 cycles. HiNa Battery Technology, a Chinese startup, deployed a "
        "1 MWh Na-ion grid storage system in Shanxi Province in early 2024, demonstrating the technology's "
        "viability for utility-scale applications.\n\n"
        "The primary limitation of Na-ion technology is its lower energy density compared to Li-ion "
        "(typically 120-180 Wh/kg vs. 200-300 Wh/kg). However, recent research on Prussian blue analog "
        "cathodes and hard carbon anodes suggests that energy densities approaching 200 Wh/kg are "
        "achievable within the next 3-5 years.\n\n"
        "From an environmental perspective, Na-ion batteries avoid the use of cobalt, nickel, and lithium, "
        "all of which carry significant mining-related environmental and social concerns. The manufacturing "
        "process is compatible with existing Li-ion production lines, reducing capital investment requirements "
        "for technology transition."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 370)
    page.insert_textbox(rect, naion, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 6: Flow Batteries ---
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT, y), "5. Redox Flow Battery Technology", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 28
    flow = (
        "Redox flow batteries (RFBs) represent a fundamentally different approach to energy storage, "
        "where energy is stored in liquid electrolytes contained in external tanks. This architecture "
        "decouples energy capacity (determined by tank volume) from power output (determined by cell "
        "stack size), offering unique scalability advantages for long-duration storage applications.\n\n"
        "Vanadium redox flow batteries (VRFBs) are the most commercially mature RFB technology, with "
        "installations exceeding 1 GWh globally. The Dalian VRFB project in China, commissioned in 2022, "
        "is the world's largest at 400 MWh / 100 MW, providing 4 hours of storage capacity.\n\n"
        "The cost structure of VRFBs differs markedly from solid-state batteries. While the initial "
        "capital cost is higher ($350-500/kWh), the electrolyte does not degrade over time and can be "
        "recycled with near-100% efficiency. When evaluated over a 20-year lifecycle, the levelized cost "
        "of VRFBs becomes competitive with Li-ion for applications requiring 4+ hours of storage.\n\n"
        "Emerging flow battery chemistries include iron-chromium, zinc-bromine, and organic aqueous "
        "systems. Form Energy has developed an iron-air battery system with costs projected at $20/kWh "
        "for 100-hour storage duration, though this technology operates at lower round-trip efficiency "
        "(approximately 45%) compared to VRFBs (75-80%)."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 380)
    page.insert_textbox(rect, flow, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 7: Comparative Analysis ---
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT, y), "6. Comparative Analysis", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 28
    comp = (
        "Table 1 summarizes the key performance metrics across the four battery technologies reviewed "
        "in this study. The data represents commercially available or near-commercial systems as of Q1 2025.\n\n"
        "Technology        Energy Density   Cycle Life    Cost ($/kWh)   Safety\n"
        "Li-ion (LFP)      160-200 Wh/kg    4,000-6,000   $120-150       Moderate\n"
        "Li-ion (NMC)      230-300 Wh/kg    1,500-3,000   $130-170       Low-Moderate\n"
        "Solid-State       350-500 Wh/kg    5,000-10,000  $300-500*      High\n"
        "Na-ion            120-180 Wh/kg    2,000-4,000   $70-100        High\n"
        "VRFB              15-25 Wh/L       15,000+       $350-500       High\n\n"
        "* Projected at-scale cost\n\n"
        "The analysis reveals that no single technology optimally serves all use cases. Li-ion remains "
        "the best choice for applications requiring high energy density and established supply chains. "
        "Solid-state batteries show the highest potential for next-generation performance but face "
        "manufacturing hurdles. Na-ion offers the lowest projected cost and best environmental profile "
        "for stationary storage. VRFBs excel in long-duration, high-cycle applications."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 400)
    page.insert_textbox(rect, comp, fontsize=10, fontname="cour" if "Table" not in comp[:10] else "helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    # --- Page 8: Conclusions & References ---
    page = doc.new_page(width=W, height=H)
    y = 72
    page.insert_text(pymupdf.Point(LEFT, y), "7. Conclusions and Future Outlook", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 28
    conclusions = (
        "The energy storage landscape is undergoing a period of unprecedented innovation and investment. "
        "Our review of 247 studies highlights several key findings:\n\n"
        "First, lithium-ion technology will continue to dominate the market through 2030, driven by "
        "manufacturing scale and continuous incremental improvements. The transition to LFP chemistry "
        "for grid storage reduces both cost and supply chain risk.\n\n"
        "Second, solid-state batteries represent the most disruptive technology on the horizon. If "
        "manufacturing challenges are resolved, they could achieve cost parity with Li-ion by 2032 "
        "while offering 2x the energy density and significantly improved safety.\n\n"
        "Third, sodium-ion batteries will play an increasingly important role in grid-scale storage "
        "in regions with limited lithium resources. China's rapid deployment of Na-ion technology "
        "provides a real-world validation pathway.\n\n"
        "Fourth, flow batteries are uniquely positioned for long-duration storage (8+ hours) and "
        "will become critical as renewable penetration exceeds 50% of grid capacity.\n\n"
        "The authors recommend a portfolio approach to energy storage deployment, matching technology "
        "characteristics to specific application requirements rather than seeking a single universal solution."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 320)
    page.insert_textbox(rect, conclusions, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    y += 340
    page.insert_text(pymupdf.Point(LEFT, y), "References", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    y += 24
    refs = (
        "[1] Bloomberg New Energy Finance. Battery Price Survey 2024. BNEF, December 2024.\n"
        "[2] CATL. First Generation Sodium-Ion Battery Technical Specifications. July 2023.\n"
        "[3] Janek, J. & Zeier, W. A Solid Future for Battery Development. Nature Energy, 1, 16141 (2016).\n"
        "[4] International Energy Agency. World Energy Outlook 2024. IEA Publications, Paris.\n"
        "[5] QuantumScape Corp. Annual Technical Progress Report. SEC Filing 10-K, February 2025.\n"
        "[6] Vasquez, E. et al. Comparative Lifecycle Analysis of Grid-Scale Batteries. J. Power Sources, 512, 230484 (2024).\n"
        "[7] Zhang, H. et al. Advances in Vanadium Redox Flow Batteries. Chemical Reviews, 124(3), 1479-1528 (2024)."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 150)
    page.insert_textbox(rect, refs, fontsize=9, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    # Set metadata
    doc.set_metadata({
        "title": "Advances in Renewable Energy Storage: A Comprehensive Review of Battery Technologies",
        "author": "Elena Vasquez, James Hartfield, Mei-Lin Chang",
        "subject": "Battery Technology Review",
        "keywords": "renewable energy, battery storage, lithium-ion, solid-state, sodium-ion, flow battery",
        "creator": "LibreOffice Writer",
        "producer": "LibreOffice",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 8')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
