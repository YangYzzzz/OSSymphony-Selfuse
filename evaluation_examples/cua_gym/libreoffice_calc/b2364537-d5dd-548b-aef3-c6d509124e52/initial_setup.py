"""
Initial Setup: Create chapter quiz text files in Documents/chapter_quizzes folder
Task ID: osworld_multi_apps_grammar_test_compile_006
Domain: multi_apps (LibreOffice Writer + OS)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'osworld_multi_apps_grammar_test_compile_006'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
QUIZZES_DIR = f'{DOCUMENTS_DIR}/chapter_quizzes'


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
    # Create Documents directory if not present
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    # Create chapter_quizzes directory
    os.makedirs(QUIZZES_DIR, exist_ok=True)

    # Chapter quiz content — realistic content with meaningful questions
    chapter_quizzes = {
        'ch1_quiz.txt': {
            'title': 'Chapter 1: The Scientific Method',
            'questions': [
                'What is the first step of the scientific method?',
                'Define a hypothesis in your own words.',
                'What is the difference between a dependent and an independent variable?',
                'Why is it important to have a control group in an experiment?',
                'Describe how a scientist would record and analyze experimental data.',
            ]
        },
        'ch2_quiz.txt': {
            'title': 'Chapter 2: Cell Biology',
            'questions': [
                'What is the function of the cell membrane?',
                'Compare and contrast prokaryotic and eukaryotic cells.',
                'Describe the role of mitochondria in cellular respiration.',
                'What process allows materials to cross the cell membrane without energy?',
                'Explain how the endoplasmic reticulum assists in protein synthesis.',
            ]
        },
        'ch3_quiz.txt': {
            'title': 'Chapter 3: Genetics and Heredity',
            'questions': [
                'What is a gene and how does it relate to a chromosome?',
                'Explain the difference between dominant and recessive alleles.',
                'How does a Punnett square help predict genetic outcomes?',
                'Describe what happens during DNA replication.',
                'What is the significance of mutations in an organism\'s genome?',
            ]
        },
        'ch4_quiz.txt': {
            'title': 'Chapter 4: Evolution and Natural Selection',
            'questions': [
                'Who proposed the theory of natural selection and when?',
                'Define "survival of the fittest" in evolutionary terms.',
                'What evidence supports the theory of evolution?',
                'Describe the concept of adaptive radiation with an example.',
                'How does geographic isolation contribute to speciation?',
            ]
        },
        'ch5_quiz.txt': {
            'title': 'Chapter 5: Ecosystems and Ecology',
            'questions': [
                'What is the difference between a food chain and a food web?',
                'Define the concept of a trophic level with an example.',
                'Explain the water cycle and its importance to ecosystems.',
                'What is biodiversity and why is it important for ecosystem stability?',
                'Describe how human activities can disrupt the nitrogen cycle.',
            ]
        },
    }

    for filename, content in chapter_quizzes.items():
        filepath = os.path.join(QUIZZES_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content['title'] + '\n')
            for i, question in enumerate(content['questions'], 1):
                f.write(f'{i}. {question}\n')
        print(f'Created: {filepath}')

    # Ensure chapter_quiz_book.odt does NOT exist in initial state
    book_path = f'{DOCUMENTS_DIR}/chapter_quiz_book.odt'
    if os.path.exists(book_path):
        os.remove(book_path)
        print(f'Removed pre-existing: {book_path}')

    # GUI-ready startup: Open Nautilus file manager showing the chapter_quizzes folder
    launch_gui(f'nautilus "{QUIZZES_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus showing chapter_quizzes folder with DISPLAY=:0')


create_initial()
