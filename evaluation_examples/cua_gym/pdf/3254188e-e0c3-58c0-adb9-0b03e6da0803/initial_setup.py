"""
Initial Setup: Create a multi-page academic paper PDF with a figure on page 5.
Task ID: pdf_res_091
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_091'
PAPERS_DIR = f'{WORKDIR}/papers'
SOURCE_PDF = f'{PAPERS_DIR}/source_figure.pdf'


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
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ---- Page 1: Title page ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(
        pymupdf.Point(297, 200),
        "A Scalable Architecture for",
        fontsize=22, fontname="hebo", color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(297, 235),
        "Neural Sequence-to-Sequence Learning",
        fontsize=22, fontname="hebo", color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(297, 300),
        "Emily R. Smith, Tao Wang, Priya Gupta",
        fontsize=13, fontname="helv", color=(0.2, 0.2, 0.2),
    )
    page.insert_text(
        pymupdf.Point(297, 325),
        "Institute for Advanced Computation, MIT",
        fontsize=11, fontname="heit", color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(297, 370),
        "Published: March 2025",
        fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3),
    )

    # ---- Page 2: Abstract ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 72), "Abstract", fontsize=16, fontname="hebo", color=(0, 0, 0))
    abstract_rect = pymupdf.Rect(72, 100, 523, 350)
    page.insert_textbox(
        abstract_rect,
        "We present a novel architecture for neural sequence-to-sequence learning that "
        "achieves state-of-the-art performance on multiple benchmarks while maintaining "
        "computational efficiency. Our proposed model leverages hierarchical attention "
        "mechanisms combined with sparse transformer blocks to reduce the quadratic "
        "complexity of standard attention to near-linear scaling. Experiments on machine "
        "translation (WMT'24 En-De, En-Fr), abstractive summarization (CNN/DailyMail), "
        "and code generation (HumanEval) demonstrate consistent improvements of 2.3-4.1 "
        "BLEU points over strong baselines. We also provide a comprehensive ablation study "
        "examining the contribution of each architectural component.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Keywords
    page.insert_text(pymupdf.Point(72, 370), "Keywords:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(
        pymupdf.Point(140, 370),
        "sequence-to-sequence, transformer, attention mechanism, neural machine translation",
        fontsize=11, fontname="heit", color=(0.2, 0.2, 0.2),
    )

    # ---- Page 3: Introduction ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 72), "1  Introduction", fontsize=16, fontname="hebo", color=(0, 0, 0))
    intro_rect = pymupdf.Rect(72, 100, 523, 500)
    page.insert_textbox(
        intro_rect,
        "The transformer architecture (Vaswani et al., 2017) has become the dominant paradigm "
        "for sequence modeling tasks across natural language processing, computer vision, and "
        "multimodal learning. Despite its remarkable success, the standard transformer suffers "
        "from quadratic memory and computational complexity with respect to sequence length, "
        "limiting its applicability to long-context scenarios.\n\n"
        "Several approaches have been proposed to address this limitation, including sparse "
        "attention patterns (Child et al., 2019), linear attention approximations (Katharopoulos "
        "et al., 2020), and state-space models (Gu et al., 2022). However, these methods often "
        "sacrifice model quality for efficiency, resulting in degraded performance on tasks "
        "requiring fine-grained token-level interactions.\n\n"
        "In this paper, we propose a hierarchical attention architecture that dynamically "
        "allocates computational resources based on input complexity. Our key insight is that "
        "most sequence positions require only local context, while a small subset of critical "
        "positions benefit from global attention. By identifying these critical positions through "
        "a lightweight gating mechanism, we achieve near-linear scaling without sacrificing quality.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # ---- Page 4: Related Work ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 72), "2  Related Work", fontsize=16, fontname="hebo", color=(0, 0, 0))
    rw_rect = pymupdf.Rect(72, 100, 523, 500)
    page.insert_textbox(
        rw_rect,
        "2.1  Efficient Transformers\n\n"
        "The quest for efficient attention mechanisms has produced a rich body of work. "
        "Linformer (Wang et al., 2020) projects key-value pairs to lower dimensions, achieving "
        "linear complexity but with fixed compression ratios. Performer (Choromanski et al., 2021) "
        "approximates softmax attention via random feature maps, enabling linear-time computation "
        "at the cost of approximation error. BigBird (Zaheer et al., 2020) combines local windowed "
        "attention with random and global tokens, demonstrating strong performance on long documents.\n\n"
        "2.2  Hierarchical Models\n\n"
        "Hierarchical approaches process sequences at multiple granularities. HAT (Hao et al., 2021) "
        "uses multi-scale attention heads operating at different resolutions. Hourglass Transformer "
        "(Nawrot et al., 2022) downsamples and upsamples the sequence, applying full attention only "
        "at coarser levels. Our approach differs by using adaptive gating rather than fixed "
        "hierarchical structure, allowing the model to dynamically adjust its receptive field.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # ---- Page 5: The Figure Page (Architecture Diagram) ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 72), "3  Proposed Architecture", fontsize=16, fontname="hebo", color=(0, 0, 0))
    page.insert_text(
        pymupdf.Point(72, 100),
        "Figure 1 illustrates the overall architecture of our proposed model.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
    )

    shape = page.new_shape()

    # -- Draw architecture diagram --
    # Input Embedding box (bottom)
    shape.draw_rect(pymupdf.Rect(200, 650, 395, 690))
    shape.finish(color=(0, 0, 0), fill=(0.85, 0.92, 1.0), width=1.5)

    # Local Attention block
    shape.draw_rect(pymupdf.Rect(200, 560, 395, 600))
    shape.finish(color=(0, 0, 0), fill=(0.8, 1.0, 0.8), width=1.5)

    # Gating Mechanism block
    shape.draw_rect(pymupdf.Rect(200, 470, 395, 510))
    shape.finish(color=(0, 0, 0), fill=(1.0, 0.9, 0.75), width=1.5)

    # Global Attention block
    shape.draw_rect(pymupdf.Rect(120, 380, 280, 420))
    shape.finish(color=(0, 0, 0), fill=(1.0, 0.8, 0.8), width=1.5)

    # Sparse Attention block
    shape.draw_rect(pymupdf.Rect(315, 380, 475, 420))
    shape.finish(color=(0, 0, 0), fill=(0.9, 0.8, 1.0), width=1.5)

    # Feed-Forward Network block
    shape.draw_rect(pymupdf.Rect(200, 290, 395, 330))
    shape.finish(color=(0, 0, 0), fill=(0.85, 0.92, 1.0), width=1.5)

    # Output Projection block
    shape.draw_rect(pymupdf.Rect(200, 200, 395, 240))
    shape.finish(color=(0, 0, 0), fill=(0.95, 0.95, 0.95), width=1.5)

    # Arrows (upward flow)
    # Input -> Local Attention
    shape.draw_line(pymupdf.Point(297, 650), pymupdf.Point(297, 600))
    shape.finish(color=(0, 0, 0), width=1.2)
    # Local Attention -> Gating
    shape.draw_line(pymupdf.Point(297, 560), pymupdf.Point(297, 510))
    shape.finish(color=(0, 0, 0), width=1.2)
    # Gating -> Global Attention (left branch)
    shape.draw_line(pymupdf.Point(260, 470), pymupdf.Point(200, 420))
    shape.finish(color=(0, 0, 0), width=1.2)
    # Gating -> Sparse Attention (right branch)
    shape.draw_line(pymupdf.Point(335, 470), pymupdf.Point(395, 420))
    shape.finish(color=(0, 0, 0), width=1.2)
    # Global Attention -> FFN
    shape.draw_line(pymupdf.Point(200, 380), pymupdf.Point(260, 330))
    shape.finish(color=(0, 0, 0), width=1.2)
    # Sparse Attention -> FFN
    shape.draw_line(pymupdf.Point(395, 380), pymupdf.Point(335, 330))
    shape.finish(color=(0, 0, 0), width=1.2)
    # FFN -> Output
    shape.draw_line(pymupdf.Point(297, 290), pymupdf.Point(297, 240))
    shape.finish(color=(0, 0, 0), width=1.2)

    shape.commit()

    # Labels inside boxes
    page.insert_text(pymupdf.Point(240, 676), "Input Embedding", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(240, 586), "Local Attention", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(230, 496), "Gating Mechanism", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(145, 406), "Global Attention", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(340, 406), "Sparse Attention", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(228, 316), "Feed-Forward Network", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(237, 226), "Output Projection", fontsize=11, fontname="helv", color=(0, 0, 0))

    # Figure caption below diagram
    page.insert_text(
        pymupdf.Point(120, 720),
        "Figure 1: Architecture of the proposed hierarchical attention model.",
        fontsize=10, fontname="heit", color=(0.2, 0.2, 0.2),
    )

    # ---- Page 6: Experiments ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 72), "4  Experiments", fontsize=16, fontname="hebo", color=(0, 0, 0))
    exp_rect = pymupdf.Rect(72, 100, 523, 400)
    page.insert_textbox(
        exp_rect,
        "We evaluate our model on three benchmark tasks:\n\n"
        "Machine Translation: WMT'24 English-German and English-French datasets. We use "
        "the standard train/dev/test splits and report detokenized BLEU scores.\n\n"
        "Abstractive Summarization: CNN/DailyMail dataset with ROUGE-1, ROUGE-2, and ROUGE-L "
        "metrics. We follow the preprocessing of See et al. (2017).\n\n"
        "Code Generation: HumanEval benchmark measuring pass@1 and pass@10 scores for "
        "function-level Python code generation.\n\n"
        "Our model achieves 32.8 BLEU on En-De (+2.3 over baseline), 41.5 BLEU on En-Fr (+3.1), "
        "45.2 ROUGE-1 on CNN/DM (+1.8), and 78.4% pass@1 on HumanEval (+4.1 percentage points).",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # ---- Page 7: Conclusion ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 72), "5  Conclusion", fontsize=16, fontname="hebo", color=(0, 0, 0))
    conc_rect = pymupdf.Rect(72, 100, 523, 300)
    page.insert_textbox(
        conc_rect,
        "We have presented a hierarchical attention architecture that achieves near-linear "
        "complexity while maintaining state-of-the-art quality across multiple sequence modeling "
        "tasks. Our adaptive gating mechanism allows the model to dynamically allocate "
        "computational resources, focusing global attention only where needed. Future work "
        "will explore extending this approach to multimodal settings and investigating the "
        "learned gating patterns for interpretability.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    doc.save(SOURCE_PDF)
    doc.close()
    print(f'Initial file created: {SOURCE_PDF}')

    # Open the source PDF in Evince for the agent
    launch_gui(f'evince "{SOURCE_PDF}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
