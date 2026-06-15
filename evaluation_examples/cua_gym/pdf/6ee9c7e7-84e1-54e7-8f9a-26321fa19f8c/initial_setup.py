"""
Initial Setup: Create a 45-page academic paper PDF for chapter splitting task
Task ID: pdf_res_018
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_018'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/long_paper.pdf'

# Page dimensions (A4)
A4_W, A4_H = 595, 842

# Chapter definitions with realistic academic content
CHAPTERS = [
    {
        "title": "Chapter 1: Introduction and Background",
        "pages": 8,
        "sections": [
            ("1.1 Research Motivation",
             "The rapid advancement of machine learning techniques has transformed numerous industries, "
             "from healthcare diagnostics to autonomous vehicle navigation. Despite these breakthroughs, "
             "significant challenges remain in developing robust systems that can generalize across diverse "
             "domains. This research addresses the critical gap between laboratory performance and real-world "
             "deployment of adaptive learning systems. Our investigation focuses on the interplay between "
             "model architecture, training methodology, and environmental variability, seeking to establish "
             "a comprehensive framework for evaluating system reliability under non-stationary conditions."),
            ("1.2 Problem Statement",
             "Current approaches to domain adaptation suffer from three fundamental limitations. First, "
             "they assume a static target distribution, which rarely holds in practice. Second, the "
             "computational overhead of continuous adaptation makes real-time deployment infeasible for "
             "resource-constrained environments. Third, existing evaluation metrics fail to capture the "
             "nuanced performance degradation patterns observed in longitudinal deployments. We formalize "
             "these challenges and propose a unified mathematical framework that addresses each limitation "
             "through a novel combination of meta-learning and distributional robustness optimization."),
            ("1.3 Contributions",
             "This paper makes the following key contributions: (1) We introduce the Dynamic Adaptation "
             "Benchmark (DAB), a comprehensive evaluation suite comprising 12 real-world datasets with "
             "controlled distribution shifts. (2) We propose AdaptiveNet, a lightweight architecture that "
             "achieves state-of-the-art adaptation performance while reducing computational cost by 73%. "
             "(3) We present a theoretical analysis establishing convergence guarantees for our approach "
             "under mild assumptions on distribution smoothness. (4) We conduct extensive experiments "
             "demonstrating consistent improvements across all benchmark tasks."),
            ("1.4 Literature Review",
             "Domain adaptation has been extensively studied in the machine learning literature. Seminal "
             "works by Ben-David et al. (2010) established theoretical foundations through the concept of "
             "domain divergence. Subsequent advances include deep domain confusion networks (Tzeng et al., "
             "2014), adversarial discriminative domain adaptation (Tzeng et al., 2017), and maximum mean "
             "discrepancy approaches (Long et al., 2015). Recent trends emphasize self-supervised "
             "pre-training followed by task-specific fine-tuning, as demonstrated by BERT (Devlin et al., "
             "2019) and GPT architectures (Brown et al., 2020). However, these approaches require "
             "substantial computational resources and labeled data for effective transfer."),
        ]
    },
    {
        "title": "Chapter 2: Methodology and Framework Design",
        "pages": 12,
        "sections": [
            ("2.1 System Architecture Overview",
             "The AdaptiveNet framework consists of three interconnected modules: the Feature Extraction "
             "Module (FEM), the Distribution Alignment Module (DAM), and the Prediction Calibration Module "
             "(PCM). The FEM employs a hierarchical attention mechanism that selectively amplifies "
             "domain-invariant features while suppressing domain-specific noise. The DAM utilizes optimal "
             "transport theory to align source and target distributions in a learned latent space. The PCM "
             "applies temperature scaling and Platt calibration to ensure reliable confidence estimates "
             "across domain boundaries."),
            ("2.2 Feature Extraction Module",
             "Our feature extraction approach builds upon the Vision Transformer (ViT) backbone with "
             "several critical modifications. We introduce cross-domain attention heads that compute "
             "attention weights jointly over source and target samples within each mini-batch. This enables "
             "the model to discover shared structural patterns without explicit domain labels during "
             "inference. The module processes input through L=12 transformer layers with embedding "
             "dimension d=768, using a modified positional encoding scheme that accounts for varying "
             "input resolutions. We further incorporate gradient reversal layers at strategic positions "
             "to encourage domain-invariant representations."),
            ("2.3 Distribution Alignment Module",
             "The DAM operates on the principle of Wasserstein distance minimization between the source "
             "and target feature distributions. Unlike previous approaches that rely on kernel-based "
             "maximum mean discrepancy (MMD), our method directly estimates the optimal transport plan "
             "using Sinkhorn iterations. This provides three advantages: (1) computational efficiency "
             "scaling as O(n log n) compared to O(n^2) for kernel methods, (2) interpretable transport "
             "maps that reveal which source features correspond to which target features, and (3) natural "
             "handling of multi-modal distributions through the regularized transport formulation."),
            ("2.4 Prediction Calibration Module",
             "Calibration of model outputs is essential for trustworthy decision-making in safety-critical "
             "applications. The PCM implements a novel domain-conditional calibration scheme that learns "
             "separate temperature parameters for different regions of the input space. During training, "
             "we optimize a composite loss combining the standard cross-entropy objective with an "
             "Expected Calibration Error (ECE) penalty term. The calibration parameters are updated using "
             "a held-out calibration set, preventing overfitting to the training distribution. We prove "
             "that this approach achieves asymptotically optimal calibration under domain shift."),
            ("2.5 Training Protocol",
             "Training proceeds in three phases. Phase I (epochs 1-50) focuses on source domain "
             "pre-training using standard supervised learning. Phase II (epochs 51-100) introduces the "
             "domain alignment objective with linearly increasing weight. Phase III (epochs 101-150) "
             "jointly optimizes all objectives with the calibration module active. We employ AdamW "
             "optimizer with learning rate 3e-4, weight decay 0.01, and cosine annealing schedule. "
             "Data augmentation includes random cropping, horizontal flipping, color jittering, and "
             "our novel domain-mixing augmentation strategy that creates synthetic intermediate domains."),
            ("2.6 Theoretical Analysis",
             "We establish convergence guarantees for AdaptiveNet under the following assumptions: "
             "(A1) The source and target distributions are absolutely continuous with respect to "
             "Lebesgue measure. (A2) The density ratio is bounded above by a constant K. (A3) The "
             "labeling function is Lipschitz continuous with constant L. Under these conditions, "
             "we prove that the excess risk of AdaptiveNet decreases as O(1/sqrt(n)) where n is the "
             "number of unlabeled target samples. This matches the minimax optimal rate for domain "
             "adaptation under covariate shift, while achieving it with significantly lower computational "
             "complexity than existing methods."),
        ]
    },
    {
        "title": "Chapter 3: Experimental Evaluation",
        "pages": 15,
        "sections": [
            ("3.1 Experimental Setup",
             "We evaluate AdaptiveNet on the Dynamic Adaptation Benchmark (DAB) consisting of 12 "
             "datasets spanning four application domains: medical imaging (chest X-rays, retinal scans, "
             "histopathology), autonomous driving (nuScenes, Waymo, Cityscapes), satellite imagery "
             "(EuroSAT, BigEarthNet, fMoW), and natural language understanding (Amazon reviews, "
             "MultiNLI, SQuAD). Each dataset is paired with multiple distribution shift scenarios "
             "including temporal shift, geographical shift, acquisition protocol change, and label "
             "distribution shift. All experiments are conducted on a cluster of 8 NVIDIA A100 GPUs."),
            ("3.2 Baselines and Metrics",
             "We compare against 15 state-of-the-art methods: ERM (baseline), DANN, ADDA, MCD, CDAN, "
             "MDD, BSP, SHOT, NRC, TENT, T3A, CoTTA, SAR, EATA, and RoTTA. Performance is measured "
             "using accuracy, F1 score, Expected Calibration Error (ECE), and our proposed Adaptation "
             "Efficiency Index (AEI) which captures the trade-off between adaptation performance and "
             "computational cost. Statistical significance is assessed using paired bootstrap tests "
             "with 10,000 resamples and significance level alpha=0.05."),
            ("3.3 Medical Imaging Results",
             "On medical imaging tasks, AdaptiveNet achieves the highest average accuracy of 87.3% "
             "across all shift scenarios, compared to 83.1% for the best baseline (EATA). The most "
             "pronounced improvements are observed on temporal shift scenarios, where imaging protocols "
             "change over time. On the CheXpert temporal adaptation task, AdaptiveNet improves AUC from "
             "0.812 to 0.879, representing a 36% reduction in the performance gap relative to the "
             "oracle (trained on target data). Notably, AdaptiveNet maintains ECE below 0.05 across "
             "all medical imaging scenarios, which is crucial for clinical decision support applications."),
            ("3.4 Autonomous Driving Results",
             "For autonomous driving, we evaluate on three types of domain shift: weather conditions "
             "(clear to rainy/foggy), geographical regions (US to Europe/Asia), and sensor configurations "
             "(different LIDAR-camera setups). AdaptiveNet achieves mean IoU of 62.8% on the "
             "Cityscapes-to-nuScenes transfer, compared to 58.4% for CoTTA and 55.2% for TENT. The "
             "improvement is particularly significant for small object classes (pedestrians, cyclists) "
             "where domain shift effects are most severe. Processing latency of 23ms per frame meets "
             "real-time requirements for deployment at 30 FPS."),
            ("3.5 Satellite Imagery Results",
             "Satellite imagery presents unique challenges due to varying atmospheric conditions, "
             "acquisition angles, and spatial resolutions. On the EuroSAT geographical shift benchmark, "
             "AdaptiveNet achieves 91.2% overall accuracy with only 2.1% degradation compared to the "
             "in-domain baseline, outperforming all competitors. The fMoW temporal shift evaluation "
             "demonstrates robust performance across a 10-year time span, with accuracy declining only "
             "3.8% from 2005 to 2015 data, compared to 11.2% for the best baseline. Analysis of the "
             "learned transport maps reveals that AdaptiveNet effectively identifies and compensates for "
             "seasonal vegetation changes and urban development patterns."),
            ("3.6 Natural Language Understanding Results",
             "Cross-domain text classification experiments on Amazon reviews show AdaptiveNet achieving "
             "93.4% accuracy averaged over 12 domain pairs, surpassing DANN (88.7%) and CDAN (90.1%). "
             "On MultiNLI, adaptation from fiction to government domain yields 82.6% accuracy compared "
             "to 78.3% for the best baseline. The attention visualization reveals that our cross-domain "
             "attention mechanism successfully identifies domain-invariant linguistic patterns such as "
             "sentiment-bearing phrases and logical connectors while ignoring domain-specific vocabulary. "
             "SQuAD adaptation experiments demonstrate 71.4 F1 on out-of-domain questions."),
            ("3.7 Ablation Studies",
             "We conduct comprehensive ablation studies to quantify the contribution of each component. "
             "Removing the DAM reduces average accuracy by 4.2 percentage points, confirming the "
             "importance of explicit distribution alignment. Disabling the PCM increases ECE by 0.08 on "
             "average while having minimal impact on accuracy, suggesting that calibration and "
             "discrimination are largely orthogonal objectives. Replacing our attention-based FEM with "
             "a standard ResNet backbone reduces accuracy by 2.8 points but improves inference speed by "
             "1.7x, presenting a practical speed-accuracy tradeoff for resource-constrained deployments. "
             "The domain-mixing augmentation strategy contributes 1.5 points of accuracy improvement."),
            ("3.8 Computational Efficiency Analysis",
             "AdaptiveNet processes 142 images per second on a single A100 GPU during inference, "
             "compared to 89 for TENT and 67 for CoTTA. Training requires 18 GPU-hours for the full "
             "three-phase protocol, compared to 45 GPU-hours for CDAN and 32 GPU-hours for MDD. Memory "
             "footprint during inference is 2.1 GB, fitting comfortably within edge deployment constraints. "
             "The Sinkhorn-based alignment requires only 15 iterations to converge (compared to 50+ for "
             "exact OT solvers), contributing to the favorable computational profile. We provide detailed "
             "profiling results showing that the FEM accounts for 68% of compute, DAM for 22%, and PCM "
             "for 10%."),
        ]
    },
    {
        "title": "Chapter 4: Discussion and Conclusions",
        "pages": 10,
        "sections": [
            ("4.1 Key Findings Summary",
             "Our experimental evaluation demonstrates that AdaptiveNet consistently outperforms existing "
             "domain adaptation methods across diverse application domains and shift types. The most "
             "significant improvements are observed in scenarios with large distribution shifts, where "
             "traditional methods often fail to provide meaningful adaptation. The combination of "
             "attention-based feature extraction, optimal transport alignment, and domain-conditional "
             "calibration creates a synergistic system where each component addresses a distinct aspect "
             "of the adaptation challenge."),
            ("4.2 Practical Implications",
             "The efficiency gains of AdaptiveNet have immediate practical implications for deploying "
             "adaptive systems in production environments. Medical imaging departments can maintain "
             "diagnostic accuracy as scanning equipment is upgraded without retraining from scratch. "
             "Autonomous driving systems can adapt to new geographical regions with minimal computational "
             "overhead. Earth observation analysts can process multi-temporal satellite archives without "
             "manual recalibration. These capabilities significantly reduce the total cost of ownership "
             "for AI systems in dynamic operational environments."),
            ("4.3 Limitations",
             "Several limitations merit discussion. First, our theoretical guarantees rely on the bounded "
             "density ratio assumption (A2), which may be violated in extreme distribution shift scenarios "
             "such as zero-shot cross-lingual transfer. Second, while AdaptiveNet reduces computational "
             "cost compared to competitors, the three-phase training protocol requires careful "
             "hyperparameter tuning for optimal results. Third, our evaluation focuses on classification "
             "and segmentation tasks; extending the framework to generative tasks and reinforcement "
             "learning remains an open question. Fourth, the interpretability of the learned transport "
             "maps, while improved over kernel-based methods, still requires domain expertise to extract "
             "actionable insights."),
            ("4.4 Future Directions",
             "Several promising research directions emerge from this work. Continual adaptation in "
             "non-stationary environments represents a natural extension, where the target distribution "
             "evolves over time rather than remaining fixed. Federated domain adaptation, where source "
             "data cannot be centralized due to privacy constraints, poses additional challenges that "
             "our transport-based framework is well-positioned to address. We also plan to investigate "
             "the integration of large language models as auxiliary knowledge sources for guiding the "
             "adaptation process in multi-modal settings."),
            ("4.5 Conclusions",
             "This paper presented AdaptiveNet, a comprehensive framework for efficient and reliable "
             "domain adaptation. Through the synergistic combination of cross-domain attention, optimal "
             "transport alignment, and domain-conditional calibration, AdaptiveNet achieves "
             "state-of-the-art performance across 12 diverse benchmarks while reducing computational "
             "cost by 73% compared to the best-performing baseline. Our theoretical analysis provides "
             "convergence guarantees under mild assumptions, and our extensive ablation studies quantify "
             "the contribution of each component. The Dynamic Adaptation Benchmark introduced in this "
             "work provides a standardized evaluation framework for future research in this important "
             "area. We believe that the principles underlying AdaptiveNet, particularly the integration "
             "of distributional robustness with computational efficiency, will prove broadly applicable "
             "across machine learning applications."),
        ]
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


def create_initial():
    # Create directories
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    for chapter in CHAPTERS:
        ch_title = chapter["title"]
        sections = chapter["sections"]
        target_pages = chapter["pages"]

        # First page of chapter: chapter title page
        page = doc.new_page(width=A4_W, height=A4_H)

        # Chapter title
        page.insert_text(
            pymupdf.Point(72, 120),
            ch_title,
            fontsize=22,
            fontname="hebo",
            color=(0.1, 0.1, 0.3),
        )

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 140), pymupdf.Point(523, 140))
        shape.finish(color=(0.3, 0.3, 0.5), width=1.5)
        shape.commit()

        # Start writing section content on the first page
        y_pos = 180
        section_idx = 0
        pages_created = 1

        while pages_created < target_pages:
            if section_idx < len(sections):
                sec_title, sec_text = sections[section_idx]

                # Section title
                if y_pos > 720:
                    # Need new page
                    page = doc.new_page(width=A4_W, height=A4_H)
                    pages_created += 1
                    y_pos = 72

                page.insert_text(
                    pymupdf.Point(72, y_pos),
                    sec_title,
                    fontsize=14,
                    fontname="hebo",
                    color=(0.15, 0.15, 0.35),
                )
                y_pos += 28

                # Section body text - fill with content, wrapping across pages
                rect = pymupdf.Rect(72, y_pos, 523, 770)
                # Repeat text to fill more space
                full_text = sec_text
                while len(full_text) < 2000:
                    full_text += " " + sec_text

                excess = page.insert_textbox(
                    rect,
                    full_text,
                    fontsize=10.5,
                    fontname="helv",
                    color=(0.1, 0.1, 0.1),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )

                if excess and pages_created < target_pages:
                    # Text overflowed, continue on next page
                    remaining = full_text  # approximate
                    while pages_created < target_pages and excess:
                        page = doc.new_page(width=A4_W, height=A4_H)
                        pages_created += 1

                        # Page header
                        page.insert_text(
                            pymupdf.Point(72, 42),
                            ch_title,
                            fontsize=8,
                            fontname="heit",
                            color=(0.5, 0.5, 0.5),
                        )

                        y_pos = 72
                        rect = pymupdf.Rect(72, y_pos, 523, 770)
                        excess = page.insert_textbox(
                            rect,
                            remaining,
                            fontsize=10.5,
                            fontname="helv",
                            color=(0.1, 0.1, 0.1),
                            align=pymupdf.TEXT_ALIGN_JUSTIFY,
                        )

                    y_pos = 770
                else:
                    y_pos = 770  # force next section to new page

                section_idx += 1
            else:
                # No more sections, fill remaining pages with continuation text
                page = doc.new_page(width=A4_W, height=A4_H)
                pages_created += 1

                # Page header
                page.insert_text(
                    pymupdf.Point(72, 42),
                    ch_title,
                    fontsize=8,
                    fontname="heit",
                    color=(0.5, 0.5, 0.5),
                )

                filler_text = (
                    "Additional analysis and supplementary discussion for this chapter continues here. "
                    "The detailed mathematical proofs and derivations supporting the theoretical claims "
                    "made in previous sections are presented in full. We provide step-by-step verification "
                    "of each lemma and theorem, including the measure-theoretic foundations required for "
                    "the optimal transport formulation. Extended experimental results with additional "
                    "hyperparameter configurations and ablation studies are tabulated for completeness. "
                    "Cross-validation results across five random seeds demonstrate the statistical "
                    "stability of our findings. Visualization of learned feature spaces using t-SNE and "
                    "UMAP projections further illustrate the effectiveness of the domain alignment module. "
                    "Comparison with concurrent work published during the review period of this manuscript "
                    "is included to position our contributions within the rapidly evolving landscape. "
                    "Detailed resource utilization profiles for different hardware configurations help "
                    "practitioners estimate deployment costs for their specific use cases."
                )
                while len(filler_text) < 3000:
                    filler_text += " " + filler_text[:500]

                rect = pymupdf.Rect(72, 72, 523, 770)
                page.insert_textbox(
                    rect,
                    filler_text,
                    fontsize=10.5,
                    fontname="helv",
                    color=(0.1, 0.1, 0.1),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )

        # Add page numbers
        # (page numbers added later for all pages)

    # Add page numbers to all pages
    for i in range(doc.page_count):
        p = doc[i]
        p.insert_text(
            pymupdf.Point(290, 820),
            str(i + 1),
            fontsize=9,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

    # Verify page count
    assert doc.page_count == 45, f"Expected 45 pages, got {doc.page_count}"

    # Add metadata
    doc.set_metadata({
        "title": "AdaptiveNet: Efficient Domain Adaptation via Optimal Transport Alignment",
        "author": "Research Team",
        "subject": "Machine Learning, Domain Adaptation",
        "keywords": "domain adaptation, optimal transport, deep learning",
    })

    # Add table of contents
    toc = [
        [1, "Chapter 1: Introduction and Background", 1],
        [1, "Chapter 2: Methodology and Framework Design", 9],
        [1, "Chapter 3: Experimental Evaluation", 21],
        [1, "Chapter 4: Discussion and Conclusions", 36],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 45')

    # Open in Evince for GUI readiness
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
