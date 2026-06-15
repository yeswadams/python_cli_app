from models.game import Game
from models.score_manager import ScoreManager
from models.login import UserManager
import re

class CLIApp:
    def __init__(self):
        self.score_manager = ScoreManager()
        self.user_manager = UserManager()
        self.current_user = None

    def show_menu(self):
        print("\n--- Main Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. Play Game")
        print("4. View High Scores")
        print("5. Exit")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Enter choice: ")
            if choice == "1":
                name = input("Enter your name: ")
                if not re.match(r'^[a-zA-Z0-9]+$', name):
                    print("Invalid username. Please use only letters and numbers.")
                    continue
                email = input("Enter your email: ")
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    print("Invalid email format. Please use a valid email address.")
                    continue
                password = input("Enter a password: ")
                self.user_manager.register_user(name, email, password)
            elif choice == "2":
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                self.current_user = self.user_manager.login_user(email, password)
            elif choice == "3":
                if not self.current_user:
                    print("You must log in first!")
                    continue
                game = Game(self.current_user.username)
                game.start_game()
                while game.attempts < game.max_attempts:
                    guess = game.get_guess()
                    if game.check_guess(guess):
                        score = game.calculate_score()
                        print(f"You won! Score: {score}")
                        self.score_manager.add_score(self.current_user.username, score)
                        break
                else:
                    print(f"Game Over! The number was {game.secret_number}")
            elif choice == "4":
                self.score_manager.display_scores()
            elif choice == "5":
                print("Thank you for playing!")
                break
            else:
                print("Invalid choice, try again.")
