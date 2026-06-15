"""
Initial Setup: Academic writing workspace initialization
Task ID: osworld_multi_apps_workspace_init_012
Domain: multi_apps (OS, VSCode, Chrome)

Creates the initial state:
  - ~/Documents/thesis directory with realistic LaTeX project files
  - Desktop is idle; Chrome and VSCode are closed
  - No apps are pre-launched (agent will open them)
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_workspace_init_012'
THESIS_DIR = '/home/user/Documents/thesis'


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


def kill_apps():
    """Ensure Chrome and VSCode are closed before setup."""
    for app in ['chrome', 'chromium', 'code', 'nautilus']:
        subprocess.run(['pkill', '-f', app],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)


def create_thesis_project():
    """Create a realistic LaTeX thesis project in ~/Documents/thesis."""
    os.makedirs(THESIS_DIR, exist_ok=True)

    # Main thesis file
    main_tex = r"""\documentclass[12pt,a4paper]{report}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{natbib}
\usepackage{geometry}
\geometry{margin=1in}

\title{Uncertainty Quantification in Deep Neural Networks:\\
A Bayesian Approach}
\author{Alex Rivera}
\date{\today}

\begin{document}

\maketitle
\tableofcontents

\include{chapters/introduction}
\include{chapters/background}
\include{chapters/methodology}
\include{chapters/experiments}
\include{chapters/conclusion}

\bibliographystyle{plainnat}
\bibliography{references}

\end{document}
"""
    Path(os.path.join(THESIS_DIR, 'main.tex')).write_text(main_tex)

    # Chapters directory
    chapters_dir = os.path.join(THESIS_DIR, 'chapters')
    os.makedirs(chapters_dir, exist_ok=True)

    # Introduction chapter
    intro_tex = r"""\chapter{Introduction}
\label{chap:introduction}

Deep neural networks (DNNs) have demonstrated remarkable performance across a
wide range of tasks, including image recognition \citep{he2016deep}, natural
language processing \citep{vaswani2017attention}, and scientific discovery
\citep{jumper2021alphafold}. Despite these advances, a critical limitation
remains: standard DNNs provide point estimates without quantifying the
uncertainty of their predictions.

\section{Motivation}

Uncertainty quantification (UQ) is essential in high-stakes applications such
as medical diagnosis, autonomous driving, and climate modeling. A model that
returns a confident but incorrect prediction can be more dangerous than one
that correctly signals low confidence. This thesis investigates Bayesian
methods for UQ in DNNs.

\section{Research Questions}

This thesis addresses the following questions:
\begin{enumerate}
    \item How can Bayesian inference be efficiently applied to large-scale DNNs?
    \item What are the trade-offs between accuracy and uncertainty calibration?
    \item How do different approximate inference methods compare in practice?
\end{enumerate}

\section{Thesis Structure}

Chapter~\ref{chap:background} reviews related work. Chapter~\ref{chap:methodology}
describes our proposed method. Chapter~\ref{chap:experiments} presents experimental
results. Chapter~\ref{chap:conclusion} concludes with future directions.
"""
    Path(os.path.join(chapters_dir, 'introduction.tex')).write_text(intro_tex)

    # Background chapter
    background_tex = r"""\chapter{Background}
\label{chap:background}

\section{Bayesian Inference}

Bayesian inference provides a principled framework for reasoning under
uncertainty. Given observed data $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^N$,
the posterior distribution over parameters $\theta$ is:

\begin{equation}
p(\theta \mid \mathcal{D}) = \frac{p(\mathcal{D} \mid \theta)\, p(\theta)}{p(\mathcal{D})}
\end{equation}

For neural networks, exact posterior computation is intractable due to the
high dimensionality of $\theta$ and the non-linearity of the model.

\section{Approximate Inference Methods}

Several approximate inference techniques have been proposed:

\subsection{Variational Inference}
Variational inference (VI) approximates the posterior with a tractable
distribution $q_\phi(\theta)$ by minimizing the KL divergence:
\begin{equation}
q^*(\theta) = \argmin_{q \in \mathcal{Q}} \mathrm{KL}(q_\phi(\theta) \,\|\, p(\theta \mid \mathcal{D}))
\end{equation}

\subsection{Monte Carlo Dropout}
\citet{gal2016dropout} showed that training with dropout and sampling at
test time approximates Bayesian inference. This approach scales to large
architectures without modifying the training objective.

\subsection{Deep Ensembles}
\citet{lakshminarayanan2017simple} propose training multiple models with
random initialization and combining predictions. Despite its simplicity,
this approach achieves strong calibration empirically.
"""
    Path(os.path.join(chapters_dir, 'background.tex')).write_text(background_tex)

    # Methodology chapter
    methodology_tex = r"""\chapter{Methodology}
\label{chap:methodology}

\section{Proposed Framework}

We propose a scalable Bayesian framework combining stochastic weight
averaging Gaussian (SWAG) \citep{maddox2019simple} with low-rank
approximations of the posterior covariance.

\section{Model Architecture}

Our base architecture is a ResNet-50 \citep{he2016deep} modified to support
Monte Carlo sampling at inference time. Let $f_\theta: \mathcal{X} \to
\mathcal{Y}$ denote the neural network with parameters $\theta$.

\section{Training Procedure}

Algorithm~\ref{alg:training} summarizes our training procedure.

\begin{enumerate}
    \item Pre-train with standard SGD for $T_0$ epochs.
    \item Switch to cyclic learning rate schedule.
    \item Collect weight snapshots $\{\theta^{(s)}\}_{s=1}^S$ at cycle ends.
    \item Fit Gaussian $q(\theta) = \mathcal{N}(\bar\theta, \Sigma)$ to snapshots.
