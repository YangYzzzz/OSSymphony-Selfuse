"""
Initial Setup: Grammar Quiz Archive for instructor_test_booklet task
Task ID: osworld_multi_apps_grammar_test_compile_011
Domain: libreoffice_writer + os
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_grammar_test_compile_011'
QUIZ_DIR = f'{WORKDIR}/Documents/quiz_archive'


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


QUIZ_DATA = [
    {
        "title": "Parts of Speech",
        "questions": [
            ("Identify the noun in this sentence: 'The curious cat sat on the windowsill.'", "LO-1", "cat", 1),
            ("Which word is an adjective in: 'She wore a beautiful red dress to the ceremony.'", "LO-1", "beautiful", 1),
            ("Select the verb in: 'The students eagerly completed their homework before dinner.'", "LO-1", "completed", 1),
            ("What is the adverb in: 'He quickly ran toward the finish line.'", "LO-1", "quickly", 1),
            ("Identify the pronoun in: 'After Maria finished, she shared her results with the class.'", "LO-2", "she", 1),
            ("Which word is a preposition in: 'The book was placed beneath the heavy oak table.'", "LO-2", "beneath", 1),
            ("Find the conjunction in: 'Tom wanted pizza, but his sister preferred salad.'", "LO-2", "but", 2),
            ("What type of noun is 'flock' in: 'A flock of geese flew over the river'?", "LO-3", "collective noun", 2),
            ("Identify the interjection in: 'Wow, that was an incredible performance by the orchestra!'", "LO-3", "Wow", 1),
            ("Which phrase contains a gerund: A) 'to run fast', B) 'running daily', C) 'ran quickly', D) 'runs often'", "LO-3", "B", 2),
        ]
    },
    {
        "title": "Sentence Structure",
        "questions": [
            ("What type of sentence is: 'Although it was raining, the game continued without delay.'?", "LO-4", "complex sentence", 2),
            ("Identify the subject in: 'Under the bridge, three children played chess.'", "LO-4", "three children", 1),
            ("What is the direct object in: 'The professor assigned a lengthy research paper to the class.'?", "LO-4", "a lengthy research paper", 1),
            ("Which sentence is compound: A) 'I went home.' B) 'I went home and cooked.' C) 'When I arrived, I cooked.' D) 'I cooked, yet ate little.'", "LO-5", "D", 2),
            ("Find the indirect object in: 'She gave her younger brother a birthday present.'", "LO-5", "her younger brother", 1),
            ("What type of clause is 'because he forgot his umbrella' in the sentence 'He got wet because he forgot his umbrella.'?", "LO-5", "subordinate/dependent clause", 2),
            ("Identify the predicate in: 'The tall oak tree swayed gracefully in the autumn wind.'", "LO-6", "swayed gracefully in the autumn wind", 1),
            ("Which sentence contains a compound subject: A) 'James runs.' B) 'James and Laura run.' C) 'He runs fast.' D) 'Running is fun.'", "LO-6", "B", 1),
            ("What is the appositive in: 'My neighbor, an experienced chef, opened a new restaurant.'?", "LO-6", "an experienced chef", 2),
            ("Identify the type of sentence: 'Close the window before the rain comes in!'", "LO-6", "imperative sentence", 1),
        ]
    },
    {
        "title": "Punctuation Rules",
        "questions": [
            ("Which sentence is correctly punctuated: A) 'Its raining today.' B) \"It's raining today.\" C) 'Its' raining today.' D) \"Its' raining today.\"", "LO-7", "B", 1),
            ("Add the missing comma(s): 'After finishing the project Maria submitted it to her supervisor.'", "LO-7", "After finishing the project, Maria submitted it to her supervisor.", 2),
            ("Which sentence uses a semicolon correctly: A) 'I like tea; and coffee.' B) 'She arrived early; he came late.' C) 'Run; fast.' D) 'It was; hot outside.'", "LO-7", "B", 2),
            ("Correct the apostrophe use: 'The student's submitted their essay's on time.'", "LO-8", "The students submitted their essays on time.", 2),
            ("Which sentence needs a colon: A) 'He brought supplies.' B) 'He brought three things, a map, a compass, and rope.' C) 'He brought: supplies.' D) 'He brought the following: a map, a compass, and rope.'", "LO-8", "D", 1),
            ("Fix the hyphen error: 'She is a well known scientist in her field.'", "LO-8", "She is a well-known scientist in her field.", 1),
            ("Where should the comma go: 'Yes I agree with your assessment of the situation.'", "LO-9", "Yes, I agree with your assessment of the situation.", 1),
            ("Which is correct for a series with internal commas: A) commas B) semicolons C) colons D) dashes", "LO-9", "B", 2),
            ("Fix the quotation marks: 'She said, I'll be there soon.'", "LO-9", 'She said, "I\'ll be there soon."', 2),
            ("Where does the period go: A) 'She said \"hello\".' B) 'She said \"hello.\"' C) Either is correct D) Neither is correct", "LO-9", "B", 1),
        ]
    },
    {
        "title": "Verb Tenses",
        "questions": [
            ("Change to past perfect: 'She finishes the report before the deadline.'", "LO-10", "She had finished the report before the deadline.", 2),
            ("What tense is: 'By next Friday, the committee will have reviewed all applications.'?", "LO-10", "future perfect", 2),
            ("Choose the correct form: 'If I _____ (be) you, I would reconsider.' A) was B) were C) am D) had been", "LO-10", "B", 1),
            ("Correct the tense error: 'Yesterday, she walks into the office and announces the results.'", "LO-11", "Yesterday, she walked into the office and announced the results.", 2),
            ("What tense is used: 'The children are playing in the park right now.'?", "LO-11", "present continuous/progressive", 1),
            ("Complete with the correct form: 'He _____ (work) at this company since 2018.' A) works B) worked C) has been working D) had worked", "LO-11", "C", 2),
            ("Identify the error: 'She has went to the store three times this week.'", "LO-12", "has went → has gone", 1),
            ("What tense conveys a repeated past action: A) simple past B) past progressive C) used to + infinitive D) past perfect", "LO-12", "C", 1),
            ("Change to passive voice: 'The team completed the project ahead of schedule.'", "LO-12", "The project was completed ahead of schedule by the team.", 2),
            ("Correct: 'I am knowing the answer to your question.' A) I know B) I am known C) I had known D) I knew", "LO-12", "A", 1),
        ]
    },
    {
        "title": "Subject-Verb Agreement",
        "questions": [
            ("Choose the correct verb: 'Neither the students nor the teacher _____ (was/were) informed.'", "LO-13", "was", 2),
            ("Select the correct form: 'The news _____ (is/are) very concerning today.'", "LO-13", "is", 1),
            ("Which is correct: A) 'Each of the boys have' B) 'Each of the boys has' C) 'Each of the boys are' D) 'Each of the boys were'", "LO-13", "B", 1),
            ("Correct the error: 'The committee are divided on the issue of budget allocations.'", "LO-14", "The committee is divided on the issue of budget allocations.", 2),
            ("Choose: 'Mathematics _____ (is/are) my favorite subject.'", "LO-14", "is", 1),
            ("Which is correct: A) 'Five miles are a long walk.' B) 'Five miles is a long walk.' C) Both are correct D) Neither is correct", "LO-14", "B", 1),
            ("Correct: 'The data clearly shows that our hypothesis were correct.'", "LO-15", "The data clearly show that our hypothesis was correct.", 2),
            ("Select correct verb: 'Everyone in the three departments _____ (has/have) been notified.'", "LO-15", "has", 1),
            ("Which sentence has correct agreement: A) 'The jury have reached a verdict.' B) 'The jury has reached a verdict.' C) Both D) Neither", "LO-15", "B", 2),
            ("Correct: 'There is many reasons why this project will succeed.'", "LO-15", "There are many reasons why this project will succeed.", 1),
        ]
    },
    {
        "title": "Pronoun Usage",
        "questions": [
            ("Choose correctly: 'Between you and _____ (I/me), this plan needs revision.'", "LO-16", "me", 1),
            ("Select the correct pronoun: 'The award was given to Sarah and _____ (I/me/myself).'", "LO-16", "me", 1),
            ("What is the antecedent of 'it' in: 'When the engine overheated, it caused significant delays.'?", "LO-16", "the engine", 1),
            ("Correct the pronoun error: 'Everyone must submit their essay by Friday.'  Is this correct?", "LO-17", "Yes, this is now accepted as correct gender-neutral usage.", 2),
            ("Choose: 'The company revised _____ (its/their/it's) policy on remote work.'", "LO-17", "its", 1),
            ("Identify the reflexive pronoun in: 'The director personally reviewed each application himself.'", "LO-17", "himself", 1),
            ("Which is correct: A) 'Who did you speak with?' B) 'Whom did you speak with?' C) Both are acceptable D) Neither is correct", "LO-18", "C", 2),
            ("Correct the error: 'Her and I went to the conference together last month.'", "LO-18", "She and I went to the conference together last month.", 2),
            ("Choose the correct relative pronoun: 'The scientist _____ (who/whom/that/which) won the award retired last year.'", "LO-18", "who", 1),
            ("Identify the intensive pronoun in: 'The CEO herself attended the product launch event.'", "LO-18", "herself", 1),
        ]
    },
    {
        "title": "Word Choice and Vocabulary",
        "questions": [
            ("Choose the correct word: 'The new policy will _____ (affect/effect) all employees starting Monday.'", "LO-19", "affect", 1),
            ("Select correctly: 'Please _____ (lay/lie) the documents on the conference table.'", "LO-19", "lay", 2),
            ("Which is correct: A) 'He inferred that she was unhappy.' B) 'He implied that she was unhappy.' C) Both mean the same D) Neither is correct", "LO-19", "A", 2),
            ("Choose: 'The company will _____ (assure/ensure/insure) that all safety standards are met.'", "LO-20", "ensure", 1),
            ("Correct the word choice: 'The principal reason for the delay was due to supply chain issues.'", "LO-20", "The principal reason for the delay was supply chain issues. ('due to' is redundant with 'reason')", 2),
            ("Select correctly: 'After the accident, the driver was _____ (cite/sight/site/sited) for reckless driving.' A) cited B) sighted C) sited D) cited", "LO-20", "A", 1),
            ("Which is the correct use of 'comprise': A) 'The team comprises five members.' B) 'The team is comprised of five members.' C) Both are correct D) Neither is correct", "LO-21", "A", 2),
            ("Choose: 'The research _____ (corroborates/collaborates) our initial findings.'", "LO-21", "corroborates", 1),
            ("Select: 'The speaker _____ (alluded/eluded/deluded) to budget cuts without mentioning specific figures.'", "LO-21", "alluded", 1),
            ("Correct the malapropism: 'The lawyer's summation was very illusive and hard to follow.'", "LO-21", "elusive", 2),
        ]
    },
    {
        "title": "Modifiers and Parallel Structure",
        "questions": [
            ("Fix the dangling modifier: 'Walking down the street, the trees looked beautiful in autumn.'", "LO-22", "Walking down the street, she noticed the trees looked beautiful in autumn.", 2),
            ("Correct the misplaced modifier: 'She nearly drove the car for six hours without stopping.'", "LO-22", "She drove the car for nearly six hours without stopping.", 2),
            ("Which sentence has parallel structure: A) 'He likes swimming, to jog, and cycling.' B) 'He likes swimming, jogging, and cycling.' C) 'He likes to swim, jogging, and cycle.' D) 'He swims, jogged, and cycles.'", "LO-22", "B", 1),
            ("Fix parallel structure: 'The report was thorough, accurate, and had been written well.'", "LO-23", "The report was thorough, accurate, and well-written.", 2),
            ("Identify the squinting modifier in: 'Students who practice writing frequently improve their skills.'", "LO-23", "'frequently' — it could modify 'practice' or 'improve'", 2),
            ("Correct: 'Only the manager approved the budget for the new project.'  vs 'The manager approved only the budget for the new project.' — How do they differ?", "LO-23", "First: only the manager approved it (not others). Second: only the budget was approved (not other things).", 2),
            ("Fix the faulty parallelism: 'She was told to arrive early, completing the paperwork, and that she should dress professionally.'", "LO-24", "She was told to arrive early, to complete the paperwork, and to dress professionally.", 2),
            ("Which sentence avoids a dangling modifier: A) 'After finishing the test, the results were analyzed.' B) 'After finishing the test, the teacher analyzed the results.' C) Both are correct D) Neither is correct", "LO-24", "B", 1),
            ("Correct the double negative: 'The witness didn't see nothing unusual at the time of the incident.'", "LO-24", "The witness didn't see anything unusual at the time of the incident.", 1),
            ("Fix: 'To be a good writer, practice must be done daily.'", "LO-24", "To be a good writer, you must practice daily.", 1),
        ]
    },
    {
        "title": "Sentence Clarity and Style",
        "questions": [
            ("Rewrite to eliminate wordiness: 'At this point in time, the committee is in the process of reviewing the applications that were submitted.'", "LO-25", "The committee is currently reviewing the submitted applications.", 2),
            ("Identify the passive construction and suggest active alternative: 'Mistakes were made by the project team during the initial phase.'", "LO-25", "The project team made mistakes during the initial phase.", 2),
            ("Fix the ambiguous pronoun reference: 'When Anna met Clara, she seemed nervous about the presentation.'", "LO-25", "When Anna met Clara, Clara seemed nervous about the presentation. (or 'Anna seemed nervous')", 2),
            ("Choose the more concise version: A) 'Due to the fact that' B) 'Because' C) Both are acceptable D) Neither is correct", "LO-26", "B", 1),
            ("Improve coherence by choosing the correct transition: 'The experiment failed. _____, the team documented all findings carefully.' A) However B) Therefore C) Furthermore D) Nevertheless", "LO-26", "D", 2),
            ("Identify the cliche and suggest a replacement: 'At the end of the day, the quality of our work speaks for itself.'", "LO-26", "'At the end of the day' is a cliche; replace with 'Ultimately' or 'In the final analysis'", 1),
            ("Fix the sentence fragment: 'Running through the park early in the morning. A great way to start the day.'", "LO-27", "Running through the park early in the morning is a great way to start the day.", 2),
            ("Correct the comma splice: 'The presentation was too long, the audience lost interest halfway through.'", "LO-27", "The presentation was too long; the audience lost interest halfway through. (or use 'so' or a period)", 2),
            ("Combine for better flow: 'She studied diligently. She passed the exam. She received a scholarship.'", "LO-27", "Having studied diligently, she passed the exam and received a scholarship.", 1),
            ("What is the purpose of a topic sentence in a paragraph?", "LO-27", "A topic sentence introduces the main idea of the paragraph and controls the direction of the supporting details.", 1),
        ]
    },
    {
        "title": "Reading Comprehension and Analysis",
        "questions": [
            ("What is the difference between the main idea and the theme of a text?", "LO-28", "The main idea is the specific central point of the text; the theme is the broader, universal concept underlying the text.", 2),
            ("Define 'inference' in reading comprehension.", "LO-28", "An inference is a conclusion drawn from evidence and reasoning rather than from explicit statements in the text.", 1),
            ("What does 'connotation' mean in the context of word choice?", "LO-28", "Connotation refers to the emotional or cultural associations of a word beyond its literal (denotative) meaning.", 1),
            ("Explain the difference between 'tone' and 'mood' in a text.", "LO-29", "Tone is the author's attitude toward the subject; mood is the emotional atmosphere created for the reader.", 2),
            ("What is an 'unreliable narrator'?", "LO-29", "An unreliable narrator is one whose account of events cannot be fully trusted due to personal bias, limited knowledge, or deliberate deception.", 2),
            ("Distinguish between 'simile' and 'metaphor'.", "LO-29", "A simile compares two things using 'like' or 'as'; a metaphor directly states that one thing is another without using comparison words.", 1),
            ("What is the purpose of a 'counterargument' in persuasive writing?", "LO-30", "A counterargument acknowledges opposing viewpoints, which strengthens credibility and allows the writer to rebut them effectively.", 2),
            ("Define 'rhetorical question' and give an example.", "LO-30", "A rhetorical question is asked for effect without expecting an answer. Example: 'Is this the kind of society we want to live in?'", 1),
            ("What does 'synthesizing information' mean when reading multiple sources?", "LO-30", "Synthesizing means combining ideas from multiple sources to form a new, integrated understanding rather than simply summarizing each source.", 2),
            ("Explain how 'context clues' help readers understand unfamiliar words.", "LO-30", "Context clues are words or phrases surrounding an unfamiliar word that provide hints about its meaning, allowing readers to make informed guesses.", 1),
        ]
    },
]


def create_quiz_file(filepath, topic_data, topic_num):
    """Create a single quiz text file with questions and answer key."""
    lines = []
    topic_title = topic_data["title"]
    lines.append(f"Topic {topic_num:02d}: {topic_title}")
    lines.append("=" * 60)
    lines.append("")
    lines.append("Instructions: Answer all questions in this section.")
    lines.append("")

    for q_num, (question, lo_tag, answer, points) in enumerate(topic_data["questions"], 1):
        lines.append(f"Question {q_num}. {question} [{lo_tag}]")
        lines.append("")

    lines.append("")
    lines.append("### Answer Key ###")
    lines.append("")
    lines.append(f"Topic: {topic_title}")
    lines.append("")

    for q_num, (question, lo_tag, answer, points) in enumerate(topic_data["questions"], 1):
        lines.append(f"Q{q_num}: {answer} | Points: {points} | {lo_tag}")

    content = "\n".join(lines) + "\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def create_initial():
    # Ensure Documents directory exists
    docs_dir = f'{WORKDIR}/Documents'
    os.makedirs(docs_dir, exist_ok=True)

    # Create quiz_archive directory
    os.makedirs(QUIZ_DIR, exist_ok=True)

    # Create 10 quiz files
    for i, topic_data in enumerate(QUIZ_DATA, 1):
        filename = f"quiz_topic_{i:02d}.txt"
        filepath = os.path.join(QUIZ_DIR, filename)
        create_quiz_file(filepath, topic_data, i)
        print(f"Created: {filepath}")

    print(f"\nAll 10 quiz files created in: {QUIZ_DIR}")

    # Verify files exist
    for i in range(1, 11):
        fpath = os.path.join(QUIZ_DIR, f"quiz_topic_{i:02d}.txt")
        if os.path.exists(fpath):
            size = os.path.getsize(fpath)
            print(f"  quiz_topic_{i:02d}.txt: {size} bytes")
        else:
            print(f"  ERROR: quiz_topic_{i:02d}.txt not found!")

    # GUI-ready startup: open file manager showing the quiz_archive folder
    launch_gui(f'nautilus "{QUIZ_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
