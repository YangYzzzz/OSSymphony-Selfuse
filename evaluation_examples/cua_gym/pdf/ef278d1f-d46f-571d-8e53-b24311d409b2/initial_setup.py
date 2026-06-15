"""
Initial Setup: Create a 4-page filled survey PDF form with 15 form fields
Task ID: pdf_pw_029
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_029'
FORMS_DIR = f'{WORKDIR}/forms'
OUTPUT = f'{FORMS_DIR}/completed_survey.pdf'


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
    os.makedirs(FORMS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ---- PAGE 1: Personal Information ----
    page1 = doc.new_page(width=612, height=792)  # Letter size

    # Title
    page1.insert_text(pymupdf.Point(72, 50), "Community Engagement Survey 2025",
                      fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.5))
    page1.insert_text(pymupdf.Point(72, 75), "Section 1: Personal Information",
                      fontsize=14, fontname="hebo", color=(0.2, 0.2, 0.2))

    # Horizontal rule
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 85), pymupdf.Point(540, 85))
    shape.finish(color=(0.5, 0.5, 0.5), width=1)
    shape.commit()

    # Field 1: Full Name (text)
    page1.insert_text(pymupdf.Point(72, 115), "Full Name:", fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "full_name"
    w.field_value = "Rebecca Martinez"
    w.rect = pymupdf.Rect(200, 100, 500, 122)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    # Field 2: Email Address (text)
    page1.insert_text(pymupdf.Point(72, 155), "Email Address:", fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "email"
    w.field_value = "r.martinez@greenvalley.org"
    w.rect = pymupdf.Rect(200, 140, 500, 162)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    # Field 3: Phone Number (text)
    page1.insert_text(pymupdf.Point(72, 195), "Phone Number:", fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "phone"
    w.field_value = "(503) 555-8214"
    w.rect = pymupdf.Rect(200, 180, 500, 202)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    # Field 4: Age Range (dropdown)
    page1.insert_text(pymupdf.Point(72, 235), "Age Range:", fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
    w.field_name = "age_range"
    w.choice_values = ["Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    w.field_value = "35-44"
    w.rect = pymupdf.Rect(200, 220, 500, 242)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    # Field 5: Neighborhood (text)
    page1.insert_text(pymupdf.Point(72, 275), "Neighborhood:", fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "neighborhood"
    w.field_value = "Hawthorne District"
    w.rect = pymupdf.Rect(200, 260, 500, 282)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page1.add_widget(w)

    # Footer
    page1.insert_text(pymupdf.Point(260, 760), "Page 1 of 4",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ---- PAGE 2: Community Involvement ----
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 50), "Section 2: Community Involvement",
                      fontsize=14, fontname="hebo", color=(0.2, 0.2, 0.2))

    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 60), pymupdf.Point(540, 60))
    shape2.finish(color=(0.5, 0.5, 0.5), width=1)
    shape2.commit()

    # Field 6: Volunteer Hours per Month (text)
    page2.insert_text(pymupdf.Point(72, 95), "Volunteer Hours/Month:", fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "volunteer_hours"
    w.field_value = "12"
    w.rect = pymupdf.Rect(260, 80, 500, 102)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page2.add_widget(w)

    # Field 7: Checkbox - Attended Town Hall
    page2.insert_text(pymupdf.Point(100, 140), "Attended a town hall meeting this year",
                      fontsize=11, fontname="helv")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "attended_town_hall"
    w.field_value = "Yes"
    w.rect = pymupdf.Rect(72, 127, 92, 147)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page2.add_widget(w)

    # Field 8: Checkbox - Participated in Clean-up
    page2.insert_text(pymupdf.Point(100, 175), "Participated in neighborhood clean-up events",
                      fontsize=11, fontname="helv")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "participated_cleanup"
    w.field_value = "Yes"
    w.rect = pymupdf.Rect(72, 162, 92, 182)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page2.add_widget(w)

    # Field 9: Checkbox - Donated to local charity
    page2.insert_text(pymupdf.Point(100, 210), "Donated to a local charity or nonprofit",
                      fontsize=11, fontname="helv")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = "donated_charity"
    w.field_value = "Off"
    w.rect = pymupdf.Rect(72, 197, 92, 217)
    w.border_color = (0.3, 0.3, 0.3)
    w.border_width = 1
    page2.add_widget(w)

    # Field 10: Preferred Communication (dropdown)
    page2.insert_text(pymupdf.Point(72, 260), "Preferred Communication:", fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
    w.field_name = "preferred_communication"
    w.choice_values = ["Email", "Phone", "Text Message", "Social Media", "Mail"]
    w.field_value = "Email"
    w.rect = pymupdf.Rect(270, 245, 500, 267)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page2.add_widget(w)

    page2.insert_text(pymupdf.Point(260, 760), "Page 2 of 4",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ---- PAGE 3: Satisfaction & Priorities ----
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 50), "Section 3: Satisfaction & Priorities",
                      fontsize=14, fontname="hebo", color=(0.2, 0.2, 0.2))

    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 60), pymupdf.Point(540, 60))
    shape3.finish(color=(0.5, 0.5, 0.5), width=1)
    shape3.commit()

    # Field 11: Overall Satisfaction (radio - simulated with text + text field)
    page3.insert_text(pymupdf.Point(72, 95), "Overall satisfaction with local services:",
                      fontsize=11, fontname="hebo")
    page3.insert_text(pymupdf.Point(90, 115), "Very Satisfied    Satisfied    Neutral    Dissatisfied    Very Dissatisfied",
                      fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "overall_satisfaction"
    w.field_value = "Satisfied"
    w.rect = pymupdf.Rect(72, 130, 300, 152)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page3.add_widget(w)

    # Field 12: Parks and Recreation rating (radio - simulated)
    page3.insert_text(pymupdf.Point(72, 185), "Rate parks and recreation facilities:",
                      fontsize=11, fontname="hebo")
    page3.insert_text(pymupdf.Point(90, 205), "Excellent    Good    Fair    Poor",
                      fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "parks_rating"
    w.field_value = "Good"
    w.rect = pymupdf.Rect(72, 220, 300, 242)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page3.add_widget(w)

    # Field 13: Top Priority (text)
    page3.insert_text(pymupdf.Point(72, 280), "What is your top priority for improvement?",
                      fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "top_priority"
    w.field_value = "Safer bike lanes along Belmont Avenue"
    w.rect = pymupdf.Rect(72, 290, 540, 340)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
    page3.add_widget(w)

    page3.insert_text(pymupdf.Point(260, 760), "Page 3 of 4",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ---- PAGE 4: Additional Comments ----
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(72, 50), "Section 4: Additional Feedback",
                      fontsize=14, fontname="hebo", color=(0.2, 0.2, 0.2))

    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(72, 60), pymupdf.Point(540, 60))
    shape4.finish(color=(0.5, 0.5, 0.5), width=1)
    shape4.commit()

    # Field 14: How did you hear about us (text)
    page4.insert_text(pymupdf.Point(72, 95), "How did you hear about this survey?",
                      fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "heard_about"
    w.field_value = "Flyer at the community center"
    w.rect = pymupdf.Rect(72, 105, 540, 127)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    page4.add_widget(w)

    # Field 15: Additional Comments (text, multiline)
    page4.insert_text(pymupdf.Point(72, 165), "Additional comments or suggestions:",
                      fontsize=11, fontname="hebo")
    w = pymupdf.Widget()
    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    w.field_name = "additional_comments"
    w.field_value = "I would love to see more weekend farmers markets and better street lighting near Foster Road."
    w.rect = pymupdf.Rect(72, 175, 540, 300)
    w.text_fontsize = 11
    w.fill_color = (0.97, 0.97, 0.97)
    w.border_color = (0.4, 0.4, 0.4)
    w.border_width = 1
    w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
    page4.add_widget(w)

    # Thank you message
    page4.insert_text(pymupdf.Point(72, 350),
                      "Thank you for taking the time to complete this survey!",
                      fontsize=12, fontname="hebo", color=(0.1, 0.4, 0.1))
    page4.insert_text(pymupdf.Point(72, 370),
                      "Your feedback helps shape the future of our community.",
                      fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    page4.insert_text(pymupdf.Point(260, 760), "Page 4 of 4",
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Make sure survey_data.json does NOT exist
    json_path = f'{FORMS_DIR}/survey_data.json'
    if os.path.exists(json_path):
        os.remove(json_path)

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
