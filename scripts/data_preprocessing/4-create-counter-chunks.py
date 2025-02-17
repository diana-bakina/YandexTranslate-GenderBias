import os
import pandas as pd

# Get repository root dynamically
repo_path = os.path.dirname(os.path.abspath(__file__))  # Get script location
data_folder = os.path.join(repo_path, "data_preprocessing")  # Where counter_sentences.csv is stored
output_folder = os.path.join(repo_path, "data_preprocessing", "chunks-counter")  # Where chunks will be saved

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Paths to files
input_csv = os.path.join(data_folder, "counter_sentences.csv")

# Read the full dataset
data = pd.read_csv(input_csv)

# Break into portions of 200 lines
chunk_size = 200
for i, chunk in enumerate(range(0, len(data), chunk_size)):
    chunk_data = data.iloc[chunk:chunk + chunk_size]
    output_csv = os.path.join(output_folder, f"counter_chunk_{i}.csv")
    chunk_data.to_csv(output_csv, index=False)
    print(f"File saved: {output_csv}")
