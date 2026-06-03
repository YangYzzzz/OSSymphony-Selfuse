"""
Initial Setup: Create semester_tests folder with 10 test files for compilation task.
Task ID: osworld_multi_apps_grammar_test_compile_008
Domain: multi_apps (LibreOffice Writer + OS)

Creates:
  /home/user/Documents/semester_tests/test_01.txt through test_10.txt
  Each file has a title line + 10 questions with correct answers in brackets.
  NO final_exam_complete.odt exists initially.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DOCUMENTS = '/home/user/Documents'
SEMESTER_TESTS_DIR = '/home/user/Documents/semester_tests'


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


# Test data: 10 subjects, each with 10 questions and labeled correct answers
TEST_DATA = [
    {
        "title": "Biology 101 - Chapter 5: Cell Biology",
        "questions": [
            ("What is the powerhouse of the cell?", ["a) Nucleus", "b) Mitochondria", "c) Ribosome", "d) Golgi apparatus"], "b"),
            ("Which organelle is responsible for protein synthesis?", ["a) Lysosome", "b) Vacuole", "c) Ribosome", "d) Centrosome"], "c"),
            ("What is the primary component of the cell membrane?", ["a) Proteins", "b) Carbohydrates", "c) Phospholipid bilayer", "d) Cholesterol"], "c"),
            ("Which process allows water to move across a semipermeable membrane?", ["a) Active transport", "b) Endocytosis", "c) Osmosis", "d) Diffusion"], "c"),
            ("What is the function of the Golgi apparatus?", ["a) Energy production", "b) Protein modification and packaging", "c) DNA replication", "d) Lipid synthesis"], "b"),
            ("The process by which cells engulf large particles is called:", ["a) Pinocytosis", "b) Exocytosis", "c) Phagocytosis", "d) Diffusion"], "c"),
            ("Which type of cell division produces gametes?", ["a) Mitosis", "b) Binary fission", "c) Meiosis", "d) Budding"], "c"),
            ("The fluid inside the nucleus is called:", ["a) Cytoplasm", "b) Nucleoplasm", "c) Cytosol", "d) Karyoplasm"], "b"),
            ("Which structure controls what enters and leaves the nucleus?", ["a) Cell wall", "b) Nuclear pore", "c) Plasma membrane", "d) Endoplasmic reticulum"], "b"),
            ("What is the term for programmed cell death?", ["a) Necrosis", "b) Apoptosis", "c) Lysis", "d) Autophagy"], "b"),
        ]
    },
    {
        "title": "Chemistry 202 - Chapter 3: Chemical Bonding",
        "questions": [
            ("What type of bond is formed by sharing electrons?", ["a) Ionic bond", "b) Hydrogen bond", "c) Covalent bond", "d) Van der Waals force"], "c"),
            ("The electronegativity difference for an ionic bond is generally greater than:", ["a) 0.5", "b) 1.0", "c) 1.7", "d) 2.5"], "c"),
            ("Which molecule has a trigonal planar geometry?", ["a) CH4", "b) NH3", "c) BF3", "d) H2O"], "c"),
            ("A coordinate covalent bond is also known as:", ["a) Polar bond", "b) Dative bond", "c) Double bond", "d) Sigma bond"], "b"),
            ("What is the bond angle in a tetrahedral molecule?", ["a) 90 degrees", "b) 109.5 degrees", "c) 120 degrees", "d) 180 degrees"], "b"),
            ("Which of the following is a nonpolar covalent molecule?", ["a) HCl", "b) H2O", "c) N2", "d) CO"], "c"),
            ("The octet rule applies to elements that seek how many electrons in their outer shell?", ["a) 2", "b) 4", "c) 6", "d) 8"], "d"),
            ("Which theory predicts molecular shape based on electron pairs?", ["a) MO theory", "b) VSEPR theory", "c) Crystal field theory", "d) Hybridization theory"], "b"),
            ("What type of hybridization is present in ethene (C2H4)?", ["a) sp3", "b) sp2", "c) sp", "d) dsp2"], "b"),
            ("Resonance structures differ only in:", ["a) Number of atoms", "b) Molecular formula", "c) Position of electrons", "d) Atomic masses"], "c"),
        ]
    },
    {
        "title": "Physics 301 - Chapter 7: Electromagnetism",
        "questions": [
            ("What is the SI unit of electric charge?", ["a) Ampere", "b) Volt", "c) Coulomb", "d) Farad"], "c"),
            ("Ohm's law states that V equals:", ["a) I/R", "b) I*R", "c) R/I", "d) P*I"], "b"),
            ("Which law relates the magnetic field around a current-carrying conductor?", ["a) Faraday's law", "b) Gauss's law", "c) Ampere's law", "d) Lenz's law"], "c"),
            ("The unit of magnetic flux density is:", ["a) Weber", "b) Tesla", "c) Henry", "d) Gauss"], "b"),
            ("In a series circuit, current is:", ["a) Different at each point", "b) The same throughout", "c) Zero at the resistor", "d) Maximum at the source"], "b"),
            ("Capacitance is the ability of a component to:", ["a) Resist current flow", "b) Store electrical charge", "c) Convert AC to DC", "d) Generate magnetic fields"], "b"),
            ("What is the frequency of AC power in the United States?", ["a) 50 Hz", "b) 60 Hz", "c) 100 Hz", "d) 120 Hz"], "b"),
            ("Electromagnetic induction occurs when:", ["a) Two charges attract", "b) A conductor moves through a magnetic field", "c) Current flows through a resistor", "d) A capacitor charges"], "b"),
            ("The transformer is based on the principle of:", ["a) Conduction", "b) Convection", "c) Mutual inductance", "d) Capacitance"], "c"),
            ("In a parallel circuit, voltage is:", ["a) Different across each branch", "b) The same across all branches", "c) Zero at the junction", "d) Added at each branch"], "b"),
        ]
    },
    {
        "title": "Mathematics 101 - Chapter 4: Calculus Fundamentals",
        "questions": [
            ("The derivative of sin(x) is:", ["a) cos(x)", "b) -cos(x)", "c) tan(x)", "d) -sin(x)"], "a"),
            ("What is the integral of 1/x dx?", ["a) x^2/2 + C", "b) ln|x| + C", "c) e^x + C", "d) 1/x^2 + C"], "b"),
            ("The limit of (sin x)/x as x approaches 0 is:", ["a) 0", "b) infinity", "c) 1", "d) undefined"], "c"),
            ("The chain rule is used when differentiating:", ["a) Sums of functions", "b) Products of functions", "c) Composite functions", "d) Quotients of functions"], "c"),
            ("What does the second derivative test determine?", ["a) Inflection points only", "b) Whether a critical point is a max or min", "c) The slope of a tangent line", "d) The area under the curve"], "b"),
            ("Integration by parts follows the formula:", ["a) uv - integral(u dv)", "b) uv + integral(v du)", "c) uv - integral(v du)", "d) integral(u) * integral(v)"], "c"),
            ("A function is concave down when its second derivative is:", ["a) Positive", "b) Zero", "c) Negative", "d) Undefined"], "c"),
            ("The Fundamental Theorem of Calculus connects:", ["a) Algebra and geometry", "b) Differentiation and integration", "c) Limits and sequences", "d) Trigonometry and calculus"], "b"),
            ("What is the derivative of e^x?", ["a) xe^(x-1)", "b) e^x * ln(e)", "c) e^x", "d) e^(x+1)"], "c"),
            ("L'Hopital's rule applies when a limit is in the form:", ["a) 0/infinity", "b) 0/0 or infinity/infinity", "c) infinity/0", "d) 1/infinity"], "b"),
        ]
    },
    {
        "title": "History 201 - Chapter 6: World War II",
        "questions": [
            ("World War II began in:", ["a) 1935", "b) 1937", "c) 1939", "d) 1941"], "c"),
            ("The Allied forces that liberated France in 1944 launched which operation?", ["a) Operation Barbarossa", "b) Operation Overlord", "c) Operation Market Garden", "d) Operation Sea Lion"], "b"),
            ("Which event caused the United States to enter World War II?", ["a) Invasion of Poland", "b) Fall of France", "c) Attack on Pearl Harbor", "d) Battle of Britain"], "c"),
            ("The Holocaust was the systematic murder of approximately how many Jewish people?", ["a) 1 million", "b) 3 million", "c) 6 million", "d) 10 million"], "c"),
            ("Which conference divided post-war Europe between the Allies?", ["a) Paris Peace Conference", "b) Tehran Conference", "c) Yalta Conference", "d) Potsdam Conference"], "c"),
            ("The Manhattan Project resulted in:", ["a) Development of radar", "b) Creation of the atomic bomb", "c) German rocket technology", "d) Mass production of tanks"], "b"),
            ("Japan surrendered on which date in 1945?", ["a) May 8", "b) June 6", "c) August 15", "d) September 2"], "d"),
            ("The Nuremberg Trials were held to prosecute:", ["a) Soviet war criminals", "b) Japanese military leaders", "c) Nazi war criminals", "d) Italian Fascist leaders"], "c"),
            ("Operation Barbarossa was Germany's invasion of:", ["a) France", "b) Britain", "c) Soviet Union", "d) Poland"], "c"),
            ("The Battle of Stalingrad was a turning point because:", ["a) Germany captured Moscow", "b) Allies landed in Normandy", "c) Germany suffered its first major defeat", "d) Japan attacked Pearl Harbor"], "c"),
        ]
    },
    {
        "title": "Literature 102 - Chapter 8: Modern American Literature",
        "questions": [
            ("Who wrote 'The Great Gatsby'?", ["a) Ernest Hemingway", "b) F. Scott Fitzgerald", "c) William Faulkner", "d) John Steinbeck"], "b"),
            ("The term 'stream of consciousness' refers to:", ["a) Dialogue-heavy narrative", "b) Third-person omniscient narration", "c) A narrative technique depicting thought flow", "d) Plot-driven storytelling"], "c"),
            ("Which novel features the character Atticus Finch?", ["a) Of Mice and Men", "b) The Catcher in the Rye", "c) To Kill a Mockingbird", "d) Beloved"], "c"),
            ("The Lost Generation refers to:", ["a) Young writers during the Cold War", "b) American writers disillusioned after World War I", "c) Beat Generation writers of the 1950s", "d) Writers of the Harlem Renaissance"], "b"),
            ("Which work is considered the foundation of American literature by Ralph Ellison?", ["a) Moby Dick", "b) Invisible Man", "c) Native Son", "d) Their Eyes Were Watching God"], "b"),
            ("Hemingway's 'iceberg theory' suggests that:", ["a) Most meaning should be explicit", "b) Stories should be set in cold climates", "c) The deeper meaning lies beneath the surface", "d) Short sentences are always better"], "c"),
            ("The Harlem Renaissance was primarily a movement in:", ["a) Literature and music only", "b) Political activism only", "c) African American arts and culture", "d) Visual arts only"], "c"),
            ("Which poet is associated with the phrase 'I celebrate myself'?", ["a) Emily Dickinson", "b) Walt Whitman", "c) Robert Frost", "d) Langston Hughes"], "b"),
            ("The protagonist of 'The Catcher in the Rye' is:", ["a) Tom Sawyer", "b) Huck Finn", "c) Jay Gatsby", "d) Holden Caulfield"], "d"),
            ("Magical realism combines:", ["a) Science fiction and horror", "b) Realistic settings with fantastical elements", "c) Mystery and romance", "d) Historical fiction and fantasy"], "b"),
        ]
    },
    {
        "title": "Economics 301 - Chapter 9: Macroeconomics",
        "questions": [
            ("GDP stands for:", ["a) Gross Domestic Product", "b) General Development Policy", "c) Government Debt Percentage", "d) Global Distribution Price"], "a"),
            ("Inflation is defined as:", ["a) A decrease in the money supply", "b) A sustained increase in the general price level", "c) Reduction in government spending", "d) An increase in real wages"], "b"),
            ("The Phillips Curve illustrates the relationship between:", ["a) GDP and unemployment", "b) Inflation and interest rates", "c) Inflation and unemployment", "d) GDP and inflation"], "c"),
            ("Monetary policy is controlled by:", ["a) The President", "b) Congress", "c) The Central Bank", "d) The Treasury Department"], "c"),
            ("A budget deficit occurs when:", ["a) Exports exceed imports", "b) Tax revenue exceeds government spending", "c) Government spending exceeds tax revenue", "d) GDP growth is negative"], "c"),
            ("Keynesian economics advocates for:", ["a) Reducing government intervention", "b) Free market solutions", "c) Government spending to stimulate demand", "d) Supply-side tax cuts"], "c"),
            ("The multiplier effect describes how:", ["a) Taxes reduce consumer spending", "b) An initial spending increase leads to greater total output", "c) Inflation reduces purchasing power", "d) Interest rates affect investment"], "b"),
            ("Stagflation is characterized by:", ["a) High growth and low inflation", "b) High inflation and low unemployment", "c) High inflation and high unemployment", "d) Low growth and low inflation"], "c"),
            ("The velocity of money refers to:", ["a) How fast prices change", "b) The rate at which money circulates in the economy", "c) The speed of international transactions", "d) How quickly banks lend money"], "b"),
            ("Comparative advantage explains why countries:", ["a) Should be self-sufficient", "b) Should not trade with each other", "c) Benefit from specialization and trade", "d) Should impose tariffs"], "c"),
        ]
    },
    {
        "title": "Computer Science 201 - Chapter 5: Data Structures",
        "questions": [
            ("What is the time complexity of searching in a balanced BST?", ["a) O(1)", "b) O(n)", "c) O(log n)", "d) O(n log n)"], "c"),
            ("A stack follows which principle?", ["a) FIFO", "b) LIFO", "c) FILO", "d) LIFI"], "b"),
            ("Which data structure uses nodes with two pointers?", ["a) Array", "b) Stack", "c) Queue", "d) Doubly linked list"], "d"),
            ("The time complexity of quicksort on average is:", ["a) O(n)", "b) O(n log n)", "c) O(n^2)", "d) O(log n)"], "b"),
            ("What is a hash collision?", ["a) When two different keys map to the same hash value", "b) When the hash table is full", "c) When a key cannot be found", "d) When two hash tables are merged"], "a"),
            ("A complete binary tree has nodes filled:", ["a) From right to left", "b) Randomly", "c) From left to right at each level", "d) Only at the leaf level"], "c"),
            ("Which traversal visits the root last?", ["a) Preorder", "b) Inorder", "c) Postorder", "d) Level order"], "c"),
            ("A graph with no cycles is called:", ["a) Complete graph", "b) Bipartite graph", "c) Tree", "d) Connected graph"], "c"),
            ("Dynamic programming works by:", ["a) Using recursion only", "b) Storing solutions to subproblems to avoid recomputation", "c) Dividing problems into equal halves", "d) Using greedy choices"], "b"),
            ("The worst-case time complexity of bubble sort is:", ["a) O(n log n)", "b) O(n)", "c) O(log n)", "d) O(n^2)"], "d"),
        ]
    },
    {
        "title": "Psychology 101 - Chapter 10: Learning and Memory",
        "questions": [
            ("Classical conditioning was first described by:", ["a) B.F. Skinner", "b) Ivan Pavlov", "c) William James", "d) Sigmund Freud"], "b"),
            ("Operant conditioning uses:", ["a) Stimulus-response associations", "b) Cognitive maps", "c) Reinforcement and punishment", "d) Unconscious drives"], "c"),
            ("Working memory has a capacity of approximately:", ["a) 3-4 items", "b) 7 plus or minus 2 items", "c) 12-15 items", "d) Unlimited items"], "b"),
            ("Long-term potentiation is associated with:", ["a) Short-term memory formation", "b) Synaptic strengthening and memory", "c) Forgetting", "d) Sleep regulation"], "b"),
            ("The serial position effect refers to:", ["a) Better recall of middle items", "b) Better recall of first and last items in a list", "c) Recall declining over time", "d) Interference between memories"], "b"),
            ("Implicit memory involves:", ["a) Deliberate recollection of facts", "b) Conscious episodic memories", "c) Unconscious memory for skills and conditioning", "d) Working memory only"], "c"),
            ("The spacing effect suggests that learning is better when:", ["a) Practice is massed in one session", "b) Study sessions are spread over time", "c) Information is repeated immediately", "d) Rewards are given instantly"], "b"),
            ("Anterograde amnesia affects:", ["a) Memories formed before the injury", "b) Procedural memory only", "c) The ability to form new memories after the injury", "d) Motor skills only"], "c"),
            ("Schema theory describes how:", ["a) Memories are stored chemically", "b) Prior knowledge frameworks organize new information", "c) Fear is conditioned", "d) Punishment reduces behavior"], "b"),
            ("The tip-of-the-tongue phenomenon is a form of:", ["a) Complete forgetting", "b) Retrieval failure with partial accessibility", "c) Retrograde amnesia", "d) Proactive interference"], "b"),
        ]
    },
    {
        "title": "Environmental Science 201 - Chapter 12: Climate Change",
        "questions": [
            ("The greenhouse effect is caused primarily by:", ["a) Ozone depletion", "b) Greenhouse gases trapping heat", "c) Solar radiation increase", "d) Ocean current changes"], "b"),
            ("Which gas contributes most to the greenhouse effect?", ["a) Oxygen", "b) Nitrogen", "c) Carbon dioxide", "d) Argon"], "c"),
            ("The IPCC stands for:", ["a) International Panel on Carbon Control", "b) Intergovernmental Panel on Climate Change", "c) International Program for Climate Conservation", "d) Integrated Panel for Carbon Credits"], "b"),
            ("Sea level rise is caused by:", ["a) Increased rainfall only", "b) Thermal expansion and melting ice", "c) Ocean basin changes", "d) Decreased ocean salinity"], "b"),
            ("The Kyoto Protocol was an agreement to:", ["a) Protect endangered species", "b) Manage ocean resources", "c) Reduce greenhouse gas emissions", "d) Prevent ozone depletion"], "c"),
            ("Ocean acidification occurs when CO2:", ["a) Evaporates from seawater", "b) Dissolves in seawater forming carbonic acid", "c) Reacts with salt to form acid", "d) Is absorbed by marine plants"], "b"),
            ("The carbon cycle involves:", ["a) Only photosynthesis", "b) Only respiration", "c) Exchange of carbon between atmosphere, biosphere, and oceans", "d) Industrial carbon capture only"], "c"),
            ("Renewable energy sources include:", ["a) Coal and oil", "b) Natural gas and nuclear", "c) Solar, wind, and hydropower", "d) Peat and biomass only"], "c"),
            ("The albedo effect refers to:", ["a) The warming caused by CO2", "b) The reflectivity of surfaces affecting energy absorption", "c) The cooling from volcanic eruptions", "d) Atmospheric ozone concentration"], "b"),
            ("Climate models predict that average global temperatures by 2100 could rise by:", ["a) Less than 0.5°C", "b) Between 1.5°C and 4°C", "c) More than 10°C", "d) Exactly 2°C"], "b"),
        ]
    },
]


def format_question_line(q_text, options, answer):
    """Format a question with options and mark the correct answer in brackets."""
    lines = [q_text]
    for opt in options:
        opt_letter = opt[0]  # e.g., 'a'
        if opt_letter == answer:
            lines.append(f"  {opt} [{answer.upper()}]")
        else:
            lines.append(f"  {opt}")
    return "\n".join(lines)


def create_test_file(filepath, test_data):
    """Write a single test file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"{test_data['title']}\n")
        f.write("=" * 60 + "\n\n")
        for i, (q_text, options, answer) in enumerate(test_data['questions'], 1):
            f.write(f"Question {i}:\n")
            f.write(format_question_line(q_text, options, answer))
            f.write("\n\n")


