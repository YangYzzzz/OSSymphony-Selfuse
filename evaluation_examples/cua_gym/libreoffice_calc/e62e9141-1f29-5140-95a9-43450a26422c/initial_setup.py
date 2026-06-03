"""
Initial Setup: Python card game (War) with a broken shuffle bug
Task ID: osworld_multi_apps_vscode_debug_game_009
Domain: vscode (multi_apps)
Description:
    Creates a War card game project at /home/user/Desktop/war_game/.
    The deck.py has a shuffle bug: it does NOT actually randomize the deck
    (calls sorted() instead of random.shuffle), so every game starts with
    the same card order.  VSCode is opened with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Desktop/war_game'

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f'  created: {path}')


def launch_gui(command: str, delay_sec: float = 1.5):
    """Launch a GUI application on DISPLAY=:0 without blocking."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


# ---------------------------------------------------------------------------
# card.py
# ---------------------------------------------------------------------------

CARD_PY = '''\
"""card.py — A single playing card."""


class Card:
    SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    RANK_VALUES = {r: i for i, r in enumerate(RANKS, start=2)}

    def __init__(self, suit: str, rank: str):
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit: {suit!r}")
        if rank not in self.RANKS:
            raise ValueError(f"Invalid rank: {rank!r}")
        self.suit = suit
        self.rank = rank
        self.value = self.RANK_VALUES[rank]

    def __repr__(self) -> str:
        return f"{self.rank} of {self.suit}"

    def __lt__(self, other: "Card") -> bool:
        return self.value < other.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.value == other.value
'''

# ---------------------------------------------------------------------------
# deck.py  — BUGGY VERSION (shuffle doesn\'t randomize; uses sorted instead)
# ---------------------------------------------------------------------------

DECK_PY = '''\
"""deck.py — A standard 52-card deck.

BUG: The shuffle() method calls sorted() (deterministic ascending order)
instead of random.shuffle(), so every game starts with the exact same
card order.  Find and fix this bug.
"""

import random
from card import Card


class Deck:
    def __init__(self):
        self.cards = [
            Card(suit, rank)
            for suit in Card.SUITS
            for rank in Card.RANKS
        ]

    def shuffle(self):
        # BUG: This sorts the deck instead of shuffling it randomly.
        # Every game will start with cards in the same ascending order.
        self.cards = sorted(self.cards)

    def deal(self, num_players: int = 2):
        """Deal all cards evenly to num_players hands (list of lists)."""
        hands = [[] for _ in range(num_players)]
        for i, card in enumerate(self.cards):
            hands[i % num_players].append(card)
        return hands

    def __len__(self) -> int:
        return len(self.cards)

    def __repr__(self) -> str:
        return f"Deck({len(self.cards)} cards)"
'''

# ---------------------------------------------------------------------------
# player.py
# ---------------------------------------------------------------------------

PLAYER_PY = '''\
"""player.py — A player in the War card game."""

from typing import List
from card import Card


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []

    def receive_cards(self, cards: List[Card]):
        """Add cards to the bottom of the player\'s hand."""
        self.hand.extend(cards)

    def draw(self) -> Card:
        """Draw (remove and return) the top card from the hand."""
        if not self.hand:
            raise IndexError(f"{self.name} has no cards to draw.")
        return self.hand.pop(0)

    def battle(self, other: "Player"):
        """
        Play one battle round.

        Each player draws one card. The player with the higher-value card
        wins both cards (winner gains cards at bottom of hand).

        Returns:
            (winner_name, my_card, their_card) — winner_name is None on tie.
        """
        my_card = self.draw()
        their_card = other.draw()

        if my_card > their_card:
            self.receive_cards([my_card, their_card])
            return (self.name, my_card, their_card)
        elif their_card > my_card:
            other.receive_cards([my_card, their_card])
            return (other.name, my_card, their_card)
        else:
            # Tie — each player keeps their own card
            self.receive_cards([my_card])
            other.receive_cards([their_card])
            return (None, my_card, their_card)

    def card_count(self) -> int:
        return len(self.hand)

    def __repr__(self) -> str:
        return f"Player({self.name!r}, {self.card_count()} cards)"
'''

# ---------------------------------------------------------------------------
# main.py
# ---------------------------------------------------------------------------

