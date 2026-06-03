"""
Initial Setup: Create ~/Documents/research_paper.pdf
Task ID: pdf_cross_148
Domain: pdf + libreoffice_writer (cross-domain)

Creates a realistic 20-page academic research paper with 35 APA references on pages 18-20.
Opens the PDF in Evince for the agent to read and extract references from.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_148'
OUTPUT = f'{WORKDIR}/research_paper.pdf'


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


def create_research_paper():
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                        PageBreak, HRFlowable)
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.colors import black, HexColor
        from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
        _create_with_reportlab()
    except ImportError:
        _create_with_fpdf()


def _create_with_reportlab():
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    PageBreak, HRFlowable)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import black, HexColor
    from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER

    os.makedirs(WORKDIR, exist_ok=True)

    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=1.0 * inch,
        rightMargin=1.0 * inch,
        topMargin=1.0 * inch,
        bottomMargin=1.0 * inch,
        title="Advances in Neural Architecture Search: A Comprehensive Survey",
        author="Chen, L., Patel, R., Okonkwo, A., Yamamoto, S., & Reyes, M.",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'PaperTitle',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        spaceAfter=18,
        alignment=TA_CENTER,
        textColor=HexColor('#1a1a2e'),
    )
    author_style = ParagraphStyle(
        'Authors',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=6,
        alignment=TA_CENTER,
    )
    abstract_heading = ParagraphStyle(
        'AbstractHeading',
        parent=styles['Heading1'],
        fontSize=12,
        leading=16,
        spaceBefore=20,
        spaceAfter=6,
        alignment=TA_CENTER,
        textColor=HexColor('#1a1a2e'),
    )
    abstract_style = ParagraphStyle(
        'Abstract',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        leftIndent=0.5 * inch,
        rightIndent=0.5 * inch,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
    )
    heading1 = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontSize=13,
        leading=18,
        spaceBefore=18,
        spaceAfter=8,
        textColor=HexColor('#1a1a2e'),
    )
    heading2 = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=11,
        leading=16,
        spaceBefore=12,
        spaceAfter=6,
        textColor=HexColor('#2d4059'),
    )
    body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        leading=15,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
    )
    ref_heading = ParagraphStyle(
        'RefHeading',
        parent=styles['Heading1'],
        fontSize=13,
        leading=18,
        spaceBefore=20,
        spaceAfter=10,
        textColor=HexColor('#1a1a2e'),
    )
    ref_style = ParagraphStyle(
        'Reference',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=14,
        leftIndent=0.5 * inch,
        firstLineIndent=-0.5 * inch,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
    )

    story = []

    # ---- PAGE 1: Title, Authors, Abstract ----
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        "Advances in Neural Architecture Search: A Comprehensive Survey",
        title_style
    ))
    story.append(Paragraph(
        "Lingyu Chen<super>1</super>, Rohan Patel<super>2</super>, "
        "Adaeze Okonkwo<super>3</super>, Sho Yamamoto<super>4</super>, "
        "& Miguel Reyes<super>5</super>",
        author_style
    ))
    story.append(Paragraph(
        "<super>1</super>Department of Computer Science, Stanford University &nbsp;&nbsp; "
        "<super>2</super>School of Engineering, MIT &nbsp;&nbsp; "
        "<super>3</super>AI Research Lab, Cambridge University",
        ParagraphStyle('Affil', parent=styles['Normal'], fontSize=9,
                       alignment=TA_CENTER, spaceAfter=4)
    ))
    story.append(Paragraph(
        "<super>4</super>Graduate School of Informatics, Kyoto University &nbsp;&nbsp; "
        "<super>5</super>Department of Statistics, UC Berkeley",
        ParagraphStyle('Affil2', parent=styles['Normal'], fontSize=9,
                       alignment=TA_CENTER, spaceAfter=12)
    ))
    story.append(Paragraph(
        "Correspondence: l.chen@cs.stanford.edu",
        ParagraphStyle('Corr', parent=styles['Normal'], fontSize=9,
                       alignment=TA_CENTER, spaceAfter=6)
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#cccccc'),
                            spaceAfter=10))
    story.append(Paragraph("Abstract", abstract_heading))
    story.append(Paragraph(
        "Neural Architecture Search (NAS) has emerged as a transformative paradigm in deep "
        "learning, automating the design of neural network architectures that previously required "
        "extensive expert knowledge. This comprehensive survey examines the state-of-the-art "
        "NAS methodologies, covering search strategies including reinforcement learning, "
        "evolutionary algorithms, gradient-based methods, and one-shot approaches. We analyze "
        "performance estimation strategies, hardware-aware NAS, multi-objective optimization, "
        "and emerging trends such as zero-cost proxies and transferable NAS. Our review "
        "synthesizes findings from over 200 publications spanning 2017-2024, identifying key "
        "challenges, benchmark evaluations, and promising future research directions. We also "
        "discuss practical considerations for deploying NAS in real-world applications including "
        "edge computing, medical imaging, and natural language processing.",
        abstract_style
    ))
    story.append(Paragraph(
        "<b>Keywords:</b> neural architecture search, automated machine learning, deep learning, "
        "hyperparameter optimization, reinforcement learning, evolutionary computation",
        ParagraphStyle('KW', parent=styles['Normal'], fontSize=9.5,
                       leftIndent=0.5 * inch, rightIndent=0.5 * inch,
                       spaceAfter=10)
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#cccccc'),
                            spaceAfter=6))
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph(
        "Received: November 3, 2024 &nbsp;&nbsp;&nbsp; Accepted: February 12, 2025 &nbsp;&nbsp;&nbsp; "
        "Published: March 1, 2025 &nbsp;&nbsp;&nbsp; DOI: 10.1016/j.neunet.2025.03.018",
        ParagraphStyle('Dates', parent=styles['Normal'], fontSize=8.5,
                       alignment=TA_CENTER, spaceAfter=8)
    ))

    # ---- PAGE 2: Introduction ----
    story.append(PageBreak())
    story.append(Paragraph("1. Introduction", heading1))
    story.append(Paragraph(
        "The design of neural network architectures has traditionally been a labor-intensive "
        "process requiring substantial domain expertise and computational resources. "
        "Architecture search algorithms, broadly termed Neural Architecture Search (NAS), "
        "represent a paradigm shift in deep learning research by automating this design process. "
        "Since the seminal work of Zoph and Le (2017), NAS has progressed from computationally "
        "prohibitive methods requiring thousands of GPU-hours to efficient single-shot approaches "
        "that complete in minutes on commodity hardware.",
        body
    ))
    story.append(Paragraph(
        "The field has witnessed explosive growth, with over 1,200 papers published between "
        "2018 and 2024 according to recent bibliometric analyses. NAS methods have achieved "
        "state-of-the-art performance across diverse tasks including image classification "
        "(Tan & Le, 2019), object detection (Chen et al., 2019), semantic segmentation "
        "(Liu et al., 2019), and natural language processing (So et al., 2019). However, "
        "the reproducibility, computational cost, and fair comparison of NAS methods remain "
        "significant challenges that the research community continues to grapple with.",
        body
    ))
    story.append(Paragraph(
        "This survey makes several key contributions: (1) a comprehensive taxonomy of NAS "
        "methods organized by search space, search strategy, and performance estimation; "
        "(2) a critical analysis of evaluation methodologies and reproducibility issues; "
        "(3) coverage of hardware-aware NAS targeting mobile and edge devices; "
        "(4) discussion of multi-task and transfer NAS; and (5) identification of open "
        "research problems and future directions.",
        body
    ))
    story.append(Paragraph("1.1 Scope and Organization", heading2))
    story.append(Paragraph(
        "This survey covers publications from January 2017 through December 2024, indexed in "
        "IEEE Xplore, ACM Digital Library, arXiv, and major machine learning conference "
        "proceedings (NeurIPS, ICML, ICLR, CVPR, ECCV, ICCV, AAAI, IJCAI). We focus on "
        "supervised learning settings while briefly discussing semi-supervised, self-supervised, "
        "and reinforcement learning applications of NAS. The remainder of this paper is "
        "organized as follows: Section 2 defines the NAS problem formulation; Section 3 "
        "covers search spaces; Section 4 reviews search strategies; Sections 5 and 6 address "
        "performance estimation and hardware-aware NAS; Section 7 discusses applications; "
        "Section 8 presents benchmarks; Section 9 identifies future directions.",
        body
    ))

    # ---- PAGE 3: Problem Formulation ----
    story.append(PageBreak())
    story.append(Paragraph("2. Problem Formulation", heading1))
    story.append(Paragraph(
        "Formally, NAS can be framed as a bi-level optimization problem. Given a dataset D "
        "partitioned into training D_train and validation D_val sets, NAS seeks an architecture "
        "a* from a search space A that minimizes a validation objective L_val while its "
        "associated weights w*(a) minimize the training objective L_train. The bi-level nature "
        "arises because optimal weights depend on the architecture, while architecture selection "
        "depends on the performance of trained weights.",
        body
    ))
    story.append(Paragraph(
        "Three components define any NAS system: (1) the search space A encoding prior "
        "knowledge about useful architectural patterns; (2) the search strategy S determining "
        "how candidate architectures are sampled or generated; and (3) the performance "
        "estimation strategy E approximating validation performance without full training. "
        "The interaction between these components determines the effectiveness, efficiency, "
        "and generalizability of the NAS method.",
        body
    ))
    story.append(Paragraph("2.1 Search Space Design", heading2))
    story.append(Paragraph(
        "Search space design critically affects NAS performance. Chain-structured search "
        "spaces define architectures as sequential operations with configurable layer types, "
        "filter sizes, and connections. Cell-based search spaces, popularized by NASNet "
        "(Zoph et al., 2018), define a small cell structure that is stacked to form the full "
        "network, enabling efficient exploration and transferability across datasets. "
        "Hierarchical search spaces combine multiple levels of abstraction. Morphism-based "
        "spaces apply continuous transformations to existing architectures. Most recently, "
        "transformer search spaces explore attention mechanisms and positional encodings for "
        "vision transformers.",
        body
    ))

    # ---- PAGES 4-8: Search Strategies ----
    story.append(PageBreak())
    story.append(Paragraph("3. Search Strategies", heading1))
    story.append(Paragraph(
        "Search strategies define how the architecture optimization problem is solved. "
        "We organize strategies into four major families: reinforcement learning (RL), "
        "evolutionary algorithms (EA), gradient-based methods (GRAD), and Bayesian "
        "optimization (BO). Each approach offers distinct trade-offs between computational "
        "cost, sample efficiency, and optimization landscape coverage.",
        body
    ))
    story.append(Paragraph("3.1 Reinforcement Learning-Based NAS", heading2))
    story.append(Paragraph(
        "RL-based NAS formulates architecture design as a sequential decision process where "
        "a controller (typically an RNN) generates architecture descriptions token by token. "
        "The controller is trained using REINFORCE or proximal policy optimization (PPO) with "
        "validation accuracy as the reward signal. Zoph and Le (2017) demonstrated that RL-NAS "
        "could discover architectures competitive with hand-crafted designs on CIFAR-10 and "
        "Penn Treebank, albeit requiring 800 GPUs for 28 days.",
        body
    ))
    story.append(Paragraph(
        "Subsequent work reduced computational costs through parameter sharing (Pham et al., "
        "2018) and block-wise search (Zhong et al., 2018). MetaQNN (Baker et al., 2017) "
        "applied Q-learning to architecture search, while ENAS (Pham et al., 2018) shared "
        "weights across child models to reduce training cost by 1000x. MnasNet (Tan et al., "
        "2019) incorporated latency constraints directly into the RL reward, enabling "
        "hardware-aware architecture search for mobile deployment.",
        body
    ))
    story.append(Paragraph("3.2 Evolutionary Algorithm-Based NAS", heading2))
    story.append(Paragraph(
        "Evolutionary approaches maintain a population of candidate architectures that undergo "
        "mutation and selection over multiple generations. Real (et al., 2017) applied "
        "tournament selection and mutation operations including adding/removing connections and "
        "changing activation functions. AmoebaNet (Real et al., 2019) extended this to "
        "discover NASNet-level architectures. NSGA-Net (Lu et al., 2019) used non-dominated "
        "sorting for multi-objective optimization balancing accuracy and FLOPs.",
        body
    ))

    story.append(PageBreak())
    story.append(Paragraph("3.3 Gradient-Based NAS", heading2))
    story.append(Paragraph(
        "DARTS (Liu et al., 2019) revolutionized NAS efficiency by relaxing the discrete "
        "architecture search space to a continuous domain using softmax parameterization over "
        "candidate operations. Architecture parameters and network weights are optimized "
        "jointly using stochastic gradient descent on training and validation losses "
        "respectively. DARTS reduced search time from thousands of GPU-hours to ~1.5 GPU-days "
        "on CIFAR-10 while maintaining competitive performance.",
        body
    ))
    story.append(Paragraph(
        "DARTS variants address known limitations including performance collapse (R-DARTS, "
        "Zela et al., 2020), discretization gap (SDARTS, Chen & Hsieh, 2020), and skip "
        "connection dominance (P-DARTS, Chen et al., 2019). PC-DARTS (Xu et al., 2020) "
        "reduces memory cost through partial channel connections. iDARTS (Zhang et al., 2021) "
        "improves inner loop stability, while GDAS (Dong & Yang, 2019) uses Gumbel-softmax "
        "for stochastic operation sampling.",
        body
    ))

    for i in range(3):
        story.append(PageBreak())
        sections = [
            ("4. Performance Estimation Strategies",
             "4.1 Lower Fidelity Estimates",
             "Performance estimation is a critical bottleneck in NAS. Training each candidate "
             "architecture to convergence is prohibitively expensive, motivating a range of "
             "approximation strategies. Lower-fidelity estimates use reduced dataset sizes, "
             "fewer training epochs, smaller proxy architectures, or downsampled inputs. "
             "While computationally efficient, they introduce estimation bias that can "
             "misrank candidate architectures, particularly when the performance correlation "
             "between proxy and target tasks is weak.",
             "4.2 Weight Sharing and One-Shot Methods",
             "One-shot methods encode all candidate architectures into a single supernet "
             "where subgraphs share weights. By training the supernet once, individual "
             "architectures are evaluated by inheriting weights from the supernet without "
             "retraining. SMASH (Brock et al., 2018) used a hypernetwork to generate "
             "architecture weights. SNAS (Xie et al., 2019) applied stochastic operations "
             "for efficient gradient estimation."),
            ("5. Hardware-Aware Neural Architecture Search",
             "5.1 Latency Modeling",
             "Hardware-aware NAS explicitly incorporates device constraints into the "
             "optimization objective. Early approaches built lookup tables mapping operations "
             "to measured latency on target hardware. ProxylessNAS (Cai et al., 2019) "
             "combined gradient-based NAS with hardware latency models for mobile CPU and GPU "
             "targets. FBNet (Wu et al., 2019) used differentiable sampling with expected "
             "latency as a differentiable cost.",
             "5.2 Neural Processing Unit Optimization",
             "Application-specific integrated circuits including neural processing units "
             "(NPUs) present unique NAS challenges. NPU execution patterns differ substantially "
             "from GPU or CPU execution, with performance heavily dependent on operator fusion "
             "patterns and memory access sequences. Once-for-All (Cai et al., 2020) trained "
             "a supernet from which any valid subnetwork could be extracted for immediate "
             "deployment on target devices without retraining."),
            ("6. Multi-Objective and Transfer NAS",
             "6.1 Multi-Task Architecture Search",
             "Multi-task NAS optimizes architectures shared across multiple related tasks. "
             "This setting introduces additional complexity as performance must be evaluated "
             "across tasks simultaneously. MTNAS (Liang et al., 2019) extended DARTS to "
             "multi-task learning with task-specific decoder heads. Graph Neural Architecture "
             "Search (GNAS) explored architectures for graph-structured data across node "
             "classification, link prediction, and graph classification tasks.",
             "6.2 Transfer and Meta-NAS",
             "Transfer NAS leverages knowledge from previously searched tasks or datasets "
             "to accelerate architecture search on new tasks. Meta-learning approaches train "
             "NAS controllers across many tasks so they can quickly adapt to new ones. "
             "TaskNAS (Gu et al., 2021) learned task embeddings to predict transferable "
             "architectural priors. Progressive NAS with transfer (Liu et al., 2020) "
             "demonstrated that architectures found on CIFAR-10 transfer effectively to "
             "ImageNet with appropriate cell stacking strategies."),
        ]
        if i < len(sections):
            s = sections[i]
            story.append(Paragraph(s[0], heading1))
            story.append(Paragraph(s[1], heading2))
            story.append(Paragraph(s[2], body))
            story.append(Paragraph(s[3], heading2))
            story.append(Paragraph(s[4], body))

    # ---- PAGES 10-11: Applications ----
    story.append(PageBreak())
    story.append(Paragraph("7. Applications", heading1))
    story.append(Paragraph("7.1 Image Classification and Object Detection", heading2))
    story.append(Paragraph(
        "Image classification on ImageNet (Russakovsky et al., 2015) represents the primary "
        "benchmark for evaluating NAS methods. NASNet-A (Zoph et al., 2018) achieved 82.7% "
        "top-1 accuracy with 88.9M parameters. EfficientNet (Tan & Le, 2019) introduced "
        "compound scaling and achieved 84.3% with compound coefficient phi=7. In object "
        "detection, DetNAS (Chen et al., 2019) searched backbone architectures yielding "
        "2.4% mAP improvement over ResNet-50 on COCO.",
        body
    ))
    story.append(Paragraph("7.2 Medical Image Analysis", heading2))
    story.append(Paragraph(
        "Medical imaging presents unique NAS challenges including limited labeled data, "
        "3D volumetric inputs, and clinical interpretability requirements. DiabNAS "
        "(Zhou et al., 2020) searched architectures for diabetic retinopathy screening, "
        "achieving AUC of 0.972 exceeding specialist performance. NAS has been applied to "
        "brain tumor segmentation (Baid et al., 2021), chest X-ray classification "
        "(Wang et al., 2020), and histopathology image analysis.",
        body
    ))

    story.append(PageBreak())
    story.append(Paragraph("7.3 Natural Language Processing", heading2))
    story.append(Paragraph(
        "Transformer architecture search represents a growing NAS frontier. Evolved Transformer "
        "(So et al., 2019) searched the attention mechanism and feed-forward layer configurations "
        "using evolutionary algorithms, yielding improved machine translation BLEU scores. "
        "AutoBERT-Zero (Ji et al., 2021) discovered novel attention patterns outperforming "
        "hand-designed BERT variants on GLUE benchmarks. TextNAS (Yao et al., 2020) searched "
        "architectures for text classification tasks.",
        body
    ))

    # ---- PAGES 12-13: Benchmarks ----
    story.append(PageBreak())
    story.append(Paragraph("8. NAS Benchmarks", heading1))
    story.append(Paragraph("8.1 Tabular Benchmarks", heading2))
    story.append(Paragraph(
        "NAS-Bench-101 (Ying et al., 2019) provided the first public NAS benchmark with "
        "pre-computed performance for 423,624 unique architectures on CIFAR-10. This enabled "
        "reproducible NAS evaluation at negligible computational cost. NAS-Bench-201 "
        "(Dong & Yang, 2020) extended this to three datasets (CIFAR-10, CIFAR-100, ImageNet16) "
        "enabling cross-dataset comparison. NAS-Bench-301 (Siems et al., 2020) used a "
        "surrogate model to interpolate performance for the full DARTS search space.",
        body
    ))
    story.append(Paragraph("8.2 Reproducibility and Fair Comparison", heading2))
    story.append(Paragraph(
        "Reproducibility challenges in NAS arise from inconsistent training protocols, "
        "hardware differences, and stochastic optimization. Li and Talwalkar (2020) showed "
        "that many NAS methods do not significantly outperform random architecture selection "
        "with the same training budget when controlling for confounds. The NAS community has "
        "responded with standardized evaluation protocols and ablation study requirements for "
        "top-tier conferences.",
        body
    ))

    # ---- PAGES 14-15: Future Directions ----
    story.append(PageBreak())
    story.append(Paragraph("9. Challenges and Future Directions", heading1))
    story.append(Paragraph("9.1 Scalability to Large Models", heading2))
    story.append(Paragraph(
        "Current NAS methods face scalability challenges when applied to billion-parameter "
        "foundation models. GPT-NAS and related approaches adapt existing NAS techniques to "
        "transformer-scale models by leveraging weight sharing and progressive training. "
        "The computational cost of NAS grows with model size, motivating zero-cost proxy "
        "methods that estimate architecture quality without any training.",
        body
    ))
    story.append(Paragraph("9.2 Generalization Across Domains", heading2))
    story.append(Paragraph(
        "Most NAS methods are developed and evaluated on standard computer vision benchmarks, "
        "raising questions about generalization to other domains. Domain-specific constraints "
        "such as 3D inputs in medical imaging, variable-length sequences in NLP, and "
        "graph-structured data in molecular property prediction require specialized search "
        "spaces. Cross-domain NAS is an emerging research direction with significant "
        "practical potential.",
        body
    ))

    story.append(PageBreak())
    story.append(Paragraph("9.3 Ethical and Environmental Considerations", heading2))
    story.append(Paragraph(
        "The environmental impact of NAS is substantial. Strubell et al. (2019) estimated "
        "that training a single NAS model can emit as much CO2 as five cars over their "
        "lifetime. Green NAS initiatives focus on reducing computational budgets through "
        "efficient search strategies, zero-shot proxies, and carbon-aware scheduling. "
        "Equitable access to NAS is another concern, as computationally expensive methods "
        "favor well-resourced research groups.",
        body
    ))
    story.append(Paragraph("9.4 AutoML Integration", heading2))
    story.append(Paragraph(
        "NAS is increasingly integrated into broader AutoML pipelines that jointly optimize "
        "preprocessing, feature engineering, architecture, and hyperparameter choices. "
        "Auto-Sklearn 2.0 (Feurer et al., 2022) and AutoGluon (Erickson et al., 2020) "
        "incorporate NAS components for tabular, image, and text modalities. The convergence "
        "of NAS with neural ordinary differential equations, implicit networks, and "
        "physics-informed neural networks suggests rich future research opportunities.",
        body
    ))

    # ---- PAGES 16-17: Conclusion and Discussion ----
    story.append(PageBreak())
    story.append(Paragraph("10. Discussion", heading1))
    story.append(Paragraph(
        "Across the reviewed literature, several key themes emerge. First, the field has "
        "shifted decisively from computationally expensive RL and EA methods toward efficient "
        "one-shot and gradient-based approaches without sacrificing final accuracy. Second, "
        "hardware awareness has become a first-class consideration, with latency-constrained "
        "NAS enabling practical deployment on resource-constrained devices. Third, the "
        "introduction of public benchmarks has raised the bar for rigorous evaluation while "
        "revealing that many early NAS claims were overstated relative to carefully tuned "
        "random baselines.",
        body
    ))
    story.append(Paragraph(
        "Notable gaps in the literature include limited exploration of NAS for continual "
        "learning, federated settings, and privacy-preserving applications. The intersection "
        "of NAS with neural network robustness (adversarial examples, distribution shift) "
        "remains underexplored. Multi-modal NAS jointly searching image, text, and audio "
        "architectures is an emerging frontier with potential for multimodal foundation "
        "model development.",
        body
    ))

    story.append(PageBreak())
    story.append(Paragraph("11. Conclusion", heading1))
    story.append(Paragraph(
        "This survey has presented a comprehensive review of Neural Architecture Search "
        "methods spanning seven years of intensive research. We traced the evolution from "
        "computationally prohibitive RL and EA approaches to efficient gradient-based and "
        "one-shot methods that democratize NAS. Hardware-aware NAS has emerged as a "
        "practical necessity for real-world deployment, while multi-objective formulations "
        "enable richer optimization landscapes.",
        body
    ))
    story.append(Paragraph(
        "The field faces important challenges including reproducibility, scalability, and "
        "environmental sustainability. Public benchmarks and standardized evaluation protocols "
        "are positive developments that improve scientific rigor. Looking forward, the "
        "integration of NAS into AutoML systems, the application to foundation models, "
        "and the development of green NAS methods represent the most promising directions. "
        "We anticipate continued rapid progress as the community addresses these challenges "
        "and expands the scope of automated architecture design.",
        body
    ))

    # ---- PAGE 16: Appendix A — Comparison Table ----
    story.append(PageBreak())
    story.append(Paragraph("Appendix A: Comparison of NAS Methods", heading1))
    story.append(Paragraph(
        "Table A1 summarizes key properties of representative NAS methods discussed in this survey, "
        "including search strategy, search space type, performance estimation approach, computational "
        "cost (GPU-days), and the primary benchmark on which results were reported.",
        body
    ))
    story.append(Paragraph(
        "The table highlights the dramatic reduction in computational cost from RL-based methods "
        "(e.g., NASNet at ~2,000 GPU-days) to gradient-based methods (e.g., DARTS at ~1.5 GPU-days) "
        "and one-shot approaches (e.g., ENAS at ~0.5 GPU-days). Hardware-aware methods "
        "(e.g., MnasNet, FBNet) achieve competitive accuracy-latency trade-offs by incorporating "
        "device constraints directly into optimization.",
        body
    ))
    story.append(Paragraph(
        "Reproducibility scores are based on whether the original paper provided (a) public code, "
        "(b) pretrained models, (c) full hyperparameter settings, and (d) multiple random seed "
        "results. Methods scoring 4/4 are marked as Excellent; 3/4 as Good; below 3 as Poor. "
        "The mean reproducibility score across reviewed methods was 2.3/4.0, highlighting the "
        "persistent reproducibility challenge in NAS research.",
        body
    ))
    story.append(Paragraph("Appendix B: Glossary of Terms", heading1))
    story.append(Paragraph(
        "<b>Architecture Search Space (A):</b> The set of all candidate neural network architectures "
        "that can be generated or evaluated by a NAS method. <b>Cell:</b> A directed acyclic graph "
        "representing a building block of operations, typically stacked to form the full network. "
        "<b>One-shot NAS:</b> Methods that train a single supernet once and evaluate sub-architectures "
        "by weight inheritance. <b>DARTS:</b> Differentiable Architecture Search; relaxes discrete "
        "search to continuous domain via softmax parameterization.",
        body
    ))
    story.append(Paragraph(
        "<b>Performance Estimation:</b> Techniques for approximating architecture quality without "
        "full training. <b>Hardware-Aware NAS:</b> Methods that incorporate device-specific "
        "constraints (latency, memory, energy) into the optimization objective. <b>Zero-Cost Proxy:</b> "
        "Architecture quality estimators that require no training (e.g., gradient norms, activation "
        "statistics at initialization). <b>Multi-Objective NAS:</b> Optimization formulations "
        "balancing multiple objectives such as accuracy, latency, and model size.",
        body
    ))

    # ---- PAGE 17: Appendix C — Reproducibility Details ----
    story.append(PageBreak())
    story.append(Paragraph("Appendix C: Reproducibility Details", heading1))
    story.append(Paragraph(
        "All experiments reported in Section 8 were conducted using PyTorch 2.1.0 on NVIDIA A100-80GB "
        "GPUs. Training used the AdamW optimizer with cosine annealing learning rate schedule "
        "(initial lr=3e-4, weight decay=1e-2). Data augmentation followed the standard protocol: "
        "random horizontal flip, random crop with padding=4, and CutOut (length=16) for CIFAR-10 "
        "and CIFAR-100. ImageNet experiments used RandAugment (N=2, M=9) following the EfficientNet "
        "training protocol.",
        body
    ))
    story.append(Paragraph(
        "Statistical significance was assessed using the Wilcoxon signed-rank test across 5 "
        "independent runs with different random seeds. Reported values are mean ± standard deviation. "
        "For NAS methods requiring GPU hours, we report GPU-hours on a single A100-80GB GPU; "
        "original papers may have used different hardware (V100, P100, or TPU), requiring "
        "appropriate normalization. Our compute budget for all experiments totaled approximately "
        "1,847 A100-GPU-hours, equivalent to approximately 0.43 tonnes CO2e.",
        body
    ))
    story.append(Paragraph("Appendix D: Extended Related Work", heading1))
    story.append(Paragraph(
        "Hyperparameter Optimization (HPO) methods such as Hyperband (Li et al., 2018), "
        "BOHB (Falkner et al., 2018), and Population-Based Training (Jaderberg et al., 2017) "
        "are closely related to NAS but typically optimize fixed-architecture hyperparameters "
        "rather than structural design choices. The boundary between HPO and NAS is blurring "
        "as joint architecture-hyperparameter search methods emerge. AutoML systems like "
        "Auto-Sklearn and AutoGluon integrate NAS with automated feature engineering, "
        "preprocessing, and ensemble construction.",
        body
    ))
    story.append(Paragraph(
        "Continual learning with NAS (Progressive Neural Networks, PackNet) enables models to "
        "grow their architecture in response to new tasks without forgetting prior knowledge. "
        "Neural Architecture Generation using large language models represents a very recent "
        "direction where GPT-4 and similar models generate architecture specifications from "
        "natural language descriptions, effectively using the LLM as a NAS controller. "
        "This approach achieved competitive results on standard benchmarks while requiring "
        "significantly fewer FLOPs than traditional NAS methods.",
        body
    ))

    # ---- PAGES 18-20: References (35 APA entries) ----
    story.append(PageBreak())
    story.append(Paragraph("References", ref_heading))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#999999'),
                            spaceAfter=8))

    references = [
        "Baker, B., Gupta, O., Naik, N., & Raskar, R. (2017). Designing neural network architectures using reinforcement learning. <i>International Conference on Learning Representations (ICLR)</i>. https://arxiv.org/abs/1611.02167",

        "Baid, U., Ghodasara, S., Mohan, S., Bilello, M., Calabrese, E., Colak, E., Farahani, K., Kalpathy-Cramer, J., Kitamura, F. C., Pati, S., & Bakas, S. (2021). The RSNA-ASNR-MICCAI BraTS 2021 benchmark on brain tumor segmentation and radiogenomic classification. <i>arXiv preprint arXiv:2107.02314</i>.",

        "Brock, A., Lim, T., Ritchie, J. M., & Weston, N. (2018). SMASH: One-shot model architecture search through hypernetworks. <i>International Conference on Learning Representations (ICLR)</i>. https://openreview.net/forum?id=rydeCEhs-",

        "Cai, H., Gan, C., Wang, T., Zhang, Z., & Han, S. (2020). Once-for-all: Train one network and specialize it for efficient deployment. <i>International Conference on Learning Representations (ICLR)</i>. https://openreview.net/forum?id=HylxE1HKwS",

        "Cai, H., Zhu, L., & Han, S. (2019). ProxylessNAS: Direct neural architecture search on target task and hardware. <i>International Conference on Learning Representations (ICLR)</i>. https://arxiv.org/abs/1812.00332",

        "Chen, P., & Hsieh, C. J. (2020). SDARTS: Searching for accurate and stable architectures. <i>arXiv preprint arXiv:2006.10355</i>.",

        "Chen, T., Goodfellow, I., & Shlens, J. (2019). Net2Net: Accelerating learning via knowledge transfer. <i>International Conference on Learning Representations (ICLR)</i>. https://arxiv.org/abs/1511.05641",

        "Chen, X., Xie, L., Wu, J., & Tian, Q. (2019). Progressive DARTS: Bridging the optimization gap for NAS in the wild. <i>arXiv preprint arXiv:1912.10952</i>.",

        "Dong, X., & Yang, Y. (2019). Searching for a robust neural architecture in four GPU hours. <i>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 1761–1770.",

        "Dong, X., & Yang, Y. (2020). NAS-Bench-201: Extending the scope of reproducible neural architecture search. <i>International Conference on Learning Representations (ICLR)</i>. https://openreview.net/forum?id=HJxyZkBKDr",

        "Erickson, N., Mueller, J., Shirkov, A., Zhang, H., Larroy, P., Li, M., & Smola, A. (2020). AutoGluon-tabular: Robust and accurate AutoML for structured data. <i>arXiv preprint arXiv:2003.06505</i>.",

        "Feurer, M., Eggensperger, K., Falkner, S., Lindauer, M., & Hutter, F. (2022). Auto-Sklearn 2.0: Hands-free AutoML via meta-learning. <i>Journal of Machine Learning Research</i>, <i>23</i>(261), 1–61.",

        "Gu, J., Dong, X., & Yang, Y. (2021). TaskNAS: Task-aware few-shot learning via meta neural architecture search. <i>International Conference on Computer Vision (ICCV)</i>. https://doi.org/10.1109/ICCV48922.2021.01237",

        "Ji, S., Zhang, Z., Ji, R., & Gao, Y. (2021). AutoBERT-Zero: Evolving BERT backbone from scratch. <i>arXiv preprint arXiv:2107.07445</i>.",

        "Li, L., & Talwalkar, A. (2020). Random search and reproducibility for neural architecture search. <i>Proceedings of the Conference on Uncertainty in Artificial Intelligence (UAI)</i>, 367–377.",

        "Liang, Y., Jiang, L., & Zheng, Y. (2019). MTNAS: Multi-task neural architecture search for computer vision. <i>arXiv preprint arXiv:1911.04440</i>.",

        "Liu, C., Zoph, B., Neumann, M., Shlens, J., Hua, W., Li, L. J., Fei-Fei, L., Yuille, A., Huang, J., & Murphy, K. (2018). Progressive neural architecture search. <i>Proceedings of the European Conference on Computer Vision (ECCV)</i>, 19–34.",

        "Liu, H., Simonyan, K., & Yang, Y. (2019). DARTS: Differentiable architecture search. <i>International Conference on Learning Representations (ICLR)</i>. https://openreview.net/forum?id=S1eYcEt_7",

        "Lu, Z., Whalen, I., Boddeti, V., Dhebar, Y., Deb, K., Goodman, E., & Banzhaf, W. (2019). NSGA-Net: Neural architecture search using multi-objective genetic algorithm. <i>Proceedings of the Genetic and Evolutionary Computation Conference (GECCO)</i>, 419–427.",

        "Pham, H., Guan, M., Zoph, B., Le, Q. V., & Dean, J. (2018). Efficient neural architecture search via parameter sharing. <i>Proceedings of the International Conference on Machine Learning (ICML)</i>, 4095–4104.",

        "Real, E., Aggarwal, A., Huang, Y., & Le, Q. V. (2019). Regularized evolution for image classifier architecture search. <i>Proceedings of the AAAI Conference on Artificial Intelligence</i>, <i>33</i>(01), 4780–4789.",

        "Real, E., Moore, S., Selle, A., Saxena, S., Suematsu, Y. L., Tan, J., Le, Q. V., & Kurakin, A. (2017). Large-scale evolution of image classifiers. <i>Proceedings of the International Conference on Machine Learning (ICML)</i>, 2902–2911.",

        "Russakovsky, O., Deng, J., Su, H., Krause, J., Satheesh, S., Ma, S., Huang, Z., Karpathy, A., Khosla, A., Bernstein, M., Berg, A. C., & Fei-Fei, L. (2015). ImageNet large scale visual recognition challenge. <i>International Journal of Computer Vision</i>, <i>115</i>(3), 211–252.",

        "Siems, J., Zimmer, L., Zela, A., Lukasik, J., Keuper, M., & Hutter, F. (2020). NAS-Bench-301 and the case for surrogate benchmarks for neural architecture search. <i>arXiv preprint arXiv:2008.09777</i>.",

        "So, D. R., Liang, C., & Le, Q. V. (2019). The Evolved Transformer. <i>Proceedings of the International Conference on Machine Learning (ICML)</i>, 5877–5886.",

        "Strubell, E., Ganesh, A., & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. <i>Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (ACL)</i>, 3645–3650.",

        "Tan, M., Chen, B., Pang, R., Vasudevan, V., Sandler, M., Howard, A., & Le, Q. V. (2019). MnasNet: Platform-aware neural architecture search for mobile. <i>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 2820–2828.",

        "Tan, M., & Le, Q. V. (2019). EfficientNet: Rethinking model scaling for convolutional neural networks. <i>Proceedings of the International Conference on Machine Learning (ICML)</i>, 6105–6114.",

        "Wang, X., Peng, Y., Lu, L., Lu, Z., Bagheri, M., & Summers, R. M. (2020). ChestX-Ray14: Hospital-scale chest X-ray database and benchmarks. <i>Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 2097–2106.",

        "Wu, B., Dai, X., Zhang, P., Wang, Y., Sun, F., Wu, Y., Tian, Y., Vajda, P., Jia, Y., & Keutzer, K. (2019). FBNet: Hardware-aware efficient convNet design via differentiable neural architecture search. <i>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 10734–10742.",

        "Xie, S., Zheng, H., Liu, C., & Lin, L. (2019). SNAS: Stochastic neural architecture search. <i>International Conference on Learning Representations (ICLR)</i>. https://openreview.net/forum?id=rylqooRqK7",

        "Xu, Y., Xie, L., Zhang, X., Chen, X., Qi, G. J., Tian, Q., & Xiong, H. (2020). PC-DARTS: Partial channel connections for memory-efficient architecture search. <i>International Conference on Learning Representations (ICLR)</i>. https://openreview.net/forum?id=BJlS634tPr",

        "Yao, Y., Guan, C., & Chen, H. (2020). TextNAS: A neural architecture search space tailored for text representation. <i>Proceedings of the AAAI Conference on Artificial Intelligence</i>, <i>34</i>(05), 9242–9249.",

        "Ying, C., Klein, A., Christiansen, E., Real, E., Murphy, K., & Hutter, F. (2019). NAS-Bench-101: Towards reproducible neural architecture search. <i>Proceedings of the International Conference on Machine Learning (ICML)</i>, 7105–7114.",

        "Zoph, B., Vasudevan, V., Shlens, J., & Le, Q. V. (2018). Learning transferable architectures for scalable image recognition. <i>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 8697–8710.",
    ]

    for idx, ref in enumerate(references, 1):
        story.append(Paragraph(f"{idx}. {ref}", ref_style))

    doc.build(story)
    print(f"Initial file created: {OUTPUT}")


def _create_with_fpdf():
    """Fallback: create PDF using fpdf2."""
    from fpdf import FPDF

    os.makedirs(WORKDIR, exist_ok=True)

    class ResearchPDF(FPDF):
        def header(self):
            pass
        def footer(self):
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(128)
            self.cell(0, 10, f'Page {self.page_no()}', align='C')

    pdf = ResearchPDF()
    pdf.set_margins(25, 25, 25)
    pdf.set_auto_page_break(auto=True, margin=20)

    # Page 1 - Title page
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(26, 26, 46)
    pdf.multi_cell(0, 10, 'Advances in Neural Architecture Search: A Comprehensive Survey', align='C')
    pdf.ln(5)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(0)
    pdf.multi_cell(0, 7, 'Chen, L., Patel, R., Okonkwo, A., Yamamoto, S., & Reyes, M.', align='C')
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.multi_cell(0, 7, 'Abstract', align='C')
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(0, 7,
        'Neural Architecture Search (NAS) has emerged as a transformative paradigm in deep '
        'learning, automating the design of neural network architectures. This comprehensive '
        'survey examines state-of-the-art NAS methodologies covering reinforcement learning, '
        'evolutionary algorithms, gradient-based methods, and one-shot approaches. We analyze '
        'performance estimation strategies, hardware-aware NAS, multi-objective optimization, '
        'and emerging trends.')

    # Pages 2-17 - Paper body
    sections = [
        ('1. Introduction', 'NAS represents a paradigm shift in deep learning by automating neural architecture design. '
         'This survey covers publications from 2017-2024 from major ML conferences.'),
        ('2. Problem Formulation', 'NAS is framed as bi-level optimization. Three components define any NAS system: '
         'search space, search strategy, and performance estimation strategy.'),
        ('3. Search Strategies', 'We review RL-based, evolutionary, gradient-based, and Bayesian optimization '
         'approaches. DARTS revolutionized NAS efficiency through continuous relaxation.'),
        ('4. Performance Estimation', 'Lower-fidelity estimates, weight sharing, and one-shot methods enable '
         'efficient performance estimation without full training.'),
        ('5. Hardware-Aware NAS', 'Latency-constrained NAS enables practical deployment. Once-for-All trains '
         'a supernet for flexible deployment across devices.'),
        ('6. Multi-Objective NAS', 'NSGA-Net uses multi-objective optimization. Transfer NAS leverages '
         'knowledge from previous searches to accelerate new ones.'),
        ('7. Applications', 'NAS has advanced image classification, object detection, medical imaging, '
         'and natural language processing benchmarks.'),
        ('8. Benchmarks', 'NAS-Bench-101, NAS-Bench-201, and NAS-Bench-301 enable reproducible evaluation. '
         'Random search baselines challenge many NAS claims.'),
        ('9. Future Directions', 'Scalability, cross-domain generalization, environmental impact, '
         'and AutoML integration are key future research directions.'),
        ('10. Discussion', 'The field shifted from expensive RL/EA toward efficient one-shot methods. '
         'Hardware awareness is now a first-class optimization objective.'),
        ('11. Conclusion', 'NAS has evolved dramatically over seven years. Integration with AutoML, '
         'foundation models, and green computing represent future opportunities.'),
        ('Supplementary: Notation Table', 'A: search space, a: architecture, w: weights, '
         'L: loss function, D: dataset split notation used throughout this paper.'),
        ('Supplementary: Extended Results', 'Detailed ablation studies on CIFAR-10, CIFAR-100, '
         'ImageNet. Statistical significance tests across 5 random seeds for each method.'),
        ('Supplementary: Implementation Details', 'All experiments use PyTorch 2.0 on NVIDIA A100 GPUs. '
         'Reproducibility code and pretrained models available at github.com/nas-survey-2025.'),
        ('Supplementary: Ethical Considerations', 'Carbon emissions calculated per codecarbon.io tracker. '
         'We used renewable energy credits to offset our experimental compute costs.'),
        ('Supplementary: Author Contributions', 'L.C. led survey design and Sec. 3-4. R.P. wrote Sec. 5. '
         'A.O. wrote Sec. 7. S.Y. wrote Sec. 8. M.R. wrote Sec. 6,9.'),
    ]

    for title, content in sections:
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(26, 26, 46)
        pdf.multi_cell(0, 8, title)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0)
        pdf.multi_cell(0, 7, content)

    # Pages 18-20: References
    references = [
        "Baker, B., Gupta, O., Naik, N., & Raskar, R. (2017). Designing neural network architectures using reinforcement learning. International Conference on Learning Representations.",
        "Baid, U., Ghodasara, S., Mohan, S., & Bakas, S. (2021). The RSNA-ASNR-MICCAI BraTS 2021 benchmark on brain tumor segmentation. arXiv:2107.02314.",
        "Brock, A., Lim, T., Ritchie, J. M., & Weston, N. (2018). SMASH: One-shot model architecture search through hypernetworks. ICLR.",
        "Cai, H., Gan, C., Wang, T., Zhang, Z., & Han, S. (2020). Once-for-all: Train one network and specialize it for efficient deployment. ICLR.",
        "Cai, H., Zhu, L., & Han, S. (2019). ProxylessNAS: Direct neural architecture search on target task and hardware. ICLR.",
        "Chen, P., & Hsieh, C. J. (2020). SDARTS: Searching for accurate and stable architectures. arXiv:2006.10355.",
        "Chen, T., Goodfellow, I., & Shlens, J. (2019). Net2Net: Accelerating learning via knowledge transfer. ICLR.",
        "Chen, X., Xie, L., Wu, J., & Tian, Q. (2019). Progressive DARTS: Bridging the optimization gap for NAS in the wild. arXiv:1912.10952.",
        "Dong, X., & Yang, Y. (2019). Searching for a robust neural architecture in four GPU hours. CVPR, 1761-1770.",
        "Dong, X., & Yang, Y. (2020). NAS-Bench-201: Extending the scope of reproducible neural architecture search. ICLR.",
        "Erickson, N., Mueller, J., Shirkov, A., Zhang, H., Larroy, P., Li, M., & Smola, A. (2020). AutoGluon-tabular: Robust and accurate AutoML for structured data. arXiv:2003.06505.",
        "Feurer, M., Eggensperger, K., Falkner, S., Lindauer, M., & Hutter, F. (2022). Auto-Sklearn 2.0: Hands-free AutoML via meta-learning. Journal of Machine Learning Research, 23(261), 1-61.",
        "Gu, J., Dong, X., & Yang, Y. (2021). TaskNAS: Task-aware few-shot learning via meta neural architecture search. ICCV.",
        "Ji, S., Zhang, Z., Ji, R., & Gao, Y. (2021). AutoBERT-Zero: Evolving BERT backbone from scratch. arXiv:2107.07445.",
        "Li, L., & Talwalkar, A. (2020). Random search and reproducibility for neural architecture search. UAI, 367-377.",
        "Liang, Y., Jiang, L., & Zheng, Y. (2019). MTNAS: Multi-task neural architecture search for computer vision. arXiv:1911.04440.",
        "Liu, C., Zoph, B., Neumann, M., Shlens, J., Hua, W., Li, L. J., Fei-Fei, L., Yuille, A., Huang, J., & Murphy, K. (2018). Progressive neural architecture search. ECCV, 19-34.",
        "Liu, H., Simonyan, K., & Yang, Y. (2019). DARTS: Differentiable architecture search. ICLR.",
        "Lu, Z., Whalen, I., Boddeti, V., Dhebar, Y., Deb, K., Goodman, E., & Banzhaf, W. (2019). NSGA-Net: Neural architecture search using multi-objective genetic algorithm. GECCO, 419-427.",
        "Pham, H., Guan, M., Zoph, B., Le, Q. V., & Dean, J. (2018). Efficient neural architecture search via parameter sharing. ICML, 4095-4104.",
        "Real, E., Aggarwal, A., Huang, Y., & Le, Q. V. (2019). Regularized evolution for image classifier architecture search. AAAI, 33(01), 4780-4789.",
        "Real, E., Moore, S., Selle, A., Saxena, S., Suematsu, Y. L., Tan, J., Le, Q. V., & Kurakin, A. (2017). Large-scale evolution of image classifiers. ICML, 2902-2911.",
        "Russakovsky, O., Deng, J., Su, H., Krause, J., Satheesh, S., Ma, S., Huang, Z., Karpathy, A., Khosla, A., Bernstein, M., Berg, A. C., & Fei-Fei, L. (2015). ImageNet large scale visual recognition challenge. International Journal of Computer Vision, 115(3), 211-252.",
        "Siems, J., Zimmer, L., Zela, A., Lukasik, J., Keuper, M., & Hutter, F. (2020). NAS-Bench-301 and the case for surrogate benchmarks for neural architecture search. arXiv:2008.09777.",
        "So, D. R., Liang, C., & Le, Q. V. (2019). The Evolved Transformer. ICML, 5877-5886.",
        "Strubell, E., Ganesh, A., & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. ACL, 3645-3650.",
        "Tan, M., Chen, B., Pang, R., Vasudevan, V., Sandler, M., Howard, A., & Le, Q. V. (2019). MnasNet: Platform-aware neural architecture search for mobile. CVPR, 2820-2828.",
        "Tan, M., & Le, Q. V. (2019). EfficientNet: Rethinking model scaling for convolutional neural networks. ICML, 6105-6114.",
        "Wang, X., Peng, Y., Lu, L., Lu, Z., Bagheri, M., & Summers, R. M. (2020). ChestX-Ray14: Hospital-scale chest X-ray database and benchmarks. CVPR, 2097-2106.",
        "Wu, B., Dai, X., Zhang, P., Wang, Y., Sun, F., Wu, Y., Tian, Y., Vajda, P., Jia, Y., & Keutzer, K. (2019). FBNet: Hardware-aware efficient convNet design via differentiable NAS. CVPR, 10734-10742.",
        "Xie, S., Zheng, H., Liu, C., & Lin, L. (2019). SNAS: Stochastic neural architecture search. ICLR.",
        "Xu, Y., Xie, L., Zhang, X., Chen, X., Qi, G. J., Tian, Q., & Xiong, H. (2020). PC-DARTS: Partial channel connections for memory-efficient architecture search. ICLR.",
        "Yao, Y., Guan, C., & Chen, H. (2020). TextNAS: A neural architecture search space tailored for text representation. AAAI, 34(05), 9242-9249.",
        "Ying, C., Klein, A., Christiansen, E., Real, E., Murphy, K., & Hutter, F. (2019). NAS-Bench-101: Towards reproducible neural architecture search. ICML, 7105-7114.",
        "Zoph, B., Vasudevan, V., Shlens, J., & Le, Q. V. (2018). Learning transferable architectures for scalable image recognition. CVPR, 8697-8710.",
    ]

    ref_page_started = False
    for idx, ref in enumerate(references, 1):
        if idx == 1 or (idx == 13) or (idx == 25):
            pdf.add_page()
            if idx == 1:
                pdf.set_font('Helvetica', 'B', 13)
                pdf.set_text_color(26, 26, 46)
                pdf.cell(0, 8, 'References', ln=True)
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(0)
                pdf.ln(3)
            else:
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(0)
        text = f'{idx}. {ref}'
        pdf.multi_cell(0, 6, text)
        pdf.ln(2)

    pdf.output(OUTPUT)
    print(f'Initial file created (fpdf2): {OUTPUT}')


def main():
    create_research_paper()

    # GUI-ready startup: open the research paper PDF
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with research_paper.pdf at DISPLAY=:0')


main()
