"""
Initial Setup: Create a 100-page dissertation PDF with no bookmarks.
Task ID: pdf_res_036
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_036'
THESIS_DIR = f'{WORKDIR}/thesis'
OUTPUT = f'{THESIS_DIR}/dissertation_v2.pdf'


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

    # Dissertation content structure:
    # Part I: Theory (pages 1-49)
    #   Chapter 1: Introduction and Theoretical Framework (pages 1-24)
    #   Chapter 2: Literature Review and Methodology (pages 25-49)
    # Part II: Experiments (pages 50-99)
    #   Chapter 3: Experimental Design and Data Collection (pages 50-74)
    #   Chapter 4: Results and Discussion (pages 75-99)

    chapter_starts = {
        0: ("Part I: Theory", "Chapter 1: Introduction and Theoretical Framework"),
        24: ("", "Chapter 2: Literature Review and Methodology"),
        49: ("Part II: Experiments", "Chapter 3: Experimental Design and Data Collection"),
        74: ("", "Chapter 4: Results and Discussion"),
    }

    section_content = {
        "Chapter 1": [
            "1.1 Background and Motivation",
            "The study of computational linguistics has undergone a remarkable transformation over the past two decades. Early approaches relied heavily on rule-based systems, which, while theoretically elegant, struggled with the inherent ambiguity and variability of natural language. The emergence of statistical methods in the 1990s marked a paradigm shift, enabling systems to learn patterns from large corpora rather than relying on hand-crafted rules.",
            "Recent advances in deep learning have further revolutionized the field. Neural network architectures, particularly transformer models, have demonstrated unprecedented performance across a wide range of natural language processing tasks. These models leverage self-attention mechanisms to capture long-range dependencies in text, achieving state-of-the-art results in machine translation, text summarization, and question answering.",
            "1.2 Research Objectives",
            "This dissertation aims to address three key research questions that have emerged from the intersection of computational linguistics and cognitive science. First, we investigate how contextual representations learned by large language models relate to human semantic processing. Second, we examine the extent to which these models capture syntactic structures that align with linguistic theory. Third, we explore practical applications of these findings in developing more interpretable and efficient NLP systems.",
            "1.3 Theoretical Framework",
            "Our theoretical framework draws upon three pillars: distributional semantics, formal syntax, and cognitive processing models. The distributional hypothesis, which posits that words occurring in similar contexts tend to have similar meanings, provides the foundation for understanding how neural models learn word representations. We complement this with insights from generative grammar, particularly Minimalist Program theories, to analyze the syntactic knowledge captured by these models.",
        ],
        "Chapter 2": [
            "2.1 Historical Context",
            "The development of natural language processing can be traced through several distinct phases. The rationalist period, spanning from the 1950s through the 1980s, was characterized by symbolic approaches rooted in formal logic and linguistic theory. Researchers during this era developed intricate grammar formalisms and knowledge representation schemes, producing systems like SHRDLU and LUNAR that could handle natural language within restricted domains.",
            "The empiricist revolution of the 1990s brought statistical methods to the forefront. Hidden Markov Models, maximum entropy classifiers, and later conditional random fields became the standard tools for tasks such as part-of-speech tagging, named entity recognition, and parsing. The availability of annotated corpora like the Penn Treebank enabled supervised learning approaches that significantly outperformed their rule-based predecessors.",
            "2.2 Neural Network Approaches",
            "The application of neural networks to NLP began gaining momentum with the introduction of word embeddings. Bengio et al. (2003) proposed neural language models that learned distributed representations of words, laying the groundwork for the word2vec models (Mikolov et al., 2013) that would later become ubiquitous in NLP research. These dense, low-dimensional representations captured semantic relationships through vector arithmetic, famously encoding analogies like 'king - man + woman = queen'.",
            "2.3 Methodology",
            "Our methodology combines quantitative analysis of model representations with qualitative linguistic evaluation. We employ representational similarity analysis (RSA) to compare the geometric structure of neural network representations with behavioral data from human experiments. Additionally, we use structural probing techniques to assess the extent to which syntactic information is linearly encoded in model representations.",
        ],
        "Chapter 3": [
            "3.1 Experimental Design",
            "The experimental framework comprises three complementary studies, each designed to address one of the research questions outlined in Chapter 1. Study 1 investigates semantic representations through a series of similarity judgment tasks. Study 2 examines syntactic knowledge using targeted grammatical assessments. Study 3 evaluates the practical implications of our findings through an application-oriented evaluation.",
            "3.2 Data Collection",
            "For Study 1, we assembled a dataset of 5,000 sentence pairs drawn from multiple domains, including news articles, scientific abstracts, literary fiction, and conversational transcripts. Each pair was annotated by five human raters on a 1-7 Likert scale for semantic similarity. Inter-annotator agreement, measured by Krippendorff's alpha, was 0.78, indicating substantial agreement.",
            "For Study 2, we constructed a grammatical acceptability dataset consisting of 3,200 minimal pairs. Each pair contained one grammatically correct sentence and one containing a specific syntactic violation. Violations were systematically varied across 16 categories, including subject-verb agreement, negative polarity item licensing, reflexive binding, and island constraints.",
            "3.3 Computational Analysis",
            "All neural network experiments were conducted using a cluster of 8 NVIDIA A100 GPUs with 80GB memory each. Models were implemented in PyTorch 2.0 and trained using the AdamW optimizer with a cosine learning rate schedule. We evaluated models at five scales: 125M, 350M, 1.3B, 6.7B, and 13B parameters to study the relationship between model size and linguistic competence.",
            "3.4 Statistical Methods",
            "Statistical analyses were performed using a combination of parametric and non-parametric methods. For comparing model representations with human judgments, we computed Spearman rank correlations with bootstrap confidence intervals (10,000 iterations). Mixed-effects regression models were used to account for item-level and participant-level variability in the human data.",
        ],
        "Chapter 4": [
            "4.1 Semantic Representation Results",
            "Our analysis reveals a strong positive correlation between model representations and human semantic judgments, with the correlation strength increasing monotonically with model size. The 13B parameter model achieved a Spearman correlation of 0.847 (95% CI: [0.831, 0.862]) with human similarity ratings, significantly outperforming the 125M model (rho = 0.612, p < 0.001). Notably, the relationship between model size and correlation strength follows a logarithmic curve, suggesting diminishing returns at larger scales.",
            "4.2 Syntactic Knowledge Assessment",
            "The grammatical acceptability results paint a nuanced picture. While all models performed above chance on aggregate metrics, performance varied dramatically across syntactic categories. Subject-verb agreement and simple word order violations were handled well even by smaller models (>90% accuracy at 350M parameters). However, long-distance dependencies, such as island constraints and parasitic gaps, showed strong scaling effects, with only the 6.7B and 13B models achieving above-chance performance.",
            "4.3 Cross-Domain Generalization",
            "An important finding concerns the domain-specificity of learned representations. Models trained primarily on web text showed significantly reduced performance on scientific and literary texts, with correlation drops of 15-20% compared to in-domain evaluation. This suggests that current pre-training regimes may not adequately capture the full range of human linguistic knowledge.",
            "4.4 Discussion",
            "These results contribute to ongoing debates about the linguistic competence of neural language models. Our findings suggest that while these models develop increasingly sophisticated representations of semantic structure with scale, their acquisition of syntactic knowledge is more selective and may not fully align with human grammatical competence. The domain-specificity of learned representations further highlights the gap between broad linguistic knowledge and the narrower distributional patterns captured during pre-training.",
            "4.5 Implications for NLP System Design",
            "Based on our findings, we propose three design principles for more linguistically-informed NLP systems. First, architectural modifications that explicitly encode hierarchical structure may improve syntactic generalization without requiring massive scale. Second, diverse pre-training corpora spanning multiple genres and registers are essential for robust semantic representations. Third, human evaluation should complement automated metrics, particularly for tasks requiring nuanced linguistic understanding.",
        ],
    }

    for page_idx in range(100):
        page = doc.new_page(width=595, height=842)  # A4

        # Check if this is a chapter start page
        if page_idx in chapter_starts:
            part_title, chapter_title = chapter_starts[page_idx]
            y_pos = 120

            if part_title:
                page.insert_text(
                    pymupdf.Point(72, y_pos),
                    part_title,
                    fontsize=22,
                    fontname="hebo",
                    color=(0, 0, 0),
                )
                y_pos += 50

            page.insert_text(
                pymupdf.Point(72, y_pos),
                chapter_title,
                fontsize=18,
                fontname="hebo",
                color=(0, 0, 0),
            )
            y_pos += 40

            # Add a decorative line under the title
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, y_pos), pymupdf.Point(523, y_pos))
            shape.finish(color=(0.3, 0.3, 0.3), width=1.5)
            shape.commit()
            y_pos += 30

            # Determine which chapter content to use
            ch_key = None
            for key in section_content:
                if key in chapter_title:
                    ch_key = key
                    break

            if ch_key:
                content_rect = pymupdf.Rect(72, y_pos, 523, 780)
                paragraphs = section_content[ch_key]
                text = "\n\n".join(paragraphs)
                page.insert_textbox(
                    content_rect,
                    text,
                    fontsize=11,
                    fontname="tiro",
                    color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )
        else:
            # Regular continuation page with filler academic text
            page_number = page_idx + 1

            # Header with page number
            page.insert_text(
                pymupdf.Point(500, 40),
                str(page_number),
                fontsize=10,
                fontname="tiro",
                color=(0.4, 0.4, 0.4),
            )

            # Determine section context based on page range
            if page_idx < 24:
                section = "Chapter 1"
                section_num = "1"
            elif page_idx < 49:
                section = "Chapter 2"
                section_num = "2"
            elif page_idx < 74:
                section = "Chapter 3"
                section_num = "3"
            else:
                section = "Chapter 4"
                section_num = "4"

            # Running header
            page.insert_text(
                pymupdf.Point(72, 40),
                f"Computational Approaches to Linguistic Cognition - {section}",
                fontsize=8,
                fontname="heit",
                color=(0.5, 0.5, 0.5),
            )

            # Header line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 50), pymupdf.Point(523, 50))
            shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
            shape.commit()

            # Body text - continuation paragraphs
            body_texts = [
                f"The analysis presented in Section {section_num}.{(page_idx % 5) + 1} demonstrates the relationship between model architecture and representational capacity. As computational resources increase, the quality of learned representations improves along multiple dimensions, though the rate of improvement varies across linguistic phenomena.",
                f"Table {section_num}.{page_idx % 8 + 1} summarizes the performance metrics across all experimental conditions. The standard deviations indicate moderate variability in individual item performance, suggesting that aggregate metrics may mask important differences in how models handle specific linguistic constructions. Further analysis of error patterns reveals systematic biases that correlate with the frequency distribution of syntactic structures in the training data.",
                "The implications of these findings extend beyond the specific models examined in this study. The observed scaling laws suggest fundamental constraints on what can be learned from distributional information alone, regardless of model capacity. This observation aligns with theoretical predictions from formal linguistics regarding the poverty of the stimulus, though the precise boundary between learnable and unlearnable structures remains an open question.",
                "Furthermore, the cross-linguistic evaluation conducted as part of this analysis reveals that the patterns observed in English largely generalize to other Indo-European languages, but show notable differences in agglutinative and polysynthetic languages. These typological effects provide additional evidence for the role of morphological complexity in determining the difficulty of grammatical generalization for neural models.",
                f"We note several limitations of the current approach. First, the reliance on minimal pairs for syntactic evaluation may overestimate model competence, as models may exploit superficial cues rather than genuine structural analysis. Second, the comparison with human behavioral data is limited by the artificial nature of laboratory experiments, which may not reflect natural language processing. Third, computational constraints prevented evaluation of models beyond 13B parameters, leaving open the question of whether larger models would exhibit qualitatively different behavior.",
            ]

            content_rect = pymupdf.Rect(72, 65, 523, 780)
            full_text = "\n\n".join(body_texts)
            page.insert_textbox(
                content_rect,
                full_text,
                fontsize=11,
                fontname="tiro",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_JUSTIFY,
            )

            # Footer line
            shape2 = page.new_shape()
            shape2.draw_line(pymupdf.Point(72, 800), pymupdf.Point(523, 800))
            shape2.finish(color=(0.7, 0.7, 0.7), width=0.5)
            shape2.commit()

    # Verify NO bookmarks
    assert doc.get_toc() == [], "Initial PDF should have no bookmarks"

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 100')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
