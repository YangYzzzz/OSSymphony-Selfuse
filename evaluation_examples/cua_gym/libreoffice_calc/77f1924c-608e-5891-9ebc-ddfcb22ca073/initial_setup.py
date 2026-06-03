"""
Initial Setup: Grammar Test Compilation - Unit Tests Folder
Task ID: osworld_multi_apps_grammar_test_compile_007
Domain: multi_apps (OS file creation + LibreOffice Writer)

Creates ~/Documents/unit_tests/ with 5 .txt question files.
Each file has an instruction line followed by 5 questions.
Opens Nautilus to the Documents folder for GUI-ready state.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
UNIT_TESTS_DIR = f'{WORKDIR}/Documents/unit_tests'


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
    # Ensure Documents directory exists
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    # Create unit_tests folder (remove existing to ensure clean state)
    if os.path.exists(UNIT_TESTS_DIR):
        import shutil
        shutil.rmtree(UNIT_TESTS_DIR)
    os.makedirs(UNIT_TESTS_DIR, exist_ok=True)

    # --- multiple_choice.txt ---
    multiple_choice_content = """Instructions: Choose the best answer from the options provided for each question.
1. Which of the following best describes a subject in a sentence?
   A) The action performed in the sentence
   B) The person or thing the sentence is about
   C) A word that modifies a noun
   D) A connecting word between clauses

2. In the sentence "The quick brown fox jumps over the lazy dog," what is the verb?
   A) fox
   B) quick
   C) jumps
   D) lazy

3. Which sentence uses the correct form of "its" or "it's"?
   A) The cat licked it's paw.
   B) Its raining outside today.
   C) The school painted its gymnasium walls green.
   D) Its' the best option available.

4. What is the correct plural form of "criterion"?
   A) criterions
   B) criterias
   C) criteria
   D) criterium

5. Which sentence demonstrates correct subject-verb agreement?
   A) The team are playing well this season.
   B) Neither the students nor the teacher were present.
   C) Each of the delegates have submitted their reports.
   D) The committee is meeting tomorrow at noon.
"""

    # --- fill_blank.txt ---
    fill_blank_content = """Instructions: Fill in each blank with the most appropriate word or phrase to complete the sentence correctly.
6. The scientist ________ her research paper three times before submitting it to the journal.
7. Neither the manager nor the employees ________ aware of the new company policy.
8. If I ________ known about the traffic, I would have left earlier this morning.
9. The ancient ruins, which ________ discovered in 1987, attracted thousands of tourists each year.
10. By the time she graduates, she ________ studied at this university for four years.
"""

    # --- short_answer.txt ---
    short_answer_content = """Instructions: Answer each question in one to three complete sentences using correct grammar and punctuation.
11. Explain the difference between a dependent clause and an independent clause, and provide one example of each.
12. What is the purpose of a semicolon, and when should it be used instead of a comma?
13. Describe the difference between active voice and passive voice in writing, and explain when passive voice is appropriate.
14. What is an Oxford comma, and what role does it play in eliminating ambiguity in a list?
15. Explain the grammatical rule governing the use of "who" versus "whom" in a sentence.
"""

    # --- true_false.txt ---
    true_false_content = """Instructions: Write "True" if the statement is grammatically correct or "False" if it contains an error.
16. "Me and my colleague attended the conference last week."
17. "The data suggest that consumer spending is increasing this quarter."
18. "Between you and I, the project deadline seems unrealistic."
19. "Whomever submitted the report first will receive credit for the assignment."
20. "The reason for the delay is that the shipment was lost in transit."
"""

    # --- essay.txt ---
    essay_content = """Instructions: Write a well-organized response of at least three paragraphs, demonstrating proper grammar, punctuation, and sentence structure.
21. Discuss how social media has changed the way people communicate, focusing on both the benefits and drawbacks of digital communication.
22. Analyze the importance of reading in developing strong writing skills, drawing on examples from your own academic experience.
23. Compare and contrast formal and informal writing styles, explaining when each is appropriate and providing specific examples.
24. Argue for or against the statement: "Grammar rules are less important in the age of autocorrect and digital communication tools."
25. Reflect on a time when clear written communication was essential to resolving a misunderstanding, and describe what you learned from the experience.
"""

    files = {
        'multiple_choice.txt': multiple_choice_content,
        'fill_blank.txt': fill_blank_content,
        'short_answer.txt': short_answer_content,
        'true_false.txt': true_false_content,
        'essay.txt': essay_content,
    }

    for filename, content in files.items():
        filepath = os.path.join(UNIT_TESTS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Created: {filepath}')

    # Make sure unit_exam.odt does NOT pre-exist
    odt_path = f'{WORKDIR}/Documents/unit_exam.odt'
    if os.path.exists(odt_path):
        os.remove(odt_path)
        print(f'Removed pre-existing: {odt_path}')

    print(f'Initial unit_tests folder created at: {UNIT_TESTS_DIR}')

    # GUI-ready startup: open Nautilus to unit_tests folder and LibreOffice Writer
    launch_gui(f'nautilus "{UNIT_TESTS_DIR}"', delay_sec=1.5)
    launch_gui('libreoffice --writer', delay_sec=2.0)
    print('GUI_READY: launched Nautilus and LibreOffice Writer with DISPLAY=:0')


create_initial()
