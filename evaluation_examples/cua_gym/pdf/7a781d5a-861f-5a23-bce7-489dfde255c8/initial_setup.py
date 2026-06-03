"""
Initial Setup: Create a 30-page scanned book PDF with black border artifacts
Task ID: pdf_gf2_031
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCDIR = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_gf2_031'
OUTPUT = f'{DOCDIR}/scanned_book.pdf'

# Letter size in points
PAGE_W, PAGE_H = 612, 792
BORDER = 72  # 1 inch = 72 points

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

# Book content - realistic chapter text for a scanned technical book
chapters = [
    ("Chapter 1: Introduction to Machine Learning",
     "Machine learning is a subset of artificial intelligence that focuses on building systems "
     "that learn from data. Rather than being explicitly programmed, these systems improve their "
     "performance on a specific task through experience. The field has grown enormously since the "
     "early work of Arthur Samuel in 1959, who defined machine learning as the field of study that "
     "gives computers the ability to learn without being explicitly programmed.\n\n"
     "Modern machine learning encompasses supervised learning, unsupervised learning, and "
     "reinforcement learning. Each paradigm addresses different types of problems and uses "
     "distinct algorithmic approaches. In supervised learning, the model learns from labeled "
     "examples. In unsupervised learning, the model finds patterns in unlabeled data. "
     "Reinforcement learning involves an agent learning through trial and error in an environment."),
    ("1.1 Historical Background",
     "The origins of machine learning can be traced back to the development of the first neural "
     "network models in the 1940s. Warren McCulloch and Walter Pitts proposed a mathematical "
     "model of artificial neurons in 1943. Frank Rosenblatt introduced the Perceptron in 1958, "
     "which could learn to classify patterns. However, Minsky and Papert showed in 1969 that "
     "single-layer perceptrons had fundamental limitations, leading to the first AI winter.\n\n"
     "Interest revived in the 1980s with the development of backpropagation for training "
     "multi-layer networks. The support vector machine (SVM) was introduced by Vapnik in 1995. "
     "The modern deep learning revolution began around 2012 when AlexNet demonstrated the power "
     "of deep convolutional networks on the ImageNet benchmark."),
    ("1.2 Key Concepts and Terminology",
     "Understanding machine learning requires familiarity with several fundamental concepts. "
     "A dataset consists of examples (also called instances or samples), each described by a set "
     "of features (also called attributes or predictors). In supervised learning, each example "
     "also has a label (also called a target or response variable).\n\n"
     "The model is trained on a training set and evaluated on a separate test set to assess its "
     "generalization ability. Overfitting occurs when the model learns noise in the training data "
     "rather than the underlying pattern, leading to poor performance on unseen data. "
     "Regularization techniques help prevent overfitting by penalizing model complexity."),
    ("Chapter 2: Supervised Learning",
     "Supervised learning algorithms learn a mapping from inputs to outputs given a set of "
     "input-output pairs. The two main types of supervised learning problems are classification "
     "(predicting a categorical label) and regression (predicting a continuous value).\n\n"
     "Common algorithms include linear regression, logistic regression, decision trees, random "
     "forests, gradient boosting machines, support vector machines, and neural networks. The "
     "choice of algorithm depends on the nature of the data, the size of the dataset, and the "
     "specific requirements of the application, including interpretability and computational cost."),
    ("2.1 Linear Models",
     "Linear models form the foundation of many machine learning approaches. In linear "
     "regression, the model predicts the output as a weighted sum of input features plus a bias "
     "term: y = w1*x1 + w2*x2 + ... + wn*xn + b. The weights are learned by minimizing the "
     "sum of squared errors between predictions and actual values.\n\n"
     "Logistic regression extends the linear model for binary classification by applying the "
     "sigmoid function to the linear output. Despite its name, logistic regression is a "
     "classification algorithm. The model outputs a probability between 0 and 1, and a threshold "
     "(typically 0.5) is used to make the final classification decision."),
    ("2.2 Decision Trees and Ensembles",
     "Decision trees recursively partition the feature space into regions, making predictions "
     "based on the majority class or mean value in each region. They are easy to interpret but "
     "prone to overfitting. The tree is built by selecting the feature and split point that best "
     "separates the data according to a criterion such as Gini impurity or information gain.\n\n"
     "Ensemble methods combine multiple weak learners to create a strong learner. Random forests "
     "build many decision trees on random subsets of features and data, then aggregate their "
     "predictions. Gradient boosting sequentially builds trees that correct the errors of "
     "previous trees, achieving state-of-the-art performance on many tabular datasets."),
    ("Chapter 3: Unsupervised Learning",
     "Unsupervised learning discovers hidden patterns or structure in data without labeled "
     "examples. Common tasks include clustering (grouping similar examples), dimensionality "
     "reduction (finding lower-dimensional representations), and anomaly detection.\n\n"
     "K-means clustering partitions data into K clusters by minimizing the sum of squared "
     "distances from each point to its nearest cluster center. Hierarchical clustering builds "
     "a tree of clusters through agglomerative (bottom-up) or divisive (top-down) approaches. "
     "DBSCAN identifies clusters as dense regions separated by sparse regions, making it robust "
     "to noise and able to find arbitrarily shaped clusters."),
    ("3.1 Dimensionality Reduction",
     "High-dimensional data can be difficult to visualize and process. Dimensionality reduction "
     "techniques transform data into a lower-dimensional space while preserving important "
     "structure. Principal Component Analysis (PCA) finds orthogonal directions of maximum "
     "variance and projects data onto these principal components.\n\n"
     "t-SNE (t-distributed Stochastic Neighbor Embedding) is a nonlinear technique particularly "
     "useful for visualization in 2D or 3D. Unlike PCA, t-SNE preserves local structure and can "
     "reveal clusters that are not apparent in linear projections. UMAP (Uniform Manifold "
     "Approximation and Projection) offers similar capabilities with better scalability."),
    ("3.2 Anomaly Detection",
     "Anomaly detection identifies data points that deviate significantly from the expected "
     "pattern. Applications include fraud detection in financial transactions, intrusion "
     "detection in computer networks, and fault detection in manufacturing processes.\n\n"
     "Statistical methods model the normal data distribution and flag points with low probability. "
     "Isolation forests isolate anomalies by randomly selecting features and split values; "
     "anomalies require fewer splits to isolate. Autoencoders learn to reconstruct normal data "
     "and identify anomalies as points with high reconstruction error."),
    ("Chapter 4: Neural Networks and Deep Learning",
     "Deep learning uses neural networks with multiple hidden layers to learn hierarchical "
     "representations of data. The universal approximation theorem states that a sufficiently "
     "wide single-layer network can approximate any continuous function, but deep networks can "
     "represent certain functions exponentially more efficiently than shallow ones.\n\n"
     "Training deep networks requires careful initialization, choice of activation functions, "
     "and optimization algorithms. Batch normalization, dropout, and residual connections are "
     "key techniques that enable training of very deep architectures. The availability of large "
     "datasets and powerful GPU hardware has been crucial to the success of deep learning."),
    ("4.1 Convolutional Neural Networks",
     "Convolutional Neural Networks (CNNs) are specialized architectures for processing grid-like "
     "data such as images. Convolutional layers apply learnable filters to detect local patterns, "
     "pooling layers reduce spatial dimensions, and fully connected layers make final predictions.\n\n"
     "Key architectures include LeNet-5 (1998), AlexNet (2012), VGG (2014), GoogLeNet/Inception "
     "(2014), ResNet (2015), and EfficientNet (2019). Transfer learning allows using models "
     "pre-trained on large datasets (like ImageNet) as feature extractors or starting points "
     "for fine-tuning on smaller, domain-specific datasets."),
    ("4.2 Recurrent Neural Networks",
     "Recurrent Neural Networks (RNNs) process sequential data by maintaining a hidden state "
     "that captures information from previous time steps. Standard RNNs suffer from the vanishing "
     "gradient problem, which limits their ability to learn long-range dependencies.\n\n"
     "Long Short-Term Memory (LSTM) networks address this with gating mechanisms that control "
     "information flow. The forget gate decides what to discard, the input gate decides what new "
     "information to store, and the output gate determines the hidden state. Gated Recurrent "
     "Units (GRUs) offer a simpler alternative with comparable performance."),
    ("4.3 Transformers and Attention",
     "The Transformer architecture, introduced in 2017, replaced recurrence with self-attention "
     "mechanisms that can process entire sequences in parallel. Self-attention computes a weighted "
     "sum of all positions in the sequence, allowing the model to directly attend to relevant "
     "context regardless of distance.\n\n"
     "BERT (Bidirectional Encoder Representations from Transformers) pre-trains a deep "
     "bidirectional model on masked language modeling and next sentence prediction. GPT (Generative "
     "Pre-trained Transformer) uses autoregressive pre-training for text generation. These models "
     "have achieved remarkable performance across NLP tasks through pre-training and fine-tuning."),
    ("Chapter 5: Reinforcement Learning",
     "Reinforcement learning (RL) involves an agent learning to make decisions by interacting "
     "with an environment. The agent receives rewards or penalties based on its actions and aims "
     "to maximize the cumulative reward over time. The key challenge is balancing exploration "
     "(trying new actions) with exploitation (using known good actions).\n\n"
     "The Markov Decision Process (MDP) provides the mathematical framework for RL, defined by "
     "states, actions, transition probabilities, and rewards. Value-based methods (Q-learning, "
     "DQN) estimate the value of state-action pairs. Policy-based methods (REINFORCE, PPO) "
     "directly optimize the policy that maps states to actions."),
    ("5.1 Q-Learning and Deep Q-Networks",
     "Q-learning is a model-free RL algorithm that learns the optimal action-value function "
     "Q(s, a), representing the expected cumulative reward of taking action a in state s and "
     "following the optimal policy thereafter. The Q-value is updated iteratively using the "
     "Bellman equation: Q(s,a) <- Q(s,a) + alpha * (r + gamma * max Q(s',a') - Q(s,a)).\n\n"
     "Deep Q-Networks (DQN) use a neural network to approximate Q(s,a), enabling RL in "
     "high-dimensional state spaces such as Atari games. Key innovations include experience "
     "replay (storing and reusing past transitions) and target networks (stabilizing training "
     "by using a slowly updated copy of the Q-network for computing targets)."),
    ("5.2 Policy Gradient Methods",
     "Policy gradient methods directly parameterize and optimize the policy pi(a|s; theta). "
     "The REINFORCE algorithm estimates the gradient of expected reward using Monte Carlo "
     "sampling and updates the policy parameters in the direction of higher reward.\n\n"
     "Actor-Critic methods combine value-based and policy-based approaches. The actor learns "
     "the policy while the critic estimates the value function, reducing variance in gradient "
     "estimates. Proximal Policy Optimization (PPO) constrains policy updates to prevent large "
     "steps that could destabilize training, achieving robust performance across diverse tasks."),
    ("Chapter 6: Model Evaluation and Selection",
     "Proper model evaluation is critical for developing reliable machine learning systems. "
     "The goal is to estimate how well a model will perform on unseen data. Overfitting to the "
     "training data gives an optimistic estimate of performance, while the test set provides an "
     "unbiased evaluation.\n\n"
     "Cross-validation partitions the data into K folds, trains on K-1 folds, and evaluates "
     "on the remaining fold. This process is repeated K times, and results are averaged. "
     "Stratified cross-validation ensures each fold has approximately the same class distribution "
     "as the full dataset, which is important for imbalanced classification problems."),
    ("6.1 Classification Metrics",
     "For classification tasks, accuracy alone can be misleading, especially with imbalanced "
     "classes. Precision measures the fraction of positive predictions that are correct. Recall "
     "measures the fraction of actual positives that are correctly identified. The F1 score is "
     "the harmonic mean of precision and recall.\n\n"
     "The ROC curve plots true positive rate against false positive rate at various thresholds. "
     "The AUC (Area Under the ROC Curve) provides a threshold-independent measure of model "
     "quality. The confusion matrix gives a detailed breakdown of true positives, true negatives, "
     "false positives, and false negatives for each class."),
    ("6.2 Regression Metrics",
     "For regression tasks, common metrics include Mean Squared Error (MSE), Root Mean Squared "
     "Error (RMSE), Mean Absolute Error (MAE), and R-squared (coefficient of determination). "
     "MSE penalizes large errors more heavily due to squaring, while MAE is more robust to "
     "outliers.\n\n"
     "R-squared represents the proportion of variance in the target variable explained by the "
     "model. A value of 1.0 indicates perfect prediction, while 0.0 means the model is no "
     "better than predicting the mean. Negative R-squared values indicate the model performs "
     "worse than the constant mean predictor."),
    ("Chapter 7: Feature Engineering",
     "Feature engineering is the process of using domain knowledge to create features that "
     "make machine learning algorithms work better. Good features can significantly improve "
     "model performance, often more than algorithmic improvements alone.\n\n"
     "Common techniques include handling missing values (imputation, indicator variables), "
     "encoding categorical variables (one-hot encoding, target encoding), scaling numerical "
     "features (standardization, normalization), and creating interaction features. Feature "
     "selection methods identify the most informative features, reducing dimensionality and "
     "improving model interpretability."),
    ("7.1 Handling Missing Data",
     "Missing data is common in real-world datasets. Simple approaches include dropping rows "
     "or columns with missing values, which can lead to information loss. Mean or median "
     "imputation replaces missing values with the column average but ignores relationships "
     "between features.\n\n"
     "More sophisticated methods include K-nearest neighbors imputation, which uses similar "
     "instances to estimate missing values, and multiple imputation using chained equations "
     "(MICE), which models each feature with missing values as a function of other features. "
     "Adding a binary indicator for whether the value was missing can also be informative."),
    ("7.2 Feature Scaling and Transformation",
     "Many algorithms (e.g., SVMs, k-NN, gradient descent) are sensitive to feature scales. "
     "Standardization (z-score normalization) transforms features to have zero mean and unit "
     "variance. Min-max scaling rescales features to a fixed range, typically [0, 1].\n\n"
     "Log transformations can help with skewed distributions. Power transforms (Box-Cox, "
     "Yeo-Johnson) find the optimal transformation to make data more Gaussian. Polynomial "
     "features create nonlinear terms by computing products and powers of existing features, "
     "allowing linear models to capture nonlinear relationships."),
    ("Chapter 8: Practical Considerations",
     "Deploying machine learning models in production involves challenges beyond model accuracy. "
     "Data pipelines must be robust and reproducible. Models need monitoring for performance "
     "degradation (concept drift) when the data distribution changes over time.\n\n"
     "MLOps practices include version control for data and models, automated testing of model "
     "performance, A/B testing for comparing models in production, and automated retraining "
     "pipelines. Fairness, accountability, and transparency are increasingly important "
     "considerations in deployed machine learning systems."),
    ("8.1 Data Quality and Preprocessing",
     "The quality of training data directly impacts model performance. Data quality issues "
     "include duplicates, inconsistent formats, outliers, label noise, and sampling bias. "
     "Data validation checks should be automated as part of the training pipeline.\n\n"
     "Text preprocessing may include tokenization, lowercasing, removing stopwords, stemming, "
     "and lemmatization. Image preprocessing includes resizing, normalization, and data "
     "augmentation (random flips, rotations, crops) to increase training set diversity. "
     "Audio preprocessing involves computing spectrograms or mel-frequency cepstral coefficients."),
    ("8.2 Scalability and Efficiency",
     "Training machine learning models on large datasets requires efficient computation. "
     "Mini-batch stochastic gradient descent processes data in small batches, enabling training "
     "on datasets that do not fit in memory. Distributed training across multiple GPUs or "
     "machines can further reduce training time.\n\n"
     "Model compression techniques include pruning (removing unnecessary weights), quantization "
     "(reducing numerical precision), and knowledge distillation (training a smaller model to "
     "mimic a larger one). These techniques are crucial for deploying models on edge devices "
     "with limited computational resources."),
    ("Appendix A: Mathematical Foundations",
     "Linear algebra provides the language of machine learning. Vectors represent data points "
     "and model parameters. Matrices represent datasets and linear transformations. Key "
     "operations include matrix multiplication, eigendecomposition, and singular value "
     "decomposition (SVD).\n\n"
     "Probability and statistics underpin many machine learning concepts. Bayes' theorem "
     "relates conditional probabilities and forms the basis of Bayesian machine learning. "
     "Maximum likelihood estimation finds parameters that maximize the probability of observed "
     "data. Information theory concepts like entropy and KL divergence measure uncertainty "
     "and distribution differences."),
    ("Appendix B: Optimization",
     "Most machine learning models are trained by minimizing a loss function using optimization "
     "algorithms. Gradient descent updates parameters in the direction of steepest descent: "
     "theta <- theta - alpha * gradient(L). The learning rate alpha controls step size and "
     "must be carefully tuned.\n\n"
     "Adam optimizer combines momentum (exponentially decaying average of past gradients) with "
     "RMSProp (adaptive learning rates). It is the default optimizer for many deep learning "
     "applications. Learning rate schedules (cosine annealing, warm restarts, reduce on plateau) "
     "can further improve convergence."),
    ("Appendix C: Software Tools",
     "Popular machine learning libraries include scikit-learn for classical ML algorithms, "
     "PyTorch and TensorFlow for deep learning, XGBoost and LightGBM for gradient boosting, "
     "and Hugging Face Transformers for NLP models.\n\n"
     "Experiment tracking tools such as MLflow, Weights & Biases, and Neptune help manage "
     "hyperparameters, metrics, and artifacts across experiments. Jupyter notebooks are widely "
     "used for interactive development and visualization. Cloud platforms (AWS SageMaker, "
     "Google Vertex AI, Azure ML) provide managed infrastructure for training and deployment."),
    ("References and Further Reading",
     "Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer.\n"
     "Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press.\n"
     "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning. "
     "Springer.\n"
     "Murphy, K. P. (2012). Machine Learning: A Probabilistic Perspective. MIT Press.\n"
     "Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction. MIT Press.\n"
     "Chollet, F. (2021). Deep Learning with Python. Manning Publications.\n"
     "Geron, A. (2022). Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow. "
     "O'Reilly Media.\n"
     "Jurafsky, D., & Martin, J. H. (2024). Speech and Language Processing. Pearson."),
    ("Index",
     "A\nAccuracy 245, Adam optimizer 312, Anomaly detection 134, Attention mechanism 198, "
     "Autoencoder 141, AUC-ROC 250\n\n"
     "B\nBackpropagation 156, Batch normalization 172, Bayes' theorem 308, BERT 201, "
     "Bias-variance tradeoff 38, Boosting 98\n\n"
     "C\nClassification 52, Clustering 118, CNN 176, Confusion matrix 248, Cross-validation 242, "
     "Curse of dimensionality 126\n\n"
     "D\nDecision tree 88, Deep learning 152, Dimensionality reduction 124, Dropout 170, "
     "DQN 222\n\n"
     "E-F\nEnsemble methods 94, Epoch 158, F1 score 247, Feature engineering 264, "
     "Feature scaling 280\n\n"
     "G-K\nGAN 210, Gradient descent 310, GRU 192, K-means 120, K-NN 72\n\n"
     "L-N\nLasso 68, LSTM 190, Learning rate 162, Linear regression 54, "
     "Logistic regression 62, Neural network 152, NLP 196\n\n"
     "O-P\nOverfitting 36, PCA 128, Perceptron 20, Policy gradient 228, PPO 232, "
     "Precision 246, Pruning 298\n\n"
     "R-S\nRandom forest 96, Recall 246, Regularization 40, Reinforcement learning 216, "
     "ResNet 184, RNN 188, SVM 76\n\n"
     "T-Z\nTransfer learning 186, Transformer 198, t-SNE 130, UMAP 132, "
     "Underfitting 38, XGBoost 100"),
]

def create_initial():
    os.makedirs(DOCDIR, exist_ok=True)

    doc = pymupdf.open()

    for i in range(30):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        shape = page.new_shape()

        # Draw black border artifacts (simulating scanning artifacts)
        # Top border
        shape.draw_rect(pymupdf.Rect(0, 0, PAGE_W, BORDER))
        shape.finish(color=(0, 0, 0), fill=(0, 0, 0))
        # Bottom border
        shape.draw_rect(pymupdf.Rect(0, PAGE_H - BORDER, PAGE_W, PAGE_H))
        shape.finish(color=(0, 0, 0), fill=(0, 0, 0))
        # Left border
        shape.draw_rect(pymupdf.Rect(0, BORDER, BORDER, PAGE_H - BORDER))
        shape.finish(color=(0, 0, 0), fill=(0, 0, 0))
        # Right border
        shape.draw_rect(pymupdf.Rect(PAGE_W - BORDER, BORDER, PAGE_W, PAGE_H - BORDER))
        shape.finish(color=(0, 0, 0), fill=(0, 0, 0))

        shape.commit()

        # Add content in the central area (within the 72pt margins)
        content_x = BORDER + 10  # small inner margin
        content_top = BORDER + 15

        title, body = chapters[i]

        # Page number at bottom center of content area
        page.insert_text(
            pymupdf.Point(PAGE_W / 2 - 10, PAGE_H - BORDER - 10),
            str(i + 1),
            fontsize=10,
            fontname="tiro",
            color=(0, 0, 0),
        )

        # Chapter/section title
        page.insert_text(
            pymupdf.Point(content_x, content_top + 16),
            title,
            fontsize=14,
            fontname="hebo",
            color=(0, 0, 0),
        )

        # Body text in a bounded rectangle
        text_rect = pymupdf.Rect(content_x, content_top + 40, PAGE_W - BORDER - 10, PAGE_H - BORDER - 25)
        page.insert_textbox(
            text_rect,
            body,
            fontsize=10,
            fontname="tiro",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

    # Set metadata
    doc.set_metadata({
        "title": "Introduction to Machine Learning: Theory and Practice",
        "author": "Dr. Alexandra Chen, Prof. Robert Williams",
        "subject": "Machine Learning Textbook",
        "keywords": "machine learning, AI, deep learning, neural networks",
        "creator": "Scanner Pro 3000",
        "producer": "Scanned Document",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')

create_initial()
