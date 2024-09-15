from transformers import AutoTokenizer
from collections import Counter
import pandas as pd

def get_top_tokens(file_path, top_n=30, model_name='distilbert-base-uncased'):
    # Initialize the tokenizer with clean_up_tokenization_spaces=False
    tokenizer = AutoTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=False)

    # Initialize a Counter for token frequencies
    token_counts = Counter()

    # Process the text file line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Tokenize the line
            tokens = tokenizer.tokenize(line)
            # Update the token counts
            token_counts.update(tokens)

    # Get the top 'n' most common tokens
    top_tokens = token_counts.most_common(top_n)

    return top_tokens

# Path to the text file
file_path = "extracted_text.txt"  # replace with your file path

# Get the top 30 most common tokens
top_30_tokens = get_top_tokens(file_path)

# Display the top 30 tokens
for token, count in top_30_tokens:
    print(f'{token}: {count}')

# Save the top 30 tokens to a CSV file
top_tokens_df = pd.DataFrame(top_30_tokens, columns=['Token', 'Count'])
output_csv_path = "top_30_tokens.csv"  # specify the output CSV file path
top_tokens_df.to_csv(output_csv_path, index=False)

print(f'Top 30 tokens have been saved to {output_csv_path}')
