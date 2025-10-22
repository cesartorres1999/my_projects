# Pseudocode
#BEGIN
# PRINT welcome message with room description

# phrase ← INPUT("Enter any mystery phrase you choose")
# WHILE phrase is empty:
#     PRINT "Please enter a non-empty phrase."
#     phrase ← INPUT(...)

# target_code ← compute_code(phrase)  // sum(ord(c) for c in phrase) % 10000
# PRINT instructions describing how to derive the code (no secrets hard-coded)

# // Safe step
# REPEAT
#     code_input ← INPUT("Enter the 4-digit code")
#     IF code_input is not exactly 4 digits:
#         PRINT friendly message about format
#         CONTINUE
#     IF int(code_input) equals target_code (with zero padding rules):
#         PRINT "Safe unlocked"
#         BREAK
#     ELSE
#         PRINT "Incorrect code; hint: re-check your calculation."
# UNTIL unlocked

# // Key step

# remainder ← len(phrase) % 3
# correct_key ← MAP {0: "sun", 1: "moon", 2: "star"}[remainder]
# PRINT instructions describing mapping (again no fixed answers; depends on phrase)

# REPEAT
#     key_choice ← INPUT("Choose a key: Sun, Moon, or Star")
#     NORMALIZE key_choice to lowercase and strip
#     IF key_choice not in {"sun","moon","star"}:
#         PRINT friendly guidance and allowed options
#         CONTINUE
#     IF key_choice equals correct_key:
#         PRINT "Door unlocked"
#         success ← TRUE
#     ELSE
#         PRINT "Wrong key; try again."
# UNTIL success

# PRINT final message: "Escape successful!"
# END

# Python program
def prompt_nonempty(prompt_text: str) -> str:
    """
    Prompt the user for a non-empty string. Re-prompts kindly until a non-empty value is entered.
    
    Args:
        prompt_text: The message to display to the user.
    Returns:
        A non-empty string input by the user (leading/trailing whitespace stripped).
    """
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print(f"Please enter something non-empty. Let's try again.")


def compute_code(phrase: str) -> str:
    """
    Compute the 4-digit safe code based on a user-provided phrase.
    
    Rule (as written on the in-room note):
      - Sum the character codes (ord) of every character in the phrase.
      - Take the result modulo 10000.
      - Represent it as a 4-digit string (leading zeros allowed).
    
    Args:
        phrase: The user-chosen phrase.
    Returns:
        A 4-character string representing the code, zero-padded if necessary.
    """
    total = sum(ord(c) for c in phrase)
    code_num = total % 10000
    return f"{code_num:04d}"


def explain_code_rules(phrase: str) -> None:
    """
    Print friendly, explicit instructions on how to derive the safe code from the phrase.
    
    Args:
        phrase: The user-chosen phrase (used only to tailor messages with f-strings).
    """
    print(f"You examine a note near the safe. It reads:")
    print(f"- 'Use the mystery phrase you chose to compute the code.'")
    print(f"- 'Add the character codes (ordinals) of each character in your phrase.'")
    print(f"- 'Take that sum modulo 10000, and enter it as a 4-digit code (leading zeros allowed).'")
    print(f"For reference, your current phrase is: '{phrase}'.")


def ask_for_code(target_code: str) -> None:
    """
    Interactively ask the user to enter the 4-digit code, validating format and correctness.
    Continues until the user enters the correct code.
    
    Args:
        target_code: The correct 4-digit code string computed from the phrase.
    """
    while True:
        raw = input("Enter the 4-digit code for the safe: ").strip()
        if not (len(raw) == 4 and raw.isdigit()):
            print(f"That didn’t look like exactly 4 digits. Please enter a 4-digit code like '0072' or '4521'.")
            continue
        if raw == target_code:
            print(f"Step 1: Code {raw} accepted, safe unlocked.")
            return
        print(f"That code didn’t work. Kindly re-check your calculation and try again.")


def correct_key_from_phrase(phrase: str) -> str:
    """
    Determine which key opens the door based on the length of the user phrase.
    
    Rule (as written on the in-room note):
      - Compute length_of_phrase % 3
      - 0 -> 'sun', 1 -> 'moon', 2 -> 'star'
    
    Args:
        phrase: The user-chosen phrase.
    Returns:
        The lowercase name of the correct key: 'sun', 'moon', or 'star'.
    """
    remainder = len(phrase) % 3
    mapping = {0: "sun", 1: "moon", 2: "star"}
    return mapping[remainder]


