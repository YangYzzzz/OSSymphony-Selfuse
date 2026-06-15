"""
Reward Script: Per-chapter mini Table of Contents
Task ID: writer_mt_073
Domain: libreoffice_writer
Scoring:
  Component 1 (0.20): Four "In This Chapter" title paragraphs exist
  Component 2 (0.20): Each mini-TOC is placed immediately after its chapter Heading 1
  Component 3 (0.15): Chapter 1 mini-TOC lists correct H2/H3 entries
  Component 4 (0.15): Chapter 2 mini-TOC lists correct H2/H3 entries
  Component 5 (0.15): Chapter 3 mini-TOC lists correct H2/H3 entries
  Component 6 (0.15): Chapter 4 mini-TOC lists correct H2/H3 entries
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_073'

# Expected chapter titles (Heading 1)
CHAPTER_TITLES = [
    "Chapter 1: Introduction to Data Science",
    "Chapter 2: Statistical Methods and Analysis",
    "Chapter 3: Machine Learning Fundamentals",
    "Chapter 4: Data Visualization and Communication",
]

# Expected H2 and H3 sub-sections per chapter (from the initial document structure)
EXPECTED_SUBSECTIONS = {
    "Chapter 1: Introduction to Data Science": [
        "The Evolution of Data Science",
        "Historical Milestones",
        "The Big Data Revolution",
        "Core Disciplines and Skill Sets",
        "Statistical Foundations",
        "Programming Proficiency",
        "The Data Science Lifecycle",
        "Problem Formulation",
        "Data Collection Strategies",
        "Model Deployment",
        "Ethics in Data Science",
        "Privacy and Consent",
        "Algorithmic Bias",
        "Industry Applications Overview",
        "Healthcare Analytics",
        "Financial Modeling",
        "Tools and Technologies",
        "Python Ecosystem",
        "Cloud Computing Platforms",
    ],
    "Chapter 2: Statistical Methods and Analysis": [
        "Descriptive Statistics",
        "Measures of Central Tendency",
        "Variability and Spread",
        "Probability Distributions",
        "Normal Distribution",
        "Discrete Distributions",
        "Distribution Fitting",
        "Hypothesis Testing",
        "Type I and Type II Errors",
        "Power Analysis",
        "Regression Analysis",
        "Simple Linear Regression",
        "Multiple Regression",
        "Model Diagnostics",
        "Bayesian Statistics",
        "Prior and Posterior Distributions",
        "Markov Chain Monte Carlo",
        "Experimental Design",
        "Randomized Controlled Trials",
        "A/B Testing in Practice",
        "Nonparametric Methods",
        "Rank-Based Tests",
        "Bootstrap Methods",
    ],
    "Chapter 3: Machine Learning Fundamentals": [
        "Supervised Learning",
        "Classification Algorithms",
        "Regression Algorithms",
        "Feature Engineering",
        "Unsupervised Learning",
        "Clustering Methods",
        "Dimensionality Reduction",
        "Model Evaluation and Validation",
        "Cross-Validation Techniques",
        "Performance Metrics",
        "Overfitting Prevention",
        "Ensemble Methods",
        "Bagging and Random Forests",
        "Gradient Boosting Machines",
        "Neural Networks and Deep Learning",
        "Feedforward Networks",
        "Convolutional Neural Networks",
        "Recurrent Networks",
        "Practical Machine Learning Pipelines",
        "Data Pipeline Design",
        "Model Serving and Monitoring",
    ],
    "Chapter 4: Data Visualization and Communication": [
        "Principles of Effective Visualization",
        "Tufte's Principles",
        "The Grammar of Graphics",
        "Chart Types and Selection",
        "Comparison Charts",
        "Distribution Charts",
        "Relationship Charts",
        "Interactive Visualizations",
        "Dashboard Design",
        "User Interaction Patterns",
        "Visualization Tools and Libraries",
        "Python Visualization Stack",
        "Business Intelligence Tools",
        "Storytelling with Data",
        "Narrative Structure",
        "Audience Adaptation",
    ],
}


def verify_task(file_path):
    """
    Verify that per-chapter mini-TOCs have been inserted.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs

    # Build a map: chapter_title -> paragraph index of the Heading 1
    chapter_indices = []
    for i, para in enumerate(paragraphs):
        style = para.style.name if para.style else ''
        if style == 'Heading 1' and para.text.strip() in CHAPTER_TITLES:
            chapter_indices.append((i, para.text.strip()))

    # Find "In This Chapter" paragraphs
    itc_indices = []
    for i, para in enumerate(paragraphs):
        if para.text.strip() == 'In This Chapter':
            itc_indices.append(i)

    # Component 1: Four "In This Chapter" title paragraphs exist (0.20 points)
    try:
        itc_count = len(itc_indices)
        if itc_count == 4:
            print(f"PASS: Component 1 -- Found 4 'In This Chapter' paragraphs (0.20 pts)")
            total_score += 0.20
        elif itc_count > 0:
            partial = 0.20 * (min(itc_count, 4) / 4.0)
            print(f"PARTIAL: Component 1 -- Found {itc_count}/4 'In This Chapter' paragraphs ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No 'In This Chapter' paragraphs found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Each mini-TOC is placed immediately after its chapter Heading 1 (0.20 points)
    try:
        correctly_placed = 0
        for ch_idx, ch_title in chapter_indices:
            # Check if the paragraph right after (ch_idx + 1) is "In This Chapter"
            if (ch_idx + 1) < len(paragraphs):
                next_text = paragraphs[ch_idx + 1].text.strip()
                if next_text == 'In This Chapter':
                    correctly_placed += 1
                else:
                    print(f"  INFO: After '{ch_title}' (para {ch_idx}), found '{next_text[:60]}' instead of 'In This Chapter'")
            else:
                print(f"  INFO: No paragraph after '{ch_title}' (para {ch_idx})")

        if correctly_placed == 4:
            print(f"PASS: Component 2 -- All 4 mini-TOCs placed correctly after chapter headings (0.20 pts)")
            total_score += 0.20
        elif correctly_placed > 0:
            partial = 0.20 * (correctly_placed / 4.0)
            print(f"PARTIAL: Component 2 -- {correctly_placed}/4 mini-TOCs placed correctly ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No mini-TOCs placed correctly after chapter headings")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Components 3-6: Verify each chapter's mini-TOC contains correct entries
    # For each chapter, extract the text between "In This Chapter" and the next heading or body text
    def extract_mini_toc_entries(doc_paragraphs, itc_para_index):
        """Extract the TOC entry texts from the mini-TOC starting at itc_para_index."""
        entries = []
        idx = itc_para_index + 1
        while idx < len(doc_paragraphs):
            para = doc_paragraphs[idx]
            text = para.text.strip()
            style = para.style.name if para.style else ''
            # Stop at headings or empty paragraphs followed by body text
            if style.startswith('Heading'):
                break
            if text == '':
                # Empty paragraph signals end of TOC block
                break
            entries.append(text)
            idx += 1
        return entries

    chapter_component_weights = [0.15, 0.15, 0.15, 0.15]
    for comp_num, (ch_title, weight) in enumerate(zip(CHAPTER_TITLES, chapter_component_weights), start=3):
        try:
            expected = EXPECTED_SUBSECTIONS[ch_title]

            # Find the "In This Chapter" paragraph for this chapter
            ch_itc_idx = None
            for ch_idx, ch_name in chapter_indices:
                if ch_name == ch_title and (ch_idx + 1) < len(paragraphs):
                    if paragraphs[ch_idx + 1].text.strip() == 'In This Chapter':
                        ch_itc_idx = ch_idx + 1
                        break

            if ch_itc_idx is None:
                print(f"FAIL: Component {comp_num} -- No mini-TOC found for '{ch_title}'")
                continue

            actual_entries = extract_mini_toc_entries(paragraphs, ch_itc_idx)

            # Check how many expected entries are present in the actual TOC
            matched = 0
            for exp_entry in expected:
                if any(exp_entry in act for act in actual_entries):
                    matched += 1

            match_ratio = matched / len(expected) if expected else 0

            if match_ratio >= 0.9:
                print(f"PASS: Component {comp_num} -- '{ch_title}' mini-TOC has {matched}/{len(expected)} entries ({weight} pts)")
                total_score += weight
            elif match_ratio > 0:
                partial = weight * match_ratio
                print(f"PARTIAL: Component {comp_num} -- '{ch_title}' mini-TOC has {matched}/{len(expected)} entries ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component {comp_num} -- '{ch_title}' mini-TOC has 0/{len(expected)} matching entries")
        except Exception as e:
            print(f"ERROR: Component {comp_num} -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
