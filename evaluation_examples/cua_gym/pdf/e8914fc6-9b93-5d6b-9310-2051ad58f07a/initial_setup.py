"""
Initial Setup: Create a 14-page working paper PDF with no watermarks
Task ID: pdf_res_026
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_026'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/working_paper.pdf'


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
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page dimensions ---
    W, H = 612, 792  # US Letter

    # Content for a realistic 14-page working paper
    title = "The Impact of Remote Work on Organizational Productivity:\nA Multi-Industry Longitudinal Study"
    authors = "Dr. Elena Vasquez, Prof. James Whitfield, Dr. Aisha Okonkwo\nCenter for Workforce Innovation, Stanford University"

    abstract = (
        "This working paper presents findings from a three-year longitudinal study examining the effects "
        "of remote work arrangements on organizational productivity across seven industry sectors. Using "
        "a mixed-methods approach combining quantitative performance metrics from 2,847 organizations "
        "with qualitative interviews of 312 senior managers, we find that hybrid remote work models "
        "yield an average productivity increase of 13.2% compared to fully in-office arrangements. "
        "However, the magnitude of this effect varies significantly by industry, with technology and "
        "professional services firms experiencing gains of up to 22.7%, while manufacturing and "
        "healthcare organizations show more modest improvements of 4.1-6.8%. We identify three key "
        "mediating factors: digital infrastructure maturity, management trust orientation, and task "
        "interdependence levels. Our findings challenge the prevailing assumption that productivity "
        "necessarily declines with increased remote work and suggest that organizational context plays "
        "a critical role in determining outcomes. Policy implications for workforce planning and "
        "corporate real estate strategy are discussed."
    )

    sections = [
        {
            "title": "1. Introduction",
            "content": (
                "The global shift toward remote work, accelerated by the COVID-19 pandemic, has "
                "fundamentally altered the landscape of modern employment. As of 2025, approximately "
                "38% of knowledge workers in OECD countries maintain some form of remote work "
                "arrangement, compared to just 5.7% in 2019 (Bureau of Labor Statistics, 2025). "
                "This transformation has prompted urgent questions about the long-term implications "
                "for organizational productivity, employee well-being, and economic competitiveness.\n\n"
                "Despite growing academic interest, existing research on remote work productivity "
                "remains fragmented and inconclusive. Early studies conducted during the pandemic "
                "produced contradictory findings, with some reporting productivity gains of 10-20% "
                "(Bloom et al., 2022) while others documented significant declines, particularly "
                "in collaborative tasks (Yang et al., 2021). These discrepancies can be attributed "
                "to several methodological limitations: small sample sizes, single-industry focus, "
                "short observation periods, and inadequate controls for pandemic-specific confounds.\n\n"
                "This paper addresses these gaps by presenting results from a comprehensive three-year "
                "study spanning seven industry sectors. Our research design incorporates both objective "
                "performance metrics and subjective managerial assessments, enabling a nuanced "
                "understanding of how remote work affects different dimensions of organizational "
                "productivity. We contribute to the literature in three ways: (1) by providing "
                "cross-industry comparative evidence, (2) by identifying mediating factors that "
                "explain variation in outcomes, and (3) by developing a predictive framework for "
                "assessing remote work suitability at the organizational level."
            )
        },
        {
            "title": "2. Literature Review",
            "content": (
                "2.1 Theoretical Frameworks\n\n"
                "The theoretical foundations of remote work research draw on several established "
                "frameworks. Self-Determination Theory (Deci & Ryan, 1985) suggests that remote work "
                "may enhance intrinsic motivation by providing greater autonomy, while Social Exchange "
                "Theory (Blau, 1964) posits that organizational trust is essential for successful "
                "remote arrangements. The Job Demands-Resources model (Bakker & Demerouti, 2007) "
                "offers a framework for understanding how remote work simultaneously reduces certain "
                "job demands (e.g., commuting stress) while potentially increasing others (e.g., "
                "technology-mediated communication burden).\n\n"
                "2.2 Empirical Evidence\n\n"
                "Pre-pandemic studies generally supported the productivity benefits of remote work "
                "under controlled conditions. The seminal Ctrip experiment (Bloom et al., 2015) "
                "found a 13% performance increase among call center workers randomly assigned to "
                "work from home. However, subsequent research revealed important boundary conditions. "
                "Gajendran and Harrison's (2007) meta-analysis of 46 studies found that telecommuting "
                "had a small positive effect on performance (d = 0.11) but that this effect was "
                "moderated by the intensity of telecommuting and job complexity.\n\n"
                "2.3 Industry-Specific Considerations\n\n"
                "Recent work has emphasized the importance of industry context. Barrero et al. (2023) "
                "developed a framework for classifying jobs by remote work feasibility, finding that "
                "approximately 37% of US jobs can be performed entirely remotely. However, this "
                "classification does not address productivity implications, which depend on factors "
                "such as task interdependence, client interaction requirements, and regulatory "
                "constraints specific to each industry."
            )
        },
        {
            "title": "3. Methodology",
            "content": (
                "3.1 Research Design\n\n"
                "We employed a convergent parallel mixed-methods design, collecting quantitative and "
                "qualitative data concurrently over a 36-month period (January 2022 to December 2024). "
                "The quantitative component utilized panel data from 2,847 organizations, while the "
                "qualitative component consisted of semi-structured interviews with 312 senior managers "
                "across the seven target industries.\n\n"
                "3.2 Sample and Data Collection\n\n"
                "Organizations were recruited through partnerships with industry associations in seven "
                "sectors: Technology (n=487), Professional Services (n=412), Financial Services "
                "(n=398), Education (n=356), Healthcare (n=344), Manufacturing (n=421), and Retail "
                "(n=429). Inclusion criteria required organizations to have at least 50 employees "
                "and to have implemented some form of remote work policy during the study period.\n\n"
                "Productivity metrics were collected quarterly and included: revenue per employee, "
                "project completion rates, customer satisfaction scores (NPS), employee turnover "
                "rates, and innovation indices (patent filings, new product launches). All metrics "
                "were normalized within industry groups to enable cross-sector comparison.\n\n"
                "3.3 Analytical Approach\n\n"
                "Quantitative analysis employed fixed-effects panel regression models with robust "
                "standard errors clustered at the organization level. The primary specification was:\n\n"
                "    Y_it = alpha_i + beta * RemoteIntensity_it + gamma * X_it + delta_t + epsilon_it\n\n"
                "where Y_it represents the productivity metric for organization i at time t, "
                "RemoteIntensity_it measures the proportion of employees working remotely, X_it "
                "is a vector of time-varying controls, alpha_i captures organization fixed effects, "
                "and delta_t represents time fixed effects. Qualitative data were analyzed using "
                "thematic analysis following Braun and Clarke (2006)."
            )
        },
        {
            "title": "4. Results",
            "content": (
                "4.1 Overall Productivity Effects\n\n"
                "Table 1 presents the main regression results. Across the full sample, hybrid remote "
                "work arrangements (defined as 2-3 days remote per week) were associated with a "
                "statistically significant increase in revenue per employee of 13.2% (p < 0.001, "
                "95% CI: 10.4-16.0%). Fully remote arrangements showed a smaller but still positive "
                "effect of 7.8% (p < 0.01), while organizations that returned to fully in-office "
                "work experienced a 3.1% decline relative to their pandemic-era hybrid arrangements.\n\n"
                "Project completion rates improved by 8.7% under hybrid arrangements, with the most "
                "pronounced effects in technology (14.2%) and professional services (11.9%). Customer "
                "satisfaction scores showed no statistically significant change across work arrangements, "
                "suggesting that remote work does not compromise service quality.\n\n"
                "4.2 Industry-Specific Findings\n\n"
                "The magnitude of productivity effects varied substantially across industries. "
                "Technology firms exhibited the largest gains, with hybrid arrangements yielding "
                "a 22.7% increase in revenue per employee. Professional services followed at 18.3%, "
                "financial services at 14.1%, and education at 11.6%. Healthcare and manufacturing "
                "showed more modest improvements of 6.8% and 4.1% respectively, while retail "
                "demonstrated the smallest effect at 3.2%.\n\n"
                "4.3 Mediating Factors\n\n"
                "Three factors emerged as significant mediators of the remote work-productivity "
                "relationship. Digital infrastructure maturity explained 34% of the between-organization "
                "variance in productivity outcomes. Organizations scoring in the top quartile of our "
                "Digital Readiness Index (DRI) achieved productivity gains 2.4 times larger than those "
                "in the bottom quartile. Management trust orientation, measured via the Organizational "
                "Trust Scale (Mayer & Davis, 1999), explained an additional 21% of variance. Task "
                "interdependence levels, assessed using Thompson's (1967) framework, accounted for 18% "
                "of variance, with pooled and sequential interdependence showing greater compatibility "
                "with remote arrangements than reciprocal interdependence."
            )
        },
        {
            "title": "5. Discussion",
            "content": (
                "5.1 Interpretation of Findings\n\n"
                "Our results provide strong evidence that hybrid remote work arrangements can enhance "
                "organizational productivity, but that the magnitude of this effect is heavily "
                "contingent on industry context and organizational characteristics. The finding that "
                "hybrid models outperform both fully remote and fully in-office arrangements aligns "
                "with emerging theoretical perspectives on the importance of combining focused "
                "individual work with periodic in-person collaboration (Gratton, 2021).\n\n"
                "The industry-level variation we observe can be explained through the lens of task "
                "characteristics and knowledge work intensity. Industries with higher proportions of "
                "autonomous, knowledge-intensive tasks (technology, professional services) benefit "
                "most from the flexibility afforded by remote work. In contrast, industries with "
                "significant physical task components or regulatory constraints on remote operations "
                "(manufacturing, healthcare) show more limited gains.\n\n"
                "5.2 Implications for Theory\n\n"
                "Our findings extend Self-Determination Theory by demonstrating that the autonomy "
                "benefits of remote work are moderated by organizational and industry context. The "
                "identification of digital infrastructure maturity as the strongest mediator suggests "
                "that the relationship between remote work and productivity is not merely a function "
                "of individual preferences but depends critically on the technological ecosystem within "
                "which work is performed.\n\n"
                "5.3 Practical Implications\n\n"
                "For organizational leaders, our results suggest that a one-size-fits-all approach "
                "to remote work policy is suboptimal. We recommend that organizations assess their "
                "position on the three mediating dimensions identified in this study before designing "
                "remote work policies. The predictive framework presented in Appendix B provides a "
                "practical tool for this assessment. Additionally, our findings highlight the "
                "importance of investing in digital infrastructure as a prerequisite for successful "
                "remote work implementation."
            )
        },
        {
            "title": "6. Limitations and Future Research",
            "content": (
                "Several limitations should be acknowledged. First, our sample is limited to OECD "
                "countries and may not generalize to emerging economies where digital infrastructure "
                "and labor market conditions differ substantially. Second, while our panel design "
                "controls for time-invariant organization-level confounds, we cannot fully rule out "
                "reverse causality, as more productive organizations may be more likely to adopt "
                "flexible work arrangements. Third, our productivity metrics are primarily "
                "organizational-level measures and may not capture individual-level variation within "
                "organizations.\n\n"
                "Future research should address these limitations through randomized controlled trials "
                "at the organizational level, extend the geographic scope to non-OECD contexts, and "
                "develop more granular productivity measures that account for the quality and "
                "innovativeness of work output. The role of emerging technologies such as AI-assisted "
                "collaboration tools in mediating remote work productivity also warrants investigation."
            )
        },
        {
            "title": "7. Conclusion",
            "content": (
                "This study provides robust, cross-industry evidence that hybrid remote work "
                "arrangements can significantly enhance organizational productivity when implemented "
                "under favorable conditions. The key conditions we identify include mature digital "
                "infrastructure, trust-oriented management practices, and task structures compatible "
                "with distributed work. Rather than asking whether remote work improves or harms "
                "productivity, organizations should ask under what conditions remote work is most "
                "effective for their specific context. The framework and evidence presented here "
                "offer a foundation for making these assessments."
            )
        },
        {
            "title": "References",
            "content": (
                "Bakker, A. B., & Demerouti, E. (2007). The Job Demands-Resources model: State of "
                "the art. Journal of Managerial Psychology, 22(3), 309-328.\n\n"
                "Barrero, J. M., Bloom, N., & Davis, S. J. (2023). The evolution of work from home. "
                "Journal of Economic Perspectives, 37(4), 23-50.\n\n"
                "Blau, P. M. (1964). Exchange and Power in Social Life. Wiley.\n\n"
                "Bloom, N., Liang, J., Roberts, J., & Ying, Z. J. (2015). Does working from home "
                "work? Evidence from a Chinese experiment. Quarterly Journal of Economics, 130(1), "
                "165-218.\n\n"
                "Bloom, N., Han, R., & Liang, J. (2022). How hybrid working from home works out. "
                "Working Paper 30292, National Bureau of Economic Research.\n\n"
                "Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. Qualitative "
                "Research in Psychology, 3(2), 77-101.\n\n"
                "Bureau of Labor Statistics. (2025). American Time Use Survey: Telework Supplement. "
                "U.S. Department of Labor.\n\n"
                "Deci, E. L., & Ryan, R. M. (1985). Intrinsic Motivation and Self-Determination in "
                "Human Behavior. Plenum Press.\n\n"
                "Gajendran, R. S., & Harrison, D. A. (2007). The good, the bad, and the unknown about "
                "telecommuting: Meta-analysis of psychological mediators and individual consequences. "
                "Journal of Applied Psychology, 92(6), 1524-1541.\n\n"
                "Gratton, L. (2021). How to do hybrid right. Harvard Business Review, 99(3), 66-74.\n\n"
                "Mayer, R. C., & Davis, J. H. (1999). The effect of the performance appraisal system "
                "on trust for management. Journal of Applied Psychology, 84(1), 123-136.\n\n"
                "Thompson, J. D. (1967). Organizations in Action. McGraw-Hill.\n\n"
                "Yang, L., Holtz, D., Jaffe, S., et al. (2021). The effects of remote work on "
                "collaboration among information workers. Nature Human Behaviour, 6(1), 43-54."
            )
        },
    ]

    # --- Page 1: Title Page ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 200), "WORKING PAPER", fontsize=14, fontname="helv", color=(0.4, 0.4, 0.4))
    y = 250
    for line in title.split('\n'):
        page.insert_text(pymupdf.Point(72, y), line, fontsize=20, fontname="hebo", color=(0, 0, 0))
        y += 30
    y += 30
    for line in authors.split('\n'):
        page.insert_text(pymupdf.Point(72, y), line, fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
        y += 20
    y += 40
    page.insert_text(pymupdf.Point(72, y), "Working Paper No. WP-2025-0142", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    y += 20
    page.insert_text(pymupdf.Point(72, y), "March 2025", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    y += 20
    page.insert_text(pymupdf.Point(72, y), "Draft - Prepared for internal review", fontsize=10, fontname="heit", color=(0.5, 0.5, 0.5))

    # --- Page 2: Abstract ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Abstract", fontsize=16, fontname="hebo", color=(0, 0, 0))
    rect = pymupdf.Rect(72, 100, W - 72, H - 72)
    page.insert_textbox(rect, abstract, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Keywords
    page.insert_text(pymupdf.Point(72, 520), "Keywords:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(140, 520), "remote work, productivity, hybrid work, organizational performance, longitudinal study",
                     fontsize=10, fontname="heit", color=(0.2, 0.2, 0.2))

    page.insert_text(pymupdf.Point(72, 560), "JEL Classification:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(190, 560), "J24, M12, O33", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))

    # --- Pages 3-14: Sections ---
    current_page = None
    y_pos = 0
    margin_top = 72
    margin_bottom = 72
    margin_left = 72
    margin_right = 72
    line_height = 15
    max_y = H - margin_bottom

    for section in sections:
        # Start each major section on a new page
        page = doc.new_page(width=W, height=H)
        y_pos = margin_top

        # Section title
        page.insert_text(pymupdf.Point(margin_left, y_pos), section["title"],
                        fontsize=14, fontname="hebo", color=(0, 0, 0))
        y_pos += 30

        # Section content - use textbox for auto-wrapping
        content_rect = pymupdf.Rect(margin_left, y_pos, W - margin_right, max_y)
        excess = page.insert_textbox(content_rect, section["content"],
                                     fontsize=10.5, fontname="helv", color=(0, 0, 0),
                                     align=pymupdf.TEXT_ALIGN_JUSTIFY)

        # If there's overflow, add continuation pages
        # insert_textbox returns a string (excess text) or a negative float (no overflow)
        while isinstance(excess, str) and len(excess.strip()) > 0:
            page = doc.new_page(width=W, height=H)
            content_rect = pymupdf.Rect(margin_left, margin_top, W - margin_right, max_y)
            excess = page.insert_textbox(content_rect, excess,
                                         fontsize=10.5, fontname="helv", color=(0, 0, 0),
                                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Ensure we have exactly 14 pages - pad with appendix content if needed
    while doc.page_count < 14:
        page = doc.new_page(width=W, height=H)
        appendix_num = doc.page_count - 10  # rough numbering
        page.insert_text(pymupdf.Point(margin_left, margin_top),
                        f"Appendix {chr(64 + appendix_num)}: Supplementary Materials",
                        fontsize=14, fontname="hebo", color=(0, 0, 0))

        appendix_text = (
            "Table A1: Full Regression Results by Industry\n\n"
            "Industry          | Hybrid Effect | Full Remote | 95% CI         | N\n"
            "Technology        |    +22.7%     |   +15.1%    | [19.2, 26.2]   | 487\n"
            "Prof. Services    |    +18.3%     |   +11.4%    | [14.8, 21.8]   | 412\n"
            "Financial Svcs    |    +14.1%     |    +8.9%    | [10.6, 17.6]   | 398\n"
            "Education         |    +11.6%     |    +6.2%    | [8.1, 15.1]    | 356\n"
            "Healthcare        |     +6.8%     |    +3.7%    | [3.3, 10.3]    | 344\n"
            "Manufacturing     |     +4.1%     |    +1.8%    | [0.6, 7.6]     | 421\n"
            "Retail            |     +3.2%     |    +0.9%    | [-0.3, 6.7]    | 429\n\n"
            "Notes: All effects are relative to fully in-office baseline. Hybrid defined as 2-3 "
            "days remote per week. Standard errors clustered at organization level. Statistical "
            "significance: *** p<0.001, ** p<0.01, * p<0.05.\n\n"
            "Figure A1: Productivity Trends by Work Arrangement (2022-2024)\n\n"
            "The figure shows quarterly productivity indices normalized to Q1 2022 = 100 for each "
            "of the three work arrangement categories. Hybrid arrangements show consistent upward "
            "trajectory, fully remote shows moderate gains with seasonal variation, and fully "
            "in-office shows relative decline beginning in Q3 2022.\n\n"
            "Table A2: Digital Readiness Index Components\n\n"
            "Component                      | Weight | Mean Score (SD)\n"
            "Cloud infrastructure adoption  |  0.25  | 3.42 (1.18)\n"
            "Collaboration tool maturity    |  0.25  | 3.67 (0.94)\n"
            "Cybersecurity readiness        |  0.20  | 3.21 (1.31)\n"
            "Employee digital literacy      |  0.15  | 3.89 (0.87)\n"
            "IT support responsiveness      |  0.15  | 3.54 (1.06)\n\n"
            "Notes: Scores on 1-5 Likert scale. N = 2,847 organizations."
        )
        content_rect = pymupdf.Rect(margin_left, margin_top + 30, W - margin_right, max_y)
        page.insert_textbox(content_rect, appendix_text,
                           fontsize=9.5, fontname="helv", color=(0, 0, 0))

    # If we have more than 14 pages, trim
    while doc.page_count > 14:
        doc.delete_page(doc.page_count - 1)

    # Add page numbers to all pages
    for i in range(doc.page_count):
        p = doc[i]
        p.insert_text(pymupdf.Point(W / 2 - 10, H - 40), str(i + 1),
                      fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))

    # Set metadata
    doc.set_metadata({
        "title": "The Impact of Remote Work on Organizational Productivity",
        "author": "Elena Vasquez, James Whitfield, Aisha Okonkwo",
        "subject": "Working Paper - Remote Work Productivity",
        "keywords": "remote work, productivity, hybrid, organizational performance",
        "creator": "Stanford Center for Workforce Innovation",
    })

    # Add table of contents / bookmarks
    toc = [
        [1, "Title Page", 1],
        [1, "Abstract", 2],
        [1, "1. Introduction", 3],
        [1, "2. Literature Review", 4],
        [1, "3. Methodology", 5],
        [1, "4. Results", 6],
        [1, "5. Discussion", 7],
        [1, "6. Limitations and Future Research", 8],
        [1, "7. Conclusion", 9],
        [1, "References", 10],
    ]
    # Only set TOC entries for pages that exist
    toc = [t for t in toc if t[2] <= doc.page_count]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 14')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
