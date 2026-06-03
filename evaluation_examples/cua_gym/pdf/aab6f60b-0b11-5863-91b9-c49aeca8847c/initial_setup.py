"""
Initial Setup: Create a 52-page research paper PDF with chapter bookmarks (no appendix bookmark)
Task ID: pdf_mbc_037
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_037'
OUTPUT = f'{WORKDIR}/Documents/research_paper.pdf'


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
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    doc = pymupdf.open()

    # --- Research paper content ---
    # Chapter structure with page ranges:
    # Title page: page 1
    # Chapter 1: Introduction (pages 2-8)
    # Chapter 2: Literature Review (pages 9-18)
    # Chapter 3: Methodology (pages 19-28)
    # Chapter 4: Results (pages 29-38)
    # Chapter 5: Discussion (pages 39-44)
    # Appendix A: Data Tables (pages 45-52) - NO bookmark for this

    title = "Advanced Machine Learning Approaches for Climate Pattern Recognition: A Comprehensive Study"
    authors = "Dr. Elena Vasquez, Dr. James Thornton, Dr. Mei-Lin Park"
    institution = "Department of Environmental Data Science, Pacific Northwest Research University"

    chapter_titles = {
        1: "Introduction",
        2: "Literature Review",
        3: "Methodology",
        4: "Results and Analysis",
        5: "Discussion and Future Directions",
    }

    chapter_start_pages = {
        1: 2,
        2: 9,
        3: 19,
        4: 29,
        5: 39,
    }

    # Content snippets per chapter for realistic pages
    chapter_content = {
        1: [
            "Climate change remains one of the most pressing challenges facing humanity in the 21st century. "
            "The ability to accurately predict and model climate patterns has become increasingly critical for "
            "policymakers, urban planners, and environmental scientists. Traditional statistical methods, while "
            "valuable, often struggle to capture the complex nonlinear relationships inherent in atmospheric data.",
            "Recent advances in machine learning, particularly deep neural networks and ensemble methods, have "
            "shown promising results in various scientific domains. However, their application to climate science "
            "presents unique challenges related to data sparsity, temporal dependencies, and the need for "
            "physically interpretable models.",
            "This study investigates the application of advanced machine learning techniques to the problem of "
            "regional climate pattern recognition. We analyze over 40 years of satellite and ground-station "
            "data from 2,847 monitoring stations across the Pacific Northwest region.",
            "Our primary research objectives are threefold: (1) to develop a hybrid model combining convolutional "
            "neural networks with physics-informed constraints, (2) to evaluate the model's performance against "
            "established climate indices, and (3) to assess the interpretability of learned features.",
            "The remainder of this paper is organized as follows. Chapter 2 provides a comprehensive review of "
            "relevant literature. Chapter 3 describes our methodology in detail. Chapter 4 presents the results "
            "of our experiments. Chapter 5 discusses implications and future research directions.",
            "Significance of this research extends beyond academic interest. Improved climate pattern recognition "
            "directly supports agricultural planning, water resource management, and disaster preparedness "
            "initiatives across the region.",
        ],
        2: [
            "The intersection of machine learning and climate science has been an active area of research since "
            "the early 2000s. Rasp et al. (2018) demonstrated that neural networks could effectively parameterize "
            "subgrid processes in climate models, achieving significant improvements over traditional approaches.",
            "Convolutional neural networks (CNNs) have been applied to various geospatial problems. Liu et al. "
            "(2016) used CNNs for land cover classification from satellite imagery with 94.3% accuracy. "
            "Subsequently, Reichstein et al. (2019) proposed a framework for integrating deep learning with "
            "physical process understanding.",
            "Transfer learning techniques have shown particular promise in climate applications where labeled "
            "data is scarce. Martinez and Chen (2020) demonstrated that pre-training on global reanalysis data "
            "improved regional prediction accuracy by 23% compared to training from scratch.",
            "Physics-informed neural networks (PINNs) represent a paradigm shift in scientific machine learning. "
            "Raissi et al. (2019) introduced the concept of embedding physical constraints directly into the "
            "loss function, ensuring that model predictions remain consistent with known physical laws.",
            "Ensemble methods have been widely used in climate modeling. Random forests and gradient boosting "
            "machines have proven effective for feature selection and prediction in environmental datasets. "
            "Breiman (2001) established the theoretical foundation that underpins modern ensemble approaches.",
            "The challenge of temporal dependencies in climate data has been addressed through various recurrent "
            "architectures. Long Short-Term Memory (LSTM) networks have demonstrated strong performance in "
            "time series forecasting of temperature and precipitation anomalies.",
            "Attention mechanisms, originally developed for natural language processing, have found applications "
            "in climate science. Vaswani et al. (2017) introduced the Transformer architecture, which has "
            "since been adapted for spatiotemporal climate prediction tasks.",
            "Gap analysis reveals that few studies have combined physics-informed constraints with modern "
            "deep learning architectures specifically for regional climate pattern recognition. This gap "
            "motivates the present study.",
            "Satellite-based observations provide critical data for climate analysis. The MODIS, Landsat, and "
            "Sentinel missions have generated petabytes of Earth observation data requiring sophisticated "
            "analytical techniques.",
        ],
        3: [
            "Our methodology consists of four main components: data acquisition and preprocessing, feature "
            "engineering, model architecture design, and validation framework. Each component is described "
            "in detail in the following sections.",
            "Data were collected from the NOAA Climate Data Online repository, encompassing daily observations "
            "from 2,847 ground stations across Washington, Oregon, Idaho, and British Columbia for the period "
            "1980-2023. Variables include temperature (min, max, mean), precipitation, wind speed, humidity, "
            "and barometric pressure.",
            "Quality control procedures followed WMO guidelines (2018). Missing data imputation used a "
            "spatiotemporal kriging approach, which accounts for both spatial correlation between stations "
            "and temporal autocorrelation within station records.",
            "Feature engineering incorporated domain knowledge from atmospheric science. We computed 47 derived "
            "features including: temperature gradients, precipitation intensity indices, atmospheric stability "
            "parameters, and teleconnection indices (ENSO, PDO, NAO).",
            "The proposed PhysNet-Climate architecture combines a ResNet-50 backbone for spatial feature "
            "extraction with a Temporal Fusion Transformer for capturing long-range temporal dependencies. "
            "Physics constraints are enforced through custom loss terms.",
            "The physics-informed loss function incorporates three conservation laws: energy balance, "
            "mass conservation (moisture budget), and the thermal wind relationship. These constraints "
            "prevent the model from learning physically implausible patterns.",
            "Training utilized a distributed computing setup with 8 NVIDIA A100 GPUs. The Adam optimizer "
            "with cosine annealing learning rate schedule was employed. Total training time was approximately "
            "72 hours for the full model ensemble.",
            "Cross-validation employed a modified blocked time-series split to prevent data leakage. Five folds "
            "were created, each with 8 years of training data and 2 years of validation data. The final "
            "evaluation used a held-out test set spanning 2021-2023.",
            "Statistical significance was assessed using the Wilcoxon signed-rank test with Bonferroni "
            "correction for multiple comparisons. Effect sizes were computed using Cohen's d.",
        ],
        4: [
            "The PhysNet-Climate model achieved a mean absolute error (MAE) of 0.87 degrees C for temperature "
            "prediction and 2.3 mm for daily precipitation, representing improvements of 31% and 18% "
            "respectively over the baseline CNN model.",
            "Table 4.1 presents the comparative performance metrics across all models. The physics-informed "
            "variant consistently outperformed purely data-driven approaches, with particularly notable "
            "improvements during extreme weather events.",
            "Analysis of learned features revealed that the model captured physically meaningful patterns. "
            "The first principal component of the embedding space correlated strongly (r=0.94) with the "
            "Pacific Decadal Oscillation index.",
            "Regional performance varied considerably. Coastal stations showed the highest prediction accuracy "
            "(MAE = 0.62 degrees C), while mountainous regions presented greater challenges (MAE = 1.24 degrees C), "
            "consistent with the known complexity of orographic effects.",
            "The attention mechanism weights provided interpretable insights into the model's decision process. "
            "For precipitation prediction, the model assigned highest attention to humidity values from "
            "48-72 hours prior and to upstream station data.",
            "Extreme event detection achieved an F1 score of 0.83 for heat waves and 0.79 for atmospheric "
            "rivers. The recall for high-impact events (defined as exceeding the 95th percentile) was 0.91, "
            "suggesting the model is particularly skilled at detecting rare but consequential patterns.",
            "Ablation studies confirmed the importance of physics-informed constraints. Removing the energy "
            "balance constraint increased MAE by 12%, while removing the moisture budget constraint "
            "increased precipitation MAE by 19%.",
            "Computational efficiency analysis showed that the model required 0.3 seconds per inference "
            "on a single GPU, making it suitable for operational forecasting applications.",
            "Uncertainty quantification using Monte Carlo dropout revealed well-calibrated prediction "
            "intervals, with 95% confidence intervals containing the true value 93.7% of the time.",
        ],
        5: [
            "The results demonstrate that physics-informed deep learning represents a viable and promising "
            "approach to regional climate pattern recognition. The consistent improvement over baseline "
            "methods across multiple metrics validates our hybrid architecture design.",
            "The interpretability analysis addresses a critical concern in applying machine learning to "
            "scientific problems. The strong correlation between learned features and established climate "
            "indices suggests that the model is capturing genuine physical relationships.",
            "Comparison with operational weather forecasting models reveals complementary strengths. "
            "While numerical weather prediction excels at short-range forecasts (1-5 days), our model "
            "shows advantages at the subseasonal-to-seasonal timescale (2-8 weeks).",
            "Limitations of this study include the geographic restriction to the Pacific Northwest region. "
            "Transfer learning experiments suggest that the model architecture generalizes well, but "
            "region-specific calibration remains necessary.",
            "Future work should investigate the integration of additional data sources, including satellite "
            "radiance data, soil moisture measurements, and urban heat island effects. The modular "
            "architecture of PhysNet-Climate facilitates such extensions.",
            "The ethical implications of climate prediction technology deserve consideration. Improved "
            "accuracy could exacerbate existing inequalities if access to predictions is not equitably "
            "distributed across communities.",
        ],
    }

    appendix_content = [
        "Table A.1: Complete Station Metadata (Stations 1-500)",
        "Table A.2: Monthly Temperature Anomalies by Region (1980-2023)",
        "Table A.3: Precipitation Distribution Statistics by Season",
        "Table A.4: Model Hyperparameter Sensitivity Analysis",
        "Table A.5: Cross-validation Fold Assignments",
        "Table A.6: Feature Importance Rankings (Top 47 Features)",
        "Table A.7: Extreme Event Catalog with Detection Results",
        "Table A.8: Comparison of Interpolation Methods for Missing Data",
    ]

    # Create 52 pages
    for page_num in range(52):
        page = doc.new_page(width=612, height=792)  # Letter size

        if page_num == 0:
            # Title page
            page.insert_text(pymupdf.Point(72, 200), title,
                             fontsize=18, fontname="hebo", color=(0, 0, 0.4))
            page.insert_text(pymupdf.Point(72, 280), authors,
                             fontsize=12, fontname="tiit", color=(0.2, 0.2, 0.2))
            page.insert_text(pymupdf.Point(72, 310), institution,
                             fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))
            page.insert_text(pymupdf.Point(72, 360), "Published: March 2025",
                             fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))
            page.insert_text(pymupdf.Point(72, 390), "DOI: 10.1234/pnru.climate.2025.0847",
                             fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))

        elif page_num >= 44:
            # Appendix pages (pages 45-52, 0-indexed 44-51)
            appendix_page_idx = page_num - 44
            page.insert_text(pymupdf.Point(72, 60),
                             "Appendix A - Data Tables",
                             fontsize=14, fontname="hebo", color=(0, 0, 0.3))
            # Add page number
            page.insert_text(pymupdf.Point(306, 770), str(page_num + 1),
                             fontsize=10, fontname="tiro", color=(0.4, 0.4, 0.4))

            if appendix_page_idx < len(appendix_content):
                page.insert_text(pymupdf.Point(72, 100),
                                 appendix_content[appendix_page_idx],
                                 fontsize=12, fontname="hebo", color=(0, 0, 0))

                # Add fake table data
                y_start = 140
                headers = ["ID", "Station Name", "Latitude", "Longitude", "Elevation (m)", "Start Year"]
                for col_idx, h in enumerate(headers):
                    page.insert_text(pymupdf.Point(72 + col_idx * 85, y_start),
                                     h, fontsize=8, fontname="hebo", color=(0, 0, 0))
                # Draw header line
                shape = page.new_shape()
                shape.draw_line(pymupdf.Point(72, y_start + 5), pymupdf.Point(540, y_start + 5))
                shape.finish(color=(0, 0, 0), width=0.5)
                shape.commit()

                stations = [
                    ["001", "Cascade Summit", "47.42", "-121.58", "1,203", "1982"],
                    ["002", "Portland Metro", "45.52", "-122.67", "15", "1980"],
                    ["003", "Olympic Coast", "47.91", "-124.63", "8", "1983"],
                    ["004", "Boise Valley", "43.61", "-116.20", "824", "1980"],
                    ["005", "Victoria Harbor", "48.43", "-123.37", "20", "1981"],
                    ["006", "Mount Baker", "48.78", "-121.81", "1,495", "1985"],
                    ["007", "Eugene Plains", "44.05", "-123.09", "130", "1980"],
                    ["008", "Spokane East", "47.66", "-117.42", "588", "1981"],
                    ["009", "Astoria Point", "46.19", "-123.83", "5", "1984"],
                    ["010", "Bend Highland", "44.06", "-121.31", "1,112", "1986"],
                ]
                for row_idx, row in enumerate(stations):
                    y = y_start + 20 + row_idx * 18
                    for col_idx, val in enumerate(row):
                        page.insert_text(pymupdf.Point(72 + col_idx * 85, y),
                                         val, fontsize=7, fontname="tiro", color=(0, 0, 0))
            else:
                page.insert_text(pymupdf.Point(72, 100),
                                 "(Continued from previous page)",
                                 fontsize=10, fontname="tiit", color=(0.3, 0.3, 0.3))

        else:
            # Determine which chapter this page belongs to
            current_chapter = None
            for ch in sorted(chapter_start_pages.keys(), reverse=True):
                if (page_num + 1) >= chapter_start_pages[ch]:
                    current_chapter = ch
                    break

            if current_chapter is None:
                current_chapter = 1

            # Chapter heading on first page of chapter
            if (page_num + 1) == chapter_start_pages[current_chapter]:
                page.insert_text(pymupdf.Point(72, 80),
                                 f"Chapter {current_chapter}: {chapter_titles[current_chapter]}",
                                 fontsize=16, fontname="hebo", color=(0, 0, 0.3))
                content_y_start = 120
            else:
                content_y_start = 72

            # Add paragraph content
            paragraphs = chapter_content.get(current_chapter, [])
            if paragraphs:
                chapter_page_offset = (page_num + 1) - chapter_start_pages[current_chapter]
                para_idx = chapter_page_offset % len(paragraphs)
                text = paragraphs[para_idx]

                rect = pymupdf.Rect(72, content_y_start, 540, 720)
                page.insert_textbox(rect, text, fontsize=11, fontname="tiro",
                                    color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

                # Add a second paragraph if available
                para_idx2 = (para_idx + 1) % len(paragraphs)
                if para_idx2 != para_idx:
                    rect2 = pymupdf.Rect(72, content_y_start + 200, 540, 720)
                    page.insert_textbox(rect2, paragraphs[para_idx2], fontsize=11,
                                        fontname="tiro", color=(0, 0, 0),
                                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

            # Page number
            page.insert_text(pymupdf.Point(306, 770), str(page_num + 1),
                             fontsize=10, fontname="tiro", color=(0.4, 0.4, 0.4))

    # Set Table of Contents (bookmarks) - chapters 1-5 only, NO appendix bookmark
    toc = [
        [1, "Chapter 1: Introduction", 2],
        [1, "Chapter 2: Literature Review", 9],
        [1, "Chapter 3: Methodology", 19],
        [1, "Chapter 4: Results and Analysis", 29],
        [1, "Chapter 5: Discussion and Future Directions", 39],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
