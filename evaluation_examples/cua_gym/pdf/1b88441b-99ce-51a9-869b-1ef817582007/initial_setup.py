"""
Initial Setup: Create thesis.pdf (60-page academic thesis) and scripts directory
Task ID: pdf_cross_107
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import math

WORKDIR = '/home/user'
TASK_ID = 'pdf_cross_107'
DOCS_DIR = f'{WORKDIR}/Documents'
SCRIPTS_DIR = f'{WORKDIR}/scripts'
THESIS_PDF = f'{DOCS_DIR}/thesis.pdf'


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
    import pymupdf

    # Ensure directories exist
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # Remove old files if exist
    if os.path.exists(THESIS_PDF):
        os.remove(THESIS_PDF)
    stats_file = f'{DOCS_DIR}/thesis_stats.txt'
    if os.path.exists(stats_file):
        os.remove(stats_file)
    script_file = f'{SCRIPTS_DIR}/pdf_stats.py'
    if os.path.exists(script_file):
        os.remove(script_file)

    doc = pymupdf.open()

    # ============================================================
    # THESIS CONTENT — 60 pages of a realistic academic thesis
    # Title: "Machine Learning Approaches to Climate Change Prediction"
    # Author: Dr. Emily Chen, Department of Computer Science
    # ============================================================

    # Chapter structure
    chapters = [
        # (chapter_title, num_pages, page_start_idx)
        ("Abstract", 1, 0),
        ("Chapter 1: Introduction", 6, 1),
        ("Chapter 2: Literature Review", 9, 7),
        ("Chapter 3: Methodology", 10, 16),
        ("Chapter 4: Experimental Results", 12, 26),
        ("Chapter 5: Discussion", 8, 38),
        ("Chapter 6: Conclusion", 5, 46),
        ("References", 7, 51),
        ("Appendix A: Data Sources", 3, 58),
        ("Appendix B: Code Listings", 2, 61),
    ]

    # Some paragraph-level content keyed by chapter
    chapter_contents = {
        "Abstract": [
            "This thesis investigates the application of advanced machine learning "
            "techniques to the challenging domain of climate change prediction. We "
            "present a comprehensive study of convolutional neural networks, recurrent "
            "architectures, and ensemble methods applied to long-range atmospheric "
            "forecasting tasks.",
            "Our primary contributions include: (1) a novel multi-scale temporal "
            "fusion network (MSTFN) that outperforms existing LSTM-based baselines by "
            "an average of 12.3% on RMSE across six benchmark datasets; (2) an "
            "interpretability framework based on gradient-weighted class activation "
            "mapping adapted for spatiotemporal data; and (3) a curated, open-source "
            "dataset aggregating 40 years of ERA5 reanalysis data with quality "
            "control annotations.",
            "Experiments conducted across multiple climate zones demonstrate that "
            "MSTFN achieves state-of-the-art results on temperature anomaly prediction "
            "for 3-, 6-, and 12-month forecast horizons. Statistical significance "
            "testing (p < 0.001) confirms the improvements are robust. The framework "
            "is released as open-source software to facilitate reproducibility and "
            "community adoption.",
        ],
        "Introduction": [
            "Climate change represents one of the most pressing scientific and "
            "societal challenges of the 21st century. Accurate long-range forecasting "
            "of atmospheric variables is critical for agriculture, energy planning, "
            "disaster preparedness, and policy formulation. Traditional numerical "
            "weather prediction (NWP) models, while physically grounded, face "
            "computational constraints that limit their applicability at decadal "
            "forecast horizons.",
            "Machine learning (ML) methods have emerged as promising complements to "
            "NWP, offering data-driven pattern recognition capabilities that scale "
            "efficiently with the proliferation of earth observation datasets. Recent "
            "successes in deep learning—particularly in image recognition and natural "
            "language processing—have inspired researchers to adapt these architectures "
            "for geospatial and temporal climate data.",
            "This thesis is organized as follows: Chapter 2 surveys the existing "
            "literature on machine learning for climate modeling. Chapter 3 describes "
            "the proposed methodology, including data preprocessing pipelines, model "
            "architectures, and training procedures. Chapter 4 presents quantitative "
            "experimental results and ablation studies. Chapter 5 discusses "
            "implications, limitations, and directions for future work. Chapter 6 "
            "concludes the thesis.",
            "The overarching hypothesis driving this research is that hierarchical "
            "feature extraction over multiple temporal scales can capture both "
            "short-range synoptic patterns and long-range teleconnections that are "
            "physically relevant to climate forecasting. We test this hypothesis "
            "through controlled ablation experiments and comparison against state-of-the-art baselines.",
            "Our work draws on datasets from NOAA, NASA, and the European Centre for "
            "Medium-Range Weather Forecasts (ECMWF). The training infrastructure relies "
            "on distributed GPU clusters with a total of 128 NVIDIA A100 GPUs, "
            "enabling experiments at planetary scales that were previously infeasible.",
            "Throughout this document, we use the following notation conventions: "
            "bold lowercase letters denote vectors, bold uppercase letters denote "
            "matrices, and calligraphic letters denote sets or spaces. "
            "The symbol T denotes transpose, and || · || denotes the L2 norm unless "
            "otherwise specified.",
        ],
        "Literature Review": [
            "The field of machine learning for weather and climate prediction has grown "
            "substantially over the past decade. Scher and Messori (2019) demonstrated "
            "that simple feedforward networks trained on reanalysis data could produce "
            "skillful multi-day predictions. Weyn et al. (2020) extended this work "
            "using a cubed-sphere convolutional architecture, achieving competitive "
            "performance against operational models for two-week forecasts.",
            "Long short-term memory (LSTM) networks have been widely adopted for "
            "sequential climate data. Salman et al. (2015) applied LSTMs to monthly "
            "temperature and precipitation forecasting in Southeast Asia. Shi et al. "
            "(2015) introduced the ConvLSTM architecture, combining spatial and temporal "
            "modeling, and demonstrated superior performance on radar echo extrapolation "
            "tasks compared to fully connected LSTMs.",
            "Attention mechanisms and Transformer architectures have begun to influence "
            "climate modeling. Pathak et al. (2022) presented FourCastNet, a Fourier "
            "neural operator framework that produces accurate 10-day forecasts with "
            "orders-of-magnitude speedup over NWP. Bi et al. (2023) introduced Pangu-Weather, "
            "a 3D transformer trained on 39 years of ERA5 data.",
            "Graph neural networks have been applied to climate modeling by Keisler "
            "(2022) and Lam et al. (2023). The latter's GraphCast model achieved "
            "state-of-the-art medium-range forecasting, surpassing ECMWF HRES in 90% "
            "of test variables and forecast lead times. These results underscore the "
            "potential of data-driven approaches.",
            "Despite these advances, several challenges remain: (1) accurate long-range "
            "forecasts beyond two weeks remain elusive; (2) most models lack physical "
            "interpretability; (3) uncertainty quantification is rarely addressed; "
            "(4) transfer learning across climate regimes is poorly understood.",
            "Our work addresses challenges (1) and (2) by proposing the MSTFN "
            "architecture with integrated attention visualization, and challenge (3) "
            "by employing Monte Carlo Dropout and conformal prediction.",
            "In the domain of climate downscaling, deep learning has shown promise "
            "for super-resolution of coarse model outputs. Vandal et al. (2017) used "
            "convolutional networks for statistical downscaling of precipitation. "
            "Leinonen et al. (2020) applied GANs to cloud microphysics emulation.",
            "Reinforcement learning has recently been applied to adaptive observation "
            "systems for weather prediction. Hoffman et al. (2021) demonstrated that "
            "RL-based adaptive sampling strategies outperform traditional designs for "
            "tropical cyclone intensity forecasting.",
            "This review reveals a clear trend toward larger, more general foundation "
            "models for weather and climate. Our contribution fits within this trend "
            "but uniquely emphasizes long-range (monthly to seasonal) forecasting and "
            "the explicit modeling of multi-scale interactions.",
        ],
    }

    # Paragraph text for filling pages
    generic_paragraphs = [
        "The experimental validation of our approach was conducted using a rigorous "
        "cross-validation protocol designed to prevent data leakage across temporal "
        "boundaries. Specifically, data from 1980–2005 was used for training, "
        "2006–2015 for validation, and 2016–2020 for held-out testing. "
        "This temporal split ensures that no future information contaminates the "
        "training process and that reported metrics reflect genuine out-of-sample performance.",

        "Table 4.1 summarizes the performance of all evaluated models across the six "
        "benchmark datasets. MSTFN achieves the lowest RMSE and highest skill score "
        "(SS) in 34 of 36 experimental conditions. The improvements are largest for "
        "12-month forecasts and smallest for 3-month forecasts, consistent with our "
        "hypothesis that multi-scale temporal modeling provides the most benefit at "
        "longer horizons where synoptic-scale variability is less dominant.",

        "We observe that the attention weights learned by MSTFN exhibit physically "
        "interpretable spatial patterns. In particular, for North American temperature "
        "anomaly prediction, the model assigns high attention to the Nino3.4 region "
        "in the tropical Pacific, consistent with the well-known ENSO teleconnection. "
        "Similar patterns are observed for the Indian Ocean Dipole and the Arctic "
        "Oscillation, suggesting that the model is implicitly learning established "
        "climatological relationships without explicit supervision.",

        "Ablation studies confirm the contribution of each architectural component. "
        "Removing the multi-scale temporal pyramid reduces RMSE by 8.7% on average. "
        "Removing the cross-scale attention module reduces RMSE by 4.2%. Replacing "
        "the spatial encoder with a standard CNN reduces RMSE by 3.1%. These results "
        "validate our design choices and motivate the increased architectural complexity "
        "compared to simpler baselines.",

        "Computational profiling reveals that MSTFN requires approximately 2.3× more "
        "floating-point operations per forward pass compared to the best-performing "
        "baseline (ConvLSTM-Large). However, owing to its parallelizable attention "
        "mechanism, the wall-clock inference time is only 1.6× longer. For operational "
        "deployment, this overhead is acceptable given the substantial accuracy gains.",

        "The robustness of MSTFN was assessed by evaluating performance on out-of-distribution "
        "climate scenarios including the 1998 El Nino event and the 2012 Arctic sea ice "
        "minimum. In both cases, MSTFN outperformed all baselines, suggesting that the "
        "multi-scale representation generalizes to extreme climate states not fully "
        "represented in the training distribution.",

        "Ethical considerations in AI-assisted climate forecasting include the "
        "potential for over-reliance on black-box predictions and the unequal access "
        "to computational resources across countries. We recommend that operational "
        "deployment of ML-based climate models be accompanied by transparent uncertainty "
        "communication and open access to pre-trained weights.",

        "Future work will investigate (1) the integration of MSTFN with physical "
        "equation constraints via physics-informed neural networks; (2) extension to "
        "coupled ocean-atmosphere modeling; (3) applications to regional extreme "
        "event prediction; and (4) few-shot adaptation to newly instrumented "
        "observational sites with limited historical data.",
    ]

    # Reference entries
    references = [
        "Bi, K., Xie, L., Zhang, H., Chen, X., Gu, X., & Tian, Q. (2023). Accurate "
        "medium-range global weather forecasting with 3D neural networks. Nature, "
        "619(7970), 533–538. https://doi.org/10.1038/s41586-023-06185-3",

        "Keisler, R. (2022). Forecasting global weather with graph neural networks. "
        "arXiv preprint arXiv:2202.07575.",

        "Lam, R., Sanchez-Gonzalez, A., Willson, M., Wirnsberger, P., Fortunato, M., "
        "Alet, F., ... & Battaglia, P. (2023). Learning skillful medium-range global "
        "weather forecasting. Science, 382(6677), 1416–1421.",

        "Pathak, J., Subramanian, S., Harrington, P., Raja, S., Chattopadhyay, A., "
        "Mardani, M., ... & Anandkumar, A. (2022). FourCastNet: A global data-driven "
        "high-resolution weather model using adaptive Fourier neural operators. "
        "arXiv preprint arXiv:2202.11214.",

        "Scher, S., & Messori, G. (2019). Weather and climate forecasting with neural "
        "networks: using general circulation models (GCMs) with different complexity "
        "as a study ground. Geoscientific Model Development, 12(7), 2797–2809.",

        "Shi, X., Chen, Z., Wang, H., Yeung, D.-Y., Wong, W.-K., & Woo, W.-C. (2015). "
        "Convolutional LSTM network: A machine learning approach for precipitation "
        "nowcasting. Advances in Neural Information Processing Systems, 28.",

        "Vandal, T., Kodra, E., Ganguly, S., Michaelis, A., Nemani, R., & Ganguly, "
        "A. R. (2017). DeepSD: Generating high resolution climate change projections "
        "through single image super-resolution. Proceedings of the 23rd ACM SIGKDD "
        "International Conference on Knowledge Discovery and Data Mining, 1663–1672.",

        "Weyn, J. A., Durran, D. R., & Caruana, R. (2020). Improving data-driven "
        "global weather prediction using deep convolutional neural networks on a "
        "cubed sphere. Journal of Advances in Modeling Earth Systems, 12(9).",
    ]

    # ---- Helper: add a styled page ----
    def add_title_page():
        page = doc.new_page(width=595, height=842)
        shape = page.new_shape()
        # Dark blue header band
        shape.draw_rect(pymupdf.Rect(0, 0, 595, 140))
        shape.finish(color=None, fill=(0.08, 0.22, 0.45))
        shape.commit()

        page.insert_text(pymupdf.Point(297, 70), "DOCTORAL THESIS",
                         fontsize=16, fontname="hebo", color=(1, 1, 1),
                         rotate=0)
        page.insert_textbox(
            pymupdf.Rect(60, 160, 535, 300),
            "Machine Learning Approaches to Climate Change Prediction:\n"
            "Multi-Scale Temporal Fusion for Long-Range Atmospheric Forecasting",
            fontsize=18, fontname="tibo", color=(0.05, 0.15, 0.40),
            align=pymupdf.TEXT_ALIGN_CENTER,
        )
        page.insert_textbox(
            pymupdf.Rect(100, 340, 495, 440),
            "Dr. Emily J. Chen\n"
            "Department of Computer Science\n"
            "Institute for Climate and Data Science\n"
            "University of Westbrook",
            fontsize=13, fontname="helv", color=(0.1, 0.1, 0.1),
            align=pymupdf.TEXT_ALIGN_CENTER,
        )
        page.insert_textbox(
            pymupdf.Rect(100, 460, 495, 520),
            "Submitted in partial fulfillment of the requirements\n"
            "for the degree of Doctor of Philosophy",
            fontsize=11, fontname="tiit", color=(0.2, 0.2, 0.2),
            align=pymupdf.TEXT_ALIGN_CENTER,
        )
        page.insert_textbox(
            pymupdf.Rect(100, 560, 495, 600),
            "Westbrook, 2024",
            fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2),
            align=pymupdf.TEXT_ALIGN_CENTER,
        )
        # Add a decorative line
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(72, 530), pymupdf.Point(523, 530))
        shape2.finish(color=(0.08, 0.22, 0.45), width=1.5)
        shape2.commit()

        # Add a small chart-like image (scatter plot representation using shapes)
        shape3 = page.new_shape()
        cx, cy = 297, 700
        r = 60
        shape3.draw_circle(pymupdf.Point(cx, cy), r)
        shape3.finish(color=(0.08, 0.22, 0.45), fill=(0.85, 0.91, 0.97), width=1)
        shape3.commit()
        page.insert_text(pymupdf.Point(267, 704),
                         "CLIMATE AI", fontsize=9, fontname="hebo",
                         color=(0.08, 0.22, 0.45))

        # External hyperlink on title page
        page.insert_link({
            "kind": pymupdf.LINK_URI,
            "from": pymupdf.Rect(200, 760, 395, 780),
            "uri": "https://doi.org/10.1000/thesis.2024.climate",
        })
        page.insert_text(pymupdf.Point(200, 775),
                         "DOI: 10.1000/thesis.2024.climate",
                         fontsize=9, color=(0, 0, 0.7))

    def add_toc_page():
        page = doc.new_page(width=595, height=842)
        page.insert_text(pymupdf.Point(72, 72),
                         "TABLE OF CONTENTS", fontsize=16, fontname="hebo")
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(523, 80))
        shape.finish(color=(0, 0, 0), width=1)
        shape.commit()
        toc_entries = [
            ("Abstract", "ii"),
            ("Chapter 1: Introduction", "1"),
            ("Chapter 2: Literature Review", "7"),
            ("Chapter 3: Methodology", "16"),
            ("Chapter 4: Experimental Results", "26"),
            ("Chapter 5: Discussion", "38"),
            ("Chapter 6: Conclusion", "46"),
            ("References", "51"),
            ("Appendix A: Data Sources", "58"),
            ("Appendix B: Code Listings", "61"),
        ]
        y = 110
        for title, pg in toc_entries:
            page.insert_text(pymupdf.Point(80, y), title, fontsize=11, fontname="helv")
            page.insert_text(pymupdf.Point(490, y), pg, fontsize=11, fontname="helv")
            y += 22

    def add_content_page(chapter_title, section_paragraphs, page_num_display,
                         add_image=False, add_links=False):
        page = doc.new_page(width=595, height=842)

        # Header
        page.insert_text(pymupdf.Point(72, 45),
                         chapter_title, fontsize=11, fontname="hebo",
                         color=(0.3, 0.3, 0.3))
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 52), pymupdf.Point(523, 52))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape.commit()

        y = 80
        content_rect_width = 451
        line_height_approx = 14
        char_per_line_approx = 90

        for para in section_paragraphs:
            if y > 760:
                break
            # Estimate height needed
            lines_needed = math.ceil(len(para) / char_per_line_approx)
            height_needed = lines_needed * line_height_approx + 8
            rect = pymupdf.Rect(72, y, 72 + content_rect_width,
                                min(y + height_needed, 800))
            page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                                align=pymupdf.TEXT_ALIGN_JUSTIFY)
            y += height_needed + 6

        if add_image and y < 700:
            # Draw a synthetic "figure" using shapes
            fig_y = y + 10
            shape_img = page.new_shape()
            shape_img.draw_rect(pymupdf.Rect(100, fig_y, 495, fig_y + 100))
            shape_img.finish(color=(0.5, 0.5, 0.5), fill=(0.92, 0.95, 0.98), width=1)
            shape_img.commit()
            # Simulate chart bars
            bar_colors = [
                (0.08, 0.36, 0.62), (0.20, 0.55, 0.33),
                (0.75, 0.25, 0.10), (0.55, 0.25, 0.65),
            ]
            bar_x = 130
            bar_heights = [70, 50, 80, 45]
            for bh, bc in zip(bar_heights, bar_colors):
                sh = page.new_shape()
                sh.draw_rect(pymupdf.Rect(bar_x, fig_y + 100 - bh - 5,
                                         bar_x + 40, fig_y + 95))
                sh.finish(color=None, fill=bc)
                sh.commit()
                bar_x += 60
            page.insert_text(pymupdf.Point(230, fig_y + 112),
                             "Figure: Model comparison (RMSE)",
                             fontsize=9, fontname="tiit", color=(0.3, 0.3, 0.3))

        if add_links and y < 780:
            link_y = min(y + 20, 790)
            page.insert_link({
                "kind": pymupdf.LINK_URI,
                "from": pymupdf.Rect(72, link_y - 12, 350, link_y + 2),
                "uri": "https://github.com/emilychen/mstfn-climate",
            })
            page.insert_text(pymupdf.Point(72, link_y),
                             "Code available: github.com/emilychen/mstfn-climate",
                             fontsize=9, color=(0, 0, 0.8))

        # Footer with page number
        page.insert_text(pymupdf.Point(285, 820),
                         str(page_num_display), fontsize=9, fontname="helv",
                         color=(0.4, 0.4, 0.4))

    # ---- PAGE 0: Title page ----
    add_title_page()

    # ---- PAGE 1: Table of Contents ----
    add_toc_page()

    # ---- PAGE 2: Abstract ----
    add_content_page("Abstract", chapter_contents["Abstract"], "ii",
                     add_image=False, add_links=False)

    # ---- PAGES 3–8: Chapter 1 Introduction (6 pages) ----
    intro_paras = chapter_contents["Introduction"]
    for i in range(6):
        paras = intro_paras[i:i+1] + generic_paragraphs[:2]
        add_content_page("Chapter 1: Introduction",
                         paras, str(i + 1),
                         add_image=(i in [1, 4]),
                         add_links=(i == 5))

    # ---- PAGES 9–17: Chapter 2 Literature Review (9 pages) ----
    lit_paras = chapter_contents["Literature Review"]
    for i in range(9):
        paras = lit_paras[i:i+1] + generic_paragraphs[2:4]
        add_content_page("Chapter 2: Literature Review",
                         paras, str(i + 7),
                         add_image=(i in [2, 6]),
                         add_links=(i in [3, 7]))

    # ---- PAGES 18–27: Chapter 3 Methodology (10 pages) ----
    for i in range(10):
        paras = [
            f"Section 3.{i + 1}: " + generic_paragraphs[i % len(generic_paragraphs)],
            generic_paragraphs[(i + 1) % len(generic_paragraphs)],
            generic_paragraphs[(i + 2) % len(generic_paragraphs)],
        ]
        add_content_page("Chapter 3: Methodology",
                         paras, str(i + 16),
                         add_image=(i in [0, 3, 7]),
                         add_links=(i in [4, 9]))

    # ---- PAGES 28–39: Chapter 4 Experimental Results (12 pages) ----
    for i in range(12):
        paras = [
            f"Experiment {i + 1}: " + generic_paragraphs[(i + 2) % len(generic_paragraphs)],
            generic_paragraphs[(i + 3) % len(generic_paragraphs)],
        ]
        add_content_page("Chapter 4: Experimental Results",
                         paras, str(i + 26),
                         add_image=(i % 3 == 0),
                         add_links=(i % 4 == 0))

    # ---- PAGES 40–47: Chapter 5 Discussion (8 pages) ----
    for i in range(8):
        paras = [
            generic_paragraphs[(i + 1) % len(generic_paragraphs)],
            generic_paragraphs[(i + 4) % len(generic_paragraphs)],
        ]
        add_content_page("Chapter 5: Discussion",
                         paras, str(i + 38),
                         add_image=(i in [1, 5]),
                         add_links=(i == 3))

    # ---- PAGES 48–52: Chapter 6 Conclusion (5 pages) ----
    conclusion_paras = [
        "This thesis has presented MSTFN, a novel multi-scale temporal fusion network "
        "for long-range climate forecasting. Through extensive experimentation on six "
        "benchmark datasets, we demonstrated that MSTFN outperforms existing deep "
        "learning baselines by 12.3% on RMSE for monthly-to-seasonal forecasts.",
        "The interpretability analysis revealed that MSTFN implicitly learns physically "
        "meaningful teleconnections, including ENSO and the Arctic Oscillation, without "
        "explicit supervision. This finding provides evidence that the model is not "
        "merely fitting statistical patterns but is capturing causally relevant "
        "atmospheric dynamics.",
        "The limitations of this work include the reliance on ERA5 reanalysis data, "
        "which itself contains model artifacts, and the computational cost of training "
        "at planetary resolution. Future work should investigate transfer learning "
        "from physics-based simulations and more efficient attention mechanisms.",
        "In conclusion, this thesis demonstrates the viability of data-driven approaches "
        "for long-range climate prediction and opens several promising avenues for "
        "future research. We hope that the open-source release of MSTFN and the "
        "accompanying dataset will accelerate progress in this important field.",
        "The societal implications of improved climate forecasting cannot be overstated. "
        "From agricultural planning in developing nations to infrastructure resilience "
        "in coastal cities, accurate seasonal-to-decadal predictions have direct "
        "humanitarian value.",
    ]
    for i in range(5):
        add_content_page("Chapter 6: Conclusion",
                         [conclusion_paras[i]] + generic_paragraphs[:2],
                         str(i + 46),
                         add_image=(i == 2),
                         add_links=(i == 4))

    # ---- PAGES 53–59: References (7 pages) ----
    for i in range(7):
        ref_slice = references[i % len(references):i % len(references) + 3]
        if not ref_slice:
            ref_slice = references[:3]
        add_content_page("References", ref_slice, str(i + 51),
                         add_image=False, add_links=False)

    # ---- PAGES 60–62: Appendix A (3 pages) ----
    appendix_a_paras = [
        "Table A.1: ERA5 reanalysis variables used in this study. Variables include "
        "2-meter temperature (T2M), sea surface temperature (SST), geopotential "
        "height at 500 hPa (Z500), total column water vapor (TCWV), and 10-meter "
        "wind components (U10, V10). All variables are provided at 0.25° × 0.25° "
        "horizontal resolution on a regular latitude-longitude grid.",
        "Data was obtained from the Copernicus Climate Change Service (C3S) Climate "
        "Data Store (CDS) using the Python cdsapi library. Quality control procedures "
        "included outlier detection using 5σ thresholds, gap-filling by linear "
        "interpolation for gaps ≤ 3 days, and standardization to zero mean and unit "
        "variance computed over the training period.",
        "Additional observational datasets used for evaluation include the HadCRUT5 "
        "global surface temperature record, the NOAA Extended Reconstructed Sea "
        "Surface Temperature (ERSSTv5) dataset, and the Berkeley Earth global land "
        "temperature dataset. These are used exclusively for out-of-sample validation "
        "and were not used in model training.",
    ]
    for i in range(3):
        add_content_page("Appendix A: Data Sources",
                         [appendix_a_paras[i]] + generic_paragraphs[1:3],
                         str(i + 58),
                         add_image=(i == 1),
                         add_links=False)

    # ---- PAGES 63–64: Appendix B (2 pages) ----
    appendix_b_paras = [
        "The following Python code listing shows the core MSTFN forward pass. "
        "The full implementation is available at https://github.com/emilychen/mstfn-climate. "
        "Dependencies include PyTorch 2.1, einops, and timm. Training was conducted "
        "with PyTorch Distributed Data Parallel on 128 NVIDIA A100 40GB GPUs.",
        "Listing B.1: MSTFN temporal pyramid encoder. The encoder accepts a sequence "
        "of spatial feature maps and produces multi-scale temporal representations "
        "by applying dilated convolutions with dilation rates [1, 2, 4, 8]. "
        "These representations are then combined via a learned attention-weighted sum.",
    ]
    for i in range(2):
        add_content_page("Appendix B: Code Listings",
                         [appendix_b_paras[i]] + generic_paragraphs[:2],
                         str(i + 61),
                         add_image=False,
                         add_links=(i == 0))

    # ---- Set PDF metadata ----
    doc.set_metadata({
        "title": "Machine Learning Approaches to Climate Change Prediction",
        "author": "Dr. Emily J. Chen",
        "subject": "Doctoral Thesis in Computer Science",
        "keywords": "machine learning, climate change, neural networks, forecasting",
        "creator": "LaTeX with hyperref package",
        "producer": "pdfTeX-1.40.25",
    })

    # ---- Set Table of Contents ----
    toc = [
        [1, "Abstract", 3],
        [1, "Chapter 1: Introduction", 4],
        [1, "Chapter 2: Literature Review", 10],
        [1, "Chapter 3: Methodology", 19],
        [1, "Chapter 4: Experimental Results", 29],
        [1, "Chapter 5: Discussion", 41],
        [1, "Chapter 6: Conclusion", 49],
        [1, "References", 54],
        [1, "Appendix A: Data Sources", 61],
        [1, "Appendix B: Code Listings", 64],
    ]
    doc.set_toc(toc)

    doc.save(THESIS_PDF)
    doc.close()

    page_count = 0
    doc2 = pymupdf.open(THESIS_PDF)
    page_count = doc2.page_count
    doc2.close()
    print(f'Initial thesis PDF created: {THESIS_PDF}')
    print(f'Pages: {page_count}')
    print(f'Scripts directory: {SCRIPTS_DIR} (pdf_stats.py NOT present)')

    # GUI-ready startup: open thesis.pdf in evince
    launch_gui(f'evince "{THESIS_PDF}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
