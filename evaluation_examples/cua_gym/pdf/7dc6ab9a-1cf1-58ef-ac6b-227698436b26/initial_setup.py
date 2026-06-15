"""
Initial Setup: Create a 25-page textbook chapter PDF with bold terms throughout.
Task ID: pdf_res_064
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_064'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/textbook_chapter.pdf'

# Page layout constants
PAGE_W, PAGE_H = 595, 842  # A4
MARGIN_LEFT = 72
MARGIN_RIGHT = 523
MARGIN_TOP = 72
MARGIN_BOTTOM = 770
LINE_HEIGHT = 14
BOLD_FONT = "hebo"
NORMAL_FONT = "helv"
TITLE_SIZE = 22
HEADING_SIZE = 16
SUBHEADING_SIZE = 13
BODY_SIZE = 11

# ---------- Textbook content with bold terms marked as **term** ----------

CHAPTER_TITLE = "Chapter 7: Foundations of Machine Learning"

# Each section: (heading, list_of_paragraphs)
# Bold terms are wrapped in ** **
SECTIONS = [
    ("7.1 Introduction to Machine Learning", [
        "**Machine learning** is a subfield of **artificial intelligence** that focuses on building systems capable of learning from data. Unlike traditional programming where rules are explicitly coded, machine learning algorithms identify patterns in datasets and use these patterns to make predictions or decisions. The field has experienced remarkable growth over the past two decades, driven by increases in computational power and the availability of large-scale datasets.",
        "The core idea behind machine learning is that computers can learn to perform tasks without being explicitly programmed for each specific scenario. This is achieved through **training**, a process where an algorithm is exposed to examples and adjusts its internal parameters to minimize prediction errors. The quality and quantity of **training data** directly influence the performance of the resulting model.",
        "There are three primary paradigms in machine learning: **supervised learning**, **unsupervised learning**, and **reinforcement learning**. Each paradigm addresses different types of problems and requires different approaches to data preparation and model evaluation. Understanding these paradigms is essential for selecting the appropriate technique for a given problem.",
    ]),
    ("7.2 Supervised Learning", [
        "In **supervised learning**, the algorithm is trained on a labeled dataset where each example consists of an input and the corresponding desired output. The goal is to learn a mapping function from inputs to outputs that generalizes well to unseen data. Common supervised learning tasks include **classification** and **regression**.",
        "**Classification** involves predicting a discrete label for a given input. For example, an email **spam filter** classifies incoming messages as either spam or not spam. The algorithm learns decision boundaries in the **feature space** that separate different classes. Popular classification algorithms include **logistic regression**, **decision trees**, **random forests**, and **support vector machines**.",
        "**Regression** tasks involve predicting a continuous numerical value. For instance, predicting house prices based on features such as square footage, number of bedrooms, and location is a regression problem. **Linear regression** is the simplest regression technique, modeling the relationship between variables as a straight line. More complex approaches include **polynomial regression** and **gradient boosting** methods.",
        "The performance of supervised learning models is evaluated using metrics specific to the task. For classification, common metrics include **accuracy**, **precision**, **recall**, and the **F1 score**. For regression, metrics such as **mean squared error** (MSE) and **R-squared** are typically used. Proper evaluation requires splitting data into **training sets** and **test sets** to assess generalization.",
    ]),
    ("7.3 Unsupervised Learning", [
        "**Unsupervised learning** deals with data that has no labeled responses. The objective is to discover hidden patterns or intrinsic structures within the data. This paradigm is particularly valuable for **exploratory data analysis** and situations where labeled data is scarce or expensive to obtain.",
        "**Clustering** is one of the most common unsupervised learning techniques. It involves grouping similar data points together based on some measure of similarity. The **k-means** algorithm partitions data into k clusters by minimizing the distance between points and their assigned **cluster centroids**. Other clustering methods include **hierarchical clustering** and **DBSCAN**, each with different assumptions about cluster shapes and density.",
        "**Dimensionality reduction** is another key unsupervised technique that reduces the number of features in a dataset while preserving important information. **Principal Component Analysis** (PCA) identifies the directions of maximum **variance** in the data and projects it onto a lower-dimensional space. This is useful for visualization, noise reduction, and improving the efficiency of subsequent algorithms.",
        "**Anomaly detection** is an unsupervised approach used to identify unusual data points that deviate significantly from the majority. Applications include **fraud detection** in financial transactions, identifying manufacturing defects, and monitoring network security. Statistical methods, isolation forests, and **autoencoders** are commonly used for anomaly detection.",
    ]),
    ("7.4 Neural Networks and Deep Learning", [
        "**Neural networks** are computational models inspired by the structure of biological neural systems. A neural network consists of layers of interconnected nodes called **neurons**, where each connection has an associated **weight**. The network processes input through successive layers, transforming the data at each stage to produce an output.",
        "The basic building block is the **perceptron**, a single neuron that computes a weighted sum of its inputs and applies an **activation function** to produce an output. Common activation functions include the **sigmoid function**, the **hyperbolic tangent** (tanh), and the **Rectified Linear Unit** (ReLU). The choice of activation function affects the network's ability to model complex, non-linear relationships.",
        "**Deep learning** refers to neural networks with multiple hidden layers, enabling them to learn hierarchical representations of data. **Convolutional Neural Networks** (CNNs) are specialized architectures designed for processing grid-structured data like images. They use **convolutional layers** to automatically learn spatial features such as edges, textures, and object parts.",
        "**Recurrent Neural Networks** (RNNs) are designed for sequential data such as text and time series. They maintain a hidden state that captures information from previous time steps. However, standard RNNs struggle with **long-range dependencies**. **Long Short-Term Memory** (LSTM) networks and **Gated Recurrent Units** (GRUs) address this limitation through gating mechanisms that control information flow.",
        "Training deep neural networks requires **backpropagation**, an algorithm that computes gradients of the **loss function** with respect to each weight. These gradients guide the **optimization** process, typically using variants of **stochastic gradient descent** (SGD). Challenges such as **vanishing gradients** and **overfitting** must be managed through techniques like **batch normalization**, **dropout**, and **regularization**.",
    ]),
    ("7.5 Model Evaluation and Selection", [
        "Properly evaluating machine learning models is critical to ensure they generalize well to new data. **Overfitting** occurs when a model learns the noise in the training data rather than the underlying pattern, resulting in poor performance on unseen data. Conversely, **underfitting** occurs when a model is too simple to capture the underlying structure.",
        "**Cross-validation** is a robust technique for estimating model performance. In **k-fold cross-validation**, the dataset is divided into k subsets (folds), and the model is trained k times, each time using a different fold as the validation set and the remaining folds for training. This provides a more reliable estimate of performance than a single train-test split.",
        "The **bias-variance tradeoff** is a fundamental concept in model selection. **Bias** refers to errors from overly simplistic assumptions, while **variance** refers to sensitivity to fluctuations in the training data. An ideal model balances both, achieving low bias and low variance. **Ensemble methods** like **bagging** and **boosting** aim to reduce variance and bias respectively.",
        "**Hyperparameter tuning** involves selecting the best configuration for model parameters that are not learned during training. Techniques include **grid search**, **random search**, and **Bayesian optimization**. The **learning rate**, **regularization strength**, and network architecture are examples of hyperparameters that significantly impact model performance.",
    ]),
    ("7.6 Feature Engineering", [
        "**Feature engineering** is the process of creating, selecting, and transforming variables (features) to improve model performance. It is often considered the most important step in the machine learning pipeline, as the quality of features directly determines the ceiling of model accuracy.",
        "**Feature scaling** ensures that features with different ranges contribute equally to the model. **Min-max normalization** scales values to a fixed range, typically [0, 1], while **standardization** transforms features to have zero mean and unit **standard deviation**. These techniques are particularly important for algorithms sensitive to feature magnitudes, such as **gradient descent** and **k-nearest neighbors**.",
        "**Feature selection** reduces the number of input variables by identifying the most relevant ones. Methods include **filter methods** (statistical tests), **wrapper methods** (recursive feature elimination), and **embedded methods** (LASSO regression). Removing irrelevant features reduces **computational complexity** and can improve model interpretability.",
        "Handling **missing data** is a common challenge. Strategies include removing records with missing values, **imputation** using mean, median, or mode values, and more sophisticated approaches like **multiple imputation** and model-based imputation. The choice of strategy depends on the nature and extent of missingness in the dataset.",
    ]),
    ("7.7 Ensemble Methods", [
        "**Ensemble methods** combine multiple models to produce a stronger predictive system. The principle behind ensembles is that a group of weak learners can collectively form a strong learner. Three primary ensemble strategies are **bagging**, **boosting**, and **stacking**.",
        "**Bagging** (Bootstrap Aggregating) trains multiple instances of the same algorithm on different random subsets of the training data. **Random forests** are the most well-known bagging method, combining hundreds of **decision trees**, each trained on a bootstrap sample with a random subset of features. The final prediction is made by majority vote (classification) or averaging (regression).",
        "**Boosting** sequentially trains models, with each new model focusing on the errors of the previous ones. **AdaBoost** adjusts sample weights to emphasize misclassified examples. **Gradient boosting** fits new models to the residual errors using **gradient descent** in function space. **XGBoost** and **LightGBM** are highly optimized implementations that have dominated machine learning competitions.",
        "**Stacking** (Stacked Generalization) uses predictions from multiple base models as inputs to a **meta-learner** that produces the final prediction. This approach leverages the diverse strengths of different algorithms. For example, combining a neural network, a random forest, and a support vector machine through a logistic regression meta-learner often outperforms any individual model.",
    ]),
    ("7.8 Natural Language Processing", [
        "**Natural Language Processing** (NLP) is a branch of machine learning focused on enabling computers to understand, interpret, and generate human language. NLP applications range from **text classification** and **sentiment analysis** to **machine translation** and **question answering**.",
        "Traditional NLP relies on **tokenization**, the process of breaking text into individual words or subword units called **tokens**. **Bag-of-words** models represent documents as vectors of word frequencies, ignoring word order. **TF-IDF** (Term Frequency-Inverse Document Frequency) improves upon this by weighting terms based on their importance across the corpus.",
        "**Word embeddings** represent words as dense numerical vectors in a continuous space. **Word2Vec** and **GloVe** are popular embedding techniques that capture semantic relationships between words. In these representations, semantically similar words appear close together in the **embedding space**, enabling algorithms to leverage linguistic relationships.",
        "Modern NLP is dominated by **transformer** architectures. The **attention mechanism** allows models to focus on relevant parts of the input when producing each output element. **BERT** (Bidirectional Encoder Representations from Transformers) and **GPT** (Generative Pre-trained Transformer) are landmark transformer models that achieve state-of-the-art results through **pre-training** on massive text corpora followed by **fine-tuning** on specific tasks.",
    ]),
    ("7.9 Computer Vision", [
        "**Computer vision** enables machines to interpret and understand visual information from images and videos. Core tasks include **image classification**, **object detection**, **semantic segmentation**, and **image generation**. The field has been revolutionized by deep learning, particularly **convolutional neural networks**.",
        "**Image classification** assigns a single label to an entire image. Architectures like **AlexNet**, **VGGNet**, **ResNet**, and **Inception** have progressively improved classification accuracy on benchmarks such as **ImageNet**. **Transfer learning** allows these pre-trained models to be adapted to new tasks with limited labeled data.",
        "**Object detection** identifies and localizes multiple objects within an image using **bounding boxes**. Two-stage detectors like **Faster R-CNN** first propose candidate regions, then classify them. Single-stage detectors like **YOLO** (You Only Look Once) and **SSD** perform detection in a single pass, trading some accuracy for speed.",
        "**Semantic segmentation** assigns a class label to every pixel in an image. **Fully Convolutional Networks** (FCNs) adapt classification architectures for dense prediction. **U-Net**, originally designed for biomedical image segmentation, uses an **encoder-decoder** architecture with skip connections to preserve spatial detail. Applications include autonomous driving, medical imaging, and satellite imagery analysis.",
    ]),
    ("7.10 Reinforcement Learning", [
        "**Reinforcement learning** (RL) involves an **agent** that learns to make decisions by interacting with an **environment**. At each time step, the agent observes a **state**, takes an **action**, and receives a **reward** signal. The goal is to learn a **policy** that maximizes the cumulative reward over time.",
        "The **Markov Decision Process** (MDP) provides the mathematical framework for reinforcement learning. An MDP is defined by a set of states, actions, **transition probabilities**, and a reward function. The **Bellman equation** expresses the relationship between the value of a state and the values of successor states, forming the basis for many RL algorithms.",
        "**Q-learning** is a model-free RL algorithm that learns the value of state-action pairs without requiring a model of the environment. **Deep Q-Networks** (DQN) combine Q-learning with deep neural networks to handle high-dimensional state spaces, famously achieving human-level performance on Atari games. Techniques such as **experience replay** and **target networks** stabilize the training process.",
        "**Policy gradient** methods directly optimize the policy function. **REINFORCE** computes gradients of the expected reward with respect to policy parameters. **Actor-critic** methods combine a policy network (actor) with a value network (critic) to reduce variance. **Proximal Policy Optimization** (PPO) and **Soft Actor-Critic** (SAC) are modern algorithms widely used in robotics, game playing, and autonomous systems.",
    ]),
    ("7.11 Ethics and Responsible AI", [
        "As machine learning systems become more prevalent, addressing **ethical considerations** is paramount. **Algorithmic bias** can perpetuate or amplify existing societal inequalities when models are trained on biased data. For example, facial recognition systems have shown higher error rates for certain demographic groups, raising concerns about **fairness** in automated decision-making.",
        "**Transparency** and **explainability** are essential for building trust in machine learning systems. **Black-box models** like deep neural networks are often difficult to interpret. Techniques such as **SHAP** (SHapley Additive exPlanations) and **LIME** (Local Interpretable Model-agnostic Explanations) provide insights into model predictions, helping stakeholders understand why specific decisions are made.",
        "**Data privacy** is another critical concern. Machine learning models can inadvertently memorize sensitive information from training data. **Differential privacy** provides mathematical guarantees that individual data points cannot be identified from model outputs. **Federated learning** allows models to be trained across distributed devices without centralizing sensitive data.",
        "Establishing **governance frameworks** for AI deployment requires collaboration between technologists, policymakers, and domain experts. **Model auditing**, regular performance monitoring, and clear **accountability** structures help ensure that machine learning systems operate within acceptable boundaries and continue to serve their intended purpose responsibly.",
    ]),
    ("7.12 Practical Considerations and Deployment", [
        "Deploying machine learning models in production environments introduces challenges beyond model accuracy. **Model serving** infrastructure must handle prediction requests with low **latency** and high **throughput**. Technologies like **TensorFlow Serving**, **TorchServe**, and **ONNX Runtime** provide optimized model inference engines.",
        "**Data pipelines** are essential for feeding fresh data to models in production. **ETL** (Extract, Transform, Load) processes clean and prepare incoming data. **Feature stores** centralize feature computation and serving, ensuring consistency between training and inference. **Apache Kafka** and **Apache Spark** are commonly used for real-time and batch data processing respectively.",
        "**Model monitoring** detects performance degradation over time. **Data drift** occurs when the distribution of incoming data changes relative to the training data. **Concept drift** happens when the relationship between inputs and outputs evolves. Monitoring systems track prediction distributions, error rates, and feature statistics to trigger retraining when necessary.",
        "**MLOps** (Machine Learning Operations) applies DevOps principles to the machine learning lifecycle. **Version control** for data, code, and models ensures reproducibility. **Continuous integration and deployment** (CI/CD) pipelines automate testing and deployment. Tools like **MLflow**, **Kubeflow**, and **Weights & Biases** support experiment tracking, model registry, and automated workflows.",
    ]),
    ("7.13 Summary and Future Directions", [
        "This chapter has covered the fundamental concepts of machine learning, from **supervised** and **unsupervised learning** to advanced topics like **deep learning** and **reinforcement learning**. Understanding these foundations is essential for applying machine learning effectively across diverse domains including healthcare, finance, natural language processing, and computer vision.",
        "The field continues to evolve rapidly. **Foundation models** trained on vast datasets demonstrate impressive capabilities across multiple tasks. **Self-supervised learning** reduces dependence on labeled data by learning representations from unlabeled examples. **Neural architecture search** automates the design of network structures, potentially discovering architectures beyond human intuition.",
        "As practitioners, maintaining a balance between model sophistication and practical constraints is crucial. **Interpretability**, **scalability**, **fairness**, and **robustness** remain active research areas. The most successful applications of machine learning combine strong technical foundations with careful consideration of the problem domain, data quality, and ethical implications.",
    ]),
]


def parse_bold_terms(text):
    """Extract bold terms from text marked with **term**."""
    import re
    terms = re.findall(r'\*\*(.+?)\*\*', text)
    return terms


def render_paragraph(page, y_pos, text, body_size, margin_left, margin_right):
    """Render a paragraph with bold terms. Returns new y position."""
    import re
    # Split text into segments: normal and bold
    segments = re.split(r'(\*\*.+?\*\*)', text)

    # Calculate available width
    max_width = margin_right - margin_left
    x = margin_left
    line_y = y_pos

    for seg in segments:
        if not seg:
            continue
        is_bold = seg.startswith('**') and seg.endswith('**')
        if is_bold:
            seg_text = seg[2:-2]
            font = BOLD_FONT
        else:
            seg_text = seg
            font = NORMAL_FONT

        # Split into words and render word by word
        words = seg_text.split(' ')
        for i, word in enumerate(words):
            if not word and i > 0:
                continue
            display_word = word + (' ' if i < len(words) - 1 else '')
            # Estimate word width (approximate: 0.55 * fontsize per char for helv)
            char_w = body_size * 0.52 if font == NORMAL_FONT else body_size * 0.56
            word_w = len(display_word) * char_w

            if x + word_w > margin_right and x > margin_left:
                # New line
                x = margin_left
                line_y += LINE_HEIGHT
                if line_y > MARGIN_BOTTOM - 20:
                    return line_y, True  # page full

            page.insert_text(
                pymupdf.Point(x, line_y),
                display_word,
                fontsize=body_size,
                fontname=font,
                color=(0, 0, 0),
            )
            x += word_w

    # Add paragraph spacing
    line_y += LINE_HEIGHT * 1.5
    return line_y, False


def create_initial():
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Track current page and y position
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page_num = 0
    y = MARGIN_TOP

    # --- Title page (page 1) ---
    page.insert_text(
        pymupdf.Point(MARGIN_LEFT, 120),
        CHAPTER_TITLE,
        fontsize=TITLE_SIZE,
        fontname=BOLD_FONT,
        color=(0.1, 0.1, 0.4),
    )

    # Subtitle
    page.insert_text(
        pymupdf.Point(MARGIN_LEFT, 160),
        "An Introduction to Modern Data Science",
        fontsize=14,
        fontname="heit",
        color=(0.3, 0.3, 0.3),
    )

    # Author info
    page.insert_text(
        pymupdf.Point(MARGIN_LEFT, 200),
        "Dr. Alexandra Petrov & Prof. James Nakamura",
        fontsize=12,
        fontname=NORMAL_FONT,
        color=(0.2, 0.2, 0.2),
    )
    page.insert_text(
        pymupdf.Point(MARGIN_LEFT, 218),
        "Department of Computer Science, Stanford University",
        fontsize=11,
        fontname=NORMAL_FONT,
        color=(0.3, 0.3, 0.3),
    )

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_LEFT, 240), pymupdf.Point(MARGIN_RIGHT, 240))
    shape.finish(color=(0.5, 0.5, 0.5), width=1)
    shape.commit()

    # Chapter overview
    y = 270
    overview_text = "This chapter provides a comprehensive introduction to the field of machine learning, covering core paradigms, algorithms, evaluation techniques, and practical deployment considerations. By the end of this chapter, students will have a solid foundation for understanding and applying machine learning methods to real-world problems."

    rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + 80)
    page.insert_textbox(
        rect,
        overview_text,
        fontsize=BODY_SIZE,
        fontname=NORMAL_FONT,
        color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page number
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - 5, PAGE_H - 30),
        "1",
        fontsize=10,
        fontname=NORMAL_FONT,
        color=(0.4, 0.4, 0.4),
    )

    # --- Content pages ---
    current_page_num = 1  # 0-indexed page already created

    for section_idx, (heading, paragraphs) in enumerate(SECTIONS):
        # Start new page for each section (except we might continue on current if space)
        if current_page_num > 0:  # Always start section on new page after title
            page = doc.new_page(width=PAGE_W, height=PAGE_H)
            current_page_num += 1
            y = MARGIN_TOP

        # Section heading
        page.insert_text(
            pymupdf.Point(MARGIN_LEFT, y + 5),
            heading,
            fontsize=HEADING_SIZE,
            fontname=BOLD_FONT,
            color=(0.1, 0.1, 0.4),
        )
        y += HEADING_SIZE + 15

        # Horizontal rule under heading
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN_LEFT, y - 5), pymupdf.Point(MARGIN_RIGHT, y - 5))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()
        y += 8

        for para in paragraphs:
            y_new, page_full = render_paragraph(page, y, para, BODY_SIZE, MARGIN_LEFT, MARGIN_RIGHT)
            y = y_new

            if page_full or y > MARGIN_BOTTOM - 30:
                # Add page number to current page
                page.insert_text(
                    pymupdf.Point(PAGE_W / 2 - 5, PAGE_H - 30),
                    str(current_page_num + 1),
                    fontsize=10,
                    fontname=NORMAL_FONT,
                    color=(0.4, 0.4, 0.4),
                )
                # Start new page
                page = doc.new_page(width=PAGE_W, height=PAGE_H)
                current_page_num += 1
                y = MARGIN_TOP

        # Add page number
        page.insert_text(
            pymupdf.Point(PAGE_W / 2 - 5, PAGE_H - 30),
            str(current_page_num + 1),
            fontsize=10,
            fontname=NORMAL_FONT,
            color=(0.4, 0.4, 0.4),
        )

    # Pad to ensure we have exactly 25 pages
    while doc.page_count < 25:
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        current_page_num += 1

        # Add continuation content to padding pages
        y = MARGIN_TOP
        page.insert_text(
            pymupdf.Point(MARGIN_LEFT, y),
            f"Chapter 7 (continued)",
            fontsize=HEADING_SIZE,
            fontname=BOLD_FONT,
            color=(0.1, 0.1, 0.4),
        )
        y += 30

        # Add review/exercise content with bold terms
        extra_content = [
            "**Review Questions** for this chapter cover the key concepts discussed in the preceding sections. Students should be able to explain the differences between **supervised learning** and **unsupervised learning**, describe the role of **activation functions** in neural networks, and articulate why **cross-validation** is preferred over simple train-test splits.",
            "**Practice Exercise 1**: Given a dataset of customer transactions, design a **feature engineering** pipeline that includes **feature scaling**, **missing data** handling, and **feature selection**. Justify your choice of **normalization** technique and explain how **dimensionality reduction** could improve your model's performance.",
            "**Practice Exercise 2**: Compare the performance of a **random forest** classifier with a **gradient boosting** classifier on a binary classification task. Use **k-fold cross-validation** with k=5 and report **accuracy**, **precision**, **recall**, and **F1 score** for each model. Discuss the **bias-variance tradeoff** implications of your results.",
            "**Practice Exercise 3**: Implement a simple **convolutional neural network** for **image classification** on the CIFAR-10 dataset. Experiment with different numbers of **convolutional layers**, **dropout** rates, and **learning rates**. Plot the **training loss** and **validation loss** curves and identify any signs of **overfitting**.",
            "**Key Terminology Review**: The following terms represent the core vocabulary for this chapter: **algorithm**, **model**, **training data**, **test data**, **hyperparameter**, **loss function**, **optimization**, **generalization**, **regularization**, and **deployment**. Students should be able to define each term and provide practical examples.",
            "**Further Reading**: For a deeper exploration of **deep learning**, consult Goodfellow, Bengio, and Courville's textbook. For practical implementations using **TensorFlow** and **PyTorch**, refer to the official documentation and tutorial series. The **Stanford CS229** and **CS231n** course materials provide excellent supplementary resources for **machine learning** and **computer vision** respectively.",
        ]

        for para in extra_content:
            if y > MARGIN_BOTTOM - 40:
                break
            y_new, page_full = render_paragraph(page, y, para, BODY_SIZE, MARGIN_LEFT, MARGIN_RIGHT)
            y = y_new
            if page_full:
                break

        # Page number
        page.insert_text(
            pymupdf.Point(PAGE_W / 2 - 5, PAGE_H - 30),
            str(current_page_num + 1),
            fontsize=10,
            fontname=NORMAL_FONT,
            color=(0.4, 0.4, 0.4),
        )

    # If we went over 25 pages, trim
    while doc.page_count > 25:
        doc.delete_page(doc.page_count - 1)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 25')

    # Verify
    doc = pymupdf.open(OUTPUT)
    print(f'Verified page count: {doc.page_count}')

    # Count bold terms for reference
    bold_terms = set()
    for section_heading, paragraphs in SECTIONS:
        for para in paragraphs:
            terms = parse_bold_terms(para)
            for t in terms:
                bold_terms.add(t.lower())
    print(f'Total unique bold terms defined: {len(bold_terms)}')
    doc.close()

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


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


create_initial()
