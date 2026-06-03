"""
Reward Script: Cypress Component Testing Configuration for Vue 3 Project
Task ID: vscode_gf3_064
Domain: vscode
Scoring:
  C1 (0.30) — cypress.config.ts exists with component testing, Vue framework, webpack bundler
  C2 (0.15) — ProductCard.cy.ts exists and imports ProductCard component
  C3 (0.15) — ProductCard.cy.ts uses cy.mount() to render the component
  C4 (0.15) — ProductCard.cy.ts asserts price with currency formatting ($)
  C5 (0.25) — ProductCard.cy.ts tests Add to Cart event emission (cy.spy)
"""

import os
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'vue-app')
CONFIG_PATH = os.path.join(PROJECT, 'cypress.config.ts')
TEST_PATH = os.path.join(PROJECT, 'cypress', 'component', 'ProductCard.cy.ts')


def verify_task():
    total_score = 0.0

    # ── Component 1: cypress.config.ts with Vue + webpack component testing (0.30) ──
    try:
        if not os.path.isfile(CONFIG_PATH):
            print(f"FAIL: Component 1 — cypress.config.ts not found at {CONFIG_PATH}")
        else:
            with open(CONFIG_PATH, 'r') as f:
                cfg = f.read()

            has_component = bool(re.search(r'component\s*:', cfg))
            has_vue = bool(re.search(r"framework\s*:\s*['\"]vue['\"]", cfg))
            has_webpack = bool(re.search(r"bundler\s*:\s*['\"]webpack['\"]", cfg))

            sub = 0.0
            if has_component:
                sub += 0.10
            if has_vue:
                sub += 0.10
            if has_webpack:
                sub += 0.10

            if sub >= 0.30:
                print(f"PASS: Component 1 — cypress.config.ts has component testing with Vue/webpack ({sub} pts)")
            else:
                missing = []
                if not has_component:
                    missing.append("component section")
                if not has_vue:
                    missing.append("framework:'vue'")
                if not has_webpack:
                    missing.append("bundler:'webpack'")
                print(f"PARTIAL: Component 1 — missing: {', '.join(missing)} ({sub} pts)")
            if sub > 0:
                total_score += sub
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ── Component 2: ProductCard.cy.ts exists and imports ProductCard (0.15) ──
    try:
        if not os.path.isfile(TEST_PATH):
            print(f"FAIL: Component 2 — {TEST_PATH} not found")
        else:
            with open(TEST_PATH, 'r') as f:
                test_content = f.read()
            # Check for import of ProductCard component
            if re.search(r"import\s+.*ProductCard", test_content):
                print(f"PASS: Component 2 — ProductCard.cy.ts imports ProductCard (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — no import of ProductCard found in test file")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ── Component 3: Uses cy.mount() to render component (0.15) ──
    try:
        if not os.path.isfile(TEST_PATH):
            print(f"FAIL: Component 3 — test file not found")
        else:
            with open(TEST_PATH, 'r') as f:
                test_content = f.read()
            # cy.mount(ProductCard, ...) pattern
            if re.search(r'cy\.mount\s*\(\s*ProductCard', test_content):
                print(f"PASS: Component 3 — cy.mount(ProductCard) found (0.15 pts)")
                total_score += 0.15
            elif re.search(r'cy\.mount\s*\(', test_content):
                # cy.mount exists but not with ProductCard directly — partial
                print(f"PARTIAL: Component 3 — cy.mount() found but not with ProductCard (0.08 pts)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 3 — no cy.mount() call found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ── Component 4: Asserts price with currency formatting (0.15) ──
    try:
        if not os.path.isfile(TEST_PATH):
            print(f"FAIL: Component 4 — test file not found")
        else:
            with open(TEST_PATH, 'r') as f:
                test_content = f.read()
            # Look for assertion on price with $ sign (currency formatting)
            has_price_assert = bool(re.search(r"should\s*\(\s*['\"]contain['\"].*\\\$[\d]", test_content)) or \
                               bool(re.search(r"contain.*\$\d+\.\d{2}", test_content))
            if has_price_assert:
                print(f"PASS: Component 4 — price currency formatting assertion found (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — no price currency formatting assertion found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ── Component 5: Tests Add to Cart event emission with cy.spy (0.25) ──
    try:
        if not os.path.isfile(TEST_PATH):
            print(f"FAIL: Component 5 — test file not found")
        else:
            with open(TEST_PATH, 'r') as f:
                test_content = f.read()

            has_spy = bool(re.search(r'cy\.spy\s*\(', test_content))
            has_add_to_cart = bool(re.search(r'add.to.cart', test_content, re.IGNORECASE))
            has_called_assert = bool(re.search(r"calledOnce|calledWith|have\.been\.called", test_content))

            sub = 0.0
            if has_spy and has_add_to_cart and has_called_assert:
                sub = 0.25
                print(f"PASS: Component 5 — cy.spy + Add to Cart event + assertion found (0.25 pts)")
            elif has_add_to_cart and has_called_assert:
                sub = 0.15
                print(f"PARTIAL: Component 5 — Add to Cart event test found but no cy.spy ({sub} pts)")
            elif has_add_to_cart:
                sub = 0.08
                print(f"PARTIAL: Component 5 — Add to Cart reference found but incomplete test ({sub} pts)")
            else:
                print(f"FAIL: Component 5 — no Add to Cart event test found")
            if sub > 0:
                total_score += sub
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
