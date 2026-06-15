"""
Initial Setup: Multi-app task — PDF paper + Writer document + Chrome
Task ID: osworld_multi_apps_paper_scholar_browse_013
Domain: multi_apps (libreoffice_writer + chrome + pdf)
"""

import os
import shlex
import subprocess
import time
import textwrap

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_paper_scholar_browse_013'
PDF_OUTPUT = f'{WORKDIR}/{TASK_ID}.pdf'
DOC_OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'


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


def create_pdf():
    """Create a realistic multimodal learning paper PDF with 3 authors."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_xy(15, 20)
    title = "Multimodal Contrastive Learning with Unified Transformer Encoders"
    # Wrap title manually
    pdf.multi_cell(180, 8, title, align='C')

    # Authors
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 12)
    authors = "Jiasen Lu    Dhruv Batra    Devi Parikh"
    pdf.cell(0, 8, authors, ln=True, align='C')

    # Affiliation
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 6, "Georgia Institute of Technology", ln=True, align='C')
    pdf.cell(0, 6, "{jlu, dbatra, dparikh}@gatech.edu", ln=True, align='C')

    pdf.ln(4)

    # Abstract
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Abstract", ln=True)
    pdf.set_font("Helvetica", "", 10)
    abstract = textwrap.fill(
        "We present a unified multimodal contrastive learning framework that jointly encodes visual and "
        "textual representations using a shared Transformer backbone. Our approach leverages large-scale "
        "image-text pairs collected from the web and introduces a novel cross-modal attention mechanism "
        "to align semantically related concepts. We demonstrate state-of-the-art performance on visual "
        "question answering, image-text retrieval, and visual reasoning benchmarks. Our model, dubbed "
        "UniVLP (Unified Vision-Language Pre-training), achieves 78.4% accuracy on VQA v2, "
        "surpassing all prior vision-language models by a significant margin. We further show that "
        "the learned representations exhibit strong zero-shot transfer capabilities across diverse "
        "downstream tasks without task-specific fine-tuning.",
        width=100
    )
    pdf.multi_cell(180, 5, abstract)

    pdf.ln(4)

    # Section 1: Introduction
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "1  Introduction", ln=True)
    pdf.set_font("Helvetica", "", 10)
    intro = (
        "The ability to understand and reason across multiple modalities is a fundamental challenge in "
        "artificial intelligence. Recent advances in large language models have demonstrated remarkable "
        "performance in text-based tasks, but extending these capabilities to visual inputs remains an "
        "open problem. Multimodal learning aims to bridge this gap by learning joint representations "
        "that capture the rich semantic relationships between images and text.\n\n"
        "Prior work on vision-language models has explored various architectures, including dual-encoder "
        "models, cross-attention networks, and generative approaches. However, most existing methods "
        "treat visual and textual inputs as fundamentally different modalities and use separate encoders "
        "with limited cross-modal interaction. In this paper, we propose a unified architecture that "
        "processes both modalities through a shared Transformer encoder with modality-specific input "
        "embeddings.\n\n"
        "Our key contributions are as follows:\n"
        "(1) A unified Transformer encoder architecture for joint vision-language representation learning.\n"
        "(2) A novel contrastive learning objective that aligns visual and textual representations.\n"
        "(3) State-of-the-art results on multiple multimodal benchmarks.\n"
        "(4) Extensive ablation studies demonstrating the effectiveness of each component."
    )
    pdf.multi_cell(180, 5, intro)

    pdf.ln(4)

    # Section 2: Related Work
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "2  Related Work", ln=True)
    pdf.set_font("Helvetica", "", 10)
    related = (
        "Vision-language pre-training has been studied extensively in recent years. ViLBERT [Lu et al., 2019] "
        "introduced a two-stream model that processes visual and textual inputs separately with cross-modal "
        "attention layers. UNITER [Chen et al., 2020] proposed a universal image-text representation "
        "model trained on four image-text datasets. CLIP [Radford et al., 2021] demonstrated that "
        "simple contrastive learning on large-scale web-scraped data yields powerful zero-shot visual "
        "representations. ALIGN [Jia et al., 2021] scaled this approach to even larger datasets.\n\n"
        "Our work builds on these foundations while introducing a more tightly integrated unified "
        "architecture. Unlike prior approaches that use separate visual and textual encoders, we "
        "propose a single shared encoder that processes patch embeddings and token embeddings jointly, "
        "enabling richer cross-modal interactions at all layers of the network."
    )
    pdf.multi_cell(180, 5, related)

    pdf.ln(4)

    # Section 3: Method
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "3  Method", ln=True)
    pdf.set_font("Helvetica", "", 10)
    method = (
        "3.1  Input Representation\n\n"
        "Given an image I and a text sentence T, we first extract image patches using a convolutional "
        "stem network following ViT [Dosovitskiy et al., 2021]. Each image is divided into N patches "
        "of size 16x16 pixels, resulting in a sequence of patch embeddings {v_1, ..., v_N}. Text is "
        "tokenized using a WordPiece tokenizer with a vocabulary of 30,000 tokens, yielding a sequence "
        "of token embeddings {w_1, ..., w_M}.\n\n"
        "3.2  Unified Transformer Encoder\n\n"
        "Both patch embeddings and token embeddings are concatenated and fed into a 12-layer Transformer "
        "encoder. Modality-specific positional embeddings and type embeddings are added to distinguish "
        "between visual and textual tokens. The self-attention mechanism allows each token to attend "
        "to all other tokens regardless of modality.\n\n"
        "3.3  Training Objective\n\n"
        "We train UniVLP using three objectives: (1) masked language modeling on text tokens, "
        "(2) masked image modeling on visual tokens, and (3) image-text contrastive learning. "
        "The contrastive objective aligns the [CLS] representations of matched image-text pairs "
        "while pushing apart unmatched pairs using InfoNCE loss with a temperature parameter."
    )
    pdf.multi_cell(180, 5, method)

    pdf.add_page()

    # Section 4: Experiments
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "4  Experiments", ln=True)
    pdf.set_font("Helvetica", "", 10)
    experiments = (
        "4.1  Datasets\n\n"
        "We pre-train UniVLP on a combination of Conceptual Captions (3.3M image-text pairs), "
        "MSCOCO (113K images with 5 captions each), Visual Genome (108K images with region "
        "descriptions), and SBU Captions (1M image-caption pairs). For evaluation, we use VQA v2, "
        "GQA, NLVR2, Flickr30K retrieval, and MSCOCO captioning.\n\n"
        "4.2  Results\n\n"
        "UniVLP achieves 78.4% accuracy on VQA v2 test-dev, outperforming all existing methods "
        "including ViLBERT (70.55%), UNITER (73.82%), and OSCAR (73.82%). On NLVR2, our model "
        "achieves 84.0% accuracy, a 5.2% improvement over the previous state-of-the-art. "
        "On Flickr30K image-to-text retrieval, we achieve 88.6% recall@1.\n\n"
        "4.3  Ablation Study\n\n"
        "We conduct ablation studies to analyze the contribution of each component. Removing "
        "the contrastive objective reduces VQA accuracy by 2.3%. Replacing the unified encoder "
        "with dual encoders reduces performance by 1.8%. These results confirm the importance "
        "of tight cross-modal integration."
    )
    pdf.multi_cell(180, 5, experiments)

    pdf.ln(4)

    # Section 5: Conclusion
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "5  Conclusion", ln=True)
    pdf.set_font("Helvetica", "", 10)
    conclusion = (
        "We presented UniVLP, a unified vision-language pre-training framework that achieves "
        "state-of-the-art performance across multiple multimodal benchmarks. Our approach "
        "demonstrates the benefits of tight cross-modal integration through a shared Transformer "
        "encoder. Future work includes scaling to larger datasets and exploring generative "
        "multimodal tasks."
    )
    pdf.multi_cell(180, 5, conclusion)

    pdf.ln(4)

    # References
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "References", ln=True)
    pdf.set_font("Helvetica", "", 9)
    references = [
        "[1] Lu, J., Batra, D., Parikh, D., Lee, S. ViLBERT: Pretraining Task-Agnostic "
        "Visiolinguistic Representations for Vision-and-Language Tasks. NeurIPS 2019.",
        "[2] Chen, Y., Li, L., Yu, L., et al. UNITER: Universal Image-Text Representation "
        "Learning. ECCV 2020.",
        "[3] Radford, A., Kim, J. W., Hallacy, C., et al. Learning Transferable Visual Models "
        "from Natural Language Supervision. ICML 2021.",
        "[4] Jia, C., Yang, Y., Xia, Y., et al. Scaling Up Visual and Vision-Language "
        "Representation Learning with Noisy Text Supervision. ICML 2021.",
        "[5] Dosovitskiy, A., Beyer, L., Kolesnikov, A., et al. An Image is Worth 16x16 "
        "Words: Transformers for Image Recognition at Scale. ICLR 2021.",
    ]
    for ref in references:
        pdf.multi_cell(180, 5, ref)
        pdf.ln(1)

    pdf.output(PDF_OUTPUT)
    print(f'PDF created: {PDF_OUTPUT}')


def create_writer_doc():
    """Create a blank LibreOffice Writer document."""
    from docx import Document

    doc = Document()
    # Leave it blank — the agent will fill it in
    doc.save(DOC_OUTPUT)
    print(f'Writer document created: {DOC_OUTPUT}')


def create_initial():
    create_pdf()
    create_writer_doc()

    # GUI-ready startup: open PDF in Evince and Writer document in LibreOffice Writer
    # Also ensure Chrome is available
    launch_gui(f'evince "{PDF_OUTPUT}"', delay_sec=2.0)
    launch_gui(f'libreoffice --writer "{DOC_OUTPUT}"', delay_sec=2.0)
    # Chrome available but not necessarily pre-opened (agent will open it to search)
    print('GUI_READY: launched PDF viewer and LibreOffice Writer with DISPLAY=:0')


create_initial()
