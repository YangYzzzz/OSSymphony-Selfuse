"""
Initial Setup: Create a 12-page statistics paper with 'p < 0.05' appearing 9 times across pages 5-10
Task ID: pdf_res_003
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_003'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/stats_analysis.pdf'


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

    # ---- Page layout constants ----
    W, H = 595, 842  # A4
    LEFT = 72
    RIGHT = W - 72
    TOP = 72
    BOT = H - 50
    TEXT_W = RIGHT - LEFT

    def add_header_footer(page, page_num):
        """Add running header and footer."""
        page.insert_text(pymupdf.Point(LEFT, 30), "Journal of Applied Statistics, Vol. 47, No. 3, 2025",
                         fontsize=8, fontname="tiit", color=(0.4, 0.4, 0.4))
        page.insert_text(pymupdf.Point(W / 2 - 10, H - 20), str(page_num),
                         fontsize=9, fontname="tiro", color=(0.3, 0.3, 0.3))

    def insert_body(page, y, text, fontname="tiro", fontsize=10.5, color=(0, 0, 0)):
        """Insert wrapped body text starting at y. Returns new y after text."""
        rect = pymupdf.Rect(LEFT, y, RIGHT, BOT)
        page.insert_textbox(rect, text, fontsize=fontsize, fontname=fontname,
                            color=color, align=pymupdf.TEXT_ALIGN_JUSTIFY)
        # Estimate how far the text extends
        lines = len(text) * fontsize * 0.5 / TEXT_W
        return y + lines * (fontsize + 2) + 10

    # ============================================================
    # PAGE 1: Title page
    # ============================================================
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, 1)
    p.insert_text(pymupdf.Point(LEFT, 120),
                  "A Comprehensive Statistical Analysis of Treatment",
                  fontsize=18, fontname="tibo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(LEFT, 148),
                  "Efficacy Across Multi-Center Clinical Trials",
                  fontsize=18, fontname="tibo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(LEFT, 195),
                  "Rebecca A. Morrison, David K. Patel, Lisa Tanaka, James O'Brien",
                  fontsize=11, fontname="tiro", color=(0.2, 0.2, 0.2))
    p.insert_text(pymupdf.Point(LEFT, 215),
                  "Department of Biostatistics, Stanford University School of Medicine",
                  fontsize=10, fontname="tiit", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(LEFT, 235),
                  "Correspondence: r.morrison@stanford.edu",
                  fontsize=9, fontname="tiro", color=(0.3, 0.3, 0.3))

    abstract_text = (
        "Abstract: This study presents a comprehensive statistical evaluation of treatment efficacy "
        "data collected from 14 clinical trial centers across North America between 2021 and 2024. "
        "We employed mixed-effects regression models, Kaplan-Meier survival analysis, and Bayesian "
        "hierarchical modeling to assess outcomes across 2,847 participants. Primary endpoints included "
        "overall survival, progression-free survival, and quality-of-life indices. Our analysis reveals "
        "statistically significant improvements in treatment arms compared to control groups, with "
        "effect sizes ranging from 0.34 to 0.72 (Cohen's d). The findings support the hypothesis that "
        "the novel therapeutic protocol yields clinically meaningful benefits across diverse patient "
        "populations and treatment settings."
    )
    rect = pymupdf.Rect(LEFT, 270, RIGHT, 430)
    p.insert_textbox(rect, abstract_text, fontsize=10, fontname="tiro",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    keywords_text = "Keywords: clinical trials, mixed-effects models, treatment efficacy, survival analysis, multi-center study"
    p.insert_text(pymupdf.Point(LEFT, 445), keywords_text,
                  fontsize=9, fontname="tiit", color=(0.2, 0.2, 0.2))

    # ============================================================
    # PAGE 2: Introduction
    # ============================================================
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, 2)
    p.insert_text(pymupdf.Point(LEFT, TOP), "1. Introduction", fontsize=14, fontname="tibo")
    intro_text = (
        "The evaluation of treatment efficacy in multi-center clinical trials presents "
        "unique statistical challenges. Heterogeneity across trial sites, varying patient "
        "demographics, and differences in clinical protocols necessitate robust analytical "
        "frameworks that can account for these sources of variability. Previous meta-analyses "
        "(Thompson et al., 2022; Williams & Garcia, 2023) have highlighted the importance "
        "of hierarchical modeling approaches when synthesizing evidence across centers.\n\n"
        "In this paper, we extend the work of Chen and Nakamura (2023) by incorporating "
        "time-varying covariates and center-specific random effects into a unified Bayesian "
        "framework. Our approach allows for simultaneous estimation of treatment effects and "
        "between-center heterogeneity, providing more precise confidence intervals than "
        "traditional fixed-effects approaches.\n\n"
        "The remainder of this paper is organized as follows. Section 2 describes the study "
        "design and data collection methodology. Section 3 presents the statistical methods "
        "employed, including model specification and estimation procedures. Section 4 reports "
        "the results of our primary and secondary analyses. Section 5 discusses the implications "
        "of our findings, and Section 6 offers concluding remarks.\n\n"
        "The dataset comprises 2,847 patients enrolled across 14 centers, with follow-up "
        "periods ranging from 6 to 36 months. Enrollment criteria required participants to be "
        "between 18 and 75 years of age, with confirmed diagnoses and no prior exposure to the "
        "experimental compound. Randomization was stratified by center, age group, and baseline "
        "disease severity."
    )
    rect = pymupdf.Rect(LEFT, TOP + 22, RIGHT, BOT)
    p.insert_textbox(rect, intro_text, fontsize=10.5, fontname="tiro",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 3: Study Design & Methods (part 1)
    # ============================================================
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, 3)
    p.insert_text(pymupdf.Point(LEFT, TOP), "2. Study Design and Data Collection", fontsize=14, fontname="tibo")
    methods1_text = (
        "2.1 Participant Recruitment\n\n"
        "Participants were recruited from 14 academic medical centers across the United States "
        "and Canada between January 2021 and December 2023. Each center obtained independent "
        "IRB approval prior to enrollment. Inclusion criteria specified adults aged 18-75 with "
        "confirmed Stage II-III disease per the revised 2020 classification system.\n\n"
        "2.2 Randomization and Blinding\n\n"
        "A central randomization server employed block randomization with variable block sizes "
        "(4, 6, or 8) stratified by center, age (<50 vs >= 50), and disease severity (moderate "
        "vs severe). The study was double-blinded, with matching placebo prepared by an "
        "independent pharmacy. Unblinding occurred only after database lock.\n\n"
        "2.3 Data Collection Procedures\n\n"
        "Clinical assessments were performed at baseline, weeks 4, 8, 12, 24, and 36. "
        "Laboratory panels included complete blood count, comprehensive metabolic panel, and "
        "disease-specific biomarkers (IL-6, CRP, TNF-alpha). Quality of life was assessed "
        "using the SF-36 instrument at each visit. Adverse events were coded using MedDRA "
        "version 25.0 and graded per CTCAE v5.0 criteria."
    )
    rect = pymupdf.Rect(LEFT, TOP + 22, RIGHT, BOT)
    p.insert_textbox(rect, methods1_text, fontsize=10.5, fontname="tiro",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 4: Statistical Methods
    # ============================================================
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, 4)
    p.insert_text(pymupdf.Point(LEFT, TOP), "3. Statistical Methods", fontsize=14, fontname="tibo")
    methods2_text = (
        "3.1 Primary Analysis\n\n"
        "The primary endpoint was overall survival (OS), defined as time from randomization to "
        "death from any cause. Kaplan-Meier curves were constructed for each treatment arm, and "
        "differences were assessed using the log-rank test. Hazard ratios were estimated via Cox "
        "proportional hazards models with treatment, center, and stratification factors as "
        "covariates. The proportional hazards assumption was verified using Schoenfeld residuals.\n\n"
        "3.2 Mixed-Effects Modeling\n\n"
        "To account for between-center variability, we specified a linear mixed-effects model "
        "with center as a random intercept and treatment as a fixed effect. The model can be "
        "written as:\n\n"
        "    Y_ij = beta_0 + beta_1 * Treatment_ij + b_j + epsilon_ij\n\n"
        "where b_j ~ N(0, sigma_b^2) represents the random center effect and epsilon_ij ~ "
        "N(0, sigma^2) is the residual error. Model parameters were estimated using restricted "
        "maximum likelihood (REML).\n\n"
        "3.3 Bayesian Hierarchical Model\n\n"
        "We also fitted a Bayesian hierarchical model using Hamiltonian Monte Carlo (HMC) "
        "sampling, implemented in Stan. Weakly informative priors were placed on treatment "
        "effects (Normal(0, 10)) and variance components (half-Cauchy(0, 5)). Four chains of "
        "5,000 iterations (2,000 warmup) were run, with convergence assessed via R-hat "
        "statistics and trace plots."
    )
    rect = pymupdf.Rect(LEFT, TOP + 22, RIGHT, BOT)
    p.insert_textbox(rect, methods2_text, fontsize=10.5, fontname="tiro",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 5 (0-indexed: 4): Results - first occurrence of 'p < 0.05'
    # Occurrences on this page: 2
    # ============================================================
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, 5)
    p.insert_text(pymupdf.Point(LEFT, TOP), "4. Results", fontsize=14, fontname="tibo")
    results1_text = (
        "4.1 Patient Characteristics\n\n"
        "A total of 2,847 patients were randomized: 1,426 to the treatment arm and 1,421 to "
        "placebo. Baseline characteristics were well-balanced between arms (Table 1). Median "
        "age was 54.2 years (IQR: 43.8-63.1), 52.3% were female, and 67.8% had severe disease "
        "at baseline. The median follow-up time was 28.4 months (range: 6.1-36.0).\n\n"
        "4.2 Primary Endpoint: Overall Survival\n\n"
        "Median overall survival was 24.7 months in the treatment arm versus 19.3 months in "
        "the placebo arm (HR = 0.71, 95% CI: 0.62-0.81, p < 0.05). The 2-year survival rate "
        "was 52.1% in the treatment group compared with 38.6% in the control group. Subgroup "
        "analyses demonstrated consistent treatment benefit across all pre-specified subgroups, "
        "including age, sex, disease severity, and geographic region.\n\n"
        "4.3 Secondary Endpoint: Progression-Free Survival\n\n"
        "Progression-free survival was significantly longer in the treatment arm (median 16.2 "
        "vs 11.8 months, HR = 0.68, 95% CI: 0.59-0.78, p < 0.05). The treatment effect was "
        "particularly pronounced in patients with severe baseline disease (HR = 0.59, 95% CI: "
        "0.48-0.73)."
    )
    rect = pymupdf.Rect(LEFT, TOP + 22, RIGHT, BOT)
    p.insert_textbox(rect, results1_text, fontsize=10.5, fontname="tiro",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 6 (0-indexed: 5): Results continued
    # Occurrences: 2
    # ============================================================
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, 6)
    p.insert_text(pymupdf.Point(LEFT, TOP), "4.4 Quality of Life Outcomes", fontsize=12, fontname="tibo")
    results2_text = (
        "Mean SF-36 physical component scores improved significantly from baseline in the "
        "treatment arm (delta = 8.4 points, SD = 12.1) compared with placebo (delta = 3.2 "
        "points, SD = 11.8; between-group difference = 5.2, 95% CI: 3.8-6.6, p < 0.05). "
        "Mental component scores also showed improvement, though the difference was smaller "
        "(between-group difference = 2.8, 95% CI: 1.4-4.2, p < 0.05).\n\n"
        "4.5 Biomarker Analysis\n\n"
        "IL-6 levels decreased by a median of 34.2% in the treatment arm versus 12.7% in "
        "the placebo arm at week 12 (Mann-Whitney U test, U = 845,231). CRP showed similar "
        "patterns, with treatment-associated reductions of 41.5% compared to 18.3% in controls. "
        "TNF-alpha levels remained stable in both groups throughout the study period.\n\n"
        "4.6 Mixed-Effects Model Results\n\n"
        "The linear mixed-effects model confirmed the treatment effect after adjusting for "
        "center-level variability. The estimated treatment coefficient was beta_1 = 3.47 "
        "(SE = 0.82), indicating a significant positive effect on the primary outcome measure. "
        "The intra-class correlation coefficient (ICC) for center was 0.08, suggesting modest "
        "but non-negligible between-center heterogeneity."
    )
    rect = pymupdf.Rect(LEFT, TOP + 20, RIGHT, BOT)
    p.insert_textbox(rect, results2_text, fontsize=10.5, fontname="tiro",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 7 (0-indexed: 6): More results
    # Occurrences: 2
    # ============================================================
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, 7)
    p.insert_text(pymupdf.Point(LEFT, TOP), "4.7 Bayesian Analysis", fontsize=12, fontname="tibo")
    results3_text = (
        "The Bayesian hierarchical model yielded a posterior mean treatment effect of 3.52 "
        "(95% credible interval: 1.91-5.13), consistent with the frequentist analysis. The "
        "posterior probability that the treatment effect exceeds 2.0 (the pre-specified "
        "minimum clinically important difference) was 0.94.\n\n"
        "4.8 Subgroup Analyses\n\n"
        "Pre-specified subgroup analyses revealed differential treatment effects across patient "
        "subpopulations. Patients aged 50-65 demonstrated the strongest response (HR = 0.58, "
        "95% CI: 0.44-0.76, p < 0.05), while those over 65 showed a more modest benefit "
        "(HR = 0.79, 95% CI: 0.63-0.99, p < 0.05). Female patients showed numerically greater "
        "benefit than males, though the interaction term was not statistically significant "
        "(p = 0.12).\n\n"
        "4.9 Safety and Adverse Events\n\n"
        "Grade 3 or higher adverse events occurred in 23.4% of the treatment group versus "
        "18.7% of the placebo group. The most common treatment-related adverse events were "
        "fatigue (34.2%), nausea (21.8%), and headache (18.4%). Three treatment-related deaths "
        "were reported (0.2%), all attributed to cardiac events in patients with pre-existing "
        "cardiovascular conditions."
    )
    rect = pymupdf.Rect(LEFT, TOP + 20, RIGHT, BOT)
    p.insert_textbox(rect, results3_text, fontsize=10.5, fontname="tiro",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 8 (0-indexed: 7): Tables
    # Occurrences: 1
    # ============================================================
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, 8)
    p.insert_text(pymupdf.Point(LEFT, TOP), "Table 2. Summary of Statistical Tests", fontsize=12, fontname="tibo")

    table_text = (
        "Endpoint                   HR/Diff    95% CI           P-value      Significance\n"
        "------------------------------------------------------------------------------------\n"
        "Overall Survival           0.71       0.62-0.81        0.0003       p < 0.05\n"
        "Progression-Free Surv.     0.68       0.59-0.78        0.0001       Yes\n"
        "QoL Physical               +5.2       3.8-6.6          0.0012       Yes\n"
        "QoL Mental                 +2.8       1.4-4.2          0.0234       Yes\n"
        "Subgroup: Age 50-65        0.58       0.44-0.76        0.0001       Yes\n"
        "Subgroup: Age >65          0.79       0.63-0.99        0.0420       Yes\n"
        "Subgroup: Female           0.64       0.51-0.80        0.0002       Yes\n"
        "Subgroup: Male             0.77       0.63-0.94        0.0098       Yes\n"
    )
    rect = pymupdf.Rect(LEFT, TOP + 25, RIGHT, TOP + 200)
    p.insert_textbox(rect, table_text, fontsize=9, fontname="cour",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    # Additional text below the table
    table_note = (
        "Note: All P-values are two-sided. Hazard ratios less than 1.0 favor the treatment arm. "
        "Confidence intervals were computed using the profile likelihood method.\n\n"
        "4.10 Sensitivity Analyses\n\n"
        "To assess robustness, we conducted several sensitivity analyses. Excluding the two "
        "smallest centers (n < 100) did not materially change the results (HR = 0.72, 95% CI: "
        "0.63-0.83). An intention-to-treat analysis including all randomized patients regardless "
        "of protocol deviations yielded similar findings (HR = 0.73, 95% CI: 0.64-0.84). "
        "Multiple imputation for missing quality-of-life data (15.2% missing at 36 months) "
        "produced treatment effect estimates within 5% of the complete-case analysis."
    )
    rect = pymupdf.Rect(LEFT, TOP + 215, RIGHT, BOT)
    p.insert_textbox(rect, table_note, fontsize=10.5, fontname="tiro",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 9 (0-indexed: 8): Discussion
    # Occurrences: 1
    # ============================================================
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, 9)
    p.insert_text(pymupdf.Point(LEFT, TOP), "5. Discussion", fontsize=14, fontname="tibo")
    discussion_text = (
        "The results of this multi-center trial provide strong evidence for the efficacy of "
        "the novel therapeutic protocol. The observed hazard ratio of 0.71 for overall survival "
        "is clinically meaningful and compares favorably with established treatments in this "
        "disease area. Our findings align with the preliminary phase II data reported by "
        "Nakamura et al. (2022) and extend them to a larger, more diverse population.\n\n"
        "The mixed-effects analysis is particularly noteworthy. By explicitly modeling center-level "
        "heterogeneity, we obtained more precise treatment effect estimates than would be possible "
        "with a simple stratified analysis. The ICC of 0.08 indicates that approximately 8% of "
        "the total variance in outcomes is attributable to differences between centers, consistent "
        "with previous multi-center oncology trials.\n\n"
        "The Bayesian analysis provided complementary insights. The posterior probability of 0.94 "
        "that the treatment effect exceeds the MCID of 2.0 is directly interpretable as a "
        "probability statement about clinical relevance, unlike a traditional frequentist "
        "significance test. This distinction is increasingly "
        "recognized as important in the clinical trial literature (Gelman et al., 2023).\n\n"
        "Several limitations warrant discussion. First, the study population was predominantly "
        "North American, which may limit generalizability to other populations. Second, the "
        "36-month follow-up period may be insufficient to capture long-term treatment effects "
        "or late-occurring adverse events."
    )
    rect = pymupdf.Rect(LEFT, TOP + 22, RIGHT, BOT - 30)
    p.insert_textbox(rect, discussion_text, fontsize=10.5, fontname="tiro",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # Add a standalone line with 'p < 0.05' using insert_text (single span)
    p.insert_text(pymupdf.Point(LEFT, BOT - 10),
                  "All primary comparisons achieved significance at p < 0.05 (two-sided).",
                  fontsize=10.5, fontname="tiro", color=(0, 0, 0))

    # ============================================================
    # PAGE 10 (0-indexed: 9): Discussion continued
    # Occurrences: 1
    # ============================================================
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, 10)
    discussion2_text = (
        "5.1 Comparison with Existing Literature\n\n"
        "Our findings are consistent with the growing body of evidence supporting this "
        "therapeutic approach. The meta-analysis by Thompson et al. (2022) reported a pooled "
        "hazard ratio of 0.75 (95% CI: 0.65-0.87) across 8 earlier trials, which aligns with "
        "our estimate of 0.71. However, our study benefits from a larger sample size, longer "
        "follow-up, and more rigorous statistical methodology.\n\n"
        "5.2 Clinical Implications\n\n"
        "The observed treatment benefit, with overall survival improvement that was "
        "consistently demonstrated across subgroups at a statistically significant level, "
        "has immediate clinical implications. "
        "First, it supports adoption of the protocol as a standard-of-care option for patients "
        "meeting our inclusion criteria. Second, the subgroup analyses suggest that patients "
        "aged 50-65 may derive the greatest benefit, informing treatment selection decisions.\n\n"
        "5.3 Future Directions\n\n"
        "Several avenues for future research emerge from this work. Longer-term follow-up will "
        "be essential to characterize the durability of the treatment effect. Biomarker-guided "
        "patient selection strategies, using the IL-6 and CRP patterns identified here, could "
        "improve treatment precision. Finally, combination regimens incorporating this therapy "
        "with emerging immunological agents merit investigation."
    )
    rect = pymupdf.Rect(LEFT, TOP, RIGHT, BOT - 30)
    p.insert_textbox(rect, discussion2_text, fontsize=10.5, fontname="tiro",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # Add a standalone line with 'p < 0.05' using insert_text (single span)
    p.insert_text(pymupdf.Point(LEFT, BOT - 10),
                  "The threshold of p < 0.05 was consistently met across all primary analyses.",
                  fontsize=10.5, fontname="tiro", color=(0, 0, 0))

    # ============================================================
    # PAGE 11 (0-indexed: 10): Conclusions
    # ============================================================
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, 11)
    p.insert_text(pymupdf.Point(LEFT, TOP), "6. Conclusions", fontsize=14, fontname="tibo")
    conclusion_text = (
        "This multi-center randomized controlled trial demonstrates that the novel therapeutic "
        "protocol produces statistically significant and clinically meaningful improvements in "
        "overall survival, progression-free survival, and quality of life. The consistency of "
        "results across frequentist and Bayesian analytical frameworks, and across multiple "
        "patient subgroups, strengthens confidence in the robustness of these findings.\n\n"
        "The mixed-effects approach effectively addressed between-center heterogeneity, "
        "providing more reliable effect estimates for a multi-center trial of this scale. We "
        "recommend this analytical strategy for future multi-center trials in similar settings.\n\n"
        "Acknowledgments\n\n"
        "This work was supported by grants from the National Institutes of Health (R01-CA234567) "
        "and the National Science Foundation (DMS-1901234). The authors thank the patients and "
        "families who participated in this trial, the clinical research coordinators at all 14 "
        "sites, and the Data Safety Monitoring Board members for their invaluable contributions."
    )
    rect = pymupdf.Rect(LEFT, TOP + 22, RIGHT, BOT)
    p.insert_textbox(rect, conclusion_text, fontsize=10.5, fontname="tiro",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 12 (0-indexed: 11): References
    # ============================================================
    p = doc.new_page(width=W, height=H)
    add_header_footer(p, 12)
    p.insert_text(pymupdf.Point(LEFT, TOP), "References", fontsize=14, fontname="tibo")
    references_text = (
        "1. Chen, W. & Nakamura, T. (2023). Bayesian hierarchical models for multi-center "
        "clinical trials: A practical guide. Biometrics, 79(2), 1123-1138.\n\n"
        "2. Gelman, A., Vehtari, A., Simpson, D. et al. (2023). Bayesian workflow for "
        "clinical trials. Statistics in Medicine, 42(8), 1412-1430.\n\n"
        "3. Nakamura, T. et al. (2022). Phase II results of the novel therapeutic protocol: "
        "A multi-center study. Journal of Clinical Oncology, 40(15), 4521-4532.\n\n"
        "4. Thompson, R.J., Williams, S.A. & Garcia, M.L. (2022). Meta-analysis of treatment "
        "efficacy in Stage II-III disease: An updated systematic review. Lancet Oncology, "
        "23(4), 567-579.\n\n"
        "5. Williams, S.A. & Garcia, M.L. (2023). Accounting for heterogeneity in multi-center "
        "trials: A comparison of analytical approaches. Journal of the Royal Statistical "
        "Society, Series A, 186(1), 89-112.\n\n"
        "6. Morrison, R.A. & Patel, D.K. (2024). Statistical considerations for adaptive "
        "clinical trial designs. Annual Review of Statistics and Its Application, 11, 45-68.\n\n"
        "7. Kaplan, E.L. & Meier, P. (1958). Nonparametric estimation from incomplete "
        "observations. Journal of the American Statistical Association, 53(282), 457-481.\n\n"
        "8. Cox, D.R. (1972). Regression models and life tables. Journal of the Royal "
        "Statistical Society, Series B, 34(2), 187-220."
    )
    rect = pymupdf.Rect(LEFT, TOP + 22, RIGHT, BOT)
    p.insert_textbox(rect, references_text, fontsize=9.5, fontname="tiro",
                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify the 'p < 0.05' count
    doc = pymupdf.open(OUTPUT)
    total_count = 0
    for i in range(doc.page_count):
        instances = doc[i].search_for("p < 0.05")
        if instances:
            print(f"  Page {i+1}: found {len(instances)} instances of 'p < 0.05'")
            total_count += len(instances)
    doc.close()
    print(f"  Total 'p < 0.05' instances: {total_count}")
    print(f"  Page count: 12")

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
