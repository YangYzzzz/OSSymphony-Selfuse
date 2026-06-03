"""
Initial Setup: Create unlabeled academic paper PDF with 6 images and no figure captions
Task ID: pdf_res_075
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_075'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/unlabeled_paper.pdf'

# Page dimensions (Letter size)
W, H = 612, 792
MARGIN = 72
TEXT_W = W - 2 * MARGIN

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


def add_text(page, x, y, text, fontsize=11, fontname="helv", color=(0, 0, 0)):
    """Insert text and return approximate new y position."""
    page.insert_text(pymupdf.Point(x, y), text, fontsize=fontsize, fontname=fontname, color=color)
    return y + fontsize + 4


def add_paragraph(page, x, y, text, fontsize=11, fontname="helv", max_width=None):
    """Insert a paragraph within a textbox and return new y."""
    if max_width is None:
        max_width = TEXT_W
    rect = pymupdf.Rect(x, y, x + max_width, y + 400)
    excess = page.insert_textbox(rect, text, fontsize=fontsize, fontname=fontname,
                                  color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # Estimate lines used
    avg_chars_per_line = max_width / (fontsize * 0.5)
    num_lines = max(1, len(text) / avg_chars_per_line)
    used_height = num_lines * (fontsize + 3) + 8
    return y + used_height


def create_colored_image(width, height, color_rgb):
    """Create a simple colored PNG image in memory as bytes."""
    from PIL import Image as PILImage
    import io
    img = PILImage.new("RGB", (width, height), color_rgb)
    # Add some visual pattern to make it look like a figure
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    # Draw grid lines
    for i in range(0, width, width // 8):
        draw.line([(i, 0), (i, height)], fill=(200, 200, 200), width=1)
    for j in range(0, height, height // 6):
        draw.line([(0, j), (width, j)], fill=(200, 200, 200), width=1)
    # Draw some bars/shapes to simulate chart data
    bar_w = width // 10
    import random
    random.seed(sum(color_rgb))
    for k in range(6):
        bx = width // 8 + k * (bar_w + bar_w // 2)
        bar_h = random.randint(height // 4, height * 3 // 4)
        r = max(0, color_rgb[0] - 40)
        g = max(0, color_rgb[1] - 40)
        b = max(0, color_rgb[2] - 40)
        draw.rectangle([bx, height - bar_h - 10, bx + bar_w, height - 10], fill=(r, g, b))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def create_initial():
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # =========================================================================
    # Page 1: Title page
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    y = 120
    page.insert_text(pymupdf.Point(W/2 - 180, y), "Adaptive Multi-Scale Feature Fusion for",
                     fontsize=18, fontname="tibo", color=(0, 0, 0))
    y += 26
    page.insert_text(pymupdf.Point(W/2 - 170, y), "Real-Time Object Detection in Urban Scenes",
                     fontsize=18, fontname="tibo", color=(0, 0, 0))
    y += 50
    page.insert_text(pymupdf.Point(W/2 - 140, y), "Yiming Zhang, Priya Sharma, David Kim",
                     fontsize=12, fontname="tiit", color=(0.2, 0.2, 0.2))
    y += 20
    page.insert_text(pymupdf.Point(W/2 - 160, y), "Department of Computer Science, Stanford University",
                     fontsize=11, fontname="tiit", color=(0.3, 0.3, 0.3))
    y += 18
    page.insert_text(pymupdf.Point(W/2 - 100, y), "{yzhang, psharma, dkim}@stanford.edu",
                     fontsize=10, fontname="cour", color=(0.3, 0.3, 0.3))

    y += 50
    page.insert_text(pymupdf.Point(MARGIN, y), "Abstract", fontsize=14, fontname="tibo")
    y += 22
    abstract = (
        "We present a novel multi-scale feature fusion architecture designed for real-time object detection "
        "in complex urban environments. Our approach introduces an adaptive gating mechanism that dynamically "
        "selects and combines features from multiple resolution levels based on scene complexity. Experiments "
        "on the UrbanDet-5K and CityScapes benchmarks demonstrate that our method achieves state-of-the-art "
        "accuracy while maintaining inference speeds above 45 FPS on a single NVIDIA RTX 4090. The proposed "
        "Adaptive Feature Pyramid Network (AFPN) reduces false positive rates by 23.7% compared to standard "
        "FPN architectures, particularly for small and occluded objects. We also introduce a novel context-aware "
        "non-maximum suppression strategy that improves detection consistency across consecutive frames."
    )
    y = add_paragraph(page, MARGIN, y, abstract, fontsize=10, fontname="tiit")

    y += 15
    page.insert_text(pymupdf.Point(MARGIN, y), "1  Introduction", fontsize=14, fontname="tibo")
    y += 22
    intro1 = (
        "Object detection in urban scenes presents unique challenges due to varying object scales, occlusion "
        "patterns, and cluttered backgrounds. While modern deep learning approaches have achieved remarkable "
        "progress on standard benchmarks such as COCO and Pascal VOC, their performance often degrades "
        "significantly when deployed in real-world urban monitoring systems. The primary bottleneck lies in "
        "the inability of existing feature pyramid networks to adaptively weight feature contributions from "
        "different scales based on the input scene characteristics."
    )
    y = add_paragraph(page, MARGIN, y, intro1, fontsize=11)

    intro2 = (
        "Recent studies by Chen et al. (2024) and Nakamura & Okoye (2023) have highlighted the importance of "
        "multi-scale reasoning for detecting small pedestrians and vehicles in dense traffic scenarios. However, "
        "these methods rely on fixed fusion weights that cannot adapt to the wide variety of scenes encountered "
        "in urban deployments. In this paper, we address this limitation through an attention-based gating "
        "mechanism that learns to modulate feature fusion weights conditioned on global scene descriptors."
    )
    y = add_paragraph(page, MARGIN, y, intro2, fontsize=11)

    # =========================================================================
    # Page 2: More introduction + Figure 1 (architecture overview)
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    y = MARGIN + 10
    intro3 = (
        "Our contributions are threefold: (1) we propose the Adaptive Feature Pyramid Network (AFPN) that "
        "dynamically adjusts fusion weights based on input complexity, (2) we design a context-aware NMS "
        "module that leverages temporal consistency for video-based detection, and (3) we compile and release "
        "the UrbanDet-5K benchmark, consisting of 5,000 annotated urban scenes from 12 cities worldwide."
    )
    y = add_paragraph(page, MARGIN, y, intro3, fontsize=11)
    y += 10

    page.insert_text(pymupdf.Point(MARGIN, y), "2  Related Work", fontsize=14, fontname="tibo")
    y += 22
    rw1 = (
        "Feature pyramid networks (FPN) were first introduced by Lin et al. (2017) and have since become a "
        "foundational component in most modern object detection architectures. PANet (Liu et al., 2018) "
        "added bottom-up path augmentation, while BiFPN (Tan et al., 2020) proposed weighted bidirectional "
        "feature fusion. NAS-FPN (Ghiasi et al., 2019) used neural architecture search to discover optimal "
        "feature fusion topologies, but the resulting architectures lack interpretability and generalization."
    )
    y = add_paragraph(page, MARGIN, y, rw1, fontsize=11)

    rw2 = (
        "Attention mechanisms have been widely adopted for feature recalibration. Squeeze-and-Excitation "
        "networks (Hu et al., 2018) introduced channel attention, while CBAM (Woo et al., 2018) combined "
        "channel and spatial attention. More recently, transformer-based detectors such as DETR (Carion et al., "
        "2020) and Deformable DETR (Zhu et al., 2021) have shown that global attention can replace hand-crafted "
        "components, though they typically require longer training schedules and higher computational budgets."
    )
    y = add_paragraph(page, MARGIN, y, rw2, fontsize=11)
    y += 10

    # IMAGE 1: Architecture diagram
    img1_data = create_colored_image(400, 180, (70, 130, 180))
    img1_rect = pymupdf.Rect(MARGIN + 40, y, W - MARGIN - 40, y + 180)
    page.insert_image(img1_rect, stream=img1_data)
    # NO CAPTION - this is the unlabeled version

    # =========================================================================
    # Page 3: Methodology
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    y = MARGIN + 10
    page.insert_text(pymupdf.Point(MARGIN, y), "3  Methodology", fontsize=14, fontname="tibo")
    y += 22
    m1 = (
        "Our approach builds upon the standard FPN backbone with three key modifications. First, we replace "
        "static lateral connections with learned gating modules that control information flow between scales. "
        "Second, we introduce a global scene descriptor that provides top-down contextual guidance to the "
        "gating modules. Third, we augment the detection head with a temporal consistency module for video input."
    )
    y = add_paragraph(page, MARGIN, y, m1, fontsize=11)

    page.insert_text(pymupdf.Point(MARGIN, y + 5), "3.1  Adaptive Gating Module", fontsize=12, fontname="tibo")
    y += 28
    m2 = (
        "Let F_l denote the feature map at pyramid level l, with spatial resolution (H/2^l, W/2^l). The "
        "standard FPN computes the fused feature at level l as G_l = F_l + Upsample(G_{l+1}), where the "
        "addition assigns equal weight to both terms. Our adaptive gating module replaces this with a learned "
        "weighting: G_l = alpha_l * F_l + (1 - alpha_l) * Upsample(G_{l+1}), where alpha_l is predicted by "
        "a lightweight network conditioned on the global scene descriptor."
    )
    y = add_paragraph(page, MARGIN, y, m2, fontsize=11)

    m3 = (
        "The gating network consists of a global average pooling layer followed by two fully connected layers "
        "with a sigmoid activation. This design adds negligible computational overhead (less than 0.3% of total "
        "FLOPs) while providing meaningful adaptability. During training, we apply a diversity regularization "
        "term that encourages different gating values across pyramid levels to prevent degenerate solutions."
    )
    y = add_paragraph(page, MARGIN, y, m3, fontsize=11)
    y += 10

    # IMAGE 2: Gating module detail
    img2_data = create_colored_image(380, 160, (180, 100, 60))
    img2_rect = pymupdf.Rect(MARGIN + 50, y, W - MARGIN - 50, y + 160)
    page.insert_image(img2_rect, stream=img2_data)
    # NO CAPTION

    y += 175
    m4 = (
        "The global scene descriptor is computed by applying a lightweight encoder (MobileNetV3-Small) to a "
        "downsampled version of the input image. This descriptor captures high-level scene attributes such as "
        "density, lighting conditions, and dominant object categories, enabling the gating module to anticipate "
        "which scales are most informative for the current input."
    )
    y = add_paragraph(page, MARGIN, y, m4, fontsize=11)

    # =========================================================================
    # Page 4: More methodology
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    y = MARGIN + 10
    page.insert_text(pymupdf.Point(MARGIN, y), "3.2  Context-Aware NMS", fontsize=12, fontname="tibo")
    y += 22
    m5 = (
        "Standard non-maximum suppression (NMS) operates independently on each frame, which can lead to "
        "flickering detections in video streams. Our context-aware NMS module maintains a short-term memory "
        "of recent detection boxes and confidence scores. For each candidate detection in the current frame, "
        "we compute a temporal consistency score based on IoU overlap with detections in the previous K frames. "
        "This score is combined with the detection confidence to produce a more stable ranking for suppression."
    )
    y = add_paragraph(page, MARGIN, y, m5, fontsize=11)

    m6 = (
        "Formally, let b_t denote a detection box at time t with confidence c_t. The temporal consistency "
        "score is defined as tau(b_t) = max_{k in 1..K} IoU(b_t, b_{t-k}) * c_{t-k}. The adjusted confidence "
        "is then c'_t = lambda * c_t + (1-lambda) * tau(b_t), where lambda controls the balance between "
        "instantaneous confidence and temporal consistency. We set lambda=0.7 in all experiments."
    )
    y = add_paragraph(page, MARGIN, y, m6, fontsize=11)
    y += 10

    page.insert_text(pymupdf.Point(MARGIN, y), "3.3  Training Procedure", fontsize=12, fontname="tibo")
    y += 22
    m7 = (
        "We train the complete model end-to-end using a multi-task loss combining classification, bounding "
        "box regression, and gating diversity regularization. The backbone is initialized with ImageNet-pretrained "
        "weights, and the entire model is trained for 90 epochs using SGD with momentum 0.9, weight decay 1e-4, "
        "and an initial learning rate of 0.01 with cosine annealing. We use a batch size of 16 distributed across "
        "4 GPUs. Data augmentation includes random horizontal flipping, multi-scale training with scales in "
        "[640, 800, 1024], Mosaic augmentation, and MixUp with ratio sampled from Beta(1.5, 1.5)."
    )
    y = add_paragraph(page, MARGIN, y, m7, fontsize=11)
    y += 10

    # IMAGE 3: Training pipeline
    img3_data = create_colored_image(420, 150, (60, 160, 80))
    img3_rect = pymupdf.Rect(MARGIN + 30, y, W - MARGIN - 30, y + 150)
    page.insert_image(img3_rect, stream=img3_data)
    # NO CAPTION

    # =========================================================================
    # Page 5: Experiments setup
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    y = MARGIN + 10
    page.insert_text(pymupdf.Point(MARGIN, y), "4  Experiments", fontsize=14, fontname="tibo")
    y += 22
    page.insert_text(pymupdf.Point(MARGIN, y), "4.1  Datasets", fontsize=12, fontname="tibo")
    y += 22
    e1 = (
        "We evaluate our approach on three benchmarks: (1) UrbanDet-5K, our newly collected dataset of 5,000 "
        "urban scenes with 87,342 annotated objects across 12 categories; (2) CityScapes (Cordts et al., 2016), "
        "a well-established urban scene understanding benchmark with 5,000 finely annotated images; and (3) "
        "BDD100K (Yu et al., 2020), a large-scale diverse driving dataset. For UrbanDet-5K, we use a 70/15/15 "
        "train/val/test split. For CityScapes and BDD100K, we follow the standard splits."
    )
    y = add_paragraph(page, MARGIN, y, e1, fontsize=11)

    page.insert_text(pymupdf.Point(MARGIN, y + 5), "4.2  Implementation Details", fontsize=12, fontname="tibo")
    y += 28
    e2 = (
        "Our primary backbone is ResNet-101 with deformable convolutions in stages 3-5. We also report results "
        "with ResNet-50 and Swin-T for comparison. The feature pyramid has 5 levels (P3-P7) with 256 channels. "
        "The gating network uses a hidden dimension of 64. Inference is performed at the original image resolution "
        "with a single forward pass (no test-time augmentation). All timing measurements are conducted on a single "
        "NVIDIA RTX 4090 GPU with TensorRT FP16 optimization."
    )
    y = add_paragraph(page, MARGIN, y, e2, fontsize=11)

    page.insert_text(pymupdf.Point(MARGIN, y + 5), "4.3  Main Results", fontsize=12, fontname="tibo")
    y += 28
    e3 = (
        "Table 1 presents the comparison of our method against recent state-of-the-art approaches on UrbanDet-5K. "
        "Our AFPN with ResNet-101 backbone achieves 52.3 mAP, surpassing the previous best (DINO, 49.8 mAP) "
        "by 2.5 points while running at 47.2 FPS compared to DINO's 18.6 FPS. Notably, even with the lighter "
        "ResNet-50 backbone, our method achieves 49.1 mAP at 62.3 FPS, outperforming all methods except DINO "
        "in accuracy while being significantly faster."
    )
    y = add_paragraph(page, MARGIN, y, e3, fontsize=11)
    y += 10

    # IMAGE 4: Comparison bar chart
    img4_data = create_colored_image(400, 170, (150, 70, 150))
    img4_rect = pymupdf.Rect(MARGIN + 40, y, W - MARGIN - 40, y + 170)
    page.insert_image(img4_rect, stream=img4_data)
    # NO CAPTION

    # =========================================================================
    # Page 6: More results and tables
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    y = MARGIN + 10
    e4 = (
        "On the CityScapes validation set, our method achieves 43.8 AP, compared to 41.2 AP for Cascade R-CNN "
        "and 42.7 AP for HTC++. The improvement is most pronounced for the 'person' and 'bicycle' categories, "
        "which are typically small and frequently occluded in urban scenes. On BDD100K, we observe consistent "
        "improvements across all weather and lighting conditions, with the largest gains in nighttime scenes "
        "(+4.1 AP) and rainy conditions (+3.7 AP), validating the adaptability of our gating mechanism."
    )
    y = add_paragraph(page, MARGIN, y, e4, fontsize=11)

    page.insert_text(pymupdf.Point(MARGIN, y + 5), "4.4  Ablation Study", fontsize=12, fontname="tibo")
    y += 28
    e5 = (
        "We conduct extensive ablation studies to validate each component of our approach. Table 2 shows the "
        "contribution of each module on UrbanDet-5K. Starting from the FPN baseline (46.1 mAP), adding the "
        "adaptive gating module improves performance to 50.4 mAP (+4.3). The context-aware NMS provides a "
        "further 0.8 mAP improvement on the video evaluation protocol. The diversity regularization contributes "
        "1.1 mAP, confirming that preventing degenerate gating values is essential for full performance."
    )
    y = add_paragraph(page, MARGIN, y, e5, fontsize=11)

    e6 = (
        "We also study the sensitivity to the number of pyramid levels and the gating network capacity. Using "
        "3 levels (P3-P5) instead of 5 reduces mAP by 1.8 points, primarily affecting large object detection. "
        "Increasing the gating hidden dimension from 64 to 256 provides only marginal improvement (+0.2 mAP) "
        "at a 15% computational overhead, confirming that our lightweight design is near-optimal."
    )
    y = add_paragraph(page, MARGIN, y, e6, fontsize=11)
    y += 10

    # IMAGE 5: Ablation results
    img5_data = create_colored_image(380, 160, (100, 140, 180))
    img5_rect = pymupdf.Rect(MARGIN + 50, y, W - MARGIN - 50, y + 160)
    page.insert_image(img5_rect, stream=img5_data)
    # NO CAPTION

    y += 175
    e7 = (
        "Furthermore, we visualize the learned gating values across different scenes. As shown in the figures "
        "above, the model assigns higher weights to fine-grained features (P3-P4) in dense pedestrian scenes "
        "and shifts attention to coarser features (P5-P7) in highway scenes with large vehicles. This confirms "
        "that the adaptive mechanism learns meaningful scale-selection strategies."
    )
    y = add_paragraph(page, MARGIN, y, e7, fontsize=11)

    # =========================================================================
    # Page 7: Discussion
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    y = MARGIN + 10
    page.insert_text(pymupdf.Point(MARGIN, y), "5  Discussion", fontsize=14, fontname="tibo")
    y += 22
    d1 = (
        "Our results demonstrate that adaptive feature fusion provides significant benefits for urban object "
        "detection, particularly in challenging conditions. The gating mechanism effectively learns to route "
        "information through the feature pyramid based on scene characteristics, reducing the reliance on "
        "fixed fusion strategies that may be suboptimal for diverse inputs."
    )
    y = add_paragraph(page, MARGIN, y, d1, fontsize=11)

    d2 = (
        "One limitation of our approach is the dependence on the global scene descriptor, which requires a "
        "separate lightweight encoder. While the computational overhead is minimal (3.2% of total FLOPs), it "
        "does introduce an additional component that must be trained. Future work could explore conditioning "
        "the gating mechanism directly on intermediate FPN features to eliminate this dependency."
    )
    y = add_paragraph(page, MARGIN, y, d2, fontsize=11)

    d3 = (
        "The context-aware NMS module shows promising results for video-based detection but requires careful "
        "tuning of the temporal window K and balance parameter lambda. We found K=5 and lambda=0.7 to work "
        "well across all benchmarks, but scene-specific tuning could yield further improvements. Additionally, "
        "the temporal memory introduces a small latency that may be undesirable in safety-critical applications."
    )
    y = add_paragraph(page, MARGIN, y, d3, fontsize=11)

    d4 = (
        "We also note that the improvements are most significant for small objects (AP_S improves by 5.2 points) "
        "and partially occluded objects (recall at IoU=0.75 improves by 7.8%). This aligns with our hypothesis "
        "that adaptive scale selection benefits categories where the optimal feature resolution varies "
        "significantly across instances."
    )
    y = add_paragraph(page, MARGIN, y, d4, fontsize=11)
    y += 10

    # IMAGE 6: Qualitative results
    img6_data = create_colored_image(420, 160, (170, 120, 50))
    img6_rect = pymupdf.Rect(MARGIN + 30, y, W - MARGIN - 30, y + 160)
    page.insert_image(img6_rect, stream=img6_data)
    # NO CAPTION

    # =========================================================================
    # Page 8: More discussion / Broader impact
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    y = MARGIN + 10
    page.insert_text(pymupdf.Point(MARGIN, y), "5.1  Broader Impact", fontsize=12, fontname="tibo")
    y += 22
    d5 = (
        "Improved object detection in urban environments has direct applications in autonomous driving, traffic "
        "monitoring, and urban safety systems. Our method's ability to maintain real-time performance while "
        "improving accuracy makes it particularly suitable for deployment on edge devices in smart city "
        "infrastructure. However, we acknowledge the ethical considerations surrounding surveillance technology "
        "and advocate for responsible deployment with appropriate privacy safeguards."
    )
    y = add_paragraph(page, MARGIN, y, d5, fontsize=11)

    d6 = (
        "The UrbanDet-5K dataset was collected from publicly available traffic cameras with all personally "
        "identifiable information (faces, license plates) automatically anonymized using a pre-trained "
        "anonymization pipeline. The dataset will be released under a CC-BY-NC 4.0 license for research "
        "purposes only."
    )
    y = add_paragraph(page, MARGIN, y, d6, fontsize=11)
    y += 10

    page.insert_text(pymupdf.Point(MARGIN, y), "5.2  Computational Efficiency Analysis", fontsize=12, fontname="tibo")
    y += 22
    d7 = (
        "We provide a detailed breakdown of computational costs in Table 3. The adaptive gating module adds only "
        "0.12 GFLOPs to the base FPN (21.4 GFLOPs), representing a 0.56% increase. The scene descriptor encoder "
        "adds 0.68 GFLOPs (3.18%). The context-aware NMS adds negligible FLOPs but requires 2.1 MB of additional "
        "memory for the temporal buffer. Overall, our method achieves a 5.4% mAP improvement with less than 4% "
        "computational overhead, yielding an excellent efficiency-accuracy trade-off."
    )
    y = add_paragraph(page, MARGIN, y, d7, fontsize=11)

    d8 = (
        "When deployed with TensorRT FP16 optimization, the complete pipeline processes a 1280x720 input in "
        "21.2ms (47.2 FPS) on an RTX 4090. This includes image preprocessing (1.3ms), backbone + AFPN inference "
        "(15.4ms), detection head (3.1ms), and NMS (1.4ms). The gating module adds only 0.4ms to the FPN stage, "
        "confirming its lightweight nature."
    )
    y = add_paragraph(page, MARGIN, y, d8, fontsize=11)

    # =========================================================================
    # Page 9: Conclusion
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    y = MARGIN + 10
    page.insert_text(pymupdf.Point(MARGIN, y), "6  Conclusion", fontsize=14, fontname="tibo")
    y += 22
    c1 = (
        "We presented the Adaptive Feature Pyramid Network (AFPN), a novel architecture for real-time object "
        "detection in urban environments. Our adaptive gating mechanism dynamically adjusts feature fusion "
        "weights based on scene complexity, achieving state-of-the-art accuracy on UrbanDet-5K, CityScapes, "
        "and BDD100K while maintaining real-time inference speeds. Combined with our context-aware NMS module, "
        "the proposed method provides stable, high-quality detections suitable for deployment in urban "
        "monitoring systems."
    )
    y = add_paragraph(page, MARGIN, y, c1, fontsize=11)

    c2 = (
        "Future work will explore extending the adaptive gating mechanism to instance segmentation and 3D "
        "object detection tasks. We also plan to investigate knowledge distillation techniques to transfer "
        "the learned gating strategies to even more compact models suitable for mobile and embedded deployment. "
        "The UrbanDet-5K dataset and model checkpoints will be publicly released to facilitate further research."
    )
    y = add_paragraph(page, MARGIN, y, c2, fontsize=11)
    y += 15

    page.insert_text(pymupdf.Point(MARGIN, y), "Acknowledgments", fontsize=12, fontname="tibo")
    y += 20
    c3 = (
        "This work was supported by the National Science Foundation under Grant No. IIS-2345678 and a Google "
        "Research Scholar award. We thank the anonymous reviewers for their constructive feedback and suggestions. "
        "We also acknowledge the Stanford Vision Lab for providing computational resources."
    )
    y = add_paragraph(page, MARGIN, y, c3, fontsize=11)

    # =========================================================================
    # Page 10: References
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    y = MARGIN + 10
    page.insert_text(pymupdf.Point(MARGIN, y), "References", fontsize=14, fontname="tibo")
    y += 25

    refs = [
        "Carion, N., Massa, F., Synnaeve, G., Usunier, N., Kirillov, A., & Zagoruyko, S. (2020). End-to-end object detection with transformers. ECCV.",
        "Chen, L., Rodriguez, A., & Watanabe, T. (2024). Scale-adaptive detection networks for dense urban scenes. CVPR.",
        "Cordts, M., Omran, M., Ramos, S., Rehfeld, T., Enzweiler, M., Benenson, R., ... & Schiele, B. (2016). The cityscapes dataset for semantic urban scene understanding. CVPR.",
        "Ghiasi, G., Lin, T. Y., & Le, Q. V. (2019). NAS-FPN: Learning scalable feature pyramid architecture for object detection. CVPR.",
        "Hu, J., Shen, L., & Sun, G. (2018). Squeeze-and-excitation networks. CVPR.",
        "Lin, T. Y., Dollar, P., Girshick, R., He, K., Hariharan, B., & Belongie, S. (2017). Feature pyramid networks for object detection. CVPR.",
        "Liu, S., Qi, L., Qin, H., Shi, J., & Jia, J. (2018). Path aggregation network for instance segmentation. CVPR.",
        "Nakamura, H. & Okoye, C. (2023). Efficient multi-resolution fusion for pedestrian detection. ICCV.",
        "Tan, M., Pang, R., & Le, Q. V. (2020). EfficientDet: Scalable and efficient object detection. CVPR.",
        "Woo, S., Park, J., Lee, J. Y., & Kweon, I. S. (2018). CBAM: Convolutional block attention module. ECCV.",
        "Yu, F., Chen, H., Wang, X., Xian, W., Chen, Y., Liu, F., ... & Darrell, T. (2020). BDD100K: A diverse driving dataset for heterogeneous multitask learning. CVPR.",
        "Zhang, H., Li, F., Liu, S., Zhang, L., Su, H., Zhu, J., ... & Shum, H. Y. (2022). DINO: DETR with improved denoising anchor boxes for end-to-end object detection. ICLR.",
        "Zhu, X., Su, W., Lu, L., Li, B., Wang, X., & Dai, J. (2021). Deformable DETR: Deformable transformers for end-to-end object detection. ICLR.",
    ]
    for i, ref in enumerate(refs):
        ref_text = f"[{i+1}] {ref}"
        rect = pymupdf.Rect(MARGIN, y, W - MARGIN, y + 50)
        page.insert_textbox(rect, ref_text, fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 45

    # Save the document
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify no figure labels present
    doc = pymupdf.open(OUTPUT)
    all_text = ""
    for pg in doc:
        all_text += pg.get_text("text")
    doc.close()
    assert "Fig." not in all_text, "ERROR: 'Fig.' found in initial PDF - must not contain figure labels!"
    print(f'Verification passed: No figure labels found in initial PDF')
    print(f'Page count: {pymupdf.open(OUTPUT).page_count}')

    # Count total images
    doc = pymupdf.open(OUTPUT)
    total_images = 0
    for pg in doc:
        total_images += len(pg.get_images())
    doc.close()
    print(f'Total images: {total_images}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
