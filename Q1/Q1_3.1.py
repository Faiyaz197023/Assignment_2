from collections import Counter
import re
import pandas as pd


def get_top_words(file_path, top_n=30):
    # Read the text file
    with open(file_path, 'r') as file:
        text = file.read()


    text = re.sub(r'\W+', ' ', text.lower())


    words = text.split()


    word_counts = Counter(words)


    top_words = word_counts.most_common(top_n)

    return top_words


file_path = "extracted_text.txt"


top_30_words = get_top_words(file_path)


for word, count in top_30_words:
    print(f'{word}: {count}')

# Store the top 30 words and their counts into a CSV file
top_words_df = pd.DataFrame(top_30_words, columns=['Word', 'Count'])
output_csv_path = "top_30_words.csv"  # specify the output CSV file path
top_words_df.to_csv(output_csv_path, index=False)

print(f'Top 30 words have been saved to {output_csv_path}')
