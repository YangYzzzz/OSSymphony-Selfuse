"""
Initial Setup: Create assessment_bank folder with grammar quiz files
Task ID: osworld_multi_apps_grammar_test_compile_009
Domain: multi_apps (LibreOffice Writer + text files)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_grammar_test_compile_009'
DOCS_DIR = f'{WORKDIR}/Documents'
BANK_DIR = f'{DOCS_DIR}/assessment_bank'


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


EASY_QUESTIONS = {
    'easy_01': {
        'questions': [
            "1. Choose the correct verb: She _____ (go/goes) to school every day.",
            "2. Fill in the blank: They _____ (is/are) my best friends.",
            "3. Select the right article: I saw _____ (a/an) elephant at the zoo.",
            "4. Choose the correct pronoun: _____ (Him/He) and I went to the market.",
            "5. Fill in the blank: The cat _____ (sit/sits) on the mat.",
            "6. Choose the correct form: She _____ (don't/doesn't) like spinach.",
            "7. Select the correct tense: Yesterday, I _____ (walk/walked) to school.",
            "8. Fill in the blank: There _____ (is/are) many books on the shelf.",
            "9. Choose the correct word: The weather is _____ (good/well) today.",
            "10. Fill in the blank: He _____ (has/have) two brothers.",
        ],
        'answers': ["goes", "are", "an", "He", "sits", "doesn't", "walked", "are", "good", "has"]
    },
    'easy_02': {
        'questions': [
            "1. Choose the correct possessive: This is _____ (my/mine) book.",
            "2. Fill in the blank: We _____ (was/were) at home last night.",
            "3. Select the correct preposition: She is good _____ (in/at) mathematics.",
            "4. Choose the correct form: He _____ (plays/play) tennis on weekends.",
            "5. Fill in the blank: The children _____ (is/are) playing in the park.",
            "6. Choose the correct conjunction: I like apples _____ (but/and) oranges.",
            "7. Select the correct adjective form: This is the _____ (more/most) beautiful flower.",
            "8. Fill in the blank: She _____ (don't/doesn't) know the answer.",
            "9. Choose the correct article: _____ (The/A) sun rises in the east.",
            "10. Fill in the blank: My mother _____ (cook/cooks) dinner every evening.",
        ],
        'answers': ["my", "were", "at", "plays", "are", "and", "most", "doesn't", "The", "cooks"]
    },
    'easy_03': {
        'questions': [
            "1. Choose the correct word: He runs _____ (fast/fastly) on the track.",
            "2. Fill in the blank: She _____ (has/have) finished her homework.",
            "3. Select the correct plural: There are three _____ (child/children) in the room.",
            "4. Choose the correct tense: They _____ (will go/went) to the park tomorrow.",
            "5. Fill in the blank: The dog _____ (bark/barks) loudly at night.",
            "6. Choose the correct word: It is _____ (hotter/more hot) today than yesterday.",
            "7. Select the correct pronoun: _____ (Her/She) is a talented singer.",
            "8. Fill in the blank: We _____ (have/has) a test next Monday.",
            "9. Choose the correct form: He _____ (didn't/doesn't) come to school yesterday.",
            "10. Fill in the blank: The books _____ (is/are) on the table.",
        ],
        'answers': ["fast", "has", "children", "will go", "barks", "hotter", "She", "have", "didn't", "are"]
    },
    'easy_04': {
        'questions': [
            "1. Choose the correct verb: The team _____ (play/plays) well together.",
            "2. Fill in the blank: I _____ (am/is) very happy today.",
            "3. Select the correct preposition: He walked _____ (in/into) the room.",
            "4. Choose the correct word: She sings _____ (beautiful/beautifully) in the choir.",
            "5. Fill in the blank: They _____ (haven't/hasn't) seen the movie yet.",
            "6. Choose the correct tense: She _____ (study/studied) for three hours last night.",
            "7. Select the correct article: He is _____ (a/an) honest man.",
            "8. Fill in the blank: The students _____ (was/were) excited about the trip.",
            "9. Choose the correct form: We _____ (don't/doesn't) need more supplies.",
            "10. Fill in the blank: My parents _____ (was/were) born in 1965.",
        ],
        'answers': ["plays", "am", "into", "beautifully", "haven't", "studied", "an", "were", "don't", "were"]
    },
    'easy_05': {
        'questions': [
            "1. Choose the correct word: The soup smells _____ (good/well).",
            "2. Fill in the blank: She _____ (bring/brought) a cake to the party.",
            "3. Select the correct form: He is taller _____ (than/then) his brother.",
            "4. Choose the correct possessive: The decision was _____ (their/theirs) to make.",
            "5. Fill in the blank: Nobody _____ (know/knows) the answer.",
            "6. Choose the correct word: This is _____ (fewer/less) expensive than that one.",
            "7. Select the correct tense: By next year, she _____ (will have/would have) graduated.",
            "8. Fill in the blank: Either John or Mary _____ (have/has) the key.",
            "9. Choose the correct form: He _____ (lays/lies) down when he is tired.",
            "10. Fill in the blank: The news _____ (is/are) very shocking today.",
        ],
        'answers': ["good", "brought", "than", "theirs", "knows", "less", "will have", "has", "lies", "is"]
    },
}

HARD_QUESTIONS = {
    'hard_01': {
        'questions': [
            "1. Identify the error: 'Each of the students have submitted their assignment.' Correct it.",
            "2. Choose the correct form: If I _____ (was/were) you, I would apologize immediately.",
            "3. Rewrite using the correct word: The data _____ (show/shows) a significant increase.",
            "4. Identify the dangling modifier: 'Walking down the street, the trees looked beautiful.' Correct it.",
            "5. Choose the correct form: She _____ (should have went/should have gone) earlier.",
            "6. Fill in the blank: The committee _____ (have/has) reached a unanimous decision.",
            "7. Correct the sentence: 'Between you and I, the project needs more work.'",
            "8. Choose the correct word: His performance was _____ (different from/different than) expected.",
            "9. Identify the error: 'Whoever finishes first will receive the prize.' Is this correct?",
            "10. Choose the correct form: The phenomenon _____ (occur/occurs) rarely in nature.",
        ],
        'answers': [
            "has submitted",
            "were",
            "shows",
            "Walking down the street, I saw beautiful trees.",
            "should have gone",
            "has",
            "Between you and me",
            "different from",
            "Correct",
            "occurs"
        ]
    },
    'hard_02': {
        'questions': [
            "1. Correct the faulty parallelism: 'She likes reading, to swim, and dancing.'",
            "2. Choose the correct form: The number of students _____ (has/have) increased this year.",
            "3. Identify the error in: 'Everyone brought their own lunch to the meeting.'",
            "4. Choose the correct word: He is _____ (adverse/averse) to taking risks.",
            "5. Correct the error: 'The report was wrote by the research team.'",
            "6. Fill in the blank: Neither the manager nor the employees _____ (was/were) informed.",
            "7. Choose the correct usage: She _____ (lay/laid) the books on the table yesterday.",
            "8. Identify and correct: 'The criteria for selection is unclear.'",
            "9. Choose the correct form: _____ (Who/Whom) did you speak with at the conference?",
            "10. Correct the error: 'The data is being analyzed as we speak.'",
        ],
        'answers': [
            "She likes reading, swimming, and dancing.",
            "has",
            "Correct (acceptable singular they usage)",
            "averse",
            "The report was written by the research team.",
            "were",
            "laid",
            "The criteria for selection are unclear.",
            "Whom",
            "Correct"
        ]
    },
    'hard_03': {
        'questions': [
            "1. Correct the error: 'The team of researchers have published their findings.'",
            "2. Choose the correct form: She acted _____ (as if/like) she knew the answer.",
            "3. Identify the ambiguous pronoun: 'When Jane met Susan, she was very nervous.'",
            "4. Choose the correct word: The treaty will _____ (effect/affect) trade relations.",
            "5. Correct the sentence: 'Having eaten dinner, the movie was started.'",
            "6. Choose the correct form: It is I _____ (who/whom) should apologize.",
            "7. Identify the error: 'Less than ten people attended the seminar.'",
            "8. Fill in the blank: The jury _____ (has/have) reached a verdict.",
            "9. Choose the correct usage: He could _____ (of/have) warned us earlier.",
            "10. Correct if needed: 'Hopefully, the weather will improve by tomorrow.'",
        ],
        'answers': [
            "The team of researchers has published its findings.",
            "as if",
            "Ambiguous - unclear if 'she' refers to Jane or Susan",
            "affect",
            "Having eaten dinner, we started the movie.",
            "who",
            "Fewer than ten people attended the seminar.",
            "has",
            "have",
            "Correct (acceptable in modern usage)"
        ]
    },
    'hard_04': {
        'questions': [
            "1. Correct the misplaced modifier: 'He almost drove his children to school every day.'",
            "2. Choose the correct form: The statistics _____ (was/were) compiled by researchers.",
            "3. Identify the error: 'The reason is because she forgot to set her alarm.'",
            "4. Choose the correct word: This approach is _____ (preferable to/preferable than) the other.",
            "5. Correct the error: 'Between the three candidates, she was most qualified.'",
            "6. Fill in the blank: A number of issues _____ (has/have) been raised in the meeting.",
            "7. Choose the correct form: I wish I _____ (was/were) more patient.",
            "8. Identify and correct: 'He is one of those managers who demands perfection.'",
            "9. Choose the correct word: She was _____ (disinterested/uninterested) in the outcome.",
            "10. Correct the sentence: 'The professor, along with her students, have published the paper.'",
        ],
        'answers': [
            "He drove his children to school almost every day.",
            "were",
            "The reason is that she forgot to set her alarm.",
            "preferable to",
            "Among the three candidates, she was most qualified.",
            "have",
            "were",
            "He is one of those managers who demand perfection.",
            "uninterested",
            "The professor, along with her students, has published the paper."
        ]
    },
    'hard_05': {
        'questions': [
            "1. Identify the error: 'My friend and me went to the concert last night.'",
            "2. Choose the correct form: Scarcely had she arrived _____ (when/than) the phone rang.",
            "3. Correct the error: 'The media has been biased in its reporting.'",
            "4. Choose the correct word: The lawyer's argument was _____ (comprised of/composed of) logical fallacies.",
            "5. Identify the error: 'He is the most unique candidate for the position.'",
            "6. Fill in the blank: The scissors _____ (need/needs) to be sharpened.",
            "7. Choose the correct form: She denied _____ (to take/taking) the documents.",
            "8. Correct the faulty comparison: 'His salary is higher than his colleague.'",
            "9. Choose the correct word: The report was _____ (comprised/composed) of three sections.",
            "10. Identify and correct: 'Neither of the answers are correct.'",
        ],
        'answers': [
            "My friend and I went to the concert last night.",
            "when",
            "Correct (media can be treated as singular)",
            "composed of",
            "He is a unique candidate (unique cannot be modified by 'most')",
            "need",
            "taking",
            "His salary is higher than his colleague's.",
            "composed",
            "Neither of the answers is correct."
        ]
    },
}


def create_quiz_file(filepath, questions, answers):
    """Write a quiz file with questions and embedded answer key."""
    lines = []
    for q in questions:
        lines.append(q)
        lines.append("")  # blank line between questions
    lines.append("Answers: " + ", ".join(answers))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Created: {filepath}")


def create_initial():
    # Create directories
    os.makedirs(BANK_DIR, exist_ok=True)
    print(f"Created directory: {BANK_DIR}")

    # Create easy files
    for i, (key, data) in enumerate(EASY_QUESTIONS.items(), 1):
        filename = f'easy_{i:02d}.txt'
        filepath = os.path.join(BANK_DIR, filename)
        create_quiz_file(filepath, data['questions'], data['answers'])

    # Create hard files
    for i, (key, data) in enumerate(HARD_QUESTIONS.items(), 1):
        filename = f'hard_{i:02d}.txt'
        filepath = os.path.join(BANK_DIR, filename)
        create_quiz_file(filepath, data['questions'], data['answers'])

    print(f"\nAll quiz files created in: {BANK_DIR}")
    print("Files:")
    for f in sorted(os.listdir(BANK_DIR)):
        print(f"  {f}")

    # GUI-ready startup: open file manager to show the assessment_bank folder
    launch_gui(f'nautilus "{BANK_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with assessment_bank folder')


create_initial()
