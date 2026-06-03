"""
Reward Script: Gitolite server setup verification
Task ID: os_gf5_028
Domain: OS (system administration)
Scoring:
  - Component 1: Gitolite binary installed (0.15 pts)
  - Component 2: Gitolite initialized with .gitolite dir and .gitolite.rc (0.20 pts)
  - Component 3: company-config.git repository exists (0.20 pts)
  - Component 4: gitolite.conf defines company-config with correct permissions (0.25 pts)
  - Component 5: Admin key (id_rsa.pub) in keydir + authorized_keys has gitolite entries (0.20 pts)
"""

import os
import re

WORKDIR = '/home/user'

def verify_task():
    """
    Verify Gitolite server setup with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Gitolite binary is installed (0.15 points)
    try:
        gitolite_path = '/usr/bin/gitolite'
        if os.path.isfile(gitolite_path) and os.access(gitolite_path, os.X_OK):
            print(f"PASS: Component 1 — Gitolite binary found at {gitolite_path} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Gitolite binary not found or not executable at {gitolite_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Gitolite initialized — .gitolite dir with conf/keydir subdirs + .gitolite.rc (0.20 points)
    try:
        gitolite_dir = os.path.join(WORKDIR, '.gitolite')
        gitolite_rc = os.path.join(WORKDIR, '.gitolite.rc')
        conf_dir = os.path.join(gitolite_dir, 'conf')
        keydir_dir = os.path.join(gitolite_dir, 'keydir')

        checks_passed = 0
        if os.path.isdir(gitolite_dir):
            checks_passed += 1
        else:
            print(f"  DETAIL: .gitolite directory missing")
        if os.path.isfile(gitolite_rc):
            checks_passed += 1
        else:
            print(f"  DETAIL: .gitolite.rc missing")
        if os.path.isdir(conf_dir):
            checks_passed += 1
        else:
            print(f"  DETAIL: .gitolite/conf directory missing")
        if os.path.isdir(keydir_dir):
            checks_passed += 1
        else:
            print(f"  DETAIL: .gitolite/keydir directory missing")

        if checks_passed == 4:
            print(f"PASS: Component 2 — Gitolite initialized (all 4 checks: .gitolite, .gitolite.rc, conf, keydir) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Gitolite initialization incomplete ({checks_passed}/4 checks passed)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: company-config.git repository exists in ~/repositories/ (0.20 points)
    try:
        repo_path = os.path.join(WORKDIR, 'repositories', 'company-config.git')
        head_file = os.path.join(repo_path, 'HEAD')

        if os.path.isdir(repo_path) and os.path.isfile(head_file):
            # Verify it's a valid bare git repo by checking HEAD content
            with open(head_file, 'r') as f:
                head_content = f.read().strip()
            if head_content.startswith('ref:'):
                print(f"PASS: Component 3 — company-config.git exists as valid bare repo (HEAD: {head_content}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — company-config.git HEAD has unexpected content: {head_content}")
        else:
            print(f"FAIL: Component 3 — company-config.git not found at {repo_path}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: gitolite.conf defines company-config repo with correct permissions (0.25 points)
    # alice has RW, bob has R
    try:
        conf_path = os.path.join(WORKDIR, '.gitolite', 'conf', 'gitolite.conf')
        if not os.path.isfile(conf_path):
            print(f"FAIL: Component 4 — gitolite.conf not found at {conf_path}")
        else:
            with open(conf_path, 'r') as f:
                conf_content = f.read()

            # Check for company-config repo definition
            has_repo_def = bool(re.search(r'repo\s+company-config', conf_content))
            # Check alice has RW (but not necessarily RW+)
            has_alice_rw = bool(re.search(r'RW\s.*=\s*.*alice', conf_content))
            # Check bob has R (read-only, not RW)
            has_bob_r = bool(re.search(r'^\s*R\s+.*=\s*.*bob', conf_content, re.MULTILINE))

            sub_score = 0.0
            if has_repo_def:
                sub_score += 0.05
                print(f"  DETAIL: company-config repo defined in conf ✓")
            else:
                print(f"  DETAIL: company-config repo NOT defined in conf")

            if has_alice_rw:
                sub_score += 0.10
                print(f"  DETAIL: alice has RW permission ✓")
            else:
                print(f"  DETAIL: alice does NOT have RW permission")

            if has_bob_r:
                sub_score += 0.10
                print(f"  DETAIL: bob has R (read-only) permission ✓")
            else:
                print(f"  DETAIL: bob does NOT have R permission")

            if sub_score >= 0.25:
                print(f"PASS: Component 4 — gitolite.conf has correct company-config permissions (0.25 pts)")
                total_score += sub_score
            elif sub_score > 0:
                print(f"PARTIAL: Component 4 — gitolite.conf partially correct ({sub_score}/0.25 pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 4 — gitolite.conf checks all failed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Admin key configured — id_rsa.pub in keydir + authorized_keys has gitolite entries (0.20 points)
    try:
        keydir_path = os.path.join(WORKDIR, '.gitolite', 'keydir')
        auth_keys_path = os.path.join(WORKDIR, '.ssh', 'authorized_keys')

        sub_score = 0.0

        # Check id_rsa.pub exists in keydir
        if os.path.isdir(keydir_path):
            keydir_files = os.listdir(keydir_path)
            if 'id_rsa.pub' in keydir_files:
                sub_score += 0.05
                print(f"  DETAIL: id_rsa.pub found in keydir ✓")
            else:
                print(f"  DETAIL: id_rsa.pub NOT in keydir (found: {keydir_files})")
        else:
            print(f"  DETAIL: keydir does not exist")

        # Check authorized_keys has gitolite-shell entries
        if os.path.isfile(auth_keys_path):
            with open(auth_keys_path, 'r') as f:
                auth_content = f.read()

            has_gitolite_marker = '# gitolite start' in auth_content
            has_alice_entry = 'gitolite-shell alice' in auth_content
            has_bob_entry = 'gitolite-shell bob' in auth_content

            if has_gitolite_marker:
                sub_score += 0.05
                print(f"  DETAIL: authorized_keys has gitolite markers ✓")
            else:
                print(f"  DETAIL: authorized_keys missing gitolite markers")

            if has_alice_entry:
                sub_score += 0.05
                print(f"  DETAIL: authorized_keys has alice gitolite entry ✓")
            else:
                print(f"  DETAIL: authorized_keys missing alice entry")

            if has_bob_entry:
                sub_score += 0.05
                print(f"  DETAIL: authorized_keys has bob gitolite entry ✓")
            else:
                print(f"  DETAIL: authorized_keys missing bob entry")
        else:
            print(f"  DETAIL: authorized_keys not found")

        if sub_score >= 0.20:
            print(f"PASS: Component 5 — Admin key and SSH config correct (0.20 pts)")
            total_score += sub_score
        elif sub_score > 0:
            print(f"PARTIAL: Component 5 — SSH/key config partially correct ({sub_score}/0.20 pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 5 — SSH/key config not set up")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid floating point artifacts
    final_score = round(final_score, 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
