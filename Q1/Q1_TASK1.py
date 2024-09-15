import pandas as pd

# List of files to read and corresponding columns to extract
files_columns = [
    ("CSV1.csv", "SHORT-TEXT"),  # File and column for CSV1
    ("CSV2.csv", "TEXT"),        # File and column for CSV2
    ("CSV3.csv", "TEXT")    ,
    ("CSV4.csv","TEXT")# File and column for CSV3
]

# Initialize an empty list to hold all text
all_text = []

# Read the files and extract the specified columns
for file, column in files_columns:
    df = pd.read_csv(file)[[column]]
    # Flatten the column into a list of strings and extend to all_text
    all_text.extend(df[column].dropna().astype(str).tolist())

# Join all text into a single string with proper spaces
text_line = ' '.join(all_text)

# Write the text line to a file
with open("extracted_text.txt", "w") as text_file:
    text_file.write(text_line)
