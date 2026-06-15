"""
Initial Setup: Create filled student quiz PDF form and answer key JSON
Task ID: pdf_gf3_047
Domain: pdf
"""

import os
import json
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_047'
QUIZZES_DIR = f'{WORKDIR}/quizzes'
SCRIPTS_DIR = f'{WORKDIR}/scripts'
STUDENT_PDF = f'{QUIZZES_DIR}/student_answers.pdf'
ANSWER_KEY_JSON = f'{QUIZZES_DIR}/answer_key.json'


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


# MC answer choices the student selected (some correct, some wrong)
STUDENT_MC_ANSWERS = [
    "B", "A", "C", "D", "B",   # 1-5
    "A", "C", "B", "D", "A",   # 6-10
    "C", "B", "A", "D", "C",   # 11-15
    "B", "D", "A", "C", "B",   # 16-20
    "A", "C", "D", "B", "A",   # 21-25
    "C", "D", "B", "A", "D",   # 26-30
]

# Correct MC answers (student gets some right, some wrong)
CORRECT_MC_ANSWERS = [
    "B", "A", "C", "D", "A",   # 1-5  (q5 wrong: student=B, correct=A)
    "A", "C", "B", "D", "B",   # 6-10 (q10 wrong: student=A, correct=B)
    "C", "B", "A", "D", "C",   # 11-15 (all correct)
    "B", "D", "C", "C", "B",   # 16-20 (q18 wrong: student=A, correct=C; q19 wrong: student=C, correct=C - actually same... let me fix)
    "A", "C", "D", "B", "A",   # 21-25 (all correct)
    "C", "A", "B", "A", "D",   # 26-30 (q27 wrong: student=D, correct=A; q28 wrong: student=B, correct=B - same... fix)
]

# Let me be more deliberate:
# Student answers vs correct answers - make exactly 6 MC wrong
CORRECT_MC_ANSWERS = list(STUDENT_MC_ANSWERS)  # start same
# Make questions 5, 10, 18, 22, 27, 30 incorrect
CORRECT_MC_ANSWERS[4] = "A"   # q5:  student=B, correct=A
CORRECT_MC_ANSWERS[9] = "B"   # q10: student=A, correct=B
CORRECT_MC_ANSWERS[17] = "C"  # q18: student=A, correct=C
CORRECT_MC_ANSWERS[21] = "D"  # q22: student=C, correct=D
CORRECT_MC_ANSWERS[26] = "A"  # q27: student=D, correct=A
CORRECT_MC_ANSWERS[29] = "C"  # q30: student=D, correct=C
# So 24 MC correct = 24 points out of 30

# Short answer student responses and keywords
SA_QUESTIONS = [
    "What is photosynthesis?",
    "Explain the water cycle.",
    "Describe Newton's first law of motion.",
    "What causes tides on Earth?",
    "Define the term 'ecosystem'.",
    "Explain how vaccines work.",
    "What is the significance of the ozone layer?",
    "Describe the process of cellular respiration.",
    "What are the main causes of climate change?",
    "Explain the concept of supply and demand.",
]

STUDENT_SA_ANSWERS = [
    "Photosynthesis is when plants convert sunlight and carbon dioxide into glucose and oxygen using chlorophyll",
    "Water evaporates from oceans, forms clouds through condensation, then falls as precipitation back to earth",
    "An object at rest stays at rest and an object in motion stays in motion unless acted upon by an external force",
    "Tides are caused by the gravitational pull of the moon and sun on Earth's oceans",
    "An ecosystem is a community of living organisms interacting with their physical environment",
    "Vaccines introduce a weakened form of a pathogen to stimulate the immune system to produce antibodies",
    "The ozone layer protects Earth from ultraviolet radiation from the sun",
    "Cells break down glucose using oxygen to produce ATP energy and release carbon dioxide",
    "Burning fossil fuels and deforestation release greenhouse gases that trap heat",
    "When demand increases and supply stays the same, prices go up",
]

SA_KEYWORDS = [
    ["plants", "sunlight", "carbon dioxide", "glucose", "oxygen"],
    ["evaporation", "condensation", "precipitation", "water", "cycle"],
    ["rest", "motion", "force", "object", "external"],
    ["gravitational", "moon", "sun", "oceans", "pull"],
    ["community", "organisms", "environment", "living", "interacting"],
    ["weakened", "pathogen", "immune", "antibodies", "system"],
    ["ozone", "ultraviolet", "radiation", "protects", "sun"],
    ["glucose", "oxygen", "ATP", "energy", "carbon dioxide"],
    ["fossil fuels", "greenhouse", "gases", "heat", "deforestation"],
    ["demand", "supply", "prices", "increases", "market"],
]


