"""
Reward Script: Remove duplicate reference entries from bibliography section
Task ID: osworld_writer_duplicate_line_removal_005
Domain: libreoffice_writer
Scoring:
  Component 1: Exactly 9 reference entries remain after the References heading (0.4 pts)
  Component 2: No duplicate reference entries (all unique) (0.3 pts)
  Component 3: The 9 unique references match the expected set and order (0.3 pts)
Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_duplicate_line_removal_005'

# The 9 expected unique reference texts (in original order), identified from task context
EXPECTED_REFERENCES = [
    '[1] Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). Efficient estimation of word representations in vector space. arXiv preprint arXiv:1301.3781.',
    '[2] Sutskever, I., Vinyals, O., & Le, Q. V. (2014). Sequence to sequence learning with neural networks. Advances in Neural Information Processing Systems, 27.',
    '[3] Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural machine translation by jointly learning to align and translate. International Conference on Learning Representations (ICLR).',
    '[4] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). Attention is all you need. Advances in Neural Information Processing Systems, 30.',
    '[5] Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. Proceedings of NAACL-HLT 2019, 4171\u20134186.',
    '[6] Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., et al. (2020). Language models are few-shot learners. Advances in Neural Information Processing Systems, 33.',
    '[7] Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., & Amodei, D. (2020). Scaling laws for neural language models. arXiv preprint arXiv:2001.08361.',
    '[8] Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., Levy, O., Lewis, M., Zettlemoyer, L., & Stoyanov, V. (2019). RoBERTa: A robustly optimized BERT pretraining approach. arXiv preprint arXiv:1907.11692.',
    '[9] Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., & Sutskever, I. (2019). Language models are unsupervised multitask learners. OpenAI Blog, 1(8).',
]


def get_reference_paragraphs(doc):
    """Extract non-empty paragraph texts that appear after the 'References' heading."""
    refs = []
    in_refs = False
    for para in doc.paragraphs:
        text = para.text.strip()
        if text == 'References':
            in_refs = True
            continue
        if in_refs and text:
            refs.append(text)
    return refs


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate the reference entries in the document
    ref_entries = get_reference_paragraphs(doc)
    print(f"INFO: Found {len(ref_entries)} reference entries after 'References' heading")
    for i, r in enumerate(ref_entries):
        print(f"  ref[{i}]: {r[:80]}")

    # Component 1: Exactly 9 reference entries remain (0.4 points)
    # Task requires removing 5 duplicates from the 14 initial entries, leaving 9 unique ones.
    # Initial doc has 14 entries; golden has 9. This check fails on initial (14 != 9).
    try:
        expected_count = 9
        actual_count = len(ref_entries)
        if actual_count == expected_count:
            print(f"PASS: Component 1 — exactly {expected_count} reference entries found (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected {expected_count} reference entries, found {actual_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No duplicate reference entries — all entries are unique (0.3 points)
    # Initial doc has 5 duplicates; golden has none. This check fails on initial.
    try:
        unique_refs = set(ref_entries)
        if len(unique_refs) == len(ref_entries):
            print(f"PASS: Component 2 — all {len(ref_entries)} reference entries are unique (0.3 pts)")
            total_score += 0.3
        else:
            num_dups = len(ref_entries) - len(unique_refs)
            print(f"FAIL: Component 2 — found {num_dups} duplicate reference entries")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The references match expected set in the correct original order (0.3 points)
    # Verifies that the 9 unique refs are the correct ones and in the right sequence.
    # This fails on initial (wrong count / extra refs present).
    try:
        # Compare each expected reference against actual, checking both content and order
        order_match = True
        if len(ref_entries) == len(EXPECTED_REFERENCES):
            for idx, (actual, expected) in enumerate(zip(ref_entries, EXPECTED_REFERENCES)):
                if actual.strip() != expected.strip():
                    print(f"FAIL: Component 3 — ref[{idx}] mismatch.")
                    print(f"  Expected: {expected[:80]!r}")
                    print(f"  Actual:   {actual[:80]!r}")
                    order_match = False
                    break
        else:
            order_match = False
            print(f"FAIL: Component 3 — count mismatch ({len(ref_entries)} vs {len(EXPECTED_REFERENCES)}), skipping order check")

        if order_match:
            print(f"PASS: Component 3 — references match expected set and order (0.3 pts)")
            total_score += 0.3
        else:
            if len(ref_entries) != len(EXPECTED_REFERENCES):
                pass  # already printed above
            # else mismatch already printed inside loop
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
