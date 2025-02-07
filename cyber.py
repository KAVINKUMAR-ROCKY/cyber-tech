import os
import json
import string
import random
import getpass
from cryptography.fernet import Fernet

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
        print("Error: Could not decrypt passwords. The file might be corrupted.")
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
        return "🔒 Very Strong"
    elif strength_score == 4:
        return "🛡️ Strong"
    elif strength_score == 3:
        return "⚠️ Medium"
    elif strength_score == 2:
        return "❌ Weak"
    else:
        return "❗ Very Weak"

# Function to generate a strong password
def generate_strong_password(length=12):
    if length < 8:
        length = 8  # Enforce minimum security standards

    password_chars = (
        random.choice(string.ascii_uppercase) +
        random.choice(string.ascii_lowercase) +
        random.choice(string.digits) +
        random.choice(string.punctuation)
    )

    remaining_chars = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length - 4))
    password = list(password_chars + remaining_chars)
    random.shuffle(password)  # Shuffle for better randomness

    return ''.join(password)

# Function to add a password to storage
def add_password():
    site = input("Enter website: ").strip()
    username = input("Enter username: ").strip()
    
    # Mask password input
    password = getpass.getpass("Enter password (or type 'gen' to generate a strong one): ").strip()
    
    if password.lower() == "gen":
        password = generate_strong_password()
        print(f"Generated Strong Password: {password}")

    # Check strength before saving
    strength = check_password_strength(password)
    print(f"Password Strength: {strength}")

    passwords = load_passwords()
    passwords[site] = {"username": username, "password": password}
    save_passwords(passwords)

    print("✅ Password saved successfully!")

# Function to view stored passwords
def view_passwords():
    passwords = load_passwords()
    if not passwords:
        print("No passwords stored.")
        return

    print("\nStored Passwords:")
    for site, creds in passwords.items():
        print(f"🌐 Website: {site} | 👤 Username: {creds['username']} | 🔑 Password: {creds['password']}")

# Main Menu
def main():
    while True:
        print("\n🔐 Password Manager")
        print("1️⃣ Check Password Strength")
        print("2️⃣ Generate Strong Password")
        print("3️⃣ Add Password")
        print("4️⃣ View Passwords")
        print("5️⃣ Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            password = input("Enter a password to check its strength: ").strip()
            strength = check_password_strength(password)
            print(f"🔍 Password Strength: {strength}")

        elif choice == "2":
            try:
                password_length = int(input("Enter desired password length (min 8): ").strip())
                generated_password = generate_strong_password(password_length)
                print(f"✅ Generated Strong Password: {generated_password}")
            except ValueError:
                print("❌ Please enter a valid number for password length.")

        elif choice == "3":
            add_password()

        elif choice == "4":
            view_passwords()

        elif choice == "5":
            print("👋 Exiting the program. Stay secure!")
            break

        else:
            print("⚠️ Invalid choice! Please select a valid option.")

# Start the program
if __name__ == "__main__":
    main()
