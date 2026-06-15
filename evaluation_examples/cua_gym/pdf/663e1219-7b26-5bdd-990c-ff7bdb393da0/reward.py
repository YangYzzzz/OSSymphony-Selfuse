"""
Reward Script: PDF-based quiz grader verification
Task ID: pdf_gf3_047
Domain: pdf
Scoring:
  Component 1 (0.15): quiz_grader.py exists and is executable Python
  Component 2 (0.20): quiz_grader.py runs without errors and produces grade_report.pdf
  Component 3 (0.20): quiz_grader.py reads form fields from student PDF (uses widgets)
  Component 4 (0.15): grade_report.pdf is a valid PDF with student name and total score
  Component 5 (0.15): grade_report.pdf contains per-question MC breakdown with incorrect answers flagged
  Component 6 (0.15): grade_report.pdf contains SA results with keyword info
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_047'

SCRIPT_PATH = f'{WORKDIR}/scripts/quiz_grader.py'
GRADE_REPORT_PATH = f'{WORKDIR}/quizzes/grade_report.pdf'
STUDENT_PDF_PATH = f'{WORKDIR}/quizzes/student_answers.pdf'
ANSWER_KEY_PATH = f'{WORKDIR}/quizzes/answer_key.json'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: quiz_grader.py exists and is valid Python (0.15 points)
    try:
        if not os.path.exists(SCRIPT_PATH):
            print(f"FAIL: Component 1 — {SCRIPT_PATH} does not exist")
        else:
            with open(SCRIPT_PATH, 'r') as f:
                code = f.read()
            # Verify it's non-trivial Python (has key function definitions or imports)
            compile(code, SCRIPT_PATH, 'exec')
            if len(code) > 200:
                print(f"PASS: Component 1 — quiz_grader.py exists and is valid Python ({len(code)} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — quiz_grader.py is too small ({len(code)} bytes), likely not a real implementation")
    except SyntaxError as e:
        print(f"FAIL: Component 1 — quiz_grader.py has syntax errors: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Script runs without errors and produces grade_report.pdf (0.20 points)
    # First, remove any existing grade_report.pdf to verify the script actually creates it
    try:
        if os.path.exists(GRADE_REPORT_PATH):
            os.remove(GRADE_REPORT_PATH)

        if os.path.exists(SCRIPT_PATH):
            # Run the script and verify it produces grade_report.pdf
            exit_code = os.system(f'cd {WORKDIR} && python3 {SCRIPT_PATH} > /tmp/grader_output.txt 2>&1')

            if exit_code == 0 and os.path.exists(GRADE_REPORT_PATH):
                print(f"PASS: Component 2 — quiz_grader.py runs successfully and creates grade_report.pdf (0.20 pts)")
                total_score += 0.20
            elif exit_code != 0:
                # Read error output
                try:
                    with open('/tmp/grader_output.txt', 'r') as f:
                        err = f.read()[:500]
                    print(f"FAIL: Component 2 — quiz_grader.py exited with code {exit_code}: {err}")
                except:
                    print(f"FAIL: Component 2 — quiz_grader.py exited with code {exit_code}")
            else:
                print(f"FAIL: Component 2 — quiz_grader.py ran but did not create grade_report.pdf")
        else:
            print(f"FAIL: Component 2 — quiz_grader.py does not exist, cannot run")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Script reads form fields using widgets (0.20 points)
    # Verify the script source code contains proper form-field reading logic
    try:
        if os.path.exists(SCRIPT_PATH):
            with open(SCRIPT_PATH, 'r') as f:
                code = f.read()

            has_widget_read = ('widget' in code.lower() or 'widgets' in code.lower() or
                               'field_name' in code or 'field_value' in code or
                               'get_form_text' in code or 'AcroForm' in code)
            has_pdf_lib = ('pymupdf' in code or 'import fitz' in code or 'pikepdf' in code)
            has_answer_key = ('answer_key' in code or 'answer_key.json' in code or 'mc_answers' in code)
            has_json = ('json' in code)

            checks_passed = 0
            if has_widget_read:
                checks_passed += 1
            if has_pdf_lib:
                checks_passed += 1
            if has_answer_key and has_json:
                checks_passed += 1

            if checks_passed >= 3:
                print(f"PASS: Component 3 — Script reads form fields (widgets={has_widget_read}, pdf_lib={has_pdf_lib}, answer_key={has_answer_key}) (0.20 pts)")
                total_score += 0.20
            elif checks_passed >= 2:
                print(f"PARTIAL: Component 3 — Script has partial form field reading ({checks_passed}/3 checks) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — Script does not properly read form fields (widget={has_widget_read}, pdf_lib={has_pdf_lib}, answer_key={has_answer_key})")
        else:
            print(f"FAIL: Component 3 — quiz_grader.py does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: grade_report.pdf has student name and total score (0.15 points)
    try:
        if not os.path.exists(GRADE_REPORT_PATH):
            print(f"FAIL: Component 4 — grade_report.pdf does not exist")
        else:
            import pymupdf
            doc = pymupdf.open(GRADE_REPORT_PATH)
            all_text = ""
            for page in doc:
                all_text += page.get_text()
            doc.close()

            has_student_name = 'Emily Rodriguez' in all_text or 'emily rodriguez' in all_text.lower()
            # Check for total score - should show something like "71 / 80" or "71/80" or "Total Score: 71"
            has_total_score = ('/ 80' in all_text or '/80' in all_text or
                               'out of 80' in all_text.lower() or
                               'total' in all_text.lower())

            if has_student_name and has_total_score:
                print(f"PASS: Component 4 — grade_report.pdf contains student name and total score (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — student_name={has_student_name}, total_score={has_total_score}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: grade_report.pdf contains per-question MC breakdown with incorrect answers flagged (0.15 points)
    try:
        if not os.path.exists(GRADE_REPORT_PATH):
            print(f"FAIL: Component 5 — grade_report.pdf does not exist")
        else:
            import pymupdf
            doc = pymupdf.open(GRADE_REPORT_PATH)
            all_text = ""
            for page in doc:
                all_text += page.get_text()
            doc.close()

            text_lower = all_text.lower()

            # Check for MC per-question breakdown
            # Should have question references like Q1, Q2, etc. or mc_1 etc.
            has_question_refs = sum(1 for i in range(1, 31) if f'Q{i}' in all_text or f'q{i}' in text_lower or f'mc_{i}' in text_lower)

            # Check that incorrect answers are flagged (the golden shows "Incorrect (answer: X)")
            has_incorrect_flag = ('incorrect' in text_lower or 'wrong' in text_lower or
                                  'correct answer' in text_lower or 'answer:' in text_lower)

            if has_question_refs >= 15 and has_incorrect_flag:
                print(f"PASS: Component 5 — MC breakdown present ({has_question_refs} questions referenced, incorrect flagged) (0.15 pts)")
                total_score += 0.15
            elif has_question_refs >= 10:
                print(f"PARTIAL: Component 5 — Partial MC breakdown ({has_question_refs} questions, incorrect_flag={has_incorrect_flag}) (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 5 — MC breakdown missing (questions_found={has_question_refs}, incorrect_flag={has_incorrect_flag})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: grade_report.pdf contains SA results with keyword info (0.15 points)
    try:
        if not os.path.exists(GRADE_REPORT_PATH):
            print(f"FAIL: Component 6 — grade_report.pdf does not exist")
        else:
            import pymupdf
            doc = pymupdf.open(GRADE_REPORT_PATH)
            all_text = ""
            for page in doc:
                all_text += page.get_text()
            doc.close()

            text_lower = all_text.lower()

            # Check for SA question references
            has_sa_refs = sum(1 for i in range(1, 11) if f'SA{i}' in all_text or f'sa{i}' in text_lower or f'sa_{i}' in text_lower or f'Short Answer {i}' in all_text)

            # Check for keyword-related information
            has_keyword_info = ('keyword' in text_lower or 'matched' in text_lower or
                                'missing' in text_lower or '/ 5' in all_text or '/5' in all_text)

            # Check for SA scores (e.g., "5 / 5", "3 / 5", etc.)
            has_sa_scores = ('/ 5' in all_text or '/5' in all_text or
                             'score:' in text_lower or 'points' in text_lower)

            if has_sa_refs >= 5 and (has_keyword_info or has_sa_scores):
                print(f"PASS: Component 6 — SA results present ({has_sa_refs} SA questions, keywords={has_keyword_info}, scores={has_sa_scores}) (0.15 pts)")
                total_score += 0.15
            elif has_sa_refs >= 3:
                print(f"PARTIAL: Component 6 — Partial SA results ({has_sa_refs} SA questions) (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 6 — SA results missing (sa_refs={has_sa_refs}, keyword_info={has_keyword_info})")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
