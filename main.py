import argparse

from models.cli_app import CLIApp
from models.game import Game
from models.login import UserManager
from models.score_manager import ScoreManager
from utils.helpers import is_valid_email, is_valid_username


def build_parser():
    parser = argparse.ArgumentParser(
        description="Secure CLI number guessing game with user accounts and high scores."
    )
    subparsers = parser.add_subparsers(dest="command")

    register_parser = subparsers.add_parser("register", help="Create a user account")
    register_parser.add_argument("--username", required=True, help="Letters and numbers only")
    register_parser.add_argument("--email", required=True, help="User email address")
    register_parser.add_argument("--password", required=True, help="Account password")

    login_parser = subparsers.add_parser("login", help="Verify account credentials")
    login_parser.add_argument("--email", required=True, help="User email address")
    login_parser.add_argument("--password", required=True, help="Account password")

    subparsers.add_parser("scores", help="Show saved high scores")

    play_parser = subparsers.add_parser("play", help="Play one game from the terminal")
    play_parser.add_argument("--username", required=True, help="Player name for this round")
    play_parser.add_argument("--max-attempts", type=int, default=10, help="Maximum guesses allowed")

    return parser


def run_command(args):
    if args.command == "register":
        if not is_valid_username(args.username):
            print("Invalid username. Please use only letters and numbers.")
            return 1
        if not is_valid_email(args.email):
            print("Invalid email format. Please use a valid email address.")
            return 1
        return 0 if UserManager().register_user(args.username, args.email, args.password) else 1

    if args.command == "login":
        return 0 if UserManager().login_user(args.email, args.password) else 1

    if args.command == "scores":
        ScoreManager().display_scores()
        return 0

    if args.command == "play":
        if not is_valid_username(args.username):
            print("Invalid username. Please use only letters and numbers.")
            return 1
        game = Game(args.username, max_attempts=args.max_attempts)
        score_manager = ScoreManager()
        game.start_game()
        while game.has_attempts_remaining():
            guess = game.get_guess()
            if game.check_guess(guess):
                score = game.calculate_score()
                print(f"You won! Score: {score}")
                score_manager.add_score(args.username, score)
                return 0
        print(f"Game Over! The number was {game.secret_number}")
        return 0

    app = CLIApp()
    app.run()
    return 0


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return run_command(args)


if __name__ == "__main__":
    raise SystemExit(main())
