"""
Initial Setup: Create an 8-page neural networks research paper PDF
Task ID: pdf_res_002
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_002'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/neural_nets.pdf'

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

    # --- Page dimensions ---
    W, H = 595, 842  # A4

    # --- Common layout constants ---
    LEFT = 72
    RIGHT = W - 72
    TEXT_W = RIGHT - LEFT
    TOP_START = 72
    LINE_H = 14  # line height for body text
    HEADING_SIZE = 14
    BODY_SIZE = 10.5
    TITLE_SIZE = 20
    AUTHOR_SIZE = 11

    # ============================================================
    # PAGE 1: Title, Authors, Abstract
    # ============================================================
    page = doc.new_page(width=W, height=H)
    y = 100
    # Title
    page.insert_text(pymupdf.Point(W/2 - 180, y),
                     "Deep Neural Networks for Robust",
                     fontsize=TITLE_SIZE, fontname="tibo", color=(0, 0, 0))
    y += 28
    page.insert_text(pymupdf.Point(W/2 - 160, y),
                     "Image Classification Under Noise",
                     fontsize=TITLE_SIZE, fontname="tibo", color=(0, 0, 0))
    y += 40
    # Authors
    authors = "Elena Marchetti, Rajesh Patel, Yuki Tanaka, David Okonkwo"
    page.insert_text(pymupdf.Point(W/2 - 170, y),
                     authors,
                     fontsize=AUTHOR_SIZE, fontname="tiit", color=(0.2, 0.2, 0.2))
    y += 18
    page.insert_text(pymupdf.Point(W/2 - 140, y),
                     "Department of Computer Science, Westfield University",
                     fontsize=9, fontname="tiro", color=(0.3, 0.3, 0.3))
    y += 14
    page.insert_text(pymupdf.Point(W/2 - 100, y),
                     "{emarchetti, rpatel, ytanaka, dokonkwo}@westfield.edu",
                     fontsize=9, fontname="cour", color=(0.3, 0.3, 0.3))

    y += 40
    # Abstract heading
    page.insert_text(pymupdf.Point(W/2 - 30, y),
                     "Abstract",
                     fontsize=12, fontname="tibo", color=(0, 0, 0))
    y += 20
    abstract = (
        "We present a comprehensive study on the robustness of deep neural network architectures "
        "for image classification tasks under varying levels of Gaussian, salt-and-pepper, and "
        "adversarial noise. Our investigation covers convolutional neural networks (CNNs), residual "
        "networks (ResNets), and vision transformers (ViTs) trained on CIFAR-100 and ImageNet-1K "
        "datasets. We introduce a novel data augmentation strategy called Adaptive Noise Injection "
        "(ANI) that dynamically adjusts noise parameters during training based on model confidence "
        "scores. Experimental results demonstrate that ANI improves top-1 accuracy by 3.7% on "
        "average across all architectures when evaluated on corrupted test sets, while maintaining "
        "competitive performance on clean data. We further analyze the learned feature representations "
        "through gradient-weighted class activation mapping (Grad-CAM) and find that ANI-trained "
        "models attend to more semantically meaningful regions compared to standard augmentation baselines."
    )
    rect = pymupdf.Rect(LEFT + 20, y, RIGHT - 20, y + 160)
    page.insert_textbox(rect, abstract, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    y += 175
    # Keywords
    page.insert_text(pymupdf.Point(LEFT + 20, y),
                     "Keywords: ",
                     fontsize=BODY_SIZE, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(LEFT + 80, y),
                     "deep learning, image classification, robustness, noise augmentation, vision transformers",
                     fontsize=BODY_SIZE, fontname="tiit", color=(0, 0, 0))

    # ============================================================
    # PAGE 2: Introduction
    # ============================================================
    page = doc.new_page(width=W, height=H)
    y = TOP_START
    page.insert_text(pymupdf.Point(LEFT, y), "1. Introduction",
                     fontsize=HEADING_SIZE, fontname="tibo", color=(0, 0, 0))
    y += 24
    intro_text = (
        "The deployment of deep neural networks in safety-critical applications such as autonomous "
        "driving, medical imaging, and surveillance systems demands robust performance under "
        "real-world conditions. While state-of-the-art models achieve remarkable accuracy on "
        "curated benchmark datasets, their performance often degrades significantly when confronted "
        "with noisy or corrupted inputs that are commonplace in practical deployment scenarios.\n\n"
        "Recent work by Hendrycks and Dietterich (2019) established standardized benchmarks for "
        "evaluating model robustness, revealing that even top-performing architectures suffer "
        "accuracy drops of 40-60% on corrupted versions of ImageNet. This vulnerability poses "
        "significant risks in applications where misclassification can have severe consequences.\n\n"
        "Several approaches have been proposed to address this challenge. Data augmentation "
        "strategies, including Mixup (Zhang et al., 2018), CutMix (Yun et al., 2019), and "
        "AugMax (Wang et al., 2021), introduce controlled perturbations during training to improve "
        "generalization. Adversarial training methods (Madry et al., 2018) explicitly optimize "
        "against worst-case perturbations but often sacrifice clean accuracy.\n\n"
        "In this paper, we propose Adaptive Noise Injection (ANI), a training-time augmentation "
        "strategy that dynamically calibrates noise intensity based on the model's current "
        "confidence distribution over the training batch. Unlike fixed augmentation schedules, "
        "ANI increases perturbation strength when the model is overconfident and reduces it when "
        "the model struggles, creating a curriculum-like effect that encourages progressive "
        "robustness acquisition.\n\n"
        "Our contributions are as follows: (1) We introduce ANI, an adaptive noise augmentation "
        "framework compatible with any differentiable model; (2) We conduct extensive experiments "
        "across three major architectures on two large-scale datasets; (3) We provide detailed "
        "ablation studies and feature visualization analyses demonstrating the mechanisms by which "
        "ANI enhances robustness."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    page.insert_textbox(rect, intro_text, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 3: Related Work
    # ============================================================
    page = doc.new_page(width=W, height=H)
    y = TOP_START
    page.insert_text(pymupdf.Point(LEFT, y), "2. Related Work",
                     fontsize=HEADING_SIZE, fontname="tibo", color=(0, 0, 0))
    y += 24
    page.insert_text(pymupdf.Point(LEFT, y), "2.1 Noise Robustness in Deep Learning",
                     fontsize=12, fontname="tibo", color=(0, 0, 0))
    y += 20
    rw1 = (
        "The study of noise robustness in neural networks dates back to the seminal work of "
        "Bishop (1995), who showed that training with noise is equivalent to a form of regularization. "
        "More recently, the ImageNet-C benchmark (Hendrycks and Dietterich, 2019) provided a "
        "standardized suite of 15 corruption types at 5 severity levels, enabling systematic "
        "comparison across methods. Subsequent work extended this to ImageNet-3DCC (Kar et al., 2022) "
        "with 3D-aware corruptions.\n\n"
        "Ford et al. (2019) demonstrated a strong connection between adversarial robustness and "
        "corruption robustness, suggesting that defenses against adversarial examples may transfer "
        "to natural corruptions. However, Kang et al. (2019) found this transfer is architecture "
        "and corruption-type dependent."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 140)
    page.insert_textbox(rect, rw1, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 155

    page.insert_text(pymupdf.Point(LEFT, y), "2.2 Data Augmentation Strategies",
                     fontsize=12, fontname="tibo", color=(0, 0, 0))
    y += 20
    rw2 = (
        "Data augmentation has emerged as one of the most effective and efficient strategies for "
        "improving model robustness. Classical approaches include random cropping, flipping, and "
        "color jittering (Krizhevsky et al., 2012). AutoAugment (Cubuk et al., 2019) introduced "
        "learned augmentation policies using reinforcement learning, while RandAugment (Cubuk et al., "
        "2020) simplified this with random selection from a predefined transformation set.\n\n"
        "Mixing-based augmentations have shown particular promise. Mixup (Zhang et al., 2018) "
        "creates convex combinations of training examples and labels. CutMix (Yun et al., 2019) "
        "replaces rectangular regions with patches from other images. AugMax (Wang et al., 2021) "
        "combines multiple augmentations and selects the worst case for training."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 140)
    page.insert_textbox(rect, rw2, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 155

    page.insert_text(pymupdf.Point(LEFT, y), "2.3 Vision Transformers and Robustness",
                     fontsize=12, fontname="tibo", color=(0, 0, 0))
    y += 20
    rw3 = (
        "Vision Transformers (Dosovitskiy et al., 2021) have demonstrated competitive or superior "
        "performance compared to CNNs on various benchmarks. Bhojanapalli et al. (2021) showed that "
        "ViTs are inherently more robust to natural corruptions than CNNs of similar capacity, "
        "attributing this to the self-attention mechanism's ability to capture global dependencies. "
        "However, Paul and Chen (2022) noted that this advantage diminishes with targeted adversarial "
        "attacks designed specifically for transformer architectures."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    page.insert_textbox(rect, rw3, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 4: Methodology (contains "experimental setup" at ~y=350)
    # ============================================================
    page = doc.new_page(width=W, height=H)
    y = TOP_START
    page.insert_text(pymupdf.Point(LEFT, y), "3. Methodology",
                     fontsize=HEADING_SIZE, fontname="tibo", color=(0, 0, 0))
    y += 24
    page.insert_text(pymupdf.Point(LEFT, y), "3.1 Adaptive Noise Injection (ANI)",
                     fontsize=12, fontname="tibo", color=(0, 0, 0))
    y += 20
    method1 = (
        "Our proposed method, Adaptive Noise Injection (ANI), operates by monitoring the model's "
        "prediction confidence during training and adjusting the noise magnitude accordingly. "
        "Given a mini-batch B of training samples, we compute the average maximum softmax "
        "probability as a proxy for model confidence. When confidence exceeds a threshold tau, "
        "we increase the noise standard deviation sigma by a factor alpha; when confidence drops "
        "below tau, we decrease sigma by a factor beta. This creates an adaptive curriculum where "
        "the model faces progressively harder perturbations as it becomes more capable.\n\n"
        "Formally, let p_max(x) denote the maximum softmax probability for input x. The noise "
        "parameter at training step t is updated as follows:\n\n"
        "    sigma_t = sigma_{t-1} * alpha   if  E[p_max(x)] > tau\n"
        "    sigma_t = sigma_{t-1} * beta    if  E[p_max(x)] <= tau\n\n"
        "where alpha > 1 and 0 < beta < 1 are hyperparameters controlling the adaptation rate. "
        "We set default values of alpha=1.05, beta=0.95, and tau=0.8 based on preliminary experiments."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 180)
    page.insert_textbox(rect, method1, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 190

    # "experimental setup" heading placed at approximately y=350
    page.insert_text(pymupdf.Point(LEFT, 350), "3.2 Experimental Setup",
                     fontsize=12, fontname="tibo", color=(0, 0, 0))
    y = 370
    method2 = (
        "We evaluate ANI across three architectures: ResNet-50 (He et al., 2016), "
        "EfficientNet-B4 (Tan and Le, 2019), and ViT-B/16 (Dosovitskiy et al., 2021). "
        "All models are trained on CIFAR-100 and ImageNet-1K with standard preprocessing "
        "pipelines. For CIFAR-100, images are resized to 32x32 with random horizontal flipping "
        "and normalization. For ImageNet-1K, we use 224x224 center crops with random resized "
        "cropping and horizontal flipping during training.\n\n"
        "Training proceeds for 200 epochs on CIFAR-100 and 90 epochs on ImageNet-1K using SGD "
        "with momentum 0.9 and weight decay 1e-4. The initial learning rate is set to 0.1 with "
        "cosine annealing. We apply ANI with three noise types: Gaussian (sigma_0=0.1), "
        "salt-and-pepper (probability p_0=0.05), and adversarial (PGD with epsilon_0=4/255). "
        "The confidence threshold tau is set to 0.8 for all experiments.\n\n"
        "We compare against five baselines: standard training (no augmentation), Gaussian noise "
        "augmentation (fixed sigma=0.2), Mixup (alpha=0.2), AugMax, and adversarial training "
        "(PGD-7, epsilon=8/255). All models are evaluated on clean test sets and corrupted "
        "versions using the ImageNet-C protocol."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    page.insert_textbox(rect, method2, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 5: Results - Tables
    # ============================================================
    page = doc.new_page(width=W, height=H)
    y = TOP_START
    page.insert_text(pymupdf.Point(LEFT, y), "4. Results",
                     fontsize=HEADING_SIZE, fontname="tibo", color=(0, 0, 0))
    y += 24
    page.insert_text(pymupdf.Point(LEFT, y), "4.1 CIFAR-100 Results",
                     fontsize=12, fontname="tibo", color=(0, 0, 0))
    y += 20
    results1 = (
        "Table 1 presents the classification accuracy of all models on clean and corrupted "
        "CIFAR-100 test sets. ANI consistently improves robustness across all architectures "
        "and corruption types while maintaining competitive clean accuracy."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 40)
    page.insert_textbox(rect, results1, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 50

    # Table 1 header
    page.insert_text(pymupdf.Point(LEFT, y),
                     "Table 1: CIFAR-100 Top-1 Accuracy (%) under various corruptions",
                     fontsize=9, fontname="tibo", color=(0, 0, 0))
    y += 16
    # Draw table
    cols = [LEFT, LEFT+110, LEFT+175, LEFT+240, LEFT+305, LEFT+370]
    headers = ["Method", "Clean", "Gaussian", "S&P", "Adversarial", "Mean"]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(cols[i], y), h,
                         fontsize=9, fontname="tibo", color=(0, 0, 0))
    y += 4
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(LEFT, y), pymupdf.Point(RIGHT-40, y))
    shape.finish(color=(0, 0, 0), width=0.5)
    y += 14
    table_data = [
        ["Standard", "78.3", "52.1", "49.8", "12.4", "48.2"],
        ["Gaussian Aug.", "76.9", "61.3", "58.7", "14.2", "52.8"],
        ["Mixup", "79.1", "58.4", "55.9", "15.8", "51.8"],
        ["AugMax", "77.2", "63.8", "61.2", "18.9", "55.3"],
        ["Adv. Training", "74.5", "59.7", "57.3", "35.2", "56.7"],
        ["ANI (Ours)", "77.8", "66.1", "64.5", "28.7", "59.3"],
    ]
    for row in table_data:
        for i, val in enumerate(row):
            fn = "tibo" if row[0] == "ANI (Ours)" else "tiro"
            page.insert_text(pymupdf.Point(cols[i], y), val, fontsize=9, fontname=fn, color=(0, 0, 0))
        y += 14
    shape.draw_line(pymupdf.Point(LEFT, y - 4), pymupdf.Point(RIGHT-40, y - 4))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()

    y += 20
    page.insert_text(pymupdf.Point(LEFT, y), "4.2 ImageNet-1K Results",
                     fontsize=12, fontname="tibo", color=(0, 0, 0))
    y += 20
    results2 = (
        "On the larger-scale ImageNet-1K benchmark, ANI demonstrates even more pronounced "
        "improvements. Table 2 shows results for ResNet-50 architecture, where ANI achieves "
        "the best mean corruption accuracy of 47.2%, outperforming the next best method "
        "(AugMax) by 2.8 percentage points. Notably, ANI maintains 75.9% clean accuracy, "
        "only 0.5% below the standard training baseline, indicating minimal sacrifice of "
        "clean performance for substantially improved robustness."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 80)
    page.insert_textbox(rect, results2, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 6: Results - Analysis
    # ============================================================
    page = doc.new_page(width=W, height=H)
    y = TOP_START
    page.insert_text(pymupdf.Point(LEFT, y), "4.3 Ablation Studies",
                     fontsize=12, fontname="tibo", color=(0, 0, 0))
    y += 20
    ablation = (
        "We conduct ablation studies to understand the contribution of each component in ANI. "
        "First, we examine the effect of the confidence threshold tau by varying it from 0.5 to "
        "0.95. Results indicate that tau=0.8 provides the best trade-off between clean and "
        "corrupted accuracy. Lower thresholds lead to overly aggressive noise injection early in "
        "training, while higher thresholds delay adaptation and reduce the training-time benefit.\n\n"
        "Second, we evaluate the adaptation rates alpha and beta. Faster adaptation (alpha=1.1, "
        "beta=0.9) causes oscillation in the noise schedule, while slower rates (alpha=1.02, "
        "beta=0.98) converge to suboptimal noise levels. The default values of alpha=1.05 and "
        "beta=0.95 achieve a stable, monotonically increasing noise schedule that aligns with "
        "the model's learning curve.\n\n"
        "Third, we test ANI with individual noise types versus the combined multi-noise variant. "
        "While single-noise ANI improves robustness to the corresponding corruption, the combined "
        "approach provides broader generalization. Gaussian-only ANI improves Gaussian corruption "
        "accuracy by 15.2% but adversarial accuracy by only 2.1%. The combined ANI achieves "
        "balanced improvements of 14.0%, 14.7%, and 16.3% for Gaussian, salt-and-pepper, and "
        "adversarial corruptions respectively."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 250)
    page.insert_textbox(rect, ablation, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 265

    page.insert_text(pymupdf.Point(LEFT, y), "4.4 Feature Visualization Analysis",
                     fontsize=12, fontname="tibo", color=(0, 0, 0))
    y += 20
    feature_vis = (
        "To understand how ANI affects learned representations, we employ Grad-CAM visualization "
        "on the final convolutional layer of ResNet-50. Figure 3 shows Grad-CAM heatmaps for "
        "representative images from ImageNet-1K. Standard-trained models tend to focus on small, "
        "often spurious regions (e.g., background textures), while ANI-trained models attend to "
        "larger, more semantically meaningful regions corresponding to the actual object.\n\n"
        "Quantitatively, we measure the intersection-over-union (IoU) between Grad-CAM activation "
        "regions and ground-truth bounding boxes on ImageNet-S (Gao et al., 2022). ANI-trained "
        "ResNet-50 achieves a mean IoU of 0.43, compared to 0.31 for standard training and 0.38 "
        "for adversarial training, suggesting that ANI encourages more semantically grounded "
        "feature learning."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    page.insert_textbox(rect, feature_vis, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 7: Discussion
    # ============================================================
    page = doc.new_page(width=W, height=H)
    y = TOP_START
    page.insert_text(pymupdf.Point(LEFT, y), "5. Discussion",
                     fontsize=HEADING_SIZE, fontname="tibo", color=(0, 0, 0))
    y += 24
    discussion = (
        "Our experimental results demonstrate that Adaptive Noise Injection provides a principled "
        "and effective approach to improving the robustness of deep neural networks without "
        "significant clean accuracy degradation. The adaptive nature of ANI distinguishes it from "
        "fixed augmentation strategies, which often require extensive hyperparameter tuning for "
        "each architecture and dataset combination.\n\n"
        "The feature visualization analysis provides insights into the mechanism behind ANI's "
        "effectiveness. By progressively increasing noise intensity as the model becomes more "
        "confident, ANI forces the network to rely on robust, high-level semantic features "
        "rather than fragile low-level patterns. This aligns with theoretical work by Ilyas et al. "
        "(2019), who argued that non-robust features contribute significantly to standard accuracy "
        "but are eliminated under perturbation.\n\n"
        "A limitation of our approach is the computational overhead introduced by the confidence "
        "monitoring step, which requires an additional forward pass through the batch to compute "
        "softmax probabilities. In practice, this adds approximately 15% to training time. Future "
        "work could explore more efficient confidence estimation methods, such as using the "
        "logit magnitudes directly.\n\n"
        "Another area for future investigation is the application of ANI to other domains beyond "
        "image classification, including object detection, semantic segmentation, and natural "
        "language processing. The general principle of adaptive perturbation scheduling based on "
        "model confidence is domain-agnostic, though the specific noise types would need to be "
        "adapted to the input modality.\n\n"
        "We also note that while ANI improves robustness to common corruptions, it does not "
        "provide certified robustness guarantees. Combining ANI with certified defense methods "
        "(Cohen et al., 2019) could potentially yield models that are both practically and "
        "provably robust."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, H - 60)
    page.insert_textbox(rect, discussion, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ============================================================
    # PAGE 8: Conclusion & References
    # ============================================================
    page = doc.new_page(width=W, height=H)
    y = TOP_START
    page.insert_text(pymupdf.Point(LEFT, y), "6. Conclusion",
                     fontsize=HEADING_SIZE, fontname="tibo", color=(0, 0, 0))
    y += 24
    conclusion = (
        "We presented Adaptive Noise Injection (ANI), a dynamic data augmentation strategy that "
        "calibrates perturbation intensity based on model confidence during training. Through "
        "comprehensive experiments on CIFAR-100 and ImageNet-1K using ResNet-50, EfficientNet-B4, "
        "and ViT-B/16 architectures, we demonstrated that ANI achieves state-of-the-art mean "
        "corruption accuracy while maintaining competitive clean performance. Feature visualization "
        "analysis revealed that ANI encourages models to learn more semantically meaningful "
        "representations, providing an explanation for its robustness benefits."
    )
    rect = pymupdf.Rect(LEFT, y, RIGHT, y + 90)
    page.insert_textbox(rect, conclusion, fontsize=BODY_SIZE, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 110

    page.insert_text(pymupdf.Point(LEFT, y), "References",
                     fontsize=HEADING_SIZE, fontname="tibo", color=(0, 0, 0))
    y += 20
    references = [
        "Bhojanapalli, S., et al. (2021). Understanding robustness of transformers for image classification. ICCV.",
        "Bishop, C. M. (1995). Training with noise is equivalent to Tikhonov regularization. Neural Computation.",
        "Cohen, J., et al. (2019). Certified adversarial robustness via randomized smoothing. ICML.",
        "Cubuk, E. D., et al. (2019). AutoAugment: Learning augmentation strategies from data. CVPR.",
        "Cubuk, E. D., et al. (2020). RandAugment: Practical automated data augmentation. NeurIPS.",
        "Dosovitskiy, A., et al. (2021). An image is worth 16x16 words: Transformers for image recognition. ICLR.",
        "Ford, N., et al. (2019). Adversarial examples are not bugs, they are features. NeurIPS.",
        "Gao, S., et al. (2022). Large-scale unsupervised semantic segmentation. TPAMI.",
        "He, K., et al. (2016). Deep residual learning for image recognition. CVPR.",
        "Hendrycks, D. and Dietterich, T. (2019). Benchmarking neural network robustness to common corruptions. ICLR.",
        "Ilyas, A., et al. (2019). Adversarial examples are not bugs, they are features. NeurIPS.",
        "Kang, D., et al. (2019). Testing robustness against unforeseen adversaries. arXiv:1908.08016.",
        "Kar, O., et al. (2022). 3D Common Corruptions and Data Augmentation. CVPR.",
        "Krizhevsky, A., et al. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS.",
        "Madry, A., et al. (2018). Towards deep learning models resistant to adversarial attacks. ICLR.",
        "Paul, S. and Chen, P. (2022). Vision transformers are robust learners. AAAI.",
        "Tan, M. and Le, Q. V. (2019). EfficientNet: Rethinking model scaling for CNNs. ICML.",
        "Wang, H., et al. (2021). Augmax: Adversarial composition of random augmentations. NeurIPS.",
        "Yun, S., et al. (2019). CutMix: Regularization strategy to train strong classifiers. ICCV.",
        "Zhang, H., et al. (2018). mixup: Beyond empirical risk minimization. ICLR.",
    ]
    for ref in references:
        rect = pymupdf.Rect(LEFT, y, RIGHT, y + 24)
        page.insert_textbox(rect, ref, fontsize=8, fontname="tiro",
                            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        y += 22

    shape.commit() if hasattr(shape, 'commit') else None

    # Add page numbers to all pages
    for i in range(len(doc)):
        p = doc[i]
        p.insert_text(pymupdf.Point(W/2 - 5, H - 30), str(i + 1),
                      fontsize=10, fontname="tiro", color=(0.4, 0.4, 0.4))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince at page 4
    launch_gui(f'evince --page-index=3 "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
