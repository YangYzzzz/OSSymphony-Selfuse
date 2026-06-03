"""
Initial Setup: Create a 100-page thesis PDF with no footers.
Task ID: pdf_res_034
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_034'
THESIS_DIR = f'{WORKDIR}/thesis'
OUTPUT = f'{THESIS_DIR}/thesis_final.pdf'

# Realistic thesis chapter structure
CHAPTERS = [
    ("Abstract", 1),
    ("Acknowledgements", 1),
    ("Table of Contents", 2),
    ("List of Figures", 1),
    ("List of Tables", 1),
    ("Chapter 1: Introduction", 8),
    ("Chapter 2: Literature Review", 12),
    ("Chapter 3: Theoretical Framework", 10),
    ("Chapter 4: Methodology", 10),
    ("Chapter 5: Data Collection and Analysis", 14),
    ("Chapter 6: Results", 12),
    ("Chapter 7: Discussion", 10),
    ("Chapter 8: Conclusions and Future Work", 6),
    ("Bibliography", 8),
    ("Appendix A: Survey Instruments", 2),
    ("Appendix B: Statistical Tables", 2),
]

# Realistic body paragraphs for filling pages
BODY_PARAGRAPHS = [
    "The rapid advancement of machine learning techniques over the past decade has fundamentally transformed how researchers approach complex problems in computational linguistics. Natural language processing, once dominated by rule-based systems and statistical methods, has been revolutionised by deep learning architectures that can learn hierarchical representations of text.",
    "This thesis investigates the application of transformer-based models to low-resource language pairs, with a particular focus on Welsh-English and Scots Gaelic-English translation. These language pairs present unique challenges due to the limited availability of parallel corpora and the morphological complexity of Celtic languages.",
    "Previous work by Henderson et al. (2023) demonstrated that transfer learning from high-resource language pairs can significantly improve translation quality for under-resourced languages. However, their approach relied on typologically similar source languages, which may not always be available.",
    "Our experimental framework builds upon the Oxford Neural Machine Translation toolkit, incorporating novel data augmentation strategies that leverage monolingual corpora in both source and target languages. We employ back-translation, paraphrase mining, and cross-lingual word embedding alignment to expand our training data.",
    "The methodology follows a mixed-methods research design, combining quantitative evaluation metrics such as BLEU, chrF++, and COMET scores with qualitative analysis through human evaluation campaigns. A panel of twelve bilingual annotators assessed translation adequacy and fluency on a five-point Likert scale.",
    "Statistical analysis was performed using R version 4.3.2 with the lme4 package for mixed-effects modelling. We accounted for annotator variability by including random intercepts for each evaluator and random slopes for translation direction in our regression models.",
    "Results indicate a statistically significant improvement in translation quality when using our proposed augmentation pipeline compared to the baseline system (p < 0.001, Cohen's d = 0.82). The effect was particularly pronounced for longer sentences exceeding twenty tokens in length.",
    "The implications of these findings extend beyond the specific language pairs studied here. Our augmentation framework is language-agnostic and can be applied to any low-resource translation scenario where monolingual data is more readily available than parallel corpora.",
    "Furthermore, we conducted an ablation study removing each component of the augmentation pipeline individually. Back-translation contributed the largest improvement (+3.2 BLEU points), followed by cross-lingual embedding alignment (+1.8 BLEU points) and paraphrase mining (+1.1 BLEU points).",
    "The qualitative analysis revealed that human evaluators consistently preferred translations produced by the augmented system, particularly for sentences containing idiomatic expressions and culturally specific references that are difficult to translate literally.",
    "We also examined the impact of domain-specific fine-tuning on translation quality across four domains: academic text, news articles, literary prose, and conversational dialogue. Domain adaptation yielded the greatest improvements for literary prose, which contains the most creative and non-literal language use.",
    "Error analysis of the system outputs revealed three primary categories of translation errors: lexical choice errors (42%), syntactic restructuring failures (31%), and morphological agreement violations (27%). These proportions remained relatively stable across all experimental conditions.",
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


def create_initial():
    os.makedirs(THESIS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # A4 page dimensions
    W, H = 595, 842
    LEFT_MARGIN = 72
    RIGHT_MARGIN = 523
    TOP_START = 80
    BODY_RECT_TOP = 120
    BODY_RECT_BOTTOM = 780
    TEXT_WIDTH = RIGHT_MARGIN - LEFT_MARGIN

    page_count = 0
    para_idx = 0

    for chapter_title, num_pages in CHAPTERS:
        for page_in_chapter in range(num_pages):
            page = doc.new_page(width=W, height=H)
            page_count += 1

            if page_in_chapter == 0:
                # Chapter title page
                page.insert_text(
                    pymupdf.Point(LEFT_MARGIN, TOP_START),
                    chapter_title,
                    fontsize=18,
                    fontname="hebo",
                    color=(0, 0, 0),
                )
                body_top = 130
            else:
                body_top = TOP_START

            # Fill page with body text
            rect = pymupdf.Rect(LEFT_MARGIN, body_top, RIGHT_MARGIN, BODY_RECT_BOTTOM)
            # Compose enough text to fill the page
            fill_text = ""
            for i in range(6):
                p = BODY_PARAGRAPHS[(para_idx + i) % len(BODY_PARAGRAPHS)]
                fill_text += p + "\n\n"
            para_idx += 3  # advance so each page has different content

            page.insert_textbox(
                rect,
                fill_text,
                fontsize=11,
                fontname="tiro",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

            # Page number at bottom center (but NO footer text)
            page.insert_text(
                pymupdf.Point(W / 2 - 5, H - 30),
                str(page_count),
                fontsize=9,
                fontname="tiro",
                color=(0.4, 0.4, 0.4),
            )

    # Ensure exactly 100 pages
    while doc.page_count < 100:
        page = doc.new_page(width=W, height=H)
        page_count += 1
        rect = pymupdf.Rect(LEFT_MARGIN, TOP_START, RIGHT_MARGIN, BODY_RECT_BOTTOM)
        fill_text = ""
        for i in range(6):
            p = BODY_PARAGRAPHS[(para_idx + i) % len(BODY_PARAGRAPHS)]
            fill_text += p + "\n\n"
        para_idx += 3

        page.insert_textbox(
            rect,
            fill_text,
            fontsize=11,
            fontname="tiro",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )
        page.insert_text(
            pymupdf.Point(W / 2 - 5, H - 30),
            str(page_count),
            fontsize=9,
            fontname="tiro",
            color=(0.4, 0.4, 0.4),
        )

    # Set metadata
    doc.set_metadata({
        "title": "Advancing Neural Machine Translation for Low-Resource Celtic Languages",
        "author": "Eleanor M. Richardson",
        "subject": "Computational Linguistics, Machine Translation",
        "keywords": "NMT, low-resource, Celtic languages, transfer learning, data augmentation",
        "creator": "LaTeX with hyperref",
        "producer": "pdfTeX-1.40.25",
    })

    # Set table of contents
    toc = []
    page_offset = 1
    for chapter_title, num_pages in CHAPTERS:
        toc.append([1, chapter_title, page_offset])
        page_offset += num_pages
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: {page_count}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
