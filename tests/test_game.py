# tests
import pytest
from models.game import BaseGame, Game
from models.score_manager import ScoreManager
from models.login import Account, User, UserManager
from main import main
from utils.helpers import is_valid_email, is_valid_username
from utils.storage import load_json_list, save_json_list

# ---Game Test ---
def test_game_initialization():
    game = Game("TestPlayer")
    assert isinstance(game, BaseGame)
    assert game.player_name == "TestPlayer"
    assert 1 <= game.secret_number <= 100
    assert game.attempts == 0
    assert game.max_attempts == 10

def test_game_attempt_tracking():
    game = Game("Tester", max_attempts=1)
    assert game.has_attempts_remaining() is True
    game.secret_number = 99
    game.check_guess(1)
    assert game.has_attempts_remaining() is False

def test_check_guess_too_low(capsys):
    game = Game("Tester")   
    game.secret_number = 50
    result = game.check_guess(30)
    captured = capsys.readouterr()
    assert "Too low" in captured.out
    assert result is False

def test_check_guess_correct(capsys):
    game = Game("Tester")
    game.secret_number = 42
    result = game.check_guess(42)
    capture = capsys.readouterr()
    assert "Correct!" in capture.out
    assert result is True

def test_calculate_score():
    game = Game("Tester")
    game.secret_number = 10 
    game.attempts = 3
    score = game.calculate_score() 
    assert score == max(0, 100  -(3 - 1) * 10)

def test_add_and_display_scores(tmp_path, capsys):
    score_file = tmp_path / "score.json"
    manager = ScoreManager(scores_file=str(score_file))    
    manager.add_score("Alice", 90)
    manager.add_score("Bob", 80)
    manager.display_scores()
    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "Bob" in captured.out

def test_scores_are_sorted_and_limited(tmp_path):
    score_file = tmp_path / "score.json"
    manager = ScoreManager(scores_file=str(score_file), max_scores=2)
    manager.add_score("Alice", 40)
    manager.add_score("Bob", 90)
    manager.add_score("Casey", 60)
    assert manager.scores == [
        {"name": "Bob", "score": 90},
        {"name": "Casey", "score": 60},
    ]

def test_register_and_login_user(tmp_path):
    user_file = tmp_path / "users.json" 
    manager = UserManager(users_file=str(user_file))
    user = manager.register_user("Alice", "alice@example.com", "password123")
    assert user is not None
    assert isinstance(user, Account)
    assert isinstance(user, User)
    logged_in = manager.login_user("alice@example.com", "password123")
    assert logged_in is not None
    assert logged_in.username == "Alice"

def test_duplicate_email_is_rejected(tmp_path):
    user_file = tmp_path / "users.json"
    manager = UserManager(users_file=str(user_file))
    assert manager.register_user("Alice", "alice@example.com", "password123") is not None
    assert manager.register_user("Alicia", "alice@example.com", "newpass") is None
    assert len(manager.users) == 1

def test_invalid_login_returns_none(tmp_path):
    user_file = tmp_path / "users.json"
    manager = UserManager(users_file=str(user_file))
    manager.register_user("Alice", "alice@example.com", "password123")
    assert manager.login_user("alice@example.com", "wrong-password") is None

def test_json_loader_recovers_from_bad_file(tmp_path):
    data_file = tmp_path / "broken.json"
    data_file.write_text("{bad json")
    assert load_json_list(str(data_file)) == []

def test_json_save_creates_parent_directory(tmp_path):
    data_file = tmp_path / "nested" / "users.json"
    save_json_list(str(data_file), [{"username": "Alice"}])
    assert load_json_list(str(data_file)) == [{"username": "Alice"}]

@pytest.mark.parametrize(
    ("username", "expected"),
    [
        ("Alice123", True),
        ("Alice Smith", False),
        ("", False),
    ],
)
def test_username_validation(username, expected):
    assert is_valid_username(username) is expected

@pytest.mark.parametrize(
    ("email", "expected"),
    [
        ("alice@example.com", True),
        ("alice.example.com", False),
        ("alice@", False),
    ],
)
def test_email_validation(email, expected):
    assert is_valid_email(email) is expected

def test_argparse_scores_command(capsys):
    result = main(["scores"])
    captured = capsys.readouterr()
    assert result == 0
    assert "Scores" in captured.out or "No scores yet" in captured.out
