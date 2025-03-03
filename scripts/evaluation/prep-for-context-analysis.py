import os
import csv

# Define repository root dynamically
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Define file paths
input_csv = os.path.join(repo_path, "data", "translations", "results-context", "checked_results_context.csv")
original_file = os.path.join(repo_path, "data", "translations", "results-context", "orig_context.txt")
translation_file = os.path.join(repo_path, "data", "translations", "results-context", "context_translations.txt")

# Split into original and translated text
with open(input_csv, 'r', encoding='utf-8') as csv_file, \
     open(original_file, 'w', encoding='utf-8') as orig_file, \
     open(translation_file, 'w', encoding='utf-8') as trans_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        orig_file.write(row['Original'] + '\n')
        trans_file.write(row['Translation'] + '\n')

print(f"Original texts saved to: {original_file}")
print(f"Translated texts saved to: {translation_file}")
