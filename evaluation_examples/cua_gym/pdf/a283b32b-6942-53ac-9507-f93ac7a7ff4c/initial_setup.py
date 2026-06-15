"""
Initial Setup: Complete document preparation on raw_thesis.pdf
Task ID: pdf_adv_200
Domain: pdf

Creates a 50-page raw thesis PDF with no metadata, no bookmarks,
no page numbers, no watermarks. Opens in Evince for agent interaction.
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_adv_200'
OUTPUT = f'{WORKDIR}/raw_thesis.pdf'


def launch_gui(command: str, delay_sec: float = 2.0):
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
    os.makedirs(WORKDIR, exist_ok=True)

    doc = pymupdf.open()

    # Page layout constants
    PAGE_W, PAGE_H = 595, 842  # A4

    # Thesis content structure (50 pages total)
    # p1: Abstract, p3: Introduction, p8: Literature Review,
    # p15: Methodology, p25: Results, p40: Conclusion, p45: References

    sections = [
        # (start_page_1indexed, title, paragraphs)
        (1, "Abstract", [
            "This thesis investigates the application of advanced machine learning techniques "
            "to the domain of climate modeling. We present novel deep learning architectures "
            "capable of capturing complex spatiotemporal patterns in atmospheric data.",
            "Our models achieve a 23% improvement in prediction accuracy compared to traditional "
            "numerical weather prediction (NWP) models on benchmark datasets spanning 1980–2024.",
            "Key contributions include: (1) a transformer-based encoder for geospatial climate "
            "features, (2) an uncertainty quantification framework for ensemble predictions, "
            "and (3) an open-source dataset of processed ERA5 reanalysis fields.",
        ]),
        (2, "Acknowledgments", [
            "I would like to thank my supervisor, Prof. James Harrington, for his invaluable "
            "guidance and support throughout this research project.",
            "This work was supported by the National Science Foundation grant NSF-2024-CL-0042 "
            "and the European Centre for Medium-Range Weather Forecasts (ECMWF) data access program.",
            "I am grateful to my colleagues at the Climate AI Lab for insightful discussions "
            "and feedback during the course of this project.",
        ]),
        (3, "Introduction", [
            "Climate change represents one of the defining challenges of the twenty-first century. "
            "Accurate modeling and prediction of climate systems is essential for informing "
            "policy decisions, disaster preparedness, and long-term environmental planning.",
            "Traditional numerical weather prediction (NWP) models, while physically grounded, "
            "are computationally expensive and struggle to capture fine-scale regional variability. "
            "Machine learning (ML) offers a complementary approach that can leverage large "
            "observational datasets to learn complex nonlinear relationships.",
            "1.1 Motivation",
            "The increasing availability of high-resolution satellite imagery, radiosonde data, "
            "and reanalysis products has created unprecedented opportunities for data-driven "
            "climate modeling. Neural networks trained on decades of observational data can "
            "potentially capture teleconnections and feedback mechanisms that are difficult "
            "to represent in first-principles models.",
            "1.2 Research Questions",
            "This thesis addresses the following research questions: (1) Can transformer-based "
            "architectures effectively encode long-range dependencies in global climate fields? "
            "(2) How can uncertainty be quantified in ML-based climate predictions? (3) What "
            "are the computational trade-offs between ML and NWP approaches at different scales?",
            "1.3 Thesis Organization",
            "Chapter 2 reviews related work in ML-based weather and climate prediction. "
            "Chapter 3 describes the observational datasets and preprocessing pipeline. "
            "Chapter 4 presents the proposed model architectures. Chapter 5 reports "
            "experimental results and comparative analyses. Chapter 6 concludes with "
            "directions for future research.",
        ]),
        (5, "Background", [
            "2.1 Numerical Weather Prediction",
            "Numerical weather prediction has been the operational backbone of meteorological "
            "services since the 1950s. The ECMWF Integrated Forecasting System (IFS) and "
            "NCEP's Global Forecast System (GFS) represent state-of-the-art NWP systems.",
            "2.2 Deep Learning for Earth Sciences",
            "Convolutional neural networks (CNNs) were among the first deep learning models "
            "applied to gridded climate data. Shi et al. (2015) introduced ConvLSTM for "
            "precipitation nowcasting, demonstrating that spatial CNN and temporal LSTM "
            "components could be effectively combined.",
        ]),
        (8, "Literature Review", [
            "3.1 Early Machine Learning Approaches",
            "The application of statistical and machine learning methods to atmospheric science "
            "dates back to the 1980s with the work of Lorenz on predictability limits and "
            "statistical post-processing of NWP output. Ensemble Kalman filtering (EnKF) "
            "incorporated statistical methods into data assimilation workflows by the 2000s.",
            "3.2 Graph Neural Networks for Climate",
            "Keisler (2022) introduced GraphCast, a graph neural network trained on ERA5 "
            "reanalysis data. By representing the Earth's surface as an icosahedral mesh, "
            "GraphCast achieves skillful 10-day forecasts at 0.25° resolution.",
            "Lam et al. (2023) extended this work with further architectural improvements, "
            "demonstrating that GNN-based models could outperform ECMWF HRES on 90% of "
            "test variables at forecast lead times beyond 5 days.",
            "3.3 Transformer Architectures",
            "The attention mechanism introduced by Vaswani et al. (2017) has transformed "
            "natural language processing and is increasingly applied to spatiotemporal data. "
            "Bi et al. (2023) presented Pangu-Weather, a 3D Earth-specific transformer "
            "that demonstrated superior performance on multiple forecast benchmarks.",
            "3.4 Diffusion Models for Ensemble Generation",
            "Score-based diffusion models have recently been applied to generate calibrated "
            "ensemble predictions. Price et al. (2023) introduced GenCast, a probabilistic "
            "medium-range forecast model based on denoising diffusion.",
            "3.5 Identified Research Gaps",
            "Despite rapid progress, several challenges remain: (1) Most models operate at "
            "coarse resolution (0.25°–1°) and lack downscaling capability; (2) uncertainty "
            "quantification in deterministic ML forecasts is underexplored; (3) physical "
            "consistency constraints are rarely enforced during training.",
        ]),
        (12, "Datasets and Preprocessing", [
            "4.1 ERA5 Reanalysis",
            "The primary dataset used in this study is the ERA5 global atmospheric reanalysis "
            "produced by ECMWF. ERA5 provides hourly data at 0.25° horizontal resolution "
            "for 137 pressure levels from 1940 to present.",
            "4.2 CMIP6 Projections",
            "We supplement ERA5 with outputs from 12 CMIP6 general circulation models to "
            "evaluate the generalization of ML models under climate change scenarios.",
            "4.3 Preprocessing Pipeline",
            "All input fields were normalized using climatological mean and standard deviation "
            "computed over the 1981–2010 baseline period. Spatial interpolation to a common "
            "1° × 1° grid was performed using bilinear remapping.",
        ]),
        (15, "Methodology", [
            "5.1 Model Architecture Overview",
            "We propose the Climate Transformer Network (CTN), a hierarchical architecture "
            "combining local convolutional feature extraction with global attention mechanisms.",
            "5.2 Encoder Design",
            "The encoder processes input climate fields as a sequence of patches. Each patch "
            "covers a 4° × 4° geographic region and all pressure levels, yielding a 3D tensor "
            "of shape (H/4, W/4, L, C) where H and W are the grid dimensions, L is the number "
            "of vertical levels, and C is the number of atmospheric variables.",
            "5.3 Attention Mechanism",
            "We employ a factored attention scheme: (1) spatial self-attention within each "
            "vertical column, (2) cross-level attention between pressure levels, and (3) "
            "temporal attention across the input sequence of 6-hourly analysis fields.",
            "5.4 Uncertainty Quantification",
            "Epistemic uncertainty is estimated through Monte Carlo dropout with dropout rate "
            "p=0.1 applied during both training and inference. Aleatoric uncertainty is "
            "modeled by predicting the parameters of a Gaussian distribution over each output.",
            "5.5 Training Procedure",
            "Models were trained on 4× NVIDIA A100 80GB GPUs using the AdamW optimizer with "
            "learning rate 1×10⁻⁴ and cosine annealing schedule over 100 epochs. The training "
            "set spans 1979–2017; validation covers 2018–2020; testing covers 2021–2023.",
            "5.6 Baseline Comparisons",
            "We compare CTN against: (1) ECMWF HRES operational forecast, (2) GraphCast "
            "(Lam et al., 2023), (3) Pangu-Weather (Bi et al., 2023), and (4) a standard "
            "U-Net baseline trained on the same data.",
        ]),
        (19, "Experimental Design", [
            "6.1 Evaluation Metrics",
            "Primary metrics include anomaly correlation coefficient (ACC), root mean square "
            "error (RMSE), and continuous ranked probability score (CRPS) for probabilistic "
            "forecasts. Metrics are computed separately for each forecast lead time (1–15 days).",
            "6.2 Ablation Studies",
            "We conduct ablation studies to quantify the contribution of each architectural "
            "component: (1) replacing factored attention with full self-attention, (2) "
            "removing the temporal attention module, (3) using a fixed dropout rate.",
            "6.3 Computational Budget",
            "Training CTN requires approximately 72 GPU-hours on 4× A100. Inference for "
            "a single 15-day forecast takes 45 seconds on a single A100.",
        ]),
        (22, "Validation Framework", [
            "7.1 Cross-validation Protocol",
            "To ensure fair comparison, all models are evaluated on the same held-out test "
            "period (2021–2023) with forecasts initialized at 00:00 UTC daily.",
            "7.2 Statistical Significance",
            "Improvements in skill score are assessed using the Diebold-Mariano test with "
            "Newey-West standard errors to account for temporal autocorrelation.",
            "7.3 Regional Analysis",
            "In addition to global metrics, we compute skill scores for six WMO regions to "
            "identify systematic biases and geographic patterns in model performance.",
        ]),
        (25, "Results", [
            "8.1 Global Forecast Skill",
            "Table 8.1 summarizes the ACC and RMSE for 500 hPa geopotential height (Z500), "
            "850 hPa temperature (T850), and 10 m wind speed (U10, V10) at day 5 and day 10.",
            "CTN achieves ACC of 0.927 for Z500 at day 5, compared to 0.921 for ECMWF HRES "
            "and 0.918 for GraphCast. At day 10, CTN maintains ACC of 0.751, compared to "
            "0.739 for ECMWF HRES.",
            "8.2 Temperature Prediction",
            "For 2 m temperature (T2M), CTN achieves RMSE of 1.42 K at day 3 forecast, a "
            "15% improvement over the U-Net baseline (1.67 K). Pangu-Weather achieves "
            "1.38 K, indicating that CTN approaches state-of-the-art performance.",
            "8.3 Precipitation Prediction",
            "Precipitation prediction remains challenging for all data-driven models. CTN "
            "achieves a CRPS of 2.14 mm/day for 24-hour accumulated precipitation, compared "
            "to 2.31 mm/day for ECMWF HRES ensemble mean.",
            "8.4 Uncertainty Calibration",
            "Figure 8.3 shows reliability diagrams for CTN probabilistic predictions. The "
            "model is well-calibrated for temperature and geopotential, with reliability "
            "diagrams close to the diagonal for all forecast lead times up to day 7.",
            "8.5 Extreme Events",
            "We evaluate model performance on 20 historical extreme weather events including "
            "tropical cyclones, heat waves, and extratropical cyclones. CTN correctly "
            "identifies 85% of events at day-5 lead time, compared to 79% for ECMWF HRES.",
            "8.6 Ablation Results",
            "Removing temporal attention reduces day-5 ACC from 0.927 to 0.914, confirming "
            "that multi-step temporal context is important for medium-range prediction.",
        ]),
        (30, "Analysis and Discussion", [
            "9.1 Physical Consistency",
            "A key concern with data-driven models is the potential violation of conservation "
            "laws. We assess mass conservation by computing the global mean surface pressure "
            "drift over 15-day integrations.",
            "CTN exhibits a mean surface pressure drift of 0.3 hPa after 15 days, substantially "
            "less than the U-Net baseline (1.2 hPa) but larger than ECMWF HRES (0.05 hPa).",
            "9.2 Bias Analysis",
            "Tropical precipitation is systematically underestimated by CTN in the ITCZ region. "
            "This likely reflects limitations of the ERA5 training data, which may itself "
            "contain biases in convection parameterization.",
            "9.3 Computational Efficiency",
            "CTN inference is approximately 1000× faster than ECMWF HRES on equivalent hardware. "
            "This enables applications such as large ensemble generation and rapid experimental "
            "forecasting that are computationally prohibitive with NWP.",
            "9.4 Limitations",
            "Current limitations include: (1) inability to assimilate new observations after "
            "training; (2) reduced skill for mesoscale phenomena below 100 km resolution; "
            "(3) potential distributional shift under novel climate states.",
        ]),
        (35, "Case Studies", [
            "10.1 Hurricane Ian (2022)",
            "Hurricane Ian made landfall in southwestern Florida on September 28, 2022 as "
            "a Category 4 hurricane. We evaluate CTN track and intensity forecasts initialized "
            "at 5-day lead time.",
            "CTN predicted landfall within 85 km of the actual location at day-5 lead, compared "
            "to a National Hurricane Center official track error of 120 km. Maximum wind speed "
            "intensity was predicted within 8 kt.",
            "10.2 European Heat Wave (August 2022)",
            "The August 2022 European heat wave produced record temperatures across France, "
            "Spain, and the United Kingdom. CTN T2M forecasts at 7-day lead captured the "
            "anomaly pattern with ACC of 0.89 over the European domain.",
            "10.3 Arctic Amplification Episode",
            "An extreme warming event in the Arctic stratosphere in January 2021 preceded "
            "a polar vortex disruption and subsequent cold air outbreaks. CTN predicted the "
            "stratospheric warming event 8 days in advance.",
        ]),
        (40, "Conclusion", [
            "11.1 Summary of Contributions",
            "This thesis has presented the Climate Transformer Network (CTN), a novel deep "
            "learning architecture for medium-range weather and climate prediction. Key "
            "contributions are summarized below.",
            "First, we introduced a factored attention mechanism that efficiently handles "
            "the 3D spatiotemporal structure of atmospheric fields, enabling global-scale "
            "modeling at competitive computational cost.",
            "Second, we developed an uncertainty quantification framework combining Monte "
            "Carlo dropout with distributional output heads, providing calibrated probabilistic "
            "forecasts.",
            "Third, CTN achieves state-of-the-art performance on multiple standard benchmarks, "
            "outperforming ECMWF HRES on 67% of evaluated metrics at 10-day lead time.",
            "11.2 Impact and Future Directions",
            "The results demonstrate that transformer-based architectures can learn complex "
            "climate dynamics from observational data alone, opening pathways for operational "
            "deployment of ML-based forecasting systems.",
            "Future work includes: (1) incorporating physical conservation constraints as "
            "soft regularization during training; (2) extending the model to seasonal "
            "prediction timescales; (3) coupling with land surface and ocean models; "
            "(4) developing hybrid ML-NWP systems that leverage the strengths of both approaches.",
            "11.3 Broader Implications",
            "Advances in ML-based climate prediction can contribute to improved disaster "
            "preparedness, more accurate climate projections, and ultimately more effective "
            "mitigation and adaptation policies.",
        ]),
        (43, "Future Work", [
            "12.1 Physical Hybrid Models",
            "A promising avenue is the development of physics-informed neural networks (PINNs) "
            "that enforce conservation laws as hard constraints during training.",
            "12.2 High-Resolution Downscaling",
            "Climate impacts at the local level require high-resolution information that "
            "global models cannot provide. Statistical downscaling with diffusion models "
            "could bridge this gap.",
            "12.3 Seasonal and Decadal Prediction",
            "Extending CTN to seasonal timescales requires incorporating ocean state initialization "
            "and longer temporal context windows.",
        ]),
        (45, "References", [
            "Bi, K., Xie, L., Zhang, H., Chen, X., Gu, X., & Tian, Q. (2023). Accurate medium-range "
            "global weather forecasting with 3D neural networks. Nature, 619, 533–538.",
            "Chen, L., Zhong, X., Zhang, F., Cheng, Y., Xu, Y., Qi, Y., & Li, H. (2023). FuXi: "
            "A cascade machine learning forecasting system for 15-day global weather forecast. "
            "npj Climate and Atmospheric Science, 6, 190.",
            "Keisler, R. (2022). Forecasting global weather with graph neural networks. "
            "arXiv preprint arXiv:2202.07575.",
            "Lam, R., Sanchez-Gonzalez, A., Willson, M., Wirnsberger, P., Fortunato, M., "
            "Alet, F., ... & Battaglia, P. (2023). Learning skillful medium-range global "
            "weather forecasting. Science, 382, 1416–1421.",
            "Nguyen, T., Brandstetter, J., Kapoor, A., Gupta, J. K., & Grover, A. (2023). "
            "ClimaX: A foundation model for weather and climate. arXiv:2301.10343.",
            "Price, I., Sanchez-Gonzalez, A., Alet, F., Andersson, T. R., El-Kadi, A., "
            "Masters, D., ... & Battaglia, P. (2023). GenCast: Diffusion-based ensemble "
            "weather forecasting. arXiv:2312.15796.",
            "Rasp, S., Dueben, P. D., Scher, S., Weyn, J. A., Mouatadid, S., & Thuerey, N. "
            "(2020). WeatherBench: A benchmark data set for data-driven weather forecasting. "
            "Journal of Advances in Modeling Earth Systems, 12, e2020MS002203.",
            "Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., "
            "... & Polosukhin, I. (2017). Attention is all you need. Advances in Neural "
            "Information Processing Systems, 30.",
            "Hersbach, H., Bell, B., Berrisford, P., Hirahara, S., Horányi, A., Muñoz-Sabater, "
            "J., ... & Thépaut, J. N. (2020). The ERA5 global reanalysis. Quarterly Journal "
            "of the Royal Meteorological Society, 146, 1999–2049.",
            "Pathak, J., Subramanian, S., Harrington, P., Raja, S., Chattopadhyay, A., "
            "Mardani, M., ... & Anandkumar, A. (2022). FourCastNet: A global data-driven "
            "high-resolution weather model using adaptive Fourier neural operators. "
            "arXiv:2202.11214.",
        ]),
        (48, "Appendix A: Model Hyperparameters", [
            "Table A.1: CTN Model Configuration",
            "Encoder patch size: 4° × 4°",
            "Number of transformer layers: 12",
            "Attention heads: 16",
            "Hidden dimension: 1024",
            "Feed-forward dimension: 4096",
            "Dropout rate: 0.1",
            "Input variables: Z500, T850, T2M, U10, V10, Q850, PSL (7 variables)",
            "Pressure levels: 13 (50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000 hPa)",
            "Input time steps: 4 (t, t-6h, t-12h, t-18h)",
            "Output lead times: 6h, 12h, ..., 15d (60 steps)",
            "",
            "Table A.2: Training Configuration",
            "Optimizer: AdamW (β₁=0.9, β₂=0.999, ε=1e-8)",
            "Learning rate: 1×10⁻⁴ with cosine annealing",
            "Weight decay: 0.05",
            "Batch size: 8 per GPU × 4 GPUs = 32 total",
            "Gradient clip: L2 norm ≤ 1.0",
            "Training epochs: 100",
            "Hardware: 4× NVIDIA A100 80GB SXM4",
        ]),
        (50, "Appendix B: Dataset Details", [
            "B.1 ERA5 Variables Used",
            "The following ERA5 fields were used as model inputs and outputs:",
            "Atmospheric fields (pressure levels): Geopotential (Z), Temperature (T), "
            "Specific humidity (Q), U-component of wind, V-component of wind.",
            "Surface fields: 2 m temperature, 10 m U-wind, 10 m V-wind, "
            "Mean sea level pressure, Total precipitation.",
            "B.2 Data Preprocessing",
            "All fields were regridded to 1° × 1° resolution (360 × 181 grid).",
            "Normalization: each variable standardized to zero mean, unit variance.",
            "Land-sea mask applied as an additional input channel.",
            "Missing data filled using nearest-neighbor interpolation.",
        ]),
    ]

    # Build page content map
    page_content = {}
    for start_page, section_title, paragraphs in sections:
        page_content[start_page] = (section_title, paragraphs)

    # Create 50-page document
    for page_idx in range(50):
        page_num = page_idx + 1
        page = doc.new_page(width=PAGE_W, height=PAGE_H)

        if page_num in page_content:
            section_title, paragraphs = page_content[page_num]
        else:
            # Find the most recent section
            section_title = "Content"
            paragraphs = []
            for sp in sorted(page_content.keys(), reverse=True):
                if sp <= page_num:
                    section_title, prev_paragraphs = page_content[sp]
                    # Generate continuation content
                    paragraphs = [
                        f"This section continues on page {page_num}.",
                        f"The detailed analysis of {section_title.lower()} includes additional "
                        f"quantitative results and qualitative discussion points that support "
                        f"the main findings presented on the preceding pages.",
                        "Further empirical evidence is provided through cross-validation "
                        "experiments conducted on independent test datasets spanning multiple "
                        "geographic regions and temporal periods.",
                        "Statistical analyses confirm the robustness of the reported improvements "
                        "with p-values below 0.01 for all primary metrics.",
                    ]
                    break

        # Insert content
        y_pos = 72

        # Section title (larger, bold-like)
        page.insert_text(
            pymupdf.Point(72, y_pos),
            section_title,
            fontsize=16,
            fontname="hebo",
            color=(0, 0, 0),
        )
        y_pos += 30

        # Body paragraphs
        for para in paragraphs:
            if not para:
                y_pos += 10
                continue
            # Word-wrap at ~80 chars per line equivalent
            rect = pymupdf.Rect(72, y_pos, PAGE_W - 72, y_pos + 200)
            excess = page.insert_textbox(
                rect,
                para,
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )
            # insert_textbox returns a float (negative = didn't fit fully)
            y_pos += min(max(30, len(para) // 8), 140)
            if y_pos > PAGE_H - 72:
                break

    # IMPORTANT: No metadata, no bookmarks, no page numbers, no watermarks
    # This is the raw state before the agent applies transformations
    doc.set_metadata({})  # Clear any default metadata

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Sanity check
    doc2 = pymupdf.open(OUTPUT)
    assert doc2.page_count == 50, f"Expected 50 pages, got {doc2.page_count}"
    meta = doc2.metadata
    assert not meta.get('title'), f"Should have no title metadata, got: {meta.get('title')}"
    assert not meta.get('author'), f"Should have no author metadata, got: {meta.get('author')}"
    toc = doc2.get_toc()
    assert len(toc) == 0, f"Should have no bookmarks, got: {len(toc)}"
    doc2.close()
    print('Sanity check passed: 50 pages, no metadata, no bookmarks')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
