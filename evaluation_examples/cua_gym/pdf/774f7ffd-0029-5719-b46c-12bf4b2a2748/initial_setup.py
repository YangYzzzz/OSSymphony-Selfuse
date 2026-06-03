"""
Initial Setup: Create a 30-page thesis PDF with 6 unnumbered section headings
Task ID: pdf_res_092
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_092'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/unnumbered_thesis.pdf'


def launch_gui(command: str, delay_sec: float = 1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def build_thesis(headings, output_path):
    """Build a 30-page thesis PDF with the given heading list."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    W, H = 595, 842
    ML, MR, MT, MB = 72, 523, 72, 770

    # Section body paragraphs (3 per section, shorter to fit ~4 pages each)
    section_content = {
        "Introduction": [
            "The rapid advancement of renewable energy technologies has fundamentally transformed the global energy landscape over the past two decades. This thesis examines the socioeconomic impacts of large-scale solar photovoltaic deployment in emerging economies, with particular focus on Sub-Saharan Africa and Southeast Asia. As climate change continues to pose existential threats to vulnerable communities, the transition to clean energy sources has become not merely an environmental imperative but a critical development priority.",
            "Previous research has established that access to reliable electricity is strongly correlated with improvements in health outcomes, educational attainment, and economic productivity. However, the specific mechanisms through which solar energy deployment affects these development indicators remain poorly understood, particularly in rural and peri-urban contexts where grid infrastructure is limited or nonexistent. The motivation for this research stems from the observation that while installed solar capacity in developing nations has grown at a compound annual rate of 42% between 2015 and 2024, the distribution of benefits from this growth has been highly uneven.",
            "This thesis contributes to the existing literature in several important ways. First, we develop a novel analytical framework that integrates spatial econometrics with qualitative community assessment methods. Second, we present original survey data from 2,847 households across 12 countries. Third, we employ machine learning techniques to identify non-linear relationships between solar deployment characteristics and development outcomes. The central research question guiding this investigation is: To what extent does the mode of solar energy deployment differentially affect household-level economic outcomes in emerging economies?",
        ],
        "Background": [
            "The theoretical foundations of this research draw upon three distinct bodies of literature: energy economics, development studies, and environmental justice. Energy poverty, defined as the inability to access modern energy services at an affordable cost, affects approximately 770 million people globally as of 2023. The International Energy Agency estimates that achieving universal energy access by 2030 would require annual investments of $35 billion, representing less than 2% of global energy sector investment.",
            "The concept of energy justice, first articulated by Sovacool and Dworkin in 2015, provides a normative framework for evaluating the distributional impacts of energy system transitions. Three key principles guide this framework: distributional justice (equitable sharing of benefits and burdens), recognition justice (acknowledging diverse stakeholder perspectives), and procedural justice (inclusive decision-making processes). Solar photovoltaic technology has experienced remarkable cost reductions, with levelized costs falling 89% between 2010 and 2023.",
            "Previous empirical studies have produced mixed results regarding the local economic impacts of renewable energy installations. Zhang et al. (2021) found positive employment effects in Chinese provinces with high solar deployment, while Hartmann and Ankel-Peters (2022) identified minimal income effects in German municipalities hosting wind farms. These contradictory findings underscore the need for context-specific analysis that accounts for local institutional, economic, and social conditions.",
        ],
        "Methodology": [
            "This research employs a mixed-methods approach combining quantitative econometric analysis with qualitative case study research. The quantitative component utilizes a quasi-experimental difference-in-differences framework with propensity score matching. Treatment groups consist of communities within 25 kilometers of solar installations commissioned between 2018 and 2022. Control groups are matched communities with similar baseline characteristics but no proximate solar development during the study period.",
            "Primary data collection involved structured household surveys administered in 12 countries: Kenya, Tanzania, Ethiopia, Nigeria, Ghana, Senegal, India, Bangladesh, Vietnam, Indonesia, Philippines, and Cambodia. A total of 2,847 households were surveyed between March 2023 and February 2024. The survey instrument was developed through iterative pilot testing and captures household income, employment status, energy expenditure, appliance ownership, school enrollment, health facility visits, and subjective well-being.",
            "The econometric specification takes the form Y_it = alpha + beta * Treatment_i * Post_t + gamma * X_it + delta_i + theta_t + epsilon_it. For the qualitative component, we conducted semi-structured interviews with 186 community leaders, energy sector professionals, and government officials across six focal countries. Interview protocols explored perceptions of energy access, community engagement in deployment decisions, and observed changes in local economic activity.",
        ],
        "Results": [
            "The quantitative analysis reveals statistically significant but heterogeneous effects of solar deployment on household economic outcomes. The average treatment effect shows a 12.3% increase in monthly income (95% CI: 8.7-15.9%, p < 0.001), a 23.7% reduction in monthly energy expenditure (95% CI: 19.2-28.2%, p < 0.001), and a 7.8 percentage point increase in children's secondary school enrollment (95% CI: 4.1-11.5%, p < 0.001).",
            "Communities proximate to distributed solar installations experienced income gains approximately 2.4 times larger than those near utility-scale installations (18.1% vs. 7.5%, interaction term p < 0.01). The machine learning analysis identifies an inverted-U relationship between installation capacity and local economic benefit, with benefits peaking for installations between 5 and 50 megawatts. Geographic heterogeneity is pronounced, with Sub-Saharan African communities showing larger absolute gains.",
            "The qualitative findings complement the quantitative results. Community leaders consistently reported improvements in local business activity, particularly evening-hour commerce enabled by reliable lighting. However, concerns about land use competition, visual impact, and inequitable benefit-sharing were frequently raised in relation to utility-scale projects. Projects with community ownership or revenue-sharing models showed stronger positive outcomes.",
        ],
        "Discussion": [
            "The findings carry significant implications for energy policy design in emerging economies. The substantial differential in economic benefits between distributed and utility-scale solar deployment challenges the prevailing policy emphasis on large-scale installations driven by economies of scale. Our results suggest that while utility-scale solar effectively contributes to national decarbonization and grid capacity, its local development dividends are more limited than distributed systems.",
            "The inverted-U relationship between installation size and local benefit has important practical implications, suggesting an optimal scale range of 5-50 megawatts for community benefit. Several limitations warrant acknowledgment: the two-year observation period may be insufficient for long-term effects, propensity score matching cannot fully eliminate selection bias, and self-reported survey data may be subject to recall bias.",
            "Future research should examine the long-term sustainability of identified benefits through longitudinal panel studies over five to ten years. The interaction between solar deployment and digital connectivity trends merits investigation. The qualitative evidence highlights the critical importance of community engagement and benefit-sharing mechanisms in determining local acceptance and economic outcomes across all deployment modalities.",
        ],
        "Conclusion": [
            "This thesis has examined the socioeconomic impacts of solar photovoltaic deployment in emerging economies using a comprehensive mixed-methods approach. The evidence demonstrates that while solar energy generally improves household economic outcomes, the magnitude and distribution of benefits are strongly mediated by deployment modality, installation scale, and community engagement practices.",
            "The central finding that distributed solar systems generate approximately 2.4 times greater local income benefits compared to utility-scale installations represents a significant contribution to the literature. Three policy recommendations emerge: national strategies should incorporate distributional impact assessment, regulatory frameworks should mandate community benefit-sharing for utility-scale installations, and development finance institutions should expand support for distributed programs.",
            "The global energy transition represents both an unprecedented challenge and a transformative opportunity. By centering equity and community benefit in energy planning, policymakers can ensure that clean energy serves not only climate goals but also the aspirations of communities most affected by energy poverty. A more intentional, equity-focused approach to solar deployment can generate substantial co-benefits for both climate mitigation and sustainable development.",
        ],
    }

    doc = pymupdf.open()

    # --- Page 1: Title ---
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(W/2 - 200, 250), "Socioeconomic Impacts of Solar", fontsize=22, fontname="hebo", color=(0,0,0))
    p.insert_text(pymupdf.Point(W/2 - 220, 280), "Photovoltaic Deployment in Emerging", fontsize=22, fontname="hebo", color=(0,0,0))
    p.insert_text(pymupdf.Point(W/2 - 80, 310), "Economies", fontsize=22, fontname="hebo", color=(0,0,0))
    p.insert_text(pymupdf.Point(W/2 - 100, 400), "A Doctoral Thesis", fontsize=16, fontname="tiit", color=(0.3,0.3,0.3))
    p.insert_text(pymupdf.Point(W/2 - 80, 450), "Elena Vasquez", fontsize=14, fontname="helv", color=(0,0,0))
    p.insert_text(pymupdf.Point(W/2 - 140, 480), "Department of Energy Economics", fontsize=12, fontname="helv", color=(0.3,0.3,0.3))
    p.insert_text(pymupdf.Point(W/2 - 130, 500), "University of Cambridge, 2025", fontsize=12, fontname="helv", color=(0.3,0.3,0.3))

    # --- Page 2: Abstract ---
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(ML, MT + 20), "Abstract", fontsize=18, fontname="hebo", color=(0,0,0))
    abstract = (
        "This thesis investigates the socioeconomic impacts of solar photovoltaic deployment "
        "in emerging economies, focusing on the differential effects of distributed versus utility-scale "
        "installations. Using a mixed-methods approach combining quasi-experimental econometric analysis "
        "of 2,847 household surveys across 12 countries with qualitative case study research, we find "
        "that solar deployment generates significant positive effects on household income (+12.3%), "
        "energy expenditure (-23.7%), and children's school enrollment (+7.8 percentage points). "
        "Critically, distributed solar systems produce local income benefits approximately 2.4 times "
        "greater than utility-scale installations. Machine learning analysis reveals an inverted-U "
        "relationship between installation scale and local economic benefit, with optimal impacts "
        "in the 5-50 megawatt range."
    )
    p.insert_textbox(pymupdf.Rect(ML, MT+50, MR, MB), abstract, fontsize=11, fontname="helv", color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page_num = 2  # pages created so far

    # Helper to add a page with page number footer
    def add_page():
        nonlocal page_num
        page_num += 1
        pg = doc.new_page(width=W, height=H)
        pg.insert_text(pymupdf.Point(W/2 - 10, H - 30), str(page_num), fontsize=10, fontname="helv", color=(0.5,0.5,0.5))
        return pg

    # --- 6 Sections, each gets exactly 4 pages (6 * 4 = 24 pages, total = 24 + 2 = 26) ---
    for heading in headings:
        # Get base name (without number prefix) for content lookup
        base_name = heading
        for prefix in ["1. ", "2. ", "3. ", "4. ", "5. ", "6. "]:
            if heading.startswith(prefix):
                base_name = heading[len(prefix):]
                break
        paragraphs = section_content[base_name]

        # Page 1 of section: heading + first paragraph
        pg = add_page()
        y = MT + 20
        pg.insert_text(pymupdf.Point(ML, y), heading, fontsize=18, fontname="hebo", color=(0,0,0))
        y += 35
        shape = pg.new_shape()
        shape.draw_line(pymupdf.Point(ML, y), pymupdf.Point(MR, y))
        shape.finish(color=(0,0,0), width=0.5)
        shape.commit()
        y += 20

        for para in paragraphs:
            rect = pymupdf.Rect(ML, y, MR, MB)
            excess = pg.insert_textbox(rect, para, fontsize=11, fontname="helv", color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
            used = max(60, (len(para) / 70) * 14 + 10)
            y += used + 15
            if y >= MB - 40:
                break

        # Pages 2-4 of section: continuation text
        continuation_paragraphs = [
            f"The analysis within the {base_name.lower()} section extends to consider broader structural factors that influence "
            "the observed patterns. Institutional quality, measured through governance indicators from the World Bank's "
            "Worldwide Governance Indicators dataset, emerges as a significant moderating variable. Countries scoring above "
            "the median on regulatory quality show treatment effects approximately 40% larger than those below the median, "
            "suggesting that effective governance frameworks amplify the developmental benefits of solar energy deployment.",

            "Cross-country comparisons reveal interesting patterns in technology adoption trajectories. Early adopters "
            "such as Kenya and India have developed more mature local supply chains for solar components, reducing costs "
            "and increasing the share of value captured locally. Later entrants to the market, including Cambodia and "
            "Senegal, face higher per-unit costs but benefit from more advanced technology generations and lessons learned "
            "from pioneering markets. These adoption dynamics have important implications for deployment strategy.",

            "The spatial distribution of benefits warrants particular attention. Geographically weighted regression "
            "analysis reveals significant spatial autocorrelation in treatment effects, with clusters of high-impact "
            "communities typically located along transportation corridors and near urban centers. Remote communities, "
            "despite potentially greater need for energy access, show more modest economic gains from proximate solar "
            "installations, likely reflecting weaker market integration and limited complementary infrastructure.",

            "Gender-disaggregated analysis reveals important differential impacts. Female-headed households in treatment "
            "communities show income gains approximately 1.6 times larger than male-headed households, driven primarily "
            "by women's greater engagement in home-based enterprises enabled by reliable electricity. Educational "
            "enrollment effects are particularly strong for girls, with a 9.2 percentage point increase compared to "
            "6.4 percentage points for boys, consistent with theories about gendered opportunity costs of schooling.",

            "The temporal dynamics of benefit realization follow distinct patterns across outcome dimensions. Energy "
            "expenditure reductions materialize almost immediately upon connection to solar-generated electricity, "
            "while income effects emerge gradually over 6-12 months as households and local businesses adapt to "
            "improved energy availability. Educational enrollment changes are slowest to manifest, typically requiring "
            "one to two academic cycles before significant shifts become apparent in the data.",

            "Sensitivity analysis using alternative identification strategies confirms the robustness of core findings. "
            "Instrumental variable estimates using historical grid infrastructure as an instrument produce point estimates "
            "within the 95% confidence interval of the baseline difference-in-differences specification. Regression "
            "discontinuity design exploiting distance thresholds yields qualitatively similar results, with somewhat "
            "larger point estimates reflecting local average treatment effects at the boundary.",
        ]

        for page_in_section in range(3):  # 3 more pages per section
            pg = add_page()
            y = MT + 10
            start_idx = page_in_section * 2
            for para in continuation_paragraphs[start_idx:start_idx + 2]:
                rect = pymupdf.Rect(ML, y, MR, MB)
                pg.insert_textbox(rect, para, fontsize=11, fontname="helv", color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
                y += 340  # approx half page

    # Now page_num should be 26. Add 4 reference pages to reach 30.
    refs = [
        "Sovacool, B.K. and Dworkin, M.H. (2015). Energy justice: Conceptual insights and practical applications. Applied Energy, 142, 435-444.",
        "Zhang, L., Chen, W., and Liu, P. (2021). Employment effects of solar PV deployment in Chinese provinces: A spatial econometric analysis. Energy Policy, 155, 112348.",
        "Hartmann, M. and Ankel-Peters, J. (2022). Wind energy and local economic development: Evidence from German municipalities. Journal of Environmental Economics and Management, 112, 102623.",
        "International Energy Agency (2023). World Energy Outlook 2023. IEA Publications, Paris.",
        "IRENA (2024). Renewable Power Generation Costs in 2023. International Renewable Energy Agency, Abu Dhabi.",
        "Bazilian, M., Nussbaumer, P., Cabraal, A., et al. (2023). Measuring energy access: Supporting a global target. Earth's Future, 11(3), e2022EF003284.",
        "Alstone, P., Gershenson, D., and Kammen, D.M. (2015). Decentralized energy systems for clean electricity access. Nature Climate Change, 5(4), 305-314.",
        "Aklin, M., Bayer, P., Harish, S.P., and Urpelainen, J. (2018). Escaping the energy poverty trap. MIT Press.",
        "Jacobson, M.Z. et al. (2017). 100% clean and renewable wind, water, and sunlight all-sector energy roadmaps. Joule, 1(1), 108-121.",
        "Nemet, G.F. (2019). How Solar Energy Became Cheap: A Model for Low-Carbon Innovation. Routledge.",
        "Urpelainen, J. (2014). Grid and off-grid electrification: An integrated model. Energy for Sustainable Development, 22, 57-65.",
        "Khandker, S.R., Barnes, D.F., and Samad, H.A. (2012). The welfare impacts of rural electrification in Bangladesh. Energy Journal, 33(1).",
        "Burlig, F. and Preonas, L. (2016). Out of the darkness and into the light? Development effects of rural electrification. Energy Institute at Haas Working Paper 268.",
        "Dinkelman, T. (2011). The effects of rural electrification on employment: New evidence from South Africa. American Economic Review, 101(7), 3078-3108.",
        "Greenstone, M. (2014). Energy, growth, and regulation in developing countries. NBER Working Paper.",
        "Lipscomb, M., Mobarak, A.M., and Barham, T. (2013). Development effects of electrification: Evidence from the topographic placement of hydropower plants in Brazil. American Economic Journal: Applied Economics, 5(2), 200-231.",
        "Lee, K., Miguel, E., and Wolfram, C. (2020). Experimental evidence on the economics of rural electrification. Journal of Political Economy, 128(4), 1523-1565.",
        "Rud, J.P. (2012). Electricity provision and industrial development: Evidence from India. Journal of Development Economics, 97(2), 352-367.",
        "van de Walle, D., Ravallion, M., Mendiratta, V., and Koolwal, G. (2017). Long-term gains from electrification in rural India. World Bank Economic Review, 31(2), 385-411.",
        "Bridge, G., Bouzarovski, S., Bradshaw, M., and Eyre, N. (2013). Geographies of energy transition: Space, place and the low-carbon economy. Energy Policy, 53, 331-340.",
    ]

    while page_num < 30:
        pg = add_page()
        y = MT + 20
        if page_num == 27:  # first references page
            pg.insert_text(pymupdf.Point(ML, y), "References", fontsize=16, fontname="hebo", color=(0,0,0))
            y += 30
        ref_start = (page_num - 27) * 5
        for ref in refs[ref_start:ref_start + 5]:
            rect = pymupdf.Rect(ML, y, MR, y + 60)
            pg.insert_textbox(rect, ref, fontsize=9, fontname="helv", color=(0,0,0), align=pymupdf.TEXT_ALIGN_LEFT)
            y += 65

    doc.save(output_path)
    doc.close()
    print(f'File created: {output_path} ({page_num} pages)')


def create_initial():
    headings = ["Introduction", "Background", "Methodology", "Results", "Discussion", "Conclusion"]
    build_thesis(headings, OUTPUT)
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
