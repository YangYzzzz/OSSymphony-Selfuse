"""
Initial Setup: PDF Author Extract - Multi-App Task
Task ID: osworld_multi_apps_pdf_author_extract_011
Domain: libreoffice_calc (multi-app: PDF files + LibreOffice Calc)

Creates 7 benchmark PDF papers in ~/Documents/Benchmarks/ and opens
Nautilus at that directory plus LibreOffice Calc.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_author_extract_011'
BENCHMARKS_DIR = f'{WORKDIR}/Documents/Benchmarks'


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


def create_pdf_paper(output_path, title, authors_line, author_email, abstract, copyright_line):
    """Create a realistic-looking benchmark paper PDF using reportlab."""
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

    doc = SimpleDocTemplate(
        output_path,
        pagesize=LETTER,
        rightMargin=1 * inch,
        leftMargin=1 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'PaperTitle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
    author_style = ParagraphStyle(
        'Authors',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    email_style = ParagraphStyle(
        'Email',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.blue,
        spaceAfter=14,
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=11,
        leading=14,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )
    copyright_style = ParagraphStyle(
        'Copyright',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=colors.gray,
        spaceAfter=4,
    )

    story = []
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(authors_line, author_style))
    story.append(Paragraph(author_email, email_style))
    story.append(Paragraph("Abstract", section_style))
    story.append(Paragraph(abstract, body_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(copyright_line, copyright_style))

    doc.build(story)
    print(f"  Created: {output_path}")


def create_benchmarks():
    os.makedirs(BENCHMARKS_DIR, exist_ok=True)

    papers = [
        {
            "filename": "imagenet_russakovsky_2015.pdf",
            "title": "ImageNet Large Scale Visual Recognition Challenge",
            "authors_line": "Olga Russakovsky, Jia Deng, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma, Zhiheng Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C. Berg, Li Fei-Fei",
            "author_email": "olga@cs.princeton.edu",
            "abstract": (
                "The ImageNet Large Scale Visual Recognition Challenge (ILSVRC) is a benchmark "
                "in object category classification and detection on hundreds of thousands of images "
                "across thousands of object categories. We present a comprehensive analysis of "
                "results over the five years of the challenge, from 2010 to 2014. We discuss "
                "common misconceptions about the challenge and the dataset, examine how the "
                "community has improved their methods over time, highlight major breakthrough "
                "results, and provide a detailed analysis of the current state of the art. "
                "The challenge has spurred significant advances in machine vision, with deep "
                "convolutional neural networks becoming the dominant approach since AlexNet's "
                "watershed performance in 2012."
            ),
            "copyright_line": "Copyright 2015 International Journal of Computer Vision. Submitted: November 2014. Accepted: January 2015.",
        },
        {
            "filename": "squad_rajpurkar_2016.pdf",
            "title": "SQuAD: 100,000+ Questions for Machine Comprehension of Text",
            "authors_line": "Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, Percy Liang",
            "author_email": "pranavsr@cs.stanford.edu",
            "abstract": (
                "We present the Stanford Question Answering Dataset (SQuAD), a reading "
                "comprehension dataset consisting of questions posed by crowdworkers on a set "
                "of Wikipedia articles, where the answer to every question is a segment of text "
                "from the corresponding reading passage. With 100,000+ question-answer pairs on "
                "500+ articles, SQuAD is significantly larger than previous reading comprehension "
                "datasets. We analyze the types of reasoning required to answer the questions, "
                "and build several powerful models that outperform humans by a large margin. "
                "We also show that models fine-tuned on SQuAD exhibit robust zero-shot "
                "generalization capabilities to related datasets."
            ),
            "copyright_line": "Copyright 2016 Association for Computational Linguistics. Submitted: June 2016. Published: EMNLP 2016.",
        },
        {
            "filename": "glue_wang_2018.pdf",
            "title": "GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding",
            "authors_line": "Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy, Samuel Bowman",
            "author_email": "alexwang@nyu.edu",
            "abstract": (
                "Human language understanding is a long-standing challenge in natural language "
                "processing. Machine learning methods have greatly improved performance on "
                "individual NLU tasks such as natural language inference and sentiment analysis. "
                "However, progress on individual tasks can obscure the fact that these tasks "
                "vary widely in difficulty and that current models are far from human-level "
                "performance across all tasks. We introduce GLUE: the General Language "
                "Understanding Evaluation benchmark, a tool for evaluating and analyzing the "
                "performance of models across a diverse range of existing NLU tasks. GLUE is "
                "model-agnostic but favors models that share representations across tasks, "
                "since the tasks differ in format and genre."
            ),
            "copyright_line": "Copyright 2018 ICLR Workshop on Blackbox NLP. Submitted: September 2018. Published: 2018.",
        },
        {
            "filename": "hellaswag_zellers_2019.pdf",
            "title": "HellaSwag: Can a Machine Really Finish Your Sentence?",
            "authors_line": "Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, Yejin Choi",
            "author_email": "rzellers@cs.washington.edu",
            "abstract": (
                "Recent work by Zellers et al. (2018) introduced a new task of commonsense NLI: "
                "given an event description such as 'A woman sits at a piano', a machine must "
                "select the most likely followup from four choices. While the original task was "
                "designed with the best generation models of the time, we find that language "
                "models now far exceed human accuracy. We present HellaSwag, a more rigorous "
                "evaluation that involves adversarially filtered endings to machine-generated "
                "candidate continuations. Though humans find HellaSwag trivial (95.6% accuracy), "
                "state-of-the-art models struggle (48.0% accuracy). This benchmark reveals "
                "significant gaps in commonsense reasoning abilities of current language models."
            ),
            "copyright_line": "Copyright 2019 Association for Computational Linguistics. Submitted: February 2019. Published: ACL 2019.",
        },
        {
            "filename": "mmlu_hendrycks_2021.pdf",
            "title": "Measuring Massive Multitask Language Understanding",
            "authors_line": "Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, Jacob Steinhardt",
            "author_email": "dan@berkeley.edu",
            "abstract": (
                "We propose a new test to measure a text model's multitask accuracy. The test "
                "covers 57 tasks including elementary mathematics, US history, computer science, "
                "law, and more. To attain high accuracy on this test, models must possess "
                "extensive world knowledge and problem solving ability. We find that while most "
                "recent models have near-random-chance accuracy, the very largest GPT-3 model "
                "improves over random chance by almost 20 percentage points on average. However, "
                "models still have room for improvement, as they fall short of expert-level "
                "accuracy on many individual tasks. This dataset, MMLU, provides a rigorous "
                "benchmark for evaluating the breadth and depth of language model capabilities."
            ),
            "copyright_line": "Copyright 2021 ICLR. Submitted: September 2020. Published: ICLR 2021.",
        },
        {
            "filename": "humaneval_chen_2021.pdf",
            "title": "Evaluating Large Language Models Trained on Code (HumanEval)",
            "authors_line": "Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harrison Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman",
            "author_email": "mark@openai.com",
            "abstract": (
                "We introduce Codex, a GPT language model finetuned on publicly available code "
                "from GitHub, and study its Python code-writing capabilities. A distinct "
                "production version of Codex powers GitHub Copilot. On HumanEval, a new "
                "evaluation set we release to measure functional correctness for synthesizing "
                "programs from docstrings, our model solves 28.8% of the problems, while GPT-3 "
                "solves 0% and GPT-J solves 11.4%. We investigate how to best use generate-and-"
                "filter strategies to further improve functional correctness, achieving 72.3% "
                "pass rate with k=100 samples. We discuss the potential broader impacts of "
                "deploying powerful code generation technologies, covering safety and security."
            ),
            "copyright_line": "Copyright 2021 OpenAI Technical Report. Submitted: July 2021. arXiv:2107.03374.",
        },
        {
            "filename": "bigbench_srivastava_2022.pdf",
            "title": "Beyond the Imitation Game: Quantifying and Extrapolating the Capabilities of Language Models",
            "authors_line": "Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, Abu Awal Md Shoeb, Abubakar Abid, Adam Fisch, Adam R. Brown, et al.",
            "author_email": "aarohi@google.com",
            "abstract": (
                "Language models demonstrate both quantitative improvement and new qualitative "
                "capabilities with increasing scale. Despite their potentially transformative "
                "impact, these abilities are as yet poorly characterized. In order to inform "
                "future research, prepare for disruptive new model capabilities, and ameliorate "
                "socially harmful effects, we present BIG-bench (Beyond the Imitation Game "
                "Benchmark). BIG-bench currently consists of 204 tasks, contributed by 450 "
                "authors across 132 institutions. Task topics are diverse, drawing problems "
                "from linguistics, childhood development, math, common-sense reasoning, biology, "
                "physics, social bias, software development, and beyond. BIG-bench focuses on "
                "tasks that are believed to be beyond the capabilities of current language models."
            ),
            "copyright_line": "Copyright 2022 Transactions on Machine Learning Research. Submitted: June 2022. Published: 2023.",
        },
    ]

    for paper in papers:
        path = os.path.join(BENCHMARKS_DIR, paper["filename"])
        create_pdf_paper(
            output_path=path,
            title=paper["title"],
            authors_line=paper["authors_line"],
            author_email=paper["author_email"],
            abstract=paper["abstract"],
            copyright_line=paper["copyright_line"],
        )

    print(f"\nBenchmarks directory created with {len(papers)} PDF files: {BENCHMARKS_DIR}")

    # Ensure no pre-existing result file
    result_path = f'{WORKDIR}/benchmark_authors.xlsx'
    if os.path.exists(result_path):
        os.remove(result_path)
        print(f"Removed pre-existing result file: {result_path}")


def setup_gui():
    """Open Nautilus at the Benchmarks directory and LibreOffice Calc."""
    # Open Nautilus file manager at the Benchmarks directory
    launch_gui(f'nautilus "{BENCHMARKS_DIR}"', delay_sec=2.0)

    # Open LibreOffice Calc (blank spreadsheet, ready for data entry)
    launch_gui('libreoffice --calc', delay_sec=2.0)

    print("GUI_READY: Nautilus opened at ~/Documents/Benchmarks, LibreOffice Calc opened")


# Run setup
print("=== Initial Setup: osworld_multi_apps_pdf_author_extract_011 ===")
create_benchmarks()
setup_gui()
print("=== Initial setup complete ===")