def explain_key_rules(phrase: str) -> None:
    """
    Print the door key selection rules, derived from the user phrase length.
    
    Args:
        phrase: The user-chosen phrase (used to personalize guidance).
    """
    print(f"You approach the door and find three keys labeled 'Sun', 'Moon', and 'Star'.")
    print(f"Another note says:")
    print(f"  - 'Count the number of characters in your phrase.'")
    print(f"  - 'Compute length % 3. If remainder is 0 -> Sun, 1 -> Moon, 2 -> Star.'")
    print(f"Your phrase length is {len(phrase)} characters.")


def ask_for_key(correct_key: str) -> None:
    """
    Ask the user to choose among Sun, Moon, or Star, validating input and correctness.
    Keeps prompting until the correct key is chosen.
    
    Args:
        correct_key: The correct key name in lowercase ('sun', 'moon', or 'star').
    """
    valid = {"sun", "moon", "star"}
    pretty = {"sun": "Sun", "moon": "Moon", "star": "Star"}
    while True:
        choice = input("Choose a key (Sun/Moon/Star): ").strip().lower()
        if choice not in valid:
            print(f"That didn’t match one of the available keys. Please enter 'Sun', 'Moon', or 'Star'.")
            continue
        if choice == correct_key:
            print(f"Step 2: {pretty[choice]} key chosen, door unlocked.")
            return
        print(f"That key doesn’t fit. Remember to use the remainder rule. Try again!")


def escape_room() -> None:
    """
    Orchestrates the full escape-room flow:
      1) Prompt for a user phrase (not hard-coded).
      2) Explain and validate the safe code based on the phrase.
      3) Explain and validate the door key selection based on the phrase.
      4) Celebrate the successful escape.
    """
    print(f"Welcome to the Virtual Escape Room!")
    print(f"You see a locked safe, a closed door with three keys, and two cryptic notes.")
    phrase = prompt_nonempty("Choose and enter your mystery phrase (any text you like): ")
    print(f"Great choice! Your mystery phrase is '{phrase}'.")
    
    # Safe step
    explain_code_rules(phrase)
    target_code = compute_code(phrase)
    ask_for_code(target_code)
    
    # Door step
    explain_key_rules(phrase)
    correct_key = correct_key_from_phrase(phrase)
    ask_for_key(correct_key)
    
    print(f"Escape successful! You step into the fresh air beyond the door. 🎉")


# --- MAIN ENTRY POINT ---
if __name__ == "__main__":
    try:
        escape_room()
    except Exception as exc:
        # Belt-and-suspenders: catch-any to ensure kindness over crashes.
        print(f"Something unexpected happened, but you’re okay! Here’s a friendly note: {exc}")

# Test scenarios (scripted)

# These demonstrate correct behavior, including helpful validation when users make mistakes.
# Because the “answers” depend on the user’s phrase, each scenario computes its own code via the stated rules—no hard-coded secrets.

# Scenario 1: Smooth success, phrase “escape”

# Inputs

# Phrase: escape

# sum(ord(c) for c in "escape") = 101+115+99+97+112+101 = 625 → 625 % 10000 = 625 → code 0625

# Code: 0625

# Phrase length = 6 → 6 % 3 = 0 → correct key: Sun

# Key choice: Sun

# Expected key outputs

# Step 1: Code 0625 accepted, safe unlocked.

# Step 2: Sun key chosen, door unlocked.

# Escape successful!

# Scenario 2: Mistake in code, then correction; phrase “Room 101”

# Compute code

# Characters in "Room 101": R(82) o(111) o(111) m(109) (space)(32) 1(49) 0(48) 1(49)

# Sum = 82+111+111+109+32+49+48+49 = 591 → code 0591

# Inputs & outputs

# Phrase: Room 101

# Code attempt 1: 591 → Invalid format (not 4 digits).


# Program: “Please enter a 4-digit code like '0072' or '4521'.”

# Code attempt 2: 0581 → Incorrect.

# Program: “That code didn’t work. Kindly re-check your calculation and try again.”

# Code attempt 3: 0591 → Success: “Step 1: Code 0591 accepted, safe unlocked.”

# Length = 8 → 8 % 3 = 2 → Star

# Key choice: Moon → Wrong

# Program: “That key doesn’t fit. Remember to use the remainder rule. Try again!”

# Key choice: Star → Success

# “Step 2: Star key chosen, door unlocked.”

# Final: Escape successful!

# Scenario 3: Invalid key input then success; phrase “a”

# Compute code

# "a": ord('a') = 97 → 0097

# Inputs & outputs

# Phrase: a

# Code: 0097 → “Step 1: Code 0097 accepted, safe unlocked.”

# Length = 1 → 1 % 3 = 1 → Moon

# Key choice: pear → Invalid option

# Program: “Please enter 'Sun', 'Moon', or 'Star'.”

# Key choice: moon → Success

# “Step 2: Moon key chosen, door unlocked.”

# Final: Escape successful!




