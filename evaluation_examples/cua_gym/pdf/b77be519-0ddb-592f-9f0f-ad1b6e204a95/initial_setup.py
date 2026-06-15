"""
Initial Setup: Create a 60-page thesis PDF with existing bookmarks for Ch1 and Ch2.
Task ID: pdf_fm_018
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_018'
OUTPUT = f'{WORKDIR}/Documents/thesis_final.pdf'

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

# Chapter structure: title, start page (1-indexed), subsections
CHAPTERS = [
    {
        "title": "Chapter 1: Introduction",
        "page": 1,
        "subs": [
            ("1.1 Background and Motivation", 1),
            ("1.2 Research Questions", 3),
            ("1.3 Scope and Limitations", 4),
            ("1.4 Thesis Outline", 5),
        ],
    },
    {
        "title": "Chapter 2: Literature Review",
        "page": 6,
        "subs": [
            ("2.1 Theoretical Framework", 6),
            ("2.2 Previous Studies", 8),
            ("2.3 Gaps in the Literature", 11),
            ("2.4 Summary", 14),
        ],
    },
    # Chapter 3 starts at page 15 but NO bookmark for it in initial
    # Chapter 4-6 have no bookmarks either (thesis is a work in progress)
]

# Thesis content templates per page range
PAGE_CONTENT = {
    # Chapter 1: Introduction (pages 1-5)
    1: ("Chapter 1: Introduction",
        "The rapid advancement of machine learning techniques has fundamentally transformed "
        "how we approach complex optimization problems in computational biology. This thesis "
        "investigates the application of deep reinforcement learning methods to protein "
        "structure prediction, a problem that has remained one of the grand challenges in "
        "bioinformatics for over five decades.\n\n"
        "The ability to predict three-dimensional protein structures from amino acid sequences "
        "has profound implications for drug discovery, enzyme engineering, and our fundamental "
        "understanding of biological processes. Despite significant progress, current methods "
        "still face challenges with multi-domain proteins, intrinsically disordered regions, "
        "and computational efficiency at scale."),
    2: ("",
        "Recent breakthroughs by AlphaFold and RoseTTAFold have demonstrated that deep "
        "learning architectures can achieve remarkable accuracy in protein structure prediction. "
        "However, these methods rely heavily on multiple sequence alignments and template-based "
        "approaches, which may not generalize well to orphan proteins or rapidly evolving viral "
        "sequences.\n\n"
        "Our approach differs fundamentally by framing protein folding as a sequential "
        "decision-making problem, where a reinforcement learning agent learns to manipulate "
        "torsion angles along the backbone to minimize free energy. This formulation naturally "
        "captures the physical constraints of the folding process and allows the agent to "
        "develop intuitions about local and global structural motifs."),
    3: ("1.2 Research Questions",
        "This thesis addresses the following research questions:\n\n"
        "RQ1: Can deep reinforcement learning agents learn effective protein folding strategies "
        "that generalize across protein families?\n\n"
        "RQ2: How does the choice of state representation affect the agent's ability to capture "
        "long-range interactions in protein structures?\n\n"
        "RQ3: What is the computational trade-off between accuracy and efficiency when comparing "
        "RL-based methods with traditional molecular dynamics simulations?\n\n"
        "RQ4: Can transfer learning from simulated folding environments improve prediction "
        "accuracy on real-world protein structures?"),
    4: ("1.3 Scope and Limitations",
        "This research focuses specifically on single-chain proteins with fewer than 500 "
        "residues. Multi-chain complexes and membrane proteins are excluded from the current "
        "analysis due to the additional complexity of modeling inter-chain interactions and "
        "lipid bilayer environments.\n\n"
        "The reinforcement learning experiments were conducted using a coarse-grained "
        "representation of protein structures, which trades atomic-level precision for "
        "computational efficiency. All simulations were performed on NVIDIA A100 GPUs with "
        "a total compute budget of approximately 12,000 GPU-hours."),
    5: ("1.4 Thesis Outline",
        "The remainder of this thesis is organized as follows:\n\n"
        "Chapter 2 provides a comprehensive review of the literature on protein structure "
        "prediction, reinforcement learning, and their intersection.\n\n"
        "Chapter 3 describes the methodology, including the RL environment design, reward "
        "function formulation, and neural network architectures employed.\n\n"
        "Chapter 4 presents the experimental setup, datasets, and baseline comparisons.\n\n"
        "Chapter 5 reports and discusses the experimental results.\n\n"
        "Chapter 6 concludes the thesis and suggests directions for future work."),

    # Chapter 2: Literature Review (pages 6-14)
    6: ("Chapter 2: Literature Review",
        "This chapter surveys the relevant literature across three interconnected domains: "
        "protein structure prediction, deep learning for molecular modeling, and reinforcement "
        "learning for scientific discovery.\n\n"
        "2.1 Theoretical Framework\n\n"
        "The protein folding problem, first articulated by Anfinsen in 1973, posits that the "
        "native structure of a protein is determined entirely by its amino acid sequence. This "
        "thermodynamic hypothesis suggests that the folded state corresponds to the global "
        "minimum of the Gibbs free energy landscape."),
    7: ("",
        "Levinthal's paradox highlights the astronomical size of the conformational search "
        "space: a protein with 100 residues has approximately 3^198 possible backbone "
        "configurations, making exhaustive enumeration physically impossible. This paradox "
        "implies that proteins must follow specific folding pathways rather than random "
        "exploration, a principle that motivates our reinforcement learning approach.\n\n"
        "The energy landscape theory, developed by Wolynes, Onuchic, and Bryngelson, provides "
        "a statistical mechanics framework for understanding protein folding. According to this "
        "theory, evolution has shaped protein sequences to have funneled energy landscapes that "
        "guide the folding process toward the native state."),
    8: ("2.2 Previous Studies",
        "Template-based methods such as MODELLER and SWISS-MODEL have been the workhorses of "
        "protein structure prediction for decades. These methods identify structurally "
        "characterized homologs and use them as templates to build models of the target "
        "sequence. While highly effective when good templates are available, these methods "
        "fail for novel folds.\n\n"
        "Ab initio methods, including Rosetta and I-TASSER, attempt to predict structures "
        "without relying on templates. These methods typically use fragment assembly combined "
        "with physics-based and knowledge-based energy functions."),
    9: ("",
        "The emergence of deep learning has catalyzed a paradigm shift in structure prediction. "
        "Convolutional neural networks for residue-residue contact prediction, as demonstrated "
        "by MetaPSICOV and RaptorX, showed that learning from evolutionary covariance patterns "
        "could provide valuable structural information.\n\n"
        "AlphaFold2 represented a watershed moment, achieving atomic-level accuracy across "
        "a wide range of protein targets in CASP14. Its architecture combines a sophisticated "
        "attention mechanism (Evoformer) with an iterative structure refinement module that "
        "operates on an invariant point attention representation."),
    10: ("",
         "Despite AlphaFold2's success, several limitations remain:\n\n"
         "1. Dependence on multiple sequence alignments (MSAs), which are unavailable for "
         "orphan proteins and computationally expensive to generate.\n\n"
         "2. Limited ability to model conformational ensembles and intrinsically disordered "
         "regions.\n\n"
         "3. Challenges with predicting the effects of mutations on protein stability and "
         "function.\n\n"
         "4. Difficulty handling multi-state proteins that adopt different conformations "
         "depending on environmental conditions."),
    11: ("2.3 Gaps in the Literature",
         "While reinforcement learning has been applied to molecular design and drug "
         "discovery, its application to protein structure prediction remains relatively "
         "unexplored. Zhou et al. (2023) proposed an RL-based approach for side-chain "
         "packing, but did not address backbone folding.\n\n"
         "Chen and Wang (2024) demonstrated that policy gradient methods could learn "
         "effective folding strategies for small peptides (< 50 residues), but their "
         "approach did not scale to larger proteins due to the curse of dimensionality "
         "in the action space."),
    12: ("",
         "Graph neural networks have shown promise in representing protein structures as "
         "graphs where residues are nodes and edges represent spatial proximity or sequence "
         "connectivity. However, integrating graph-based representations with RL frameworks "
         "remains an open research problem.\n\n"
         "Multi-agent reinforcement learning, where different agents control different "
         "regions of the protein chain, offers a potential solution to the scalability "
         "challenge but introduces coordination difficulties that have not been adequately "
         "addressed in the literature."),
    13: ("",
         "Recent work on diffusion models for protein structure generation (e.g., RFdiffusion) "
         "suggests that generative approaches may complement or even replace traditional "
         "structure prediction methods. However, these models currently lack the ability to "
         "incorporate specific physical constraints during the generation process.\n\n"
         "The intersection of reinforcement learning with physics-informed neural networks "
         "presents another promising but underexplored direction. By incorporating physical "
         "laws as inductive biases, RL agents could potentially learn more efficient and "
         "accurate folding strategies."),
    14: ("2.4 Summary",
         "This literature review has identified several key gaps that this thesis aims to "
         "address:\n\n"
         "1. The lack of RL-based methods for full backbone protein folding at scale.\n"
         "2. The need for state representations that capture long-range interactions.\n"
         "3. The absence of systematic comparisons between RL and physics-based approaches.\n"
         "4. The potential for transfer learning to improve sample efficiency.\n\n"
         "The following chapter describes our methodology for addressing these gaps through "
         "a novel deep reinforcement learning framework for protein structure prediction."),

    # Chapter 3: Methodology (pages 15-24)
    15: ("Chapter 3: Methodology",
         "This chapter presents the methodological framework for applying deep reinforcement "
         "learning to protein structure prediction. We describe the formulation of the folding "
         "problem as a Markov Decision Process (MDP), the design of the state and action "
         "spaces, the reward function, and the neural network architectures employed.\n\n"
         "3.1 Problem Formulation\n\n"
         "We model protein folding as an episodic MDP where the agent sequentially determines "
         "the torsion angles (phi, psi, omega) for each residue along the protein backbone."),
    16: ("",
         "The state space S consists of the current partial protein structure, represented "
         "as a graph with node features encoding amino acid types, secondary structure "
         "predictions, and evolutionary information from position-specific scoring matrices.\n\n"
         "The action space A is defined as the set of discretized torsion angle adjustments. "
         "We discretize the phi and psi angles into 36 bins (10 degrees each), resulting "
         "in 1,296 possible actions per residue. The omega angle is fixed at 180 degrees "
         "for trans peptide bonds."),
    17: ("3.2 Reward Function Design",
         "The reward function plays a critical role in guiding the RL agent toward physically "
         "realistic protein structures. We design a multi-component reward:\n\n"
         "R(s, a) = w1 * R_energy(s) + w2 * R_clash(s) + w3 * R_secondary(s) + w4 * R_contact(s)\n\n"
         "where R_energy measures the change in estimated free energy, R_clash penalizes "
         "steric clashes between atoms, R_secondary rewards consistency with predicted "
         "secondary structure, and R_contact rewards formation of native-like residue contacts."),
    18: ("3.3 Neural Network Architecture",
         "Our policy network combines a graph attention network (GAT) for processing the "
         "protein structure graph with a transformer encoder for capturing sequence-level "
         "features. The architecture processes:\n\n"
         "1. Node features: amino acid type (20-dim one-hot), secondary structure prediction "
         "(3-dim), PSSM profile (20-dim), and positional encoding (32-dim).\n\n"
         "2. Edge features: sequential distance, Euclidean distance between C-alpha atoms, "
         "and angular features between residue pairs.\n\n"
         "3. Global features: protein length, amino acid composition, and estimated difficulty."),
    19: ("3.4 Training Procedure",
         "We employ Proximal Policy Optimization (PPO) with several modifications for the "
         "protein folding task:\n\n"
         "- Curriculum learning: training begins with short peptides (20-30 residues) and "
         "gradually increases to longer chains (up to 500 residues).\n\n"
         "- Experience replay with prioritized sampling based on the magnitude of the temporal "
         "difference error.\n\n"
         "- Multi-task learning across different protein families to encourage generalization.\n\n"
         "The training was conducted over 5 million episodes on a cluster of 32 NVIDIA A100 "
         "GPUs, requiring approximately 12,000 GPU-hours."),

    # Chapter 4: Experimental Setup (pages 20-34)
    20: ("Chapter 4: Experimental Setup",
         "This chapter details the experimental design, including dataset selection, "
         "baseline methods, evaluation metrics, and computational infrastructure.\n\n"
         "4.1 Datasets\n\n"
         "We curated a benchmark dataset from the Protein Data Bank (PDB), consisting of "
         "15,287 non-redundant protein structures with sequence identity below 30%. The "
         "dataset was split into training (80%), validation (10%), and test (10%) sets, "
         "stratified by SCOP superfamily to prevent data leakage."),
}

def create_initial():
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    doc = pymupdf.open()

    # Create 60 pages with thesis-like content
    for page_idx in range(60):
        page_num = page_idx + 1  # 1-indexed
        page = doc.new_page(width=595, height=842)  # A4

        # Page margins
        left, top, right, bottom = 72, 72, 523, 770

        # Header: page number
        page.insert_text(
            pymupdf.Point(right - 20, 40),
            str(page_num),
            fontsize=10,
            fontname="tiro",
            color=(0.4, 0.4, 0.4),
        )

        if page_num in PAGE_CONTENT:
            heading, body = PAGE_CONTENT[page_num]
            y = top

            if heading:
                # Section heading
                if heading.startswith("Chapter"):
                    page.insert_text(pymupdf.Point(left, y), heading,
                                     fontsize=18, fontname="hebo", color=(0, 0, 0))
                    y += 36
                    # Underline after chapter title
                    shape = page.new_shape()
                    shape.draw_line(pymupdf.Point(left, y - 10), pymupdf.Point(right, y - 10))
                    shape.finish(color=(0, 0, 0), width=0.5)
                    shape.commit()
                else:
                    page.insert_text(pymupdf.Point(left, y), heading,
                                     fontsize=14, fontname="hebo", color=(0, 0, 0))
                    y += 28

            if body:
                rect = pymupdf.Rect(left, y, right, bottom)
                page.insert_textbox(
                    rect, body,
                    fontsize=11, fontname="tiro", color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )
        else:
            # Generic thesis content for pages without specific content
            y = top
            # Determine which chapter this page falls in
            if page_num <= 5:
                ch = "Introduction"
            elif page_num <= 14:
                ch = "Literature Review"
            elif page_num <= 24:
                ch = "Methodology"
            elif page_num <= 34:
                ch = "Experimental Setup"
            elif page_num <= 49:
                ch = "Results and Discussion"
            else:
                ch = "Conclusion and Future Work"

            # Running header
            page.insert_text(
                pymupdf.Point(left, 40),
                ch,
                fontsize=9, fontname="tiit", color=(0.4, 0.4, 0.4),
            )

            filler = (
                f"This section continues the analysis presented in the preceding pages. "
                f"The experimental results demonstrate consistent improvements across all "
                f"evaluation metrics when comparing our proposed reinforcement learning "
                f"framework with traditional molecular dynamics simulations.\n\n"
                f"Table {page_num - 14}.{(page_num % 5) + 1} summarizes the key performance "
                f"indicators for the benchmark proteins in this category. The GDT-TS scores "
                f"range from {55 + (page_num % 30):.1f} to {78 + (page_num % 15):.1f}, "
                f"indicating significant variability across different protein families.\n\n"
                f"The root-mean-square deviation (RMSD) values shown in the rightmost column "
                f"confirm that our method achieves competitive accuracy, particularly for "
                f"proteins with well-defined secondary structure elements. For proteins with "
                f"significant disorder (> 30% of residues), the performance degrades, as "
                f"expected from the discussion in Section 3.2.\n\n"
                f"Further analysis of the contact map predictions reveals that long-range "
                f"contacts (sequence separation > 24 residues) remain the most challenging "
                f"to predict accurately. The precision of long-range contact prediction "
                f"correlates strongly with the overall structural accuracy (Pearson r = 0.87, "
                f"p < 0.001)."
            )

            rect = pymupdf.Rect(left, y, right, bottom)
            page.insert_textbox(rect, filler,
                                fontsize=11, fontname="tiro", color=(0, 0, 0),
                                align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Set TOC with existing bookmarks for Chapters 1 and 2 only
    toc = [
        [1, "Chapter 1: Introduction", 1],
        [2, "1.1 Background and Motivation", 1],
        [2, "1.2 Research Questions", 3],
        [2, "1.3 Scope and Limitations", 4],
        [2, "1.4 Thesis Outline", 5],
        [1, "Chapter 2: Literature Review", 6],
        [2, "2.1 Theoretical Framework", 6],
        [2, "2.2 Previous Studies", 8],
        [2, "2.3 Gaps in the Literature", 11],
        [2, "2.4 Summary", 14],
    ]
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "Deep Reinforcement Learning for Protein Structure Prediction",
        "author": "Elena Rodriguez",
        "subject": "Computational Biology, Machine Learning",
        "keywords": "protein folding, reinforcement learning, deep learning, structure prediction",
        "creator": "LaTeX with hyperref",
        "producer": "pdfTeX-1.40.25",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
