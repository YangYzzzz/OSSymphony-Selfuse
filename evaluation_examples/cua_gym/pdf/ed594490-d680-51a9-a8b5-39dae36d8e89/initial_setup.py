"""
Initial Setup: Create a 15-page thesis document with sensitive research results.
Task ID: pdf_res_047
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_047'
THESIS_DIR = f'{WORKDIR}/thesis'
OUTPUT = f'{THESIS_DIR}/confidential_results.pdf'


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
    os.makedirs(THESIS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page geometry ---
    W, H = 595, 842  # A4
    margin_left = 72
    margin_right = 523
    margin_top = 72
    text_width = margin_right - margin_left

    # ============================================================
    # Page 1: Title Page
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(W / 2 - 140, 200),
                     "CONFIDENTIAL", fontsize=28, fontname="hebo", color=(0.7, 0, 0))
    page.insert_text(pymupdf.Point(margin_left, 300),
                     "Phase III Clinical Trial Results:", fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(margin_left, 330),
                     "Compound ARX-7742 for Treatment of", fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(margin_left, 360),
                     "Treatment-Resistant Major Depressive Disorder", fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(margin_left, 440),
                     "Principal Investigator: Dr. Elena Vasquez, MD, PhD", fontsize=13, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(margin_left, 465),
                     "Co-Investigators: Dr. James Hartfield, Dr. Mei-Ling Wu", fontsize=13, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(margin_left, 500),
                     "NovaCrest Pharmaceuticals, Inc.", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(margin_left, 525),
                     "Internal Document - Not for Distribution", fontsize=11, fontname="heit", color=(0.5, 0, 0))
    page.insert_text(pymupdf.Point(margin_left, 560),
                     "Protocol ID: NCP-ARX7742-P3-2025", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(margin_left, 585),
                     "Date: March 15, 2025", fontsize=11, fontname="helv", color=(0, 0, 0))

    # ============================================================
    # Page 2: Table of Contents
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "Table of Contents", fontsize=18, fontname="hebo", color=(0, 0, 0))
    toc_entries = [
        ("1. Executive Summary", 3),
        ("2. Study Design and Methodology", 4),
        ("3. Patient Demographics and Baseline Characteristics", 5),
        ("4. Primary Efficacy Endpoints", 6),
        ("5. Secondary Efficacy Endpoints", 7),
        ("6. Biomarker Analysis", 8),
        ("7. Safety and Adverse Events", 9),
        ("8. Pharmacokinetic Data", 10),
        ("9. Subgroup Analyses", 11),
        ("10. Statistical Methodology", 12),
        ("11. Regulatory Implications", 13),
        ("12. Competitive Landscape Analysis", 14),
        ("13. Conclusions and Recommendations", 15),
    ]
    y = margin_top + 70
    for title, pg in toc_entries:
        page.insert_text(pymupdf.Point(margin_left, y), title, fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(margin_right - 20, y), str(pg), fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 22

    # ============================================================
    # Page 3: Executive Summary
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "1. Executive Summary", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    summary_text = (
        "This report presents the complete results of the Phase III randomized, double-blind, "
        "placebo-controlled trial of ARX-7742, a novel serotonin-glutamate dual modulator, for the "
        "treatment of treatment-resistant major depressive disorder (TR-MDD). The study enrolled 1,247 "
        "patients across 43 clinical sites in North America and Europe over a 52-week treatment period.\n\n"
        "ARX-7742 demonstrated statistically significant superiority over placebo on the primary endpoint "
        "(MADRS total score change from baseline at Week 12): -15.3 points vs -9.8 points (p < 0.001, "
        "Cohen's d = 0.62). The response rate (>=50% MADRS reduction) was 58.2% for ARX-7742 vs 31.4% "
        "for placebo (NNT = 3.7). Remission rates (MADRS <= 10) reached 34.7% vs 16.2% (p < 0.001).\n\n"
        "The safety profile was generally favorable. The most common adverse events were mild nausea (18.3%), "
        "headache (14.1%), and dizziness (9.7%). Serious adverse events occurred in 4.2% of the treatment "
        "group vs 3.8% in placebo. No treatment-related deaths were reported. Hepatic transaminase elevations "
        ">3x ULN occurred in 1.8% of patients, requiring enhanced monitoring protocols.\n\n"
        "Based on these results, NovaCrest plans to submit an NDA to the FDA in Q3 2025, with an anticipated "
        "PDUFA date in Q2 2026. The commercial opportunity is estimated at $2.8B peak annual revenue."
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, summary_text, fontsize=10.5, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # Page 4: Study Design
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "2. Study Design and Methodology", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    design_text = (
        "Study Design: Phase III, randomized (1:1), double-blind, placebo-controlled, multi-center, "
        "parallel-group trial with a 52-week treatment period and 4-week follow-up.\n\n"
        "Inclusion Criteria:\n"
        "  - Adults aged 18-65 with DSM-5 diagnosis of MDD\n"
        "  - Failed >= 2 adequate antidepressant trials in the current episode\n"
        "  - MADRS total score >= 26 at screening and baseline\n"
        "  - Duration of current episode: 8 weeks to 24 months\n\n"
        "Exclusion Criteria:\n"
        "  - Active suicidal ideation (C-SSRS score >= 4)\n"
        "  - History of psychotic features, bipolar disorder, or schizophrenia\n"
        "  - Substance use disorder within the past 6 months\n"
        "  - Hepatic impairment (Child-Pugh B or C)\n\n"
        "Dosing: ARX-7742 25mg once daily for Week 1, titrated to 50mg for Weeks 2-4, "
        "then 75mg maintenance dose from Week 5 onward. Dose adjustments (50-100mg) permitted "
        "based on tolerability starting Week 8.\n\n"
        "Primary Endpoint: Change from baseline in MADRS total score at Week 12.\n\n"
        "Key Secondary Endpoints: CGI-S change at Week 12, SDS total score at Week 12, "
        "MADRS response rate, MADRS remission rate, time to sustained response."
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, design_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ============================================================
    # Page 5: Patient Demographics
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "3. Patient Demographics and Baseline Characteristics", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    demo_text = (
        "A total of 1,247 patients were randomized: 624 to ARX-7742 and 623 to placebo. "
        "The safety population comprised 1,238 patients (619 ARX-7742, 619 placebo). "
        "Baseline characteristics were well-balanced between treatment groups.\n\n"
        "Mean age: 42.3 years (SD 11.8) | Female: 63.4% | White: 71.2% | Black: 14.8% | "
        "Asian: 8.3% | Hispanic: 18.6%\n\n"
        "Mean baseline MADRS: 33.7 (SD 5.1) | Mean number of prior failed treatments: 3.2 (SD 1.4)\n"
        "Mean duration of current episode: 14.2 months (SD 6.8)\n"
        "Comorbid anxiety disorder: 47.3% | Prior ECT: 8.2%\n\n"
        "Disposition: 82.4% of ARX-7742 patients and 75.1% of placebo patients completed the "
        "52-week treatment period. Discontinuation due to adverse events: 7.3% vs 4.1%. "
        "Discontinuation due to lack of efficacy: 4.8% vs 12.3%.\n\n"
        "Site Distribution: 28 sites in the US, 8 in Canada, 4 in the UK, 3 in Germany. "
        "Mean enrollment per site: 29 patients (range: 12-48)."
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, demo_text, fontsize=10.5, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # Page 6: Primary Efficacy
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "4. Primary Efficacy Endpoints", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    efficacy_text = (
        "Primary Endpoint Results - MADRS Total Score Change from Baseline at Week 12:\n\n"
        "ARX-7742 (n=624): LS Mean Change = -15.3 (SE 0.51)\n"
        "Placebo (n=623):  LS Mean Change = -9.8 (SE 0.52)\n"
        "Treatment Difference: -5.5 (95% CI: -6.9 to -4.1)\n"
        "p-value: < 0.001 | Effect Size (Cohen's d): 0.62\n\n"
        "The primary endpoint was met with high statistical significance. Separation from placebo "
        "was first observed at Week 2 (p = 0.012) and was maintained at all subsequent timepoints. "
        "The treatment effect was consistent across all pre-specified subgroups (age, sex, race, "
        "baseline severity, number of prior treatment failures).\n\n"
        "Sensitivity Analyses:\n"
        "  - MMRM analysis (primary): p < 0.001\n"
        "  - Pattern Mixture Model: p < 0.001\n"
        "  - Tipping Point Analysis: robust to 3.2-point penalty\n"
        "  - ANCOVA LOCF: p < 0.001\n\n"
        "MADRS Response Rate (>=50% reduction): ARX-7742 58.2% vs Placebo 31.4% (p < 0.001, NNT = 3.7)\n"
        "MADRS Remission Rate (<=10): ARX-7742 34.7% vs Placebo 16.2% (p < 0.001, NNT = 5.4)\n"
        "Sustained Response (>=6 consecutive weeks): ARX-7742 44.1% vs Placebo 21.8% (p < 0.001)"
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, efficacy_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ============================================================
    # Page 7: Secondary Efficacy
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "5. Secondary Efficacy Endpoints", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    secondary_text = (
        "CGI-Severity Change at Week 12:\n"
        "  ARX-7742: -1.8 (SE 0.08) vs Placebo: -1.1 (SE 0.08), p < 0.001\n\n"
        "CGI-Improvement at Week 12 (Much/Very Much Improved):\n"
        "  ARX-7742: 52.3% vs Placebo: 28.9%, p < 0.001\n\n"
        "Sheehan Disability Scale (SDS) Total Score at Week 12:\n"
        "  ARX-7742: -8.4 (SE 0.38) vs Placebo: -5.1 (SE 0.39), p < 0.001\n\n"
        "PHQ-9 Score Change at Week 12:\n"
        "  ARX-7742: -9.2 (SE 0.33) vs Placebo: -5.8 (SE 0.34), p < 0.001\n\n"
        "Quality of Life (Q-LES-Q-SF) Percent Maximum Score at Week 12:\n"
        "  ARX-7742: +18.4% vs Placebo: +9.7%, p < 0.001\n\n"
        "Time to Sustained Response (Kaplan-Meier):\n"
        "  Median: ARX-7742: 6.2 weeks vs Placebo: Not reached\n"
        "  HR = 2.14 (95% CI: 1.78-2.57), p < 0.001\n\n"
        "Cognitive Function (DSST) at Week 12:\n"
        "  ARX-7742: +5.3 symbols (SE 0.42) vs Placebo: +2.1 symbols (SE 0.43), p < 0.001\n\n"
        "All key secondary endpoints were met after multiplicity adjustment using a hierarchical "
        "testing procedure (Hochberg method)."
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, secondary_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ============================================================
    # Page 8: Biomarker Analysis
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "6. Biomarker Analysis", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    biomarker_text = (
        "Exploratory biomarker analyses were conducted in a subset of 412 patients who consented "
        "to additional blood sampling.\n\n"
        "Peripheral BDNF Levels:\n"
        "  Baseline mean: 22.4 ng/mL (SD 8.3)\n"
        "  Week 12 change - ARX-7742: +6.8 ng/mL vs Placebo: +1.2 ng/mL (p < 0.001)\n"
        "  Correlation with MADRS improvement: r = 0.34 (p < 0.001)\n\n"
        "Inflammatory Markers:\n"
        "  CRP > 3 mg/L at baseline: 38.2% of subset\n"
        "  High-CRP subgroup response rate: ARX-7742 62.4% vs Placebo 24.1% (p < 0.001)\n"
        "  Low-CRP subgroup response rate: ARX-7742 55.8% vs Placebo 35.7% (p < 0.001)\n"
        "  Interaction p-value: 0.024 (suggesting enhanced benefit in inflammatory phenotype)\n\n"
        "IL-6 Change: ARX-7742: -1.4 pg/mL vs Placebo: -0.2 pg/mL (p = 0.003)\n"
        "TNF-alpha Change: ARX-7742: -0.8 pg/mL vs Placebo: +0.1 pg/mL (p = 0.018)\n\n"
        "Cortisol (Salivary, Morning):\n"
        "  Baseline: 18.2 nmol/L (SD 7.1)\n"
        "  Week 12 change: ARX-7742: -4.3 nmol/L vs Placebo: -1.1 nmol/L (p = 0.002)\n\n"
        "These biomarker findings suggest ARX-7742 may have neuroplastic and anti-inflammatory "
        "mechanisms contributing to its antidepressant efficacy."
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, biomarker_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ============================================================
    # Page 9: Safety
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "7. Safety and Adverse Events", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    safety_text = (
        "Treatment-Emergent Adverse Events (TEAEs) occurring in >=5% of patients:\n\n"
        "  Nausea:       ARX-7742 18.3% vs Placebo 6.2%\n"
        "  Headache:     ARX-7742 14.1% vs Placebo 11.8%\n"
        "  Dizziness:    ARX-7742  9.7% vs Placebo  4.3%\n"
        "  Insomnia:     ARX-7742  8.4% vs Placebo  7.1%\n"
        "  Somnolence:   ARX-7742  7.2% vs Placebo  3.4%\n"
        "  Dry Mouth:    ARX-7742  6.8% vs Placebo  4.9%\n"
        "  Diarrhea:     ARX-7742  5.9% vs Placebo  4.2%\n"
        "  Fatigue:      ARX-7742  5.4% vs Placebo  4.8%\n\n"
        "Serious Adverse Events (SAEs): ARX-7742 4.2% vs Placebo 3.8%\n"
        "  - Suicidal ideation: 1.1% vs 1.3% (no completed suicides)\n"
        "  - Hepatic events: 0.6% vs 0.2%\n"
        "  - Seizure: 0.3% vs 0.0% (2 cases, both with risk factors)\n\n"
        "Hepatic Safety:\n"
        "  ALT > 3x ULN: ARX-7742 1.8% vs Placebo 0.5%\n"
        "  ALT > 5x ULN: ARX-7742 0.5% vs Placebo 0.2%\n"
        "  No cases of Hy's Law were identified.\n"
        "  All elevations resolved with dose reduction or discontinuation.\n\n"
        "Weight Change (Week 52): ARX-7742 +1.2 kg vs Placebo +0.4 kg (p = 0.031)\n"
        "Sexual Dysfunction (ASEX): No significant difference between groups (p = 0.412)\n"
        "QTc Prolongation: No clinically significant QTc changes observed."
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, safety_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ============================================================
    # Page 10: PK Data
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "8. Pharmacokinetic Data", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    pk_text = (
        "Population PK analysis was performed using data from 856 patients with evaluable "
        "PK samples at steady state.\n\n"
        "Key PK Parameters at 75mg Dose:\n"
        "  Cmax: 342 ng/mL (CV 28.4%)\n"
        "  Tmax: 2.5 hours (range: 1.0-5.0)\n"
        "  AUC(0-24): 4,218 ng*h/mL (CV 31.2%)\n"
        "  Cmin (trough): 89 ng/mL (CV 34.7%)\n"
        "  t1/2: 14.2 hours (SD 3.8)\n"
        "  Vd/F: 245 L (CV 22.1%)\n"
        "  CL/F: 17.8 L/h (CV 29.3%)\n\n"
        "Exposure-Response Analysis:\n"
        "  Cmin quartile and MADRS change correlation: r = -0.28 (p < 0.001)\n"
        "  Optimal exposure range: Cmin 60-150 ng/mL\n"
        "  Patients in target range: 72.4%\n\n"
        "Dose Adjustments:\n"
        "  Maintained at 75mg: 68.3%\n"
        "  Increased to 100mg: 18.4%\n"
        "  Decreased to 50mg: 13.3%\n\n"
        "Special Populations:\n"
        "  Mild hepatic impairment (Child-Pugh A): AUC +38%, dose cap at 50mg recommended\n"
        "  Mild renal impairment (eGFR 60-89): No significant PK differences\n"
        "  Elderly (>65, n=87): AUC +22%, starting dose of 25mg recommended\n"
        "  CYP2D6 poor metabolizers: AUC +45%, dose cap at 75mg recommended"
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, pk_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ============================================================
    # Page 11: Subgroup Analyses
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "9. Subgroup Analyses", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    subgroup_text = (
        "Pre-specified subgroup analyses of the primary endpoint (MADRS change at Week 12):\n\n"
        "By Sex:\n"
        "  Female (n=791): Treatment difference -5.8 (95% CI: -7.6 to -4.0)\n"
        "  Male (n=456):   Treatment difference -4.9 (95% CI: -7.1 to -2.7)\n"
        "  Interaction p = 0.482\n\n"
        "By Age Group:\n"
        "  18-35 (n=387):  Treatment difference -6.2 (95% CI: -8.5 to -3.9)\n"
        "  36-50 (n=498):  Treatment difference -5.3 (95% CI: -7.2 to -3.4)\n"
        "  51-65 (n=362):  Treatment difference -4.8 (95% CI: -7.0 to -2.6)\n"
        "  Interaction p = 0.618\n\n"
        "By Number of Prior Treatment Failures:\n"
        "  2 failures (n=542):  Treatment difference -4.7 (95% CI: -6.6 to -2.8)\n"
        "  3+ failures (n=705): Treatment difference -6.1 (95% CI: -8.0 to -4.2)\n"
        "  Interaction p = 0.133\n\n"
        "By Baseline Severity (MADRS):\n"
        "  26-32 (n=583):  Treatment difference -4.4 (95% CI: -6.2 to -2.6)\n"
        "  >32 (n=664):    Treatment difference -6.3 (95% CI: -8.3 to -4.3)\n"
        "  Interaction p = 0.058\n\n"
        "By Region:\n"
        "  North America (n=892): Treatment difference -5.7\n"
        "  Europe (n=355):        Treatment difference -5.0\n"
        "  Interaction p = 0.571\n\n"
        "All subgroup analyses showed consistent treatment benefit favoring ARX-7742."
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, subgroup_text, fontsize=10, fontname="helv", color=(0, 0, 0))

    # ============================================================
    # Page 12: Statistical Methodology
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "10. Statistical Methodology", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    stats_text = (
        "Primary Analysis Model:\n"
        "  Mixed-model repeated measures (MMRM) with unstructured covariance\n"
        "  Fixed effects: treatment, visit, treatment-by-visit, baseline MADRS, site region\n"
        "  Multiple imputation under MAR assumption for missing data\n\n"
        "Sample Size Justification:\n"
        "  Assumed treatment difference: 4.0 MADRS points (SD 12.0)\n"
        "  Power: 90% at two-sided alpha = 0.05\n"
        "  Required per group: 475 (accounting for 15% dropout)\n"
        "  Randomized: 624 per group (31% over-enrollment for regulatory robustness)\n\n"
        "Multiplicity Control:\n"
        "  Hierarchical testing of secondary endpoints (fixed sequence)\n"
        "  Hochberg procedure for supplementary analyses\n"
        "  Alpha spending: O'Brien-Fleming boundaries for interim analysis\n\n"
        "Interim Analysis:\n"
        "  Planned at 50% information fraction (n=624 completers)\n"
        "  Conducted by independent DSMB on March 1, 2025\n"
        "  Recommendation: Continue to full enrollment (no futility or overwhelming efficacy)\n\n"
        "Missing Data:\n"
        "  Overall missing: 11.3% at Week 12, 21.8% at Week 52\n"
        "  Pattern: MNAR in 4.2% (due to AE discontinuation)\n"
        "  Sensitivity: Tipping point, delta-adjustment, and jump-to-reference analyses\n"
        "  All sensitivity analyses confirmed primary result robustness"
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, stats_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ============================================================
    # Page 13: Regulatory Implications
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "11. Regulatory Implications", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    reg_text = (
        "NDA Submission Strategy:\n"
        "  Target submission: Q3 2025\n"
        "  Anticipated PDUFA date: Q2 2026\n"
        "  Filing basis: Two adequate Phase III trials (NCP-P3-2025 and NCP-P3-2024)\n"
        "  Priority Review eligibility: Under evaluation based on unmet medical need\n\n"
        "FDA Interactions:\n"
        "  Pre-NDA meeting conducted: January 15, 2025\n"
        "  Key FDA feedback:\n"
        "    - Hepatic monitoring program required in labeling\n"
        "    - REMS evaluation requested (hepatic risk management)\n"
        "    - 6-month carcinogenicity data accepted (12-month study ongoing)\n"
        "    - Pediatric study plan (PSP) agreed upon for ages 12-17\n\n"
        "Labeling Considerations:\n"
        "  Proposed indication: Treatment of TR-MDD in adults (failed >= 2 prior treatments)\n"
        "  Black box warning: Standard antidepressant suicidality warning\n"
        "  Hepatic monitoring: LFTs at baseline, monthly x3, then quarterly\n"
        "  Contraindication: Moderate-severe hepatic impairment\n\n"
        "International Regulatory:\n"
        "  EMA MAA submission planned: Q4 2025\n"
        "  PMDA (Japan) consultation: Ongoing, bridging study planned\n"
        "  Health Canada submission: Concurrent with FDA"
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, reg_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ============================================================
    # Page 14: Competitive Landscape
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "12. Competitive Landscape Analysis", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    comp_text = (
        "CONFIDENTIAL - COMMERCIAL SENSITIVE\n\n"
        "Current TR-MDD Market (2024):\n"
        "  Total addressable market: $8.4B globally\n"
        "  Esketamine (Spravato): $1.2B (2024), 38% YoY growth\n"
        "  Brexanolone (Zulresso): $0.3B (limited to PPD)\n"
        "  Psilocybin (Phase III): Compass Pathways, data expected Q4 2025\n"
        "  Rapastinel: Allergan program discontinued\n\n"
        "ARX-7742 Competitive Advantages:\n"
        "  1. Oral administration (vs intranasal/IV for esketamine)\n"
        "  2. No dissociative side effects\n"
        "  3. No requirement for REMS-certified healthcare settings\n"
        "  4. Daily home use (vs supervised administration)\n"
        "  5. Novel MOA with anti-inflammatory component\n\n"
        "Revenue Projections (CONFIDENTIAL):\n"
        "  Year 1 (2027): $420M\n"
        "  Year 2 (2028): $980M\n"
        "  Year 3 (2029): $1.8B\n"
        "  Peak (2031):   $2.8B\n\n"
        "Pricing Strategy:\n"
        "  Target WAC: $1,850/month\n"
        "  Payer access target: 65% commercial, 45% Medicare in Year 1\n"
        "  Patient assistance program: Planned from launch\n\n"
        "Patent Protection: Composition of matter patent expires 2039, method of use 2041."
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, comp_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # ============================================================
    # Page 15: Conclusions
    # ============================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(margin_left, margin_top + 30), "13. Conclusions and Recommendations", fontsize=16, fontname="hebo", color=(0, 0, 0.5))
    conclusion_text = (
        "Key Conclusions:\n\n"
        "1. ARX-7742 demonstrated robust, statistically significant, and clinically meaningful "
        "efficacy in treatment-resistant MDD, with a large treatment effect (Cohen's d = 0.62) "
        "on the primary endpoint.\n\n"
        "2. The safety profile is manageable with appropriate hepatic monitoring. No unexpected "
        "safety signals emerged during the 52-week treatment period.\n\n"
        "3. Biomarker data suggest a dual mechanism of action (neuroplastic + anti-inflammatory) "
        "that may enable precision medicine approaches.\n\n"
        "4. All key secondary endpoints were met, including functional improvement (SDS), "
        "cognitive enhancement (DSST), and quality of life (Q-LES-Q-SF).\n\n"
        "5. The benefit-risk profile strongly supports NDA submission.\n\n"
        "Recommendations:\n\n"
        "  - Proceed with NDA submission in Q3 2025 as planned\n"
        "  - Initiate Phase IIIb study in elderly population (>65 years)\n"
        "  - Begin pediatric trial per agreed PSP timeline\n"
        "  - Conduct post-marketing hepatic safety study (5,000 patient registry)\n"
        "  - Explore adjunctive use with existing antidepressants (Phase II planned)\n"
        "  - Develop companion diagnostic for CRP-based patient selection\n\n"
        "This document contains proprietary and confidential information of NovaCrest "
        "Pharmaceuticals, Inc. Unauthorized disclosure, reproduction, or distribution "
        "is strictly prohibited and may result in legal action."
    )
    rect = pymupdf.Rect(margin_left, margin_top + 55, margin_right, H - 72)
    page.insert_textbox(rect, conclusion_text, fontsize=10.5, fontname="helv", color=(0, 0, 0))

    # --- Set metadata ---
    doc.set_metadata({
        "title": "Phase III Clinical Trial Results - ARX-7742",
        "author": "Dr. Elena Vasquez",
        "subject": "Confidential Clinical Trial Results",
        "keywords": "ARX-7742, Phase III, TR-MDD, clinical trial, confidential",
        "creator": "NovaCrest Pharmaceuticals",
        "producer": "PyMuPDF",
    })

    # --- Set Table of Contents ---
    toc = [
        [1, "Executive Summary", 3],
        [1, "Study Design and Methodology", 4],
        [1, "Patient Demographics and Baseline Characteristics", 5],
        [1, "Primary Efficacy Endpoints", 6],
        [1, "Secondary Efficacy Endpoints", 7],
        [1, "Biomarker Analysis", 8],
        [1, "Safety and Adverse Events", 9],
        [1, "Pharmacokinetic Data", 10],
        [1, "Subgroup Analyses", 11],
        [1, "Statistical Methodology", 12],
        [1, "Regulatory Implications", 13],
        [1, "Competitive Landscape Analysis", 14],
        [1, "Conclusions and Recommendations", 15],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
