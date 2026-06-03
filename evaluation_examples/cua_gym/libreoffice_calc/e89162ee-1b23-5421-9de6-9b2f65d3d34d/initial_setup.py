"""
Initial Setup: Create 9 arXiv PDF preprints in ~/Downloads/Preprints
Task ID: osworld_multi_apps_pdf_author_extract_009
Domain: libreoffice_calc (multi-app: PDF + Calc)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_author_extract_009'
PREPRINTS_DIR = f'{WORKDIR}/Downloads/Preprints'

# The 9 arXiv papers with realistic first-author metadata (2021-2024)
# Format: (filename, name, email, affiliation, year, arxiv_id, title, abstract_snippet)
PAPERS = [
    {
        'filename': 'attention_free_transformer_2022.pdf',
        'name': 'Zhen Yang',
        'email': 'zhen.yang@bytedance.com',
        'affiliation': 'ByteDance Research',
        'year': 2022,
        'arxiv_id': '2209.02535',
        'title': 'Gated Linear Attention Transformers with Hardware-Efficient Training',
        'abstract': 'We propose gated linear attention (GLA) Transformers, featuring a data-dependent gating mechanism with a hardware-efficient parallel training algorithm. We develop a new Triton kernel for GLA that achieves superior training throughput compared to FlashAttention-2.',
    },
    {
        'filename': 'diffusion_probabilistic_2021.pdf',
        'name': 'Jonathan Ho',
        'email': 'jonathanho@google.com',
        'affiliation': 'Google Brain',
        'year': 2021,
        'arxiv_id': '2102.09672',
        'title': 'Cascaded Diffusion Models for High Fidelity Image Generation',
        'abstract': 'We present cascaded diffusion models for high fidelity image generation. A cascaded diffusion model comprises a pipeline of multiple diffusion models that generate images of increasing resolution, beginning with a standard diffusion model at the lowest resolution, followed by one or more super-resolution diffusion models.',
    },
    {
        'filename': 'language_model_alignment_2023.pdf',
        'name': 'Amanda Askell',
        'email': 'amanda@anthropic.com',
        'affiliation': 'Anthropic',
        'year': 2023,
        'arxiv_id': '2212.08073',
        'title': 'A General Language Assistant as a Laboratory for Alignment',
        'abstract': 'We study the properties of a helpful, harmless, and honest AI assistant. We explore the relationship between these properties, evaluate their presence across a range of language model sizes, and discuss the tradeoffs involved in training models to exhibit them.',
    },
    {
        'filename': 'multimodal_foundation_2023.pdf',
        'name': 'Haotian Liu',
        'email': 'haotianliu@cs.wisc.edu',
        'affiliation': 'University of Wisconsin-Madison',
        'year': 2023,
        'arxiv_id': '2304.08485',
        'title': 'Visual Instruction Tuning',
        'abstract': 'We present LLaVA: Large Language and Vision Assistant, an end-to-end trained large multimodal model that connects a vision encoder and LLM for general-purpose visual and language understanding.',
    },
    {
        'filename': 'retrieval_augmented_2023.pdf',
        'name': 'Patrick Lewis',
        'email': 'plewis@meta.com',
        'affiliation': 'Meta AI Research',
        'year': 2023,
        'arxiv_id': '2005.11401',
        'title': 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks',
        'abstract': 'We explore retrieval-augmented generation (RAG) models which combine pre-trained parametric and non-parametric memory for language generation. Our RAG models treat the input sequence as a query, retrieve top-K relevant passages, then generate the output conditioned on these passages.',
    },
    {
        'filename': 'neural_scaling_laws_2022.pdf',
        'name': 'Jared Kaplan',
        'email': 'jkaplan@openai.com',
        'affiliation': 'OpenAI',
        'year': 2022,
        'arxiv_id': '2001.08361',
        'title': 'Scaling Laws for Neural Language Models',
        'abstract': 'We study empirical scaling laws for language model performance on the cross-entropy loss. The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning more than seven orders of magnitude.',
    },
    {
        'filename': 'contrastive_learning_2021.pdf',
        'name': 'Ting Chen',
        'email': 'tingchen@google.com',
        'affiliation': 'Google Research, Brain Team',
        'year': 2021,
        'arxiv_id': '2002.05709',
        'title': 'A Simple Framework for Contrastive Learning of Visual Representations',
        'abstract': 'This paper presents SimCLR: a simple framework for contrastive learning of visual representations. We simplify recently proposed contrastive self-supervised learning algorithms without requiring specialized architectures or a memory bank.',
    },
    {
        'filename': 'code_generation_llm_2024.pdf',
        'name': 'Baptiste Roziere',
        'email': 'roziere@meta.com',
        'affiliation': 'Meta AI',
        'year': 2024,
        'arxiv_id': '2308.12950',
        'title': 'Code Llama: Open Foundation Models for Code',
        'abstract': 'We release Code Llama, a family of large language models for code based on Llama 2. Code Llama provides state-of-the-art performance among open models, infilling capabilities, support for large input contexts, and zero-shot instruction following ability for programming tasks.',
    },
    {
        'filename': 'reward_model_rlhf_2024.pdf',
        'name': 'Nisan Stiennon',
        'email': 'nisan@openai.com',
        'affiliation': 'OpenAI',
        'year': 2024,
        'arxiv_id': '2009.01325',
        'title': 'Learning to summarize from human feedback',
        'abstract': 'As language models become more powerful, training and evaluation are increasingly bottlenecked by access to high-quality human feedback. We apply reinforcement learning from human feedback to the task of abstractive summarization.',
    },
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


def create_arxiv_pdf(paper: dict, output_path: str):
    """Create a realistic arXiv-style PDF preprint using fpdf2."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Set margins (arXiv uses ~1 inch margins)
    pdf.set_left_margin(25)
    pdf.set_right_margin(25)
    pdf.set_top_margin(20)

    # --- arXiv header / timestamp area ---
    pdf.set_font('Helvetica', size=8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"arXiv:{paper['arxiv_id']}  [cs.LG]  Submitted {paper['year']}-03-15", ln=True)
    pdf.ln(3)

    # --- Title ---
    pdf.set_font('Helvetica', 'B', size=16)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, paper['title'])
    pdf.ln(4)

    # --- Author block ---
    pdf.set_font('Helvetica', 'B', size=12)
    pdf.cell(0, 6, paper['name'], ln=True)

    pdf.set_font('Helvetica', size=10)
    pdf.set_text_color(50, 50, 150)
    # Footnote-style email (common in arXiv papers)
    pdf.cell(0, 5, paper['email'], ln=True)

    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, paper['affiliation'], ln=True)
    pdf.ln(6)

    # --- Abstract section ---
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', 'B', size=11)
    pdf.cell(0, 6, 'Abstract', ln=True)
    pdf.ln(2)
    pdf.set_font('Helvetica', size=10)
    pdf.multi_cell(0, 5, paper['abstract'])
    pdf.ln(6)

    # --- Introduction section ---
    pdf.set_font('Helvetica', 'B', size=11)
    pdf.cell(0, 6, '1  Introduction', ln=True)
    pdf.ln(2)
    pdf.set_font('Helvetica', size=10)
    intro_text = (
        f"The field of machine learning has seen rapid advances in recent years. "
        f"In this work, we present {paper['title'].split(':')[0].strip()}, a novel approach "
        "that addresses key challenges in the domain. Our contributions are as follows: "
        "(1) We propose a new methodology with clear theoretical foundations; "
        "(2) We demonstrate state-of-the-art results on multiple benchmarks; "
        "(3) We release code and models to facilitate reproducibility."
    )
    pdf.multi_cell(0, 5, intro_text)
    pdf.ln(4)

    # --- Method section ---
    pdf.set_font('Helvetica', 'B', size=11)
    pdf.cell(0, 6, '2  Method', ln=True)
    pdf.ln(2)
    pdf.set_font('Helvetica', size=10)
    method_text = (
        "Our approach builds on recent advances in deep learning and leverages large-scale "
        "pre-training to achieve robust performance. We employ a transformer-based architecture "
        "with modifications to improve efficiency and scalability. Specifically, our model "
        "incorporates attention mechanisms that enable fine-grained reasoning while maintaining "
        "computational tractability at scale."
    )
    pdf.multi_cell(0, 5, method_text)
    pdf.ln(4)

    # --- Experiments section ---
    pdf.set_font('Helvetica', 'B', size=11)
    pdf.cell(0, 6, '3  Experiments', ln=True)
    pdf.ln(2)
    pdf.set_font('Helvetica', size=10)
    exp_text = (
        "We evaluate our approach on standard benchmarks including GLUE, SuperGLUE, and several "
        "domain-specific datasets. Our model achieves competitive performance across all tasks, "
        "with significant improvements on challenging benchmarks. We conduct ablation studies "
        "to understand the contribution of each component."
    )
    pdf.multi_cell(0, 5, exp_text)

    pdf.output(output_path)


def create_initial():
    # Create Downloads/Preprints directory
    os.makedirs(PREPRINTS_DIR, exist_ok=True)
    print(f'Created directory: {PREPRINTS_DIR}')

    # Generate all 9 PDFs
    for paper in PAPERS:
        out_path = os.path.join(PREPRINTS_DIR, paper['filename'])
        create_arxiv_pdf(paper, out_path)
        print(f'Created PDF: {out_path}')

    print(f'All {len(PAPERS)} PDFs created in {PREPRINTS_DIR}')

    # GUI-ready startup: Open Nautilus at the Preprints folder
    launch_gui(f'nautilus "{PREPRINTS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus at ~/Downloads/Preprints with DISPLAY=:0')


create_initial()
