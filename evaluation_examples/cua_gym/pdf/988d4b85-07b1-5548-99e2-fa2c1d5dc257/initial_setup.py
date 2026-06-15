"""
Initial Setup: Create a 14-page data paper PDF with 5 tables
Task ID: pdf_res_070
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_070'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/data_paper.pdf'


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


# ---------- Table Data (5 tables, realistic research content) ----------

TABLE_1_HEADER = ["Country", "Population (M)", "GDP ($B)", "Life Expectancy", "Literacy Rate (%)"]
TABLE_1_DATA = [
    ["United States", "331.9", "25,462", "77.5", "99.0"],
    ["China", "1,412.0", "17,963", "78.2", "96.8"],
    ["India", "1,417.2", "3,385", "70.8", "74.4"],
    ["Germany", "84.4", "4,072", "81.2", "99.0"],
    ["Brazil", "215.3", "1,920", "75.9", "93.2"],
    ["Japan", "125.7", "4,231", "84.8", "99.0"],
    ["Nigeria", "218.5", "477", "53.9", "62.0"],
    ["Australia", "26.0", "1,675", "83.4", "99.0"],
]

TABLE_2_HEADER = ["Variable", "Mean", "Std Dev", "Min", "Max", "N"]
TABLE_2_DATA = [
    ["Age (years)", "42.3", "12.7", "18", "89", "4,520"],
    ["BMI (kg/m2)", "26.8", "5.2", "16.1", "48.3", "4,480"],
    ["Systolic BP (mmHg)", "128.4", "18.6", "92", "198", "4,515"],
    ["Diastolic BP (mmHg)", "82.1", "11.3", "58", "132", "4,515"],
    ["Cholesterol (mg/dL)", "201.7", "38.4", "112", "342", "4,490"],
    ["Fasting Glucose (mg/dL)", "105.2", "28.9", "68", "310", "4,505"],
]

TABLE_3_HEADER = ["Model", "Accuracy (%)", "Precision (%)", "Recall (%)", "F1 Score", "AUC"]
TABLE_3_DATA = [
    ["Logistic Regression", "78.4", "76.2", "80.1", "0.781", "0.842"],
    ["Random Forest", "84.7", "83.5", "85.9", "0.847", "0.912"],
    ["Gradient Boosting", "86.2", "85.0", "87.4", "0.861", "0.925"],
    ["SVM (RBF Kernel)", "82.1", "81.3", "82.9", "0.821", "0.893"],
    ["Neural Network (MLP)", "85.5", "84.1", "86.8", "0.854", "0.918"],
    ["XGBoost", "87.1", "86.3", "87.9", "0.871", "0.931"],
    ["LightGBM", "86.8", "85.7", "87.9", "0.867", "0.928"],
]

TABLE_4_HEADER = ["Region", "Sample Size", "Prevalence (%)", "Incidence Rate", "95% CI Lower", "95% CI Upper"]
TABLE_4_DATA = [
    ["North America", "12,450", "8.2", "3.41", "3.12", "3.70"],
    ["Europe", "15,230", "7.5", "2.98", "2.74", "3.22"],
    ["East Asia", "18,670", "6.1", "2.53", "2.35", "2.71"],
    ["South Asia", "9,840", "11.3", "4.72", "4.38", "5.06"],
    ["Sub-Saharan Africa", "6,520", "14.7", "6.15", "5.62", "6.68"],
    ["Latin America", "8,310", "9.8", "4.09", "3.76", "4.42"],
    ["Middle East", "5,190", "10.1", "4.21", "3.82", "4.60"],
]

TABLE_5_HEADER = ["Parameter", "Estimate", "Std Error", "t-value", "p-value"]
TABLE_5_DATA = [
    ["Intercept", "2.341", "0.456", "5.133", "<0.001"],
    ["Age", "0.078", "0.012", "6.500", "<0.001"],
    ["Gender (Male)", "-0.342", "0.187", "-1.829", "0.068"],
    ["BMI", "0.156", "0.031", "5.032", "<0.001"],
    ["Smoking Status", "0.891", "0.203", "4.389", "<0.001"],
    ["Exercise (hrs/wk)", "-0.234", "0.058", "-4.034", "<0.001"],
    ["Family History", "0.567", "0.195", "2.908", "0.004"],
    ["Alcohol (drinks/wk)", "0.089", "0.024", "3.708", "<0.001"],
    ["Education (years)", "-0.045", "0.019", "-2.368", "0.018"],
]

ALL_TABLES = [
    (TABLE_1_HEADER, TABLE_1_DATA, "Table 1: Demographic and Economic Indicators by Country (2023)"),
    (TABLE_2_HEADER, TABLE_2_DATA, "Table 2: Descriptive Statistics of Key Clinical Variables"),
    (TABLE_3_HEADER, TABLE_3_DATA, "Table 3: Classification Model Performance Comparison"),
    (TABLE_4_HEADER, TABLE_4_DATA, "Table 4: Regional Epidemiological Summary"),
    (TABLE_5_HEADER, TABLE_5_DATA, "Table 5: Multivariate Regression Results (Dependent Variable: Disease Score)"),
]

# Tables appear on pages 4, 6, 8, 10, 12 (0-indexed: 3, 5, 7, 9, 11)
TABLE_PAGES = [3, 5, 7, 9, 11]


def draw_table(page, y_start, header, data, caption, col_widths=None):
    """Draw a table with borders on the page. Returns y position after table."""
    left_margin = 56
    fontsize_caption = 10
    fontsize_header = 9
    fontsize_data = 8.5
    row_height = 18
    cell_padding = 4

    num_cols = len(header)
    if col_widths is None:
        avail_width = 483  # page width minus margins
        col_widths = [avail_width / num_cols] * num_cols

    # Caption above table
    page.insert_text(
        pymupdf.Point(left_margin, y_start),
        caption,
        fontsize=fontsize_caption,
        fontname="hebo",
        color=(0, 0, 0),
    )
    y = y_start + 16

    shape = page.new_shape()
    total_width = sum(col_widths)

    # Draw header row
    x = left_margin
    for ci, h_text in enumerate(header):
        rect = pymupdf.Rect(x, y, x + col_widths[ci], y + row_height)
        shape.draw_rect(rect)
        shape.finish(color=(0, 0, 0), fill=(0.18, 0.31, 0.53), width=0.5)
        page.insert_text(
            pymupdf.Point(x + cell_padding, y + row_height - 5),
            h_text,
            fontsize=fontsize_header,
            fontname="hebo",
            color=(1, 1, 1),
        )
        x += col_widths[ci]
    y += row_height

    # Draw data rows
    for ri, row in enumerate(data):
        x = left_margin
        fill_color = (0.93, 0.93, 0.93) if ri % 2 == 0 else (1, 1, 1)
        for ci, cell_text in enumerate(row):
            rect = pymupdf.Rect(x, y, x + col_widths[ci], y + row_height)
            shape.draw_rect(rect)
            shape.finish(color=(0, 0, 0), fill=fill_color, width=0.3)
            page.insert_text(
                pymupdf.Point(x + cell_padding, y + row_height - 5),
                cell_text,
                fontsize=fontsize_data,
                fontname="helv",
                color=(0, 0, 0),
            )
            x += col_widths[ci]
        y += row_height

    shape.commit()
    return y + 10


# Section titles for non-table pages
SECTIONS = [
    ("Abstract", [
        "Background: Chronic disease burden continues to grow globally, with significant regional disparities "
        "in prevalence and outcomes. This study presents a comprehensive multi-regional analysis of disease "
        "risk factors and model-based predictions using data from 76,210 participants across seven geographic regions.",
        "Methods: We conducted a cross-sectional analysis using standardized clinical measurements and "
        "validated questionnaires. Machine learning classifiers were trained on 80% of the dataset with "
        "5-fold cross-validation and evaluated on the held-out 20% test set.",
        "Results: XGBoost achieved the highest classification accuracy of 87.1% (AUC=0.931). Key risk factors "
        "identified were age (OR=1.08, p<0.001), BMI (OR=1.17, p<0.001), and smoking status (OR=2.44, p<0.001). "
        "Sub-Saharan Africa showed the highest prevalence at 14.7% (95% CI: 13.8-15.6%).",
        "Conclusions: Our findings highlight the need for region-specific intervention strategies. The machine "
        "learning pipeline developed here can be deployed for real-time risk stratification in clinical settings.",
    ]),
    ("1. Introduction", [
        "The global burden of chronic disease has increased substantially over the past three decades, driven by "
        "population aging, urbanization, and changes in lifestyle factors (Murray et al., 2022). According to the "
        "World Health Organization, non-communicable diseases account for 74% of all deaths worldwide, with "
        "cardiovascular disease, cancer, diabetes, and chronic respiratory diseases being the leading contributors.",
        "Despite extensive research, significant gaps remain in our understanding of how disease risk factors "
        "interact across different populations and geographic regions. Previous studies have been limited by "
        "small sample sizes, single-region focus, or outdated analytical methods that fail to capture complex "
        "non-linear relationships among risk factors (Smith & Wang, 2021; Patel et al., 2023).",
        "Machine learning approaches offer promising alternatives to traditional statistical methods for disease "
        "risk prediction. Recent advances in gradient boosting algorithms, in particular, have demonstrated "
        "superior performance in clinical prediction tasks compared to logistic regression models (Chen & "
        "Guestrin, 2016; Ke et al., 2017).",
        "This study aims to: (1) characterize the distribution of key clinical risk factors across seven major "
        "geographic regions; (2) compare the predictive performance of seven machine learning classifiers; and "
        "(3) identify the most important modifiable risk factors for targeted intervention strategies.",
    ]),
    ("2. Methods", [
        "2.1 Study Design and Population",
        "We conducted a multi-center cross-sectional study involving 76,210 adults aged 18-89 years recruited "
        "from 142 clinical sites across seven geographic regions between January 2020 and December 2023. "
        "Participants were selected through stratified random sampling to ensure demographic representativeness.",
        "2.2 Data Collection",
        "Standardized clinical measurements were obtained by trained research staff following WHO STEPS protocol. "
        "Anthropometric measurements included height, weight, waist circumference, and blood pressure (measured "
        "in triplicate using calibrated automated devices). Fasting blood samples were collected for lipid panel "
        "and glucose measurements. Lifestyle factors were assessed using validated questionnaires adapted for "
        "local cultural contexts.",
        "2.3 Statistical Analysis",
        "Descriptive statistics were computed for all clinical variables. Continuous variables are reported as "
        "mean (SD) and categorical variables as frequency (%). Seven machine learning classifiers were trained "
        "using scikit-learn (v1.3) with 5-fold stratified cross-validation. Hyperparameter tuning was performed "
        "using Bayesian optimization with 100 iterations per model. All analyses were conducted in Python 3.11.",
    ]),
    ("3. Results", [
        "3.1 Study Population Characteristics",
        "Of the 76,210 enrolled participants, 4,520 met inclusion criteria for the primary analysis after "
        "exclusion of incomplete records and outlier detection. The mean age was 42.3 years (SD=12.7), with "
        "52.3% female. Regional sample sizes ranged from 5,190 (Middle East) to 18,670 (East Asia).",
        "3.2 Clinical Variable Distributions",
        "Mean BMI was 26.8 kg/m2 (SD=5.2), indicating a population-level tendency toward overweight status. "
        "Systolic blood pressure averaged 128.4 mmHg (SD=18.6), with 34.2% of participants meeting criteria "
        "for hypertension (SBP >= 140 mmHg). Fasting glucose levels suggested pre-diabetic patterns in 28.7% "
        "of the cohort.",
    ]),
    ("4. Discussion", [
        "Our multi-regional analysis provides several key insights into the global landscape of chronic disease "
        "risk factors. First, the substantial regional variation in disease prevalence (6.1% to 14.7%) "
        "underscores the importance of context-specific prevention strategies.",
        "The superior performance of gradient boosting methods (XGBoost: AUC=0.931, LightGBM: AUC=0.928) over "
        "traditional logistic regression (AUC=0.842) aligns with recent benchmarking studies in clinical "
        "prediction (Rajkomar et al., 2019). However, the modest improvement of XGBoost over the neural network "
        "approach (AUC=0.918) suggests diminishing returns from model complexity alone.",
        "Our regression analysis identified age, BMI, and smoking status as the three strongest independent "
        "predictors, consistent with the established literature. Notably, the protective effect of physical "
        "exercise (-0.234 per hour/week, p<0.001) was stronger than previously reported in single-region "
        "studies, possibly reflecting the greater statistical power of our multi-regional design.",
        "4.1 Limitations",
        "Several limitations warrant consideration. The cross-sectional design precludes causal inference. "
        "Self-reported lifestyle data may be subject to recall and social desirability bias. Additionally, "
        "the exclusion of 93.5% of enrolled participants due to incomplete data may introduce selection bias, "
        "though sensitivity analyses using multiple imputation yielded comparable results.",
    ]),
    ("5. Conclusion", [
        "This comprehensive multi-regional study demonstrates that ensemble machine learning methods, "
        "particularly XGBoost, offer superior predictive performance for chronic disease risk classification "
        "compared to traditional approaches. The identified regional disparities in disease burden highlight "
        "the need for tailored public health interventions.",
        "Future work should focus on: (1) prospective validation of the XGBoost risk model in independent "
        "cohorts; (2) integration of genetic and environmental exposure data; and (3) development of a "
        "web-based clinical decision support tool for real-time risk stratification.",
    ]),
    ("References", [
        "Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. Proceedings of the 22nd "
        "ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785-794.",
        "Ke, G., Meng, Q., Finley, T., et al. (2017). LightGBM: A highly efficient gradient boosting decision "
        "tree. Advances in Neural Information Processing Systems, 30, 3146-3154.",
        "Murray, C. J., et al. (2022). Global burden of 369 diseases and injuries in 204 countries, 1990-2019. "
        "The Lancet, 396(10258), 1204-1222.",
        "Patel, S. A., Ali, M. K., & Narayan, K. M. V. (2023). Multi-ethnic comparison of disease risk "
        "prediction models. Journal of Clinical Epidemiology, 145, 78-91.",
        "Rajkomar, A., Dean, J., & Kohane, I. (2019). Machine learning in medicine. New England Journal of "
        "Medicine, 380(14), 1347-1358.",
        "Smith, J. P., & Wang, Y. (2021). Regional disparities in chronic disease burden: a systematic review. "
        "Global Health Research and Policy, 6(1), 1-15.",
        "World Health Organization (2023). Noncommunicable diseases fact sheet. WHO Press.",
    ]),
]


def create_initial():
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # We need 14 pages total. Tables go on pages 4,6,8,10,12 (0-indexed: 3,5,7,9,11).
    # Sections layout:
    # Page 0: Title page
    # Page 1: Abstract
    # Page 2: Introduction (part 1)
    # Page 3: Introduction (cont) + TABLE 1
    # Page 4: Methods (part 1)
    # Page 5: Methods (cont) + TABLE 2
    # Page 6: Results (part 1)
    # Page 7: Results (cont) + TABLE 3
    # Page 8: Discussion (part 1) + TABLE 4
    # Page 9: Discussion (cont)
    # Page 10: Discussion (cont) + TABLE 5 -- wait, table pages are 3,5,7,9,11
    # Let me just place text on all 14 pages, with tables inserted on the right pages.

    left_margin = 56
    right_margin = 539
    text_width = right_margin - left_margin

    # --- Page 0: Title page ---
    page = doc.new_page(width=595, height=842)
    page.insert_text(pymupdf.Point(297, 200), "Multi-Regional Analysis of Chronic Disease",
                     fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(297, 230), "Risk Factors: A Machine Learning Approach",
                     fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(297, 290), "Elena Rodriguez, PhD; James Chen, MD, MPH;",
                     fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(297, 310), "Aisha Patel, PhD; Marcus Weber, DSc",
                     fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(297, 360), "Department of Epidemiology and Biostatistics",
                     fontsize=11, fontname="tiit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(297, 380), "Global Health Research Institute",
                     fontsize=11, fontname="tiit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(297, 420), "Journal of Global Health Analytics, 2024, 12(3): 145-162",
                     fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(297, 450), "DOI: 10.1093/jgha/2024.0312",
                     fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    # Content mapping to pages: we'll interleave text sections and tables
    # We need 13 more pages (1-13), total 14
    # Table pages (0-indexed): 3, 5, 7, 9, 11

    # Section assignments:
    # Pages 1-2: Abstract + Intro
    # Page 3: Intro cont + Table 1
    # Page 4-5: Methods, page 5 has Table 2
    # Page 6-7: Results start, page 7 has Table 3
    # Page 8-9: Results/Discussion, page 9 has Table 4
    # Page 10-11: Discussion cont, page 11 has Table 5
    # Page 12-13: Conclusion + References

    section_idx = 0  # track which section we're drawing from
    table_idx = 0

    for page_num in range(1, 14):
        page = doc.new_page(width=595, height=842)
        y = 56  # top margin

        # Page number at bottom
        page.insert_text(pymupdf.Point(297, 820), str(page_num + 1),
                         fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

        is_table_page = page_num in TABLE_PAGES

        if is_table_page and table_idx < len(ALL_TABLES):
            # First add some transitional text, then the table
            # Add a small paragraph of continuing text
            if section_idx < len(SECTIONS):
                sec_title, sec_paras = SECTIONS[section_idx]
                # Write section title if we haven't started this section
                page.insert_text(pymupdf.Point(left_margin, y + 14),
                                 sec_title, fontsize=14, fontname="hebo", color=(0, 0, 0))
                y += 30
                # Write first paragraph only
                if sec_paras:
                    rect = pymupdf.Rect(left_margin, y, right_margin, y + 80)
                    page.insert_textbox(rect, sec_paras[0],
                                        fontsize=10, fontname="helv", color=(0, 0, 0),
                                        align=pymupdf.TEXT_ALIGN_JUSTIFY)
                    y += 90
                section_idx += 1

            # Draw the table
            hdr, data, caption = ALL_TABLES[table_idx]
            # Compute column widths based on number of columns
            num_cols = len(hdr)
            avail = 483
            col_widths = [avail / num_cols] * num_cols
            draw_table(page, y, hdr, data, caption, col_widths)
            table_idx += 1

        else:
            # Pure text page
            if section_idx < len(SECTIONS):
                sec_title, sec_paras = SECTIONS[section_idx]
                page.insert_text(pymupdf.Point(left_margin, y + 14),
                                 sec_title, fontsize=14, fontname="hebo", color=(0, 0, 0))
                y += 32

                for para in sec_paras:
                    # Check if it's a subsection header (starts with digit and period or is short)
                    if len(para) < 60 and (para[0].isdigit() or para.startswith("Background") or
                                            para.startswith("Methods") or para.startswith("Results")):
                        page.insert_text(pymupdf.Point(left_margin, y + 12),
                                         para, fontsize=11, fontname="hebo", color=(0, 0, 0))
                        y += 22
                    else:
                        rect = pymupdf.Rect(left_margin, y, right_margin, y + 200)
                        excess = page.insert_textbox(rect, para,
                                                      fontsize=10, fontname="helv", color=(0, 0, 0),
                                                      align=pymupdf.TEXT_ALIGN_JUSTIFY)
                        # Estimate used height
                        # Approximate: 10pt font, ~65 chars per line, line height ~13pt
                        chars = len(para)
                        lines = max(1, chars // 75 + 1)
                        used_height = lines * 13 + 8
                        y += used_height

                    if y > 750:
                        break

                section_idx += 1
            else:
                # Extra pages: add placeholder continuation text
                page.insert_text(pymupdf.Point(left_margin, y + 14),
                                 "(continued)", fontsize=10, fontname="tiit", color=(0.5, 0.5, 0.5))

    # Set metadata
    doc.set_metadata({
        "title": "Multi-Regional Analysis of Chronic Disease Risk Factors",
        "author": "Rodriguez E, Chen J, Patel A, Weber M",
        "subject": "Epidemiology, Machine Learning, Chronic Disease",
        "keywords": "chronic disease, risk factors, machine learning, XGBoost, multi-regional",
        "creator": "LaTeX with hyperref",
        "producer": "pdfTeX-1.40.25",
    })

    # Set TOC
    toc = [
        [1, "Abstract", 2],
        [1, "1. Introduction", 3],
        [1, "2. Methods", 5],
        [1, "3. Results", 7],
        [1, "4. Discussion", 9],
        [1, "5. Conclusion", 12],
        [1, "References", 13],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready: open PDF in evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
