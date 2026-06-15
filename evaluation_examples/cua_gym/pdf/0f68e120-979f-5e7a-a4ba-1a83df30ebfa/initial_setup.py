#!/usr/bin/env python3
"""
initial_setup.py for pdf_basic_137
Creates ~/Desktop/interview_questions.pdf — an 8-page interview preparation
guide with realistic Q&A content. The text 'Tell me about a time' appears on
page 5. Opens the PDF in Evince for the agent to annotate.
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf


def launch_gui(command: str, delay_sec: float = 2.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_interview_pdf(output_path: str):
    """
    Create a realistic 8-page interview preparation PDF.
    Page 5 (index 4) contains the text 'Tell me about a time'.
    No annotations are present in the initial file.
    """
    doc = pymupdf.open()

    W, H = 595, 842
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 72
    MARGIN_TOP = 72
    MARGIN_BOTTOM = 72

    pages_content = [
        # Page 1: Cover / Title
        {
            "type": "cover",
            "title": "Interview Preparation Guide",
            "subtitle": "Comprehensive Q&A for Technical and Behavioral Interviews",
            "note": "Prepared by Career Services Team\nVersion 3.1 — March 2026",
        },
        # Page 2: Table of Contents
        {
            "type": "toc",
            "heading": "Table of Contents",
            "items": [
                "1. Introduction to Interview Types ........ 3",
                "2. Technical Interview Questions .......... 4",
                "3. Behavioral Interview Questions ......... 5",
                "4. Problem-Solving Scenarios .............. 6",
                "5. Leadership & Teamwork Questions ........ 7",
                "6. Closing Questions & Follow-Up .......... 8",
            ],
        },
        # Page 3: Introduction to Interview Types
        {
            "type": "section",
            "heading": "1. Introduction to Interview Types",
            "body": (
                "Understanding the type of interview you are preparing for is the first step toward "
                "success. Interviews broadly fall into three categories: technical interviews, "
                "behavioral interviews, and case/situational interviews.\n\n"
                "Technical interviews assess your domain knowledge, problem-solving ability, and "
                "familiarity with tools and methodologies relevant to the role. Expect coding challenges, "
                "system design questions, and deep dives into your past technical projects.\n\n"
                "Behavioral interviews, on the other hand, focus on how you have acted in past "
                "situations and how you are likely to behave in future scenarios. They are rooted in "
                "the premise that past behavior is the best predictor of future behavior.\n\n"
                "Case interviews, common in consulting and business roles, present you with a "
                "business problem to analyze and solve in real time. They test your analytical "
                "thinking, communication, and ability to work under pressure.\n\n"
                "This guide covers all three types, with particular emphasis on behavioral questions, "
                "which candidates frequently underestimate in their preparation."
            ),
        },
        # Page 4: Technical Interview Questions
        {
            "type": "section",
            "heading": "2. Technical Interview Questions",
            "body": (
                "Technical questions vary widely by role and industry. Below are representative "
                "examples across common technical disciplines.\n\n"
                "Software Engineering:\n"
                "• Explain the difference between a stack and a queue. When would you use each?\n"
                "• What is Big O notation? Analyze the time complexity of binary search.\n"
                "• Describe the MVC (Model-View-Controller) architectural pattern.\n"
                "• What are the SOLID principles? Give an example of the Single Responsibility Principle.\n"
                "• How does garbage collection work in Java or Python?\n\n"
                "Data Science & Analytics:\n"
                "• What is the bias-variance tradeoff? How do you manage it?\n"
                "• Explain the difference between supervised and unsupervised learning.\n"
                "• How would you handle missing data in a dataset?\n"
                "• What is cross-validation and why is it important?\n\n"
                "Infrastructure & DevOps:\n"
                "• What is the difference between containerization and virtualization?\n"
                "• Describe a CI/CD pipeline you have designed or worked with.\n"
                "• How do you monitor application health in production?\n\n"
                "Tip: Always think aloud during technical questions. Interviewers evaluate your "
                "reasoning process, not just the final answer."
            ),
        },
        # Page 5: Behavioral Interview Questions — CONTAINS 'Tell me about a time'
        {
            "type": "section",
            "heading": "3. Behavioral Interview Questions",
            "body": (
                "Behavioral questions are among the most important and frequently mishandled parts "
                "of any interview. They reveal how you approach challenges, collaborate with others, "
                "and grow from experience.\n\n"
                "Common Behavioral Questions:\n\n"
                "Tell me about a time when you had to meet a tight deadline. How did you manage "
                "your workload and what was the outcome?\n\n"
                "Tell me about a time you disagreed with your manager or a team member. How did "
                "you handle the disagreement, and what was the resolution?\n\n"
                "Tell me about a time you failed. What happened, what did you learn, and how did "
                "you apply those lessons going forward?\n\n"
                "Tell me about a time you took initiative on a project or introduced an improvement "
                "that was not explicitly requested. What motivated you and what was the impact?\n\n"
                "How to Answer Using the STAR Method:\n"
                "Situation — Set the context. Describe the setting briefly.\n"
                "Task — Explain your responsibility in that situation.\n"
                "Action — Detail the specific steps you took.\n"
                "Result — Share the outcome. Use metrics where possible.\n\n"
                "Practice Tip: Prepare at least three STAR stories that can be adapted to multiple "
                "question types. Focus on stories that highlight impact, growth, and collaboration."
            ),
        },
        # Page 6: Problem-Solving Scenarios
        {
            "type": "section",
            "heading": "4. Problem-Solving Scenarios",
            "body": (
                "Problem-solving questions test your analytical abilities and creative thinking. "
                "Interviewers are less concerned with the 'correct' answer than with your ability "
                "to structure a problem and reason through it systematically.\n\n"
                "Example Scenarios:\n\n"
                "Scenario A: Your team has just launched a new feature and user engagement has "
                "dropped significantly. How do you diagnose the problem?\n\n"
                "Suggested Approach: Start by clarifying the metrics — what does 'dropped "
                "significantly' mean? Define a baseline. Segment users to see if the drop is "
                "universal or isolated to specific cohorts. Check technical logs for errors. "
                "Survey affected users. Formulate and test hypotheses.\n\n"
                "Scenario B: You are given a dataset of customer transactions. How would you "
                "identify customers at risk of churning?\n\n"
                "Suggested Approach: Define churn for the business context. Identify relevant "
                "features (purchase frequency, recency, support tickets, etc.). Build a predictive "
                "model, validate it, and establish thresholds for intervention.\n\n"
                "Scenario C: A critical production server has gone down at 2 AM. Walk me through "
                "your incident response process.\n\n"
                "Suggested Approach: Assess impact immediately. Page the on-call team. Isolate the "
                "fault. Apply a temporary fix to restore service. Conduct a post-mortem to prevent "
                "recurrence. Document everything."
            ),
        },
        # Page 7: Leadership & Teamwork
        {
            "type": "section",
            "heading": "5. Leadership & Teamwork Questions",
            "body": (
                "Leadership and teamwork questions assess your interpersonal skills, ability to "
                "influence without authority, and capacity to build and sustain productive working "
                "relationships.\n\n"
                "Key Questions to Prepare For:\n\n"
                "Describe a situation in which you had to lead a team through a challenging project. "
                "What was your approach and what did you learn about your leadership style?\n\n"
                "How do you handle conflict within a team? Give a specific example where you "
                "resolved a disagreement constructively.\n\n"
                "Tell me about a time you had to give difficult feedback to a colleague or "
                "direct report. How did you approach the conversation?\n\n"
                "How do you ensure that all team members are aligned and informed during a "
                "complex, multi-stakeholder project?\n\n"
                "What strategies do you use to keep your team motivated during stressful periods?\n\n"
                "Leadership Principles to Emphasize:\n"
                "• Psychological safety — teams perform best when members feel safe to speak up.\n"
                "• Transparency — share information proactively, especially in uncertain situations.\n"
                "• Recognition — acknowledge contributions publicly and specifically.\n"
                "• Accountability — hold yourself and others to clearly defined standards.\n\n"
                "Remember: Leadership is not about title. Demonstrate leadership at any level by "
                "showing ownership, initiative, and care for your teammates."
            ),
        },
        # Page 8: Closing Questions & Follow-Up
        {
            "type": "section",
            "heading": "6. Closing Questions & Follow-Up",
            "body": (
                "The closing phase of an interview is as important as any other part. Thoughtful "
                "questions signal genuine interest and leave a strong final impression.\n\n"
                "Questions to Ask the Interviewer:\n\n"
                "• What does success look like in this role during the first 90 days?\n"
                "• How would you describe the team culture and the way decisions are made?\n"
                "• What are the biggest challenges the team is facing right now?\n"
                "• How do people in this role typically grow and develop their careers here?\n"
                "• What do you enjoy most about working at this company?\n\n"
                "Post-Interview Follow-Up:\n\n"
                "Send a thank-you email within 24 hours of your interview. Reference a specific "
                "topic you discussed to personalize the message. Reiterate your enthusiasm for the "
                "role and the organization. Keep it brief — three to four sentences is appropriate.\n\n"
                "If you have not heard back within the stated timeline, a polite follow-up email "
                "is appropriate. Avoid following up more than once unless the role is time-sensitive.\n\n"
                "Final Checklist Before Your Interview:\n"
                "[ ] Research the company's mission, products, and recent news.\n"
                "[ ] Review the job description and map your experience to each requirement.\n"
                "[ ] Prepare three to five STAR stories covering different competencies.\n"
                "[ ] Test your technology setup if interviewing remotely.\n"
                "[ ] Prepare questions to ask the interviewer.\n"
                "[ ] Get a good night's rest and arrive (or log in) early.\n\n"
                "Good luck with your interview preparation!"
            ),
        },
    ]

    for i, page_data in enumerate(pages_content):
        page = doc.new_page(width=W, height=H)

        if page_data["type"] == "cover":
            # Background header bar
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(0, 0, W, 200))
            shape.finish(color=(0.12, 0.29, 0.55), fill=(0.12, 0.29, 0.55))
            shape.commit()

            # Title text (white on blue)
            page.insert_textbox(
                pymupdf.Rect(MARGIN_LEFT, 60, W - MARGIN_RIGHT, 160),
                page_data["title"],
                fontsize=26,
                fontname="hebo",
                color=(1, 1, 1),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )

            # Subtitle (below header)
            page.insert_textbox(
                pymupdf.Rect(MARGIN_LEFT, 220, W - MARGIN_RIGHT, 290),
                page_data["subtitle"],
                fontsize=14,
                fontname="tiit",
                color=(0.2, 0.2, 0.2),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )

            # Separator line
            shape = page.new_shape()
            shape.draw_line(
                pymupdf.Point(MARGIN_LEFT + 40, 300),
                pymupdf.Point(W - MARGIN_RIGHT - 40, 300),
            )
            shape.finish(color=(0.12, 0.29, 0.55), width=1.5)
            shape.commit()

            # Note / metadata
            page.insert_textbox(
                pymupdf.Rect(MARGIN_LEFT, 320, W - MARGIN_RIGHT, 400),
                page_data["note"],
                fontsize=11,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )

        elif page_data["type"] == "toc":
            # Heading
            page.insert_textbox(
                pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP, W - MARGIN_RIGHT, MARGIN_TOP + 40),
                page_data["heading"],
                fontsize=18,
                fontname="hebo",
                color=(0.12, 0.29, 0.55),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )
            # Underline
            shape = page.new_shape()
            shape.draw_line(
                pymupdf.Point(MARGIN_LEFT, MARGIN_TOP + 46),
                pymupdf.Point(W - MARGIN_RIGHT, MARGIN_TOP + 46),
            )
            shape.finish(color=(0.12, 0.29, 0.55), width=1)
            shape.commit()

            # Items
            y = MARGIN_TOP + 70
            for item in page_data["items"]:
                page.insert_text(
                    pymupdf.Point(MARGIN_LEFT + 20, y),
                    item,
                    fontsize=12,
                    fontname="helv",
                    color=(0, 0, 0),
                )
                y += 30

        else:
            # Section page
            heading = page_data["heading"]
            body = page_data["body"]

            # Heading
            page.insert_textbox(
                pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP, W - MARGIN_RIGHT, MARGIN_TOP + 40),
                heading,
                fontsize=15,
                fontname="hebo",
                color=(0.12, 0.29, 0.55),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )
            # Underline
            shape = page.new_shape()
            shape.draw_line(
                pymupdf.Point(MARGIN_LEFT, MARGIN_TOP + 46),
                pymupdf.Point(W - MARGIN_RIGHT, MARGIN_TOP + 46),
            )
            shape.finish(color=(0.6, 0.7, 0.9), width=0.8)
            shape.commit()

            # Body
            page.insert_textbox(
                pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 58, W - MARGIN_RIGHT, H - MARGIN_BOTTOM),
                body,
                fontsize=10.5,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )

    # Save to Desktop
    os.makedirs(os.path.expanduser("~/Desktop"), exist_ok=True)
    doc.save(output_path)
    doc.close()
    print(f"Created interview_questions.pdf with 8 pages: {output_path}")


def main():
    output_path = os.path.expanduser("~/Desktop/interview_questions.pdf")
    create_interview_pdf(output_path)

    # Verify
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    doc = pymupdf.open(output_path)
    page_count = doc.page_count

    # Verify page 5 (index 4) contains the target text
    p5_text = doc[4].get_text("text")
    doc.close()

    print(f"Verified: {page_count} pages")
    assert page_count == 8, f"Expected 8 pages, got {page_count}"
    assert "Tell me about a time" in p5_text, "Target text not found on page 5"
    print("Verified: 'Tell me about a time' found on page 5")

    # Open at page 5 in Evince (page-index is 0-based, so page 5 = index 4)
    launch_gui(f'evince --page-index=4 "{output_path}"', delay_sec=2.0)
    print("Evince launched at page 5 of interview_questions.pdf")


if __name__ == "__main__":
    main()
