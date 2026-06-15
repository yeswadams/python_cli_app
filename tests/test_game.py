# tests
import pytest
from models.game import Game
from models.score_manager import ScoreManager
from models.login import UserManager

# ---Game Test ---
def test_game_initialization():
    game = Game("TestPlayer")
    assert game.player_name == "TestPlayer"
    assert 1 <= game.secret_number <= 100
    assert game.attempts == 0
    assert game.max_attempts == 10

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

def test_register_and_login_user(tmp_path):
    user_file = tmp_path / "users.json" 
    manager = UserManager(users_file=str(user_file))
    user = manager.register_user("Alice", "alice@example.com", "password123")
    assert user is not None
    logged_in = manager.login_user("alice@example.com", "password123")
    assert logged_in is not None
    assert logged_in.username == "Alice"