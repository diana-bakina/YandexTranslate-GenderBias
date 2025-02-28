import os

# Define repository root dynamically
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Define input and output folders
input_folder = os.path.join(repo_path, "data", "translations", "results-context")
output_folder = os.path.join(repo_path, "data", "translations", "results-context-fixed")

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)


def fix_delimiter(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        # Read the first line (header)
        header = f_in.readline().strip().replace(",", "\t")
        f_out.write(header + "\n")

        # Process data lines
        for line in f_in:
            # Replace delimiter while preserving quoted text
            fixed_line = line.strip().replace('\",\"', '"\t"')
            f_out.write(fixed_line + "\n")


# Process all files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.startswith("result_chunk") and file_name.endswith(".csv"):
        input_file = os.path.join(input_folder, file_name)
        output_file = os.path.join(output_folder, file_name.replace(".csv", ".tsv"))
        fix_delimiter(input_file, output_file)
        print(f"File {file_name} processed and saved as {output_file}.")

print("Processing completed.")