"""
Initial Setup: Create course_syllabus.pdf for CUA task
Task ID: pdf_basic_098
Domain: pdf
Description: Creates a 12-page course syllabus PDF with realistic content.
             Page 8 contains 'Midterm Exam: March 15' with NO highlight annotation.
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user/Desktop'
TASK_ID = 'pdf_basic_098'
OUTPUT = f'{WORKDIR}/course_syllabus.pdf'


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
    doc = pymupdf.open()

    # ---------------------------------------------------------------------------
    # Page 1 — Course Overview
    # ---------------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    shape = page.new_shape()

    # Title block
    shape.draw_rect(pymupdf.Rect(40, 40, 572, 100))
    shape.finish(color=(0.1, 0.2, 0.5), fill=(0.1, 0.2, 0.5), width=0)
    shape.commit()

    page.insert_text(pymupdf.Point(72, 80), "CS 301: Advanced Software Engineering",
                     fontsize=20, fontname="hebo", color=(1, 1, 1))
    page.insert_text(pymupdf.Point(72, 130), "Course Syllabus — Spring 2025",
                     fontsize=14, fontname="tibo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(72, 160), "Instructor: Prof. Elizabeth Carter   |   Credits: 3",
                     fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 180), "Office: Thornton Hall 214   |   Email: ecarter@university.edu",
                     fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 200), "Office Hours: Mon/Wed 2:00–4:00 PM or by appointment",
                     fontsize=11, fontname="helv", color=(0, 0, 0))

    page.insert_text(pymupdf.Point(72, 240), "Course Description",
                     fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(72, 260, 540, 380),
        "This course provides an in-depth exploration of modern software engineering "
        "principles and practices. Topics include software architecture, design patterns, "
        "agile methodologies, testing strategies, version control workflows, continuous "
        "integration, and deployment pipelines. Students will work in teams to build and "
        "maintain a substantial software project throughout the semester.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page.insert_text(pymupdf.Point(72, 400), "Prerequisites",
                     fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_textbox(
        pymupdf.Rect(72, 420, 540, 480),
        "CS 201 (Data Structures), CS 250 (Computer Organization), or instructor consent. "
        "Students are expected to be proficient in at least one object-oriented language.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page.insert_text(pymupdf.Point(72, 510), "Required Textbooks",
                     fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.5))
    books = [
        "1. Pressman, R. & Maxim, B. — Software Engineering: A Practitioner's Approach, 9th Ed.",
        "2. Martin, R. — Clean Code: A Handbook of Agile Software Craftsmanship",
        "3. Gamma et al. — Design Patterns: Elements of Reusable OO Software",
    ]
    y = 530
    for b in books:
        page.insert_text(pymupdf.Point(72, y), b, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 18

    # ---------------------------------------------------------------------------
    # Page 2 — Learning Objectives
    # ---------------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Learning Objectives",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    objectives = [
        "1. Apply fundamental software engineering principles to real-world development scenarios.",
        "2. Design and evaluate software architectures using established patterns and frameworks.",
        "3. Implement comprehensive test suites including unit, integration, and end-to-end tests.",
        "4. Utilize industry-standard tools: Git, CI/CD pipelines, Docker, and cloud platforms.",
        "5. Collaborate effectively in team settings using agile and scrum methodologies.",
        "6. Analyze software quality metrics and apply refactoring techniques systematically.",
        "7. Communicate technical decisions through written documentation and code reviews.",
        "8. Evaluate trade-offs in architectural decisions under resource and time constraints.",
    ]
    y = 110
    for obj in objectives:
        page.insert_textbox(pymupdf.Rect(72, y, 540, y + 32),
                            obj, fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 38

    # ---------------------------------------------------------------------------
    # Page 3 — Grading Policy
    # ---------------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Grading Policy",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    grade_items = [
        ("Component", "Weight", "Description"),
        ("Programming Assignments (5)", "25%", "Individual coding tasks"),
        ("Team Project — Phase 1", "10%", "Requirements & Architecture"),
        ("Team Project — Phase 2", "15%", "Implementation & Testing"),
        ("Team Project — Phase 3", "10%", "Deployment & Presentation"),
        ("Midterm Exam", "20%", "Closed-book written exam"),
        ("Final Exam", "15%", "Comprehensive, closed-book"),
        ("Participation & Quizzes", "5%", "Weekly quizzes & attendance"),
    ]

    y = 110
    col_x = [72, 280, 380]
    # Header row
    for col, (hdr, x) in enumerate(zip(grade_items[0], col_x)):
        page.insert_text(pymupdf.Point(x, y), hdr, fontsize=11, fontname="hebo", color=(1, 1, 1))
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(68, 95, 544, 115))
    shape.finish(color=(0.1, 0.2, 0.5), fill=(0.1, 0.2, 0.5), width=0)
    shape.commit()
    for col, (hdr, x) in enumerate(zip(grade_items[0], col_x)):
        page.insert_text(pymupdf.Point(x, y), hdr, fontsize=11, fontname="hebo", color=(1, 1, 1))

    y = 130
    for i, row in enumerate(grade_items[1:]):
        fill = (0.93, 0.95, 0.98) if i % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(68, y - 12, 544, y + 8))
        shape.finish(color=None, fill=fill, width=0)
        shape.commit()
        for val, x in zip(row, col_x):
            page.insert_text(pymupdf.Point(x, y), val, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    y += 20
    page.insert_text(pymupdf.Point(72, y), "Grading Scale",
                     fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.5))
    y += 20
    scale = [("A", "93–100"), ("A-", "90–92"), ("B+", "87–89"), ("B", "83–86"),
             ("B-", "80–82"), ("C+", "77–79"), ("C", "73–76"), ("C-", "70–72"),
             ("D", "60–69"), ("F", "< 60")]
    sx = 72
    for i, (grade, rng) in enumerate(scale):
        page.insert_text(pymupdf.Point(sx, y), f"{grade}: {rng}", fontsize=10,
                         fontname="helv", color=(0, 0, 0))
        sx += 55
        if i == 4:
            sx = 72
            y += 18

    # ---------------------------------------------------------------------------
    # Page 4 — Course Schedule (Weeks 1–4)
    # ---------------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Course Schedule",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    weeks_1_4 = [
        ("Week 1", "Jan 13–17", "Course Introduction; Software Process Models",
         "Pressman Ch. 1–2"),
        ("Week 2", "Jan 20–24", "Requirements Engineering; Use Cases",
         "Pressman Ch. 4–5"),
        ("Week 3", "Jan 27–31", "Software Architecture; Layered Design",
         "Pressman Ch. 8–9"),
        ("Week 4", "Feb 3–7", "Design Patterns: Creational & Structural",
         "Gamma Ch. 1–3"),
    ]
    y = 110
    col_x = [72, 140, 230, 420]
    col_hdrs = ["Week", "Dates", "Topics", "Reading"]
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(68, 95, 544, 115))
    shape.finish(color=(0.2, 0.4, 0.6), fill=(0.2, 0.4, 0.6), width=0)
    shape.commit()
    for hdr, x in zip(col_hdrs, col_x):
        page.insert_text(pymupdf.Point(x, y), hdr, fontsize=10, fontname="hebo", color=(1, 1, 1))

    y = 130
    for i, row in enumerate(weeks_1_4):
        fill = (0.95, 0.97, 1.0) if i % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(68, y - 12, 544, y + 20))
        shape.finish(color=None, fill=fill, width=0)
        shape.commit()
        page.insert_text(pymupdf.Point(col_x[0], y), row[0], fontsize=9, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(col_x[1], y), row[1], fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_textbox(pymupdf.Rect(col_x[2], y - 10, col_x[3] - 5, y + 22),
                            row[2], fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_textbox(pymupdf.Rect(col_x[3], y - 10, 544, y + 22),
                            row[3], fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 38

    # ---------------------------------------------------------------------------
    # Page 5 — Course Schedule (Weeks 5–8)
    # ---------------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Course Schedule (continued)",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    weeks_5_8 = [
        ("Week 5", "Feb 10–14", "Design Patterns: Behavioral; Observer, Strategy",
         "Gamma Ch. 4–5"),
        ("Week 6", "Feb 17–21", "Software Testing: Unit & Integration Testing",
         "Pressman Ch. 18"),
        ("Week 7", "Feb 24–28", "Test-Driven Development; Mocking Frameworks",
         "Martin Ch. 9"),
        ("Week 8", "Mar 3–7", "Continuous Integration & Delivery Pipelines",
         "Online resources"),
    ]
    y = 110
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(68, 95, 544, 115))
    shape.finish(color=(0.2, 0.4, 0.6), fill=(0.2, 0.4, 0.6), width=0)
    shape.commit()
    for hdr, x in zip(col_hdrs, col_x):
        page.insert_text(pymupdf.Point(x, y), hdr, fontsize=10, fontname="hebo", color=(1, 1, 1))

    y = 130
    for i, row in enumerate(weeks_5_8):
        fill = (0.95, 0.97, 1.0) if i % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(68, y - 12, 544, y + 20))
        shape.finish(color=None, fill=fill, width=0)
        shape.commit()
        page.insert_text(pymupdf.Point(col_x[0], y), row[0], fontsize=9, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(col_x[1], y), row[1], fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_textbox(pymupdf.Rect(col_x[2], y - 10, col_x[3] - 5, y + 22),
                            row[2], fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_textbox(pymupdf.Rect(col_x[3], y - 10, 544, y + 22),
                            row[3], fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 38

    y += 20
    page.insert_text(pymupdf.Point(72, y), "Assignment 1 Due: February 7",
                     fontsize=11, fontname="hebo", color=(0.7, 0.1, 0.1))
    y += 20
    page.insert_text(pymupdf.Point(72, y), "Assignment 2 Due: February 21",
                     fontsize=11, fontname="hebo", color=(0.7, 0.1, 0.1))

    # ---------------------------------------------------------------------------
    # Page 6 — Programming Assignments
    # ---------------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Programming Assignments",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    assignments = [
        ("PA1", "Feb 7", "Implement three GOF design patterns; unit tests required."),
        ("PA2", "Feb 21", "Refactor a legacy codebase; apply clean code principles."),
        ("PA3", "Mar 7", "Build a REST API with full test coverage (>= 85%)."),
        ("PA4", "Mar 28", "Containerize an application using Docker and Docker Compose."),
        ("PA5", "Apr 11", "Set up a CI/CD pipeline using GitHub Actions."),
    ]
    y = 110
    for pa, due, desc in assignments:
        page.insert_text(pymupdf.Point(72, y), f"{pa} — Due: {due}",
                         fontsize=12, fontname="hebo", color=(0.2, 0.4, 0.6))
        y += 18
        page.insert_textbox(pymupdf.Rect(88, y, 540, y + 28),
                            desc, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 38

    y += 10
    page.insert_text(pymupdf.Point(72, y), "Late Policy",
                     fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.5))
    y += 18
    page.insert_textbox(
        pymupdf.Rect(72, y, 540, y + 60),
        "Assignments submitted late will be penalized 10% per day, up to a maximum of 50%. "
        "No submissions are accepted after 5 days past the deadline unless a medical or "
        "family emergency extension has been granted in writing by the instructor.",
        fontsize=10, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # ---------------------------------------------------------------------------
    # Page 7 — Team Project Details
    # ---------------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Team Project",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    page.insert_textbox(
        pymupdf.Rect(72, 100, 540, 160),
        "Teams of 4–5 students will build a web application over three phases. Teams will "
        "be assigned by the instructor to ensure skill diversity. Each team must maintain a "
        "shared GitHub repository with meaningful commit history and branch protection rules.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    phases = [
        ("Phase 1 — Due: February 28", "10%",
         "Project proposal, system requirements document, high-level architecture diagram, "
         "and initial repository setup with CI pipeline."),
        ("Phase 2 — Due: April 4", "15%",
         "Functional implementation of core features, test suite with >= 80% coverage, "
         "code review documentation, and sprint retrospective report."),
        ("Phase 3 — Due: May 2", "10%",
         "Production deployment to cloud platform, performance benchmarks, final presentation "
         "(15 minutes), and peer evaluation forms."),
    ]
    y = 180
    for title, weight, desc in phases:
        page.insert_text(pymupdf.Point(72, y), f"{title}  ({weight})",
                         fontsize=12, fontname="hebo", color=(0.2, 0.4, 0.6))
        y += 18
        page.insert_textbox(pymupdf.Rect(88, y, 540, y + 44),
                            desc, fontsize=10, fontname="helv", color=(0, 0, 0),
                            align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 54

    # ---------------------------------------------------------------------------
    # Page 8 — Midterm Exam Information  ← KEY PAGE
    # ---------------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Examinations",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    page.insert_text(pymupdf.Point(72, 110), "Midterm Examination",
                     fontsize=13, fontname="hebo", color=(0.2, 0.4, 0.6))

    # *** THE TARGET LINE — NO HIGHLIGHT IN INITIAL ***
    page.insert_text(pymupdf.Point(72, 132), "Midterm Exam: March 15",
                     fontsize=12, fontname="hebo", color=(0, 0, 0))

    page.insert_text(pymupdf.Point(72, 152), "Time: 7:00 PM – 9:00 PM   |   Location: Thompson Hall 101",
                     fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_textbox(
        pymupdf.Rect(72, 172, 540, 280),
        "The midterm examination covers all material from Weeks 1 through 7. It is closed-book "
        "and closed-notes. Students may bring one 3×5 index card (hand-written, both sides). "
        "Calculators are not permitted. The exam consists of 40 multiple-choice questions (50%), "
        "three short-answer questions (30%), and one design problem (20%). Students must bring "
        "their university ID. Seating assignments will be posted 24 hours before the exam.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page.insert_text(pymupdf.Point(72, 300), "Midterm Review Session",
                     fontsize=12, fontname="hebo", color=(0.2, 0.4, 0.6))
    page.insert_text(pymupdf.Point(72, 320), "Date: March 12   |   Time: 6:00 PM – 8:00 PM",
                     fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 340), "Location: Thornton Hall 210 (Computer Lab)",
                     fontsize=11, fontname="helv", color=(0, 0, 0))

    page.insert_text(pymupdf.Point(72, 380), "Final Examination",
                     fontsize=13, fontname="hebo", color=(0.2, 0.4, 0.6))
    page.insert_text(pymupdf.Point(72, 400), "Final Exam: May 12",
                     fontsize=12, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 420), "Time: 10:30 AM – 12:30 PM   |   Location: Thompson Hall 101",
                     fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_textbox(
        pymupdf.Rect(72, 440, 540, 540),
        "The final exam is comprehensive, covering all course material. Same closed-book policy "
        "applies. Students may bring two 3×5 index cards. The exam has 50 multiple-choice "
        "questions (40%), four short-answer problems (35%), and one comprehensive design/analysis "
        "question (25%). Practice exams will be provided on the course portal.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page.insert_text(pymupdf.Point(72, 560), "Academic Integrity on Exams",
                     fontsize=12, fontname="hebo", color=(0.2, 0.4, 0.6))
    page.insert_textbox(
        pymupdf.Rect(72, 580, 540, 650),
        "Any form of cheating will result in an automatic F for the course and referral to the "
        "Office of Academic Integrity. Students must certify their honor pledge on each exam booklet.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # ---------------------------------------------------------------------------
    # Page 9 — Course Policies
    # ---------------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Course Policies",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    policies = [
        ("Attendance", "Regular attendance is expected. More than 3 unexcused absences will reduce "
         "your participation grade by 2% per absence."),
        ("Electronics", "Laptops and tablets are permitted for note-taking and coding exercises. "
         "Cell phones must be silenced and put away during class."),
        ("Academic Integrity", "All work submitted must be your own. Collaboration is permitted on "
         "team projects only. Using AI tools to generate assignment code is not permitted unless "
         "explicitly authorized by the instructor."),
        ("Accommodations", "Students needing accommodations should contact the Disability Services "
         "Office and provide documentation to the instructor within the first two weeks of class."),
        ("Communication", "Announcements are posted to the course portal. Email responses within "
         "48 hours on business days. Office hours are the preferred forum for technical questions."),
    ]
    y = 110
    for title, text in policies:
        page.insert_text(pymupdf.Point(72, y), title,
                         fontsize=12, fontname="hebo", color=(0.2, 0.4, 0.6))
        y += 18
        page.insert_textbox(pymupdf.Rect(88, y, 540, y + 46),
                            text, fontsize=10, fontname="helv", color=(0, 0, 0),
                            align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 56

    # ---------------------------------------------------------------------------
    # Page 10 — Recommended Resources
    # ---------------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Recommended Resources",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    resources = [
        "Online Platforms:",
        "  • LeetCode (algorithmic practice)",
        "  • GitHub Learning Lab (Git workflows)",
        "  • Docker Hub documentation",
        "  • AWS Free Tier (cloud deployment)",
        "",
        "Reference Books:",
        "  • Fowler, M. — Refactoring: Improving the Design of Existing Code",
        "  • Beck, K. — Test-Driven Development: By Example",
        "  • Vernon, V. — Implementing Domain-Driven Design",
        "  • Nygard, M. — Release It! Design and Deploy Production-Ready Software",
        "",
        "Video Courses:",
        "  • MIT OpenCourseWare: 6.005 Software Construction",
        "  • Coursera: Software Design and Architecture (University of Alberta)",
        "  • YouTube: GOTO Conferences (Architecture & Best Practices talks)",
    ]
    y = 110
    for res in resources:
        if res == "":
            y += 8
            continue
        fontname = "hebo" if not res.startswith("  ") else "helv"
        color = (0.1, 0.2, 0.5) if not res.startswith("  ") else (0, 0, 0)
        page.insert_text(pymupdf.Point(72, y), res, fontsize=11, fontname=fontname, color=color)
        y += 18

    # ---------------------------------------------------------------------------
    # Page 11 — Schedule Weeks 9–13
    # ---------------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Course Schedule (continued)",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    weeks_9_13 = [
        ("Week 9",  "Mar 17–21", "Software Metrics & Code Quality Analysis",  "Pressman Ch. 23"),
        ("Week 10", "Mar 24–28", "Containerization & Microservices Architecture", "Online docs"),
        ("Week 11", "Mar 31–Apr 4", "Cloud Deployment: AWS/GCP/Azure Overview", "Online docs"),
        ("Week 12", "Apr 7–11",  "Security Engineering; OWASP Top 10",        "Pressman Ch. 29"),
        ("Week 13", "Apr 14–18", "Performance Engineering & Scalability",      "Nygard Ch. 4–6"),
    ]
    y = 110
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(68, 95, 544, 115))
    shape.finish(color=(0.2, 0.4, 0.6), fill=(0.2, 0.4, 0.6), width=0)
    shape.commit()
    for hdr, x in zip(col_hdrs, col_x):
        page.insert_text(pymupdf.Point(x, y), hdr, fontsize=10, fontname="hebo", color=(1, 1, 1))

    y = 130
    for i, row in enumerate(weeks_9_13):
        fill = (0.95, 0.97, 1.0) if i % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(68, y - 12, 544, y + 20))
        shape.finish(color=None, fill=fill, width=0)
        shape.commit()
        page.insert_text(pymupdf.Point(col_x[0], y), row[0], fontsize=9, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(col_x[1], y), row[1], fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_textbox(pymupdf.Rect(col_x[2], y - 10, col_x[3] - 5, y + 22),
                            row[2], fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_textbox(pymupdf.Rect(col_x[3], y - 10, 544, y + 22),
                            row[3], fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 38

    y += 20
    page.insert_text(pymupdf.Point(72, y), "Assignment 4 Due: March 28",
                     fontsize=11, fontname="hebo", color=(0.7, 0.1, 0.1))
    y += 20
    page.insert_text(pymupdf.Point(72, y), "Assignment 5 Due: April 11",
                     fontsize=11, fontname="hebo", color=(0.7, 0.1, 0.1))
    y += 20
    page.insert_text(pymupdf.Point(72, y), "Team Project Phase 2 Due: April 4",
                     fontsize=11, fontname="hebo", color=(0.7, 0.1, 0.1))

    # ---------------------------------------------------------------------------
    # Page 12 — Important Dates & Contact
    # ---------------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Important Dates & Contact Information",
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape.commit()

    dates = [
        ("Jan 13", "First day of class"),
        ("Jan 20", "Last day to add/drop (no record)"),
        ("Feb 7",  "Assignment 1 due"),
        ("Feb 14", "Last day to withdraw (W grade)"),
        ("Feb 21", "Assignment 2 due"),
        ("Feb 28", "Team Project Phase 1 due"),
        ("Mar 7",  "Assignment 3 due"),
        ("Mar 10–14", "Spring Recess — No Classes"),
        ("Mar 15", "Midterm Exam — 7:00 PM"),
        ("Mar 28", "Assignment 4 due"),
        ("Apr 4",  "Team Project Phase 2 due"),
        ("Apr 11", "Assignment 5 due"),
        ("Apr 25", "Last day of class"),
        ("May 2",  "Team Project Phase 3 due"),
        ("May 12", "Final Exam — 10:30 AM"),
    ]
    y = 110
    for date, event in dates:
        shape = page.new_shape()
        fill = (0.95, 0.97, 1.0) if dates.index((date, event)) % 2 == 0 else (1, 1, 1)
        shape.draw_rect(pymupdf.Rect(68, y - 10, 544, y + 6))
        shape.finish(color=None, fill=fill, width=0)
        shape.commit()
        page.insert_text(pymupdf.Point(72, y), date, fontsize=10, fontname="hebo", color=(0.2, 0.4, 0.6))
        page.insert_text(pymupdf.Point(160, y), event, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 20

    y += 20
    page.insert_text(pymupdf.Point(72, y), "Teaching Assistants",
                     fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.5))
    y += 20
    tas = [
        ("Marcus Thompson",    "mthompson@university.edu", "Mon 4–6 PM, Room 310"),
        ("Priya Nair",         "pnair@university.edu",     "Wed 10 AM–12 PM, Room 305"),
        ("Jordan Williams",    "jwilliams@university.edu", "Thu 2–4 PM, Online (Zoom)"),
    ]
    for name, email, hours in tas:
        page.insert_text(pymupdf.Point(72, y), f"{name}   {email}   OH: {hours}",
                         fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 18

    # ---------------------------------------------------------------------------
    # Set document metadata and TOC
    # ---------------------------------------------------------------------------
    doc.set_metadata({
        "title": "CS 301: Advanced Software Engineering — Course Syllabus",
        "author": "Prof. Elizabeth Carter",
        "subject": "Course Syllabus Spring 2025",
        "keywords": "syllabus, software engineering, CS301, spring 2025",
        "creator": "University Academic Publishing System",
        "producer": "PyMuPDF",
    })

    toc = [
        [1, "Course Overview", 1],
        [1, "Learning Objectives", 2],
        [1, "Grading Policy", 3],
        [1, "Course Schedule", 4],
        [1, "Programming Assignments", 6],
        [1, "Team Project", 7],
        [1, "Examinations", 8],
        [1, "Course Policies", 9],
        [1, "Recommended Resources", 10],
        [1, "Important Dates", 12],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial PDF created: {OUTPUT}')
    print(f'Page count: 12')

    # GUI-ready startup: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
