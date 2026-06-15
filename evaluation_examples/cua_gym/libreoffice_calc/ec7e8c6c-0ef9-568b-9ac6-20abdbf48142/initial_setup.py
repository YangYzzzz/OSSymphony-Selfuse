"""
Initial Setup: NeurIPS RL paper PDF open on Desktop; Chrome available but not navigated.
Task ID: osworld_multi_apps_paper_scholar_browse_002
Domain: multi_apps (PDF + Chrome)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_paper_scholar_browse_002'
OUTPUT_PDF = f'{WORKDIR}/Desktop/{TASK_ID}.pdf'


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


def create_paper_pdf():
    """Create a realistic NeurIPS RL paper PDF with a corresponding author footnote."""
    try:
        from fpdf import FPDF
    except ImportError:
        subprocess.run(['pip3', 'install', 'fpdf2'], check=True)
        from fpdf import FPDF

    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # --- Title ---
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_xy(20, 20)
    pdf.multi_cell(170, 7,
        'Hierarchical Reinforcement Learning with\nAdaptive Skill Discovery for Continuous Control',
        align='C')

    # --- Conference header ---
    pdf.set_font('Helvetica', '', 10)
    pdf.set_xy(20, 40)
    pdf.cell(170, 5, '37th Conference on Neural Information Processing Systems (NeurIPS 2023)', align='C')

    # --- Authors ---
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_xy(20, 52)
    pdf.cell(170, 6,
        'Michael A. Torres\u00b9   Yuhan Li\u00b2   Priya Nair\u00b9   Sergey Levine\u00b9*   Chelsea Finn\u00b9',
        align='C')

    # --- Affiliations ---
    pdf.set_font('Helvetica', '', 9)
    pdf.set_xy(20, 62)
    pdf.cell(170, 5, '\u00b9University of California, Berkeley   \u00b2Carnegie Mellon University', align='C')

    # --- Horizontal rule ---
    pdf.set_draw_color(150, 150, 150)
    pdf.line(20, 72, 190, 72)

    # --- Abstract heading ---
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_xy(20, 76)
    pdf.cell(170, 6, 'Abstract', align='C')

    # --- Abstract body ---
    pdf.set_font('Helvetica', '', 9)
    pdf.set_xy(20, 84)
    abstract = (
        'We present HRL-ASD, a hierarchical reinforcement learning framework that automatically '
        'discovers reusable skills from raw interaction data. Unlike prior methods that rely on '
        'predefined skill libraries or handcrafted reward shaping, HRL-ASD leverages a '
        'mutual information objective to identify temporally-extended behaviors that are both '
        'diverse and useful for downstream task completion. Our high-level policy learns to '
        'compose discovered skills through goal-conditioned subgoal generation, while a low-level '
        'policy executes each skill with dense intrinsic rewards. We evaluate HRL-ASD on a suite '
        'of challenging continuous control benchmarks from DeepMind Control Suite and AntMaze, '
        'demonstrating consistent improvements over flat RL baselines and prior hierarchical '
        'methods. On AntMaze-Large, HRL-ASD achieves 78.4% success rate compared to 51.2% for '
        'the strongest baseline. We further show that discovered skills transfer across tasks, '
        'reducing sample complexity by up to 3.1x on held-out downstream environments.'
    )
    pdf.multi_cell(170, 5, abstract)

    # --- Section 1 ---
    current_y = pdf.get_y() + 6
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_xy(20, current_y)
    pdf.cell(170, 6, '1  Introduction')
    pdf.ln(6)

    pdf.set_font('Helvetica', '', 9)
    intro = (
        'Hierarchical reinforcement learning (HRL) offers a principled framework for solving '
        'long-horizon tasks by decomposing them into manageable subtasks [1, 2]. A central '
        'challenge in HRL is the skill discovery problem: how to automatically identify a set '
        'of primitives that are both general enough to transfer across contexts and specific '
        'enough to be individually learnable. Recent advances in unsupervised skill discovery '
        'have produced algorithms capable of learning diverse behaviors without task rewards [3, 4], '
        'yet these methods often fail to align discovered skills with the structure of downstream '
        'tasks.\n\n'
        'In this work, we propose HRL-ASD, which addresses this misalignment by jointly '
        'optimizing skill diversity and task utility. Our key insight is that skills should '
        'be discovered in a task-agnostic phase but evaluated and pruned based on their '
        'coverage of states relevant to the target task distribution. This leads to a compact '
        'skill library that is both interpretable and sample-efficient during downstream learning.\n\n'
        'Our contributions are: (1) a novel skill discovery objective that combines diversity '
        'maximization with task-relevant state coverage; (2) a hierarchical policy architecture '
        'that supports smooth skill transitions via a learned interpolation mechanism; '
        '(3) comprehensive empirical evaluation across 12 continuous control tasks.'
    )
    pdf.set_xy(20, pdf.get_y())
    pdf.multi_cell(170, 5, intro)

    # --- Section 2 ---
    current_y = pdf.get_y() + 6
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_xy(20, current_y)
    pdf.cell(170, 6, '2  Related Work')
    pdf.ln(6)

    pdf.set_font('Helvetica', '', 9)
    related = (
        'Options framework [5] provided the theoretical foundation for temporally-extended '
        'actions in MDPs. DIAYN [6] learns diverse skills via mutual information maximization. '
        'HIRO [7] trains a hierarchical agent with learned subgoal representations. '
        'Director [8] uses a world model to plan over abstract goals. Our work builds on '
        'these foundations while introducing task-aware skill pruning and smooth interpolation.'
    )
    pdf.set_xy(20, pdf.get_y())
    pdf.multi_cell(170, 5, related)

    # --- Footer with corresponding author note ---
    # Place footnote at bottom of page
    pdf.set_y(-30)
    pdf.set_draw_color(100, 100, 100)
    pdf.line(20, pdf.get_y(), 100, pdf.get_y())
    pdf.ln(1)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_x(20)
    pdf.multi_cell(170, 4,
        '*Corresponding author: Sergey Levine <svlevine@eecs.berkeley.edu>\n'
        'Preprint. Under review.')

    # --- Page 2 ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_xy(20, 20)
    pdf.cell(170, 6, '3  Method')
    pdf.ln(8)

    pdf.set_font('Helvetica', '', 9)
    method = (
        '3.1  Skill Discovery Phase\n\n'
        'Given an environment with state space S and action space A, we define a skill as a '
        'temporally-extended policy z : S x Z -> A parameterized by a latent code z in Z. '
        'We maximize the mutual information I(S_T ; z) where S_T is the terminal state reached '
        'after executing skill z from initial state s_0. This objective encourages each skill '
        'to reliably reach distinct regions of state space.\n\n'
        '3.2  Task-Aware Pruning\n\n'
        'After the unsupervised phase, we prune skills whose terminal state distributions '
        'have negligible overlap with the empirical state distribution of the target task. '
        'Specifically, we retain skill z_i if KL(p(S|z_i) || p_task(S)) < threshold. '
        'This yields a compact skill set of size K << |Z|.\n\n'
        '3.3  Hierarchical Policy\n\n'
        'The high-level policy selects a skill index and a duration at each meta-timestep. '
        'The low-level policy executes the selected skill with an additional intrinsic reward '
        'proportional to the probability under the skill distribution.'
    )
    pdf.set_xy(20, pdf.get_y())
    pdf.multi_cell(170, 5, method)

    # References
    current_y = pdf.get_y() + 8
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_xy(20, current_y)
    pdf.cell(170, 6, 'References')
    pdf.ln(6)

    pdf.set_font('Helvetica', '', 8)
    refs = (
        '[1] Sutton, R. et al. Between MDPs and semi-MDPs: A framework for temporal abstraction. '
        'Artificial Intelligence, 1999.\n'
        '[2] Dayan, P. & Hinton, G. Feudal reinforcement learning. NeurIPS, 1992.\n'
        '[3] Eysenbach, B., Gupta, A., Ibarz, J., & Levine, S. Diversity is all you need: '
        'Learning skills without a reward function. ICLR, 2019.\n'
        '[4] Sharma, A., Gu, S., Levine, S., Kumar, V., & Hausman, K. Dynamics-aware unsupervised '
        'discovery of skills. ICLR, 2020.\n'
        '[5] Precup, D. Temporal abstraction in reinforcement learning. PhD thesis, 2000.\n'
        '[6] Eysenbach, B. et al. DIAYN: Diversity is all you need. ICLR 2019.\n'
        '[7] Nachum, O., Gu, S., Lee, H., & Levine, S. Data-efficient hierarchical reinforcement '
        'learning. NeurIPS, 2018.\n'
        '[8] Hafner, D., Lillicrap, T., Norouzi, M., & Ba, J. Mastering Atari with Discrete '
        'World Models. ICLR, 2021.'
    )
    pdf.set_xy(20, pdf.get_y())
    pdf.multi_cell(170, 4, refs)

    pdf.output(OUTPUT_PDF)
    print(f'PDF created: {OUTPUT_PDF}')


def create_initial():
    create_paper_pdf()

    # Kill any existing PDF viewers and Chrome to start clean
    subprocess.run(['pkill', '-f', 'evince'], capture_output=True)
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    time.sleep(1)

    # Open the PDF with evince (default PDF viewer on Ubuntu)
    launch_gui(f'evince "{OUTPUT_PDF}"', delay_sec=2.5)

    # Launch Chrome with a blank new tab (not navigated to author profile)
    launch_gui('google-chrome --new-window "https://www.google.com"', delay_sec=2.0)

    print('GUI_READY: launched evince PDF viewer and Chrome with DISPLAY=:0')


create_initial()
