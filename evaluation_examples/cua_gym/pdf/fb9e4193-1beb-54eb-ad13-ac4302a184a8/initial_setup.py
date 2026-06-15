"""
Initial Setup: Create an 11-page mathematics paper PDF with equations on pages 3-8.
Task ID: pdf_res_029
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_029'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/math_paper.pdf'

# Page dimensions
W, H = 595, 842  # A4

# Layout constants
LEFT_MARGIN = 72
RIGHT_MARGIN = 523
TOP_START = 80
LINE_HEIGHT = 14
EQ_FONTSIZE = 12
BODY_FONTSIZE = 11
HEADING_FONTSIZE = 16
SUBHEADING_FONTSIZE = 13


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


def insert_wrapped_text(page, x, y, text, fontsize=BODY_FONTSIZE, fontname="helv", color=(0, 0, 0), max_width=None):
    """Insert text that wraps within margins. Returns new y position."""
    if max_width is None:
        max_width = RIGHT_MARGIN - LEFT_MARGIN
    rect = pymupdf.Rect(x, y, x + max_width, H - 50)
    excess = page.insert_textbox(
        rect, text,
        fontsize=fontsize,
        fontname=fontname,
        color=color,
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    # Estimate lines used
    avg_char_width = fontsize * 0.5
    chars_per_line = max_width / avg_char_width
    num_lines = max(1, len(text) / chars_per_line)
    return y + num_lines * (fontsize + 3)


def insert_centered_text(page, y, text, fontsize=BODY_FONTSIZE, fontname="helv", color=(0, 0, 0)):
    """Insert centered text. Returns new y position."""
    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, y + fontsize + 8)
    page.insert_textbox(
        rect, text,
        fontsize=fontsize,
        fontname=fontname,
        color=color,
        align=pymupdf.TEXT_ALIGN_CENTER,
    )
    return y + fontsize + 10


def insert_heading(page, y, text, fontsize=HEADING_FONTSIZE):
    """Insert a bold heading. Returns new y."""
    rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, y + fontsize + 8)
    page.insert_textbox(rect, text, fontsize=fontsize, fontname="hebo", color=(0, 0, 0))
    return y + fontsize + 14


def insert_equation(page, y, equation_text, label=None):
    """Insert a centered 'equation' (simulated with text). Returns new y."""
    # Equation with some vertical spacing
    y += 8
    eq_display = equation_text
    if label:
        eq_display = f"{equation_text}    ({label})"
    rect = pymupdf.Rect(LEFT_MARGIN + 40, y, RIGHT_MARGIN - 40, y + EQ_FONTSIZE + 8)
    page.insert_textbox(
        rect, eq_display,
        fontsize=EQ_FONTSIZE,
        fontname="tiit",  # Times-Italic for math look
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )
    return y + EQ_FONTSIZE + 18


def insert_body(page, y, text):
    """Insert body paragraph text. Returns new y."""
    return insert_wrapped_text(page, LEFT_MARGIN, y, text, fontsize=BODY_FONTSIZE)


def create_initial():
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ============= PAGE 1: Title Page =============
    p = doc.new_page(width=W, height=H)
    y = 150
    y = insert_centered_text(p, y, "On the Convergence Properties of Stochastic Gradient Methods", fontsize=20, fontname="tibo")
    y += 10
    y = insert_centered_text(p, y, "in Non-Convex Optimization Landscapes", fontsize=18, fontname="tibo")
    y += 30
    y = insert_centered_text(p, y, "Elena Kuznetsova, Rajesh Patel, and Yuki Tanaka", fontsize=13, fontname="helv")
    y += 5
    y = insert_centered_text(p, y, "Department of Applied Mathematics", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    y = insert_centered_text(p, y, "Pacific Institute of Mathematical Sciences", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    y += 20
    y = insert_centered_text(p, y, "March 2026", fontsize=11, fontname="heit")
    y += 40
    y = insert_heading(p, y, "Abstract", fontsize=14)
    y = insert_body(p, y,
        "We study the convergence behavior of stochastic gradient descent (SGD) and its "
        "variants when applied to non-convex optimization problems arising in deep learning "
        "and statistical estimation. Our main contribution is a unified framework that "
        "establishes convergence rates under relaxed smoothness assumptions, extending "
        "classical results that required global Lipschitz continuity of gradients. We prove "
        "that under a local smoothness condition and bounded variance, SGD with appropriately "
        "chosen step sizes achieves an iteration complexity of O(1/epsilon^2) for finding "
        "approximate first-order stationary points. Furthermore, we demonstrate that "
        "momentum-based methods can improve this rate under additional structural assumptions "
        "on the loss landscape. Our theoretical findings are validated through extensive "
        "numerical experiments on benchmark optimization problems."
    )
    y += 15
    p.insert_text(pymupdf.Point(LEFT_MARGIN, y), "Keywords: ", fontsize=11, fontname="hebo")
    p.insert_text(pymupdf.Point(LEFT_MARGIN + 65, y), "stochastic optimization, non-convex analysis, convergence rates, deep learning", fontsize=11, fontname="heit")

    # ============= PAGE 2: Introduction =============
    p = doc.new_page(width=W, height=H)
    y = TOP_START
    y = insert_heading(p, y, "1. Introduction")
    y = insert_body(p, y,
        "Optimization lies at the heart of modern machine learning. The training of neural "
        "networks, kernel methods, and generative models all reduce to minimizing a loss "
        "function over high-dimensional parameter spaces. While convex optimization provides "
        "a well-understood theoretical foundation with strong convergence guarantees, the "
        "objective functions encountered in practice are typically non-convex, exhibiting "
        "complex landscapes with saddle points, local minima, and flat regions."
    )
    y += 8
    y = insert_body(p, y,
        "Despite these challenges, first-order stochastic methods such as SGD and Adam "
        "have proven remarkably effective in practice, often converging to solutions with "
        "excellent generalization properties. Understanding why these methods succeed has "
        "been a central question in optimization theory over the past decade. Classical "
        "convergence analyses rely on assumptions such as global Lipschitz smoothness and "
        "bounded gradients, which are known to be violated in many practical settings."
    )
    y += 8
    y = insert_body(p, y,
        "In this paper, we develop a refined convergence theory that accommodates local "
        "smoothness conditions, a strictly weaker assumption than global Lipschitz continuity. "
        "Our framework unifies and extends several existing results, providing tighter bounds "
        "for both vanilla SGD and momentum-based variants. The key insight is that the "
        "smoothness constant can be replaced by a local quantity that depends on the current "
        "iterate, leading to adaptive convergence rates that better reflect practical behavior."
    )
    y += 8
    y = insert_body(p, y,
        "The remainder of this paper is organized as follows. Section 2 reviews the "
        "mathematical preliminaries and establishes notation. Section 3 presents our main "
        "convergence results for SGD under local smoothness. Section 4 extends the analysis "
        "to momentum methods. Section 5 contains numerical experiments, and Section 6 "
        "concludes with a discussion of open problems."
    )

    # ============= PAGE 3: Preliminaries (first page with equations) =============
    p = doc.new_page(width=W, height=H)
    y = TOP_START
    y = insert_heading(p, y, "2. Mathematical Preliminaries")
    y = insert_body(p, y,
        "We consider the unconstrained optimization problem of minimizing a continuously "
        "differentiable function f: R^d -> R. The standard formulation in machine learning "
        "is the empirical risk minimization problem:"
    )
    y = insert_equation(p, y, "min_{x in R^d} f(x) = (1/n) sum_{i=1}^{n} f_i(x)", "2.1")
    y = insert_body(p, y,
        "where each f_i corresponds to the loss on the i-th data sample. When n is large, "
        "computing the full gradient is prohibitively expensive, motivating the use of "
        "stochastic approximations. At each iteration k, we sample a mini-batch B_k and "
        "compute the stochastic gradient:"
    )
    y = insert_equation(p, y, "g_k = (1/|B_k|) sum_{i in B_k} nabla f_i(x_k)", "2.2")
    y += 5
    y = insert_body(p, y,
        "The standard SGD update rule with step size eta_k is given by:"
    )
    y = insert_equation(p, y, "x_{k+1} = x_k - eta_k * g_k", "2.3")
    y += 5
    y = insert_heading(p, y, "2.1 Smoothness Assumptions", fontsize=SUBHEADING_FONTSIZE)
    y = insert_body(p, y,
        "A function f is said to be L-smooth if its gradient is Lipschitz continuous with "
        "constant L > 0. Formally, for all x, y in R^d:"
    )
    y = insert_equation(p, y, "||nabla f(x) - nabla f(y)|| <= L ||x - y||", "2.4")
    y += 5
    y = insert_body(p, y,
        "This condition is equivalent to the following descent lemma, which serves as the "
        "cornerstone of most convergence analyses:"
    )
    y = insert_equation(p, y, "f(y) <= f(x) + <nabla f(x), y - x> + (L/2)||y - x||^2", "2.5")

    # ============= PAGE 4: More theory =============
    p = doc.new_page(width=W, height=H)
    y = TOP_START
    y = insert_heading(p, y, "2.2 Variance Conditions", fontsize=SUBHEADING_FONTSIZE)
    y = insert_body(p, y,
        "We require that the stochastic gradient is an unbiased estimator of the true "
        "gradient with bounded variance. Specifically, we assume:"
    )
    y = insert_equation(p, y, "E[g_k | x_k] = nabla f(x_k)", "2.6")
    y = insert_equation(p, y, "E[||g_k - nabla f(x_k)||^2 | x_k] <= sigma^2", "2.7")
    y += 5
    y = insert_body(p, y,
        "where sigma^2 > 0 is the variance bound. The unbiasedness condition (2.6) ensures "
        "that SGD moves in the correct direction on average, while the bounded variance "
        "condition (2.7) controls the noise introduced by stochastic sampling. In some "
        "settings, we employ the relaxed growth condition:"
    )
    y = insert_equation(p, y, "E[||g_k||^2 | x_k] <= A||nabla f(x_k)||^2 + B", "2.8")
    y += 5
    y = insert_body(p, y,
        "for constants A >= 1 and B >= 0. This condition is weaker than bounded variance "
        "when the gradient norm is large, and is satisfied by many practical loss functions "
        "including cross-entropy and mean squared error losses."
    )
    y += 8
    y = insert_heading(p, y, "3. Main Convergence Results", fontsize=HEADING_FONTSIZE)
    y = insert_body(p, y,
        "We now present our main convergence theorem for SGD under the local smoothness "
        "assumption. The result establishes that SGD finds epsilon-approximate stationary "
        "points with high probability."
    )

    # ============= PAGE 5: Theorem and proof =============
    p = doc.new_page(width=W, height=H)
    y = TOP_START
    y = insert_heading(p, y, "Theorem 3.1 (Convergence of SGD)", fontsize=SUBHEADING_FONTSIZE)
    y = insert_body(p, y,
        "Let f satisfy the local smoothness condition with parameter L(x), and let the "
        "stochastic gradient satisfy conditions (2.6)-(2.7). Suppose the step size sequence "
        "satisfies eta_k = c / sqrt(K) for some constant c > 0. Then after K iterations:"
    )
    y = insert_equation(p, y, "(1/K) sum_{k=0}^{K-1} E[||nabla f(x_k)||^2] <= 2(f(x_0) - f*) / (c*sqrt(K)) + c*L*sigma^2 / sqrt(K)", "3.1")
    y += 5
    y = insert_body(p, y,
        "Choosing c = sqrt(2(f(x_0) - f*) / (L * sigma^2)) yields the optimal rate:"
    )
    y = insert_equation(p, y, "min_{0<=k<K} E[||nabla f(x_k)||^2] <= 2 * sqrt(2L*sigma^2*(f(x_0) - f*)) / sqrt(K)", "3.2")
    y += 5
    y = insert_body(p, y,
        "Proof. We begin by applying the descent lemma (2.5) with y = x_{k+1} and x = x_k. "
        "Substituting the SGD update (2.3), we obtain:"
    )
    y = insert_equation(p, y, "f(x_{k+1}) <= f(x_k) - eta_k <nabla f(x_k), g_k> + (L*eta_k^2/2)||g_k||^2", "3.3")
    y += 5
    y = insert_body(p, y,
        "Taking conditional expectation with respect to x_k and using the unbiasedness "
        "condition (2.6):"
    )
    y = insert_equation(p, y, "E[f(x_{k+1}) | x_k] <= f(x_k) - eta_k ||nabla f(x_k)||^2 + (L*eta_k^2/2)(||nabla f(x_k)||^2 + sigma^2)", "3.4")
    y += 5
    y = insert_body(p, y,
        "Rearranging and summing from k = 0 to K-1, we arrive at the stated bound. The "
        "optimal choice of c balances the two terms in the upper bound."
    )

    # ============= PAGE 6: Extensions =============
    p = doc.new_page(width=W, height=H)
    y = TOP_START
    y = insert_heading(p, y, "3.2 Convergence with Diminishing Step Sizes", fontsize=SUBHEADING_FONTSIZE)
    y = insert_body(p, y,
        "An alternative approach uses diminishing step sizes of the form eta_k = alpha / (k + beta) "
        "for suitable constants alpha, beta > 0. Under this schedule, we obtain the following "
        "complementary result."
    )
    y += 5
    y = insert_heading(p, y, "Corollary 3.2", fontsize=SUBHEADING_FONTSIZE)
    y = insert_body(p, y,
        "Under the conditions of Theorem 3.1, with eta_k = alpha/(k+beta) where alpha > 1/(2L) "
        "and beta is chosen so that eta_0 <= 1/L, the iterates satisfy:"
    )
    y = insert_equation(p, y, "min_{0<=k<K} E[||nabla f(x_k)||^2] = O(log(K) / K)", "3.5")
    y += 5
    y = insert_body(p, y,
        "This rate is slightly worse than the O(1/sqrt(K)) rate of Theorem 3.1, but has "
        "the advantage of not requiring knowledge of the total iteration count K in advance. "
        "The proof follows a similar telescoping argument but requires more careful treatment "
        "of the step size sums."
    )
    y += 10
    y = insert_heading(p, y, "4. Momentum Methods", fontsize=HEADING_FONTSIZE)
    y = insert_body(p, y,
        "We now extend our analysis to momentum-based methods. The heavy-ball method "
        "introduces an additional momentum term to accelerate convergence:"
    )
    y = insert_equation(p, y, "v_{k+1} = beta * v_k + g_k", "4.1")
    y = insert_equation(p, y, "x_{k+1} = x_k - eta_k * v_{k+1}", "4.2")

    # ============= PAGE 7: More momentum =============
    p = doc.new_page(width=W, height=H)
    y = TOP_START
    y = insert_body(p, y,
        "where beta in [0, 1) is the momentum coefficient and v_0 = 0. The momentum "
        "variable v_k accumulates a weighted average of past gradients, providing a form "
        "of variance reduction that can improve convergence in favorable settings."
    )
    y += 5
    y = insert_heading(p, y, "Theorem 4.1 (Convergence with Momentum)", fontsize=SUBHEADING_FONTSIZE)
    y = insert_body(p, y,
        "Under the assumptions of Theorem 3.1 and with beta = 1 - 1/sqrt(K), the heavy-ball "
        "method satisfies:"
    )
    y = insert_equation(p, y, "min_{0<=k<K} E[||nabla f(x_k)||^2] <= C_1 / K^{2/3} + C_2 * sigma^2 / sqrt(K)", "4.3")
    y += 5
    y = insert_body(p, y,
        "where C_1 and C_2 depend on L, f(x_0) - f*, and the momentum parameter. This "
        "represents an improvement over vanilla SGD when the gradient variance sigma^2 is "
        "small relative to the optimization error f(x_0) - f*."
    )
    y += 8
    y = insert_body(p, y,
        "The Nesterov-style accelerated gradient method modifies the update by evaluating "
        "the gradient at an extrapolated point:"
    )
    y = insert_equation(p, y, "y_k = x_k + beta_k * (x_k - x_{k-1})", "4.4")
    y = insert_equation(p, y, "x_{k+1} = y_k - eta_k * nabla f(y_k)", "4.5")
    y += 5
    y = insert_body(p, y,
        "While Nesterov acceleration provides optimal rates in the convex setting, its "
        "behavior in non-convex optimization is more subtle. Recent work has shown that "
        "careful tuning of the momentum schedule beta_k can lead to improved convergence "
        "near saddle points."
    )

    # ============= PAGE 8: Adam and experiments intro =============
    p = doc.new_page(width=W, height=H)
    y = TOP_START
    y = insert_heading(p, y, "4.2 Adaptive Methods", fontsize=SUBHEADING_FONTSIZE)
    y = insert_body(p, y,
        "The Adam optimizer combines momentum with adaptive learning rates, maintaining "
        "estimates of both the first and second moments of the gradient:"
    )
    y = insert_equation(p, y, "m_{k+1} = beta_1 * m_k + (1 - beta_1) * g_k", "4.6")
    y = insert_equation(p, y, "v_{k+1} = beta_2 * v_k + (1 - beta_2) * g_k^2", "4.7")
    y = insert_equation(p, y, "x_{k+1} = x_k - eta * m_{k+1} / (sqrt(v_{k+1}) + epsilon)", "4.8")
    y += 5
    y = insert_body(p, y,
        "The convergence analysis of Adam is considerably more delicate due to the "
        "interaction between the momentum and variance tracking terms. Under suitable "
        "conditions on beta_1, beta_2, and epsilon, we establish:"
    )
    y += 5
    y = insert_heading(p, y, "Theorem 4.2 (Convergence of Adam)", fontsize=SUBHEADING_FONTSIZE)
    y = insert_body(p, y,
        "Let beta_1 < sqrt(beta_2) and eta <= epsilon * sqrt(1 - beta_2) / (1 - beta_1). "
        "Then the Adam iterates satisfy:"
    )
    y = insert_equation(p, y, "min_{0<=k<K} E[||nabla f(x_k)||^2] <= O(d * log(K) / sqrt(K))", "4.9")
    y += 5
    y = insert_body(p, y,
        "where d is the parameter dimension. The logarithmic factor and dimension "
        "dependence are artifacts of the proof technique and may not be tight. Closing "
        "this gap remains an important open problem."
    )

    # ============= PAGE 9: Numerical experiments =============
    p = doc.new_page(width=W, height=H)
    y = TOP_START
    y = insert_heading(p, y, "5. Numerical Experiments")
    y = insert_body(p, y,
        "We validate our theoretical results through experiments on three benchmark problems: "
        "(i) training a two-layer neural network on MNIST, (ii) minimizing the Rosenbrock "
        "function in d = 100 dimensions, and (iii) logistic regression on the CIFAR-10 "
        "feature dataset. All experiments are repeated 10 times with different random seeds."
    )
    y += 8
    y = insert_heading(p, y, "5.1 Two-Layer Neural Network", fontsize=SUBHEADING_FONTSIZE)
    y = insert_body(p, y,
        "We train a fully connected network with 256 hidden units and ReLU activations on "
        "the MNIST handwritten digit dataset. The network is trained using SGD, Heavy-Ball, "
        "and Adam with step sizes tuned by grid search over {0.001, 0.01, 0.05, 0.1}. "
        "Training loss convergence is measured over 50 epochs with batch size 128."
    )
    y += 8
    y = insert_body(p, y,
        "Results confirm our theoretical predictions. SGD with constant step size eta = 0.05 "
        "achieves the best final training loss of 0.0234, while Heavy-Ball with beta = 0.9 "
        "reaches comparable performance (0.0241) with faster initial progress. Adam with "
        "default parameters (beta_1 = 0.9, beta_2 = 0.999) achieves 0.0228 but exhibits "
        "more variance across runs."
    )
    y += 8
    y = insert_heading(p, y, "5.2 Rosenbrock Function", fontsize=SUBHEADING_FONTSIZE)
    y = insert_body(p, y,
        "The Rosenbrock function f(x) = sum_{i=1}^{d-1} [100(x_{i+1} - x_i^2)^2 + (1 - x_i)^2] "
        "provides a challenging non-convex test case with a narrow curved valley. We compare "
        "convergence rates for d = 100 starting from x_0 = (-1, ..., -1). All methods "
        "are run for 10^5 iterations."
    )

    # ============= PAGE 10: More experiments =============
    p = doc.new_page(width=W, height=H)
    y = TOP_START
    y = insert_heading(p, y, "5.3 Logistic Regression", fontsize=SUBHEADING_FONTSIZE)
    y = insert_body(p, y,
        "For the logistic regression experiment, we extract 512-dimensional features from "
        "a pre-trained ResNet-18 and fit a multinomial logistic regression model on CIFAR-10. "
        "This provides a near-convex setting where our bounds are expected to be tightest."
    )
    y += 8
    y = insert_body(p, y,
        "Table 1 summarizes the convergence metrics across all experiments. The columns "
        "report the average number of iterations to reach epsilon-stationarity for "
        "epsilon = 0.01, along with standard deviations."
    )
    y += 8
    # Insert a simple table
    y = insert_centered_text(p, y, "Table 1: Iterations to Epsilon-Stationarity (x 10^3)", fontsize=11, fontname="hebo")
    y += 5
    table_data = [
        ["Method", "MNIST", "Rosenbrock", "CIFAR-10"],
        ["SGD", "12.4 +/- 1.2", "87.3 +/- 5.6", "8.1 +/- 0.9"],
        ["Heavy-Ball", "9.8 +/- 1.5", "63.2 +/- 4.1", "7.2 +/- 0.7"],
        ["Adam", "8.5 +/- 2.1", "71.8 +/- 6.3", "6.9 +/- 1.1"],
    ]
    for row_i, row in enumerate(table_data):
        for col_i, cell in enumerate(row):
            x = LEFT_MARGIN + col_i * 115
            fn = "hebo" if row_i == 0 else "helv"
            p.insert_text(pymupdf.Point(x, y + 12), cell, fontsize=10, fontname=fn)
        y += 16
    # Draw table lines
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(LEFT_MARGIN, y - 16 * len(table_data) - 2), pymupdf.Point(LEFT_MARGIN + 460, y - 16 * len(table_data) - 2))
    shape.draw_line(pymupdf.Point(LEFT_MARGIN, y - 16 * (len(table_data) - 1) - 2), pymupdf.Point(LEFT_MARGIN + 460, y - 16 * (len(table_data) - 1) - 2))
    shape.draw_line(pymupdf.Point(LEFT_MARGIN, y - 2), pymupdf.Point(LEFT_MARGIN + 460, y - 2))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()

    y += 15
    y = insert_body(p, y,
        "The results are consistent with our theoretical analysis. Momentum methods "
        "consistently outperform vanilla SGD, with the improvement being most pronounced "
        "on the highly non-convex Rosenbrock problem. Adam shows competitive performance "
        "but with higher variance, as predicted by the dimension-dependent bound in Theorem 4.2."
    )

    # ============= PAGE 11: Conclusion & References =============
    p = doc.new_page(width=W, height=H)
    y = TOP_START
    y = insert_heading(p, y, "6. Conclusion")
    y = insert_body(p, y,
        "We have presented a unified convergence framework for stochastic gradient methods "
        "in non-convex optimization under local smoothness assumptions. Our results extend "
        "classical convergence theory to more realistic settings and provide practical guidance "
        "for step size selection and momentum tuning."
    )
    y += 8
    y = insert_body(p, y,
        "Several directions remain for future work. First, extending the local smoothness "
        "framework to second-order methods could yield improved convergence near saddle points. "
        "Second, the dimension dependence in the Adam convergence bound (Theorem 4.2) may be "
        "an artifact of the analysis and deserves further investigation. Finally, connecting "
        "our convergence rates to generalization bounds would provide a more complete picture "
        "of the training dynamics."
    )
    y += 15
    y = insert_heading(p, y, "References")
    refs = [
        "[1] Bottou, L., Curtis, F. E., and Nocedal, J. Optimization Methods for Large-Scale Machine Learning. SIAM Review, 60(2):223-311, 2018.",
        "[2] Ghadimi, S. and Lan, G. Stochastic First- and Zeroth-Order Methods for Nonconvex Stochastic Programming. SIAM Journal on Optimization, 23(4):2341-2368, 2013.",
        "[3] Kingma, D. P. and Ba, J. Adam: A Method for Stochastic Optimization. Proceedings of ICLR, 2015.",
        "[4] Nesterov, Y. Introductory Lectures on Convex Optimization: A Basic Course. Springer, 2004.",
        "[5] Reddi, S. J., Kale, S., and Kumar, S. On the Convergence of Adam and Beyond. Proceedings of ICLR, 2018.",
        "[6] Robbins, H. and Monro, S. A Stochastic Approximation Method. Annals of Mathematical Statistics, 22(3):400-407, 1951.",
        "[7] Polyak, B. T. Some Methods of Speeding Up the Convergence of Iteration Methods. USSR Computational Mathematics and Mathematical Physics, 4(5):1-17, 1964.",
        "[8] Zhang, J., He, T., Sra, S., and Jadbabaie, A. Why Gradient Clipping Accelerates Training: A Theoretical Justification for Adaptivity. Proceedings of ICLR, 2020.",
    ]
    for ref in refs:
        rect = pymupdf.Rect(LEFT_MARGIN, y, RIGHT_MARGIN, y + 30)
        p.insert_textbox(rect, ref, fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 28

    # Set metadata
    doc.set_metadata({
        "title": "On the Convergence Properties of Stochastic Gradient Methods in Non-Convex Optimization Landscapes",
        "author": "Elena Kuznetsova, Rajesh Patel, Yuki Tanaka",
        "subject": "Stochastic Optimization",
        "keywords": "SGD, convergence, non-convex, momentum, Adam",
    })

    # Set table of contents
    toc = [
        [1, "Abstract", 1],
        [1, "1. Introduction", 2],
        [1, "2. Mathematical Preliminaries", 3],
        [2, "2.1 Smoothness Assumptions", 3],
        [2, "2.2 Variance Conditions", 4],
        [1, "3. Main Convergence Results", 4],
        [1, "4. Momentum Methods", 6],
        [2, "4.2 Adaptive Methods", 8],
        [1, "5. Numerical Experiments", 9],
        [1, "6. Conclusion", 11],
        [1, "References", 11],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 11')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
