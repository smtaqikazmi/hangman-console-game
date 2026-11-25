# Hangman Word Guessing Game (Console)

An interactive, modular terminal-based Hangman word guessing game built in Python 3 using string manipulation, control flow, input validation, and 6-stage ASCII gallows art.

## Features
- **Word List Loading:** Reads words from `google-10000-english-no-swears.txt`, filters valid alphabetic words by length, and falls back to a built-in word list if the file is not found.
- **Random Word Selection:** Selects a secret word each round using Python's `random.choice()`.
- **Masked Word & Guess Tracking:** Displays revealed letters and underscores (for example, `_ A _ H E O N`), tracks guessed and wrong letters, and avoids penalty deductions on duplicate or invalid inputs.
- **ASCII Gallows & Replay Loop:** Updates the gallows across 6 allowed mistakes and shows victory or defeat summaries with replay (`y`/`n`) support.

## Project Structure
hangman_project/
├── hangman.py
├── google-10000-english-no-swears.txt
├── .gitignore
└── README.md

## How to Run
1. Open the `hangman_project` folder in VS Code or a terminal.
2. Make sure Python 3 is installed and `google-10000-english-no-swears.txt` is in the same folder as `hangman.py`.
3. Run:
   ```bash
   python hangman.py