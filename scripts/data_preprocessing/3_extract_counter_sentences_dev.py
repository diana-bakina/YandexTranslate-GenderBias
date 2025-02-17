import os
import pandas as pd

# Get the repository root dynamically
repo_path = os.path.dirname(os.path.abspath(__file__))  # Get script location
data_folder = os.path.join(repo_path, "..", "data", "sentences", "test")  # Path to input data
output_folder = os.path.join(repo_path, "..", "scripts", "data_preprocessing")  # Path to output

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Paths to input files
feminine_file = os.path.join(data_folder, "geneval-sentences-feminine-test.en_ru.en")
masculine_file = os.path.join(data_folder, "geneval-sentences-masculine-test.en_ru.en")
output_file = os.path.join(output_folder, "counter_sentences.csv")  # Save in data_processing

# Function for reading data from a text file
def read_sentences(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f]

# Reading sentences
feminine_sentences = read_sentences(feminine_file)
masculine_sentences = read_sentences(masculine_file)

# Creating a DataFrame
data = {
    "Type": ["Feminine"] * len(feminine_sentences) + ["Masculine"] * len(masculine_sentences),
    "Text": feminine_sentences + masculine_sentences,
}

df = pd.DataFrame(data)

# Saving to CSV
df.to_csv(output_file, index=False, encoding="utf-8")
print(f"Sentences file saved: {output_file}")
