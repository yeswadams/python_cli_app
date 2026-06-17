MENU_OPTIONS = (
    ("1", "Register"),
    ("2", "Login"),
    ("3", "Play Game"),
    ("4", "View High Scores"),
    ("5", "Exit"),
)


def print_main_menu() -> None:
    print("\n--- Main Menu ---")
    for value, label in MENU_OPTIONS:
        print(f"{value}. {label}")
