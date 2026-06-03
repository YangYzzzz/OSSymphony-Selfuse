"""
Initial Setup: Create 6 AI survey PDFs in ~/Documents/AI_Survey with first author info
Task ID: osworld_multi_apps_pdf_author_extract_004
Domain: libreoffice_calc (multi-app: PDF + Calc)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_author_extract_004'
SURVEY_DIR = f'{WORKDIR}/Documents/AI_Survey'

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


def create_pdfs():
    """Create 6 realistic AI survey PDF papers using fpdf2."""
    try:
        from fpdf import FPDF
    except ImportError:
        import subprocess as sp
        sp.run(["pip3", "install", "fpdf2"], check=True)
        from fpdf import FPDF

    os.makedirs(SURVEY_DIR, exist_ok=True)

    # 6 papers with distinct first authors — sorted by last name for reference:
    # Chen, Fischer, Huang, Kumar, Nakamura, Rodriguez
    papers = [
        {
            "filename": "survey_transformer_architectures.pdf",
            "title": "A Comprehensive Survey of Transformer Architectures in Natural Language Processing",
            "author": "David Chen",
            "email": "d.chen@mit.edu",
            "institution": "MIT CSAIL",
            "coauthors": "Linda Park, Robert Zhao",
            "abstract": (
                "Transformer models have fundamentally reshaped the field of natural language processing "
                "since their introduction in 2017. This survey provides a comprehensive overview of transformer "
                "architecture variants, including encoder-only, decoder-only, and encoder-decoder designs. "
                "We analyze over 150 seminal papers, categorize architectural innovations, and benchmark "
                "performance across 12 standard NLP datasets. Our analysis reveals key trends in scaling, "
                "efficiency, and multi-modal capabilities."
            ),
            "year": 2024,
            "venue": "ACM Computing Surveys",
        },
        {
            "filename": "survey_reinforcement_learning_robotics.pdf",
            "title": "Reinforcement Learning for Robotic Manipulation: A Survey",
            "author": "Emma Fischer",
            "email": "e.fischer@stanford.edu",
            "institution": "Stanford University",
            "coauthors": "Thomas Bauer, Aisha Ndiaye",
            "abstract": (
                "The application of reinforcement learning to robotic manipulation tasks has seen "
                "explosive growth over the past decade. This survey examines 200+ papers spanning "
                "model-free and model-based RL approaches, sim-to-real transfer techniques, and "
                "multi-task learning strategies. We identify open challenges in sample efficiency, "
                "safety constraints, and real-world deployment. Particular attention is paid to "
                "recent advances in diffusion-based policy learning and language-conditioned control."
            ),
            "year": 2024,
            "venue": "IEEE Transactions on Robotics",
        },
        {
            "filename": "survey_graph_neural_networks.pdf",
            "title": "Graph Neural Networks: Methods, Applications, and Opportunities",
            "author": "James Huang",
            "email": "j.huang@berkeley.edu",
            "institution": "UC Berkeley",
            "coauthors": "Maria Santos, Kevin Osei",
            "abstract": (
                "Graph neural networks (GNNs) have emerged as a powerful framework for learning "
                "representations of graph-structured data. This survey provides a systematic review "
                "of GNN variants including graph convolutional networks, graph attention networks, "
                "and message passing neural networks. We cover applications in molecular property "
                "prediction, social network analysis, knowledge graph reasoning, and combinatorial "
                "optimization. Theoretical foundations, expressive power, and scalability challenges "
                "are discussed in depth."
            ),
            "year": 2023,
            "venue": "Journal of Machine Learning Research",
        },
        {
            "filename": "survey_federated_learning.pdf",
            "title": "Federated Learning: Advances in Privacy-Preserving Distributed Machine Learning",
            "author": "Priya Kumar",
            "email": "p.kumar@cmu.edu",
            "institution": "Carnegie Mellon University",
            "coauthors": "Yusuf Al-Rashid, Claire Dupont",
            "abstract": (
                "Federated learning enables model training across decentralized devices without "
                "centralizing sensitive data. This comprehensive survey covers federated optimization "
                "algorithms, communication efficiency techniques, differential privacy integration, "
                "and Byzantine fault tolerance. We review 180 papers published between 2017 and 2024, "
                "highlighting practical deployments in healthcare, finance, and mobile applications. "
                "Key challenges including statistical heterogeneity, system heterogeneity, and "
                "privacy-utility trade-offs are systematically analyzed."
            ),
            "year": 2024,
            "venue": "Foundations and Trends in Machine Learning",
        },
        {
            "filename": "survey_vision_language_models.pdf",
            "title": "Vision-Language Models: A Survey of Multimodal Learning and Applications",
            "author": "Alexander Nakamura",
            "email": "a.nakamura@caltech.edu",
            "institution": "California Institute of Technology",
            "coauthors": "Brigitte Leclerc, Samuel Okonkwo",
            "abstract": (
                "Vision-language models (VLMs) that jointly process visual and textual information "
                "have achieved remarkable results on tasks ranging from image captioning to visual "
                "question answering. This survey reviews 220 papers on contrastive learning methods, "
                "generative vision-language architectures, and grounding techniques. We analyze "
                "benchmark performance on 25 evaluation datasets and provide a taxonomy of model "
                "families including CLIP-style models, large multimodal models, and specialized "
                "domain adaptations in medical imaging and autonomous driving."
            ),
            "year": 2024,
            "venue": "Proceedings of the IEEE",
        },
        {
            "filename": "survey_neural_architecture_search.pdf",
            "title": "Neural Architecture Search: Current Methods and Future Directions",
            "author": "Sofia Rodriguez",
            "email": "s.rodriguez@utexas.edu",
            "institution": "University of Texas at Austin",
            "coauthors": "Dmitri Volkov, Hina Tanaka",
            "abstract": (
                "Neural architecture search (NAS) automates the design of deep learning models, "
                "reducing the need for expert knowledge in architecture engineering. This survey "
                "classifies NAS methods into three main paradigms: evolutionary algorithms, "
                "reinforcement learning-based search, and gradient-based differentiable search. "
                "We compare search spaces, search strategies, and performance estimation approaches "
                "across 160 papers. Hardware-aware NAS, one-shot methods, and zero-shot proxies "
                "receive special attention given their practical significance."
            ),
            "year": 2023,
            "venue": "IEEE Transactions on Neural Networks and Learning Systems",
        },
    ]

    for paper in papers:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Title
        pdf.set_font("Helvetica", style="B", size=14)
        pdf.set_xy(15, 20)
        pdf.multi_cell(180, 8, paper["title"], align="C")

        # Authors line
        pdf.ln(4)
        all_authors = f"{paper['author']}, {paper['coauthors']}"
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(180, 7, all_authors, align="C")

        # Author info block
        pdf.ln(2)
        author_info = (
            f"{paper['author']}  |  {paper['email']}  |  {paper['institution']}"
        )
        pdf.set_font("Helvetica", style="I", size=10)
        pdf.multi_cell(180, 6, author_info, align="C")

        # Venue and year
        pdf.ln(2)
        venue_line = f"{paper['venue']}, {paper['year']}"
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(180, 6, venue_line, align="C")

        # Divider
        pdf.ln(4)
        pdf.set_draw_color(100, 100, 100)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(4)

        # Abstract heading
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.cell(0, 7, "Abstract", ln=True)
        pdf.ln(1)

        # Abstract text
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(180, 6, paper["abstract"])

        pdf.ln(6)

        # Introduction section
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.cell(0, 7, "1. Introduction", ln=True)
        pdf.ln(1)
        pdf.set_font("Helvetica", size=10)
        intro_text = (
            "The rapid advancement of artificial intelligence has produced a rich landscape of methods "
            "and applications. This survey aims to provide researchers and practitioners with a "
            "structured overview of the current state of the field, identifying key developments, "
            "persistent challenges, and promising directions for future work. "
            "We systematically reviewed papers from major AI venues including NeurIPS, ICML, ICLR, "
            "CVPR, ACL, and relevant journals over the past five years."
        )
        pdf.multi_cell(180, 6, intro_text)

        pdf.ln(4)
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.cell(0, 7, "2. Background and Related Work", ln=True)
        pdf.ln(1)
        pdf.set_font("Helvetica", size=10)
        bg_text = (
            "Prior surveys in this domain have focused on specific subproblems or limited time "
            "windows. Our work extends these efforts by incorporating the most recent literature "
            "and providing a unified taxonomy that spans multiple research threads. We refer readers "
            "to foundational textbooks for background on deep learning and statistical machine "
            "learning methods."
        )
        pdf.multi_cell(180, 6, bg_text)

        output_path = os.path.join(SURVEY_DIR, paper["filename"])
        pdf.output(output_path)
        print(f"Created PDF: {output_path}")

    print(f"\nAll 6 survey PDFs created in: {SURVEY_DIR}")


def create_initial():
    create_pdfs()

    # Verify that survey_authors.xlsx does NOT exist in home (pre-task state)
    survey_xlsx = f'{WORKDIR}/survey_authors.xlsx'
    if os.path.exists(survey_xlsx):
        os.remove(survey_xlsx)
        print(f"Removed pre-existing {survey_xlsx} to ensure clean initial state")

    # GUI-ready startup: open Nautilus at the AI_Survey folder
    launch_gui(f'nautilus "{SURVEY_DIR}"', delay_sec=2.0)
    print('GUI_READY: Nautilus opened at AI_Survey directory with DISPLAY=:0')


create_initial()
