# Secure CLI Number Guessing Game

An object-oriented Command-Line Interface (CLI) Number Guessing Game built in Python. This project demonstrates modular classes, JSON persistence, hashed user authentication, error resilience, argparse commands, and automated testing using pytest.

---

## Project Overview
[text](https://www.youtube.com/watch?v=D2XtN7qDMEY) - short version
[text](https://www.youtube.com/watch?v=D2XtN7qDMEY) - long version (youtube is yet to render this video)

## Key Developer Skill Sets Demonstrated

### 1. Clean Architecture & Object-Oriented Design (OOP)
The project follows a strict separation of concerns, avoiding bloated modules. It is structured logically into reusable components:
*   **Controller (`CLIApp`):** Manages the interactive menu, user input loops, and login state.
*   **Domain Models (`Game`, `User`):** Contain pure business logic (attempts calculations, score algorithms, and game initialization).
*   **Infrastructure/Managers (`UserManager`, `ScoreManager`):** Interface with external files, managing data serialization, persistence, sorting, and user records.
*   **Utilities (`utils`):** Share validation, menu display, and JSON storage helpers across the app.

### 2. Cryptographic Security Best Practices
*   **Password Hashing:** User passwords are never stored in plaintext. The project implements SHA-256 hashing using Python's `hashlib` to securely hash and verify credentials upon registration and login.
*   **State Isolation:** Ensures session safety by maintaining login states (`self.current_user`) only for authenticated execution periods.

### 3. Resilience and Error Handling
*   **Input Validation:** Graces user typos (e.g., entering letters instead of integers when guessing a number) by trapping `ValueError` and prompting the user to try again rather than crashing the system.
*   **Fault-Tolerant Persistence:** Mitigates corruption of JSON files (e.g., empty or malformed database files) by implementing custom exception recovery (`json.JSONDecodeError`), falling back safely to empty datasets.
*   **Directory Creation:** Creates parent folders for JSON files when saving to a new path.

### 4. Quality Assurance and Testing (CI/CD Ready)
*   Equipped with a focused unit-testing suite using `pytest` to validate core components like:
    *   Authentication and session state management.
    *   Game state initialization and mathematical score decay.
    *   Leaderboard sorting and multi-score tracking.
*   Utilizes `tmp_path` fixture for environment-isolated database state testing, preventing production filesystem pollution.

### 5. Professional Dependency Management
*   Uses `Pipenv` to manage virtual environment isolation, package locking, and dev dependencies (`Pipfile` & `Pipfile.lock`).

---

## Project Structure

```text
cli_app/
│
├── data/                       # Local JSON database storage
│   ├── scores.json             # Persistent high score records
│   └── users.json              # Persistent hashed user profiles
│
├── models/                     # Application domain logic
│   ├── cli_app.py              # Main CLI application flow controller
│   ├── game.py                 # Core game state & scoring calculations
│   ├── login.py                # User registration & SHA-256 authentication
│   └── score_manager.py        # Leaderboard storage, saving, & display
│
├── utils/                      # Helper modules and scripts
│   ├── cli.py                  # Shared interactive menu display
│   ├── helpers.py              # Username and email validation helpers
│   └── storage.py              # JSON load/save helpers
│
├── tests/                      # Automated test suite
│   └── test_game.py            # Unit tests for user, game, and score components
│
├── main.py                     # Entry point of the application
├── Pipfile                     # Virtual environment dependencies
├── Pipfile.lock                # Locked exact versions for reproducibility
└── README.md                   # Project documentation
```

---

## Getting Started

### Prerequisites
*   Python 3.10+
*   Pipenv (`pip install pipenv` if not installed)

### Setup & Installation

1.  **Clone the repository and navigate into it:**
    ```bash
    git clone https://github.com/yeswadams/python_cli_app.git
    cd cli_app
    ```

2.  **Install dependencies with requirements.txt:**
    ```bash
    pip install -r requirements.txt
    ```

    Or initialize the Pipenv environment:
    ```bash
    pipenv install --dev
    ```

3.  **Activate the Pipenv virtual environment shell if using Pipenv:**
    ```bash
    pipenv shell
    ```

---

## Usage

To launch the interactive CLI application:
```bash
pipenv run python main.py
```

To use argparse subcommands:
```bash
pipenv run python main.py --help
pipenv run python main.py register --username Alice --email alice@example.com --password password123
pipenv run python main.py login --email alice@example.com --password password123
pipenv run python main.py scores
pipenv run python main.py play --username Alice
```

### Flow Options:
1.  **Register:** Enter username, email, and password (hashed with SHA-256 and saved to `data/users.json`).
2.  **Login:** Enter registered credentials to verify details and begin an authenticated session.
3.  **Play Game:** Only accessible once logged in. Guess a random number between 1 and 100 with dynamic tips ("Too High" / "Too Low"). Scores are calculated based on attempts (100 base score, -10 points per extra attempt). Winning scores are saved to `data/scores.json`.
4.  **View High Scores:** Lists the top 10 historical high scores sorted in descending order.
5.  **Exit:** Gracefully shuts down the terminal runner.

---

## Testing

The test suite validates both success paths and edge cases, such as incorrect password checking, malformed JSON files, folder creation during persistence, validation helpers, sorted high scores, and invalid guesses.

To run all unit tests:
```bash
python -m pytest
```

With Pipenv:
```bash
pipenv run python -m pytest
```

### Test Coverage Highlights:
*   `test_game_initialization`: Verifies random number generation, player naming, and defaults.
*   `test_check_guess_too_low`: Mocks low guesses and asserts correct console warning feedback.
*   `test_check_guess_correct`: Asserts true conditions on a matching guess.
*   `test_calculate_score`: Checks attempts-to-score decay calculations.
*   `test_add_and_display_scores`: Tests file system saving and sorting.
*   `test_register_and_login_user`: Validates hash generation and user login verification.
