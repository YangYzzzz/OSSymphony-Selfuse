"""
Initial Setup: Create an 8-page proofreading draft PDF with instances of 'their', 'there', and 'they're'.
Task ID: pdf_res_043
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_043'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/proofreading_draft.pdf'

# Page dimensions (Letter)
W, H = 612, 792

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
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Content for 8 pages of a research draft paper.
    # Words 'their', 'there', 'they're' appear 18 times total across pages.
    # Distribution: their x8, there x7, they're x3 = 18

    pages_content = [
        # Page 1: Title page and abstract
        (
            "Collaborative Learning in Modern Organizations:\n"
            "A Study of Team Dynamics and Productivity\n\n"
            "Dr. Elena Vasquez, Prof. Marcus Chen, Dr. Anita Patel\n"
            "Department of Organizational Psychology\n"
            "Westfield University\n\n"
            "Abstract\n\n"
            "This paper examines how employees collaborate in cross-functional teams "
            "and the factors that influence their productivity. Recent studies suggest that "  # their (1)
            "organizations must adapt their management strategies to accommodate evolving "   # their (2)
            "workplace dynamics. There is growing evidence that team composition plays a "    # there (1)
            "critical role in determining project outcomes. In this study, we surveyed 450 "
            "professionals across twelve industries to understand how collaborative "
            "frameworks impact organizational performance. Our findings indicate that "
            "structured mentorship programs significantly enhance team cohesion and output "
            "quality."
        ),

        # Page 2: Introduction
        (
            "1. Introduction\n\n"
            "The modern workplace has undergone significant transformations over the past "
            "two decades. Organizations worldwide are re-evaluating their approaches to team "  # their (3)
            "management and collaboration. There are multiple frameworks that attempt to "       # there (2)
            "quantify the effectiveness of various collaboration models, yet few have been "
            "tested in longitudinal studies spanning more than five years.\n\n"
            "Cross-functional teams bring together individuals from diverse backgrounds, each "
            "contributing unique perspectives. When managed effectively, they're capable of "    # they're (1)
            "producing innovative solutions that no single department could achieve alone. "
            "However, challenges arise when communication barriers hinder knowledge sharing.\n\n"
            "Previous research by Nakamura et al. (2021) demonstrated that teams with clearly "
            "defined roles outperform those without structured hierarchies. Their findings "     # their (4)
            "align with our preliminary observations, suggesting that role clarity reduces "
            "conflict and improves decision-making speed."
        ),

        # Page 3: Literature Review
        (
            "2. Literature Review\n\n"
            "Extensive research has been conducted on collaborative work environments. "
            "Harrison and Liu (2019) explored how virtual teams maintain cohesion when "
            "members are geographically dispersed. There is consensus among researchers "  # there (3)
            "that regular synchronous communication is essential for virtual team success.\n\n"
            "Furthermore, Park and Okafor (2020) investigated the role of psychological "
            "safety in team innovation. They found that teams where members feel safe to "
            "express dissenting opinions generate 34% more viable ideas. They're particularly "  # they're (2)
            "effective when leadership actively encourages constructive disagreement.\n\n"
            "In contrast, Thompson (2018) argued that excessive collaboration can lead to "
            "decision fatigue and reduced individual accountability. His critique highlights "
            "the need for balanced approaches that preserve individual autonomy while "
            "promoting collective intelligence. There remain significant gaps in understanding "  # there (4)
            "how to calibrate collaboration intensity across different project phases."
        ),

        # Page 4: Methodology
        (
            "3. Methodology\n\n"
            "3.1 Participants\n\n"
            "A total of 450 professionals participated in this study, drawn from twelve "
            "industries including technology, healthcare, finance, and manufacturing. "
            "Participants were required to have at least three years of experience working "
            "in cross-functional teams. Their ages ranged from 25 to 58, with a mean age "  # their (5)
            "of 37.4 years (SD = 8.2).\n\n"
            "3.2 Survey Design\n\n"
            "We developed a 72-item questionnaire covering five dimensions of collaborative "
            "work: communication frequency, role clarity, conflict resolution strategies, "
            "knowledge sharing practices, and perceived team effectiveness. Each dimension "
            "was assessed using validated scales from prior research.\n\n"
            "3.3 Data Collection\n\n"
            "Surveys were distributed electronically over a six-month period from January "
            "to June 2024. There were two follow-up reminders sent at three-week intervals "  # there (5)
            "to maximize response rates. The final response rate was 78.2%, which exceeds "
            "the recommended threshold for organizational research."
        ),

        # Page 5: Results (Part 1)
        (
            "4. Results\n\n"
            "4.1 Communication Patterns\n\n"
            "Analysis of communication frequency data revealed three distinct clusters among "
            "the participating teams. High-performing teams maintained daily synchronous "
            "check-ins and used asynchronous tools for documentation. Their communication "  # their (6)
            "patterns showed a 2:1 ratio of informal to formal interactions.\n\n"
            "Medium-performing teams communicated less frequently, averaging three synchronous "
            "meetings per week. While they're not as tightly coordinated as top performers, "  # they're (3)
            "these teams still produced above-average results when project scope was well "
            "defined.\n\n"
            "4.2 Role Clarity and Conflict\n\n"
            "Teams with clearly documented role definitions experienced 41% fewer "
            "interpersonal conflicts compared to those with ambiguous role boundaries. "
            "Interestingly, there was no significant correlation between team size and "  # there (6)
            "conflict frequency after controlling for role clarity. This suggests that "
            "structured role assignment is more impactful than reducing team size."
        ),

        # Page 6: Results (Part 2)
        (
            "4.3 Knowledge Sharing\n\n"
            "Knowledge sharing practices varied substantially across industries. Technology "
            "sector teams demonstrated the highest rates of knowledge exchange, with 89% of "
            "respondents reporting regular documentation of lessons learned. Healthcare teams "
            "ranked second at 76%, followed by finance at 68%.\n\n"
            "Teams that implemented structured knowledge repositories reported 28% faster "
            "onboarding times for new members. Their project completion rates improved by "  # their (7)
            "an average of 15% compared to teams relying solely on informal knowledge "
            "transfer.\n\n"
            "4.4 Perceived Effectiveness\n\n"
            "Self-reported team effectiveness scores ranged from 2.1 to 4.8 on a 5-point "
            "Likert scale. The mean effectiveness score was 3.7 (SD = 0.9). Regression "
            "analysis revealed that communication frequency and role clarity together "
            "accounted for 52% of the variance in perceived effectiveness scores. There "  # there (7)
            "were notable differences across industry sectors, with technology and healthcare "
            "teams rating their effectiveness significantly higher than manufacturing teams."
        ),

        # Page 7: Discussion
        (
            "5. Discussion\n\n"
            "Our findings contribute to the growing body of evidence supporting structured "
            "collaboration frameworks. The strong association between communication frequency "
            "and team performance underscores the importance of intentional interaction design "
            "in organizational settings.\n\n"
            "Notably, the diminishing returns observed at very high communication frequencies "
            "suggest that organizations should avoid mandating excessive meetings. Instead, "
            "teams should be empowered to calibrate their own interaction schedules based on "  # their (8)
            "project demands and member preferences.\n\n"
            "The role clarity findings have direct implications for human resource practices. "
            "Organizations investing in detailed job descriptions and responsibility matrices "
            "can expect measurable improvements in team harmony and output quality. These "
            "results align with the framework proposed by Nakamura et al. (2021) and extend "
            "it by demonstrating applicability across multiple industry contexts.\n\n"
            "5.1 Limitations\n\n"
            "This study relies on self-reported data, which is subject to social desirability "
            "bias. Additionally, the cross-sectional design limits our ability to establish "
            "causal relationships. Future longitudinal studies should track teams over multiple "
            "project cycles to better understand temporal dynamics."
        ),

        # Page 8: Conclusion and References
        (
            "6. Conclusion\n\n"
            "This study provides empirical evidence that structured collaboration frameworks "
            "significantly enhance team performance across diverse industries. Communication "
            "frequency, role clarity, and knowledge sharing practices emerge as the three "
            "pillars of effective teamwork. Organizations seeking to improve productivity "
            "should focus on creating environments that foster regular interaction while "
            "maintaining clear accountability structures.\n\n"
            "Future research should explore the impact of emerging technologies, such as "
            "AI-assisted project management tools, on team collaboration dynamics.\n\n\n"
            "References\n\n"
            "Harrison, R., & Liu, W. (2019). Virtual team cohesion in distributed "
            "organizations. Journal of Applied Psychology, 104(3), 289-301.\n\n"
            "Nakamura, T., Singh, P., & Olsen, K. (2021). Role clarity and team performance: "
            "A meta-analysis. Organizational Behavior Review, 38(2), 145-167.\n\n"
            "Park, J., & Okafor, C. (2020). Psychological safety and innovation in "
            "cross-functional teams. Academy of Management Journal, 63(4), 1023-1048.\n\n"
            "Thompson, D. (2018). The collaboration paradox: When teamwork undermines "
            "individual performance. Harvard Business Review, 96(5), 82-91."
        ),
    ]

    # Create each page
    for i, content in enumerate(pages_content):
        page = doc.new_page(width=W, height=H)
        # Page margins
        margin_left = 72
        margin_top = 72
        margin_right = W - 72
        margin_bottom = H - 72

        rect = pymupdf.Rect(margin_left, margin_top, margin_right, margin_bottom)

        if i == 0:
            # Title page: center the title block, then body text
            # Title
            title_rect = pymupdf.Rect(margin_left, 100, margin_right, 160)
            page.insert_textbox(
                title_rect,
                "Collaborative Learning in Modern Organizations:\nA Study of Team Dynamics and Productivity",
                fontsize=16,
                fontname="tibo",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )
            # Authors
            author_rect = pymupdf.Rect(margin_left, 175, margin_right, 240)
            page.insert_textbox(
                author_rect,
                "Dr. Elena Vasquez, Prof. Marcus Chen, Dr. Anita Patel\nDepartment of Organizational Psychology\nWestfield University",
                fontsize=11,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )
            # Abstract heading
            page.insert_text(pymupdf.Point(margin_left, 290), "Abstract", fontsize=13, fontname="tibo", color=(0, 0, 0))
            # Abstract body
            abstract_text = (
                "This paper examines how employees collaborate in cross-functional teams "
                "and the factors that influence their productivity. Recent studies suggest that "
                "organizations must adapt their management strategies to accommodate evolving "
                "workplace dynamics. There is growing evidence that team composition plays a "
                "critical role in determining project outcomes. In this study, we surveyed 450 "
                "professionals across twelve industries to understand how collaborative "
                "frameworks impact organizational performance. Our findings indicate that "
                "structured mentorship programs significantly enhance team cohesion and output "
                "quality."
            )
            abstract_rect = pymupdf.Rect(margin_left, 305, margin_right, margin_bottom)
            page.insert_textbox(abstract_rect, abstract_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        else:
            # Normal content pages
            lines = content.split('\n')
            y_pos = margin_top

            for line in lines:
                if not line.strip():
                    y_pos += 8
                    continue

                # Detect headings
                is_main_heading = line.strip() and line.strip()[0].isdigit() and '.' in line.strip()[:3] and len(line.strip()) < 60 and not line.strip()[0:3].replace('.', '').replace(' ', '').isdigit() == False
                is_section = line.startswith(('1.', '2.', '3.', '4.', '5.', '6.'))
                is_subsection = line.startswith(('3.1', '3.2', '3.3', '4.1', '4.2', '4.3', '4.4', '5.1'))

                if is_subsection and len(line.strip()) < 60:
                    y_pos += 6
                    page.insert_text(pymupdf.Point(margin_left, y_pos), line.strip(), fontsize=12, fontname="tibo", color=(0, 0, 0))
                    y_pos += 18
                elif is_section and len(line.strip()) < 60:
                    page.insert_text(pymupdf.Point(margin_left, y_pos), line.strip(), fontsize=14, fontname="tibo", color=(0, 0, 0))
                    y_pos += 22
                elif line.strip() == 'References':
                    page.insert_text(pymupdf.Point(margin_left, y_pos), line.strip(), fontsize=14, fontname="tibo", color=(0, 0, 0))
                    y_pos += 22
                else:
                    # Body text in textbox for wrapping
                    text_rect = pymupdf.Rect(margin_left, y_pos, margin_right, y_pos + 200)
                    excess = page.insert_textbox(text_rect, line.strip(), fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
                    # Estimate lines used
                    chars_per_line = 85
                    num_lines = max(1, (len(line.strip()) + chars_per_line - 1) // chars_per_line)
                    y_pos += num_lines * 14 + 4

                if y_pos > margin_bottom - 20:
                    break

    # Add page numbers
    for i in range(doc.page_count):
        page = doc[i]
        page.insert_text(
            pymupdf.Point(W / 2 - 5, H - 40),
            str(i + 1),
            fontsize=10,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify word counts
    doc = pymupdf.open(OUTPUT)
    count = 0
    for page in doc:
        text = page.get_text("text").lower()
        count += text.count('their')
        count += text.count('there')
        count += text.count("they're")
        # Remove double-counts: 'their' contains 'the' but not 'there'; 'there' does not contain 'their'
    doc.close()
    print(f'Total occurrences of target words: {count}')

    # Open in Evince for agent interaction
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
