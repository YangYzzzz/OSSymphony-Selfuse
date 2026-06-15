"""
Initial Setup: Extract first-author details from workshop PDF files
Task ID: osworld_multi_apps_pdf_author_extract_010
Domain: multi_apps (PDF creation + LibreOffice Calc)

Creates 8 PDF workshop paper files in ~/Documents/Workshop_Papers/
Each PDF contains first-author metadata (name, email, affiliation, country).
Opens Nautilus on the Workshop_Papers folder to show the GUI start state.
The target file ~/workshop_authors.xlsx does NOT exist initially.
"""

import os
import shlex
import subprocess
import time

try:
    from fpdf import FPDF
except ImportError:
    import subprocess as _sp
    _sp.run(["pip3", "install", "fpdf2"], check=True)
    from fpdf import FPDF

WORKDIR = '/home/user'
PAPERS_DIR = f'{WORKDIR}/Documents/Workshop_Papers'
TASK_ID = 'osworld_multi_apps_pdf_author_extract_010'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch a GUI app on the VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


# Define 8 realistic workshop paper first authors
# Intentionally NOT sorted — the agent must sort them
PAPERS = [
    {
        "filename": "workshop_paper_001.pdf",
        "title": "Advances in Neural Architecture Search for Edge Devices",
        "authors": [
            {"name": "James Anderson", "email": "j.anderson@ucl.ac.uk",
             "affiliation": "University College London", "country": "United Kingdom"},
            {"name": "Robert Hughes", "email": "r.hughes@ucl.ac.uk",
             "affiliation": "University College London", "country": "United Kingdom"},
        ],
        "abstract": (
            "This paper presents a novel approach to neural architecture search "
            "specifically tailored for deployment on resource-constrained edge devices. "
            "Our method reduces search time by 40% while maintaining competitive accuracy."
        ),
        "venue": "Workshop on Efficient Deep Learning, NeurIPS 2024",
    },
    {
        "filename": "workshop_paper_002.pdf",
        "title": "Cross-Lingual Transfer Learning in Low-Resource NLP Settings",
        "authors": [
            {"name": "Priya Sharma", "email": "priya.sharma@iitb.ac.in",
             "affiliation": "IIT Bombay", "country": "India"},
            {"name": "Ankit Gupta", "email": "ankit.gupta@iitb.ac.in",
             "affiliation": "IIT Bombay", "country": "India"},
            {"name": "Meena Krishnan", "email": "N/A",
             "affiliation": "Infosys Research", "country": "India"},
        ],
        "abstract": (
            "We investigate cross-lingual transfer for NLP in low-resource language settings. "
            "Experiments on 12 languages show that our adapter-based approach outperforms "
            "full fine-tuning in data-scarce regimes by up to 8.3 F1 points."
        ),
        "venue": "Workshop on Low-Resource NLP, ACL 2024",
    },
    {
        "filename": "workshop_paper_003.pdf",
        "title": "Temporal Knowledge Graph Completion with Recurrent Embeddings",
        "authors": [
            {"name": "Chen Wei", "email": "chen.wei@tsinghua.edu.cn",
             "affiliation": "Tsinghua University", "country": "China"},
            {"name": "Zhang Lei", "email": "zhanglei@tsinghua.edu.cn",
             "affiliation": "Tsinghua University", "country": "China"},
        ],
        "abstract": (
            "Temporal knowledge graphs encode time-stamped relational facts. "
            "We propose a recurrent embedding model that captures temporal dynamics "
            "and achieves state-of-the-art results on ICEWS and GDELT benchmarks."
        ),
        "venue": "Workshop on Knowledge Graph Reasoning, ISWC 2024",
    },
    {
        "filename": "workshop_paper_004.pdf",
        "title": "Fairness-Aware Recommendation Systems Using Counterfactual Explanations",
        "authors": [
            {"name": "Marie Dubois", "email": "N/A",
             "affiliation": "INRIA Paris", "country": "France"},
            {"name": "Pierre Laurent", "email": "p.laurent@inria.fr",
             "affiliation": "INRIA Paris", "country": "France"},
        ],
        "abstract": (
            "We address algorithmic bias in recommendation systems by incorporating "
            "counterfactual explanations into the training objective. "
            "Our approach improves fairness metrics without sacrificing recommendation quality."
        ),
        "venue": "Workshop on Responsible AI, ECML-PKDD 2024",
    },
    {
        "filename": "workshop_paper_005.pdf",
        "title": "Scalable Federated Learning with Heterogeneous Client Data Distributions",
        "authors": [
            {"name": "Anna Muller", "email": "a.mueller@tu-berlin.de",
             "affiliation": "TU Berlin", "country": "Germany"},
            {"name": "Klaus Weber", "email": "k.weber@tu-berlin.de",
             "affiliation": "TU Berlin", "country": "Germany"},
            {"name": "Sophie Braun", "email": "s.braun@dfki.de",
             "affiliation": "DFKI", "country": "Germany"},
        ],
        "abstract": (
            "Federated learning faces challenges when client data is heterogeneous. "
            "We propose FedAdapt, a communication-efficient aggregation strategy that "
            "adapts learning rates per client cluster, reducing convergence rounds by 35%."
        ),
        "venue": "Workshop on Federated Learning, ICML 2024",
    },
    {
        "filename": "workshop_paper_006.pdf",
        "title": "Zero-Shot Compositional Visual Reasoning with Structured Prompts",
        "authors": [
            {"name": "Emily Thompson", "email": "emily.thompson@mit.edu",
             "affiliation": "Massachusetts Institute of Technology", "country": "United States"},
            {"name": "David Park", "email": "dpark@mit.edu",
             "affiliation": "Massachusetts Institute of Technology", "country": "United States"},
        ],
        "abstract": (
            "We explore zero-shot compositional visual reasoning using structured prompt "
            "engineering with large vision-language models. Our prompting framework "
            "improves accuracy by 12% on CLEVR and 9% on GQA benchmarks."
        ),
        "venue": "Workshop on Vision and Language, CVPR 2024",
    },
    {
        "filename": "workshop_paper_007.pdf",
        "title": "Continual Learning for Medical Image Segmentation Across Imaging Modalities",
        "authors": [
            {"name": "Yuki Tanaka", "email": "y.tanaka@nii.ac.jp",
             "affiliation": "National Institute of Informatics", "country": "Japan"},
            {"name": "Hiroshi Nakamura", "email": "h.nakamura@nii.ac.jp",
             "affiliation": "National Institute of Informatics", "country": "Japan"},
        ],
        "abstract": (
            "Medical imaging AI systems must adapt to new imaging modalities without "
            "forgetting previous tasks. We present a continual learning framework that "
            "achieves robust segmentation performance across CT, MRI, and ultrasound."
        ),
        "venue": "Workshop on Medical Image Analysis, MICCAI 2024",
    },
    {
        "filename": "workshop_paper_008.pdf",
        "title": "Graph Neural Networks for Protein-Ligand Binding Affinity Prediction",
        "authors": [
            {"name": "Liu Fang", "email": "liu.fang@pku.edu.cn",
             "affiliation": "Peking University", "country": "China"},
            {"name": "Wang Jian", "email": "wangjian@pku.edu.cn",
             "affiliation": "Peking University", "country": "China"},
            {"name": "Xu Ming", "email": "xuming@pku.edu.cn",
             "affiliation": "Peking University", "country": "China"},
        ],
        "abstract": (
            "Accurate prediction of protein-ligand binding affinity is critical for "
            "drug discovery. We propose AttentionGNN, a graph neural network with "
            "multi-head attention that achieves Pearson r=0.88 on the PDBbind benchmark."
        ),
        "venue": "Workshop on Machine Learning for Drug Discovery, ICLR 2024",
    },
]


