"""
Initial Setup: Create combined_report.pdf with 40 pages in ~/Documents/
Task ID: pdf_cross_146
Domain: pdf (multi-app workflow)

Creates:
  ~/Documents/combined_report.pdf  — 40-page PDF with 5 chapters:
      Ch1: pages 1-8   (heading "Chapter 1: Introduction to Data Science")
      Ch2: pages 9-16  (heading "Chapter 2: Data Collection Methods")
      Ch3: pages 17-24 (heading "Chapter 3: Statistical Analysis")
      Ch4: pages 25-32 (heading "Chapter 4: Machine Learning Techniques")
      Ch5: pages 33-40 (heading "Chapter 5: Visualization and Reporting")

Does NOT create:
  ~/Documents/book/  (agent must create this)
  ~/Documents/book/chapters/  (agent must create this)

Task (multi-app workflow):
  1. Use Terminal to batch split ~/Documents/combined_report.pdf into
     individual chapter PDFs (Chapters 1-5).
  2. In File Manager, organize chapters into ~/Documents/book/chapters/.
  3. Use GIMP to create chapter divider images (colored title pages).
  4. Use pymupdf to interleave dividers between chapters.
     Save as ~/Documents/book/complete_book.pdf.

Ground truth:
  ~/Documents/book/chapters/chapter_1.pdf  (pages 1-8,   8 pages)
  ~/Documents/book/chapters/chapter_2.pdf  (pages 9-16,  8 pages)
  ~/Documents/book/chapters/chapter_3.pdf  (pages 17-24, 8 pages)
  ~/Documents/book/chapters/chapter_4.pdf  (pages 25-32, 8 pages)
  ~/Documents/book/chapters/chapter_5.pdf  (pages 33-40, 8 pages)
  ~/Documents/book/complete_book.pdf       (45 pages: 5 dividers + 40 content)

Opens terminal and file manager for the GUI agent.
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = "/home/user/Documents"
OUTPUT = f"{WORKDIR}/combined_report.pdf"

# A4 dimensions
A4_W, A4_H = 595, 842

# Chapter definitions: (chapter_num, title, start_page_1based, end_page_1based)
CHAPTERS = [
    (1, "Introduction to Data Science",    1,  8),
    (2, "Data Collection Methods",          9, 16),
    (3, "Statistical Analysis",            17, 24),
    (4, "Machine Learning Techniques",     25, 32),
    (5, "Visualization and Reporting",     33, 40),
]

# Chapter colors for headers (R, G, B) as floats 0-1
CHAPTER_COLORS = {
    1: (0.12, 0.28, 0.58),   # dark blue
    2: (0.15, 0.45, 0.25),   # dark green
    3: (0.55, 0.18, 0.18),   # dark red
    4: (0.48, 0.22, 0.55),   # dark purple
    5: (0.55, 0.38, 0.08),   # dark orange/brown
}

# Per-chapter section topics (8 pages per chapter = 8 section topics)
CHAPTER_TOPICS = {
    1: [
        "Overview of Data Science",
        "Historical Context and Evolution",
        "Core Concepts and Terminology",
        "Data Science Lifecycle",
        "Tools and Technologies",
        "Career Paths in Data Science",
        "Ethical Considerations",
        "Summary and Key Takeaways",
    ],
    2: [
        "Primary vs Secondary Data Sources",
        "Survey Design and Methodology",
        "Web Scraping and APIs",
        "Database Querying",
        "Sensor and IoT Data Collection",
        "Data Quality Assessment",
        "Handling Missing Data",
        "Summary and Key Takeaways",
    ],
    3: [
        "Descriptive Statistics",
        "Probability Distributions",
        "Hypothesis Testing",
        "Regression Analysis",
        "ANOVA and Variance",
        "Time Series Analysis",
        "Bayesian Statistics",
        "Summary and Key Takeaways",
    ],
    4: [
        "Introduction to Machine Learning",
        "Supervised Learning Algorithms",
        "Unsupervised Learning Techniques",
        "Neural Networks and Deep Learning",
        "Model Evaluation Metrics",
        "Overfitting and Regularization",
        "Ensemble Methods",
        "Summary and Key Takeaways",
    ],
    5: [
        "Principles of Data Visualization",
        "Chart Types and Selection",
        "Tools: Matplotlib and Seaborn",
        "Interactive Dashboards",
        "Storytelling with Data",
        "Report Writing for Technical Audiences",
        "Presentation Best Practices",
        "Summary and Key Takeaways",
    ],
}

# Body text templates for each section (realistic content snippets)
SECTION_BODIES = {
    "Overview of Data Science": (
        "Data science is an interdisciplinary field that combines statistics, computer science,\n"
        "and domain expertise to extract meaningful insights from data. At its core, data\n"
        "science involves collecting, processing, analyzing, and interpreting large and complex\n"
        "datasets to inform decisions and solve real-world problems.\n\n"
        "The rapid growth of digital information has transformed data science from a niche\n"
        "academic pursuit into a critical business function. Organizations across industries—\n"
        "from healthcare and finance to retail and government—leverage data science to gain\n"
        "competitive advantages, improve operations, and deliver better outcomes.\n\n"
        "Key disciplines that comprise modern data science include:\n"
        "  • Statistics and Probability: The mathematical foundation for inference and prediction\n"
        "  • Computer Science: Algorithms, data structures, and software engineering\n"
        "  • Domain Expertise: Industry-specific knowledge to contextualize findings\n"
        "  • Communication: Translating technical results for non-technical stakeholders\n\n"
        "SECTION_MARKER: CH1_P1_OVERVIEW_OF_DATA_SCIENCE"
    ),
    "Historical Context and Evolution": (
        "The roots of data science trace back to statistics and computer science disciplines\n"
        "of the mid-20th century. The term 'data science' itself was coined in the 1990s,\n"
        "though its current form emerged prominently in the 2000s with the explosion of\n"
        "big data technologies.\n\n"
        "Key milestones in data science history:\n"
        "  1960s-70s: Development of relational databases and early statistical software\n"
        "  1980s: Growth of machine learning as a formal discipline\n"
        "  1990s: Data mining emerges; 'data scientist' term coined\n"
        "  2000s: Hadoop, MapReduce enable large-scale distributed processing\n"
        "  2010s: Deep learning renaissance; cloud computing democratizes access\n"
        "  2020s: AutoML, MLOps, and AI integration become mainstream\n\n"
        "SECTION_MARKER: CH1_P2_HISTORICAL_CONTEXT"
    ),
    "Core Concepts and Terminology": (
        "Understanding data science requires familiarity with key terminology used across\n"
        "the field. These concepts form the shared vocabulary for practitioners.\n\n"
        "Fundamental terms:\n"
        "  Feature/Variable: A measurable property used in analysis\n"
        "  Target/Label: The outcome variable to be predicted\n"
        "  Training Set: Data used to build/fit a model\n"
        "  Test Set: Held-out data used to evaluate model performance\n"
        "  Model: A mathematical representation learned from data\n"
        "  Bias-Variance Tradeoff: The balance between underfitting and overfitting\n"
        "  Cross-validation: Technique for robust model evaluation\n"
        "  Feature Engineering: Creating new informative features from raw data\n\n"
        "SECTION_MARKER: CH1_P3_CORE_CONCEPTS"
    ),
    "Data Science Lifecycle": (
        "The data science lifecycle is a systematic process for transforming raw data into\n"
        "actionable insights. While implementations vary, most frameworks include these stages:\n\n"
        "  1. Problem Definition: Clarify business question and success criteria\n"
        "  2. Data Acquisition: Identify and collect relevant data sources\n"
        "  3. Data Exploration (EDA): Understand data structure, distributions, relationships\n"
        "  4. Data Preparation: Clean, transform, and engineer features\n"
        "  5. Modeling: Select algorithms, train models, tune hyperparameters\n"
        "  6. Evaluation: Assess model performance against business metrics\n"
        "  7. Deployment: Integrate model into production systems\n"
        "  8. Monitoring: Track performance and retrain as needed\n\n"
        "SECTION_MARKER: CH1_P4_DATA_SCIENCE_LIFECYCLE"
    ),
    "Tools and Technologies": (
        "Modern data scientists rely on a rich ecosystem of tools and platforms:\n\n"
        "Programming Languages:\n"
        "  Python: Most popular for data science; rich library ecosystem\n"
        "  R: Excellent for statistical analysis and visualization\n"
        "  SQL: Essential for database querying and manipulation\n\n"
        "Key Python Libraries:\n"
        "  NumPy, Pandas: Data manipulation and analysis\n"
        "  Scikit-learn: Machine learning algorithms\n"
        "  TensorFlow, PyTorch: Deep learning frameworks\n"
        "  Matplotlib, Seaborn, Plotly: Data visualization\n\n"
        "Platforms and Infrastructure:\n"
        "  Jupyter Notebooks: Interactive development environment\n"
        "  Apache Spark: Large-scale distributed processing\n"
        "  Cloud platforms: AWS, GCP, Azure for scalable deployment\n\n"
        "SECTION_MARKER: CH1_P5_TOOLS_AND_TECHNOLOGIES"
    ),
    "Career Paths in Data Science": (
        "The data science field offers diverse career trajectories. Common roles include:\n\n"
        "  Data Analyst: Focuses on business reporting, SQL, Excel, BI tools\n"
        "  Data Engineer: Builds data pipelines and infrastructure\n"
        "  Data Scientist: Builds predictive models, communicates insights\n"
        "  ML Engineer: Deploys and operationalizes machine learning models\n"
        "  Research Scientist: Advances the theoretical foundations of AI/ML\n\n"
        "Salary and demand for data scientists remain high across industries.\n"
        "The Bureau of Labor Statistics projects 35% growth in data science roles\n"
        "through 2032, significantly above the national average.\n\n"
        "SECTION_MARKER: CH1_P6_CAREER_PATHS"
    ),
    "Ethical Considerations": (
        "Ethical data science is not optional—it is fundamental to responsible practice.\n"
        "Key ethical considerations include:\n\n"
        "  Privacy: Protecting personal data through anonymization and encryption\n"
        "  Bias and Fairness: Identifying and mitigating algorithmic discrimination\n"
        "  Transparency: Explainable AI and model interpretability\n"
        "  Consent: Ensuring data was collected with appropriate permissions\n"
        "  Security: Safeguarding data from unauthorized access and breaches\n\n"
        "Regulatory frameworks such as GDPR (EU), CCPA (California), and HIPAA (healthcare)\n"
        "impose legal obligations on data collection and usage. Organizations that fail to\n"
        "comply face substantial fines and reputational damage.\n\n"
        "SECTION_MARKER: CH1_P7_ETHICAL_CONSIDERATIONS"
    ),
    "Summary and Key Takeaways": (
        "This chapter provided a comprehensive introduction to data science as a field.\n"
        "The key takeaways are:\n\n"
        "  ✓ Data science combines statistics, computer science, and domain expertise\n"
        "  ✓ The field has evolved rapidly from academic origins to mainstream enterprise use\n"
        "  ✓ A structured lifecycle guides projects from problem definition to deployment\n"
        "  ✓ Python, SQL, and statistical thinking are foundational skills\n"
        "  ✓ Ethical considerations must be embedded throughout every project\n\n"
        "The following chapters will explore each component of the data science workflow\n"
        "in greater depth, providing practical techniques and real-world examples.\n\n"
        "CHAPTER_END_MARKER: CHAPTER_SUMMARY_PAGE"
    ),
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


def get_section_body(chapter_num: int, page_in_chapter: int, section_topic: str) -> str:
    """Get body text for a section, using template if available or generating generic content."""
    if section_topic in SECTION_BODIES:
        return SECTION_BODIES[section_topic]

    # Generate generic content with unique marker
    chapter_tag = f"CH{chapter_num}"
    page_tag = f"P{page_in_chapter}"
    marker = f"{chapter_tag}_{page_tag}_{section_topic.upper().replace(' ', '_').replace(',', '').replace('/', '_')}"

    return (
        f"This section covers {section_topic} in depth, exploring theoretical foundations\n"
        f"and practical applications relevant to Chapter {chapter_num}.\n\n"
        f"Key points covered in this section:\n"
        f"  • Conceptual overview of {section_topic.lower()}\n"
        f"  • Historical development and current best practices\n"
        f"  • Practical implementation strategies\n"
        f"  • Common pitfalls and how to avoid them\n"
        f"  • Case studies demonstrating real-world applications\n\n"
        f"Students are encouraged to complete the exercises at the end of this section\n"
        f"to reinforce their understanding of the material presented.\n\n"
        f"SECTION_MARKER: {marker}"
    )


def create_chapter_page(doc, chapter_num: int, chapter_title: str,
                        page_in_chapter: int, total_pages_in_chapter: int,
                        absolute_page_num: int, section_topic: str):
    """Add a single styled page to the document."""
    page = doc.new_page(width=A4_W, height=A4_H)
    header_color = CHAPTER_COLORS[chapter_num]

    # Light background
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, A4_W, A4_H))
    shape.finish(color=None, fill=(0.97, 0.97, 0.98), width=0)
    shape.commit()

    # Header band
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, A4_W, 65))
    shape.finish(color=None, fill=header_color, width=0)
    shape.commit()

    # Header: chapter title (left) and page number (right)
    page.insert_text(
        pymupdf.Point(36, 24),
        f"Chapter {chapter_num}: {chapter_title}",
        fontsize=9,
        fontname="hebo",
        color=(1.0, 1.0, 1.0),
    )
    page.insert_text(
        pymupdf.Point(36, 44),
        "Data Science Fundamentals — Comprehensive Study Guide",
        fontsize=8,
        fontname="helv",
        color=(0.85, 0.88, 0.93),
    )
    page.insert_text(
        pymupdf.Point(495, 34),
        f"Page {absolute_page_num}",
        fontsize=9,
        fontname="helv",
        color=(0.85, 0.88, 0.93),
    )

    # Thin separator below header
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 80), pymupdf.Point(559, 80))
    shape.finish(color=header_color, width=1.5)
    shape.commit()

    # Section title
    page.insert_text(
        pymupdf.Point(36, 108),
        section_topic,
        fontsize=14,
        fontname="hebo",
        color=header_color,
    )

    # Section subtitle line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 116), pymupdf.Point(559, 116))
    shape.finish(color=(0.65, 0.68, 0.72), width=0.8)
    shape.commit()

    # Body text
    body_text = get_section_body(chapter_num, page_in_chapter, section_topic)
    text_rect = pymupdf.Rect(36, 128, 559, 795)
    page.insert_textbox(
        text_rect,
        body_text,
        fontsize=10,
        fontname="helv",
        color=(0.10, 0.10, 0.10),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Footer line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 812), pymupdf.Point(559, 812))
    shape.finish(color=(0.72, 0.72, 0.72), width=0.5)
    shape.commit()

    page.insert_text(
        pymupdf.Point(36, 827),
        "© 2024 DataSci Publishing Ltd. All rights reserved.",
        fontsize=7.5,
        fontname="helv",
        color=(0.52, 0.52, 0.52),
    )
    page.insert_text(
        pymupdf.Point(400, 827),
        f"Chapter {chapter_num} — Section {page_in_chapter} of {total_pages_in_chapter}",
        fontsize=7.5,
        fontname="helv",
        color=(0.52, 0.52, 0.52),
    )


def create_initial():
    os.makedirs(WORKDIR, exist_ok=True)

    # Ensure book/ does NOT pre-exist (agent must create it)
    book_dir = os.path.join(WORKDIR, "book")
    if os.path.exists(book_dir):
        import shutil
        shutil.rmtree(book_dir)
    print(f"Confirmed: {book_dir}/ does not exist (agent must create it)")

    doc = pymupdf.open()
    absolute_page = 0

    for chapter_num, chapter_title, start_page, end_page in CHAPTERS:
        pages_in_chapter = end_page - start_page + 1
        topics = CHAPTER_TOPICS[chapter_num]
        assert len(topics) == pages_in_chapter, (
            f"Chapter {chapter_num} topic count mismatch: {len(topics)} vs {pages_in_chapter}"
        )

        for page_in_chapter_idx, topic in enumerate(topics):
            absolute_page += 1
            create_chapter_page(
                doc,
                chapter_num=chapter_num,
                chapter_title=chapter_title,
                page_in_chapter=page_in_chapter_idx + 1,
                total_pages_in_chapter=pages_in_chapter,
                absolute_page_num=absolute_page,
                section_topic=topic,
            )

    assert absolute_page == 40, f"Expected 40 pages, created {absolute_page}"

    doc.set_metadata({
        "title": "Data Science Fundamentals — Comprehensive Study Guide",
        "author": "DataSci Publishing Editorial Team",
        "subject": "Data Science Education",
        "keywords": "data science, machine learning, statistics, visualization",
        "creator": "DataSci Publishing Ltd.",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f"Created: {OUTPUT} (40 pages)")

    # Verify the created PDF
    verify_doc = pymupdf.open(OUTPUT)
    assert verify_doc.page_count == 40, (
        f"Expected 40 pages, got {verify_doc.page_count}"
    )
    # Spot-check chapter headings on first page of each chapter
    chapter_first_pages = [0, 8, 16, 24, 32]  # 0-indexed
    for ch_idx, page_idx in enumerate(chapter_first_pages):
        text = verify_doc[page_idx].get_text("text")
        ch_num = ch_idx + 1
        assert f"Chapter {ch_num}" in text, (
            f"Missing Chapter {ch_num} heading on page index {page_idx}"
        )
    verify_doc.close()
    print("Verified: combined_report.pdf has 40 pages with correct chapter structure")

    # Launch terminal and file manager for the GUI agent
    launch_gui("xterm", delay_sec=1.5)
    launch_gui('nautilus "/home/user/Documents"', delay_sec=1.5)
    print("GUI_READY: launched xterm and nautilus with DISPLAY=:0")


create_initial()
