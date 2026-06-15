"""
Initial Setup: Create a 15-page survey paper on machine learning
Task ID: pdf_res_001
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_001'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/survey_ml.pdf'

# Page dimensions (A4)
W, H = 595, 842
MARGIN_LEFT = 72
MARGIN_RIGHT = 523
MARGIN_TOP = 72
MARGIN_BOTTOM = 770
TEXT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT

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

def create_survey_pdf():
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # We need exactly 23 occurrences of "machine learning" across 15 pages.
    # We'll distribute them: some pages have 2-3 mentions, some have 0-1.
    # Track count carefully.

    fontsize_title = 22
    fontsize_heading = 14
    fontsize_body = 10.5
    fontsize_small = 9
    line_height = fontsize_body * 1.45

    ml_count = 0  # track occurrences

    # ---- Page 1: Title page ----
    page = doc.new_page(width=W, height=H)
    # Title
    page.insert_text(pymupdf.Point(W/2 - 180, 200),
        "A Comprehensive Survey of", fontsize=18, fontname="tibo", color=(0,0,0))
    page.insert_text(pymupdf.Point(W/2 - 150, 235),
        "Machine Learning Methods", fontsize=22, fontname="tibo", color=(0,0,0))
    # "machine learning" #1
    ml_count += 1
    page.insert_text(pymupdf.Point(W/2 - 120, 270),
        "in Modern Applications", fontsize=18, fontname="tibo", color=(0,0,0))

    # Authors
    page.insert_text(pymupdf.Point(W/2 - 140, 340),
        "Dr. Sarah Chen, Prof. James Rodriguez, Dr. Anika Patel", fontsize=11, fontname="tiro", color=(0.2,0.2,0.2))
    page.insert_text(pymupdf.Point(W/2 - 100, 365),
        "Department of Computer Science", fontsize=10, fontname="tiro", color=(0.3,0.3,0.3))
    page.insert_text(pymupdf.Point(W/2 - 80, 385),
        "Stanford University", fontsize=10, fontname="tiro", color=(0.3,0.3,0.3))
    page.insert_text(pymupdf.Point(W/2 - 30, 410),
        "2024", fontsize=10, fontname="tiro", color=(0.3,0.3,0.3))

    # Abstract heading
    page.insert_text(pymupdf.Point(MARGIN_LEFT, 480), "Abstract", fontsize=13, fontname="tibo", color=(0,0,0))
    # Draw line under abstract
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_LEFT, 485), pymupdf.Point(MARGIN_RIGHT, 485))
    shape.finish(color=(0,0,0), width=0.5)
    shape.commit()

    abstract_text = (
        "This survey provides a comprehensive overview of machine learning techniques "  # #2
        "that have transformed the landscape of artificial intelligence research over the past decade. "
        "We examine supervised, unsupervised, and reinforcement learning paradigms, analyzing their "
        "theoretical foundations and practical applications across diverse domains including healthcare, "
        "finance, natural language processing, and computer vision. Our analysis covers over 350 papers "
        "published between 2015 and 2024, highlighting key trends in machine learning research "  # #3
        "and identifying open challenges for future investigation."
    )
    ml_count += 2  # #2 and #3

    rect = pymupdf.Rect(MARGIN_LEFT, 500, MARGIN_RIGHT, 650)
    page.insert_textbox(rect, abstract_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Keywords
    page.insert_text(pymupdf.Point(MARGIN_LEFT, 670), "Keywords: ", fontsize=10, fontname="tibo", color=(0,0,0))
    page.insert_text(pymupdf.Point(130, 670),
        "deep learning, neural networks, classification, clustering, reinforcement learning",
        fontsize=10, fontname="tiit", color=(0.3,0.3,0.3))

    # ---- Page 2: Introduction ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "1. Introduction", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    intro_text = (
        "The field of machine learning has experienced unprecedented growth in recent years, "  # #4
        "driven by advances in computational hardware, the availability of large-scale datasets, "
        "and breakthroughs in algorithm design. From early perceptrons to modern transformer "
        "architectures, machine learning has evolved from a niche academic pursuit into a "  # #5
        "cornerstone technology that underpins applications ranging from autonomous vehicles to "
        "personalized medicine.\n\n"
        "This survey aims to provide researchers and practitioners with a structured overview of "
        "the current state of the art. We organize our discussion around three primary learning "
        "paradigms: supervised learning, unsupervised learning, and reinforcement learning. For "
        "each paradigm, we review foundational methods, discuss recent innovations, and highlight "
        "representative applications.\n\n"
        "The rapid expansion of machine learning applications has also raised important questions "  # #6
        "about fairness, interpretability, and robustness. We dedicate a section to these cross-cutting "
        "concerns, examining how the community has responded to calls for more responsible AI development."
    )
    ml_count += 3  # #4, #5, #6

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, intro_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 3: Background ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "2. Background and Historical Context", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    bg_text = (
        "The origins of machine learning can be traced to the seminal work of Alan Turing, "  # #7
        "who proposed the question of whether machines can think in his 1950 paper. The subsequent "
        "decades saw the development of foundational algorithms including decision trees (Quinlan, 1986), "
        "support vector machines (Vapnik, 1995), and neural networks (Rumelhart et al., 1986).\n\n"
        "The resurgence of neural networks in the 2010s, often referred to as the deep learning "
        "revolution, was catalyzed by three key factors: (1) the availability of GPU computing, "
        "(2) large annotated datasets such as ImageNet, and (3) architectural innovations including "
        "convolutional and recurrent neural networks. This period marked a turning point where "
        "machine learning systems began to surpass human-level performance on specific benchmarks "  # #8
        "in image recognition, speech processing, and game playing."
    )
    ml_count += 2  # #7, #8

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, bg_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 4: Supervised Learning ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "3. Supervised Learning", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    sl_text = (
        "Supervised learning remains the most widely deployed machine learning paradigm. "
        "applications. Given a labeled training set of input-output pairs, the goal is to learn a "
        "mapping function that generalizes to unseen data.\n\n"
        "3.1 Classification Methods\n\n"
        "Classification tasks involve predicting discrete class labels. Traditional approaches include "
        "logistic regression, k-nearest neighbors, and support vector machines. Modern deep learning "
        "classifiers, particularly convolutional neural networks (CNNs), have achieved remarkable "
        "accuracy on image classification benchmarks. ResNet (He et al., 2016) and EfficientNet "
        "(Tan & Le, 2019) represent significant milestones in this area.\n\n"
        "3.2 Regression Methods\n\n"
        "Regression tasks predict continuous output values. Linear regression, polynomial regression, "
        "and gradient boosting machines (e.g., XGBoost, LightGBM) remain popular for tabular data. "
        "Neural network-based regression models are increasingly applied to complex prediction tasks "
        "in financial forecasting, drug discovery, and climate modeling."
    )
    # removed one "machine learning" -> "ML" to control count

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, sl_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 5: Unsupervised Learning ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "4. Unsupervised Learning", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    ul_text = (
        "Unsupervised learning algorithms discover patterns in data without labeled examples. "
        "This paradigm is particularly valuable when labeled data is scarce or expensive to obtain, "
        "which is common in many real-world machine learning deployments.\n\n"  # #10
        "4.1 Clustering\n\n"
        "Clustering algorithms group similar data points together. K-means clustering, hierarchical "
        "clustering, and DBSCAN are classical methods. Spectral clustering and deep clustering "
        "approaches leverage representation learning to handle complex data geometries.\n\n"
        "4.2 Dimensionality Reduction\n\n"
        "Techniques such as Principal Component Analysis (PCA), t-SNE, and UMAP enable visualization "
        "and preprocessing of high-dimensional data. Autoencoders provide a neural network-based "
        "approach to learning compact representations."
    )
    ml_count += 1  # #10

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, ul_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 6: Reinforcement Learning ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "5. Reinforcement Learning", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    rl_text = (
        "Reinforcement learning (RL) addresses sequential decision-making problems where an agent "
        "learns to maximize cumulative reward through interaction with an environment. The integration "
        "of deep learning with reinforcement learning, known as deep RL, has produced remarkable "
        "achievements including AlphaGo (Silver et al., 2016) and robotic manipulation systems.\n\n"
        "5.1 Model-Free Methods\n\n"
        "Q-learning and policy gradient methods form the basis of model-free RL. Deep Q-Networks "
        "(DQN) and Proximal Policy Optimization (PPO) are widely used in practice. These methods "
        "have been successfully applied in game playing, recommendation systems, and resource allocation.\n\n"
        "5.2 Model-Based Methods\n\n"
        "Model-based RL algorithms learn a dynamics model of the environment, enabling more sample-efficient "
        "learning. World models and MuZero represent state-of-the-art approaches in this area."
    )
    # No "machine learning" on this page

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, rl_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 7: Deep Learning Architectures ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "6. Deep Learning Architectures", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    dl_text = (
        "Deep neural networks have become the dominant machine learning paradigm, "
        "achieving state-of-the-art results across virtually all application domains.\n\n"
        "6.1 Convolutional Neural Networks\n\n"
        "CNNs exploit spatial structure in data through local receptive fields and weight sharing. "
        "Architectures such as VGG, Inception, and ResNet have progressively improved performance "
        "on image recognition tasks. Recent innovations include attention mechanisms, depthwise "
        "separable convolutions, and neural architecture search.\n\n"
        "6.2 Transformer Models\n\n"
        "The transformer architecture (Vaswani et al., 2017) has revolutionized natural language "
        "processing and is increasingly applied to computer vision and multimodal tasks. BERT, GPT, "
        "and their successors demonstrate that large-scale pre-training followed by fine-tuning "
        "yields powerful machine learning models for diverse downstream tasks."  # #12
    )
    ml_count += 1  # #12 only (removed #11)

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, dl_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 8: Applications in Healthcare ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "7. Applications in Healthcare", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    health_text = (
        "Healthcare represents one of the most promising application domains for machine learning "  # #13
        "technologies. From diagnostic imaging to drug discovery, computational methods are "
        "transforming clinical practice.\n\n"
        "7.1 Medical Imaging\n\n"
        "Deep learning models have achieved radiologist-level performance in detecting conditions "
        "such as diabetic retinopathy, skin cancer, and lung nodules. Transfer learning from ImageNet "
        "pre-trained models has proven particularly effective when medical training data is limited.\n\n"
        "7.2 Drug Discovery\n\n"
        "Machine learning accelerates the drug discovery pipeline by predicting molecular properties, "  # #14
        "identifying drug-target interactions, and optimizing lead compounds. Graph neural networks "
        "and generative models have shown particular promise in molecular design."
    )
    ml_count += 2  # #13, #14

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, health_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 9: Applications in Finance ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "8. Applications in Finance", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    fin_text = (
        "The financial industry has been an early adopter of machine learning techniques "  # #15
        "for tasks ranging from fraud detection to algorithmic trading.\n\n"
        "8.1 Risk Assessment\n\n"
        "Credit scoring models increasingly incorporate machine learning algorithms that can capture "  # #16
        "nonlinear relationships in borrower data. Ensemble methods such as gradient boosting and "
        "random forests have largely replaced traditional logistic regression models in many "
        "financial institutions.\n\n"
        "8.2 Algorithmic Trading\n\n"
        "Quantitative trading strategies leverage time series prediction, sentiment analysis, and "
        "reinforcement learning to make automated investment decisions. However, the non-stationarity "
        "of financial markets poses unique challenges for model robustness and generalization."
    )
    ml_count += 2  # #15, #16

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, fin_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 10: NLP Applications ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "9. Natural Language Processing", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    nlp_text = (
        "Natural language processing has been profoundly transformed by advances in ML, "
        "particularly the introduction of transformer-based language models.\n\n"
        "9.1 Language Models\n\n"
        "Large language models (LLMs) such as GPT-4, PaLM, and LLaMA have demonstrated remarkable "
        "capabilities in text generation, translation, summarization, and question answering. These "
        "models are pre-trained on vast text corpora using self-supervised objectives and can be "
        "adapted to specific tasks through fine-tuning or in-context learning.\n\n"
        "9.2 Sentiment Analysis and Information Extraction\n\n"
        "Traditional NLP tasks like sentiment analysis and named entity recognition have seen "
        "significant accuracy improvements with transformer-based approaches. BERT and its variants "
        "remain strong baselines for many benchmark datasets in these areas."
    )
    # removed one "machine learning" -> "ML" on this page

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, nlp_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 11: Computer Vision ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "10. Computer Vision", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    cv_text = (
        "Computer vision has become one of the most successful application areas for machine learning, "  # #18
        "with deep learning models now exceeding human performance on several visual recognition tasks.\n\n"
        "10.1 Object Detection and Segmentation\n\n"
        "Two-stage detectors (Faster R-CNN) and single-stage detectors (YOLO, SSD) provide different "
        "trade-offs between speed and accuracy. Instance segmentation models such as Mask R-CNN enable "
        "pixel-level object delineation. Vision transformers (ViT) have emerged as competitive "
        "alternatives to CNN-based architectures.\n\n"
        "10.2 Generative Models\n\n"
        "Generative adversarial networks (GANs) and diffusion models have achieved photorealistic "
        "image synthesis. Applications include data augmentation, style transfer, super-resolution, "
        "and content creation for creative industries."
    )
    ml_count += 1  # #18

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, cv_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 12: Ethics and Fairness ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "11. Ethics, Fairness, and Interpretability", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    ethics_text = (
        "As machine learning systems are deployed in increasingly consequential settings, "  # #19
        "concerns about fairness, accountability, and transparency have gained prominence.\n\n"
        "11.1 Algorithmic Fairness\n\n"
        "Bias in training data can lead to discriminatory outcomes in machine learning predictions. "  # #20
        "Fairness-aware algorithms, disparate impact testing, and demographic parity metrics "
        "are being developed to mitigate these issues. Regulatory frameworks such as the EU AI Act "
        "impose requirements for high-risk AI applications.\n\n"
        "11.2 Explainability\n\n"
        "Interpretable models and post-hoc explanation methods (SHAP, LIME, attention visualization) "
        "help stakeholders understand model decisions. The trade-off between model complexity and "
        "interpretability remains an active research area."
    )
    ml_count += 2  # #19, #20

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, ethics_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 13: Challenges ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "12. Open Challenges", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    challenges_text = (
        "Despite remarkable progress, several challenges remain in machine learning "
        "research and deployment.\n\n"
        "12.1 Data Efficiency\n\n"
        "Current deep learning models require large amounts of labeled data. Few-shot learning, "
        "meta-learning, and self-supervised learning are being explored to reduce data requirements.\n\n"
        "12.2 Robustness and Generalization\n\n"
        "Machine learning models often fail when deployed in environments that differ from training "  # #22
        "conditions. Domain adaptation, adversarial robustness, and out-of-distribution detection "
        "are critical areas for improving model reliability.\n\n"
        "12.3 Computational Efficiency\n\n"
        "Training large models demands enormous computational resources with significant environmental "
        "impact. Model compression, knowledge distillation, and efficient architectures aim to "
        "reduce the carbon footprint of AI research."
    )
    ml_count += 1  # #22 only (removed #21)

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, challenges_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 14: Future Directions ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "13. Future Directions", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    future_text = (
        "Looking ahead, several trends are likely to shape the future of machine learning.\n\n"  # #23
        "13.1 Foundation Models\n\n"
        "Large pre-trained models that can be adapted to diverse tasks represent a paradigm shift "
        "in AI. Multi-modal foundation models that integrate vision, language, and other modalities "
        "are expected to enable new applications and improve existing ones.\n\n"
        "13.2 Autonomous Systems\n\n"
        "Self-driving vehicles, robotic manipulation, and autonomous drone navigation will continue "
        "to advance as reinforcement learning and simulation technologies mature. Safety verification "
        "and regulatory compliance remain key challenges.\n\n"
        "13.3 Scientific Discovery\n\n"
        "AI-driven scientific discovery, exemplified by AlphaFold for protein structure prediction, "
        "is opening new frontiers in biology, chemistry, materials science, and physics."
    )
    ml_count += 1  # #23

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(rect, future_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 15: Conclusion and References ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP), "14. Conclusion", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    conclusion_text = (
        "This survey has provided a comprehensive overview of the current landscape of artificial "
        "intelligence research, focusing on supervised, unsupervised, and reinforcement learning "
        "paradigms. We have examined applications across healthcare, finance, natural language "
        "processing, and computer vision, while also addressing critical issues of fairness, "
        "interpretability, and robustness. As the field continues to advance rapidly, interdisciplinary "
        "collaboration and responsible development practices will be essential for realizing the "
        "full potential of these technologies."
    )
    # No "machine learning" in conclusion (already at 23)

    rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 20, MARGIN_RIGHT, 350)
    page.insert_textbox(rect, conclusion_text, fontsize=fontsize_body, fontname="tiro",
                        color=(0,0,0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # References
    page.insert_text(pymupdf.Point(MARGIN_LEFT, 380), "References", fontsize=fontsize_heading, fontname="tibo", color=(0,0,0))

    refs = [
        "[1] He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for image recognition. CVPR.",
        "[2] Vaswani, A., et al. (2017). Attention is all you need. NeurIPS.",
        "[3] Silver, D., et al. (2016). Mastering the game of Go with deep neural networks. Nature.",
        "[4] Devlin, J., et al. (2019). BERT: Pre-training of deep bidirectional transformers. NAACL.",
        "[5] Goodfellow, I., et al. (2014). Generative adversarial nets. NeurIPS.",
        "[6] LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature.",
        "[7] Brown, T., et al. (2020). Language models are few-shot learners. NeurIPS.",
        "[8] Jumper, J., et al. (2021). Highly accurate protein structure prediction with AlphaFold. Nature.",
    ]

    y = 400
    for ref in refs:
        rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + 30)
        page.insert_textbox(rect, ref, fontsize=fontsize_small, fontname="tiro", color=(0,0,0))
        y += 30

    # Add page numbers to all pages
    for i, pg in enumerate(doc):
        pg.insert_text(pymupdf.Point(W/2 - 5, H - 30), str(i + 1),
                       fontsize=9, fontname="tiro", color=(0.5, 0.5, 0.5))

    page_count = doc.page_count
    doc.save(OUTPUT)
    doc.close()

    # Verify count
    verify_doc = pymupdf.open(OUTPUT)
    total_found = 0
    for pg in verify_doc:
        instances = pg.search_for("machine learning")
        total_found += len(instances)
    verify_doc.close()
    print(f"Created {OUTPUT} with {page_count} pages")
    print(f"'machine learning' occurrences found: {total_found} (expected 23)")
    print(f"Tracked count during creation: {ml_count}")

    return total_found

count = create_survey_pdf()

# Open in Evince for the GUI agent
launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
print('GUI_READY: launched Evince with DISPLAY=:0')
