"""
Initial Setup: Create a 12-page neuroimaging study PDF with abstract on page 1.
Task ID: pdf_fm_045
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_045'
DOC_DIR = f'{WORKDIR}/Documents/research'
OUTPUT = f'{DOC_DIR}/neuroimaging_study.pdf'


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

    # Page dimensions (Letter size)
    W, H = 612, 792
    LEFT = 72
    RIGHT = W - 72
    TEXT_WIDTH = RIGHT - LEFT

    # ── Utility functions ──

    def add_header_footer(page, page_num, total):
        """Add consistent header/footer to each page."""
        # Header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(LEFT, 50), pymupdf.Point(RIGHT, 50))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape.commit()
        page.insert_text(pymupdf.Point(LEFT, 45), "NeuroImage Clinical  |  Volume 38, 2024",
                         fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
        # Footer
        page.insert_text(pymupdf.Point(W / 2 - 5, H - 30), str(page_num),
                         fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    def insert_wrapped(page, x, y, text, fontsize=10, fontname="helv",
                       color=(0, 0, 0), max_width=None, line_height=None, align=0):
        """Insert text in a textbox and return the y position after the text."""
        if max_width is None:
            max_width = TEXT_WIDTH
        if line_height is None:
            line_height = fontsize * 1.5
        # Estimate height needed (generous)
        est_chars_per_line = max(1, int(max_width / (fontsize * 0.5)))
        est_lines = len(text) / est_chars_per_line + 2
        est_height = est_lines * line_height + 20
        rect = pymupdf.Rect(x, y, x + max_width, y + est_height)
        rc = page.insert_textbox(rect, text, fontsize=fontsize, fontname=fontname,
                                 color=color, align=align)
        # Calculate actual used height
        used_height = est_height - abs(rc) if rc < 0 else est_height
        return y + used_height

    # ================================================================
    # PAGE 1 — Title, Authors, Abstract
    # ================================================================
    p1 = doc.new_page(width=W, height=H)
    add_header_footer(p1, 1, 12)

    y = 80
    # Title
    title = "Functional Connectivity Alterations in Default Mode Network During Cognitive Load: A Multi-Site fMRI Study"
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 60)
    p1.insert_textbox(rect, title, fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.3), align=1)
    y += 70

    # Authors
    authors = "Elena Rodriguez-Martinez¹, David K. Chen², Priya Subramanian³, Thomas J. Blackwell¹, Sarah Kimura², Alexandre Fontaine-Duval⁴"
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 30)
    p1.insert_textbox(rect, authors, fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2), align=1)
    y += 35

    # Affiliations
    affiliations = (
        "¹ Department of Neuroscience, Stanford University School of Medicine, Stanford, CA\n"
        "² Montreal Neurological Institute, McGill University, Montreal, QC, Canada\n"
        "³ Centre for Brain and Cognitive Development, University College London, UK\n"
        "⁴ INSERM U1127, Institut du Cerveau, Sorbonne Université, Paris, France"
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 55)
    p1.insert_textbox(rect, affiliations, fontsize=7.5, fontname="heit", color=(0.4, 0.4, 0.4), align=1)
    y += 65

    # Separator line
    shape = p1.new_shape()
    shape.draw_line(pymupdf.Point(LEFT, y), pymupdf.Point(RIGHT, y))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.8)
    shape.commit()
    y += 15

    # Abstract heading
    p1.insert_text(pymupdf.Point(LEFT, y), "Abstract", fontsize=12, fontname="hebo", color=(0.1, 0.1, 0.3))
    y += 18

    abstract_text = (
        "Background: The default mode network (DMN) plays a critical role in self-referential processing and "
        "mind-wandering, yet its behavior under varying cognitive demands remains poorly characterized across "
        "diverse populations. This multi-site study examines DMN functional connectivity patterns during graded "
        "cognitive load paradigms in a large, demographically representative sample.\n\n"
        "Methods: We acquired resting-state and task-based fMRI data from 847 healthy adults (ages 22-68, "
        "412 female) across four international imaging centers using harmonized acquisition protocols on 3T "
        "Siemens Prisma scanners. Participants completed an adaptive n-back working memory task with four "
        "difficulty levels (0-back through 3-back). Functional connectivity was assessed using seed-based "
        "correlation analysis with posterior cingulate cortex (PCC) as the primary seed region.\n\n"
        "Results: DMN connectivity demonstrated a significant linear decrease with increasing cognitive load "
        "(F(3,843) = 47.2, p < 0.001, η² = 0.144). The strongest suppression was observed in the medial "
        "prefrontal cortex (mPFC) during 3-back conditions (mean z = -0.31, SD = 0.12). Age moderated the "
        "load-connectivity relationship (β = -0.18, p = 0.003), with older participants showing less DMN "
        "suppression at higher loads.\n\n"
        "Conclusions: These findings establish normative DMN suppression curves under cognitive load and "
        "highlight age-related differences in network dynamics that may have implications for understanding "
        "cognitive decline in aging populations."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 280)
    p1.insert_textbox(rect, abstract_text, fontsize=9.5, fontname="helv", color=(0, 0, 0), align=3)
    y += 290

    # Keywords
    p1.insert_text(pymupdf.Point(LEFT, y), "Keywords: ", fontsize=9, fontname="hebo", color=(0, 0, 0))
    p1.insert_text(pymupdf.Point(LEFT + 55, y), "default mode network; functional connectivity; fMRI; cognitive load; working memory; aging",
                   fontsize=9, fontname="heit", color=(0.2, 0.2, 0.2))

    # ================================================================
    # PAGE 2 — Introduction
    # ================================================================
    p2 = doc.new_page(width=W, height=H)
    add_header_footer(p2, 2, 12)
    y = 70
    p2.insert_text(pymupdf.Point(LEFT, y), "1. Introduction", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    y += 22

    intro_text = (
        "The default mode network (DMN) has emerged as one of the most extensively studied large-scale brain "
        "networks since its initial characterization by Raichle and colleagues (2001). Comprising the medial "
        "prefrontal cortex (mPFC), posterior cingulate cortex (PCC), precuneus, lateral temporal cortices, and "
        "angular gyri, the DMN exhibits a distinctive pattern of activation during rest and deactivation during "
        "externally directed cognitive tasks (Buckner et al., 2008; Andrews-Hanna et al., 2014).\n\n"
        "A substantial body of evidence suggests that DMN activity is inversely related to task difficulty, "
        "with greater cognitive demands producing more pronounced network suppression (McKiernan et al., 2003). "
        "This suppression is thought to reflect the reallocation of neural resources from internal mentation to "
        "task-relevant processing. However, the precise dynamics of this suppression—particularly across graded "
        "levels of cognitive demand—remain incompletely understood.\n\n"
        "Several factors may modulate the relationship between cognitive load and DMN dynamics. Age has been "
        "identified as a key variable, with older adults showing reduced DMN suppression during demanding tasks "
        "(Lustig et al., 2003; Grady et al., 2010). This age-related deficit in DMN modulation has been linked "
        "to poorer task performance and may represent an early biomarker of cognitive decline (Sperling et al., "
        "2009). However, most studies examining age effects have used limited sample sizes and single-site designs, "
        "restricting generalizability.\n\n"
        "The present study addresses these limitations through a large-scale, multi-site investigation of DMN "
        "functional connectivity during a parametric working memory paradigm. We hypothesized that: (1) DMN "
        "connectivity would show a monotonic decrease across increasing cognitive load levels; (2) age would "
        "moderate this relationship, with older adults showing reduced DMN suppression; and (3) individual "
        "differences in DMN suppression would predict behavioral performance on the working memory task.\n\n"
        "By leveraging harmonized acquisition protocols across four international imaging centers, this study "
        "provides a robust framework for establishing normative patterns of DMN behavior under cognitive demand, "
        "which may serve as a foundation for clinical applications in neurodegenerative disease research."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    p2.insert_textbox(rect, intro_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)

    # ================================================================
    # PAGE 3 — Methods (part 1)
    # ================================================================
    p3 = doc.new_page(width=W, height=H)
    add_header_footer(p3, 3, 12)
    y = 70
    p3.insert_text(pymupdf.Point(LEFT, y), "2. Methods", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    y += 22
    p3.insert_text(pymupdf.Point(LEFT, y), "2.1 Participants", fontsize=11, fontname="hebo", color=(0.15, 0.15, 0.35))
    y += 18

    methods_p1 = (
        "A total of 847 healthy adults were recruited across four imaging centers: Stanford University (n = 234), "
        "McGill University (n = 218), University College London (n = 201), and Sorbonne Université (n = 194). "
        "Participants ranged in age from 22 to 68 years (M = 41.3, SD = 12.7; 412 female, 435 male). All "
        "participants were right-handed, had normal or corrected-to-normal vision, and reported no history of "
        "neurological or psychiatric disorders.\n\n"
        "Exclusion criteria included: (1) MRI contraindications; (2) current psychotropic medication use; "
        "(3) history of head injury with loss of consciousness exceeding 5 minutes; (4) substance use disorder "
        "within the past 12 months; and (5) excessive head motion during scanning (> 0.5 mm framewise "
        "displacement in more than 20% of volumes). Following quality control, 23 participants were excluded, "
        "yielding a final sample of 824 participants.\n\n"
        "The study was approved by the institutional review boards at all participating sites and conducted in "
        "accordance with the Declaration of Helsinki. All participants provided written informed consent."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 220)
    p3.insert_textbox(rect, methods_p1, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)
    y += 230

    p3.insert_text(pymupdf.Point(LEFT, y), "2.2 MRI Acquisition", fontsize=11, fontname="hebo", color=(0.15, 0.15, 0.35))
    y += 18

    methods_mri = (
        "All imaging data were acquired on 3T Siemens Prisma MRI systems equipped with 64-channel head coils. "
        "A harmonized multi-site protocol was implemented following the recommendations of the ENIGMA consortium "
        "(Thompson et al., 2020). Structural images were acquired using a T1-weighted MPRAGE sequence (TR = 2300 ms, "
        "TE = 2.32 ms, TI = 900 ms, flip angle = 8°, voxel size = 1.0 × 1.0 × 1.0 mm³). Functional images "
        "employed a multi-band EPI sequence (TR = 800 ms, TE = 37 ms, flip angle = 52°, multi-band factor = 8, "
        "voxel size = 2.0 × 2.0 × 2.0 mm³). Each functional run lasted approximately 12 minutes."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    p3.insert_textbox(rect, methods_mri, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)

    # ================================================================
    # PAGE 4 — Methods (part 2)
    # ================================================================
    p4 = doc.new_page(width=W, height=H)
    add_header_footer(p4, 4, 12)
    y = 70
    p4.insert_text(pymupdf.Point(LEFT, y), "2.3 Cognitive Task Paradigm", fontsize=11, fontname="hebo", color=(0.15, 0.15, 0.35))
    y += 18

    task_text = (
        "Participants completed an adaptive visual n-back working memory task with four difficulty levels "
        "(0-back, 1-back, 2-back, and 3-back). Stimuli consisted of single uppercase letters presented "
        "centrally on a gray background for 500 ms with an inter-stimulus interval of 2000 ms. Each block "
        "contained 20 stimuli with 6 targets (30% target rate). Four blocks per condition were presented in "
        "a pseudorandomized order with 16-second rest periods between blocks.\n\n"
        "In the 0-back condition, participants identified a pre-specified target letter. In 1-back through 3-back "
        "conditions, participants indicated whether the current stimulus matched the stimulus presented 1, 2, or 3 "
        "positions earlier, respectively. Responses were collected via a fiber-optic button box. Reaction times "
        "and accuracy were recorded for all trials."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 200)
    p4.insert_textbox(rect, task_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)
    y += 210

    p4.insert_text(pymupdf.Point(LEFT, y), "2.4 fMRI Preprocessing", fontsize=11, fontname="hebo", color=(0.15, 0.15, 0.35))
    y += 18

    preproc_text = (
        "Functional images were preprocessed using fMRIPrep version 23.1.0 (Esteban et al., 2019), which "
        "implements a standardized pipeline including motion correction, slice timing correction, spatial "
        "normalization to MNI152NLin2009cAsym template space, and surface-based registration. Confound regression "
        "included 24 motion parameters (6 rigid-body parameters, their temporal derivatives, and quadratic terms), "
        "mean white matter and cerebrospinal fluid signals, and high-pass filtering at 0.008 Hz.\n\n"
        "Multi-site harmonization was performed using ComBat (Johnson et al., 2007) with site as the batch "
        "variable and age, sex, and education as biological covariates. Quality control metrics were computed "
        "using MRIQC (Esteban et al., 2017), and images failing visual inspection or automated quality "
        "thresholds were excluded from analysis."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    p4.insert_textbox(rect, preproc_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)

    # ================================================================
    # PAGE 5 — Methods (part 3) + Results heading
    # ================================================================
    p5 = doc.new_page(width=W, height=H)
    add_header_footer(p5, 5, 12)
    y = 70
    p5.insert_text(pymupdf.Point(LEFT, y), "2.5 Statistical Analysis", fontsize=11, fontname="hebo", color=(0.15, 0.15, 0.35))
    y += 18

    stats_text = (
        "Seed-based functional connectivity analysis was conducted using the CONN toolbox v22 (Whitfield-Gabrieli "
        "& Nieto-Castanon, 2012). The posterior cingulate cortex (PCC; MNI: 0, -52, 26; 6mm sphere) served as "
        "the primary seed region based on its role as a central hub of the DMN (Leech & Sharp, 2014). Fisher "
        "z-transformed correlation maps were generated for each condition and participant.\n\n"
        "Linear mixed-effects models were used to examine the effects of cognitive load (0-back through 3-back, "
        "treated as a continuous variable) on PCC connectivity with other DMN nodes. Random intercepts and slopes "
        "for load were included at the participant level, with site as an additional random intercept. Age, sex, "
        "and years of education were included as fixed-effect covariates. Load × age interaction terms were "
        "tested to examine age moderation effects. Multiple comparisons correction was applied using the "
        "Benjamini-Hochberg false discovery rate (FDR) procedure at q < 0.05."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 240)
    p5.insert_textbox(rect, stats_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)
    y += 260

    p5.insert_text(pymupdf.Point(LEFT, y), "3. Results", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    y += 22
    p5.insert_text(pymupdf.Point(LEFT, y), "3.1 Behavioral Performance", fontsize=11, fontname="hebo", color=(0.15, 0.15, 0.35))
    y += 18

    behav_text = (
        "Task accuracy decreased monotonically with increasing cognitive load (0-back: M = 97.2%, SD = 2.8%; "
        "1-back: M = 94.1%, SD = 4.2%; 2-back: M = 86.7%, SD = 8.3%; 3-back: M = 73.4%, SD = 12.1%). A repeated "
        "measures ANOVA confirmed a significant main effect of load on accuracy (F(3,2469) = 312.8, p < 0.001, "
        "η² = 0.275). Reaction times showed the opposite pattern, increasing with load (0-back: M = 423 ms; "
        "1-back: M = 487 ms; 2-back: M = 561 ms; 3-back: M = 634 ms; F(3,2469) = 198.4, p < 0.001)."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    p5.insert_textbox(rect, behav_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)

    # ================================================================
    # PAGE 6 — Results (connectivity)
    # ================================================================
    p6 = doc.new_page(width=W, height=H)
    add_header_footer(p6, 6, 12)
    y = 70
    p6.insert_text(pymupdf.Point(LEFT, y), "3.2 DMN Functional Connectivity Under Cognitive Load",
                   fontsize=11, fontname="hebo", color=(0.15, 0.15, 0.35))
    y += 18

    conn_text = (
        "PCC connectivity with core DMN regions showed a significant linear decrease across cognitive load levels "
        "(Table 1). The most pronounced suppression was observed in the medial prefrontal cortex (mPFC), where "
        "mean Fisher z-transformed connectivity decreased from 0.42 (SD = 0.14) at rest to -0.31 (SD = 0.12) "
        "during 3-back conditions (t(823) = -28.4, p < 0.001, Cohen's d = -1.98).\n\n"
        "The angular gyrus showed a similar pattern of load-dependent suppression, though the magnitude was "
        "somewhat smaller (rest: z = 0.38, SD = 0.11; 3-back: z = -0.18, SD = 0.15; t(823) = -21.7, p < 0.001). "
        "Lateral temporal cortex connectivity was also significantly modulated by load, though the effect was "
        "restricted to the 2-back and 3-back conditions.\n\n"
        "Whole-brain analysis revealed that reduced DMN connectivity was accompanied by increased connectivity "
        "between PCC and task-positive regions, including dorsolateral prefrontal cortex (DLPFC) and anterior "
        "insula, during higher load conditions. This anti-correlation pattern was strongest during 3-back "
        "(PCC-DLPFC: z = 0.19, SD = 0.13; PCC-anterior insula: z = 0.15, SD = 0.11)."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    p6.insert_textbox(rect, conn_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)

    # ================================================================
    # PAGE 7 — Table 1
    # ================================================================
    p7 = doc.new_page(width=W, height=H)
    add_header_footer(p7, 7, 12)
    y = 70
    p7.insert_text(pymupdf.Point(LEFT, y), "Table 1. PCC Functional Connectivity with DMN Regions Across Load Conditions",
                   fontsize=10, fontname="hebo", color=(0.1, 0.1, 0.3))
    y += 25

    # Draw table
    shape = p7.new_shape()
    col_widths = [130, 80, 80, 80, 80]
    total_w = sum(col_widths)
    x_start = LEFT
    rows_data = [
        ["Region", "Rest", "1-back", "2-back", "3-back"],
        ["mPFC", "0.42 (0.14)", "-0.08 (0.13)", "-0.21 (0.11)", "-0.31 (0.12)"],
        ["Angular Gyrus", "0.38 (0.11)", "-0.02 (0.12)", "-0.12 (0.13)", "-0.18 (0.15)"],
        ["Lateral Temporal", "0.29 (0.10)", "0.14 (0.11)", "-0.05 (0.10)", "-0.11 (0.12)"],
        ["Precuneus", "0.51 (0.13)", "0.32 (0.14)", "0.18 (0.12)", "0.08 (0.14)"],
        ["Hippocampus", "0.22 (0.09)", "0.11 (0.10)", "-0.03 (0.08)", "-0.09 (0.11)"],
    ]
    row_h = 22
    for r, row in enumerate(rows_data):
        x = x_start
        for c, val in enumerate(row):
            rect = pymupdf.Rect(x, y, x + col_widths[c], y + row_h)
            if r == 0:
                shape.draw_rect(rect)
                shape.finish(color=(0.5, 0.5, 0.5), fill=(0.85, 0.85, 0.95), width=0.5)
                p7.insert_textbox(rect, val, fontsize=9, fontname="hebo", color=(0, 0, 0), align=1)
            else:
                shape.draw_rect(rect)
                fill = (0.95, 0.95, 0.95) if r % 2 == 0 else (1, 1, 1)
                shape.finish(color=(0.7, 0.7, 0.7), fill=fill, width=0.3)
                p7.insert_textbox(rect, val, fontsize=9, fontname="helv", color=(0, 0, 0), align=1)
            x += col_widths[c]
        y += row_h
    shape.commit()

    y += 15
    p7.insert_text(pymupdf.Point(LEFT, y),
                   "Note. Values are mean Fisher z-transformed correlations (SD). All load effects significant at p < 0.001 (FDR-corrected).",
                   fontsize=8, fontname="heit", color=(0.3, 0.3, 0.3))

    # ================================================================
    # PAGE 8 — Age moderation results
    # ================================================================
    p8 = doc.new_page(width=W, height=H)
    add_header_footer(p8, 8, 12)
    y = 70
    p8.insert_text(pymupdf.Point(LEFT, y), "3.3 Age Moderation Effects", fontsize=11, fontname="hebo", color=(0.15, 0.15, 0.35))
    y += 18

    age_text = (
        "The interaction between cognitive load and age on DMN connectivity was significant for the PCC-mPFC "
        "pathway (β = -0.18, SE = 0.06, p = 0.003) and PCC-angular gyrus pathway (β = -0.14, SE = 0.05, p = 0.008). "
        "Older participants (age > 55) demonstrated attenuated DMN suppression during high-load conditions "
        "compared to younger adults (age < 35), with the largest difference observed during 3-back performance "
        "(mean difference in PCC-mPFC z = 0.15, 95% CI [0.08, 0.22]).\n\n"
        "Post-hoc analyses stratifying by age tertiles revealed that the youngest group (22-36 years, n = 278) "
        "showed the steepest load-connectivity slope (β = -0.14 per load level), while the oldest group "
        "(52-68 years, n = 271) showed a significantly shallower slope (β = -0.08 per load level; difference "
        "test: z = 3.42, p < 0.001).\n\n"
        "Sex did not significantly moderate the load-connectivity relationship in any DMN pathway after "
        "correction for multiple comparisons (all p > 0.12). Similarly, education level showed no significant "
        "moderation effects (all p > 0.25)."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 280)
    p8.insert_textbox(rect, age_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)
    y += 290

    p8.insert_text(pymupdf.Point(LEFT, y), "3.4 Brain-Behavior Relationships", fontsize=11, fontname="hebo", color=(0.15, 0.15, 0.35))
    y += 18

    brain_behav = (
        "Greater DMN suppression during 3-back was associated with higher task accuracy (r = -0.28, p < 0.001) "
        "and faster reaction times (r = 0.22, p < 0.001). Mediation analysis indicated that age-related "
        "differences in 3-back accuracy were partially mediated by individual differences in PCC-mPFC "
        "suppression (indirect effect: β = -0.07, 95% CI [-0.11, -0.03], proportion mediated = 23.4%)."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    p8.insert_textbox(rect, brain_behav, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)

    # ================================================================
    # PAGE 9 — Discussion (part 1)
    # ================================================================
    p9 = doc.new_page(width=W, height=H)
    add_header_footer(p9, 9, 12)
    y = 70
    p9.insert_text(pymupdf.Point(LEFT, y), "4. Discussion", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    y += 22

    disc_text = (
        "This multi-site study provides the most comprehensive characterization to date of DMN functional "
        "connectivity dynamics under graded cognitive load. Our findings confirm and extend previous work by "
        "demonstrating a robust, monotonic suppression of DMN connectivity as working memory demands increase, "
        "and by quantifying age-related differences in this fundamental neural mechanism.\n\n"
        "The parametric design of our cognitive task revealed that DMN suppression follows a near-linear "
        "trajectory across load levels, rather than showing threshold effects. This suggests that the DMN "
        "operates on a continuous spectrum of activation, with suppression magnitude reflecting a graded "
        "reallocation of neural resources from internal to external processing. The strongest effects were "
        "observed in the PCC-mPFC pathway, consistent with this pathway's proposed role as the core axis "
        "of the DMN (Andrews-Hanna et al., 2010).\n\n"
        "Our finding of age-related attenuation in DMN suppression aligns with the dedifferentiation hypothesis "
        "of cognitive aging (Park et al., 2004), which posits that neural representations become less distinct "
        "with age. Older adults showed less efficient suppression of task-irrelevant DMN activity, particularly "
        "at higher load levels. This reduced suppression partially mediated age-related declines in working "
        "memory accuracy, suggesting a functional consequence of this neural inefficiency.\n\n"
        "The multi-site nature of our study represents a significant strength, as it enhances generalizability "
        "and statistical power while allowing us to demonstrate that DMN suppression patterns are robust across "
        "different scanner environments and cultural contexts. The use of harmonized acquisition protocols and "
        "ComBat harmonization for statistical analysis effectively controlled for inter-site variability."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    p9.insert_textbox(rect, disc_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)

    # ================================================================
    # PAGE 10 — Discussion (part 2) + Limitations
    # ================================================================
    p10 = doc.new_page(width=W, height=H)
    add_header_footer(p10, 10, 12)
    y = 70
    p10.insert_text(pymupdf.Point(LEFT, y), "4.1 Limitations and Future Directions", fontsize=11, fontname="hebo", color=(0.15, 0.15, 0.35))
    y += 18

    lim_text = (
        "Several limitations should be considered when interpreting these results. First, our cross-sectional "
        "design precludes causal inferences about the relationship between age and DMN dynamics. Longitudinal "
        "studies tracking within-individual changes are needed to determine whether reduced DMN suppression "
        "represents a developmental trajectory or cohort effect.\n\n"
        "Second, while the n-back paradigm is well-validated, it engages multiple cognitive processes beyond "
        "working memory, including attention, monitoring, and updating. Future studies using tasks that more "
        "selectively target specific cognitive components could provide greater specificity in linking DMN "
        "dynamics to particular cognitive functions.\n\n"
        "Third, our reliance on seed-based connectivity analysis, while facilitating interpretation, may miss "
        "more complex patterns of DMN reorganization that would be captured by data-driven approaches such as "
        "independent component analysis or dynamic functional connectivity methods.\n\n"
        "Future directions include examining DMN dynamics in clinical populations with known network "
        "disruptions (e.g., Alzheimer's disease, major depressive disorder) to determine whether the normative "
        "suppression curves established here can serve as sensitive biomarkers of pathological deviation."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    p10.insert_textbox(rect, lim_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)

    # ================================================================
    # PAGE 11 — Conclusions + Acknowledgments
    # ================================================================
    p11 = doc.new_page(width=W, height=H)
    add_header_footer(p11, 11, 12)
    y = 70
    p11.insert_text(pymupdf.Point(LEFT, y), "5. Conclusions", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    y += 22

    concl_text = (
        "This study establishes normative patterns of DMN functional connectivity under parametric cognitive "
        "load in a large, multi-site sample. Our findings demonstrate that DMN suppression is a robust, "
        "graded phenomenon that scales with cognitive demand and is modulated by age. The brain-behavior "
        "relationships identified here highlight the functional significance of efficient DMN regulation for "
        "cognitive performance and suggest potential targets for interventions aimed at preserving cognitive "
        "function in aging populations."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 120)
    p11.insert_textbox(rect, concl_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)
    y += 140

    p11.insert_text(pymupdf.Point(LEFT, y), "Acknowledgments", fontsize=12, fontname="hebo", color=(0.1, 0.1, 0.3))
    y += 18
    ack_text = (
        "This work was supported by grants from the National Institutes of Health (R01-AG058628, R01-MH112847), "
        "the Canadian Institutes of Health Research (FDN-154292), the UK Medical Research Council (MR/S004831/1), "
        "and the French National Research Agency (ANR-19-CE37-0002). The authors thank all participants and the "
        "research coordinators at each site for their contributions to this study."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 80)
    p11.insert_textbox(rect, ack_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)
    y += 100

    p11.insert_text(pymupdf.Point(LEFT, y), "Data Availability Statement", fontsize=11, fontname="hebo", color=(0.15, 0.15, 0.35))
    y += 18
    data_text = (
        "De-identified neuroimaging data and analysis code are available through the OpenNeuro repository "
        "(doi: 10.18112/openneuro.ds004521). Group-level statistical maps are available on NeuroVault "
        "(collection ID: 14832). Custom analysis scripts are available at https://github.com/rodriguez-lab/dmn-cogload."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 60)
    p11.insert_textbox(rect, data_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=3)

    # ================================================================
    # PAGE 12 — References
    # ================================================================
    p12 = doc.new_page(width=W, height=H)
    add_header_footer(p12, 12, 12)
    y = 70
    p12.insert_text(pymupdf.Point(LEFT, y), "References", fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    y += 22

    refs = [
        "Andrews-Hanna, J. R., Reidler, J. S., Sepulcre, J., Poulin, R., & Buckner, R. L. (2010). Functional-anatomic fractionation of the brain's default network. Neuron, 65(4), 550-562.",
        "Andrews-Hanna, J. R., Smallwood, J., & Spreng, R. N. (2014). The default network and self-generated thought: Component processes, dynamic control, and clinical relevance. Annals of the New York Academy of Sciences, 1316(1), 29-52.",
        "Buckner, R. L., Andrews-Hanna, J. R., & Schacter, D. L. (2008). The brain's default network: Anatomy, function, and relevance to disease. Annals of the New York Academy of Sciences, 1124(1), 1-38.",
        "Esteban, O., Markiewicz, C. J., Blair, R. W., et al. (2019). fMRIPrep: A robust preprocessing pipeline for functional MRI. Nature Methods, 16(1), 111-116.",
        "Grady, C. L., Springer, M. V., Hongwanishkul, D., McIntosh, A. R., & Winocur, G. (2010). Age-related changes in brain activity across the adult lifespan. Journal of Cognitive Neuroscience, 18(2), 227-241.",
        "Johnson, W. E., Li, C., & Rabinovic, A. (2007). Adjusting batch effects in microarray expression data using empirical Bayes methods. Biostatistics, 8(1), 118-127.",
        "Leech, R., & Sharp, D. J. (2014). The role of the posterior cingulate cortex in cognition and disease. Brain, 137(1), 12-32.",
        "Lustig, C., Snyder, A. Z., Bhakta, M., O'Brien, K. C., McAvoy, M., Raichle, M. E., ... & Buckner, R. L. (2003). Functional deactivations: Change with age and dementia of the Alzheimer type. PNAS, 100(24), 14504-14509.",
        "McKiernan, K. A., Kaufman, J. N., Kucera-Thompson, J., & Binder, J. R. (2003). A parametric manipulation of factors affecting task-induced deactivation in functional neuroimaging. Journal of Cognitive Neuroscience, 15(3), 394-408.",
        "Park, D. C., Polk, T. A., Park, R., Minear, M., Savage, A., & Smith, M. R. (2004). Aging reduces neural specialization in ventral visual cortex. PNAS, 101(35), 13091-13095.",
        "Raichle, M. E., MacLeod, A. M., Snyder, A. Z., Powers, W. J., Gusnard, D. A., & Shulman, G. L. (2001). A default mode of brain function. PNAS, 98(2), 676-682.",
        "Sperling, R. A., Laviolette, P. S., O'Keefe, K., et al. (2009). Amyloid deposition is associated with impaired default network function in older persons without dementia. Neuron, 63(2), 178-188.",
        "Thompson, P. M., Jahanshad, N., Ching, C. R., et al. (2020). ENIGMA and global neuroscience: A decade of large-scale studies of the brain in health and disease across more than 40 countries. Translational Psychiatry, 10(1), 100.",
        "Whitfield-Gabrieli, S., & Nieto-Castanon, A. (2012). Conn: A functional connectivity toolbox for correlated and anticorrelated brain networks. Brain Connectivity, 2(3), 125-141.",
    ]
    for ref in refs:
        rect = pymupdf.Rect(LEFT, y, RIGHT, y + 36)
        rc = p12.insert_textbox(rect, ref, fontsize=8.5, fontname="helv", color=(0, 0, 0), align=3)
        y += 36
        if y > H - 60:
            break

    # ── Set metadata ──
    doc.set_metadata({
        "title": "Functional Connectivity Alterations in Default Mode Network During Cognitive Load",
        "author": "Rodriguez-Martinez E, Chen DK, Subramanian P, Blackwell TJ, Kimura S, Fontaine-Duval A",
        "subject": "Neuroimaging, fMRI, Default Mode Network",
        "keywords": "DMN, fMRI, cognitive load, working memory, aging, functional connectivity",
        "creator": "NeuroImage Clinical",
    })

    # ── Set table of contents ──
    toc = [
        [1, "Abstract", 1],
        [1, "1. Introduction", 2],
        [1, "2. Methods", 3],
        [2, "2.1 Participants", 3],
        [2, "2.2 MRI Acquisition", 3],
        [2, "2.3 Cognitive Task Paradigm", 4],
        [2, "2.4 fMRI Preprocessing", 4],
        [2, "2.5 Statistical Analysis", 5],
        [1, "3. Results", 5],
        [2, "3.1 Behavioral Performance", 5],
        [2, "3.2 DMN Functional Connectivity Under Cognitive Load", 6],
        [2, "3.3 Age Moderation Effects", 8],
        [2, "3.4 Brain-Behavior Relationships", 8],
        [1, "4. Discussion", 9],
        [2, "4.1 Limitations and Future Directions", 10],
        [1, "5. Conclusions", 11],
        [1, "References", 12],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
