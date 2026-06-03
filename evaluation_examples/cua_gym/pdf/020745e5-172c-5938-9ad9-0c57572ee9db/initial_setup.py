"""
Initial Setup: PDF Document Assembly Tool
Task ID: pdf_aw_050
Domain: pdf
Creates source PDFs in /home/user/assembly/ for assembly task.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_050'
ASSEMBLY_DIR = f'{WORKDIR}/assembly'

# Chapter metadata: (title, num_pages, topic_sentences)
CHAPTERS = [
    ("Chapter 1: Foundations of Data Analysis", 12, [
        "Data analysis begins with understanding the fundamental types of data one encounters in practice.",
        "Quantitative data can be further divided into discrete and continuous measurements.",
        "The process of data cleaning involves identifying and correcting errors, filling missing values, and standardizing formats.",
        "Exploratory data analysis (EDA) provides initial insights through summary statistics and visualization.",
        "Descriptive statistics such as mean, median, mode, and standard deviation form the backbone of initial analysis.",
        "Data distributions reveal the underlying patterns, whether normal, skewed, or multimodal.",
        "Sampling techniques ensure that analysis results generalize to the broader population.",
        "The concept of statistical significance helps distinguish genuine patterns from random noise.",
        "Correlation analysis measures the strength and direction of relationships between variables.",
        "Hypothesis testing provides a formal framework for drawing conclusions from sample data.",
        "Confidence intervals quantify the uncertainty inherent in any statistical estimate.",
        "The foundation laid in this chapter prepares the reader for more advanced analytical techniques.",
    ]),
    ("Chapter 2: Statistical Methods and Inference", 15, [
        "Statistical inference allows us to draw conclusions about populations from sample observations.",
        "The central limit theorem is one of the most important results in probability theory.",
        "Parametric tests assume specific distributional forms, typically normal distributions.",
        "Non-parametric methods provide alternatives when distributional assumptions are violated.",
        "Analysis of variance (ANOVA) extends the two-sample t-test to multiple group comparisons.",
        "Regression analysis models the relationship between dependent and independent variables.",
        "Multiple regression accounts for the simultaneous influence of several predictor variables.",
        "Logistic regression handles binary outcomes, widely used in classification problems.",
        "Time series analysis captures temporal patterns including trends, seasonality, and cycles.",
        "Bayesian statistics offers an alternative framework incorporating prior knowledge.",
        "The likelihood principle provides a unifying concept across different statistical paradigms.",
        "Model selection criteria such as AIC and BIC balance goodness of fit with model complexity.",
        "Cross-validation techniques estimate how well a model will perform on unseen data.",
        "Bootstrap methods provide distribution-free inference through resampling.",
        "The interplay between frequentist and Bayesian approaches enriches modern statistical practice.",
    ]),
    ("Chapter 3: Machine Learning Fundamentals", 10, [
        "Machine learning automates pattern recognition and predictive modeling from data.",
        "Supervised learning uses labeled examples to train models for classification and regression.",
        "Decision trees partition the feature space through a series of hierarchical splits.",
        "Ensemble methods like random forests and gradient boosting combine multiple weak learners.",
        "Support vector machines find optimal hyperplanes that maximize the margin between classes.",
        "Neural networks are composed of interconnected layers of artificial neurons.",
        "Unsupervised learning discovers hidden structure in data without explicit labels.",
        "Clustering algorithms such as k-means and DBSCAN group similar data points together.",
        "Dimensionality reduction techniques like PCA compress high-dimensional data while preserving variance.",
        "The bias-variance tradeoff is a central concept in understanding model generalization.",
    ]),
    ("Chapter 4: Data Visualization Principles", 8, [
        "Effective data visualization transforms complex datasets into comprehensible visual narratives.",
        "The choice of chart type depends on the nature of the data and the message to convey.",
        "Color theory plays a crucial role in creating accessible and informative visualizations.",
        "Edward Tufte's principles of data-ink ratio guide the design of elegant graphics.",
        "Interactive visualizations enable exploration of multidimensional datasets.",
        "Geographic data visualization requires careful handling of projections and spatial relationships.",
        "Dashboard design integrates multiple views to provide comprehensive analytical overviews.",
        "The ethics of visualization demand honest representation without misleading distortions.",
    ]),
    ("Chapter 5: Applied Analytics and Case Studies", 18, [
        "Real-world analytics projects require careful scoping, data acquisition, and stakeholder management.",
        "Healthcare analytics leverages patient records to improve treatment outcomes and resource allocation.",
        "Financial analytics encompasses risk modeling, fraud detection, and algorithmic trading strategies.",
        "Marketing analytics uses customer segmentation and attribution modeling to optimize campaigns.",
        "Supply chain analytics improves demand forecasting, inventory management, and logistics optimization.",
        "Natural language processing extracts insights from unstructured text data at scale.",
        "Computer vision applications range from medical imaging to autonomous vehicle navigation.",
        "A/B testing provides a rigorous framework for evaluating changes in products and services.",
        "Recommendation systems power personalized experiences across e-commerce and media platforms.",
        "Ethical considerations in analytics include privacy, fairness, transparency, and accountability.",
        "The data science lifecycle encompasses problem definition through deployment and monitoring.",
        "Feature engineering transforms raw data into informative representations for model training.",
        "Model deployment requires attention to scalability, latency, and monitoring infrastructure.",
        "Regulatory compliance shapes analytics practices in healthcare, finance, and government sectors.",
        "The future of analytics lies in automated machine learning and augmented decision-making.",
        "Edge computing brings analytical capabilities closer to data sources for real-time processing.",
        "Federated learning enables collaborative model training while preserving data privacy.",
        "This capstone chapter demonstrates how theoretical foundations translate into practical impact.",
    ]),
]


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


def create_cover_pdf(path):
    """Create a 1-page cover PDF."""
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)

    # Title
    page.insert_text(
        pymupdf.Point(297, 250),
        "DATA ANALYTICS",
        fontsize=36,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )
    # Adjust centering by drawing centered
    rect = pymupdf.Rect(72, 220, 523, 280)
    page.insert_textbox(rect, "DATA ANALYTICS", fontsize=36, fontname="hebo",
                        color=(0.1, 0.1, 0.4), align=pymupdf.TEXT_ALIGN_CENTER)

    rect2 = pymupdf.Rect(72, 290, 523, 340)
    page.insert_textbox(rect2, "A Comprehensive Guide", fontsize=20, fontname="tiit",
                        color=(0.3, 0.3, 0.3), align=pymupdf.TEXT_ALIGN_CENTER)

    # Author
    rect3 = pymupdf.Rect(72, 500, 523, 540)
    page.insert_textbox(rect3, "Dr. Elena Vasquez & Prof. James Thornton", fontsize=14,
                        fontname="helv", color=(0.2, 0.2, 0.2), align=pymupdf.TEXT_ALIGN_CENTER)

    # Publisher
    rect4 = pymupdf.Rect(72, 700, 523, 740)
    page.insert_textbox(rect4, "Meridian Academic Press | 2025", fontsize=11,
                        fontname="helv", color=(0.4, 0.4, 0.4), align=pymupdf.TEXT_ALIGN_CENTER)

    # Decorative lines
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(150, 360), pymupdf.Point(445, 360))
    shape.finish(color=(0.1, 0.1, 0.4), width=2)
    shape.draw_line(pymupdf.Point(150, 365), pymupdf.Point(445, 365))
    shape.finish(color=(0.6, 0.2, 0.2), width=1)
    shape.commit()

    doc.save(path)
    doc.close()
    print(f"Created cover: {path}")


def create_toc_template(path):
    """Create a 1-page blank TOC template."""
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)

    # Just a header to indicate this is a placeholder
    rect = pymupdf.Rect(72, 60, 523, 100)
    page.insert_textbox(rect, "Table of Contents", fontsize=24, fontname="hebo",
                        color=(0.1, 0.1, 0.4), align=pymupdf.TEXT_ALIGN_CENTER)

    # Placeholder text
    page.insert_text(pymupdf.Point(200, 200), "[Generated during assembly]",
                     fontsize=11, fontname="tiit", color=(0.5, 0.5, 0.5))

    doc.save(path)
    doc.close()
    print(f"Created TOC template: {path}")


def create_chapter_pdf(path, title, num_pages, sentences):
    """Create a chapter PDF with the specified number of pages and content."""
    doc = pymupdf.open()

    for pg_idx in range(num_pages):
        page = doc.new_page(width=595, height=842)

        if pg_idx == 0:
            # Chapter title page
            rect = pymupdf.Rect(72, 80, 523, 140)
            page.insert_textbox(rect, title, fontsize=22, fontname="hebo",
                                color=(0.1, 0.1, 0.4), align=pymupdf.TEXT_ALIGN_LEFT)

            # Horizontal rule
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 150), pymupdf.Point(523, 150))
            shape.finish(color=(0.1, 0.1, 0.4), width=1.5)
            shape.commit()

            y_pos = 180
        else:
            y_pos = 72

        # Add paragraph content per page
        sentence_idx = pg_idx % len(sentences)
        paragraph = sentences[sentence_idx]

        # Build a full page of content by repeating/expanding sentences
        content_lines = []
        content_lines.append(paragraph)
        # Add supporting text to fill the page
        filler_paragraphs = [
            f"This section continues the discussion from the previous analysis, "
            f"building on the key concepts introduced earlier in {title.split(':')[0]}.",
            "The methodology employed here follows established best practices "
            "in the field, ensuring reproducibility and statistical rigor.",
            "Researchers have noted that these techniques yield consistent results "
            "across a wide range of datasets and application domains.",
            "Table {}.{} summarizes the key findings from this phase of the analysis, "
            "highlighting both the strengths and limitations of the approach.".format(
                title.split()[1].rstrip(':'), pg_idx + 1),
            "Further investigation reveals nuanced patterns that merit deeper "
            "exploration in subsequent chapters of this comprehensive guide.",
        ]

        full_text = paragraph + "\n\n"
        for fp in filler_paragraphs:
            full_text += fp + "\n\n"

        content_rect = pymupdf.Rect(72, y_pos, 523, 780)
        page.insert_textbox(content_rect, full_text, fontsize=11,
                            fontname="helv", color=(0, 0, 0),
                            align=pymupdf.TEXT_ALIGN_JUSTIFY)

        # Page footer
        footer_rect = pymupdf.Rect(72, 800, 523, 820)
        page.insert_textbox(footer_rect, f"- {pg_idx + 1} -", fontsize=9,
                            fontname="helv", color=(0.5, 0.5, 0.5),
                            align=pymupdf.TEXT_ALIGN_CENTER)

    doc.save(path)
    doc.close()
    print(f"Created chapter: {path} ({num_pages} pages)")


def create_initial():
    os.makedirs(ASSEMBLY_DIR, exist_ok=True)

    # Create cover
    create_cover_pdf(f"{ASSEMBLY_DIR}/cover.pdf")

    # Create TOC template
    create_toc_template(f"{ASSEMBLY_DIR}/toc_template.pdf")

    # Create chapter files
    for i, (title, num_pages, sentences) in enumerate(CHAPTERS, 1):
        create_chapter_pdf(f"{ASSEMBLY_DIR}/ch{i}.pdf", title, num_pages, sentences)

    print(f"\nAll source files created in {ASSEMBLY_DIR}/")
    print("Files:")
    for f in sorted(os.listdir(ASSEMBLY_DIR)):
        fpath = os.path.join(ASSEMBLY_DIR, f)
        if os.path.isfile(fpath):
            print(f"  {f} ({os.path.getsize(fpath)} bytes)")

    # Open file manager to show assembly directory
    launch_gui(f'nautilus "{ASSEMBLY_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
