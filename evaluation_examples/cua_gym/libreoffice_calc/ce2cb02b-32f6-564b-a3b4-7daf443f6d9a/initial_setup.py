"""
Initial Setup: Extract Methodology section from PDF and save to Google Drive
Task ID: osworld_multi_apps_pdf_to_gdocs_004
Domain: multi_apps (Chrome + PDF)

Creates:
  - research_paper_draft.pdf on the Desktop with sections:
    Abstract, Introduction, Methodology, Results, Conclusion
  - Chrome open with Google Drive (drive.google.com) showing a 'shared_research' folder
"""

import os
import shlex
import subprocess
import time
import sys

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_to_gdocs_004'
DESKTOP = f'{WORKDIR}/Desktop'
PDF_PATH = f'{DESKTOP}/research_paper_draft.pdf'


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


def install_fpdf():
    """Ensure fpdf2 is available on the VM."""
    try:
        import fpdf
    except ImportError:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', 'fpdf2', '--quiet'],
            check=True
        )


def create_pdf():
    """Create research_paper_draft.pdf on the Desktop with multiple sections."""
    install_fpdf()
    from fpdf import FPDF

    os.makedirs(DESKTOP, exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # --- Title ---
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 12, 'Quantitative Analysis of Machine Learning', ln=True, align='C')
    pdf.set_font('Helvetica', '', 14)
    pdf.cell(0, 8, 'Approaches in Healthcare Diagnostics', ln=True, align='C')
    pdf.ln(4)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 6, 'Dr. Emily R. Hartwell, Dr. James P. Nguyen, Dr. Aisha O. Okafor', ln=True, align='C')
    pdf.cell(0, 6, 'Journal of Medical Informatics, Vol. 12, No. 3, March 2025', ln=True, align='C')
    pdf.ln(8)

    # --- Abstract ---
    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 8, 'Abstract', ln=True)
    pdf.set_font('Helvetica', '', 11)
    abstract_text = (
        "This paper presents a comprehensive quantitative analysis of machine learning techniques "
        "applied to healthcare diagnostics. We evaluate four approaches - logistic regression, "
        "random forest, support vector machines (SVM), and deep neural networks (DNN) - across "
        "three clinical datasets: chest X-ray classification (n=12,000), diabetic retinopathy "
        "screening (n=8,500), and ECG arrhythmia detection (n=6,200). Our results demonstrate "
        "that DNN models achieve the highest diagnostic accuracy (AUC = 0.943) but require "
        "significantly more compute resources, whereas random forest models offer a compelling "
        "accuracy-efficiency tradeoff (AUC = 0.917). We further analyze fairness metrics across "
        "demographic subgroups and find measurable disparities that future work must address."
    )
    pdf.multi_cell(0, 6, abstract_text)
    pdf.ln(6)

    # --- Introduction ---
    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 8, '1. Introduction', ln=True)
    pdf.set_font('Helvetica', '', 11)
    intro_text = (
        "The application of machine learning (ML) to clinical decision support has accelerated "
        "dramatically over the past decade, driven by the increasing availability of large "
        "digitized health record datasets and improvements in compute infrastructure. Healthcare "
        "systems globally face mounting pressure to reduce diagnostic errors, minimize physician "
        "burnout, and ensure equitable access to expert-level care in resource-limited settings.\n\n"
        "Prior work has evaluated ML classifiers in narrow, single-disease contexts (Esteva et al., "
        "2017; Rajpurkar et al., 2018). However, cross-domain comparative analyses that assess "
        "performance across multiple clinical tasks and demographic subgroups remain sparse. This "
        "gap motivates our study, which offers a rigorous head-to-head evaluation under unified "
        "data preprocessing and evaluation protocols.\n\n"
        "We make the following contributions: (1) A standardized benchmark of four ML algorithms "
        "on three distinct diagnostic tasks; (2) A fairness audit examining performance disparities "
        "by age, sex, and ethnicity; (3) Practical recommendations for practitioners selecting "
        "ML models under real-world resource constraints."
    )
    pdf.multi_cell(0, 6, intro_text)
    pdf.ln(6)

    # --- Methodology ---
    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 8, '2. Methodology', ln=True)
    pdf.set_font('Helvetica', '', 11)
    methodology_text = (
        "2.1 Dataset Collection and Preprocessing\n\n"
        "We sourced three publicly available clinical datasets. The chest X-ray dataset was "
        "obtained from NIH CXR14 (Wang et al., 2017) and filtered to 12,000 images (6,000 "
        "pathological, 6,000 normal) using stratified sampling to balance disease prevalence. "
        "The diabetic retinopathy dataset consisted of 8,500 retinal fundus photographs graded "
        "on the ETDRS severity scale (grades 0-4) from the Kaggle Diabetic Retinopathy competition "
        "(2015). The ECG arrhythmia dataset comprised 6,200 12-lead ECG recordings from the "
        "PhysioNet MIT-BIH database annotated by board-certified cardiologists.\n\n"
        "All images were resized to 224x224 pixels and normalized using per-channel mean and "
        "standard deviation computed from the training split. Tabular ECG features were "
        "standardized using z-score normalization. Missing values (< 2.1% across all datasets) "
        "were imputed using median substitution for numerical features and mode imputation for "
        "categorical features.\n\n"
        "2.2 Model Architectures\n\n"
        "Four model architectures were evaluated:\n"
        "  (a) Logistic Regression (LR): L2-regularized with C selected via 5-fold cross-validation "
        "on the training set (C in {0.001, 0.01, 0.1, 1.0, 10.0}).\n"
        "  (b) Random Forest (RF): 500 estimators, max depth = 20, minimum samples per leaf = 5. "
        "Hyperparameters were tuned using random search with 100 iterations.\n"
        "  (c) Support Vector Machine (SVM): RBF kernel with gamma = 'scale'; C and gamma jointly "
        "optimized via Bayesian hyperparameter search.\n"
        "  (d) Deep Neural Network (DNN): ResNet-50 backbone pre-trained on ImageNet, fine-tuned "
        "for 30 epochs using Adam optimizer (lr = 1e-4, weight decay = 1e-5). A cosine annealing "
        "learning rate schedule was applied. Batch size = 64.\n\n"
        "2.3 Evaluation Protocol\n\n"
        "All experiments used a stratified 70/15/15 train/validation/test split, ensuring "
        "proportional representation of class labels across splits. Primary evaluation metric "
        "was the Area Under the Receiver Operating Characteristic Curve (AUC-ROC). Secondary "
        "metrics included sensitivity (recall), specificity, F1 score, and Matthews Correlation "
        "Coefficient (MCC). Statistical significance of pairwise differences was assessed using "
        "DeLong's test for AUC comparison (DeLong et al., 1988) with Bonferroni correction for "
        "multiple comparisons (alpha = 0.05 / 6 = 0.0083).\n\n"
        "2.4 Fairness Analysis\n\n"
        "Demographic subgroup metadata (age group: <40, 40-60, >60; biological sex: male/female; "
        "self-reported ethnicity: White, Black/African American, Hispanic/Latino, Asian, Other) "
        "was available for 87.3% of subjects. Fairness was assessed using equalized odds "
        "(Hardt et al., 2016): the difference in true positive rates and false positive rates "
        "across subgroups. A disparity was flagged if the inter-group difference exceeded 0.05 "
        "for either metric."
    )
    pdf.multi_cell(0, 6, methodology_text)
    pdf.ln(6)

    # --- Results ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 8, '3. Results', ln=True)
    pdf.set_font('Helvetica', '', 11)
    results_text = (
        "3.1 Diagnostic Performance\n\n"
        "Table 1 summarizes AUC-ROC scores across all four models and three datasets. The DNN "
        "achieved the highest mean AUC across tasks (0.943 +/- 0.011), followed by RF (0.917 "
        "+/- 0.014), SVM (0.904 +/- 0.017), and LR (0.871 +/- 0.022). DNN outperformed all "
        "other models on chest X-ray classification (AUC = 0.961, p < 0.001 vs. RF by DeLong's "
        "test). On ECG arrhythmia detection, the performance gap between DNN (0.939) and RF "
        "(0.928) was not statistically significant after Bonferroni correction (p = 0.021).\n\n"
        "3.2 Computational Efficiency\n\n"
        "Training time for DNN averaged 4.7 hours (GPU: NVIDIA A100) compared to 12 minutes "
        "for RF on an 8-core CPU. Inference latency per sample: DNN = 18ms, RF = 0.8ms, "
        "SVM = 2.3ms, LR = 0.1ms. For real-time clinical decision support applications where "
        "inference must complete in under 5ms, RF remains the recommended choice.\n\n"
        "3.3 Fairness Results\n\n"
        "Statistically significant equalized odds disparities (> 0.05) were observed for DNN "
        "on chest X-ray classification across age groups (TPR gap = 0.078 between age <40 and "
        "age >60) and for SVM on diabetic retinopathy detection across ethnic groups (FPR gap "
        "= 0.063 between White and Black/African American subgroups). LR showed the most "
        "consistent fairness metrics, though this partly reflects lower overall performance "
        "suppressing variation across subgroups."
    )
    pdf.multi_cell(0, 6, results_text)
    pdf.ln(6)

    # --- Conclusion ---
    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 8, '4. Conclusion', ln=True)
    pdf.set_font('Helvetica', '', 11)
    conclusion_text = (
        "This study provides empirical evidence that DNN-based approaches offer the highest "
        "diagnostic accuracy in medical imaging tasks but introduce fairness risks and "
        "computational costs that must be carefully weighed in deployment decisions. Random "
        "forest models present a practical alternative for resource-constrained settings, "
        "achieving near-state-of-the-art performance with dramatically lower compute "
        "requirements and more consistent fairness properties.\n\n"
        "Future work should investigate post-processing fairness interventions (e.g., threshold "
        "adjustment, re-weighting) and explore federated learning paradigms that preserve "
        "patient privacy while expanding training data diversity. Broader clinical validation "
        "in prospective deployment settings remains an essential next step before any of these "
        "models are integrated into routine clinical workflows."
    )
    pdf.multi_cell(0, 6, conclusion_text)
    pdf.ln(6)

    # --- References ---
    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 8, 'References', ln=True)
    pdf.set_font('Helvetica', '', 10)
    refs = [
        "DeLong, E. R., DeLong, D. M., & Clarke-Pearson, D. L. (1988). Comparing the areas under "
        "two or more correlated receiver operating characteristic curves. Biometrics, 44(3), 837-845.",
        "Esteva, A., et al. (2017). Dermatologist-level classification of skin cancer with deep neural "
        "networks. Nature, 542, 115-118.",
        "Hardt, M., Price, E., & Srebro, N. (2016). Equality of opportunity in supervised learning. "
        "Advances in Neural Information Processing Systems, 29.",
        "Rajpurkar, P., et al. (2018). Deep learning for chest radiograph diagnosis. PLOS Medicine, "
        "15(11), e1002686.",
        "Wang, X., et al. (2017). ChestX-ray8: Hospital-scale chest X-ray database and benchmarks. "
        "CVPR 2017, 2097-2106.",
    ]
    for ref in refs:
        pdf.multi_cell(0, 5, ref)
        pdf.ln(2)

    pdf.output(PDF_PATH)
    print(f'PDF created: {PDF_PATH}')


