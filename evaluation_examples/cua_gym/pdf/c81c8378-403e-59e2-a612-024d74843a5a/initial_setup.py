"""
Initial Setup: Create a 10-page academic paper PDF with mixed English prose and mathematical notation.
Task ID: pdf_res_056
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_056'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/foreign_paper.pdf'


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

    # Remove any leftover english_text.txt (must NOT exist in initial state)
    txt_path = f'{PAPERS_DIR}/english_text.txt'
    if os.path.exists(txt_path):
        os.remove(txt_path)

    doc = pymupdf.open()

    # ---- Page 1: Title page ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(120, 120), "On the Convergence Properties of", fontsize=20, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 155), "Stochastic Gradient Methods in Deep Learning", fontsize=20, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(180, 210), "Elena Kowalski, James Harrington, Mei-Ling Zhou", fontsize=12, fontname="tiit", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(140, 235), "Department of Applied Mathematics, Stanford University", fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(200, 260), "Published: March 15, 2025", fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))

    abstract_rect = pymupdf.Rect(72, 310, 523, 520)
    abstract_text = (
        "Abstract. This paper investigates the convergence behavior of stochastic gradient descent and its "
        "variants when applied to non-convex optimization landscapes common in deep neural network training. "
        "We provide new theoretical bounds that extend the classical results of Robbins and Monro to settings "
        "where the loss surface exhibits saddle points and local minima. Our analysis covers both the standard "
        "SGD algorithm and adaptive methods such as Adam and RMSProp. We demonstrate that under mild regularity "
        "conditions, the iterates converge almost surely to a first-order stationary point. Experimental results "
        "on CIFAR-10 and ImageNet validate the tightness of our theoretical predictions."
    )
    page.insert_textbox(abstract_rect, abstract_text, fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Math on title page
    page.insert_text(pymupdf.Point(72, 550), "Key result:", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(130, 580), "E[||grad f(x_k)||^2] <= C / sqrt(T)", fontsize=12, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(130, 610), "where T is the total iteration count and C = O(sigma^2 / eta)", fontsize=10, fontname="cour", color=(0, 0, 0.5))

    # ---- Page 2: Introduction ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "1. Introduction", fontsize=16, fontname="tibo", color=(0, 0, 0))
    intro_rect = pymupdf.Rect(72, 85, 523, 300)
    intro_text = (
        "Deep learning has transformed numerous fields from computer vision to natural language processing. "
        "At the core of training deep neural networks lies the optimization of a high-dimensional non-convex "
        "objective function. Stochastic gradient descent remains the workhorse algorithm for this purpose, "
        "despite limited theoretical understanding of its behavior in non-convex settings. Recent work by "
        "Bottou, Curtis, and Nocedal has made progress in establishing convergence guarantees, but significant "
        "gaps remain. In particular, the interaction between learning rate schedules and batch size selection "
        "continues to challenge practitioners and theorists alike."
    )
    page.insert_textbox(intro_rect, intro_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Math block
    page.insert_text(pymupdf.Point(72, 320), "The standard SGD update rule is:", fontsize=11, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(150, 350), "x_{k+1} = x_k - eta_k * g(x_k, xi_k)", fontsize=12, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(150, 375), "where g(x_k, xi_k) = grad f(x_k; xi_k)", fontsize=12, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(150, 400), "E[g(x_k, xi_k)] = grad F(x_k)", fontsize=12, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(150, 425), "Var(g(x_k, xi_k)) <= sigma^2", fontsize=12, fontname="cour", color=(0, 0, 0.5))

    cont_rect = pymupdf.Rect(72, 460, 523, 620)
    cont_text = (
        "Here eta_k denotes the learning rate at iteration k, and xi_k represents the random sample drawn "
        "from the training distribution. The noise in the gradient estimate is bounded by the variance parameter sigma. "
        "Traditional convergence analysis requires the objective to be strongly convex, a condition that is "
        "rarely satisfied in deep learning. Our contribution is to relax this assumption significantly while "
        "still obtaining meaningful convergence rates."
    )
    page.insert_textbox(cont_rect, cont_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # More math
    page.insert_text(pymupdf.Point(72, 640), "Assumption 1 (L-smoothness):", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 665), "||grad F(x) - grad F(y)|| <= L * ||x - y||  for all x, y in R^d", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(72, 700), "Assumption 2 (Bounded variance):", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 725), "E[||g(x, xi) - grad F(x)||^2] <= sigma^2  for all x in R^d", fontsize=11, fontname="cour", color=(0, 0, 0.5))

    # ---- Page 3: Theoretical Framework ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "2. Theoretical Framework", fontsize=16, fontname="tibo", color=(0, 0, 0))
    framework_rect = pymupdf.Rect(72, 85, 523, 240)
    framework_text = (
        "In this section we establish the mathematical foundations for our convergence analysis. "
        "We consider the general unconstrained optimization problem of minimizing a differentiable "
        "objective function over Euclidean space. The function need not be convex, but we require "
        "it to be bounded below and sufficiently smooth. These conditions are satisfied by most "
        "loss functions used in deep learning, including cross-entropy and mean squared error with "
        "appropriate regularization."
    )
    page.insert_textbox(framework_rect, framework_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Dense math block
    page.insert_text(pymupdf.Point(72, 260), "Definition 2.1. The Lyapunov function is defined as:", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(130, 290), "V(x) = F(x) - F* + (lambda/2) * ||x - x*||^2", fontsize=12, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(72, 320), "Lemma 2.2. Under Assumptions 1-2, the following descent inequality holds:", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 350), "E[V(x_{k+1})] <= V(x_k) - eta_k * (1 - L*eta_k/2) * ||grad F(x_k)||^2", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 375), "                + eta_k^2 * L * sigma^2 / 2", fontsize=11, fontname="cour", color=(0, 0, 0.5))

    proof_rect = pymupdf.Rect(72, 410, 523, 560)
    proof_text = (
        "Proof. By the smoothness assumption, we can write the Taylor expansion of the objective "
        "function around the current iterate. Applying the gradient update rule and taking expectations "
        "over the random sample yields the desired bound. The key insight is that the cross-term "
        "involving the stochastic gradient noise vanishes in expectation due to the unbiasedness "
        "condition. The remaining variance term is controlled by the squared learning rate, which "
        "drives the trade-off between convergence speed and asymptotic accuracy."
    )
    page.insert_textbox(proof_rect, proof_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # More equations
    page.insert_text(pymupdf.Point(72, 580), "Theorem 2.3 (Main Result):", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 610), "min_{k=0..T-1} E[||grad F(x_k)||^2] <= 2*(F(x_0) - F*) / (eta*T)", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 635), "                                      + L * eta * sigma^2", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(72, 670), "Setting eta = 1 / (L * sqrt(T)):", fontsize=11, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 695), "min_{k} E[||grad F(x_k)||^2] = O( (L*Delta + sigma^2) / sqrt(T) )", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 720), "where Delta = F(x_0) - F*", fontsize=11, fontname="cour", color=(0, 0, 0.5))

    # ---- Page 4: Adaptive Methods ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "3. Extension to Adaptive Methods", fontsize=16, fontname="tibo", color=(0, 0, 0))
    adaptive_rect = pymupdf.Rect(72, 85, 523, 260)
    adaptive_text = (
        "Modern deep learning practice relies heavily on adaptive gradient methods that maintain "
        "per-parameter learning rates. The Adam optimizer, introduced by Kingma and Ba in 2015, "
        "has become the default choice for training transformers and other large-scale models. "
        "Despite its popularity, the theoretical convergence properties of Adam remain poorly "
        "understood. In this section, we extend our framework to cover Adam and related methods "
        "such as RMSProp and AdaGrad. We show that similar convergence rates can be established "
        "under slightly stronger regularity conditions."
    )
    page.insert_textbox(adaptive_rect, adaptive_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Adam algorithm
    page.insert_text(pymupdf.Point(72, 280), "Algorithm 1: Adam Update Rule", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 310), "m_k = beta_1 * m_{k-1} + (1 - beta_1) * g_k", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 335), "v_k = beta_2 * v_{k-1} + (1 - beta_2) * g_k^2", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 360), "m_hat_k = m_k / (1 - beta_1^k)", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 385), "v_hat_k = v_k / (1 - beta_2^k)", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 410), "x_{k+1} = x_k - eta * m_hat_k / (sqrt(v_hat_k) + epsilon)", fontsize=11, fontname="cour", color=(0, 0, 0.5))

    adam_rect = pymupdf.Rect(72, 445, 523, 600)
    adam_text = (
        "The bias correction terms ensure that the moment estimates are unbiased in the early stages "
        "of optimization. The epsilon parameter prevents division by zero and is typically set to a "
        "small value such as ten to the negative eighth power. In practice, the default hyperparameters "
        "of beta one equals 0.9 and beta two equals 0.999 work well across a wide range of architectures "
        "and datasets. However, recent work has shown that these defaults may not be optimal for all "
        "training scenarios, particularly for very deep networks with residual connections."
    )
    page.insert_textbox(adam_rect, adam_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Convergence theorem for Adam
    page.insert_text(pymupdf.Point(72, 620), "Theorem 3.1 (Adam Convergence):", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 650), "sum_{k=1}^{T} E[||grad F(x_k)||^2 / sqrt(v_hat_k)]", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 675), "    <= C_1 * d * log(T) + C_2 * sigma^2 * sqrt(T)", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 700), "where d is the parameter dimension", fontsize=11, fontname="cour", color=(0, 0, 0.5))

    # ---- Page 5: Experimental Setup ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "4. Experimental Setup", fontsize=16, fontname="tibo", color=(0, 0, 0))
    exp_rect = pymupdf.Rect(72, 85, 523, 320)
    exp_text = (
        "We validate our theoretical findings through extensive experiments on standard benchmarks. "
        "All experiments were conducted on a cluster of eight NVIDIA A100 GPUs with 80 gigabytes of "
        "memory each. We use PyTorch version 2.1 as our deep learning framework. For image classification, "
        "we train ResNet-50 and Vision Transformer models on CIFAR-10 and ImageNet datasets. For natural "
        "language processing, we fine-tune BERT-base on the GLUE benchmark. Each experiment is repeated five "
        "times with different random seeds and we report mean and standard deviation. The learning rate is "
        "selected by grid search over the range from 0.0001 to 0.1, with logarithmic spacing. We compare "
        "standard SGD with momentum, Adam, AdamW, and our proposed modification which we call Stabilized "
        "Adam. The key modification involves clipping the adaptive learning rate to prevent excessively "
        "large updates in the early phase of training."
    )
    page.insert_textbox(exp_rect, exp_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 340), "Hyperparameter configurations:", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 365), "SGD:    eta = 0.1, momentum = 0.9, weight_decay = 5e-4", fontsize=10, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 385), "Adam:   eta = 1e-3, beta_1 = 0.9, beta_2 = 0.999, eps = 1e-8", fontsize=10, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 405), "AdamW:  eta = 1e-3, beta_1 = 0.9, beta_2 = 0.999, lambda = 0.01", fontsize=10, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 425), "S-Adam: eta = 3e-4, beta_1 = 0.9, beta_2 = 0.98, clip = 1.0", fontsize=10, fontname="cour", color=(0, 0, 0.5))

    results_rect = pymupdf.Rect(72, 460, 523, 650)
    results_text = (
        "The training is performed for 200 epochs on CIFAR-10 and 90 epochs on ImageNet, following "
        "standard practice. We apply cosine annealing learning rate schedule with a warm-up period "
        "of 5 epochs. Data augmentation includes random horizontal flipping, random cropping with "
        "four pixel padding, and Cutout regularization. For the language tasks, we use a linear "
        "warm-up over the first ten percent of training steps followed by linear decay to zero. "
        "Batch sizes are 256 for CIFAR-10, 1024 for ImageNet, and 32 for GLUE tasks."
    )
    page.insert_textbox(results_rect, results_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Loss function
    page.insert_text(pymupdf.Point(72, 670), "The training loss function is:", fontsize=11, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 695), "L(theta) = -(1/N) * sum_{i=1}^{N} sum_{c=1}^{C} y_{ic} * log(p_{ic}(theta))", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 720), "         + (lambda/2) * ||theta||^2", fontsize=11, fontname="cour", color=(0, 0, 0.5))

    # ---- Page 6: Results ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "5. Experimental Results", fontsize=16, fontname="tibo", color=(0, 0, 0))
    res_rect = pymupdf.Rect(72, 85, 523, 300)
    res_text = (
        "Table 1 presents the classification accuracy of each optimizer on the benchmark datasets. "
        "On CIFAR-10, all methods achieve comparable final accuracy, but Stabilized Adam reaches "
        "the target accuracy approximately 30 percent faster than standard SGD. The gap is more "
        "pronounced on ImageNet, where Stabilized Adam achieves 77.2 percent top-1 accuracy compared "
        "to 76.5 percent for vanilla Adam and 76.8 percent for AdamW. Interestingly, SGD with momentum "
        "achieves the highest final accuracy of 77.4 percent on ImageNet, consistent with prior "
        "observations that SGD generalizes better on image classification tasks. For the GLUE benchmark, "
        "adaptive methods significantly outperform SGD, confirming the importance of per-parameter "
        "learning rates for fine-tuning pretrained language models."
    )
    page.insert_textbox(res_rect, res_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Table-like data as text
    page.insert_text(pymupdf.Point(72, 320), "Table 1: Test Accuracy (%) across datasets", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 345), "Optimizer    CIFAR-10    ImageNet    GLUE (avg)", fontsize=10, fontname="cour", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 362), "-----------------------------------------------", fontsize=10, fontname="cour", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 379), "SGD+M        95.3+-0.1   77.4+-0.2   78.1+-0.4", fontsize=10, fontname="cour", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 396), "Adam         95.1+-0.2   76.5+-0.3   84.6+-0.2", fontsize=10, fontname="cour", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 413), "AdamW        95.2+-0.1   76.8+-0.2   85.1+-0.3", fontsize=10, fontname="cour", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 430), "S-Adam       95.4+-0.1   77.2+-0.2   85.3+-0.2", fontsize=10, fontname="cour", color=(0, 0, 0))

    conv_rect = pymupdf.Rect(72, 460, 523, 620)
    conv_text = (
        "Figure 1 shows the training loss curves for ResNet-50 on ImageNet. The adaptive methods "
        "exhibit much faster initial convergence, reducing the training loss by more than an order "
        "of magnitude within the first ten epochs. However, SGD eventually catches up and achieves "
        "a slightly lower final training loss, which correlates with its superior generalization "
        "performance. Stabilized Adam bridges this gap by preventing the unstable gradient updates "
        "that occur in early training, leading to a smoother optimization trajectory."
    )
    page.insert_textbox(conv_rect, conv_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Convergence rate equations
    page.insert_text(pymupdf.Point(72, 640), "Measured convergence rates:", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 665), "SGD:    ||grad F||^2 ~ O(T^{-0.48}),  R^2 = 0.97", fontsize=10, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 685), "Adam:   ||grad F||^2 ~ O(T^{-0.51}),  R^2 = 0.95", fontsize=10, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 705), "S-Adam: ||grad F||^2 ~ O(T^{-0.53}),  R^2 = 0.98", fontsize=10, fontname="cour", color=(0, 0, 0.5))

    # ---- Page 7: Analysis ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "6. Analysis and Discussion", fontsize=16, fontname="tibo", color=(0, 0, 0))
    analysis_rect = pymupdf.Rect(72, 85, 523, 310)
    analysis_text = (
        "The experimental results align closely with our theoretical predictions. The observed "
        "convergence rate of approximately one over the square root of T matches the upper bound "
        "derived in Theorem 2.3. This suggests that our bounds are tight up to constant factors. "
        "A key finding is that the effective noise level varies significantly across architectures. "
        "For ResNet-50, the gradient noise is relatively low due to the residual connections, which "
        "stabilize the optimization landscape. In contrast, Vision Transformers exhibit higher "
        "gradient variance, particularly in the attention layers where the parameter space is "
        "heavily over-parameterized."
    )
    page.insert_textbox(analysis_rect, analysis_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Analysis equations
    page.insert_text(pymupdf.Point(72, 330), "Effective noise ratio:", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 355), "rho(x) = sigma(x)^2 / ||grad F(x)||^2", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 380), "For ResNet-50: rho_avg = 3.2 +- 0.8", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 405), "For ViT-Base:  rho_avg = 12.7 +- 3.4", fontsize=11, fontname="cour", color=(0, 0, 0.5))

    gen_rect = pymupdf.Rect(72, 440, 523, 620)
    gen_text = (
        "The generalization gap between training and test accuracy provides additional insight "
        "into the role of optimization dynamics. We observe that SGD consistently produces flatter "
        "minima, as measured by the Hessian spectral norm, which correlates with better generalization. "
        "Adaptive methods tend to converge to sharper minima with larger Hessian eigenvalues. "
        "Stabilized Adam mitigates this effect by capping the effective step size, preventing the "
        "optimizer from exploiting sharp descent directions that lead to narrow valleys in the loss "
        "landscape. This observation is consistent with the implicit regularization theory of SGD "
        "proposed by Smith and Le in 2018."
    )
    page.insert_textbox(gen_rect, gen_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Hessian eigenvalue math
    page.insert_text(pymupdf.Point(72, 640), "Sharpness metric:", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 665), "S(x) = max_{||delta||<=rho} [F(x + delta) - F(x)]", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 690), "     ~ (rho^2 / 2) * lambda_max(H(x))", fontsize=11, fontname="cour", color=(0, 0, 0.5))

    # ---- Page 8: Related Work ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "7. Related Work", fontsize=16, fontname="tibo", color=(0, 0, 0))
    related_rect = pymupdf.Rect(72, 85, 523, 370)
    related_text = (
        "The convergence of SGD has been studied extensively since the seminal work of Robbins and "
        "Monro in 1951. Classical results require strong convexity and bounded gradients, assumptions "
        "that are clearly violated in deep learning. Ghadimi and Lan provided the first convergence "
        "rate for SGD in the non-convex setting, showing that it achieves an epsilon-stationary point "
        "in at most order of one over epsilon squared iterations. Our work builds on this foundation "
        "but provides tighter constants and extends the analysis to adaptive methods.\n\n"
        "The convergence analysis of Adam has attracted significant attention following the work of "
        "Reddi, Kale, and Kumar, who showed that the original convergence proof by Kingma and Ba "
        "contained a flaw. They proposed AMSGrad as a fix, though subsequent work showed that the "
        "divergence issue is rare in practice. Chen and colleagues provided a refined analysis showing "
        "that Adam converges under a bounded noise condition, which is weaker than the almost sure "
        "boundedness assumed in earlier work. Our contribution unifies these results within a single "
        "Lyapunov-based framework."
    )
    page.insert_textbox(related_rect, related_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Comparison formula
    page.insert_text(pymupdf.Point(72, 390), "Table 2: Comparison of convergence rate bounds", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 415), "Ghadimi-Lan (2013):  O(1/sqrt(T))        non-convex SGD", fontsize=10, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 435), "Reddi et al. (2018): O(sqrt(d)/sqrt(T))   AMSGrad", fontsize=10, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 455), "Chen et al. (2019):  O(d^{1/4}/sqrt(T))   Adam", fontsize=10, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 475), "Ours (2025):         O(1/sqrt(T))          Adam + S-Adam", fontsize=10, fontname="cour", color=(0, 0, 0.5))

    improvement_rect = pymupdf.Rect(72, 510, 523, 680)
    improvement_text = (
        "Our dimension-independent bound for Adam represents a significant improvement over prior "
        "work. The key technical innovation is the use of a coordinate-wise Lyapunov function that "
        "accounts for the interaction between the first and second moment estimates. This allows us "
        "to cancel the dimension-dependent terms that appear in the analysis of Reddi and Chen. "
        "The practical implication is that Adam is theoretically justified for high-dimensional "
        "optimization problems, such as training large language models with billions of parameters."
    )
    page.insert_textbox(improvement_rect, improvement_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 9: Conclusion ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "8. Conclusion", fontsize=16, fontname="tibo", color=(0, 0, 0))
    conclusion_rect = pymupdf.Rect(72, 85, 523, 340)
    conclusion_text = (
        "We have presented a unified convergence analysis for stochastic gradient descent and its "
        "adaptive variants in the non-convex optimization setting. Our main theoretical contribution "
        "is a dimension-independent convergence rate for Adam, resolving a long-standing open question "
        "in the optimization literature. The analysis is based on a novel Lyapunov function that "
        "captures the interaction between momentum and adaptive learning rates.\n\n"
        "On the practical side, we introduced Stabilized Adam, a simple modification that clips the "
        "adaptive step size to prevent instability in early training. Experiments on image classification "
        "and natural language understanding benchmarks demonstrate that Stabilized Adam combines the fast "
        "convergence of adaptive methods with the generalization performance of SGD. We believe this "
        "approach will be particularly valuable for training large-scale models where both training "
        "efficiency and final model quality are critical."
    )
    page.insert_textbox(conclusion_rect, conclusion_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Future directions
    page.insert_text(pymupdf.Point(72, 360), "Future Directions:", fontsize=11, fontname="tibo", color=(0, 0, 0))
    future_rect = pymupdf.Rect(72, 380, 523, 520)
    future_text = (
        "Several promising directions remain for future investigation. First, extending our analysis "
        "to distributed and federated learning settings, where communication constraints introduce "
        "additional sources of gradient noise. Second, investigating the convergence properties of "
        "recently proposed optimizers such as LAMB and Lion, which have shown strong performance in "
        "training large language models. Third, developing tighter lower bounds to determine whether "
        "the one over square root of T rate is optimal for non-convex stochastic optimization."
    )
    page.insert_textbox(future_rect, future_text, fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Summary equation
    page.insert_text(pymupdf.Point(72, 540), "Summary of main results:", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(100, 565), "SGD:    E[||grad F(x_k)||^2] = O(1/sqrt(T))", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 590), "Adam:   E[||grad F(x_k)||^2] = O(1/sqrt(T))", fontsize=11, fontname="cour", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(100, 615), "S-Adam: E[||grad F(x_k)||^2] = O(1/sqrt(T))  [improved constants]", fontsize=11, fontname="cour", color=(0, 0, 0.5))

    # ---- Page 10: References ----
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(72, 60), "References", fontsize=16, fontname="tibo", color=(0, 0, 0))
    refs = [
        "[1] Robbins, H. and Monro, S. A stochastic approximation method. Annals of Mathematical Statistics, 22(3):400-407, 1951.",
        "[2] Bottou, L., Curtis, F., and Nocedal, J. Optimization methods for large-scale machine learning. SIAM Review, 60(2):223-311, 2018.",
        "[3] Kingma, D.P. and Ba, J. Adam: A method for stochastic optimization. In International Conference on Learning Representations, 2015.",
        "[4] Reddi, S.J., Kale, S., and Kumar, S. On the convergence of Adam and beyond. In ICLR, 2018.",
        "[5] Ghadimi, S. and Lan, G. Stochastic first- and zeroth-order methods for nonconvex stochastic programming. SIAM Journal on Optimization, 23(4):2341-2368, 2013.",
        "[6] Chen, X., Liu, S., Sun, R., and Hong, M. On the convergence of a class of Adam-type algorithms for non-convex optimization. In ICLR, 2019.",
        "[7] Smith, S. and Le, Q. A Bayesian perspective on generalization and stochastic gradient descent. In ICLR, 2018.",
        "[8] He, K., Zhang, X., Ren, S., and Sun, J. Deep residual learning for image recognition. In CVPR, pages 770-778, 2016.",
        "[9] Dosovitskiy, A. et al. An image is worth 16x16 words: Transformers for image recognition at scale. In ICLR, 2021.",
        "[10] Devlin, J. et al. BERT: Pre-training of deep bidirectional transformers for language understanding. In NAACL, 2019.",
        "[11] Loshchilov, I. and Hutter, F. Decoupled weight decay regularization. In ICLR, 2019.",
        "[12] You, Y. et al. Large batch optimization for deep learning: Training BERT in 76 minutes. In ICLR, 2020.",
        "[13] Chen, X. et al. Symbolic discovery of optimization algorithms. In NeurIPS, 2023.",
    ]
    y_pos = 95
    for ref in refs:
        ref_rect = pymupdf.Rect(72, y_pos, 523, y_pos + 45)
        page.insert_textbox(ref_rect, ref, fontsize=9, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
        y_pos += 48

    # Set metadata
    doc.set_metadata({
        "title": "On the Convergence Properties of Stochastic Gradient Methods in Deep Learning",
        "author": "Elena Kowalski, James Harrington, Mei-Ling Zhou",
        "subject": "Optimization, Deep Learning, Convergence Analysis",
        "keywords": "SGD, Adam, convergence, non-convex optimization, deep learning",
        "creator": "LaTeX",
        "producer": "PyMuPDF",
    })

    # Set TOC
    toc = [
        [1, "Abstract", 1],
        [1, "1. Introduction", 2],
        [1, "2. Theoretical Framework", 3],
        [1, "3. Extension to Adaptive Methods", 4],
        [1, "4. Experimental Setup", 5],
        [1, "5. Experimental Results", 6],
        [1, "6. Analysis and Discussion", 7],
        [1, "7. Related Work", 8],
        [1, "8. Conclusion", 9],
        [1, "References", 10],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