def create_student_pdf():
    """Create a filled PDF form with 30 MC fields and 10 SA fields."""
    os.makedirs(QUIZZES_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ---- Page 1: Header + MC Questions 1-15 ----
    page = doc.new_page(width=612, height=792)

    # Title
    page.insert_text(pymupdf.Point(72, 50), "Biology & General Science Quiz", fontsize=18, fontname="hebo", color=(0, 0, 0.5))
    page.insert_text(pymupdf.Point(72, 70), "Student Name:", fontsize=11, fontname="hebo")

    # Student name field
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "student_name"
    w.field_value = "Emily Rodriguez"
    w.rect = pymupdf.Rect(180, 58, 400, 76)
    w.text_fontsize = 11
    w.text_color = (0, 0, 0)
    w.fill_color = (0.95, 0.95, 0.95)
    w.border_color = (0, 0, 0)
    w.border_width = 0.5
    page.add_widget(w)

    page.insert_text(pymupdf.Point(72, 95), "Section 1: Multiple Choice (1 point each)", fontsize=13, fontname="hebo")

    y = 110
    for i in range(15):
        qnum = i + 1
        page.insert_text(pymupdf.Point(72, y + 13), f"Q{qnum}:", fontsize=10, fontname="hebo")

        w = pymupdf.Widget()
        w.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
        w.field_name = f"mc_{qnum}"
        w.choice_values = ["A", "B", "C", "D"]
        w.field_value = STUDENT_MC_ANSWERS[i]
        w.rect = pymupdf.Rect(110, y, 160, y + 18)
        w.text_fontsize = 10
        w.fill_color = (0.95, 0.95, 1.0)
        w.border_color = (0.3, 0.3, 0.3)
        w.border_width = 0.5
        page.add_widget(w)
        y += 28

    # ---- Page 2: MC Questions 16-30 ----
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 50), "Section 1 (continued): Multiple Choice", fontsize=13, fontname="hebo")

    y = 70
    for i in range(15, 30):
        qnum = i + 1
        page2.insert_text(pymupdf.Point(72, y + 13), f"Q{qnum}:", fontsize=10, fontname="hebo")

        w = pymupdf.Widget()
        w.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
        w.field_name = f"mc_{qnum}"
        w.choice_values = ["A", "B", "C", "D"]
        w.field_value = STUDENT_MC_ANSWERS[i]
        w.rect = pymupdf.Rect(110, y, 160, y + 18)
        w.text_fontsize = 10
        w.fill_color = (0.95, 0.95, 1.0)
        w.border_color = (0.3, 0.3, 0.3)
        w.border_width = 0.5
        page2.add_widget(w)
        y += 28

    # ---- Page 3: Short Answer Questions 1-5 ----
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 50), "Section 2: Short Answer (up to 5 points each)", fontsize=13, fontname="hebo")

    y = 75
    for i in range(5):
        qnum = i + 1
        page3.insert_text(pymupdf.Point(72, y + 13), f"SA{qnum}: {SA_QUESTIONS[i]}", fontsize=10, fontname="hebo")
        y += 20

        w = pymupdf.Widget()
        w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
        w.field_name = f"sa_{qnum}"
        w.field_value = STUDENT_SA_ANSWERS[i]
        w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
        w.rect = pymupdf.Rect(72, y, 540, y + 60)
        w.text_fontsize = 9
        w.text_color = (0, 0, 0)
        w.fill_color = (1.0, 1.0, 0.95)
        w.border_color = (0.3, 0.3, 0.3)
        w.border_width = 0.5
        page3.add_widget(w)
        y += 75

    # ---- Page 4: Short Answer Questions 6-10 ----
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(72, 50), "Section 2 (continued): Short Answer", fontsize=13, fontname="hebo")

    y = 75
    for i in range(5, 10):
        qnum = i + 1
        page4.insert_text(pymupdf.Point(72, y + 13), f"SA{qnum}: {SA_QUESTIONS[i]}", fontsize=10, fontname="hebo")
        y += 20

        w = pymupdf.Widget()
        w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
        w.field_name = f"sa_{qnum}"
        w.field_value = STUDENT_SA_ANSWERS[i]
        w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
        w.rect = pymupdf.Rect(72, y, 540, y + 60)
        w.text_fontsize = 9
        w.text_color = (0, 0, 0)
        w.fill_color = (1.0, 1.0, 0.95)
        w.border_color = (0.3, 0.3, 0.3)
        w.border_width = 0.5
        page4.add_widget(w)
        y += 75

    doc.save(STUDENT_PDF)
    doc.close()
    print(f"Created student answers PDF: {STUDENT_PDF}")


def create_answer_key():
    """Create answer key JSON with MC answers and SA keywords."""
    answer_key = {
        "mc_answers": {},
        "sa_keywords": {}
    }

    for i in range(30):
        answer_key["mc_answers"][f"mc_{i+1}"] = CORRECT_MC_ANSWERS[i]

    for i in range(10):
        answer_key["sa_keywords"][f"sa_{i+1}"] = {
            "question": SA_QUESTIONS[i],
            "keywords": SA_KEYWORDS[i],
            "max_points": 5
        }

    with open(ANSWER_KEY_JSON, 'w') as f:
        json.dump(answer_key, f, indent=2)
    print(f"Created answer key: {ANSWER_KEY_JSON}")


def main():
    create_student_pdf()
    create_answer_key()

    # Open PDF in Evince and file manager for context
    launch_gui(f'evince "{STUDENT_PDF}"', delay_sec=2.0)
    launch_gui('nautilus "/home/user/quizzes"', delay_sec=1.0)
    print("GUI_READY: launched Evince and file manager with DISPLAY=:0")


main()