MAIN_PY = '''\
"""main.py — Entry point for the War card game."""

from deck import Deck
from player import Player


def play_game(max_rounds: int = 1000) -> str:
    """Play a full game of War.  Returns the winner\'s name (or \'Draw\')."""
    deck = Deck()
    deck.shuffle()  # <-- relies on shuffle being truly random

    alice = Player("Alice")
    bob = Player("Bob")

    alice_hand, bob_hand = deck.deal(num_players=2)
    alice.receive_cards(alice_hand)
    bob.receive_cards(bob_hand)

    rounds = 0
    while alice.card_count() > 0 and bob.card_count() > 0 and rounds < max_rounds:
        winner_name, ac, bc = alice.battle(bob)
        rounds += 1

    if alice.card_count() > bob.card_count():
        return "Alice"
    elif bob.card_count() > alice.card_count():
        return "Bob"
    else:
        return "Draw"


if __name__ == "__main__":
    winner = play_game()
    print(f"Game over! Winner: {winner}")
'''

# ---------------------------------------------------------------------------
# test_war.py  — unit tests (agent should make these pass)
# ---------------------------------------------------------------------------

TEST_WAR_PY = '''\
"""test_war.py — Unit tests for the War card game.

Tests:
  1. shuffle_is_random  — deck order differs between shuffles
  2. draw_logic         — drawing reduces hand count correctly
  3. battle_logic       — higher card wins; tie handled correctly
"""

import sys
import os
import unittest

# Make sure the project directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from card import Card
from deck import Deck
from player import Player


class TestShuffleIsRandom(unittest.TestCase):
    def test_two_shuffles_differ(self):
        """After two independent shuffles the order should differ (very high probability)."""
        d1 = Deck()
        d1.shuffle()
        order1 = [str(c) for c in d1.cards]

        d2 = Deck()
        d2.shuffle()
        order2 = [str(c) for c in d2.cards]

        # The probability of two random 52-card shuffles being identical is ~1/52! ≈ 0
        # If the shuffle is deterministic (sorted), both orders will be identical.
        self.assertNotEqual(
            order1,
            order2,
            "Two shuffled decks should have different orders (shuffle is not random).",
        )

    def test_shuffle_preserves_cards(self):
        """Shuffling should not add or remove cards."""
        d = Deck()
        d.shuffle()
        self.assertEqual(len(d), 52)
        self.assertEqual(len(set(str(c) for c in d.cards)), 52)


class TestDrawLogic(unittest.TestCase):
    def test_draw_reduces_count(self):
        deck = Deck()
        p = Player("Tester")
        p.receive_cards(deck.cards[:10])
        self.assertEqual(p.card_count(), 10)
        p.draw()
        self.assertEqual(p.card_count(), 9)

    def test_draw_empty_raises(self):
        p = Player("Empty")
        with self.assertRaises(IndexError):
            p.draw()


class TestBattleLogic(unittest.TestCase):
    def _make_player_with_card(self, name: str, rank: str, suit: str = "Spades") -> Player:
        p = Player(name)
        p.receive_cards([Card(suit, rank)])
        return p

    def test_higher_card_wins(self):
        alice = self._make_player_with_card("Alice", "K")
        bob = self._make_player_with_card("Bob", "2")
        winner_name, ac, bc = alice.battle(bob)
        self.assertEqual(winner_name, "Alice")
        self.assertEqual(alice.card_count(), 2)
        self.assertEqual(bob.card_count(), 0)

    def test_lower_card_loses(self):
        alice = self._make_player_with_card("Alice", "3")
        bob = self._make_player_with_card("Bob", "A")
        winner_name, ac, bc = alice.battle(bob)
        self.assertEqual(winner_name, "Bob")
        self.assertEqual(bob.card_count(), 2)
        self.assertEqual(alice.card_count(), 0)

    def test_tie_each_keeps_card(self):
        alice = self._make_player_with_card("Alice", "7")
        bob = self._make_player_with_card("Bob", "7")
        winner_name, ac, bc = alice.battle(bob)
        self.assertIsNone(winner_name)
        self.assertEqual(alice.card_count(), 1)
        self.assertEqual(bob.card_count(), 1)


if __name__ == "__main__":
    unittest.main()
'''

# ---------------------------------------------------------------------------
# Create all files
# ---------------------------------------------------------------------------

def create_initial():
    print(f'Creating project at {WORKDIR} ...')
    write_file(os.path.join(WORKDIR, 'card.py'), CARD_PY)
    write_file(os.path.join(WORKDIR, 'deck.py'), DECK_PY)
    write_file(os.path.join(WORKDIR, 'player.py'), PLAYER_PY)
    write_file(os.path.join(WORKDIR, 'main.py'), MAIN_PY)
    write_file(os.path.join(WORKDIR, 'test_war.py'), TEST_WAR_PY)
    print('All project files created.')

    # Open VSCode with the project folder
    launch_gui(f'code "{WORKDIR}"', delay_sec=3.0)
    print('GUI_READY: VSCode launched with war_game project on DISPLAY=:0')


create_initial()