def setup_chrome_state():
    """Kill existing Chrome, set up initial state with Google Drive, then relaunch."""
    # Kill any running Chrome instances first
    subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
    time.sleep(2)

    # Create a local HTML page that simulates the Google Drive interface
    # with the shared_research folder visible
    gdrive_html = f'{WORKDIR}/gdrive_state.html'
    html_content = """<!DOCTYPE html>
<html>
<head><title>Google Drive - shared_research</title></head>
<body>
<h2>Google Drive</h2>
<p><strong>Folder:</strong> shared_research</p>
<p>This folder is empty. Use Google Drive to create documents here.</p>
</body>
</html>
"""
    with open(gdrive_html, 'w') as f:
        f.write(html_content)

    # Note: We launch Chrome pointing to Google Drive
    # The task requires the user to navigate to Google Drive and create the Doc
    print('Chrome state prepared.')


def create_initial():
    """Create all initial-env artifacts."""
    # Step 1: Create the PDF on the Desktop
    create_pdf()

    # Step 2: Prepare Chrome state
    setup_chrome_state()

    # Step 3: Launch Chrome with Google Drive open
    # Launch Chrome with remote debugging so reward-gen can inspect it
    launch_gui(
        'google-chrome --remote-debugging-port=1337 '
        '"https://drive.google.com/drive/folders/" '
        '--new-window',
        delay_sec=3.0
    )

    print(f'Initial artifacts:')
    print(f'  PDF: {PDF_PATH}')
    print(f'  Chrome: opened with Google Drive')
    print('GUI_READY: launched Chrome with Google Drive and DISPLAY=:0')


create_initial()
