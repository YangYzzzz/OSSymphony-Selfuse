"""
Initial Setup: Robotics paper review task — open PDF and blank Writer doc
Task ID: osworld_multi_apps_paper_scholar_browse_009
Domain: multi_apps (PDF + LibreOffice Writer + Chrome)

Initial state:
  - A PDF robotics paper at /home/user/osworld_multi_apps_paper_scholar_browse_009.pdf
    containing a robotics manipulation paper with a clearly marked corresponding author
  - A blank LibreOffice Writer document at /home/user/osworld_multi_apps_paper_scholar_browse_009.docx
  - Both opened in their respective apps
  - Chrome available but not pre-navigated
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_paper_scholar_browse_009'
PDF_OUTPUT = f'{WORKDIR}/{TASK_ID}.pdf'
DOCX_OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'


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


def create_pdf():
    """Create a realistic robotics manipulation paper PDF with a marked corresponding author."""
    from fpdf import FPDF, XPos, YPos

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    # Page width for text area
    W = pdf.w - pdf.l_margin - pdf.r_margin

    def heading(text, size=12, style='B'):
        pdf.set_font('Helvetica', style, size)
        pdf.multi_cell(W, size * 0.7, text, align='L',
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)

    def body(text, size=10):
        pdf.set_font('Helvetica', '', size)
        pdf.multi_cell(W, size * 0.65, text, align='J',
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    def center_text(text, size=10, style=''):
        pdf.set_font('Helvetica', style, size)
        pdf.multi_cell(W, size * 0.65, text, align='C',
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Title
    center_text(
        'Adaptive Grasp Planning for Unstructured Environments\n'
        'Using Hierarchical Reinforcement Learning',
        size=16, style='B')
    pdf.ln(3)

    # Authors line
    center_text('Wei-Lin Chen1, Soo-Jin Park2, Yuki Tanaka3*, Marcus Rodriguez1', size=11)
    pdf.ln(1)

    # Affiliations
    pdf.set_font('Helvetica', 'I', 9)
    pdf.multi_cell(W, 5, (
        '1 Stanford University Robotics Lab, Stanford, CA, USA\n'
        '2 KAIST Intelligent Systems Lab, Daejeon, South Korea\n'
        '3 University of Tokyo, Dept. of Mechano-Informatics, Tokyo, Japan'
    ), align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)

    # Corresponding author note
    pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(W, 5,
        '*Corresponding author: ytanaka@mechano.t.u-tokyo.ac.jp',
        align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    # Abstract
    heading('Abstract', size=11)
    body(
        'We present a novel framework for adaptive robotic grasping in cluttered and '
        'unstructured environments. Our approach combines hierarchical reinforcement learning '
        'with a learned grasp quality estimator to enable robust manipulation of previously '
        'unseen objects. The system first learns a high-level policy for task decomposition, '
        'then applies a low-level grasp synthesis network conditioned on object geometry and '
        'physical properties estimated from depth imagery. We demonstrate that our method '
        'achieves a 91.3% grasp success rate across 500 real-world trials spanning 78 object '
        'categories, outperforming prior baselines by 12.7 percentage points.')

    # Keywords
    pdf.set_font('Helvetica', 'B', 10)
    pdf.multi_cell(W, 7, 'Keywords: ', align='L',
                   new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('Helvetica', '', 10)
    pdf.multi_cell(W, 7,
        'robotic grasping, hierarchical reinforcement learning, '
        'manipulation, unstructured environments, deep learning',
        align='L', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    # 1. Introduction
    heading('1. Introduction')
    body(
        'Robotic manipulation in real-world environments remains one of the most challenging '
        'open problems in robotics. Unlike controlled factory settings, unstructured '
        'environments present constant variability in object placement, lighting conditions, '
        'and surface properties [1, 2]. Existing approaches either rely on precise object '
        'models [3] or require extensive teleoperation data [4], limiting generalization to '
        'novel scenarios.\n\n'
        'Reinforcement learning (RL) has demonstrated remarkable progress in simulated '
        'manipulation tasks [5, 6], yet the sim-to-real transfer gap remains a significant '
        'bottleneck [7]. Recent work by Park et al. [8] addresses this through domain '
        'randomization, achieving promising results on a restricted set of 12 objects. '
        'However, scaling to the diversity encountered in everyday tasks remains unsolved.\n\n'
        'In this paper, we propose an adaptive grasp planning framework leveraging '
        'hierarchical RL. Key contributions: (i) a hierarchical policy separating task-level '
        'planning from motor control; (ii) a geometry-conditioned grasp quality estimator; '
        'and (iii) extensive evaluation across 78 object categories in real-world settings.')

    # 2. Related Work
    heading('2. Related Work')
    body(
        'Robotic grasping has been studied from geometric, data-driven, and learning-based '
        'perspectives. Classical methods [9, 10] compute grasp quality from object geometry '
        'but require known 3D models. Data-driven approaches [11, 12] learn grasp success '
        'predictors from large datasets but struggle with out-of-distribution objects.\n\n'
        'Deep learning methods such as GraspNet [13] and ContactGrasp [14] predict grasp '
        'poses from point clouds or RGB-D images, but treat grasps independently. '
        'Hierarchical approaches [15, 16] jointly learn task and motion planning but have '
        'been validated primarily in simulation. Our work extends [17] with an explicit '
        'grasp quality estimator and large-scale hardware validation.')

    # 3. Method
    heading('3. Method')
    heading('3.1 Hierarchical Policy Architecture', size=11)
    body(
        'Our architecture has two components: a high-level planner Pi_H selecting grasp '
        'candidates from proposals, and a low-level executor Pi_L generating joint '
        'trajectories. Pi_H operates at 2 Hz receiving scene representations from an RGB-D '
        'sensor; Pi_L runs at 100 Hz with proprioceptive feedback.')

    heading('3.2 Grasp Quality Estimator', size=11)
    body(
        'For a depth image D and candidate grasp G = (p, R, w), the quality estimator '
        'Q(G|D) predicts a scalar in [0,1]. We train on 1.2M simulated grasps with '
        'physics-validated labels, then fine-tune on 8,000 real-world grasps. '
        'The network uses a PointNet++ backbone [18] with a regression head.')

    # 4. Experiments
    heading('4. Experiments')
    body(
        'We evaluate on a 7-DOF Franka Emika Panda with parallel-jaw gripper and Intel '
        'RealSense D435. Baselines: GraspNet [13], RL-Grasp [5], HierManip [17]. '
        'Results: our method 91.3% vs 78.6% (GraspNet), 74.2% (RL-Grasp), 82.1% '
        '(HierManip) over 500 trials. Gains are largest for small objects (< 5 cm).')

    # 5. Conclusion
    heading('5. Conclusion')
    body(
        'We have presented a hierarchical RL framework for adaptive robotic grasping '
        'achieving state-of-the-art performance across 78 object categories in real-world '
        'settings. Future work will address deformable objects and multi-arm coordination.')

    # References
    heading('References', size=11)
    pdf.set_font('Helvetica', '', 9)
    refs = [
        '[1] Billard & Kragic (2019). Trends in robot manipulation. Science.',
        '[2] Zhu et al. (2021). Manipulation in the wild. ICRA.',
        '[3] Mahler et al. (2017). Dex-net 2.0. RSS.',
        '[4] Rajeswaran et al. (2018). Learning dexterous manipulation. RSS.',
        '[5] Kalashnikov et al. (2018). QT-Opt. CoRL.',
        "[6] OpenAI et al. (2019). Rubik's Cube with a robot hand. arXiv:1910.07113.",
        '[7] Zhao et al. (2020). Sim-to-real survey. arXiv:2009.05502.',
        '[8] Park et al. (2022). Domain-randomized grasping. IROS.',
        '[9] Miller & Allen (2004). Graspit! RA-M.',
        '[10] Bicchi & Kumar (2000). Robotic grasping review. ICRA.',
        '[11] Levine et al. (2018). Hand-eye coordination. IJRR.',
        '[12] Pinto & Gupta (2016). Supersizing self-supervision. ICRA.',
        '[13] Fang et al. (2020). GraspNet-1Billion. CVPR.',
        '[14] Brahmbhatt et al. (2020). ContactGrasp. ICRA.',
        '[15] Eppe et al. (2019). Hierarchical task planning. arXiv.',
        '[16] Xu et al. (2019). Neural task graphs. CVPR.',
        '[17] Xia et al. (2021). ReLMoGen. ICRA.',
        '[18] Qi et al. (2017). PointNet++. NeurIPS.',
    ]
    for ref in refs:
        pdf.multi_cell(W, 5, ref, align='L',
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(PDF_OUTPUT)
    print(f'PDF created: {PDF_OUTPUT}')


def create_blank_writer_doc():
    """Create a blank LibreOffice Writer document."""
    from docx import Document
    doc = Document()
    # Remove the default empty paragraph's text (keep it blank)
    doc.save(DOCX_OUTPUT)
    print(f'Blank Writer document created: {DOCX_OUTPUT}')


def main():
    create_pdf()
    create_blank_writer_doc()

    # GUI-ready startup: open PDF viewer and LibreOffice Writer
    # Kill any existing instances of evince and soffice to avoid conflicts
    subprocess.run(['pkill', '-f', 'evince'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['pkill', '-f', 'soffice'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    # Open the PDF in Evince (standard PDF viewer on Ubuntu)
    launch_gui(f'evince "{PDF_OUTPUT}"', delay_sec=2.0)

    # Open the blank Writer document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{DOCX_OUTPUT}"', delay_sec=2.0)

    print('GUI_READY: opened PDF in Evince and blank doc in LibreOffice Writer (DISPLAY=:0)')


main()
