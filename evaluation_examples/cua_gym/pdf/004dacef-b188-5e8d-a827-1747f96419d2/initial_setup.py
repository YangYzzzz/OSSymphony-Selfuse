"""
Initial Setup: Create two PDF files with bookmarks for merging task
Task ID: pdf_mbc_055
Domain: pdf

Creates:
  - ~/Documents/part1.pdf: 25 pages, bookmarks 'Intro' (page 1), 'Body' (page 5)
  - ~/Documents/part2.pdf: 20 pages, bookmarks 'Methods' (page 1), 'Results' (page 10)
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCS_DIR = f'{WORKDIR}/Documents'
PART1 = f'{DOCS_DIR}/part1.pdf'
PART2 = f'{DOCS_DIR}/part2.pdf'


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


def create_part1():
    """Create part1.pdf: 25 pages about a research study on urban transportation."""
    doc = pymupdf.open()

    # --- Page 1: Introduction title page ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(
        pymupdf.Point(72, 120),
        "Urban Transportation Systems:",
        fontsize=24, fontname="hebo", color=(0.1, 0.1, 0.4),
    )
    page.insert_text(
        pymupdf.Point(72, 155),
        "A Comprehensive Analysis",
        fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4),
    )
    page.insert_text(
        pymupdf.Point(72, 220),
        "Dr. Elena Vasquez, Dr. Rajesh Patel",
        fontsize=14, fontname="heit", color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 250),
        "Institute of Urban Planning and Development",
        fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 275),
        "Published: March 2025",
        fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3),
    )
    intro_text = (
        "This document presents a thorough investigation into the current state of urban "
        "transportation systems across major metropolitan areas in North America. Over the "
        "past two decades, cities have faced increasing challenges related to traffic congestion, "
        "public transit efficiency, environmental sustainability, and equitable access to "
        "transportation infrastructure. Our study draws on data from 42 metropolitan regions, "
        "encompassing over 85 million residents, to provide actionable insights for urban "
        "planners, policymakers, and transportation engineers."
    )
    page.insert_textbox(
        pymupdf.Rect(72, 320, 523, 700),
        intro_text,
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Pages 2-4: More introduction content ---
    intro_sections = [
        ("1.1 Background and Motivation",
         "The rapid urbanization observed globally has placed unprecedented strain on existing "
         "transportation networks. Between 2000 and 2024, the average commute time in major "
         "US cities increased by 18%, while public transit ridership experienced significant "
         "fluctuations. Cities like Los Angeles, Houston, and Atlanta saw commute times exceed "
         "35 minutes on average, while denser urban cores such as New York and Chicago maintained "
         "relatively stable transit usage patterns. The economic cost of congestion alone was "
         "estimated at $87 billion annually by 2023, affecting both individual productivity and "
         "broader economic competitiveness. Furthermore, the environmental implications of "
         "transportation-related emissions continue to represent a major challenge for cities "
         "striving to meet their climate commitments under various international accords."),
        ("1.2 Research Objectives",
         "This study aims to: (a) evaluate the effectiveness of recent transit investments across "
         "diverse metropolitan contexts; (b) identify correlations between land use patterns and "
         "transportation outcomes; (c) assess the impact of emerging technologies including "
         "ride-sharing platforms, electric vehicles, and autonomous transit systems; and "
         "(d) develop a predictive framework for estimating future transportation demand under "
         "various growth scenarios. We employ a mixed-methods approach combining quantitative "
         "analysis of ridership and traffic data with qualitative assessments from stakeholder "
         "interviews conducted in 15 cities between January 2023 and June 2024."),
        ("1.3 Scope and Limitations",
         "Our analysis covers the period from 2015 to 2024, focusing on cities with populations "
         "exceeding 500,000 within their metropolitan statistical areas. We acknowledge several "
         "limitations: data availability varies significantly across jurisdictions, some cities "
         "underwent major infrastructure changes during the study period that may confound "
         "results, and the COVID-19 pandemic introduced unprecedented disruptions to travel "
         "patterns that are still being understood. Despite these challenges, our dataset "
         "represents one of the most comprehensive cross-city transportation analyses "
         "conducted to date, covering 42 metropolitan regions and incorporating over 12 million "
         "individual trip records, 850 transit route evaluations, and 2,400 stakeholder surveys."),
    ]
    for title, text in intro_sections:
        page = doc.new_page(width=595, height=842)
        page.insert_text(pymupdf.Point(72, 72), title, fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
        page.insert_textbox(
            pymupdf.Rect(72, 100, 523, 780),
            text, fontsize=11, fontname="helv", color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

    # --- Page 5 onward: Body section ---
    body_sections = [
        ("2.0 Literature Review",
         "Previous research in urban transportation has established several key frameworks for "
         "understanding mobility patterns. Cervero and Kockelman (1997) introduced the '3D' model "
         "of density, diversity, and design, which has been extended by subsequent scholars to "
         "include destination accessibility and distance to transit. Ewing and Cervero (2010) "
         "conducted a meta-analysis of over 50 empirical studies, finding that vehicle miles "
         "traveled (VMT) is most strongly associated with destination accessibility and that "
         "doubling residential density reduces VMT by approximately 5-12%. More recently, "
         "Shaheen and Cohen (2019) examined the impacts of shared mobility services on urban "
         "transportation systems, finding both complementary and competitive effects with "
         "traditional public transit depending on local context and implementation strategy."),
        ("2.1 Transit Investment Patterns",
         "Federal and state investments in public transportation have totaled over $420 billion "
         "between 2010 and 2024. Major projects include the Second Avenue Subway in New York "
         "($4.45 billion for Phase 1), the Purple Line in Los Angeles ($9.5 billion), and the "
         "Green Line extension in Boston ($2.3 billion). Our analysis reveals that cities with "
         "sustained capital investment programs saw 15-23% higher ridership growth compared to "
         "those with episodic funding patterns. Seattle's Sound Transit expansion, funded through "
         "the ST3 ballot measure, demonstrated particularly strong returns with a 34% increase "
         "in light rail ridership within three years of opening new stations."),
        ("2.2 Technology Integration",
         "The integration of technology into urban transportation has accelerated dramatically. "
         "Real-time transit information systems are now standard in 89% of major US transit agencies, "
         "up from just 34% in 2015. Mobile ticketing adoption reached 62% in 2024, reducing "
         "boarding times by an average of 8 seconds per passenger. Autonomous vehicle testing "
         "programs are active in 28 US cities, with Waymo and Cruise operating commercial "
         "services in Phoenix, San Francisco, and Austin. However, regulatory frameworks remain "
         "fragmented, with significant variation in how states and municipalities approach "
         "permitting, insurance requirements, and data sharing obligations."),
        ("2.3 Environmental Impact Assessment",
         "Transportation accounts for approximately 29% of total US greenhouse gas emissions, "
         "making it the largest single sectoral contributor. Our analysis of 42 metropolitan areas "
         "found that cities with comprehensive public transit networks produced 35-45% fewer "
         "per-capita transportation emissions than auto-dependent counterparts. The electrification "
         "of bus fleets has progressed significantly, with battery-electric buses comprising 12% "
         "of new bus orders in 2024, up from less than 1% in 2018. Cities leading in fleet "
         "electrification include Shenzhen (100%), Santiago (30%), and Los Angeles (25% of "
         "Metro fleet). The lifecycle emissions analysis shows that even when accounting for "
         "electricity generation mix, electric buses produce 45-65% fewer emissions than diesel."),
        ("2.4 Equity Considerations",
         "Transportation equity has emerged as a central concern in urban planning discourse. "
         "Our analysis reveals persistent disparities in transit access along socioeconomic lines. "
         "In the 42 metropolitan areas studied, low-income neighborhoods had an average of 40% "
         "fewer transit stops per square mile compared to high-income areas. Commute times for "
         "workers earning below the median income averaged 38 minutes, versus 26 minutes for "
         "those in the top income quartile. Several cities have implemented equity-focused "
         "initiatives: Kansas City eliminated fares on its bus system in 2020, resulting in a "
         "37% ridership increase; Los Angeles launched the LIFE program providing discounted "
         "fares to low-income riders; and Seattle's ORCA Opportunity program offers free transit "
         "to qualifying residents."),
        ("2.5 Ridership Trends 2015-2024",
         "National transit ridership experienced significant volatility during our study period. "
         "Pre-pandemic levels of approximately 9.9 billion annual unlinked trips (2019) dropped "
         "to 4.6 billion in 2020, a decline of 53%. Recovery has been uneven: bus ridership "
         "returned to 78% of pre-pandemic levels by 2024, while heavy rail recovered to 65% and "
         "commuter rail to only 58%. Cities with robust service frequency maintenance during the "
         "pandemic, such as Houston and Columbus, saw faster recovery trajectories. Conversely, "
         "cities that implemented severe service cuts, like Washington DC's Metro, experienced "
         "slower ridership return and lasting rider attrition."),
        ("2.6 Infrastructure Condition Assessment",
         "The state of good repair backlog across US transit agencies reached an estimated "
         "$105 billion in 2024. Our assessment of 42 metropolitan transit systems found that "
         "32% of rail vehicles exceeded their useful life benchmarks, while 28% of bus fleets "
         "were beyond recommended replacement age. Bridge and tunnel infrastructure showed "
         "particular concern, with the average age of subway tunnels in New York exceeding "
         "100 years. Cities that implemented asset management programs saw 20% lower maintenance "
         "costs and 15% higher reliability metrics compared to those without systematic approaches."),
        ("2.7 Land Use Integration",
         "The relationship between land use and transportation outcomes remains one of the "
         "strongest predictors of system performance. Transit-oriented development (TOD) projects "
         "within a half-mile of rail stations showed 40-60% lower car ownership rates compared "
         "to suburban developments. Our regression analysis identified population density, "
         "mixed-use zoning, and pedestrian infrastructure quality as the three strongest "
         "predictors of transit mode share. Cities that adopted form-based codes in transit "
         "corridors, such as Denver, Portland, and Minneapolis, saw measurable increases in "
         "both ridership and nearby property values."),
        ("2.8 Funding Models and Financial Sustainability",
         "The financial sustainability of urban transit systems varies widely across our study "
         "cities. Farebox recovery ratios ranged from 12% (Kansas City, post-fare elimination) "
         "to 61% (San Francisco BART). Innovative funding mechanisms include value capture "
         "through tax increment financing (Portland), dedicated sales taxes (Los Angeles Metro), "
         "and congestion pricing (New York, implemented 2024). Our analysis suggests that "
         "agencies with diversified revenue streams demonstrated greater financial resilience "
         "during economic downturns, with multi-source funded agencies experiencing 30% less "
         "service reduction during the 2020 fiscal crisis."),
        ("2.9 Comparative International Benchmarks",
         "Comparing US metropolitan transportation with international peers reveals both gaps "
         "and opportunities. Tokyo's rail system moves 40 million passengers daily with 99.7% "
         "on-time performance. London's congestion charge reduced central area traffic by 30%. "
         "Bogota's TransMilenio BRT system carries 2.4 million daily riders at a fraction of "
         "rail construction costs. Singapore's comprehensive approach combining congestion "
         "pricing, vehicle quotas, and world-class transit infrastructure offers a model for "
         "integrated transportation demand management. Our analysis identifies specific "
         "transferable lessons for US cities at various stages of transit development."),
        ("2.10 Emerging Mobility Services",
         "The proliferation of transportation network companies (TNCs) such as Uber and Lyft "
         "has fundamentally altered urban mobility patterns. In our 42 study cities, TNC trips "
         "grew from 500 million in 2015 to 4.2 billion in 2024. The relationship with public "
         "transit is complex: TNCs complement transit for first/last mile connections but compete "
         "for short urban trips. Micromobility services, including dockless e-scooters and "
         "e-bikes, added another dimension, with 139 million trips recorded across major US "
         "cities in 2024. Cities that integrated these services into their transit planning, "
         "rather than treating them as separate phenomena, achieved better overall mobility "
         "outcomes across accessibility, equity, and environmental metrics."),
    ]

    # Pages 5-15: Body sections (page 5 starts Body)
    for title, text in body_sections[:11]:
        page = doc.new_page(width=595, height=842)
        page.insert_text(pymupdf.Point(72, 72), title, fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
        page.insert_textbox(
            pymupdf.Rect(72, 100, 523, 780),
            text, fontsize=11, fontname="helv", color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

    # Pages 16-25: Data tables and appendix content
    data_pages = [
        ("Appendix A: Metropolitan Area Statistics",
         "Table A.1: Population and Transit Data by Metropolitan Area\n\n"
         "New York-Newark: Pop. 20.1M, Transit Trips 2.4B, Mode Share 31%\n"
         "Los Angeles-Long Beach: Pop. 13.2M, Transit Trips 392M, Mode Share 5%\n"
         "Chicago-Naperville: Pop. 9.5M, Transit Trips 507M, Mode Share 12%\n"
         "Dallas-Fort Worth: Pop. 7.6M, Transit Trips 62M, Mode Share 2%\n"
         "Houston-The Woodlands: Pop. 7.1M, Transit Trips 74M, Mode Share 3%\n"
         "Washington DC-Arlington: Pop. 6.3M, Transit Trips 287M, Mode Share 14%\n"
         "Philadelphia-Camden: Pop. 6.2M, Transit Trips 305M, Mode Share 10%\n"
         "Miami-Fort Lauderdale: Pop. 6.1M, Transit Trips 98M, Mode Share 4%\n"
         "Atlanta-Sandy Springs: Pop. 6.0M, Transit Trips 125M, Mode Share 4%\n"
         "Boston-Cambridge: Pop. 4.9M, Transit Trips 383M, Mode Share 13%"),
        ("Appendix A (continued)",
         "San Francisco-Oakland: Pop. 4.7M, Transit Trips 432M, Mode Share 17%\n"
         "Phoenix-Mesa: Pop. 4.9M, Transit Trips 38M, Mode Share 2%\n"
         "Riverside-San Bernardino: Pop. 4.6M, Transit Trips 24M, Mode Share 1%\n"
         "Detroit-Warren: Pop. 4.3M, Transit Trips 31M, Mode Share 2%\n"
         "Seattle-Tacoma: Pop. 4.0M, Transit Trips 184M, Mode Share 10%\n"
         "Minneapolis-St. Paul: Pop. 3.6M, Transit Trips 81M, Mode Share 5%\n"
         "San Diego-Chula Vista: Pop. 3.3M, Transit Trips 88M, Mode Share 4%\n"
         "Tampa-St. Petersburg: Pop. 3.2M, Transit Trips 22M, Mode Share 1%\n"
         "Denver-Aurora: Pop. 2.9M, Transit Trips 103M, Mode Share 6%\n"
         "St. Louis-East St. Louis: Pop. 2.8M, Transit Trips 41M, Mode Share 3%"),
        ("Appendix B: Investment Summary 2015-2024",
         "Table B.1: Major Transit Capital Projects Completed or Underway\n\n"
         "NYC Second Avenue Subway Phase 1: $4.45B, Opened 2017, Heavy Rail\n"
         "LA Purple Line Extension Sec 1-3: $9.50B, Est. 2027, Heavy Rail\n"
         "Seattle Link Extension: $5.40B, Ongoing, Light Rail\n"
         "Boston Green Line Extension: $2.30B, Opened 2022, Light Rail\n"
         "Denver FasTracks: $7.80B, Ongoing, Commuter Rail\n"
         "Bay Area BART Extension SJ: $6.90B, Ongoing, Heavy Rail\n"
         "DC Silver Line Phase 2: $2.70B, Opened 2022, Heavy Rail\n"
         "Houston METRONext: $3.50B, Ongoing, BRT + LRT\n"
         "Portland SW Corridor: $3.20B, Ongoing, Light Rail\n"
         "Minneapolis SW Light Rail: $2.75B, Opened 2023, Light Rail"),
        ("Appendix B (continued)",
         "Table B.2: Federal Funding Allocation by Category (Billions)\n\n"
         "Year    Capital   Operations   Research   Total\n"
         "2015    $12.4     $8.6         $1.2       $22.2\n"
         "2016    $12.8     $8.9         $1.3       $23.0\n"
         "2017    $13.1     $9.1         $1.3       $23.5\n"
         "2018    $13.5     $9.4         $1.4       $24.3\n"
         "2019    $14.0     $9.7         $1.5       $25.2\n"
         "2020    $13.2     $25.0        $1.6       $39.8\n"
         "2021    $14.8     $18.5        $1.7       $35.0\n"
         "2022    $16.2     $11.3        $1.9       $29.4\n"
         "2023    $17.5     $10.8        $2.1       $30.4\n"
         "2024    $18.9     $10.5        $2.3       $31.7"),
        ("Appendix C: Survey Methodology",
         "Stakeholder surveys were administered between January 2023 and June 2024 across "
         "15 metropolitan areas. A total of 2,400 responses were collected from transit agency "
         "officials (n=480), elected officials and staff (n=360), transportation consultants "
         "(n=320), advocacy organization representatives (n=280), and regular transit users "
         "(n=960). The survey instrument was developed through an iterative process involving "
         "expert review panels at three academic institutions. Response rates averaged 42% for "
         "agency officials and 28% for elected officials. User surveys were conducted at major "
         "transit stations during weekday peak hours using stratified random sampling to ensure "
         "demographic representativeness."),
        ("Appendix D: Statistical Methods",
         "Our quantitative analysis employed several complementary approaches. Panel regression "
         "models with city and year fixed effects were used to estimate the relationship between "
         "transit investment and ridership outcomes, controlling for population growth, economic "
         "conditions, and fuel prices. Difference-in-differences estimation was applied to evaluate "
         "the impact of specific policy interventions such as fare changes and service restructuring. "
         "Spatial econometric models accounted for spillover effects between adjacent jurisdictions. "
         "All standard errors were clustered at the metropolitan area level. Robustness checks "
         "included alternative model specifications, varying time windows, and placebo tests using "
         "pre-treatment trends."),
        ("Appendix E: Glossary of Terms",
         "APC: Automatic Passenger Counter\n"
         "BRT: Bus Rapid Transit\n"
         "CBSA: Core-Based Statistical Area\n"
         "CIG: Capital Investment Grants\n"
         "FTA: Federal Transit Administration\n"
         "GHG: Greenhouse Gas\n"
         "LRT: Light Rail Transit\n"
         "MSA: Metropolitan Statistical Area\n"
         "NTD: National Transit Database\n"
         "PMT: Passenger Miles Traveled\n"
         "TNC: Transportation Network Company\n"
         "TOD: Transit-Oriented Development\n"
         "UPT: Unlinked Passenger Trips\n"
         "VMT: Vehicle Miles Traveled\n"
         "VRH: Vehicle Revenue Hours\n"
         "VRM: Vehicle Revenue Miles"),
        ("Appendix F: Acknowledgments",
         "This research was supported by grants from the National Science Foundation (Award "
         "No. 2134567), the Federal Transit Administration (Grant No. TX-2023-0145), and the "
         "William and Flora Hewlett Foundation. The authors wish to thank Dr. Maria Santos at "
         "the University of California Berkeley, Professor James Wu at MIT, and Dr. Aisha Rahman "
         "at Georgia Tech for their valuable feedback on earlier drafts. Special thanks to the "
         "transit agency staff in all 42 metropolitan areas who generously shared data and time "
         "for interviews. Research assistants Sofia Martinez, Kenji Yamamoto, and Priya Sharma "
         "provided excellent support throughout the project."),
        ("Appendix G: References (Selected)",
         "Cervero, R., & Kockelman, K. (1997). Travel demand and the 3Ds. Transportation Research D.\n\n"
         "Ewing, R., & Cervero, R. (2010). Travel and the built environment: A meta-analysis. JAPA.\n\n"
         "Shaheen, S., & Cohen, A. (2019). Shared ride services in North America. Transport Reviews.\n\n"
         "Taylor, B., & Fink, C. (2013). Explaining transit ridership. Urban Studies, 50(14).\n\n"
         "Guerra, E., & Cervero, R. (2011). Cost of a ride. JAPA, 77(3), 267-290.\n\n"
         "Pucher, J., & Buehler, R. (2012). City Cycling. MIT Press.\n\n"
         "Litman, T. (2024). Evaluating public transit benefits and costs. Victoria Transport Policy.\n\n"
         "APTA (2024). Public Transportation Fact Book, 75th Edition. Washington, DC.\n\n"
         "NTD (2024). National Transit Database Annual Report. Federal Transit Administration."),
        ("Appendix H: Contact Information",
         "For questions about this research or to request additional data:\n\n"
         "Dr. Elena Vasquez\n"
         "Department of Urban Planning\n"
         "Institute of Urban Planning and Development\n"
         "1200 University Avenue, Suite 450\n"
         "Berkeley, CA 94720\n"
         "Email: e.vasquez@iupd.edu\n"
         "Phone: (510) 555-0142\n\n"
         "Dr. Rajesh Patel\n"
         "Department of Civil Engineering\n"
         "Massachusetts Institute of Technology\n"
         "77 Massachusetts Avenue, Room 1-290\n"
         "Cambridge, MA 02139\n"
         "Email: r.patel@mit.edu\n"
         "Phone: (617) 555-0198"),
    ]

    for title, text in data_pages:
        page = doc.new_page(width=595, height=842)
        page.insert_text(pymupdf.Point(72, 72), title, fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
        page.insert_textbox(
            pymupdf.Rect(72, 100, 523, 780),
            text, fontsize=10, fontname="helv", color=(0, 0, 0),
        )

    # Set bookmarks (TOC)
    toc = [
        [1, "Intro", 1],
        [1, "Body", 5],
    ]
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "Urban Transportation Systems: A Comprehensive Analysis",
        "author": "Dr. Elena Vasquez, Dr. Rajesh Patel",
        "subject": "Urban Transportation Research",
    })

    os.makedirs(DOCS_DIR, exist_ok=True)
    doc.save(PART1)
    doc.close()
    print(f"Created part1.pdf with {25} pages")


def create_part2():
    """Create part2.pdf: 20 pages about research methods and results."""
    doc = pymupdf.open()

    # --- Page 1: Methods title ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(
        pymupdf.Point(72, 120),
        "Research Methods and Analysis",
        fontsize=24, fontname="hebo", color=(0.2, 0.1, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 160),
        "Part 2: Methodology, Results, and Conclusions",
        fontsize=16, fontname="heit", color=(0.3, 0.3, 0.3),
    )
    methods_intro = (
        "This second volume details the methodological approaches employed in our urban "
        "transportation study, presents the primary findings from quantitative and qualitative "
        "analyses, and offers conclusions with policy recommendations. The methods described "
        "here were developed over a three-year period and have been peer-reviewed by leading "
        "transportation researchers at five major research universities."
    )
    page.insert_textbox(
        pymupdf.Rect(72, 220, 523, 700),
        methods_intro,
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Pages 2-9: Methods sections
    methods_sections = [
        ("3.1 Data Collection Framework",
         "Our data collection framework integrates multiple sources to construct a comprehensive "
         "picture of metropolitan transportation performance. Primary data sources include the "
         "National Transit Database (NTD), which provides standardized reporting from over 900 "
         "transit agencies nationwide. We supplemented NTD data with American Community Survey "
         "(ACS) commuting data, real-time GTFS feeds from 38 transit agencies, and proprietary "
         "traffic speed data from INRIX covering 425,000 road segments. GPS-based trip data "
         "from StreetLight Data provided origin-destination matrices for all 42 metropolitan "
         "areas. Data cleaning procedures removed 3.2% of records due to geocoding errors, "
         "duplicate entries, or implausible trip characteristics."),
        ("3.2 Sampling Strategy",
         "The sampling strategy was designed to ensure adequate representation across city sizes, "
         "geographic regions, and transit system types. We stratified our 42 metropolitan areas "
         "into four tiers based on population: Tier 1 (over 5 million), Tier 2 (2-5 million), "
         "Tier 3 (1-2 million), and Tier 4 (500,000-1 million). Within each tier, we ensured "
         "representation from each Census region. For the qualitative component, purposive "
         "sampling identified key informants at each transit agency, including general managers, "
         "planning directors, and operations supervisors. User surveys employed stratified random "
         "sampling at major transit hubs during morning peak (7-9 AM), midday (11 AM-1 PM), and "
         "evening peak (4-6 PM) periods across three consecutive weekdays."),
        ("3.3 Econometric Models",
         "Panel data regression with two-way fixed effects formed the backbone of our quantitative "
         "analysis. The baseline model specification is: Y_it = alpha + beta*X_it + gamma*Z_it + "
         "mu_i + lambda_t + epsilon_it, where Y_it represents the outcome variable (ridership, "
         "mode share, or congestion index) for city i in year t, X_it captures the policy variable "
         "of interest, Z_it is a vector of time-varying controls, mu_i captures city fixed effects, "
         "and lambda_t captures year fixed effects. We employ Driscoll-Kraay standard errors to "
         "account for both cross-sectional dependence and serial correlation. Instrumental variable "
         "estimation addresses potential endogeneity of transit investment using historical rail "
         "routes and federal earmark allocations as instruments."),
        ("3.4 Spatial Analysis Techniques",
         "Geographic information systems (GIS) analysis was conducted using ArcGIS Pro 3.2. We "
         "computed transit accessibility indices using a gravity-based measure that accounts for "
         "both the quantity and quality of transit service within specified travel time thresholds. "
         "Network analysis calculated shortest-path travel times between census block group "
         "centroids and the nearest transit stop, weighting by service frequency. Spatial "
         "autocorrelation was tested using Moran's I statistics, revealing significant clustering "
         "of transit performance metrics (I=0.42, p<0.001). Geographically weighted regression "
         "(GWR) was employed to examine spatial heterogeneity in the relationship between density "
         "and transit usage across metropolitan areas."),
        ("3.5 Qualitative Methods",
         "Semi-structured interviews lasting 45-90 minutes were conducted with 320 transit "
         "professionals and stakeholders. Interview protocols were developed iteratively through "
         "pilot testing with five transit agency staff members. All interviews were recorded with "
         "consent, transcribed verbatim, and coded using a combination of deductive codes derived "
         "from our theoretical framework and inductive codes emerging from the data. Inter-rater "
         "reliability was assessed using Cohen's kappa, achieving a score of 0.78 across all code "
         "categories. NVivo 14 was used for qualitative data management and analysis. Thematic "
         "analysis followed the six-phase approach outlined by Braun and Clarke (2006)."),
        ("3.6 Machine Learning Applications",
         "Random forest and gradient boosting models were trained on our panel dataset to predict "
         "ridership outcomes and identify the most important predictive features. Feature importance "
         "analysis revealed that service frequency, population density within a half-mile buffer, "
         "and fare level were the three most important predictors of station-level ridership. "
         "Neural network models (LSTM architecture) were applied to time-series ridership data "
         "to forecast short-term demand patterns with 89% accuracy at the hourly level. These "
         "models were validated using rolling window cross-validation with a 12-month training "
         "window and 3-month forecast horizon."),
        ("3.7 Cost-Benefit Analysis Framework",
         "Our cost-benefit analysis follows FTA guidelines with several enhancements. Monetized "
         "benefits include travel time savings (valued at $15.40/hour for commute trips, per "
         "DOT guidance), vehicle operating cost reductions ($0.58/mile avoided VMT), emission "
         "reductions (social cost of carbon at $51/ton CO2), crash reductions (comprehensive "
         "crash costs per NHTSA), and property value impacts (hedonic pricing estimates). Costs "
         "include capital expenditures, operating subsidies, and opportunity costs of public "
         "funds. Benefits and costs are discounted at 3% and 7% rates per OMB Circular A-94. "
         "Monte Carlo simulation with 10,000 iterations provides confidence intervals for "
         "benefit-cost ratios."),
        ("3.8 Validation and Robustness",
         "We conducted extensive validation of our models and findings. Out-of-sample prediction "
         "accuracy was tested by withholding five metropolitan areas from model estimation and "
         "comparing predicted to actual outcomes. Placebo tests using pre-treatment data confirmed "
         "parallel trends assumptions for difference-in-differences analyses. Sensitivity analyses "
         "varied key parameter assumptions including discount rates, value of time, and emission "
         "factors. Results were robust across alternative specifications, with core findings "
         "maintaining statistical significance at the 5% level in 94% of robustness checks."),
    ]

    for title, text in methods_sections:
        page = doc.new_page(width=595, height=842)
        page.insert_text(pymupdf.Point(72, 72), title, fontsize=16, fontname="hebo", color=(0.2, 0.1, 0.3))
        page.insert_textbox(
            pymupdf.Rect(72, 100, 523, 780),
            text, fontsize=11, fontname="helv", color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

    # --- Page 10 onward: Results ---
    results_sections = [
        ("4.0 Key Findings Overview",
         "Our analysis yields several significant findings that advance understanding of urban "
         "transportation dynamics. First, sustained capital investment in rail transit is "
         "associated with a 15-23% increase in ridership over a five-year horizon, controlling "
         "for population growth and economic conditions. Second, fare-free transit policies "
         "generate substantial ridership gains (30-40%) but raise questions about financial "
         "sustainability and service quality maintenance. Third, cities that integrated land use "
         "and transportation planning achieved measurably better outcomes across multiple metrics "
         "including ridership, equity, and emissions reduction."),
        ("4.1 Ridership Impact Analysis",
         "The panel regression results reveal that a 10% increase in service frequency (measured "
         "by vehicle revenue hours per capita) is associated with a 6.8% increase in unlinked "
         "passenger trips (p<0.01). This elasticity is higher for bus (0.72) than rail (0.61) "
         "service, suggesting that frequency improvements yield greater marginal returns for "
         "rubber-tire modes. New rail station openings generate a statistically significant "
         "ridership bump in the first year (average 12% within half-mile catchment area), with "
         "continued growth of 3-5% annually over the subsequent five years as land use patterns "
         "adjust. Fare increases of 10% are associated with ridership declines of 3.3% in the "
         "short run and 4.7% in the long run."),
        ("4.2 Equity Outcomes",
         "Transit equity metrics improved in 18 of 42 metropolitan areas between 2015 and 2024. "
         "Cities implementing targeted equity policies showed the most progress: fare reduction "
         "programs reached an average of 340,000 eligible riders per city, service expansions in "
         "underserved neighborhoods increased transit access scores by 22%, and multilingual "
         "passenger information systems were adopted by 76% of agencies serving diverse "
         "populations. However, gentrification near new transit stations remains a concern, "
         "with median rents within a quarter-mile of new rail stations increasing 18% faster "
         "than citywide averages. Anti-displacement policies were in place in only 12 of the "
         "42 study areas."),
        ("4.3 Environmental Results",
         "The environmental analysis demonstrates that comprehensive transit investment yields "
         "measurable emission reductions. Metropolitan areas that increased transit mode share "
         "by 2 percentage points saw per-capita transportation CO2 emissions decline by an "
         "average of 6.3%. Fleet electrification contributed an additional 2.1% emission "
         "reduction for early-adopter agencies. The total emission avoidance attributable to "
         "public transit in our 42 study areas was estimated at 37.2 million metric tons of "
         "CO2 annually, equivalent to removing 8.1 million passenger vehicles from the road."),
        ("4.4 Cost-Effectiveness Rankings",
         "Benefit-cost ratios varied significantly across project types and metropolitan contexts. "
         "BRT projects showed the highest median BCR (2.1), followed by light rail (1.7), bus "
         "network redesigns (1.6), and heavy rail extensions (1.4). However, heavy rail projects "
         "in dense urban cores (population density > 10,000/sq mi) achieved BCRs comparable to "
         "BRT (median 2.0). The most cost-effective individual project in our analysis was "
         "Houston's bus network redesign (BCR 3.4), which improved service coverage by 40% "
         "without increasing operating costs by redistributing resources from low-ridership "
         "to high-demand routes."),
        ("4.5 Technology Impact Assessment",
         "Real-time information systems showed a statistically significant positive effect on "
         "rider satisfaction (0.8 points on a 5-point scale, p<0.001) and perceived wait times "
         "(reduction of 23%). Mobile ticketing reduced average boarding times from 4.2 to 2.1 "
         "seconds for equipped vehicles. However, the digital divide poses equity concerns: "
         "smartphone ownership among transit-dependent riders was 71% compared to 92% for "
         "choice riders, potentially exacerbating information access disparities."),
        ("4.6 Policy Recommendations",
         "Based on our findings, we recommend: (1) Prioritize service frequency over coverage "
         "expansion in established networks; (2) Implement graduated fare structures that protect "
         "low-income riders while maintaining revenue; (3) Require anti-displacement policies as "
         "a condition of transit capital grants; (4) Accelerate fleet electrification with "
         "dedicated federal incentives; (5) Mandate integrated land use and transportation "
         "planning at the metropolitan level; (6) Establish performance-based funding formulas "
         "that reward efficiency and equity outcomes; (7) Invest in predictive maintenance "
         "systems to address the state of good repair backlog."),
        ("4.7 Future Research Directions",
         "Several areas warrant further investigation. The long-term impacts of remote work on "
         "commute patterns and transit demand remain uncertain. Autonomous vehicle deployment "
         "could fundamentally reshape urban mobility, but empirical evidence is limited to "
         "pilot programs. Climate adaptation requirements for transit infrastructure have not "
         "been comprehensively assessed. The interaction effects between pricing policies, "
         "service quality, and ridership require more nuanced modeling. Finally, comparative "
         "international studies with standardized metrics would strengthen the evidence base "
         "for policy transfer across different institutional and geographic contexts."),
        ("5.0 Conclusions",
         "Urban transportation in America stands at a critical juncture. The challenges of "
         "congestion, equity, and environmental sustainability demand coordinated policy "
         "responses grounded in rigorous evidence. Our analysis of 42 metropolitan areas over "
         "a decade demonstrates that strategic investments in public transit can yield substantial "
         "returns across multiple dimensions of urban well-being. However, realizing these "
         "benefits requires sustained political commitment, integrated planning approaches, and "
         "willingness to adopt innovative technologies and business models. The cities that "
         "thrive in the coming decades will be those that view transportation not as a standalone "
         "infrastructure challenge but as a foundational element of livable, equitable, and "
         "prosperous urban communities."),
        ("5.1 Final Remarks",
         "We hope this research contributes to more informed decision-making in urban "
         "transportation planning. The data, models, and policy frameworks presented here are "
         "available for use by practitioners, policymakers, and researchers. We encourage "
         "continued collaboration across sectors and disciplines to address the complex "
         "challenges facing our cities. Transportation is ultimately about connecting people "
         "to opportunities, and our collective goal should be to ensure that these connections "
         "are efficient, equitable, and sustainable for generations to come."),
    ]

    # Page 10-19: Results sections
    for title, text in results_sections[:10]:
        page = doc.new_page(width=595, height=842)
        page.insert_text(pymupdf.Point(72, 72), title, fontsize=16, fontname="hebo", color=(0.2, 0.1, 0.3))
        page.insert_textbox(
            pymupdf.Rect(72, 100, 523, 780),
            text, fontsize=11, fontname="helv", color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

    # Last page (page 20): closing
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 72), "End of Part 2", fontsize=16, fontname="hebo", color=(0.2, 0.1, 0.3))
    page.insert_textbox(
        pymupdf.Rect(72, 100, 523, 400),
        "This concludes Part 2 of the Urban Transportation Systems study. For the full "
        "introduction, literature review, and appendices, please refer to Part 1 of this "
        "publication series. Combined versions with merged bookmarks are available upon "
        "request from the research team.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Set bookmarks (TOC)
    toc = [
        [1, "Methods", 1],
        [1, "Results", 10],
    ]
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "Research Methods and Analysis: Part 2",
        "author": "Dr. Elena Vasquez, Dr. Rajesh Patel",
        "subject": "Research Methodology and Results",
    })

    doc.save(PART2)
    doc.close()
    print(f"Created part2.pdf with {20} pages")


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)
    create_part1()
    create_part2()

    # Verify page counts
    doc1 = pymupdf.open(PART1)
    doc2 = pymupdf.open(PART2)
    print(f"part1.pdf pages: {doc1.page_count}")
    print(f"part2.pdf pages: {doc2.page_count}")
    print(f"part1.pdf TOC: {doc1.get_toc()}")
    print(f"part2.pdf TOC: {doc2.get_toc()}")
    doc1.close()
    doc2.close()

    # Open part1.pdf in Evince for the agent
    launch_gui(f'evince "{PART1}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with part1.pdf')


create_initial()
