import os

# Define the repository root path
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Define input and output paths
input_file = os.path.join(repo_path, "data/context/geneval-context-wikiprofessions-2to1-test.en_ru.en")
output_folder = os.path.join(repo_path, "scripts/data_preprocessing/chunks-context")

chunk_size = 100  # Number of lines per chunk

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read the file and split into chunks
with open(input_file, 'r', encoding='utf-8') as f:
    for i, chunk in enumerate(iter(lambda: list(f.readline().strip() for _ in range(chunk_size)), [])):
        output_file = os.path.join(output_folder, f"chunk_{i}.csv")
        
        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write("\n".join(chunk))

        print(f"File created: {output_file}")

print("Splitting process completed.")
