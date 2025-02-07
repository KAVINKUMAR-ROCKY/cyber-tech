import os
import json
import string
import random
import getpass
import shutil
import datetime
from cryptography.fernet import Fernet
from termcolor import colored
import pyfiglet

# Generate or load encryption key
def load_key():
    key_path = "key.key"
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
    else:
        with open(key_path, "rb") as key_file:
            key = key_file.read()
    return key

key = load_key()
cipher = Fernet(key)

# Encrypt and save passwords securely
def save_passwords(passwords):
    encrypted_data = cipher.encrypt(json.dumps(passwords).encode())
    with open("passwords.json", "wb") as file:
        file.write(encrypted_data)

# Load and decrypt stored passwords
def load_passwords():
    if not os.path.exists("passwords.json"):
        return {}
    try:
        with open("passwords.json", "rb") as file:
            encrypted_data = file.read()
        return json.loads(cipher.decrypt(encrypted_data).decode())
    except Exception:
        print(colored("❌ Error: Could not decrypt passwords. The file might be corrupted.", "red"))
        return {}

# Function to check password strength
def check_password_strength(password):
    strength_criteria = {
        "length": len(password) >= 8,
        "uppercase": any(char.isupper() for char in password),
        "lowercase": any(char.islower() for char in password),
        "digit": any(char.isdigit() for char in password),
        "special_char": any(char in string.punctuation for char in password)
    }

    strength_score = sum(strength_criteria.values())

    if strength_score == 5:
        return colored("🔒 Very Strong", "green")
    elif strength_score == 4:
        return colored("🛡️ Strong", "blue")
    elif strength_score == 3:
        return colored("⚠️ Medium", "yellow")
    elif strength_score == 2:
        return colored("❌ Weak", "red")
    else:
        return colored("❗ Very Weak", "magenta")

# Function to generate a strong password
def generate_strong_password(length=12):
    if length < 8:
        length = 8

    password_chars = (
        random.choice(string.ascii_uppercase) +
        random.choice(string.ascii_lowercase) +
        random.choice(string.digits) +
        random.choice(string.punctuation)
    )

    remaining_chars = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length - 4))
    password = list(password_chars + remaining_chars)
    random.shuffle(password)

    return ''.join(password)

# Function to add a password to storage
def add_password():
    site = input("Enter website: ").strip()
    username = input("Enter username: ").strip()
    password = getpass.getpass("Enter password (or type 'gen' to generate a strong one): ").strip()
    
    if password.lower() == "gen":
        password = generate_strong_password()
        print(colored(f"✅ Generated Strong Password: {password}", "cyan"))

    strength = check_password_strength(password)
    print(f"🔍 Password Strength: {strength}")

    passwords = load_passwords()
    passwords[site] = {"username": username, "password": password}
    save_passwords(passwords)

    print(colored("✅ Password saved successfully!", "green"))

# Function to view stored passwords
def view_passwords():
    passwords = load_passwords()
    if not passwords:
        print(colored("⚠️ No passwords stored.", "yellow"))
        return

    print(colored("\nStored Passwords:", "cyan"))
    for site, creds in passwords.items():
        print(colored(f"🌐 Website: {site} | 👤 Username: {creds['username']} | 🔑 Password: {creds['password']}", "blue"))

# Function to print ShieldPass in ASCII Art with color and center it
def print_shieldpass():
    ascii_art = pyfiglet.figlet_format("ShieldPass")
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    colored_art = "\n".join(colored(line.center(terminal_width), "cyan") for line in ascii_art.split("\n"))
    print(colored_art)

# Function to display greeting based on time of day
def print_greeting():
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greeting = "🌅 Good Morning!"
    elif 12 <= current_hour < 18:
        greeting = "🌞 Good Afternoon!"
    else:
        greeting = "🌙 Good Evening!"

    print(colored(f"\n{greeting} Welcome to ShieldPass! 🔐", "red"))

# Function to display a welcome message
def print_welcome_message():
    welcome_message = pyfiglet.figlet_format("Welcome")
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    colored_welcome = "\n".join(colored(line.center(terminal_width), "red") for line in welcome_message.split("\n"))
    print(colored_welcome)

# Main Menu
def main():
    print_welcome_message()
    print_shieldpass()
    print_greeting()
    
    while True:
        print(colored("1️⃣ Check Password Strength", "green"))
        print(colored("2️⃣ Generate Strong Password", "blue"))
        print(colored("3️⃣ Add Password", "yellow"))
        print(colored("4️⃣ View Passwords", "magenta"))
        print(colored("5️⃣ Exit", "red"))

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            password = input("Enter a password to check its strength: ").strip()
            strength = check_password_strength(password)
            print(f"🔍 Password Strength: {strength}")

        elif choice == "2":
            try:
                password_length = int(input("Enter desired password length (min 8): ").strip())
                generated_password = generate_strong_password(password_length)
                print(colored(f"✅ Generated Strong Password: {generated_password}", "cyan"))
            except ValueError:
                print(colored("❌ Please enter a valid number for password length.", "red"))

        elif choice == "3":
            add_password()

        elif choice == "4":
            view_passwords()

        elif choice == "5":
            print(colored("👋 Exiting ShieldPass. Stay secure!", "green"))
            break

        else:
            print(colored("⚠️ Invalid choice! Please select a valid option.", "red"))

# Start the program
if __name__ == "__main__":
    main()
