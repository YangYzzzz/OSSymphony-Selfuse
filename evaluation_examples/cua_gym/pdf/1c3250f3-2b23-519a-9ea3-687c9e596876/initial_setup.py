"""
Initial Setup: Create an 85-page thesis PDF with no headers or footers.
Task ID: pdf_ro_022
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_022'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/thesis.pdf'


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions: Letter size
    W, H = 612, 792
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 540
    MARGIN_TOP = 72
    MARGIN_BOTTOM = 720
    LINE_HEIGHT = 14

    # ---- Page 1: Title Page ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(
        pymupdf.Point(W / 2 - 150, 250),
        "A Comprehensive Study of",
        fontsize=18, fontname="tibo", color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(W / 2 - 180, 285),
        "Machine Learning Applications in",
        fontsize=18, fontname="tibo", color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(W / 2 - 140, 320),
        "Environmental Science",
        fontsize=18, fontname="tibo", color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(W / 2 - 80, 400),
        "Master Thesis",
        fontsize=14, fontname="tiro", color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(W / 2 - 90, 440),
        "Emily R. Johnson",
        fontsize=14, fontname="tiro", color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(W / 2 - 120, 480),
        "Department of Computer Science",
        fontsize=12, fontname="tiro", color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(W / 2 - 100, 510),
        "University of Westfield",
        fontsize=12, fontname="tiro", color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(W / 2 - 50, 560),
        "March 2026",
        fontsize=12, fontname="tiro", color=(0, 0, 0),
    )

    # Chapter structure for an 85-page thesis
    chapters = [
        ("Chapter 1: Introduction", [
            "The intersection of machine learning and environmental science has emerged as one of the most promising areas of interdisciplinary research in recent years. As global environmental challenges intensify, the need for sophisticated analytical tools that can process vast amounts of ecological data has become increasingly apparent.",
            "Traditional statistical methods, while valuable, often struggle to capture the complex, nonlinear relationships inherent in environmental systems. Machine learning algorithms, by contrast, excel at identifying patterns in high-dimensional data, making them well-suited for tasks such as climate modeling, species distribution prediction, and pollution monitoring.",
            "This thesis presents a comprehensive investigation into the application of modern machine learning techniques to three key areas of environmental science: atmospheric pollution forecasting, biodiversity assessment through remote sensing, and water quality prediction in urban watersheds.",
            "The motivation for this research stems from the growing recognition that environmental monitoring systems generate enormous volumes of data that remain underutilized. Satellite imagery, sensor networks, and citizen science platforms collectively produce terabytes of information daily, yet much of this data is analyzed using conventional methods that fail to exploit its full potential.",
            "Our approach leverages recent advances in deep learning, ensemble methods, and transfer learning to develop models that not only achieve superior predictive accuracy but also provide interpretable insights into the underlying environmental processes.",
            "The remainder of this chapter provides background on the environmental challenges addressed, reviews the current state of machine learning in environmental applications, and outlines the specific research questions and contributions of this thesis.",
        ], 10),
        ("Chapter 2: Literature Review", [
            "The application of computational methods to environmental science has a rich history dating back to the early numerical weather prediction models of the 1950s. However, the last decade has witnessed an unprecedented acceleration in both the sophistication of available algorithms and the volume of environmental data.",
            "Early work by Richardson (1922) on numerical weather prediction laid the groundwork for computational approaches to atmospheric science. The development of general circulation models in the 1960s and 1970s represented a major milestone, enabling researchers to simulate global climate patterns for the first time.",
            "The emergence of machine learning as a distinct field in the 1980s and 1990s introduced new tools for pattern recognition and prediction. Initial applications in environmental science focused primarily on neural networks for weather forecasting and decision trees for land use classification.",
            "More recently, the deep learning revolution has opened new possibilities. Convolutional neural networks have proven highly effective for analyzing satellite imagery, while recurrent neural networks and their variants (LSTMs, GRUs) have shown promise for temporal environmental data such as air quality time series.",
            "Transfer learning has emerged as a particularly valuable technique for environmental applications, where labeled training data is often scarce. By leveraging models pre-trained on large general-purpose datasets, researchers have achieved remarkable results even with limited domain-specific data.",
            "The concept of physics-informed neural networks represents another important development, enabling the incorporation of known physical laws into the learning process. This hybrid approach combines the flexibility of neural networks with the rigor of established scientific principles.",
        ], 15),
        ("Chapter 3: Methodology", [
            "This chapter describes the methodological framework employed in this thesis, encompassing data collection, preprocessing, model architecture design, training procedures, and evaluation metrics.",
            "Our research adopts a multi-method approach, combining supervised learning for prediction tasks, unsupervised learning for pattern discovery, and semi-supervised learning to leverage the large volumes of unlabeled environmental data available.",
            "Data sources include the European Space Agency's Copernicus satellite constellation, the US Environmental Protection Agency's Air Quality System database, the Global Biodiversity Information Facility, and a network of IoT water quality sensors deployed across three metropolitan areas.",
            "For atmospheric pollution forecasting, we developed a hybrid architecture combining temporal convolutional networks with attention mechanisms. This design captures both local temporal patterns and long-range dependencies in pollution time series data.",
            "The biodiversity assessment component employs a modified ResNet-50 architecture pre-trained on ImageNet and fine-tuned on high-resolution satellite imagery. We augment this with a custom multi-scale feature extraction module designed to detect ecological features at varying spatial resolutions.",
            "Water quality prediction utilizes a graph neural network framework that models the spatial relationships between monitoring stations in urban watershed networks. This approach naturally captures the flow-dependent correlations between upstream and downstream measurements.",
            "All models were trained using a rigorous cross-validation procedure with temporal splitting to prevent data leakage. Hyperparameter optimization was conducted using Bayesian optimization with a Gaussian process surrogate model.",
        ], 18),
        ("Chapter 4: Atmospheric Pollution Forecasting", [
            "Urban air pollution remains one of the most pressing public health challenges worldwide. The World Health Organization estimates that ambient air pollution causes approximately 4.2 million premature deaths annually, with the burden falling disproportionately on low- and middle-income countries.",
            "Our atmospheric pollution forecasting system targets six key pollutants: PM2.5, PM10, NO2, SO2, O3, and CO. For each pollutant, we developed specialized prediction models that account for the distinct chemical and physical processes governing their atmospheric behavior.",
            "The training dataset encompasses five years of hourly measurements from 847 monitoring stations across 12 metropolitan areas, supplemented by meteorological reanalysis data from the ERA5 dataset and land use information from the CORINE database.",
            "Results demonstrate that our hybrid temporal convolutional network achieves a mean absolute error of 8.3 micrograms per cubic meter for 24-hour PM2.5 forecasts, representing a 23 percent improvement over the best-performing baseline model.",
            "Analysis of the attention weights reveals that the model learns to focus on specific meteorological conditions known to influence pollution dispersion, including atmospheric boundary layer height, wind speed, and temperature inversion events.",
            "We also present a novel uncertainty quantification framework based on Monte Carlo dropout that provides calibrated prediction intervals, enabling decision-makers to assess the reliability of individual forecasts.",
        ], 14),
        ("Chapter 5: Biodiversity Assessment", [
            "Remote sensing technology has transformed biodiversity monitoring by enabling large-scale habitat mapping and change detection. However, translating raw satellite imagery into accurate biodiversity indicators remains a significant challenge.",
            "Our approach addresses this challenge through a multi-task learning framework that simultaneously predicts species richness, habitat quality indices, and land cover classifications from high-resolution satellite imagery.",
            "The training dataset comprises 15,000 georeferenced field survey plots with associated biodiversity measurements, paired with corresponding Sentinel-2 satellite images at 10-meter spatial resolution.",
            "Our modified ResNet-50 architecture achieves a coefficient of determination of 0.78 for species richness prediction, significantly outperforming traditional spectral index-based approaches which achieve R-squared values of 0.45 to 0.52.",
            "Feature attribution analysis using integrated gradients reveals that the model relies heavily on texture features and spatial patterns in the near-infrared bands, consistent with ecological theory linking vegetation structure to biodiversity.",
            "We demonstrate the practical utility of our approach through a case study in the Amazon basin, where we mapped biodiversity hotspots across a 50,000 square kilometer region using a mosaic of 340 satellite scenes.",
        ], 12),
        ("Chapter 6: Water Quality Prediction", [
            "Urban water quality management presents unique challenges due to the complex interactions between natural hydrological processes, infrastructure systems, and human activities. Point and non-point source pollution, combined sewer overflows, and stormwater runoff all contribute to degradation of urban water bodies.",
            "Our graph neural network framework models the urban watershed as a directed graph, where nodes represent monitoring stations and edges encode the hydraulic connectivity between stations based on the drainage network topology.",
            "The dataset includes continuous water quality measurements from 156 monitoring stations across three metropolitan areas: Portland, Singapore, and Munich. Parameters measured include dissolved oxygen, turbidity, pH, conductivity, and concentrations of nitrogen and phosphorus species.",
            "The graph neural network achieves Nash-Sutcliffe efficiency coefficients above 0.85 for dissolved oxygen prediction at most stations, demonstrating strong ability to capture the spatial dynamics of water quality in complex urban networks.",
            "An important finding is that the learned edge attention weights correlate strongly with known pollution source locations, suggesting that the model implicitly identifies key contamination pathways without explicit supervision.",
        ], 8),
        ("Chapter 7: Discussion", [
            "The results presented in the preceding chapters demonstrate the considerable potential of machine learning for environmental monitoring and prediction. However, several important considerations merit discussion.",
            "First, model interpretability remains a critical concern for environmental applications where decisions may affect public health and ecosystem management. While we have employed various attribution methods, the inherent opacity of deep learning models continues to pose challenges for building trust among domain experts and policymakers.",
            "Second, the generalizability of our models across geographic regions and temporal periods requires careful consideration. Environmental systems exhibit substantial spatial and temporal variability, and models trained on data from one region may not transfer well to another without adaptation.",
            "Third, the computational cost of training and deploying deep learning models must be weighed against the marginal improvements they offer over simpler approaches. In resource-constrained settings, ensemble methods based on gradient boosting may provide a more practical alternative.",
            "Finally, we note that the quality and representativeness of training data remain fundamental limitations. Monitoring networks tend to be concentrated in wealthy, urban areas, potentially introducing systematic biases into models trained on these data.",
        ], 5),
        ("Chapter 8: Conclusions and Future Work", [
            "This thesis has demonstrated that modern machine learning techniques can significantly advance environmental monitoring and prediction capabilities across three important domains: atmospheric pollution forecasting, biodiversity assessment, and water quality prediction.",
            "Key contributions include the hybrid temporal convolutional network for pollution forecasting, the multi-task satellite image analysis framework for biodiversity mapping, and the graph neural network approach to urban water quality prediction.",
            "Future research directions include the development of foundation models for environmental science, the integration of physics-based constraints into all three modeling frameworks, and the creation of standardized benchmark datasets to facilitate reproducible comparison of methods.",
            "We also identify the need for more robust transfer learning approaches that can adapt models across geographic regions with minimal additional training data, addressing the current limitation of geographic specificity.",
        ], 3),
    ]

    current_page = 1  # already created title page (page index 0)

    for chapter_title, paragraphs, num_pages in chapters:
        for pg in range(num_pages):
            page = doc.new_page(width=W, height=H)
            current_page += 1
            y = MARGIN_TOP

            if pg == 0:
                # Chapter heading on first page of chapter
                page.insert_text(
                    pymupdf.Point(MARGIN_LEFT, y + 20),
                    chapter_title,
                    fontsize=16, fontname="tibo", color=(0, 0, 0),
                )
                y += 50

            # Fill page with text content
            text_rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, MARGIN_BOTTOM)
            # Cycle through paragraphs to fill pages
            para_idx = pg % len(paragraphs)
            # Build page text from multiple paragraphs
            page_text = ""
            for i in range(3):
                idx = (para_idx + i) % len(paragraphs)
                page_text += paragraphs[idx] + "\n\n"

            page.insert_textbox(
                text_rect,
                page_text.strip(),
                fontsize=11, fontname="tiro", color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

    # Verify we have 85 pages total
    total_pages = doc.page_count
    print(f"Total pages created: {total_pages}")

    # If we have too many pages, trim to 85
    if total_pages > 85:
        doc.select(list(range(85)))
        print(f"Trimmed to 85 pages")
    elif total_pages < 85:
        # Add extra pages to reach 85
        for i in range(85 - total_pages):
            page = doc.new_page(width=W, height=H)
            text_rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT, MARGIN_BOTTOM)
            page.insert_textbox(
                text_rect,
                "The analysis of environmental data continues to reveal new patterns and relationships. "
                "Statistical tests confirm the significance of the observed trends across multiple study sites. "
                "The integration of satellite observations with ground-based measurements provides a comprehensive "
                "view of the environmental changes occurring at both local and regional scales. "
                "Further investigation into the temporal dynamics of these phenomena suggests that seasonal "
                "variations play a more important role than previously recognized in the literature. "
                "The implications of these findings extend beyond the immediate study area, with potential "
                "applications in policy development and resource management strategies.\n\n"
                "Additional field campaigns conducted during the summer and autumn months provided valuable "
                "supplementary data that helped validate the remote sensing predictions. The correlation between "
                "predicted and observed values exceeded 0.90 at most validation sites, confirming the robustness "
                "of the modeling approach. Cross-validation results further support the generalizability of the "
                "trained models across different geographic regions and climatic zones.",
                fontsize=11, fontname="tiro", color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )
        print(f"Padded to 85 pages (added {85 - total_pages} pages)")

    print(f"Final page count: {doc.page_count}")
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open the PDF in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
