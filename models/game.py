# game.py
import random

class Game:
    def __init__(self, player_name: str, max_attempts: int=10):
        self.player_name = player_name
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = max_attempts
        self.score = 0

    def start_game(self):
        print(f"Welcome {self.player_name}! Guess the number between 1 and 100.")

    def get_guess(self):
        while True:
            try:
                return int(input("Enter your guess: "))
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def check_guess(self, guess: int):
        self.attempts += 1
        if guess < self.secret_number:
            print("Too low!")
        elif guess > self.secret_number:
            print("Too high!")
        else:
            print("Correct!")
            return True
        return False

    def calculate_score(self):
        self.score = max(0, 100 - (self.attempts - 1) * 10)
        return self.score
