import random
from pathlib import Path

MAX_MISTAKES = 6
WORD_LIST_FILE = "google-10000-english-no-swears.txt"

FALLBACK_WORDS = [
    "python",
    "algorithm",
    "variable",
    "function",
    "iteration",
    "dictionary",
    "boolean",
    "terminal",
]

STAGES = [
    # 0 mistakes
    """
  +---+
  |   |
      |
      |
      |
      |
=========
""",
    # 1 mistake (head)
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========
""",
    # 2 mistakes (torso)
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
""",
    # 3 mistakes (one arm)
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
""",
    # 4 mistakes (both arms)
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
""",
    # 5 mistakes (one leg)
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========
""",
    # 6 mistakes (both legs - game over)
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========
""",
]


def load_words(filepath: str = WORD_LIST_FILE, min_len: int = 4, max_len: int = 12) -> list[str]:
    """Load clean words from the text file, or use fallback words if file is missing."""
    path = Path(filepath)
    if path.is_file():
        words: list[str] = []
        seen: set[str] = set()
        for line in path.read_text(encoding="utf-8").splitlines():
            word = line.strip().lower()
            if word.isalpha() and min_len <= len(word) <= max_len and word not in seen:
                seen.add(word)
                words.append(word)
        if words:
            return words
    return FALLBACK_WORDS


def choose_word(words: list[str]) -> str:
    """Select a random secret word from the list."""
    return random.choice(words)


def format_masked_word(secret_word: str, guessed_letters: set[str]) -> str:
    """Return spaced underscores and revealed letters, e.g. '_ A _ H E O N'."""
    return " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in secret_word
    )


def get_valid_guess(all_guessed: set[str]) -> str:
    """Prompt until a single unused alphabetic letter is entered."""
    while True:
        raw = input("Enter a single letter: ").strip().lower()
        if len(raw) != 1 or not raw.isalpha():
            print("Invalid input. Please enter a single alphabetic letter (A-Z).")
            continue
        if raw in all_guessed:
            print(f"You already guessed '{raw.upper()}'. No penalty - try another letter.")
            continue
        return raw


def render_board(
    secret_word: str,
    correct_letters: set[str],
    wrong_letters: set[str],
    mistakes: int,
) -> None:
    """Display the ASCII gallows art, masked word, and guessed letter history."""
    print(STAGES[mistakes])
    print(f"Word: {format_masked_word(secret_word, correct_letters)}")
    print(f"Mistakes: {mistakes} / {MAX_MISTAKES}")
    guessed_sorted = ", ".join(sorted(ch.upper() for ch in (correct_letters | wrong_letters)))
    wrong_sorted = ", ".join(sorted(ch.upper() for ch in wrong_letters))
    print(f"Guessed letters: {guessed_sorted if guessed_sorted else 'None'}")
    print(f"Wrong guesses: {wrong_sorted if wrong_sorted else 'None'}")
    print("-" * 40)


def show_outcome(won: bool, secret_word: str, mistakes: int) -> None:
    """Display clean victory or defeat screen."""
    print("\n" + "=" * 40)
    if won:
        print("VICTORY! You guessed the secret word!")
    else:
        print(STAGES[MAX_MISTAKES])
        print("DEFEAT! You have reached 6 mistakes.")
    print(f"Secret word : {secret_word.upper()}")
    print(f"Mistakes    : {mistakes} / {MAX_MISTAKES}")
    print("=" * 40 + "\n")


def play_round(words: list[str]) -> None:
    """Play a single round of Hangman."""
    secret_word = choose_word(words)
    target_letters = set(secret_word)
    correct_letters: set[str] = set()
    wrong_letters: set[str] = set()
    mistakes = 0

    print("\n=== HANGMAN ===")
    while mistakes < MAX_MISTAKES:
        render_board(secret_word, correct_letters, wrong_letters, mistakes)
        guess = get_valid_guess(correct_letters | wrong_letters)

        if guess in target_letters:
            correct_letters.add(guess)
            print(f"Good guess! '{guess.upper()}' is in the word.")
            if target_letters.issubset(correct_letters):
                show_outcome(True, secret_word, mistakes)
                return
        else:
            wrong_letters.add(guess)
            mistakes += 1
            print(f"Sorry, '{guess.upper()}' is not in the word.")

    show_outcome(False, secret_word, mistakes)


def main() -> None:
    """Load the word list and run the game with replay support."""
    words = load_words()
    while True:
        play_round(words)
        again = input("Do you want to play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Thanks for playing Hangman!")
            break


if __name__ == "__main__":
    main()