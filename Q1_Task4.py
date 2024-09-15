import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import re
from collections import Counter

# Load scispaCy NER model for diseases and drugs
nlp_bc5cdr_md = spacy.load('en_ner_bc5cdr_md')

# Increase the maximum length limit for large texts
nlp_bc5cdr_md.max_length = 10000000  # Increase limit if needed

# Load BioBERT tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("alvaroalon2/biobert_diseases_ner")
model = AutoModelForTokenClassification.from_pretrained("alvaroalon2/biobert_diseases_ner")


# Function to extract diseases and drugs entities from text using scispaCy
def extract_diseases_drugs_scispacy(text):
    doc = nlp_bc5cdr_md(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ['DISEASE', 'CHEMICAL']]
    return entities


# Function to extract diseases and drugs entities from text using BioBERT
def extract_diseases_drugs_biobert(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    entities = []
    current_entity = []
    current_label = None

    for token, prediction in zip(tokens, predictions[0]):
        token = re.sub('##', '', token)  # Handling subword tokens
        label = model.config.id2label[prediction.item()]

        if label.startswith('B-'):
            if current_entity:
                if current_label in ['DISEASE', 'CHEMICAL']:
                    entities.append(("".join(current_entity), current_label))
            current_entity = [token]
            current_label = label[2:]
        elif label.startswith('I-') and current_label in ['DISEASE', 'CHEMICAL']:
            current_entity.append(token)
        else:
            if current_entity and current_label in ['DISEASE', 'CHEMICAL']:
                entities.append(("".join(current_entity), current_label))
            current_entity = []
            current_label = None

    if current_entity and current_label in ['DISEASE', 'CHEMICAL']:
        entities.append(("".join(current_entity), current_label))

    return entities


# Function to compare diseases and drugs entities extracted by both models
def compare_disease_drug_entities(text):
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

    # Display the comparison results
    print(f"Total diseases/drugs detected by scispaCy: {len(scispacy_entities)}")
    print(f"Total diseases/drugs detected by BioBERT: {len(biobert_entities)}")

    print("\nCommon entities:")
    print(common_entities)

    print("\nEntities unique to scispaCy:")
    print(unique_to_scispacy)

    print("\nEntities unique to BioBERT:")
    print(unique_to_biobert)

    # Analyzing the most common entities
    all_scispacy_entities = [ent[0] for ent in scispacy_entities]
    all_biobert_entities = [ent[0] for ent in biobert_entities]

    print("\nMost common entities in scispaCy:")
    print(Counter(all_scispacy_entities).most_common(10))

    print("\nMost common entities in BioBERT:")
    print(Counter(all_biobert_entities).most_common(10))


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

# Process each chunk separately
for i, chunk in enumerate(text_chunks):
    print(f"Processing chunk {i + 1}/{len(text_chunks)}...")
    compare_disease_drug_entities(chunk)
