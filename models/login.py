import json
import os 
import hashlib

class User:
    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        
    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password_hash
        }

class UserManager:
    def __init__(self, users_file = "data/users.json"):
        self.users_file = users_file
        self.users = self.load_users()
        
    def load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except json.decoder.JSONDecodeError:
                return []
        else:
            return []
        
    def add_user(self, user):
        self.users.append(user.to_dict())
        self.save_users()
                           
    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
        
    def register_user(self, username, email, password):
        if any(user["email"] == email for user in self.users):
            print("Email already registered")
            return None
        password_hash = self.hash_password(password)
        new_user = User(username, email, password_hash)
        self.add_user(new_user)
        print("Registration successful!")
        return new_user
    
    def login_user(self, email, password):
        for user in self.users:
            if user["email"] == email and user["password"] == password:
                print(f"Welcome back, {user['username']}!")
                return User(user["username"], user["email"], user["password"])
        print("Invalid email or password")
        return None
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()