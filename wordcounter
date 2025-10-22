# Word Frequency Analyzer

# Prompt user for input
text = input("Enter a paragraph of text:\n")

# Clean the text
text = text.lower()  # convert to lowercase
for char in [",", ".", "!", "?"]:
    text = text.replace(char, "")  # remove punctuation

# Split into words
words = text.split()

# Count words using a dictionary
word_counts = {}
for word in words:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1

# Sort words by frequency (descending), then alphabetically
sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))

# Get the top 5 (or fewer if not enough words)
top_words = sorted_words[:5]

# Print results
for word, count in top_words:
    print(f"{word}: {count}")
