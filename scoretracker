# Score Tracker Program

scores = []

while True:
    user_input = input("Enter a score (0-100) or 'done': ").strip()

    if user_input.lower() == "done":
        break

    # Validate: must be a number between 0 and 100 inclusive
    try:
        value = float(user_input)
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 100.")
        continue

    if 0 <= value <= 100:
        scores.append(value)
    else:
        print("Invalid input. Please enter a number between 0 and 100.")

# After input loop
if scores:
    scores.sort()  # in-place
    minimum = min(scores)
    maximum = max(scores)
    average = sum(scores) / len(scores)

    print(f"\nMinimum score: {minimum}")
    print(f"Maximum score: {maximum}")
    print(f"Average score: {average:.2f}")  # f-string w/ 2 decimals
    print(f"Sorted scores: {scores}")
else:
    print("\nNo scores were entered.")
