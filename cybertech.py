import random
import string

# A Simple Password Generator (optional)
def generate_strong_password(length=12):
    """Generate a simple random password using alphanumeric characters."""
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Main Program Menu
def main():
    print("1. Password Strength Checking")
    print("2. Strong Password Generator")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        password = input("Enter a password to check its strength: ")
        print(f"Password is: {password}")

    elif choice == "2":
        password_length = int(input("Enter the desired password length: "))
        generated_password = generate_strong_password(password_length)
        print(f"Generated strong password: {generated_password}")

    elif choice == "3":
        print("Exiting the program.")
        exit()

    else:
        print("Invalid choice! Please select a valid option.")
        main()  # Return to the main menu

# Start the program
if __name__ == "__main__":
    main()
