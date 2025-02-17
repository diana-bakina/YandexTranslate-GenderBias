import os

# Define paths relative to the repository
repo_path = os.path.dirname(os.path.abspath(__file__))  # Get the root directory of the repository
input_file = os.path.join(repo_path, "data/context/geneval-context-wikiprofessions-2to1-test.en_ru.en")
output_folder = os.path.join(repo_path, "scripts/data_preprocessing/chunks-context")

chunk_size = 100  # Number of lines per batch

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read the source file
with open(input_file, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f.readlines()]

# Split lines into batches and save them as separate files
for i in range(0, len(lines), chunk_size):
    batch_lines = lines[i:i + chunk_size]
    output_file = os.path.join(output_folder, f"chunk_{i // chunk_size}.csv")
    
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write("\n".join(batch_lines))
    
    print(f"File created: {output_file}")