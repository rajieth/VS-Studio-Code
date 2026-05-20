#!/usr/bin/env python3
"""Simple password generator and strength checker.

This tool generates passwords and evaluates strength only.
No master password, no file storage, no data collection.
"""

import secrets
import string
import sys

DEFAULT_LENGTH = 16
MIN_LENGTH = 8
SEPARATOR = "=" * 50


def color_text(text, code):
    if not sys.stdout.isatty():
        return text
    return f"\033[{code}m{text}\033[0m"


def print_banner():
    print(color_text("\nPassword Generator", "35"))
    print(color_text("A simple tool for creating strong passwords.\n", "33"))


def print_divider():
    print(color_text(SEPARATOR, "34"))


def get_menu_choice():
    print_divider()
    print("Please choose an option:")
    print("1) Generate a strong password")
    print("2) Check password strength")
    print("3) Show security tips")
    print("4) Exit")
    choice = input("Enter 1-4: ").strip()
    return choice


def generate_password(length=DEFAULT_LENGTH):
    if length < MIN_LENGTH:
        length = MIN_LENGTH

    char_groups = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
    ]

    password_chars = [secrets.choice(group) for group in char_groups]
    all_chars = "".join(char_groups)
    password_chars += [secrets.choice(all_chars) for _ in range(length - len(password_chars))]
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def password_strength(password):
    score = 0
    reasons = []

    if len(password) >= 14:
        score += 2
    elif len(password) >= 10:
        score += 1
    else:
        reasons.append("Too short: use at least 12 characters.")

    if any(c.islower() for c in password):
        score += 1
    else:
        reasons.append("Add lowercase letters.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        reasons.append("Add uppercase letters.")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        reasons.append("Add digits.")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        reasons.append("Add symbols such as !, @, #, or ?.")

    lowered = password.lower()
    if "password" in lowered or "123" in lowered or "qwerty" in lowered:
        score = max(score - 2, 0)
        reasons.append("Avoid common words and patterns.")

    if score >= 5:
        label = "Excellent"
    elif score == 4:
        label = "Good"
    elif score == 3:
        label = "Fair"
    else:
        label = "Weak"

    return label, reasons


def show_security_tips():
    tips = [
        "Use a different password for every important account.",
        "Longer passwords are harder to crack than shorter ones.",
        "Include letters, numbers, and symbols.",
        "Avoid common words, sequences, and repeated characters.",
    ]
    print(color_text("\nSecurity tips:", "36"))
    for tip in tips:
        print(color_text(f"- {tip}", "33"))
    print()


def main():
    print_banner()

    while True:
        choice = get_menu_choice()

        if choice == "1":
            length_input = input("Enter password length (recommended 16): ").strip()
            try:
                length = int(length_input)
            except ValueError:
                length = DEFAULT_LENGTH
            password = generate_password(length)
            print(color_text(f"\nGenerated password: {password}", "32"))
            print()

        elif choice == "2":
            password = input("Enter the password to check: ").strip()
            label, reasons = password_strength(password)
            print(color_text(f"\nStrength: {label}", "36"))
            if reasons:
                print(color_text("Improvement suggestions:", "33"))
                for reason in reasons:
                    print(f"- {reason}")
            else:
                print(color_text("This password is strong.", "32"))
            print()

        elif choice == "3":
            show_security_tips()

        elif choice == "4":
            print(color_text("Goodbye. Stay secure!", "36"))
            break

        else:
            print(color_text("Invalid choice. Please enter a number from 1 to 4.\n", "31"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(color_text("\nProgram interrupted. Goodbye.", "31"))
    finally:
        try:
            input("Press Enter to close this window...")
        except Exception:
            pass
