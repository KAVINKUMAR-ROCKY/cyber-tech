import random
import string

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
        return "Very Strong"
    elif strength_score == 4:
        return "Strong"
    elif strength_score == 3:
        return "Medium"
    elif strength_score == 2:
        return "Weak"
    else:
        return "Very Weak"

# Function to generate a strong password
def generate_strong_password(length=12):
    if length < 8:
        length = 8  # Ensuring minimum security standards
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Main Menu
def main():
    while True:
        print("\n1. Check Password Strength")
        print("2. Generate Strong Password")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            password = input("Enter a password to check its strength: ")
            strength = check_password_strength(password)
            print(f"Password Strength: {strength}")

        elif choice == "2":
            password_length = int(input("Enter desired password length (min 8): "))
            generated_password = generate_strong_password(password_length)
            print(f"Generated Strong Password: {generated_password}")

        elif choice == "3":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice! Please select a valid option.")

# Start the program
if __name__ == "__main__":
    main()
