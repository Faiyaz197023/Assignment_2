from collections import Counter
import re
import pandas as pd

# Function to read text file and count word occurrences
def get_top_words(file_path, top_n=30):
    # Read the text file
    with open(file_path, 'r') as file:
        text = file.read()

    # Convert to lowercase and remove non-alphanumeric characters (excluding spaces)
    text = re.sub(r'\W+', ' ', text.lower())

    # Split text into words
    words = text.split()

    # Count the occurrences of each word
    word_counts = Counter(words)

    # Get the top 'n' most common words
    top_words = word_counts.most_common(top_n)

    return top_words

# Path to the text file
file_path = "extracted_text.txt"  # replace with your file path

# Get the top 30 most common words
top_30_words = get_top_words(file_path)

# Display the top 30 words
for word, count in top_30_words:
    print(f'{word}: {count}')

# Store the top 30 words and their counts into a CSV file
top_words_df = pd.DataFrame(top_30_words, columns=['Word', 'Count'])
output_csv_path = "top_30_words.csv"  # specify the output CSV file path
top_words_df.to_csv(output_csv_path, index=False)

print(f'Top 30 words have been saved to {output_csv_path}')
