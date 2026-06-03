"""
Initial Setup: Grammar Test Compile - Create exam_repository with 10 test files
Task ID: osworld_multi_apps_grammar_test_compile_012
Domain: libreoffice_writer (multi-app)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'osworld_multi_apps_grammar_test_compile_012'
EXAM_REPO = f'{WORKDIR}/Documents/exam_repository'
OUTPUT_ODT = f'{WORKDIR}/Documents/exam_package_final.odt'


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
    # Create exam_repository directory
    os.makedirs(EXAM_REPO, exist_ok=True)

    # Ensure no compiled document exists
    if os.path.exists(OUTPUT_ODT):
        os.remove(OUTPUT_ODT)

    # Define 10 exam files with topics and difficulties
    exam_files = [
        {
            'filename': 'exam_verbs_easy.txt',
            'topic': 'verbs',
            'difficulty': 'easy',
            'questions': [
                'Q1. Choose the correct form: She _____ (run/runs) every morning.',
                'Q2. Fill in the blank: They _____ (go/goes) to school by bus.',
                'Q3. Which is correct? He _____ (watch/watches) TV after dinner.',
                'Q4. Select the past tense: Yesterday, I _____ (walk/walked) to the park.',
                'Q5. Choose the correct verb: The cat _____ (sit/sits) on the mat.',
                'Q6. Fill in: We _____ (play/plays) football on weekends.',
                'Q7. Which verb form is correct? She _____ (has/have) a new book.',
                'Q8. Select: They _____ (was/were) happy to see us.',
                'Q9. Choose: He _____ (don\'t/doesn\'t) like vegetables.',
                'Q10. Fill in the blank: The birds _____ (fly/flies) south in winter.',
            ],
            'answers': ['A: runs', 'A: go', 'A: watches', 'A: walked', 'A: sits',
                        'A: play', 'A: has', 'A: were', 'A: doesn\'t', 'A: fly'],
        },
        {
            'filename': 'exam_nouns_medium.txt',
            'topic': 'nouns',
            'difficulty': 'medium',
            'questions': [
                'Q1. Identify the noun type: "happiness" is a _____ noun.',
                'Q2. Choose the plural: The _____ (child/children) played in the park.',
                'Q3. Which word is a collective noun? (flock/fly/green/run)',
                'Q4. Select the proper noun: (city/London/happiness/water)',
                'Q5. What is the possessive form of "James"? (James\'/Jamess/James\'s/James)',
                'Q6. Identify: "The _____ of the team was impressive." (moral/morale/moral/morals)',
                'Q7. Choose the abstract noun: (table/joy/mountain/river)',
                'Q8. Fill in: A _____ (pride/pack/flock) of lions roamed the savanna.',
                'Q9. Which is a compound noun? (sunflower/run/blue/fast)',
                'Q10. Select the uncountable noun: (idea/water/book/chair)',
            ],
            'answers': ['A: abstract', 'A: children', 'A: flock', 'A: London', 'A: James\'s',
                        'A: morale', 'A: joy', 'A: pride', 'A: sunflower', 'A: water'],
        },
        {
            'filename': 'exam_adjectives_hard.txt',
            'topic': 'adjectives',
            'difficulty': 'hard',
            'questions': [
                'Q1. Form the superlative: "good" → _____ (most good/better/best/goodest)',
                'Q2. Identify the type: "golden" in "golden opportunity" is a _____ adjective.',
                'Q3. Select the correct order: She wore a _____ dress. (Italian silk blue/blue silk Italian/beautiful blue Italian silk)',
                'Q4. Which adjective is predicative? "The _____ dog barked." (The: old, or "The dog was _____.": loud)',
                'Q5. Comparatives: "This problem is _____ than the last." (more complex/most complex/complexer)',
                'Q6. Choose the participial adjective: (bored/quickly/run/and)',
                'Q7. Identify: "She gave a _____ performance." Which type? (attributive/predicative/substantive)',
                'Q8. Which phrase uses an adjective correctly? (She ran quick./The quick fox jumped./He speaks quick.)',
                'Q9. Form a compound adjective: "a task that lasts three hours" = a _____ task. (three-hour/three hours/3-hours)',
                'Q10. What is the antonym of "benevolent"? (kind/malevolent/generous/charitable)',
            ],
            'answers': ['A: best', 'A: attributive', 'A: beautiful blue Italian silk',
                        'A: predicative (was loud)', 'A: more complex', 'A: bored',
                        'A: attributive', 'A: The quick fox jumped.', 'A: three-hour', 'A: malevolent'],
        },
        {
            'filename': 'exam_adverbs_medium.txt',
            'topic': 'adverbs',
            'difficulty': 'medium',
            'questions': [
                'Q1. Identify the adverb: "She sings _____ (beautiful/beautifully/beauty)."',
                'Q2. What type of adverb is "here"? (manner/place/time/degree)',
                'Q3. Choose the correct form: He speaks _____ (slow/slowly) in class.',
                'Q4. Which adverb modifies the adjective? "The food was _____ hot." (very/much/lot)',
                'Q5. Form the adverb from "happy": _____ (happily/happly/happyly/happily)',
                'Q6. Select the degree adverb: "She is _____ tall." (extremely/here/never)',
                'Q7. Which word is a conjunctive adverb? (however/because/and/or)',
                'Q8. Choose the correct position: "Often he arrives late." — is "often" correctly placed? (yes/no)',
                'Q9. Identify the adverb type: "yesterday" is an adverb of _____ (time/manner/place)',
                'Q10. Which sentence uses "well" correctly? (She sings good./He runs well./They played good.)',
            ],
            'answers': ['A: beautifully', 'A: place', 'A: slowly', 'A: very', 'A: happily',
                        'A: extremely', 'A: however', 'A: yes', 'A: time', 'A: He runs well.'],
        },
        {
            'filename': 'exam_prepositions_easy.txt',
            'topic': 'prepositions',
            'difficulty': 'easy',
            'questions': [
                'Q1. Fill in: The cat is _____ (in/on/under) the table.',
                'Q2. Choose: She arrived _____ (at/on/in) Monday.',
                'Q3. Which preposition fits? "He walked _____ (through/between/across) the tunnel."',
                'Q4. Select: "I have been living here _____ (for/since) three years."',
                'Q5. Fill in: The book is _____ (between/among) the two pens.',
                'Q6. Choose: We talked _____ (about/of/for) the movie.',
                'Q7. Which is correct? "She is good _____ (at/in/on) mathematics."',
                'Q8. Fill in: He ran _____ (away from/toward) the finish line.',
                'Q9. Select: "The letter was written _____ (by/with/from) the teacher."',
                'Q10. Choose: "They met _____ (at/on/in) the corner of the street."',
            ],
            'answers': ['A: on', 'A: on', 'A: through', 'A: for', 'A: between',
                        'A: about', 'A: at', 'A: toward', 'A: by', 'A: at'],
        },
        {
            'filename': 'exam_conjunctions_medium.txt',
            'topic': 'conjunctions',
            'difficulty': 'medium',
            'questions': [
                'Q1. Identify the type: "and" is a _____ conjunction. (coordinating/subordinating/correlative)',
                'Q2. Choose the subordinating conjunction: (but/because/or/nor)',
                'Q3. Fill in: _____ (Although/Because) it was raining, we went outside.',
                'Q4. Which pair is a correlative conjunction? (neither…nor/and…but/since…after)',
                'Q5. Select: "He _____ (neither/either) reads nor writes well."',
                'Q6. Identify: "so that" is a conjunction expressing _____ (purpose/contrast/addition)',
                'Q7. Choose: "I like coffee, _____ (but/and/or) she prefers tea."',
                'Q8. Which sentence uses a conjunction correctly? (She cried because she happy./He left since he was tired.)',
                'Q9. Fill in: We will go _____ (whether/if) or not you agree.',
                'Q10. Identify the conjunction type in: "I will go if you come." (causal/conditional/concessive)',
            ],
            'answers': ['A: coordinating', 'A: because', 'A: Although', 'A: neither...nor', 'A: neither',
                        'A: purpose', 'A: but', 'A: He left since he was tired.', 'A: whether', 'A: conditional'],
        },
        {
            'filename': 'exam_pronouns_hard.txt',
            'topic': 'pronouns',
            'difficulty': 'hard',
            'questions': [
                'Q1. Identify: "who" in "The man who came yesterday" is a _____ pronoun. (relative/interrogative/demonstrative)',
                'Q2. Choose the reflexive pronoun: "She hurt _____ (her/herself/hers) while cooking."',
                'Q3. Which is an indefinite pronoun? (this/those/someone/they)',
                'Q4. Select the correct case: "Between you and _____ (I/me), this is wrong."',
                'Q5. Identify the type of "this" in "This is my book.": (demonstrative/relative/personal)',
                'Q6. Choose: "_____ (Whoever/Whomever) finishes first wins the prize."',
                'Q7. Which sentence has a pronoun error? (He gave it to them./She and me went home./They helped us.)',
                'Q8. Select the correct form: "It was _____ (she/her) who called."',
                'Q9. What type is "each other"? (reciprocal/reflexive/relative pronoun)',
                'Q10. Choose the correct pronoun: "The team won _____ (its/their) first match."',
            ],
            'answers': ['A: relative', 'A: herself', 'A: someone', 'A: me', 'A: demonstrative',
                        'A: Whoever', 'A: She and me went home.', 'A: she', 'A: reciprocal', 'A: its'],
        },
        {
            'filename': 'exam_tenses_hard.txt',
            'topic': 'tenses',
            'difficulty': 'hard',
            'questions': [
                'Q1. Identify: "By next year, I will have graduated." is in _____ tense. (future perfect/future simple/past perfect)',
                'Q2. Choose: "She _____ (has been working/worked) here since 2020." (for ongoing action to present)',
                'Q3. Which tense: "When I arrived, he had already left."? (past perfect/past simple/present perfect)',
                'Q4. Select: "They _____ (are playing/play) football every Saturday." (habitual action)',
                'Q5. Identify the tense: "The earth revolves around the sun." (simple present/present progressive/present perfect)',
                'Q6. Choose: "He _____ (will be working/will work) when you arrive tomorrow." (future progressive)',
                'Q7. Which is correct? "I have seen that film _____ (already/yet/just already)."',
                'Q8. Fill in: "She _____ (had been studying/studied) for six hours before the exam."',
                'Q9. Identify: "No sooner had he left than it started raining." — what structure is used? (inversion/subjunctive/passive)',
                'Q10. Select the correct sequence: "If I _____ (study/studied) harder, I would have passed." (third conditional)',
            ],
            'answers': ['A: future perfect', 'A: has been working', 'A: past perfect', 'A: play',
                        'A: simple present', 'A: will be working', 'A: already', 'A: had been studying',
                        'A: inversion', 'A: had studied'],
        },
        {
            'filename': 'exam_articles_easy.txt',
            'topic': 'articles',
            'difficulty': 'easy',
            'questions': [
                'Q1. Fill in: _____ (A/An) elephant never forgets.',
                'Q2. Choose: She is _____ (a/an/the) honest person.',
                'Q3. Which article is correct? "I saw _____ (a/the) movie you recommended."',
                'Q4. Fill in: He wants to be _____ (a/an/the) doctor.',
                'Q5. Select: "_____ (The/A) sun rises in the east."',
                'Q6. Choose: "They visited _____ (a/the/—) France last summer."',
                'Q7. Which is correct? "She plays _____ (the/a/—) piano beautifully."',
                'Q8. Fill in: "This is _____ (a/an/the) most interesting book I\'ve read."',
                'Q9. Select: "He works as _____ (a/an/the) engineer at a tech company."',
                'Q10. Choose: "We stayed at _____ (a/an/the) hotel near the airport."',
            ],
            'answers': ['A: An', 'A: an', 'A: the', 'A: a', 'A: The',
                        'A: —', 'A: the', 'A: the', 'A: an', 'A: a'],
        },
        {
            'filename': 'exam_punctuation_medium.txt',
            'topic': 'punctuation',
            'difficulty': 'medium',
            'questions': [
                'Q1. Which sentence is correctly punctuated? (Its a lovely day./It\'s a lovely day.)',
                'Q2. Add the missing punctuation: "He said I will be late" → _____ (quoted speech punctuation)',
                'Q3. Choose the correct use of semicolons: "I went to the store; I bought milk." (correct/incorrect)',
                'Q4. When should you use a colon? (Before a list/Instead of a comma/Instead of a period)',
                'Q5. Identify the error: "The dogs bowl was empty." (missing apostrophe/extra comma/no error)',
                'Q6. Which is correct? (She likes reading, writing, and painting./She likes reading writing and painting.)',
                'Q7. Where does the comma go? "After the game we went home." → _____ (after game/no comma/after After)',
                'Q8. Choose the correctly hyphenated form: (well-known author/wellknown author/well known-author)',
                'Q9. Identify: An em dash is used to _____ (introduce a list/add emphasis or interruption/end a sentence)',
                'Q10. Which sentence uses quotation marks correctly? (She said "hello"./She said, "Hello."/She said "Hello")',
            ],
            'answers': ['A: It\'s a lovely day.', 'A: He said, "I will be late."', 'A: correct',
                        'A: Before a list', 'A: missing apostrophe', 'A: She likes reading, writing, and painting.',
                        'A: after game', 'A: well-known author', 'A: add emphasis or interruption',
                        'A: She said, "Hello."'],
        },
    ]

    for ef in exam_files:
        filepath = os.path.join(EXAM_REPO, ef['filename'])
        lines = []
        lines.append(f"METADATA: topic={ef['topic']}, difficulty={ef['difficulty']}, questions=10")
        lines.append('')
        lines.append(f"=== GRAMMAR EXAM: {ef['topic'].upper()} ({ef['difficulty'].upper()}) ===")
        lines.append('')
        for q in ef['questions']:
            lines.append(q)
            lines.append('')
        lines.append('--- ANSWER KEY ---')
        for ans in ef['answers']:
            lines.append(ans)
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))
        print(f'Created: {filepath}')

    print(f'\nexam_repository created at: {EXAM_REPO}')
    print(f'Files created: {len(exam_files)}')
    print(f'No compiled document exists at: {OUTPUT_ODT}')

    # GUI-ready startup: open file manager showing the exam_repository
    launch_gui(f'nautilus "{EXAM_REPO}"', delay_sec=1.5)
    launch_gui('libreoffice --writer', delay_sec=2.0)
    print('GUI_READY: launched Nautilus and LibreOffice Writer with DISPLAY=:0')


create_initial()