def create_initial():
    # Create Documents directory if it doesn't exist
    os.makedirs(DOCUMENTS, exist_ok=True)

    # Create semester_tests directory
    os.makedirs(SEMESTER_TESTS_DIR, exist_ok=True)

    # Remove any existing final_exam_complete.odt (if any leftover from previous run)
    final_exam_path = os.path.join(WORKDIR, 'final_exam_complete.odt')
    if os.path.exists(final_exam_path):
        os.remove(final_exam_path)
        print(f"Removed leftover: {final_exam_path}")

    # Create each test file
    for idx, test_data in enumerate(TEST_DATA, 1):
        filename = f"test_{idx:02d}.txt"
        filepath = os.path.join(SEMESTER_TESTS_DIR, filename)
        create_test_file(filepath, test_data)
        print(f"Created: {filepath}")

    print(f"\nAll 10 test files created in: {SEMESTER_TESTS_DIR}")

    # GUI-ready startup: open LibreOffice Writer (new empty document) and Nautilus showing semester_tests folder
    launch_gui('libreoffice --writer', delay_sec=2.0)
    launch_gui(f'nautilus "{SEMESTER_TESTS_DIR}"', delay_sec=1.5)
    print('GUI_READY: launched LibreOffice Writer and Nautilus with semester_tests folder (DISPLAY=:0)')


create_initial()
