"""
Initial Setup: Create a 16-page computer vision paper PDF with 10 embedded images
Task ID: pdf_res_037
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import io

WORKDIR = '/home/user'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/vision_paper.pdf'

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

def create_sample_image(width, height, color_rgb, label="", img_format="PNG"):
    """Create a simple synthetic image in memory and return bytes."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (width, height), color_rgb)
    draw = ImageDraw.Draw(img)
    # Add some visual structure
    # Draw a border
    draw.rectangle([2, 2, width-3, height-3], outline=(60, 60, 60), width=2)
    # Draw grid lines for chart-like appearance
    for x in range(0, width, width // 5):
        draw.line([(x, 0), (x, height)], fill=(200, 200, 200), width=1)
    for y in range(0, height, height // 5):
        draw.line([(0, y), (width, y)], fill=(200, 200, 200), width=1)
    # Draw some data-like shapes
    import random
    random.seed(hash(label) % 10000)
    for _ in range(8):
        x1 = random.randint(10, width - 40)
        y1 = random.randint(10, height - 40)
        x2 = x1 + random.randint(15, 35)
        y2 = y1 + random.randint(15, 35)
        c = (random.randint(50, 220), random.randint(50, 220), random.randint(50, 220))
        draw.rectangle([x1, y1, x2, y2], fill=c, outline=(40, 40, 40))
    # Add label text
    if label:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        except Exception:
            font = ImageFont.load_default()
        draw.text((10, height - 25), label, fill=(0, 0, 0), font=font)
    buf = io.BytesIO()
    img.save(buf, format=img_format)
    return buf.getvalue()

def create_initial():
    import pymupdf

    os.makedirs(PAPERS_DIR, exist_ok=True)
    # Make sure figures directory does NOT exist
    figures_dir = f'{PAPERS_DIR}/figures'
    if os.path.exists(figures_dir):
        import shutil
        shutil.rmtree(figures_dir)

    doc = pymupdf.open()

    # Define 10 images with metadata for embedding
    image_specs = [
        {"width": 480, "height": 320, "color": (240, 245, 255), "label": "Fig 1: Architecture Overview"},
        {"width": 400, "height": 300, "color": (255, 245, 240), "label": "Fig 2: Feature Pyramid Network"},
        {"width": 500, "height": 280, "color": (240, 255, 240), "label": "Fig 3: Attention Maps"},
        {"width": 420, "height": 350, "color": (255, 255, 235), "label": "Fig 4: Detection Results COCO"},
        {"width": 460, "height": 300, "color": (245, 240, 255), "label": "Fig 5: Precision-Recall Curve"},
        {"width": 380, "height": 280, "color": (255, 240, 245), "label": "Fig 6: Ablation Study"},
        {"width": 500, "height": 340, "color": (235, 255, 255), "label": "Fig 7: Qualitative Comparison"},
        {"width": 440, "height": 310, "color": (255, 250, 235), "label": "Fig 8: Error Analysis"},
        {"width": 470, "height": 290, "color": (240, 255, 250), "label": "Fig 9: Real-world Deployment"},
        {"width": 450, "height": 330, "color": (250, 240, 240), "label": "Fig 10: Failure Cases"},
    ]

    # Pre-generate all image bytes
    image_bytes_list = []
    for spec in image_specs:
        img_bytes = create_sample_image(spec["width"], spec["height"], spec["color"], spec["label"])
        image_bytes_list.append(img_bytes)

    # Page dimensions (A4)
    W, H = 595, 842

    # ---- Page 1: Title Page ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 80), "Adaptive Multi-Scale Vision Transformer for", fontsize=18, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 105), "Real-Time Object Detection in Complex Scenes", fontsize=18, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 145), "Yiming Zhang, Sarah Chen, Marcus Liu, Priya Patel, David Kim", fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 165), "Department of Computer Science, Stanford University", fontsize=10, fontname="heit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 185), "{yzhang, schen, mliu, ppatel, dkim}@cs.stanford.edu", fontsize=9, fontname="cour", color=(0.3, 0.3, 0.3))

    # Abstract
    page.insert_text(pymupdf.Point(72, 230), "Abstract", fontsize=14, fontname="hebo", color=(0, 0, 0))
    abstract_rect = pymupdf.Rect(72, 250, 523, 420)
    page.insert_textbox(abstract_rect,
        "We present AMViT (Adaptive Multi-Scale Vision Transformer), a novel architecture for real-time object "
        "detection that dynamically adjusts its computational budget based on scene complexity. Our approach "
        "leverages a hierarchical attention mechanism that selectively processes image regions at multiple "
        "resolutions, achieving state-of-the-art accuracy on COCO and PASCAL VOC benchmarks while maintaining "
        "real-time inference speeds exceeding 45 FPS on standard hardware. Through extensive ablation studies, "
        "we demonstrate that our adaptive scaling strategy reduces computational cost by 38% compared to "
        "fixed-resolution approaches without sacrificing detection quality. We further validate our method on "
        "autonomous driving and surveillance scenarios, showing robust performance under challenging conditions "
        "including occlusion, varying illumination, and dense object distributions.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 435), "Keywords:", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(140, 435), "object detection, vision transformer, multi-scale, real-time, attention mechanism", fontsize=10, fontname="heit", color=(0.2, 0.2, 0.2))

    # ---- Page 2: Introduction ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "1  Introduction", fontsize=14, fontname="hebo", color=(0, 0, 0))
    intro_rect = pymupdf.Rect(72, 80, 523, 340)
    page.insert_textbox(intro_rect,
        "Object detection remains a fundamental challenge in computer vision, serving as a critical component "
        "in applications ranging from autonomous navigation to medical imaging analysis. While recent transformer-based "
        "architectures have demonstrated remarkable accuracy improvements, their computational demands often "
        "preclude deployment in latency-sensitive applications.\n\n"
        "The core tension between detection accuracy and computational efficiency has motivated numerous "
        "architectural innovations. Feature Pyramid Networks (FPN) introduced multi-scale feature extraction "
        "to handle objects of varying sizes. DETR pioneered the use of transformers for end-to-end detection, "
        "eliminating the need for hand-crafted components like non-maximum suppression. More recently, "
        "Swin Transformer demonstrated that hierarchical vision transformers could achieve competitive "
        "performance across diverse vision tasks.\n\n"
        "However, existing approaches process all image regions with uniform computational effort, regardless "
        "of scene complexity. In practice, many real-world scenes contain large homogeneous regions (sky, road "
        "surfaces) alongside cluttered areas with multiple overlapping objects. This observation motivates our "
        "key insight: adaptively allocating computation based on local complexity can dramatically reduce "
        "overall cost without sacrificing detection quality in challenging regions.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Figure 1 on page 2
    page.insert_text(pymupdf.Point(72, 360), "Figure 1: Overall architecture of the proposed AMViT framework.", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_rect = pymupdf.Rect(72, 375, 523, 590)
    page.insert_image(img_rect, stream=image_bytes_list[0])

    more_text_rect = pymupdf.Rect(72, 610, 523, 780)
    page.insert_textbox(more_text_rect,
        "In this paper, we propose AMViT, an adaptive multi-scale vision transformer that dynamically "
        "adjusts its processing resolution for different image regions. As illustrated in Figure 1, our "
        "architecture consists of three main components: (1) a lightweight complexity estimator that quickly "
        "classifies image patches into complexity levels, (2) a multi-resolution processing backbone that "
        "applies different transformer depths to each complexity level, and (3) a unified detection head "
        "that aggregates multi-scale features for final predictions.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 3: Related Work ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "2  Related Work", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 85), "2.1  CNN-based Object Detection", fontsize=12, fontname="hebo", color=(0, 0, 0))
    rw_rect = pymupdf.Rect(72, 105, 523, 320)
    page.insert_textbox(rw_rect,
        "The evolution of CNN-based detectors has progressed through several paradigm shifts. Two-stage "
        "detectors like Faster R-CNN [35] first generate region proposals, then classify and refine them. "
        "Single-stage detectors including YOLO [33] and SSD [27] directly predict bounding boxes from feature "
        "maps, trading some accuracy for significantly faster inference. RetinaNet [26] addressed the foreground-"
        "background class imbalance with focal loss, narrowing the gap between single and two-stage approaches.\n\n"
        "Feature Pyramid Networks [25] introduced a top-down pathway with lateral connections for multi-scale "
        "feature extraction, becoming a standard component in modern detectors. PANet [28] further enhanced "
        "this with bottom-up path augmentation, while NAS-FPN [11] used neural architecture search to discover "
        "optimal feature pyramid configurations.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 335), "2.2  Vision Transformers", fontsize=12, fontname="hebo", color=(0, 0, 0))
    vt_rect = pymupdf.Rect(72, 355, 523, 530)
    page.insert_textbox(vt_rect,
        "Vision Transformer (ViT) [8] demonstrated that pure transformer architectures could achieve "
        "competitive image classification results when trained on large datasets. DeiT [40] introduced "
        "data-efficient training strategies, making ViT practical with standard ImageNet training. Swin "
        "Transformer [29] proposed shifted window attention for efficient hierarchical representation "
        "learning, achieving state-of-the-art results across multiple vision benchmarks.\n\n"
        "For object detection specifically, DETR [3] pioneered transformer-based detection with a set "
        "prediction approach using bipartite matching. Deformable DETR [47] improved convergence speed "
        "through deformable attention modules. DAB-DETR [22] and DN-DETR [21] further enhanced query "
        "formulation strategies for faster and more stable training.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Figure 2 on page 3
    page.insert_text(pymupdf.Point(72, 550), "Figure 2: Comparison of Feature Pyramid Network variants.", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_rect = pymupdf.Rect(100, 565, 490, 780)
    page.insert_image(img_rect, stream=image_bytes_list[1])

    # ---- Page 4: Related Work continued ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "2.3  Adaptive Computation", fontsize=12, fontname="hebo", color=(0, 0, 0))
    ac_rect = pymupdf.Rect(72, 80, 523, 300)
    page.insert_textbox(ac_rect,
        "Adaptive computation has been explored in various forms. Early exit networks [38] allow samples to "
        "be classified at intermediate layers based on confidence. Token pruning methods [34, 43] reduce the "
        "number of tokens processed by later transformer layers. Dynamic networks [12] adjust architecture "
        "depth or width based on input complexity.\n\n"
        "In the context of object detection, several works have explored spatial adaptivity. QueryDet [44] "
        "uses sparse queries for small object detection. Dynamic Head [6] adapts attention across scales, "
        "spatial locations, and output channels. However, none of these approaches combine multi-scale "
        "processing with input-adaptive resolution selection as we propose.\n\n"
        "Our work differs from prior adaptive methods in two key respects: (1) we operate at the patch level "
        "rather than the token level, preserving spatial structure critical for detection, and (2) our "
        "complexity estimator operates with negligible overhead, enabling true real-time adaptation.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 5: Method ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "3  Method", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 85), "3.1  Complexity-Aware Patch Embedding", fontsize=12, fontname="hebo", color=(0, 0, 0))
    method_rect = pymupdf.Rect(72, 105, 523, 310)
    page.insert_textbox(method_rect,
        "Given an input image I of resolution H x W, we first divide it into non-overlapping patches of size "
        "P x P. For each patch p_i, our lightweight complexity estimator C(.) computes a complexity score "
        "s_i = C(p_i), where s_i is in [0, 1]. This estimator consists of a single convolutional layer followed "
        "by global average pooling and a sigmoid activation, adding less than 0.1 GFLOP to the total computation.\n\n"
        "Based on the complexity scores, patches are sorted into three processing tiers:\n"
        "- Low complexity (s_i < 0.3): Processed at 1/4 resolution with 2 transformer blocks\n"
        "- Medium complexity (0.3 <= s_i < 0.7): Processed at 1/2 resolution with 4 transformer blocks\n"
        "- High complexity (s_i >= 0.7): Processed at full resolution with 6 transformer blocks\n\n"
        "This tiered approach ensures that computational resources are concentrated on the most informative "
        "regions while maintaining sufficient coverage of simpler areas.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Figure 3 on page 5
    page.insert_text(pymupdf.Point(72, 330), "Figure 3: Visualization of attention maps at different complexity tiers.", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_rect = pymupdf.Rect(72, 345, 523, 565)
    page.insert_image(img_rect, stream=image_bytes_list[2])

    method2_rect = pymupdf.Rect(72, 585, 523, 780)
    page.insert_textbox(method2_rect,
        "3.2  Hierarchical Multi-Resolution Backbone\n\n"
        "Our backbone architecture processes the three patch tiers in parallel through dedicated transformer "
        "branches. Each branch consists of a sequence of multi-head self-attention layers with residual "
        "connections and layer normalization. The key innovation is the cross-tier attention mechanism that "
        "allows information flow between resolution levels through lightweight bridge connections.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 6: Method continued ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "3.3  Adaptive Feature Aggregation", fontsize=12, fontname="hebo", color=(0, 0, 0))
    agg_rect = pymupdf.Rect(72, 80, 523, 280)
    page.insert_textbox(agg_rect,
        "After processing through the multi-resolution backbone, features from all three tiers are unified "
        "through our adaptive feature aggregation module. This module employs deformable cross-attention to "
        "align features across different spatial resolutions before concatenation.\n\n"
        "Let F_l, F_m, F_h denote the feature maps from low, medium, and high complexity tiers respectively. "
        "The aggregated feature F_agg is computed as:\n\n"
        "F_agg = W_l * Upsample(F_l) + W_m * Upsample(F_m) + W_h * F_h\n\n"
        "where W_l, W_m, W_h are learnable attention weights that are conditioned on the input image "
        "through a global average pooling and MLP pathway. This allows the network to dynamically "
        "adjust the contribution of each resolution level based on scene characteristics.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 300), "3.4  Detection Head", fontsize=12, fontname="hebo", color=(0, 0, 0))
    head_rect = pymupdf.Rect(72, 320, 523, 500)
    page.insert_textbox(head_rect,
        "The detection head follows the standard anchor-free design with separate classification and "
        "regression branches. Each branch consists of four 3x3 convolutional layers with group normalization "
        "and ReLU activation. The classification branch outputs C channel predictions per spatial location, "
        "while the regression branch predicts 4D bounding box offsets.\n\n"
        "We additionally incorporate a centerness branch that helps suppress low-quality detections far "
        "from object centers, similar to FCOS [39]. The final loss is a weighted combination of focal "
        "classification loss, GIoU regression loss, and centerness BCE loss.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 7: Experiments Setup ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "4  Experiments", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 85), "4.1  Experimental Setup", fontsize=12, fontname="hebo", color=(0, 0, 0))
    setup_rect = pymupdf.Rect(72, 105, 523, 330)
    page.insert_textbox(setup_rect,
        "Datasets. We evaluate our method on three benchmarks: (1) COCO 2017 [24] with 118K training images "
        "and 5K validation images across 80 categories, (2) PASCAL VOC 2012 [10] with 11,540 training images "
        "across 20 categories, and (3) a proprietary autonomous driving dataset consisting of 45K images "
        "captured across diverse urban environments.\n\n"
        "Implementation Details. Our models are implemented in PyTorch and trained on 8 NVIDIA A100 GPUs "
        "with a total batch size of 64. We use the AdamW optimizer with an initial learning rate of 1e-4 "
        "and a cosine learning rate schedule over 36 epochs. Standard data augmentation includes random "
        "horizontal flipping, multi-scale training (resolution range 480-800), and Mosaic augmentation.\n\n"
        "Baselines. We compare against Faster R-CNN [35], RetinaNet [26], DETR [3], Deformable DETR [47], "
        "DINO [46], Swin-T [29], and RT-DETR [31]. All baselines use ResNet-50 or equivalent backbones "
        "for fair comparison.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Figure 4 on page 7
    page.insert_text(pymupdf.Point(72, 350), "Figure 4: Detection results on COCO validation set.", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_rect = pymupdf.Rect(90, 365, 505, 600)
    page.insert_image(img_rect, stream=image_bytes_list[3])

    results_text = pymupdf.Rect(72, 620, 523, 780)
    page.insert_textbox(results_text,
        "Figure 4 shows qualitative detection results on challenging COCO validation images. Our AMViT "
        "correctly detects small and occluded objects that baseline methods miss, while maintaining accurate "
        "bounding box regression for large objects.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 8: Main Results ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "4.2  Main Results on COCO", fontsize=12, fontname="hebo", color=(0, 0, 0))
    main_rect = pymupdf.Rect(72, 80, 523, 230)
    page.insert_textbox(main_rect,
        "Table 1 presents the main results on the COCO 2017 validation set. Our AMViT-Base achieves 49.3 AP "
        "at 47 FPS, outperforming all baselines in the real-time regime. Compared to RT-DETR-R50, we improve "
        "by 2.1 AP while running 8% faster. Against DINO-Swin-T, we achieve comparable accuracy (49.3 vs 49.0) "
        "while being 3.2x faster.\n\n"
        "The AMViT-Large variant pushes accuracy to 52.7 AP while still maintaining 31 FPS, suitable for "
        "many practical applications. The Small variant achieves 45.8 AP at 68 FPS, making it ideal for "
        "edge deployment scenarios.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Figure 5 on page 8
    page.insert_text(pymupdf.Point(72, 250), "Figure 5: Precision-Recall curves across object categories.", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_rect = pymupdf.Rect(80, 265, 515, 510)
    page.insert_image(img_rect, stream=image_bytes_list[4])

    more_rect = pymupdf.Rect(72, 530, 523, 780)
    page.insert_textbox(more_rect,
        "Figure 5 shows precision-recall curves for selected object categories. Our method demonstrates "
        "consistently high precision across recall levels, particularly excelling on small and medium-sized "
        "objects where the adaptive resolution mechanism provides the greatest benefit. The improvement is "
        "most pronounced for categories like 'bicycle', 'traffic light', and 'stop sign' where multi-scale "
        "representation is crucial.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 9: Ablation ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "4.3  Ablation Studies", fontsize=12, fontname="hebo", color=(0, 0, 0))
    abl_rect = pymupdf.Rect(72, 80, 523, 280)
    page.insert_textbox(abl_rect,
        "We conduct extensive ablation studies to validate each component of our approach. All experiments "
        "use AMViT-Base on COCO 2017 val unless otherwise noted.\n\n"
        "Effect of Complexity Tiers. We compare our three-tier complexity scheme against uniform processing "
        "and two-tier alternatives. The three-tier scheme achieves the best accuracy-speed trade-off, with "
        "two-tier being 1.2 AP lower and uniform processing being 2.8 AP lower at the same FPS target.\n\n"
        "Cross-Tier Attention. Removing cross-tier attention connections reduces AP by 1.5 points, confirming "
        "that information exchange between resolution levels is critical. Using simple concatenation instead "
        "of deformable cross-attention results in a 0.8 AP drop.\n\n"
        "Complexity Estimator Design. We compare our lightweight convolutional estimator against gradient-based "
        "complexity measures and learned token scoring. Our approach provides the best trade-off between "
        "estimation accuracy and computational overhead.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Figure 6 on page 9
    page.insert_text(pymupdf.Point(72, 300), "Figure 6: Ablation study results comparing component contributions.", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_rect = pymupdf.Rect(100, 315, 495, 560)
    page.insert_image(img_rect, stream=image_bytes_list[5])

    abl2_rect = pymupdf.Rect(72, 580, 523, 780)
    page.insert_textbox(abl2_rect,
        "Figure 6 visualizes the contribution of each component to the final performance. The adaptive "
        "complexity estimator and cross-tier attention provide the largest individual gains, while the "
        "combination of all components yields a synergistic improvement that exceeds the sum of individual "
        "contributions by approximately 0.7 AP.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 10: More Ablation ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "4.4  Qualitative Analysis", fontsize=12, fontname="hebo", color=(0, 0, 0))
    qual_rect = pymupdf.Rect(72, 80, 523, 240)
    page.insert_textbox(qual_rect,
        "To gain deeper insight into our model's behavior, we visualize the complexity maps and detection "
        "outputs for representative scenes from the COCO validation set. Figure 7 presents side-by-side "
        "comparisons between our AMViT and the strongest baseline (DINO-Swin-T) on challenging scenarios "
        "including crowded pedestrian scenes, dense traffic, and small object detection.\n\n"
        "Our model consistently assigns high complexity scores to regions containing small or overlapping "
        "objects, while efficiently processing background regions at reduced resolution. This behavior "
        "emerges naturally from training without explicit supervision of the complexity estimator.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Figure 7 on page 10
    page.insert_text(pymupdf.Point(72, 260), "Figure 7: Qualitative comparison between AMViT and DINO-Swin-T.", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_rect = pymupdf.Rect(72, 275, 523, 550)
    page.insert_image(img_rect, stream=image_bytes_list[6])

    qual2_rect = pymupdf.Rect(72, 570, 523, 780)
    page.insert_textbox(qual2_rect,
        "The qualitative comparison reveals several notable patterns. In crowded scenes (top row), AMViT "
        "detects 15% more instances than DINO-Swin-T while maintaining high precision. In scenes with "
        "scale variation (middle row), our adaptive processing correctly handles both distant pedestrians "
        "and nearby vehicles. The failure mode analysis (bottom row) shows that remaining errors primarily "
        "occur with heavily occluded objects at extreme scales.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 11: Error Analysis ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "4.5  Error Analysis", fontsize=12, fontname="hebo", color=(0, 0, 0))
    error_rect = pymupdf.Rect(72, 80, 523, 240)
    page.insert_textbox(error_rect,
        "We perform a detailed error analysis following the TIDE framework [2] to understand the remaining "
        "failure modes of our approach. Figure 8 breaks down detection errors by category: classification "
        "errors account for 32% of total errors, localization errors for 28%, missed detections for 24%, "
        "and duplicate detections for 16%.\n\n"
        "Compared to baseline methods, AMViT significantly reduces missed detection errors (-40%) and "
        "localization errors (-22%), primarily due to the multi-resolution processing. Classification errors "
        "show a modest reduction (-8%), suggesting that category confusion remains a challenge that is "
        "largely orthogonal to spatial resolution.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Figure 8 on page 11
    page.insert_text(pymupdf.Point(72, 260), "Figure 8: Error analysis breakdown following the TIDE framework.", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_rect = pymupdf.Rect(80, 275, 515, 550)
    page.insert_image(img_rect, stream=image_bytes_list[7])

    # ---- Page 12: Deployment ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "5  Real-World Deployment", fontsize=14, fontname="hebo", color=(0, 0, 0))
    deploy_rect = pymupdf.Rect(72, 85, 523, 300)
    page.insert_textbox(deploy_rect,
        "To validate the practical applicability of AMViT, we deploy our model in two real-world scenarios: "
        "autonomous driving perception and retail store analytics.\n\n"
        "Autonomous Driving. We integrate AMViT into a modular self-driving stack and evaluate on the "
        "nuScenes validation set. Our model achieves 58.2 NDS (nuScenes Detection Score) while running at "
        "42 FPS on a single NVIDIA Jetson Orin, meeting the real-time requirements for L4 autonomous "
        "driving. The adaptive complexity allocation is particularly beneficial in highway scenarios where "
        "large portions of the field of view contain road surface and sky.\n\n"
        "Retail Analytics. In a pilot deployment across 12 retail locations, AMViT tracks customer "
        "movements and product interactions with 94.3% accuracy. The system processes 8 camera feeds "
        "simultaneously on a single GPU workstation, demonstrating the efficiency of our approach.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Figure 9 on page 12
    page.insert_text(pymupdf.Point(72, 320), "Figure 9: Real-world deployment results in autonomous driving.", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_rect = pymupdf.Rect(72, 335, 523, 575)
    page.insert_image(img_rect, stream=image_bytes_list[8])

    deploy2_rect = pymupdf.Rect(72, 595, 523, 780)
    page.insert_textbox(deploy2_rect,
        "Figure 9 illustrates the deployment pipeline and representative detection results from our "
        "autonomous driving evaluation. The complexity maps (center column) clearly show that the model "
        "allocates more computation to regions containing vehicles, pedestrians, and traffic infrastructure "
        "while processing empty road and sky regions at minimal resolution.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 13: Failure Cases ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "5.1  Limitations and Failure Cases", fontsize=12, fontname="hebo", color=(0, 0, 0))
    fail_rect = pymupdf.Rect(72, 80, 523, 260)
    page.insert_textbox(fail_rect,
        "Despite strong overall performance, our approach has several limitations. First, the complexity "
        "estimator can occasionally misclassify regions, particularly when objects have low contrast against "
        "the background. Second, the three-tier quantization of complexity scores introduces discontinuities "
        "at tier boundaries. Third, our current implementation does not support temporal information, which "
        "could further improve efficiency in video scenarios.\n\n"
        "Figure 10 shows representative failure cases. In highly cluttered scenes with extreme occlusion (a), "
        "the model misses severely occluded instances. Under unusual lighting conditions (b), the complexity "
        "estimator assigns incorrect scores. With very small objects at image boundaries (c), the patch-level "
        "processing can miss objects that span patch boundaries.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Figure 10 on page 13
    page.insert_text(pymupdf.Point(72, 280), "Figure 10: Representative failure cases and analysis.", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    img_rect = pymupdf.Rect(80, 295, 515, 570)
    page.insert_image(img_rect, stream=image_bytes_list[9])

    # ---- Page 14: Discussion ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "6  Discussion", fontsize=14, fontname="hebo", color=(0, 0, 0))
    disc_rect = pymupdf.Rect(72, 85, 523, 420)
    page.insert_textbox(disc_rect,
        "Our results demonstrate that adaptive computation is a powerful paradigm for efficient object "
        "detection. The success of AMViT can be attributed to several factors:\n\n"
        "Computational Efficiency. By allocating computation proportional to scene complexity, AMViT "
        "achieves a 38% reduction in average FLOPs compared to fixed-resolution processing. This "
        "efficiency gain is most pronounced in scenes with significant background content, which "
        "represents the majority of real-world applications.\n\n"
        "Multi-Scale Representation. The parallel processing of patches at different resolutions "
        "naturally captures multi-scale information without the overhead of traditional FPN structures. "
        "The cross-tier attention mechanism ensures that context information flows between scale levels.\n\n"
        "Training Stability. Unlike some adaptive methods that require careful curriculum learning or "
        "specialized training schedules, AMViT converges reliably with standard training procedures. "
        "The complexity estimator learns meaningful representations within the first 5 epochs, after "
        "which its predictions remain largely stable.\n\n"
        "One intriguing direction for future work is extending the adaptive paradigm to video detection, "
        "where temporal redundancy could provide even greater efficiency gains. Additionally, combining "
        "our spatial adaptivity with token pruning methods could yield further computational savings.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 15: Conclusion ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "7  Conclusion", fontsize=14, fontname="hebo", color=(0, 0, 0))
    conc_rect = pymupdf.Rect(72, 85, 523, 280)
    page.insert_textbox(conc_rect,
        "We have presented AMViT, an adaptive multi-scale vision transformer for real-time object detection. "
        "Our approach introduces a lightweight complexity estimator that dynamically routes image patches to "
        "appropriate resolution levels, enabling efficient multi-scale processing without the computational "
        "overhead of traditional architectures.\n\n"
        "Extensive experiments on COCO, PASCAL VOC, and autonomous driving benchmarks demonstrate that AMViT "
        "achieves state-of-the-art accuracy-speed trade-offs, outperforming existing methods by 2+ AP while "
        "maintaining real-time inference speeds. Our ablation studies confirm the importance of each component, "
        "and real-world deployment results validate the practical applicability of our approach.\n\n"
        "We believe that adaptive computation represents a promising direction for efficient vision systems "
        "and hope that AMViT inspires further research in this area.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 310), "Acknowledgments", fontsize=12, fontname="hebo", color=(0, 0, 0))
    ack_rect = pymupdf.Rect(72, 330, 523, 420)
    page.insert_textbox(ack_rect,
        "This research was supported by NSF grants IIS-2247357 and CNS-2312456, and a Google Research "
        "Award. We thank the Stanford Vision Lab for providing compute resources and the anonymous reviewers "
        "for their constructive feedback.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 16: References ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 60), "References", fontsize=14, fontname="hebo", color=(0, 0, 0))
    refs = [
        "[1] Beal, J., et al. Toward transformer-based object detection. arXiv:2012.09958, 2020.",
        "[2] Bolya, D., et al. TIDE: A general toolbox for identifying object detection errors. ECCV, 2020.",
        "[3] Carion, N., et al. End-to-end object detection with transformers. ECCV, 2020.",
        "[4] Chen, K., et al. MMDetection: Open mmlab detection toolbox and benchmark. arXiv:1906.07155, 2019.",
        "[5] Chen, Q., et al. Group DETR: Fast training convergence with decoupled one-to-many supervision. ICCV, 2023.",
        "[6] Dai, X., et al. Dynamic head: Unifying object detection heads with attention. CVPR, 2021.",
        "[7] Deng, J., et al. ImageNet: A large-scale hierarchical image database. CVPR, 2009.",
        "[8] Dosovitskiy, A., et al. An image is worth 16x16 words: Transformers for image recognition. ICLR, 2021.",
        "[9] Everingham, M., et al. The PASCAL visual object classes challenge: A retrospective. IJCV, 2015.",
        "[10] Everingham, M., et al. The Pascal visual object classes (VOC) challenge. IJCV, 88(2):303-338, 2010.",
        "[11] Ghiasi, G., et al. NAS-FPN: Learning scalable feature pyramid architecture. CVPR, 2019.",
        "[12] Han, Y., et al. Dynamic neural networks: A survey. TPAMI, 44(11):7436-7456, 2022.",
        "[13] He, K., et al. Deep residual learning for image recognition. CVPR, 2016.",
        "[14] He, K., et al. Mask R-CNN. ICCV, 2017.",
        "[15] Hu, J., et al. Squeeze-and-excitation networks. CVPR, 2018.",
        "[16] Huang, G., et al. Multi-scale dense networks for resource efficient image classification. ICLR, 2018.",
        "[17] Jocher, G., et al. ultralytics/yolov5: v7.0. Zenodo, 2022.",
        "[18] Li, F., et al. DN-DETR: Accelerate DETR training by introducing query denoising. CVPR, 2022.",
        "[19] Li, Y., et al. MViTv2: Improved multiscale vision transformers. CVPR, 2022.",
        "[20] Lin, T.-Y., et al. Microsoft COCO: Common objects in context. ECCV, 2014.",
        "[21] Liu, S., et al. DAB-DETR: Dynamic anchor boxes are better queries for DETR. ICLR, 2022.",
        "[22] Liu, Z., et al. Swin Transformer: Hierarchical vision transformer using shifted windows. ICCV, 2021.",
        "[23] Lv, W., et al. RT-DETR: DETRs beat YOLOs on real-time object detection. CVPR, 2024.",
    ]
    y = 85
    for ref in refs:
        if y > 770:
            break
        page.insert_text(pymupdf.Point(72, y), ref, fontsize=8, fontname="helv", color=(0, 0, 0))
        y += 14

    # Set metadata
    doc.set_metadata({
        "title": "Adaptive Multi-Scale Vision Transformer for Real-Time Object Detection",
        "author": "Yiming Zhang, Sarah Chen, Marcus Liu, Priya Patel, David Kim",
        "subject": "Computer Vision, Object Detection",
        "keywords": "object detection, vision transformer, multi-scale, real-time, attention",
        "creator": "LaTeX with hyperref",
        "producer": "pdfTeX-1.40.25",
    })

    # Set TOC
    toc = [
        [1, "Abstract", 1],
        [1, "1 Introduction", 2],
        [1, "2 Related Work", 3],
        [2, "2.1 CNN-based Object Detection", 3],
        [2, "2.2 Vision Transformers", 3],
        [2, "2.3 Adaptive Computation", 4],
        [1, "3 Method", 5],
        [2, "3.1 Complexity-Aware Patch Embedding", 5],
        [2, "3.2 Hierarchical Multi-Resolution Backbone", 5],
        [2, "3.3 Adaptive Feature Aggregation", 6],
        [2, "3.4 Detection Head", 6],
        [1, "4 Experiments", 7],
        [2, "4.1 Experimental Setup", 7],
        [2, "4.2 Main Results on COCO", 8],
        [2, "4.3 Ablation Studies", 9],
        [2, "4.4 Qualitative Analysis", 10],
        [2, "4.5 Error Analysis", 11],
        [1, "5 Real-World Deployment", 12],
        [2, "5.1 Limitations and Failure Cases", 13],
        [1, "6 Discussion", 14],
        [1, "7 Conclusion", 15],
        [1, "References", 16],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 16')

    # Verify images
    doc = pymupdf.open(OUTPUT)
    total_images = 0
    for p in doc:
        total_images += len(p.get_images())
    doc.close()
    print(f'Total embedded images: {total_images}')

    # Make sure figures directory does NOT exist
    figures_dir = f'{PAPERS_DIR}/figures'
    if os.path.exists(figures_dir):
        import shutil
        shutil.rmtree(figures_dir)
    print(f'figures/ directory does not exist (as expected)')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