def create_paper_pdf(paper: dict, output_path: str):
    """Create a realistic workshop paper PDF with first-author metadata."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.set_xy(20, 20)
    pdf.multi_cell(170, 8, paper["title"], align="C")
    pdf.ln(4)

    # Authors section
    pdf.set_font("Helvetica", size=11)
    first = True
    for author in paper["authors"]:
        if first:
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.set_text_color(0, 0, 150)
            pdf.cell(0, 6, f"First Author: {author['name']}", ln=True, align="C")
            pdf.set_font("Helvetica", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 5, f"Email: {author['email']}", ln=True, align="C")
            pdf.cell(0, 5, f"Affiliation: {author['affiliation']}", ln=True, align="C")
            pdf.cell(0, 5, f"Country: {author['country']}", ln=True, align="C")
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", size=11)
            first = False
        else:
            pdf.cell(0, 5, f"{author['name']} ({author['affiliation']})", ln=True, align="C")
    pdf.ln(4)

    # Venue
    pdf.set_font("Helvetica", style="I", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, paper["venue"], ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    # Horizontal rule
    pdf.set_draw_color(150, 150, 150)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(4)

    # Abstract
    pdf.set_font("Helvetica", style="B", size=11)
    pdf.cell(0, 6, "Abstract", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 5, paper["abstract"])
    pdf.ln(4)

    # Introduction placeholder
    pdf.set_font("Helvetica", style="B", size=11)
    pdf.cell(0, 6, "1. Introduction", ln=True)
    pdf.set_font("Helvetica", size=10)
    intro = (
        "Recent advances in machine learning have opened new avenues for tackling "
        "complex real-world problems. In this work, we build upon prior research to "
        "propose novel techniques with empirical validation across standard benchmarks."
    )
    pdf.multi_cell(0, 5, intro)
    pdf.ln(2)

    # Method placeholder
    pdf.set_font("Helvetica", style="B", size=11)
    pdf.cell(0, 6, "2. Methodology", ln=True)
    pdf.set_font("Helvetica", size=10)
    method = (
        "Our proposed framework consists of three main components: a feature extraction "
        "module, a task-specific adaptation layer, and an evaluation pipeline. We describe "
        "each component in detail and provide complexity analysis."
    )
    pdf.multi_cell(0, 5, method)
    pdf.ln(2)

    # Experiments
    pdf.set_font("Helvetica", style="B", size=11)
    pdf.cell(0, 6, "3. Experiments", ln=True)
    pdf.set_font("Helvetica", size=10)
    experiments = (
        "We evaluate our approach on multiple benchmark datasets. Results demonstrate "
        "significant improvements over baselines. Ablation studies confirm the contribution "
        "of each component to overall performance."
    )
    pdf.multi_cell(0, 5, experiments)
    pdf.ln(2)

    # Conclusion
    pdf.set_font("Helvetica", style="B", size=11)
    pdf.cell(0, 6, "4. Conclusion", ln=True)
    pdf.set_font("Helvetica", size=10)
    conclusion = (
        "We presented a novel approach that achieves strong performance on the target task. "
        "Future work will explore scaling to larger datasets and extending the framework "
        "to additional application domains."
    )
    pdf.multi_cell(0, 5, conclusion)

    pdf.output(output_path)


def create_initial():
    # Ensure the Papers directory exists
    os.makedirs(PAPERS_DIR, exist_ok=True)

    # Create each PDF
    for paper in PAPERS:
        output_path = os.path.join(PAPERS_DIR, paper["filename"])
        create_paper_pdf(paper, output_path)
        print(f"Created: {output_path}")

    # Verify workshop_authors.xlsx does NOT exist (task target must not pre-exist)
    target = os.path.join(WORKDIR, 'workshop_authors.xlsx')
    if os.path.exists(target):
        os.remove(target)
        print(f"Removed pre-existing: {target}")

    print(f"\nAll 8 PDF workshop papers created in: {PAPERS_DIR}")
    print("Target file ~/workshop_authors.xlsx does not exist (as required).")

    # GUI-ready startup: open Nautilus on the Workshop_Papers folder
    launch_gui(f'nautilus "{PAPERS_DIR}"', delay_sec=2.0)
    print("GUI_READY: launched Nautilus on Workshop_Papers directory with DISPLAY=:0")


create_initial()
