#!/usr/bin/env python3

# ============================================================
# pepper.py > author whoamiestevan
# Personal Combination Generator with Dog Companion
# ============================================================

import os
import sys
import time
from itertools import product

VERSION = "1.0"


# ============================================================
# Dog Companion Visuals
# ============================================================

def draw_dog(mouth_open=True, word=""):
    """Displays the dog header at the top of the screen with optional text."""
    eye = "@" if mouth_open else "-"
    dog_art = f"""
        / \\__
       (    {eye}\\___
       /         O
      /   (_____/
     /_____/   U
    """
    print(dog_art)
    if word:
        print(f"        [ {word} ]")
    print("-" * 50)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def render_header(mouth_open=True, bark_word=""):
    """Clears screen and always renders the dog at the top."""
    clear_screen()
    draw_dog(mouth_open, bark_word)


# ============================================================
# Utility Functions
# ============================================================

def loading(text, duration=1.0):
    print(text, end="", flush=True)

    symbols = ["|", "/", "-", "\\"]
    start = time.time()
    index = 0

    while time.time() - start < duration:
        print("\b" + symbols[index % len(symbols)], end="", flush=True)
        index += 1
        time.sleep(0.1)

    print("\b ", end="", flush=True)
    print()


# ============================================================
# Startup
# ============================================================

def startup():
    render_header(mouth_open=True, bark_word="WOOF!")
    print("\nPepper.py — Wordlist Generator")
    print()

    loading("Starting ", 0.8)
    
    render_header(mouth_open=False, bark_word="READY!")
    print("\nPepper is ready!\n")
    time.sleep(0.7)


# ============================================================
# Get Words
# ============================================================

def get_words():
    words = []

    render_header(mouth_open=True, bark_word="FEED ME WORDS!")
    print("\n=== ENTER 7 WORDS ===")
    print("(These can be words, numbers, or symbols)\n")

    for i in range(7):
        while True:
            word = input(f"Word {i + 1:02d}: ").strip()

            if word:
                words.append(word)
                break

            print("[!] Input cannot be empty.")

    render_header(mouth_open=True, bark_word="YUM!")
    print(f"\n[+] Successfully loaded {len(words)} words.\n")
    time.sleep(0.8)

    return words


# ============================================================
# Calculate Total
# ============================================================

def calculate_total(number_of_words, max_len=None):
    if max_len is None:
        max_len = number_of_words

    total = 0
    for length in range(1, max_len + 1):
        total += number_of_words ** length

    return total


# ============================================================
# Show Statistics
# ============================================================

def statistics(words):
    render_header(mouth_open=True, bark_word="STATS!")
    number = len(words)

    print("\n=== STATISTICS ===")
    print(f"\nWords entered: {number}")
    print("\nCandidates by length:")

    for length in range(1, number + 1):
        amount = number ** length
        print(f"  {length:2d} item(s): {amount:,}")

    total = calculate_total(number)
    print(f"\nTOTAL: {total:,}\n")


# ============================================================
# Show Words
# ============================================================

def show_words(words):
    render_header(mouth_open=False, bark_word="YOUR WORDS")
    print("\n=== ENTERED WORDS ===\n")

    for index, word in enumerate(words, 1):
        print(f"{index:02d}. {word}")

    print()


# ============================================================
# Estimate File Size
# ============================================================

def estimate_size(words):
    render_header(mouth_open=True, bark_word="BIG FILE?")
    total = calculate_total(len(words))

    average_length = (
        sum(len(word) for word in words)
        / len(words)
    )

    estimated = 0

    for length in range(1, len(words) + 1):
        combinations = len(words) ** length
        line_size = (average_length * length + 1)
        estimated += combinations * line_size

    print("\n=== SIZE ESTIMATE ===")
    print(f"\nCandidates: {total:,}")
    print(f"Average word length: {average_length:.2f} characters")
    print(f"Estimated TXT size: {format_size(estimated)}\n")


def format_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size)

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} PB"


# ============================================================
# Generate Directly to File
# ============================================================

def generate_to_file(words):
    render_header(mouth_open=True, bark_word="WORKING...")
    print("\n=== GENERATE WORDLIST ===\n")

    try:
        max_depth_input = input(f"Maximum combination length (1-{len(words)}, default {len(words)}): ").strip()
        max_depth = int(max_depth_input) if max_depth_input else len(words)
        max_depth = max(1, min(len(words), max_depth))
    except ValueError:
        max_depth = len(words)

    filename = input("Output filename (default: pepper.txt): ").strip() or "pepper.txt"

    total = calculate_total(len(words), max_depth)

    print(f"\nCandidates to generate: {total:,}")

    confirm = input("\nStart generation? [y/N]: ").strip().lower()

    if confirm != "y":
        print("[!] Generation cancelled.\n")
        return

    print()

    count = 0
    start_time = time.time()
    mouth_state = True

    try:
        with open(filename, "w", encoding="utf-8") as file:
            for length in range(1, max_depth + 1):
                for combination in product(words, repeat=length):
                    result = "".join(combination)
                    file.write(result + "\n")
                    count += 1

                    # Animate dog barking & progress counter periodically
                    if count % 20000 == 0:
                        mouth_state = not mouth_state
                        bark = "BARK!" if mouth_state else "WOOF!"
                        percent = (count / total) * 100

                        render_header(mouth_open=mouth_state, bark_word=bark)
                        print("\n=== GENERATING... ===")
                        print(f"Target File: {filename}")
                        print(f"Progress   : [{percent:6.2f}%] {count:,} / {total:,}")

        elapsed = time.time() - start_time

        render_header(mouth_open=True, bark_word="DONE!")
        print("\n[+] Generation complete!")
        print(f"[+] Candidates written: {count:,}")
        print(f"[+] Output file: {filename}")
        print(f"[+] Time: {elapsed:.2f} seconds\n")

    except KeyboardInterrupt:
        render_header(mouth_open=False, bark_word="STOPPED")
        print(f"\n[!] Generation interrupted.")
        print(f"[+] Candidates written before stopping: {count:,}\n")

    except OSError as error:
        print(f"\n[!] File error: {error}\n")


# ============================================================
# Menu
# ============================================================

def menu(words):
    while True:
        render_header(mouth_open=True, bark_word="PEPPER MENU")
        print("╔════════════════════════════════════╗")
        print("║  1. Generate wordlist              ║")
        print("║  2. Show entered words             ║")
        print("║  3. Show statistics                ║")
        print("║  4. Estimate file size             ║")
        print("║  5. Exit                           ║")
        print("╚════════════════════════════════════╝\n")

        choice = input("Pepper > ").strip()

        if choice == "1":
            generate_to_file(words)
        elif choice == "2":
            show_words(words)
        elif choice == "3":
            statistics(words)
        elif choice == "4":
            estimate_size(words)
        elif choice == "5":
            render_header(mouth_open=False, bark_word="BYE BYE!")
            print("\n[+] Goodbye!\n")
            break
        else:
            print("\n[!] Invalid option.")

        input("\nPress ENTER to continue...")


# ============================================================
# Main
# ============================================================

def main():
    startup()
    words = get_words()
    menu(words)


if __name__ == "__main__":
    main()
