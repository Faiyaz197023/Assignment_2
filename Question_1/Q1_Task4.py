import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import re
from collections import Counter
import time
import csv

# Load scispaCy NER model for diseases and drugs
nlp_bc5cdr_md = spacy.load('en_ner_bc5cdr_md')
nlp_bc5cdr_md.max_length = 10000000  # Increase limit if needed

# Load BioBERT tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("alvaroalon2/biobert_diseases_ner")
model = AutoModelForTokenClassification.from_pretrained("alvaroalon2/biobert_diseases_ner")

# Check if GPU is available and move the model to the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


# Function to extract diseases and drugs entities from text using scispaCy
def extract_diseases_drugs_scispacy(text):
    doc = nlp_bc5cdr_md(text)
    entities = [(ent.text.strip().lower(), ent.label_) for ent in doc.ents if ent.label_ in ['DISEASE', 'CHEMICAL']]
    return entities


# Function to extract diseases and drugs entities from text using BioBERT
def extract_diseases_drugs_biobert(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    entities = []
    current_entity = []
    current_label = None

    for token, prediction in zip(tokens, predictions[0]):
        token = token.replace('##', '')  # Handling subword tokens
        label = model.config.id2label[prediction.item()]

        if label.startswith('B-'):
            if current_entity:
                if current_label in ['DISEASE', 'CHEMICAL']:
                    entities.append((" ".join(current_entity).strip().lower(), current_label))
            current_entity = [token]
            current_label = label[2:]
        elif label.startswith('I-') and current_label in ['DISEASE', 'CHEMICAL']:
            current_entity.append(token)
        else:
            if current_entity and current_label in ['DISEASE', 'CHEMICAL']:
                entities.append((" ".join(current_entity).strip().lower(), current_label))
            current_entity = []
            current_label = None

    if current_entity and current_label in ['DISEASE', 'CHEMICAL']:
        entities.append((" ".join(current_entity).strip().lower(), current_label))

    return entities


# Function to compare diseases and drugs entities extracted by both models
def compare_disease_drug_entities(text, chunk_num):
    # Extracting entities using scispaCy and BioBERT
    scispacy_entities = extract_diseases_drugs_scispacy(text)
    biobert_entities = extract_diseases_drugs_biobert(text)

    # Convert lists of entities into sets
    scispacy_set = set(scispacy_entities)
    biobert_set = set(biobert_entities)

    # Calculate common entities and unique entities
    common_entities = scispacy_set & biobert_set
    unique_to_scispacy = scispacy_set - biobert_set
    unique_to_biobert = biobert_set - scispacy_set

    # Save comparison results to a single CSV file
    save_comparison_results(chunk_num, common_entities, unique_to_scispacy, unique_to_biobert)


# Function to save comparison results in a single CSV file
def save_comparison_results(chunk_num, common_entities, unique_scispacy, unique_biobert):
    with open('comparison_results.csv', mode='a', newline='') as file:  # Open file in append mode
        writer = csv.writer(file)
        if chunk_num == 1:  # Write header only once for the first chunk
            writer.writerow(['Entity', 'Source', 'Chunk'])

        for entity in common_entities:
            writer.writerow([entity[0], 'Both', chunk_num])
        for entity in unique_scispacy:
            writer.writerow([entity[0], 'SciSpaCy', chunk_num])
        for entity in unique_biobert:
            writer.writerow([entity[0], 'BioBERT', chunk_num])


# Function to split large text into smaller chunks
def chunk_text(text, chunk_size=100000):
    """Split the text into chunks of specified size."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


# Example usage with chunking
file_path = 'extracted_text.txt'
with open(file_path, 'r') as file:
    text = file.read()

# Split the text into smaller chunks
text_chunks = chunk_text(text)

# Remove any existing CSV file to start fresh
with open('comparison_results.csv', 'w') as f:
    pass

# Process each chunk separately and append results to the same CSV file
for i, chunk in enumerate(text_chunks):
    start_time = time.time()
    print(f"Processing chunk {i + 1}/{len(text_chunks)}...")
    compare_disease_drug_entities(chunk, i + 1)
    print(f"Chunk {i + 1} processed in {time.time() - start_time:.2f} seconds")
