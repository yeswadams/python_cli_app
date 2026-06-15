from utils.storage import load_users, save_users
from utils.cli import login_screen, register_screen

def main():
    users = load_users()
    users = login_screen(users)
    
    
    
if __name__ == "__main__":
    main()
   