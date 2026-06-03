"""
Initial Setup: Create an 85-page thesis PDF without headers
Task ID: pdf_res_062
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_062'
THESIS_DIR = f'{WORKDIR}/thesis'
OUTPUT = f'{THESIS_DIR}/long_thesis.pdf'

# Chapter structure: chapter_number -> (start_page_0indexed, title)
CHAPTERS = {
    1: (0, "Introduction to Climate Modeling"),
    2: (19, "Statistical Foundations of Machine Learning"),
    3: (39, "Deep Learning Architectures for Climate Data"),
    4: (59, "Experimental Results and Validation"),
    5: (74, "Conclusions and Future Directions"),
}

def get_chapter_for_page(page_idx):
    """Return chapter number for a given 0-indexed page."""
    for ch_num in sorted(CHAPTERS.keys(), reverse=True):
        if page_idx >= CHAPTERS[ch_num][0]:
            return ch_num
    return 1

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

def create_initial():
    os.makedirs(THESIS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Body text snippets for realistic content per chapter
    chapter_body_texts = {
        1: [
            "Climate change represents one of the most pressing challenges of our time. The interaction between atmospheric processes, ocean dynamics, and terrestrial ecosystems creates a complex system that defies simple analytical approaches.",
            "Traditional climate models rely on numerical solutions to partial differential equations governing fluid dynamics, thermodynamics, and radiative transfer. These models, known as General Circulation Models (GCMs), have been the backbone of climate science for decades.",
            "However, the computational cost of running high-resolution GCMs limits their practical application for long-term projections and ensemble studies. This has motivated researchers to explore machine learning as a complementary tool.",
            "In this thesis, we investigate how modern machine learning techniques can augment traditional climate modeling approaches, with particular emphasis on improving prediction accuracy while reducing computational overhead.",
        ],
        2: [
            "The mathematical foundations of machine learning rest upon statistical learning theory, optimization, and probability theory. Understanding these foundations is crucial for applying ML techniques to scientific domains.",
            "We begin with a review of supervised learning frameworks. Given a dataset D = {(x_i, y_i)}_{i=1}^{n}, the goal is to learn a function f: X -> Y that minimizes the expected risk R(f) = E[L(f(x), y)].",
            "Regularization techniques play a central role in preventing overfitting when dealing with high-dimensional climate data. L1 and L2 regularization, dropout, and early stopping each offer different tradeoffs.",
            "Bayesian approaches provide a principled framework for quantifying uncertainty in predictions, which is essential for climate projections where confidence intervals carry significant policy implications.",
        ],
        3: [
            "Deep neural networks have demonstrated remarkable capabilities in modeling complex nonlinear relationships. Convolutional neural networks (CNNs) excel at capturing spatial patterns in gridded climate data.",
            "Recurrent neural networks (RNNs), particularly Long Short-Term Memory (LSTM) networks, have shown promise in modeling temporal dependencies in climate time series spanning decades.",
            "The Transformer architecture, originally developed for natural language processing, has been adapted for spatiotemporal climate prediction through vision transformers and temporal attention mechanisms.",
            "Graph neural networks offer a natural framework for modeling climate data on irregular grids, such as ocean measurement stations and weather observation networks distributed across the globe.",
        ],
        4: [
            "Our experimental framework evaluates model performance across three benchmark datasets: ERA5 reanalysis data (1979-2023), CMIP6 model outputs, and station-based observational records from 15,000 weather stations.",
            "For temperature prediction, our hybrid CNN-LSTM architecture achieves a root mean squared error (RMSE) of 0.42 K on the ERA5 test set, compared to 0.67 K for the baseline persistence model.",
            "Precipitation forecasting remains more challenging due to its intermittent and spatially heterogeneous nature. Our attention-based model reduces the false alarm rate by 23% compared to conventional approaches.",
            "Cross-validation experiments demonstrate that models trained on reanalysis data transfer effectively to observational records, with degradation of less than 8% in skill scores across all metrics.",
        ],
        5: [
            "This thesis has demonstrated that machine learning techniques can significantly enhance climate prediction capabilities when integrated with domain knowledge from atmospheric science.",
            "Key contributions include: (1) a novel hybrid architecture combining physical constraints with data-driven learning, (2) a comprehensive benchmark suite for evaluating ML climate models, and (3) uncertainty quantification methods tailored for climate projections.",
            "Future work should focus on extending these approaches to coupled Earth system models, incorporating feedback mechanisms between atmosphere, ocean, cryosphere, and biosphere components.",
            "The code, trained models, and benchmark datasets developed in this thesis are publicly available to support reproducibility and further research in the growing field of AI for climate science.",
        ],
    }

    section_titles_per_chapter = {
        1: ["1.1 Motivation and Background", "1.2 Climate System Overview", "1.3 Computational Challenges", "1.4 Thesis Structure and Contributions"],
        2: ["2.1 Supervised Learning Theory", "2.2 Regularization Methods", "2.3 Bayesian Inference", "2.4 Model Selection and Validation"],
        3: ["3.1 Convolutional Networks for Spatial Data", "3.2 Recurrent Networks for Temporal Modeling", "3.3 Transformer Architectures", "3.4 Graph Neural Networks"],
        4: ["4.1 Experimental Setup and Datasets", "4.2 Temperature Prediction Results", "4.3 Precipitation Forecasting", "4.4 Transfer Learning Experiments"],
        5: ["5.1 Summary of Contributions", "5.2 Limitations", "5.3 Future Research Directions", "5.4 Open-Source Resources"],
    }

    for page_idx in range(85):
        page = doc.new_page(width=595, height=842)  # A4
        ch_num = get_chapter_for_page(page_idx)
        ch_start = CHAPTERS[ch_num][0]
        ch_title = CHAPTERS[ch_num][1]
        page_in_chapter = page_idx - ch_start

        # First page of chapter: chapter title page
        if page_idx == ch_start:
            # Chapter heading
            page.insert_text(
                pymupdf.Point(72, 200),
                f"Chapter {ch_num}",
                fontsize=28,
                fontname="hebo",
                color=(0, 0, 0),
            )
            page.insert_text(
                pymupdf.Point(72, 250),
                ch_title,
                fontsize=20,
                fontname="helv",
                color=(0.2, 0.2, 0.2),
            )
            # Decorative line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 270), pymupdf.Point(523, 270))
            shape.finish(color=(0.3, 0.3, 0.3), width=1.5)
            shape.commit()

            # Brief intro paragraph
            bodies = chapter_body_texts[ch_num]
            rect = pymupdf.Rect(72, 310, 523, 750)
            page.insert_textbox(
                rect,
                bodies[0],
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )
        else:
            # Regular content pages
            sections = section_titles_per_chapter[ch_num]
            bodies = chapter_body_texts[ch_num]

            y_pos = 72  # top margin (NO header in initial)

            # Determine which section to show on this page
            section_idx = min(page_in_chapter - 1, len(sections) - 1)
            if section_idx >= 0 and page_in_chapter <= len(sections):
                # Section heading
                page.insert_text(
                    pymupdf.Point(72, y_pos + 20),
                    sections[section_idx],
                    fontsize=14,
                    fontname="hebo",
                    color=(0.1, 0.1, 0.1),
                )
                y_pos += 45

            # Body text - fill the page with realistic content
            body_idx = page_in_chapter % len(bodies)
            text_block = bodies[body_idx]

            # Repeat/vary text to fill the page
            full_text = ""
            for i in range(6):
                para_idx = (body_idx + i) % len(bodies)
                full_text += bodies[para_idx] + "\n\n"

            rect = pymupdf.Rect(72, y_pos, 523, 790)
            page.insert_textbox(
                rect,
                full_text.strip(),
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

        # Page number at bottom center
        page.insert_text(
            pymupdf.Point(280, 820),
            str(page_idx + 1),
            fontsize=10,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open PDF in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')

create_initial()
