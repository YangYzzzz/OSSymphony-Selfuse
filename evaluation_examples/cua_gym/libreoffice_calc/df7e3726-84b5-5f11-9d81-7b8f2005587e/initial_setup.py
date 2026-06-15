"""
Initial Setup: Create 80-page dissertation PDF with bookmarks for Chapters 1-7
Task ID: pdf_fm_030
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_030'
OUTPUT_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{OUTPUT_DIR}/dissertation.pdf'

# Page dimensions (Letter size)
W, H = 612, 792
MARGIN = 72
TEXT_W = W - 2 * MARGIN

# Chapter structure: (title, start_page_1indexed, num_pages)
# Total pages = 80
CHAPTERS = [
    ("Chapter 1: Introduction", 1, 8),
    ("Chapter 2: Literature Review", 9, 12),
    ("Chapter 3: Methodology", 21, 14),
    ("Chapter 4: Data Collection", 35, 17),
    ("Chapter 5: Results", 52, 12),
    ("Chapter 6: Discussion", 64, 10),
    ("Chapter 7: Conclusions", 74, 7),
]
# Total = 8+12+14+17+12+10+7 = 80

# Realistic dissertation content per chapter
CHAPTER_CONTENT = {
    "Chapter 1: Introduction": [
        "The rapid advancement of machine learning technologies has fundamentally transformed how organizations approach complex decision-making processes across multiple industries.",
        "Over the past decade, researchers have documented significant improvements in predictive accuracy when applying deep neural network architectures to structured datasets with temporal dependencies.",
        "This dissertation investigates the application of transformer-based models to financial time series forecasting, with particular emphasis on volatility prediction in emerging market equities.",
        "The motivation for this research stems from the observation that traditional econometric models, while theoretically grounded, often fail to capture non-linear dependencies present in high-frequency financial data.",
        "Our primary research questions address three fundamental gaps in the existing literature: first, whether attention mechanisms can effectively model long-range dependencies in daily return series; second, how multi-scale feature extraction improves forecast accuracy; and third, what role data augmentation plays in mitigating overfitting in small-sample regimes.",
        "The significance of this work extends beyond academic interest, as improved volatility forecasts have direct implications for portfolio risk management, derivatives pricing, and regulatory capital allocation.",
        "We adopt a mixed-methods approach combining quantitative model development with qualitative analysis of model interpretability, providing insights into the economic mechanisms captured by learned representations.",
        "The remainder of this dissertation is organized as follows: Chapter 2 reviews the relevant literature, Chapter 3 describes our methodology, Chapter 4 details the data collection process, Chapter 5 presents our experimental results, Chapter 6 discusses the implications, and Chapter 7 concludes with recommendations for future research.",
    ],
    "Chapter 2: Literature Review": [
        "The literature on financial time series forecasting spans several decades and encompasses contributions from econometrics, statistics, and computer science.",
        "Early work by Engle (1982) introduced the ARCH family of models, which captured time-varying volatility through autoregressive conditional heteroskedasticity specifications.",
        "Bollerslev (1986) extended this framework with the Generalized ARCH model, which remains one of the most widely used volatility models in both academic research and industry practice.",
        "The application of neural networks to financial prediction dates back to the 1990s, with White (1988) providing early evidence of nonlinear predictability in stock returns using feedforward architectures.",
        "More recently, recurrent neural networks, particularly Long Short-Term Memory networks proposed by Hochreiter and Schmidhuber (1997), have shown promise in capturing temporal dependencies in sequential financial data.",
        "The attention mechanism, originally developed for machine translation by Bahdanau et al. (2014), represented a paradigm shift in sequence modeling by allowing models to selectively focus on relevant portions of input sequences.",
        "Vaswani et al. (2017) introduced the Transformer architecture, which relies entirely on self-attention and has since become the dominant approach in natural language processing and is increasingly applied to time series tasks.",
        "Several studies have applied transformer variants to financial forecasting, including the Temporal Fusion Transformer by Lim et al. (2021) and the Autoformer by Wu et al. (2021).",
        "Despite these advances, a comprehensive comparison of transformer architectures for emerging market volatility prediction remains absent from the literature.",
        "Our work addresses this gap by systematically evaluating multiple transformer variants against traditional benchmarks across a diverse set of emerging market indices.",
        "The concept of transfer learning, widely successful in computer vision and NLP, has received limited attention in financial forecasting due to concerns about regime changes and market microstructure differences.",
        "We review the growing body of work on data augmentation for time series, including window slicing, jittering, and synthetic data generation through generative adversarial networks.",
    ],
    "Chapter 3: Methodology": [
        "This chapter describes our methodological framework, including the model architectures evaluated, the training procedures employed, and the evaluation metrics used to assess forecast quality.",
        "We implement five model variants: a vanilla Transformer encoder, a Temporal Fusion Transformer (TFT), an Informer with ProbSparse attention, a standard LSTM baseline, and a GARCH(1,1) econometric baseline.",
        "All deep learning models share a common preprocessing pipeline that includes logarithmic transformation of returns, z-score normalization using rolling 252-day windows, and feature engineering based on established technical indicators.",
        "The input feature set comprises 23 variables organized into four categories: price-derived features (returns, realized volatility, range), volume-based indicators (volume ratio, on-balance volume), market microstructure proxies (bid-ask spread estimates, Amihud illiquidity), and macroeconomic factors (interest rate differentials, commodity prices, VIX).",
        "We employ a walk-forward validation scheme with expanding training windows, where models are retrained every 63 trading days (approximately one quarter) to account for potential distributional shifts.",
        "Hyperparameter optimization follows a two-stage approach: initial Bayesian optimization using Tree-structured Parzen Estimators over a coarse grid, followed by fine-tuning of the top three configurations via grid search.",
        "The Transformer encoder uses 4 attention heads, 3 encoder layers, a model dimension of 128, and a feedforward dimension of 512, with dropout rate of 0.1 applied to both attention weights and feedforward layers.",
        "Training uses the Adam optimizer with a learning rate of 1e-4, weight decay of 1e-5, and a cosine annealing schedule with warm restarts every 50 epochs.",
        "Our loss function combines mean squared error for point forecasts with a quantile regression component at the 5th, 25th, 75th, and 95th percentiles to capture the full forecast distribution.",
        "Model interpretability analysis leverages integrated gradients attribution, attention weight visualization, and SHAP values computed on a representative test subset.",
        "We implement all models in PyTorch 2.0 with mixed-precision training on NVIDIA A100 GPUs, achieving training times between 45 minutes and 3 hours depending on model complexity.",
        "Statistical significance of performance differences is assessed using the Model Confidence Set procedure of Hansen et al. (2011) and the Diebold-Mariano test with Newey-West heteroskedasticity-robust standard errors.",
        "To ensure reproducibility, all experiments use fixed random seeds, and our complete codebase is available in the supplementary materials.",
        "We additionally perform ablation studies removing individual feature groups and attention components to quantify their marginal contributions to forecast accuracy.",
    ],
    "Chapter 4: Data Collection": [
        "This chapter details the data sources, sample construction, and quality assurance procedures used to assemble our empirical dataset.",
        "We collect daily closing prices, trading volumes, and bid-ask quotes for equity indices from 15 emerging market countries spanning the period January 2005 through December 2023.",
        "The sample countries include Brazil (Bovespa), China (CSI 300), India (Nifty 50), Indonesia (JCI), Malaysia (KLCI), Mexico (IPC), Nigeria (ASI), Pakistan (KSE-100), Philippines (PSEi), Poland (WIG 20), Russia (MOEX, until February 2022), South Africa (JSE Top 40), South Korea (KOSPI), Thailand (SET), and Turkey (BIST 100).",
        "Price data is sourced from Bloomberg Terminal and cross-validated against Refinitiv Eikon to identify and correct discrepancies, with a match rate of 99.87% across all index-date observations.",
        "Macroeconomic control variables are obtained from the Federal Reserve Economic Data (FRED) database, the International Monetary Fund's International Financial Statistics, and the Bank for International Settlements.",
        "We compute realized volatility using the Parkinson (1980) high-low range estimator, which is more efficient than close-to-close estimators for daily data and robust to market microstructure noise.",
        "Missing data treatment follows a three-step protocol: first, we interpolate isolated missing values (fewer than 3 consecutive days) using cubic spline interpolation; second, we exclude extended gaps (more than 10 consecutive trading days, typically due to market closures or political crises); third, we verify that remaining gaps do not systematically bias our sample.",
        "The final cleaned dataset comprises 69,847 index-day observations with 23 features each, resulting in approximately 1.6 million individual data points.",
        "Table 4.1 presents summary statistics for each market, including average daily returns, annualized volatility, skewness, kurtosis, and the percentage of trading days with absolute returns exceeding two standard deviations.",
        "We observe substantial cross-sectional variation in volatility levels, ranging from 12.3% annualized for Malaysia to 38.7% for Turkey, confirming the heterogeneity that motivates our multi-market analysis.",
        "The correlation structure among emerging market returns exhibits time-varying properties, with average pairwise correlations increasing from 0.31 during calm periods to 0.67 during global stress episodes such as the 2008 financial crisis and the 2020 COVID-19 pandemic.",
        "We split the data chronologically: 2005-2017 for training (approximately 60%), 2018-2020 for validation (approximately 20%), and 2021-2023 for out-of-sample testing (approximately 20%).",
        "This split ensures that the test period includes both normal market conditions and the post-pandemic recovery, providing a rigorous evaluation environment.",
        "Feature engineering produces 23 model inputs per observation, with each feature standardized using only information available at the time of prediction to prevent look-ahead bias.",
        "We conduct stationarity tests using the Augmented Dickey-Fuller test and KPSS test, confirming that all return series and derived features are stationary at the 1% significance level.",
        "Data quality checks reveal 127 suspected data errors across the full sample, all of which were manually verified and corrected using primary exchange records.",
        "The computational infrastructure for data processing consists of a PostgreSQL database for raw data storage and a Python-based ETL pipeline using pandas and Dask for parallel feature computation.",
    ],
    "Chapter 5: Results": [
        "This chapter presents the experimental results obtained from our three-phase study.",
        "Phase one evaluates point forecast accuracy across all 15 emerging markets using root mean squared error (RMSE), mean absolute error (MAE), and the quasi-likelihood loss function appropriate for volatility forecasts.",
        "Table 5.1 reports the out-of-sample RMSE for each model-market combination, with bold values indicating the best-performing model for each market.",
        "The Temporal Fusion Transformer achieves the lowest average RMSE of 0.0234 across all markets, representing a 14.7% improvement over the GARCH(1,1) baseline (RMSE = 0.0274) and a 6.8% improvement over the standard LSTM (RMSE = 0.0251).",
        "The vanilla Transformer encoder ranks second with an average RMSE of 0.0241, while the Informer variant shows comparable performance at 0.0243 but with significantly faster inference times due to its ProbSparse attention mechanism.",
        "Figure 5.1 presents a heatmap of relative model performance across markets, revealing that the TFT's advantage is most pronounced in high-volatility markets such as Turkey, Nigeria, and Pakistan.",
        "In contrast, the GARCH model remains competitive in lower-volatility, more liquid markets like South Korea and Malaysia, where linear volatility dynamics appear sufficient.",
        "Phase two examines density forecast calibration using the probability integral transform (PIT) and the Berkowitz likelihood ratio test.",
        "The TFT produces the best-calibrated predictive distributions, with PIT uniformity p-values exceeding 0.05 for 13 out of 15 markets, compared to 9 for the LSTM and only 4 for GARCH.",
        "Phase three investigates the economic significance of forecast improvements through a simple volatility-timing trading strategy that adjusts equity exposure inversely to predicted next-day volatility.",
        "The TFT-based strategy generates an annualized Sharpe ratio of 0.87 across the pooled emerging market portfolio, compared to 0.72 for LSTM-based and 0.61 for GARCH-based strategies.",
        "After accounting for realistic transaction costs of 20 basis points per trade, the TFT strategy retains a Sharpe ratio of 0.74, with statistically significant alpha of 3.2% per annum relative to a buy-and-hold benchmark.",
    ],
    "Chapter 6: Discussion": [
        "This chapter interprets our empirical findings in the context of existing literature and discusses their theoretical and practical implications.",
        "The superior performance of the Temporal Fusion Transformer aligns with recent evidence that attention-based architectures excel at capturing complex temporal dependencies in financial data.",
        "Our interpretability analysis reveals that the TFT assigns highest attention weights to realized volatility features at lags 1, 5, and 21 trading days, corresponding to daily, weekly, and monthly volatility cycles documented in the market microstructure literature.",
        "The variable selection network within the TFT identifies the VIX and US 10-year Treasury yield as the most important cross-market features, consistent with the well-documented role of US monetary conditions in driving emerging market risk sentiment.",
        "Interestingly, volume-based features receive relatively low importance weights across most markets, suggesting that price-based information subsumes the predictive content of trading activity for daily volatility forecasting.",
        "The finding that GARCH remains competitive in low-volatility markets supports a nuanced view of model selection: the additional complexity of deep learning models is most justified when the data-generating process exhibits strong non-linearities and regime changes.",
        "Our results have practical implications for risk management in emerging market portfolios, where accurate volatility forecasts are critical for Value-at-Risk calculations and dynamic hedging strategies.",
        "The economic significance results demonstrate that statistical improvements in forecast accuracy translate to meaningful financial gains, addressing a common criticism that academic forecast improvements lack practical relevance.",
        "We acknowledge several limitations: our analysis focuses on daily frequency and may not generalize to intraday or monthly horizons; the training data period includes several extraordinary market events that may inflate apparent model performance; and the transaction cost assumptions may not reflect actual implementation costs in less liquid emerging markets.",
        "Future research could extend our framework to incorporate alternative data sources such as satellite imagery, social media sentiment, and corporate filing text, which have shown promise in related prediction tasks.",
    ],
    "Chapter 7: Conclusions": [
        "This dissertation has presented a comprehensive evaluation of transformer-based models for volatility prediction in emerging market equities.",
        "Our principal finding is that the Temporal Fusion Transformer consistently outperforms both traditional econometric models and simpler deep learning architectures across a diverse set of 15 emerging markets over an 18-year sample period.",
        "The magnitude of improvement is economically meaningful, with the TFT-based trading strategy generating approximately 3.2% additional annual returns after transaction costs relative to buy-and-hold benchmarks.",
        "Three key contributions emerge from this work: first, we establish that attention mechanisms effectively capture the multi-scale temporal dynamics of emerging market volatility; second, we demonstrate that model interpretability tools can identify economically meaningful feature importance patterns; third, we show that walk-forward validation with periodic retraining is essential for maintaining forecast accuracy in non-stationary financial environments.",
        "Based on our findings, we recommend that practitioners considering deep learning for volatility forecasting begin with the TFT architecture as a strong default choice, particularly for markets exhibiting high volatility and non-linear dynamics.",
        "For lower-complexity markets, a GARCH(1,1) model may suffice and offers advantages in terms of computational efficiency, interpretability, and regulatory acceptance.",
        "Future research directions include extending the analysis to intraday frequencies, incorporating alternative data sources, investigating transfer learning across markets, and developing ensemble methods that combine the strengths of econometric and deep learning approaches.",
    ],
}


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


def create_dissertation():
    """Create an 80-page dissertation PDF with bookmarks."""
    doc = pymupdf.open()

    # Build a mapping: page_index -> (chapter_title, is_first_page_of_chapter)
    page_chapter_map = {}
    for title, start_page, num_pages in CHAPTERS:
        for p in range(num_pages):
            page_idx = start_page - 1 + p
            page_chapter_map[page_idx] = (title, p == 0)

    # Create all 80 pages
    for page_idx in range(80):
        page = doc.new_page(width=W, height=H)
        chapter_title, is_chapter_start = page_chapter_map.get(page_idx, ("", False))

        y = MARGIN

        if is_chapter_start:
            # Chapter title
            y += 30
            page.insert_text(
                pymupdf.Point(MARGIN, y),
                chapter_title,
                fontsize=20,
                fontname="hebo",
                color=(0, 0, 0.4),
            )
            y += 40

            # Horizontal rule
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(MARGIN, y), pymupdf.Point(W - MARGIN, y))
            shape.finish(color=(0.3, 0.3, 0.3), width=1.5)
            shape.commit()
            y += 20

            # Chapter content paragraphs
            paragraphs = CHAPTER_CONTENT.get(chapter_title, [])
            for i, para in enumerate(paragraphs):
                if y > H - MARGIN - 60:
                    break
                rect = pymupdf.Rect(MARGIN, y, W - MARGIN, H - MARGIN)
                excess = page.insert_textbox(
                    rect,
                    para,
                    fontsize=11,
                    fontname="tiro",
                    color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )
                # Estimate height used: count lines roughly
                lines_needed = max(1, len(para) / 75)
                y += lines_needed * 15 + 12
        else:
            # Continuation pages: generate filler academic text
            page_in_chapter = page_idx - next(
                s - 1 for t, s, n in CHAPTERS
                if s - 1 <= page_idx < s - 1 + n
            )
            section_num = page_in_chapter // 2 + 1

            # Section header on some pages
            if page_in_chapter > 0 and page_in_chapter % 3 == 0:
                ch_num = chapter_title.split(":")[0].replace("Chapter ", "") if chapter_title else ""
                page.insert_text(
                    pymupdf.Point(MARGIN, y + 15),
                    f"{ch_num}.{section_num} Analysis of Subsection {section_num}",
                    fontsize=14,
                    fontname="hebo",
                    color=(0, 0, 0.3),
                )
                y += 40

            # Fill with realistic academic prose
            filler_paragraphs = _generate_filler(page_idx, chapter_title)
            for para in filler_paragraphs:
                if y > H - MARGIN - 40:
                    break
                rect = pymupdf.Rect(MARGIN, y, W - MARGIN, H - MARGIN - 20)
                page.insert_textbox(
                    rect,
                    para,
                    fontsize=11,
                    fontname="tiro",
                    color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )
                lines_needed = max(1, len(para) / 75)
                y += lines_needed * 15 + 10

        # Page number at bottom center
        page.insert_text(
            pymupdf.Point(W / 2 - 10, H - 40),
            str(page_idx + 1),
            fontsize=10,
            fontname="tiro",
            color=(0.4, 0.4, 0.4),
        )

    # Set Table of Contents (bookmarks)
    toc = []
    for title, start_page, _ in CHAPTERS:
        toc.append([1, title, start_page])
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "Transformer-Based Volatility Prediction in Emerging Market Equities",
        "author": "Alexandra M. Richardson",
        "subject": "Doctoral Dissertation - Department of Finance",
        "keywords": "machine learning, volatility forecasting, transformers, emerging markets",
        "creator": "LaTeX with hyperref",
        "producer": "pdfTeX-1.40.25",
    })

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: 80')


def _generate_filler(page_idx, chapter_title):
    """Generate realistic filler paragraphs for non-first chapter pages."""
    fillers = [
        [
            "The analysis of cross-sectional variation reveals substantial heterogeneity in model performance across different market regimes and economic conditions.",
            "We observe that models trained with multi-scale feature extraction consistently outperform single-scale alternatives, with improvements ranging from 3.2% to 11.8% depending on the market.",
            "The statistical significance of these differences was confirmed using the Hansen Model Confidence Set procedure at the 10% significance level.",
            "Robustness checks using alternative volatility proxies, including the Garman-Klass estimator and five-minute realized variance where available, produce qualitatively similar rankings.",
        ],
        [
            "The temporal evolution of forecast errors reveals interesting patterns related to market regime transitions and structural breaks in the underlying data-generating process.",
            "During the COVID-19 market crash of March 2020, all models experienced a significant deterioration in forecast accuracy, with RMSE values increasing by factors of 2.5 to 4.7 relative to pre-crisis levels.",
            "However, the recovery speed differed markedly across model classes: the TFT adapted within approximately 15 trading days, while the GARCH model required over 40 days to return to pre-crisis error levels.",
            "This adaptive advantage of attention-based models likely reflects their ability to rapidly re-weight feature importance in response to changing market dynamics.",
        ],
        [
            "The feature importance analysis provides valuable insights into which economic variables drive model predictions across different market environments.",
            "Realized volatility at the daily lag consistently emerges as the single most important predictor, accounting for approximately 35% of total variable importance across all transformer models.",
            "The VIX index and US dollar exchange rate movements rank second and third, respectively, highlighting the central role of global risk factors in determining emerging market volatility dynamics.",
            "Domestic factors, including local interest rates and commodity price indices, show elevated importance only for specific country groups, particularly commodity-exporting nations.",
        ],
        [
            "Additional sensitivity analysis examines the impact of lookback window length on model performance, testing windows of 20, 60, 120, and 252 trading days.",
            "The optimal window length varies across markets but generally falls in the 60-120 day range, balancing the tradeoff between capturing recent dynamics and maintaining sufficient training signal.",
            "Ensemble methods combining predictions from multiple window lengths yield a modest further improvement of approximately 1.5% in average RMSE, suggesting complementary information across temporal scales.",
            "We note that the computational overhead of maintaining multiple windows is non-trivial and may not be justified in production environments where inference latency is a binding constraint.",
        ],
        [
            "The distributional analysis of forecast residuals provides additional evidence regarding model adequacy and potential areas for improvement.",
            "Kolmogorov-Smirnov tests reject the null hypothesis of normally distributed residuals for all model-market combinations at the 1% significance level, indicating persistent non-Gaussian features.",
            "However, the degree of non-normality, as measured by excess kurtosis, is substantially reduced for transformer-based models compared to GARCH, suggesting better tail risk capture.",
            "Quantile regression diagnostics confirm that the TFT produces well-calibrated predictive intervals, with empirical coverage rates within 2 percentage points of nominal levels for the 90% and 95% intervals.",
        ],
        [
            "A comparison of training efficiency across model architectures reveals important practical considerations for deployment in resource-constrained environments.",
            "The GARCH model requires less than one second for parameter estimation per market, making it suitable for real-time applications with hundreds of instruments.",
            "The LSTM trains in approximately 12 minutes on a single GPU, while the TFT requires approximately 45 minutes due to its more complex architecture and variable selection network.",
            "Inference time differences are less pronounced, with all deep learning models generating forecasts in under 50 milliseconds per observation on GPU hardware.",
        ],
        [
            "The economic analysis extends beyond simple Sharpe ratio comparisons to examine risk-adjusted performance under realistic portfolio constraints.",
            "Maximum drawdown analysis reveals that the TFT-based strategy experiences a worst-case drawdown of 18.3% during the 2020 crisis, compared to 25.7% for the buy-and-hold benchmark.",
            "This improved downside protection is particularly valuable for institutional investors subject to regulatory capital requirements or maximum loss constraints.",
            "The turnover analysis indicates average monthly portfolio turnover of 34% for the TFT strategy, resulting in annualized transaction costs of approximately 68 basis points under our assumptions.",
        ],
        [
            "Cross-validation of our results using alternative performance metrics reinforces the main conclusions regarding model rankings.",
            "The mean directional accuracy (MDA) of volatility forecasts ranges from 54.2% for GARCH to 61.8% for TFT, with all deep learning models significantly outperforming the coin-flip benchmark at the 1% level.",
            "The quasi-likelihood (QLIKE) loss function, which is robust to noise in the volatility proxy, produces identical model rankings to RMSE for all markets except South Korea.",
            "Information ratio analysis, which adjusts for tracking error relative to a constant-volatility benchmark, further confirms the TFT's dominance with an average information ratio of 0.93.",
        ],
    ]

    idx = page_idx % len(fillers)
    return fillers[idx]


def main():
    create_dissertation()

    # Launch Okular with the PDF (task specifies Okular)
    try:
        launch_gui(f'okular "{OUTPUT}"', delay_sec=2.0)
        print('GUI_READY: launched Okular with DISPLAY=:0')
    except Exception as e:
        print(f'Okular launch failed ({e}), falling back to evince')
        launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
        print('GUI_READY: launched evince with DISPLAY=:0')


main()
