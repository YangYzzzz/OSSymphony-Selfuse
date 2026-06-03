"""
Reward Script: Reply to existing comment on 'methodology' with specified text
Task ID: writer_struct_023
Domain: libreoffice_writer
Scoring:
  Component 1: Reply comment with exact required text exists in comments.xml (0.5 pts)
  Component 2: Reply is properly threaded under original comment via commentsExtended.xml (0.3 pts)
  Component 3: Original comment text remains unchanged (0.2 pts, gated on C1)
  Total: 1.0
"""

import os
import zipfile
import lxml.etree as etree

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_023'
FILE_PATH = os.path.join(WORKDIR, 'journal_submission.docx')

REQUIRED_REPLY_TEXT = 'Updated to reflect the mixed-methods approach discussed in Section 3.'
ORIGINAL_COMMENT_TEXT = 'Please clarify which methodology was used.'

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W14_NS = 'http://schemas.microsoft.com/office/word/2010/wordml'
W15_NS = 'http://schemas.microsoft.com/office/word/2012/wordml'


def get_comment_text(comment_elem):
    """Extract full text from a w:comment element."""
    ns = {'w': W_NS}
    texts = []
    for t in comment_elem.findall('.//w:t', ns):
        texts.append(t.text or '')
    return ''.join(texts)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    if not os.path.exists(file_path):
        print('CRITICAL: File not found: %s' % file_path)
        print('REWARD: 0.0')
        return 0.0

    try:
        z = zipfile.ZipFile(file_path, 'r')
        names = z.namelist()
        comments_xml_content = z.read('word/comments.xml') if 'word/comments.xml' in names else None
        comments_extended_xml_content = (
            z.read('word/commentsExtended.xml') if 'word/commentsExtended.xml' in names else None
        )
        z.close()
    except Exception as e:
        print('CRITICAL: Cannot open or read docx file: %s' % e)
        print('REWARD: 0.0')
        return 0.0

    if comments_xml_content is None:
        print('CRITICAL: No comments.xml found in the docx.')
        print('REWARD: 0.0')
        return 0.0

    # Parse comments.xml
    try:
        comments_root = etree.fromstring(comments_xml_content)
    except Exception as e:
        print('CRITICAL: Cannot parse comments.xml: %s' % e)
        print('REWARD: 0.0')
        return 0.0

    ns = {'w': W_NS}
    all_comments = comments_root.findall('w:comment', ns)
    print('Total comments found: %d' % len(all_comments))

    # Build a list of comment dicts: id, text, paraId
    comment_list = []
    for c in all_comments:
        cid = c.get('{%s}id' % W_NS)
        text = get_comment_text(c)
        para_elems = c.findall('w:p', ns)
        para_id = para_elems[0].get('{%s}paraId' % W14_NS) if para_elems else None
        comment_list.append({'id': cid, 'text': text, 'paraId': para_id})
        print('  Comment id=%s paraId=%s text=%r' % (cid, para_id, text))

    # ------------------------------------------------------------------
    # Component 1: A reply comment exists with the exact required text (0.5 pts)
    # Fails on initial (only 1 comment, no reply). Passes on golden (2 comments).
    # ------------------------------------------------------------------
    try:
        matching_replies = [c for c in comment_list if c['text'] == REQUIRED_REPLY_TEXT]
        if len(matching_replies) >= 1:
            reply_entry = matching_replies[0]
            print('PASS: Component 1 — Reply comment with required text found (id=%s) (0.5 pts)' % reply_entry['id'])
            total_score += 0.5
        else:
            # Diagnostic: check for partial match
            partial = [c for c in comment_list if REQUIRED_REPLY_TEXT.lower() in c['text'].lower()]
            if partial:
                print('FAIL: Component 1 — Partial text match found but not exact. Found: %r' % partial[0]['text'])
            else:
                print('FAIL: Component 1 — No comment with required reply text found.')
                print('  Expected: %r' % REQUIRED_REPLY_TEXT)
                print('  Available texts: %s' % [c['text'] for c in comment_list])
            reply_entry = None
    except Exception as e:
        print('ERROR: Component 1 — %s' % e)
        reply_entry = None

    # ------------------------------------------------------------------
    # Component 2: The reply is threaded correctly via commentsExtended.xml (0.3 pts)
    # w15:commentEx with w15:paraIdParent referencing the original comment's paraId.
    # Fails on initial (no commentsExtended.xml). Passes on golden.
    # ------------------------------------------------------------------
    try:
        if comments_extended_xml_content is None:
            print('FAIL: Component 2 — No commentsExtended.xml found (reply not threaded as reply)')
        else:
            ext_root = etree.fromstring(comments_extended_xml_content)
            w15_ns_map = {'w15': W15_NS}
            comment_ex_elems = ext_root.findall('w15:commentEx', w15_ns_map)
            print('commentsExtended entries: %d' % len(comment_ex_elems))

            # Find original comment's paraId
            original_entries = [c for c in comment_list if c['text'] == ORIGINAL_COMMENT_TEXT]
            if not original_entries:
                print('FAIL: Component 2 — Original comment not found; cannot verify threading')
            else:
                original_para_id = original_entries[0]['paraId']

                # Find commentsExtended entry with paraIdParent == original_para_id
                threading_entries = [
                    ex for ex in comment_ex_elems
                    if ex.get('{%s}paraIdParent' % W15_NS) == original_para_id
                ]

                if len(threading_entries) >= 1:
                    # Also verify the reply paraId matches
                    threading_para_id = threading_entries[0].get('{%s}paraId' % W15_NS)
                    reply_para_id = reply_entry['paraId'] if reply_entry else None

                    if reply_para_id is not None and threading_para_id == reply_para_id:
                        print('PASS: Component 2 — Reply properly threaded under original (paraIdParent=%s) (0.3 pts)' % original_para_id)
                        total_score += 0.3
                    elif reply_para_id is None:
                        # Reply found but no paraId to verify; threading entry exists with correct parent
                        print('PASS: Component 2 — Threading entry with correct parent found (0.3 pts)')
                        total_score += 0.3
                    else:
                        print('FAIL: Component 2 — Threading entry paraId=%s does not match reply paraId=%s' % (
                            threading_para_id, reply_para_id))
                else:
                    print('FAIL: Component 2 — No commentsExtended entry with paraIdParent=%s found' % original_para_id)
    except Exception as e:
        print('ERROR: Component 2 — %s' % e)

    # ------------------------------------------------------------------
    # Component 3: Original comment text remains unchanged (0.2 pts)
    # Gated on Component 1: only awarded when a reply was successfully added.
    # This prevents Component 3 from scoring points on the initial_env
    # (where the original comment exists but no reply has been added yet).
    # ------------------------------------------------------------------
    try:
        if total_score < 0.5:
            # Gate: C3 only fires if C1 passed (reply exists)
            print('SKIP: Component 3 — gated on C1 (no reply found)')
        else:
            original_preserved = any(c['text'] == ORIGINAL_COMMENT_TEXT for c in comment_list)
            if original_preserved:
                print('PASS: Component 3 — Original comment text preserved unchanged (0.2 pts)')
                total_score += 0.2
            else:
                print('FAIL: Component 3 — Original comment text not found or modified.')
                print('  Expected: %r' % ORIGINAL_COMMENT_TEXT)
    except Exception as e:
        print('ERROR: Component 3 — %s' % e)

    final_score = min(total_score, 1.0)
    print('\nScore: %.1f/1.0' % total_score)
    print('REWARD: %.1f' % final_score)
    return final_score


verify_task(FILE_PATH)
