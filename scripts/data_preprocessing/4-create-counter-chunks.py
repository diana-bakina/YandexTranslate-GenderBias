import os
import pandas as pd
import numpy as np

# Get repository root dynamically
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Define input and output paths
data_folder = os.path.join(repo_path, "scripts", "data_preprocessing")
output_folder = os.path.join(data_folder, "chunks-counter")

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Input file path
input_csv = os.path.join(data_folder, "counter_sentences.csv")

# Check if the input file exists
if not os.path.exists(input_csv):
    print(f"Error: File not found - {input_csv}")
    exit(1)

# Read the full dataset
data = pd.read_csv(input_csv)

# Split into chunks
chunk_size = 200
chunks = np.array_split(data, np.ceil(len(data) / chunk_size))

# Save each chunk
for i, chunk in enumerate(chunks):
    output_csv = os.path.join(output_folder, f"counter_chunk_{i}.csv")
    chunk.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"File saved: {output_csv}")

print("Chunking process completed.")