\end{enumerate}
"""
    Path(os.path.join(chapters_dir, 'methodology.tex')).write_text(methodology_tex)

    # Experiments chapter (placeholder)
    experiments_tex = r"""\chapter{Experiments}
\label{chap:experiments}

\section{Datasets}

We evaluate on three benchmark datasets:
\begin{itemize}
    \item \textbf{CIFAR-10/100}: Standard image classification benchmarks.
    \item \textbf{ImageNet}: Large-scale visual recognition challenge.
    \item \textbf{UCI Regression}: Tabular regression tasks from the UCI repository.
\end{itemize}

\section{Evaluation Metrics}

\begin{itemize}
    \item \textbf{NLL}: Negative log-likelihood (lower is better).
    \item \textbf{ECE}: Expected calibration error \citep{guo2017calibration}.
    \item \textbf{Brier Score}: Combined accuracy and calibration measure.
\end{itemize}

\section{Results}

% TODO: Fill in results table after running experiments
"""
    Path(os.path.join(chapters_dir, 'experiments.tex')).write_text(experiments_tex)

    # Conclusion chapter
    conclusion_tex = r"""\chapter{Conclusion}
\label{chap:conclusion}

\section{Summary}

This thesis investigated Bayesian approaches to uncertainty quantification
in deep neural networks. We demonstrated that our proposed SWAG-LR method
achieves competitive calibration with significantly lower computational
overhead compared to full Bayesian approaches.

\section{Future Work}

Several directions remain open for future research:
\begin{itemize}
    \item Extension to transformer-based architectures for NLP tasks.
    \item Integration with active learning pipelines.
    \item Application to out-of-distribution detection benchmarks.
\end{itemize}
"""
    Path(os.path.join(chapters_dir, 'conclusion.tex')).write_text(conclusion_tex)

    # References BibTeX file
    references_bib = r"""@inproceedings{he2016deep,
  title={Deep residual learning for image recognition},
  author={He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
  booktitle={CVPR},
  pages={770--778},
  year={2016}
}

@inproceedings{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and others},
  booktitle={NeurIPS},
  year={2017}
}

@article{jumper2021alphafold,
  title={Highly accurate protein structure prediction with {AlphaFold}},
  author={Jumper, John and Evans, Richard and Pritzel, Alexander and others},
  journal={Nature},
  volume={596},
  pages={583--589},
  year={2021}
}

@inproceedings{gal2016dropout,
  title={Dropout as a {Bayesian} approximation: Representing model uncertainty in deep learning},
  author={Gal, Yarin and Ghahramani, Zoubin},
  booktitle={ICML},
  year={2016}
}

@inproceedings{lakshminarayanan2017simple,
  title={Simple and scalable predictive uncertainty estimation using deep ensembles},
  author={Lakshminarayanan, Balaji and Pritzel, Alexander and Blundell, Charles},
  booktitle={NeurIPS},
  year={2017}
}

@inproceedings{maddox2019simple,
  title={A simple baseline for {Bayesian} uncertainty in deep learning},
  author={Maddox, Wesley J and Izmailov, Pavel and Garipov, Timur and Vetrov, Dmitry P and Wilson, Andrew Gordon},
  booktitle={NeurIPS},
  year={2019}
}

@inproceedings{guo2017calibration,
  title={On calibration of modern neural networks},
  author={Guo, Chuan and Pleiss, Geoff and Sun, Yu and Weinberger, Kilian Q},
  booktitle={ICML},
  year={2017}
}
"""
    Path(os.path.join(THESIS_DIR, 'references.bib')).write_text(references_bib)

    # Figures directory
    figures_dir = os.path.join(THESIS_DIR, 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    Path(os.path.join(figures_dir, 'README.txt')).write_text(
        'Place thesis figures here (PNG/PDF format).\n'
    )

    # .latexmkrc build config
    latexmkrc = """$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error %O %S';
$bibtex_use = 2;
$clean_full_ext = '%R.aux %R.bbl %R.blg %R.idx %R.ind %R.lof %R.lot %R.out %R.toc %R.acn %R.acr %R.alg %R.glg %R.glo %R.gls %R.ist %R.fls %R.log %R.fdb_latexmk';
"""
    Path(os.path.join(THESIS_DIR, '.latexmkrc')).write_text(latexmkrc)

    # README for the project
    readme = """# PhD Thesis: Uncertainty Quantification in Deep Neural Networks

## Project Structure

```
thesis/
├── main.tex            # Master document
├── references.bib      # Bibliography
├── .latexmkrc          # Build configuration
├── chapters/
│   ├── introduction.tex
│   ├── background.tex
│   ├── methodology.tex
│   ├── experiments.tex
│   └── conclusion.tex
└── figures/            # Figures and plots
```

## Building

```bash
latexmk -pdf main.tex
```

## Notes

- Uses natbib for references
- Compiled with pdflatex
"""
    Path(os.path.join(THESIS_DIR, 'README.md')).write_text(readme)

    print(f'Thesis project created at: {THESIS_DIR}')


def create_initial():
    # 1. Kill any stray apps that should be closed in initial state
    kill_apps()

    # 2. Create ~/Documents/thesis with realistic LaTeX project
    create_thesis_project()

    print(f'Initial state created: {THESIS_DIR} exists with LaTeX project files')
    print('Apps are closed; desktop is idle')
    print('GUI_READY: Initial state set — no apps launched (task requires agent to open them)')


create_initial()
