"""
Initial Setup: Create a 90-page thesis PDF with cross-reference text but no active hyperlinks.
Task ID: pdf_res_067
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_067'
THESIS_DIR = f'{WORKDIR}/thesis'
OUTPUT = f'{THESIS_DIR}/thesis_links.pdf'

# Page dimensions (A4)
W, H = 595, 842
MARGIN_L = 72
MARGIN_R = 523
MARGIN_T = 72
MARGIN_B = 770

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

# Thesis chapter structure (page ranges, 1-indexed for readability)
CHAPTERS = [
    {"title": "Abstract", "start": 1, "end": 2},
    {"title": "Acknowledgments", "start": 3, "end": 3},
    {"title": "Table of Contents", "start": 4, "end": 4},
    {"title": "Chapter 1: Introduction", "start": 5, "end": 19},
    {"title": "Chapter 2: Literature Review", "start": 20, "end": 34},
    {"title": "Chapter 3: Methodology", "start": 35, "end": 54},
    {"title": "Chapter 4: Results and Analysis", "start": 55, "end": 69},
    {"title": "Chapter 5: Discussion", "start": 70, "end": 79},
    {"title": "Appendix A: Supplementary Data", "start": 80, "end": 85},
    {"title": "Appendix B: Survey Instruments", "start": 86, "end": 88},
    {"title": "References", "start": 89, "end": 90},
]

# Cross-reference text to place on specific pages (0-indexed internally)
CROSS_REFS = {
    4: "For a comprehensive overview of prior work in this area, see Chapter 2 for the complete literature review that covers foundational theories and recent developments.",
    14: "The analytical framework builds on established protocols; see Chapter 3 for the full methodology including data collection procedures and statistical models.",
    59: "Detailed supplementary tables and raw datasets are provided separately; see Appendix A for all supporting materials referenced throughout this discussion.",
}

# Realistic paragraph content for filler
INTRO_PARAGRAPHS = [
    "The rapid advancement of artificial intelligence and machine learning technologies has fundamentally transformed the landscape of computational research across multiple disciplines. This thesis examines the intersection of deep learning architectures and natural language understanding, with particular focus on transformer-based models and their applications in domain-specific knowledge extraction.",
    "Recent developments in large-scale pre-training have demonstrated remarkable capabilities in few-shot learning and transfer across diverse tasks. However, significant challenges remain in adapting these models to specialized domains where labeled data is scarce and domain expertise is critical for accurate interpretation of results.",
    "Our research addresses these challenges through a novel framework that combines supervised fine-tuning with reinforcement learning from human feedback, enabling models to better align with expert expectations while maintaining generalization capabilities across related tasks.",
    "The primary contributions of this work include: (1) a systematic evaluation of transfer learning strategies for domain adaptation, (2) a new benchmark dataset comprising 15,000 annotated examples from the biomedical literature, and (3) an analysis of the trade-offs between model size, training efficiency, and downstream task performance.",
    "This thesis is organized as follows. The current chapter provides background context and motivation for the research questions. Subsequent chapters present the theoretical framework, experimental methodology, results, and implications for future work in this rapidly evolving field.",
]

LIT_REVIEW_PARAGRAPHS = [
    "The foundations of modern natural language processing can be traced to the seminal work of Vaswani et al. (2017), who introduced the transformer architecture. This self-attention mechanism replaced recurrent and convolutional approaches, enabling significantly more efficient parallel computation during training.",
    "Building on the transformer architecture, Devlin et al. (2019) proposed BERT, a bidirectional encoder that achieved state-of-the-art results across eleven natural language understanding benchmarks. The masked language modeling objective proved particularly effective for learning contextual representations.",
    "Subsequent work by Brown et al. (2020) demonstrated that scaling language models to 175 billion parameters enabled remarkable few-shot learning capabilities, challenging previous assumptions about the necessity of task-specific fine-tuning.",
    "In the biomedical domain, Lee et al. (2020) showed that domain-specific pre-training on PubMed abstracts yielded substantial improvements over general-purpose models, highlighting the importance of domain adaptation strategies.",
    "More recently, Ouyang et al. (2022) introduced reinforcement learning from human feedback (RLHF) as a method for aligning language model outputs with human preferences, opening new avenues for incorporating expert knowledge into model training.",
]

METHODOLOGY_PARAGRAPHS = [
    "Our experimental framework employs a three-stage training pipeline consisting of domain-adaptive pre-training, supervised fine-tuning, and preference optimization. Each stage is designed to progressively refine the model's capabilities for the target domain.",
    "Data collection involved systematic extraction of 45,000 biomedical abstracts from PubMed Central, covering publications from 2018 to 2024. We applied rigorous quality filters including citation count thresholds, journal impact factor requirements, and automated coherence scoring.",
    "The annotation protocol was developed in collaboration with three domain experts holding doctoral degrees in molecular biology. Inter-annotator agreement was measured using Fleiss' kappa, achieving a score of 0.78, indicating substantial agreement across all annotation categories.",
    "Model training was conducted on a cluster of 8 NVIDIA A100 GPUs with 80GB memory each. We employed mixed-precision training with gradient accumulation to effectively simulate larger batch sizes while maintaining memory efficiency.",
    "Statistical analysis of results utilized bootstrapped confidence intervals with 10,000 resamples, paired with Bonferroni correction for multiple comparisons. Effect sizes were reported using Cohen's d to facilitate comparison with prior work.",
]

RESULTS_PARAGRAPHS = [
    "Our primary model achieved an F1 score of 0.847 on the held-out test set, representing a 4.2 percentage point improvement over the strongest baseline. This improvement was statistically significant (p < 0.001) across all evaluation metrics.",
    "Analysis of performance by document category revealed that the model performed best on structured abstracts (F1 = 0.891) and showed more variable performance on case reports (F1 = 0.782), suggesting that structural regularity aids in information extraction.",
    "The ablation study demonstrated that each component of our training pipeline contributes meaningfully to overall performance. Removing the domain-adaptive pre-training stage resulted in a 2.8 point decrease in F1, while omitting the preference optimization step reduced performance by 1.9 points.",
    "Error analysis identified three primary failure modes: (1) ambiguous entity boundaries in complex noun phrases (accounting for 34% of errors), (2) nested entity recognition challenges (28% of errors), and (3) domain-specific abbreviation disambiguation (22% of errors).",
    "Computational efficiency analysis showed that our model requires approximately 40% fewer training steps to reach convergence compared to training from a general-purpose checkpoint, validating the effectiveness of the domain-adaptive pre-training approach.",
]

DISCUSSION_PARAGRAPHS = [
    "The results presented in the previous chapter demonstrate the viability of our proposed framework for domain-specific language understanding. The consistent improvements across multiple evaluation metrics suggest that the three-stage training pipeline captures complementary aspects of linguistic knowledge.",
    "Our findings align with recent theoretical work suggesting that domain adaptation is most effective when the pre-training corpus shares distributional characteristics with the target domain. The biomedical literature, with its relatively consistent structure and terminology, appears particularly well-suited to this approach.",
    "Several limitations of the current work should be acknowledged. First, our evaluation is restricted to English-language publications, and the generalizability to multilingual biomedical literature remains untested. Second, the computational requirements of the full training pipeline may limit accessibility for smaller research groups.",
    "Future directions include extending the framework to incorporate multimodal inputs such as figures, tables, and chemical structures that frequently appear in biomedical publications. Additionally, exploring methods for continual learning would enable the model to adapt to emerging terminology and research paradigms.",
    "In conclusion, this thesis makes meaningful contributions to the field of domain-specific natural language understanding, providing both practical tools and theoretical insights that can inform future research in specialized language model development.",
]

APPENDIX_PARAGRAPHS = [
    "Table A.1 presents the complete set of hyperparameters used across all experimental conditions. Learning rates were selected through a grid search over the range [1e-6, 5e-4] with logarithmic spacing.",
    "Table A.2 reports the per-category performance metrics for all thirteen entity types in our annotation schema. Performance varies considerably across categories, with well-defined entities (e.g., gene names) achieving F1 scores above 0.90 while more ambiguous categories (e.g., biological processes) fall below 0.80.",
    "Figure A.1 shows the training loss curves for the three-stage pipeline across five independent runs. Convergence is typically achieved within 15,000 steps for the fine-tuning stage, with minimal variance between runs.",
    "The complete survey instrument used for the expert evaluation study is reproduced in Appendix B. Participants were recruited from three major research universities and compensated at a rate of $50 per hour for their annotation time.",
    "Additional statistical analyses including confidence interval plots and effect size comparisons are available in the supplementary materials accompanying this thesis.",
]


def get_chapter_for_page(page_1indexed):
    """Return the chapter info for a given 1-indexed page number."""
    for ch in CHAPTERS:
        if ch["start"] <= page_1indexed <= ch["end"]:
            return ch
    return None


def get_paragraph_for_page(page_1indexed):
    """Select appropriate content paragraphs based on which chapter the page belongs to."""
    ch = get_chapter_for_page(page_1indexed)
    if ch is None:
        return INTRO_PARAGRAPHS[0]

    title = ch["title"]
    # Calculate offset within this chapter
    offset = page_1indexed - ch["start"]

    if "Introduction" in title:
        return INTRO_PARAGRAPHS[offset % len(INTRO_PARAGRAPHS)]
    elif "Literature" in title:
        return LIT_REVIEW_PARAGRAPHS[offset % len(LIT_REVIEW_PARAGRAPHS)]
    elif "Methodology" in title:
        return METHODOLOGY_PARAGRAPHS[offset % len(METHODOLOGY_PARAGRAPHS)]
    elif "Results" in title:
        return RESULTS_PARAGRAPHS[offset % len(RESULTS_PARAGRAPHS)]
    elif "Discussion" in title:
        return DISCUSSION_PARAGRAPHS[offset % len(DISCUSSION_PARAGRAPHS)]
    elif "Appendix" in title:
        return APPENDIX_PARAGRAPHS[offset % len(APPENDIX_PARAGRAPHS)]
    elif "References" in title:
        return "Brown, T. et al. (2020). Language Models are Few-Shot Learners. NeurIPS."
    elif "Abstract" in title:
        return "This thesis investigates the application of transformer-based language models to domain-specific natural language understanding tasks, with emphasis on biomedical text mining and information extraction."
    elif "Acknowledgments" in title:
        return "The author wishes to thank the members of the thesis committee for their invaluable guidance throughout this research. Special thanks to the Natural Language Processing Lab for providing computational resources and a stimulating research environment."
    elif "Table of Contents" in title:
        return ""  # Will be handled specially
    else:
        return INTRO_PARAGRAPHS[0]


def create_initial():
    os.makedirs(THESIS_DIR, exist_ok=True)

    doc = pymupdf.open()

    for page_num_0 in range(90):
        page_num_1 = page_num_0 + 1
        page = doc.new_page(width=W, height=H)

        ch = get_chapter_for_page(page_num_1)
        y_cursor = MARGIN_T

        # Page header (chapter title, small font)
        if ch:
            page.insert_text(
                pymupdf.Point(MARGIN_L, y_cursor),
                ch["title"],
                fontsize=9,
                fontname="tiit",
                color=(0.4, 0.4, 0.4),
            )
        y_cursor += 20

        # Horizontal rule under header
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN_L, y_cursor), pymupdf.Point(MARGIN_R, y_cursor))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape.commit()
        y_cursor += 15

        # Chapter title on first page of each chapter
        if ch and ch["start"] == page_num_1:
            page.insert_text(
                pymupdf.Point(MARGIN_L, y_cursor + 20),
                ch["title"],
                fontsize=22,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )
            y_cursor += 55

        # Table of Contents page
        if page_num_1 == 4:
            page.insert_text(
                pymupdf.Point(MARGIN_L, y_cursor + 10),
                "Table of Contents",
                fontsize=20,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )
            y_cursor += 50
            for entry in CHAPTERS:
                if entry["title"] == "Table of Contents":
                    continue
                line = f"{entry['title']} {'.' * (60 - len(entry['title']))} {entry['start']}"
                page.insert_text(
                    pymupdf.Point(MARGIN_L + 10, y_cursor),
                    line,
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                )
                y_cursor += 18
        else:
            # Regular content
            # Get main paragraph for this page
            para = get_paragraph_for_page(page_num_1)

            if para:
                rect = pymupdf.Rect(MARGIN_L, y_cursor, MARGIN_R, MARGIN_B - 60)
                # Build multi-paragraph content for the page
                content_parts = [para]

                # Add cross-reference text if this page has one
                if page_num_0 in CROSS_REFS:
                    content_parts.append("")
                    content_parts.append(CROSS_REFS[page_num_0])

                # Add additional paragraphs to fill the page
                extra_idx = (page_num_1 * 3) % 5
                extra_paragraphs = {
                    0: "The theoretical implications of these findings extend beyond the immediate scope of our investigation. By demonstrating the effectiveness of staged training approaches, we provide evidence that sequential knowledge acquisition mirrors aspects of human learning processes.",
                    1: "Cross-validation results confirmed the robustness of our findings across different data splits. The standard deviation of F1 scores across ten folds was 0.012, indicating high stability of the trained models regardless of the specific training examples selected.",
                    2: "Implementation details for all experiments are provided in the supplementary code repository. All models were implemented using PyTorch 2.0 with the Hugging Face Transformers library version 4.30, ensuring full reproducibility of reported results.",
                    3: "The ethical considerations of deploying automated text mining systems in biomedical research were carefully evaluated. Our institutional review board confirmed that the use of publicly available abstracts for model training does not require additional ethical approval.",
                    4: "Scalability analysis demonstrated that the proposed approach maintains performance advantages even when the training corpus size is reduced to 25% of the full dataset, suggesting practical applicability in resource-constrained scenarios.",
                }
                content_parts.append("")
                content_parts.append(extra_paragraphs[extra_idx])

                full_text = "\n\n".join(content_parts)
                page.insert_textbox(
                    rect,
                    full_text,
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )

        # Page number at bottom center
        page.insert_text(
            pymupdf.Point(W / 2 - 10, H - 40),
            str(page_num_1),
            fontsize=10,
            fontname="helv",
            color=(0.3, 0.3, 0.3),
        )

    # Set TOC bookmarks
    toc = []
    for ch in CHAPTERS:
        toc.append([1, ch["title"], ch["start"]])
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "Transformer-Based Language Models for Domain-Specific Natural Language Understanding",
        "author": "Elena Vasquez",
        "subject": "PhD Thesis - Computer Science",
        "keywords": "NLP, transformers, deep learning, biomedical text mining",
        "creator": "Elena Vasquez",
        "producer": "PyMuPDF",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
