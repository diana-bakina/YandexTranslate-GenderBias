import os
import pandas as pd

# Define repository root dynamically
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Define input folder and output file path
results_folder = os.path.join(repo_path, "data", "translations", "results-context")
output_file = os.path.join(results_folder, "combined_context_results.tsv")

# Get a list of all relevant files in the results folder
result_files = [os.path.join(results_folder, f) for f in os.listdir(results_folder) if f.startswith("result_") and f.endswith(".csv")]

# Sort files based on the numeric value in the filename
result_files = sorted(result_files, key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split("_")[-1]))

# Create an empty DataFrame to merge data
combined_data = pd.DataFrame()

# Process each file
for file in result_files:
    try:
        print(f"Reading file: {file}")
        data = pd.read_csv(file, sep='\t')  # Use tab as a separator
        combined_data = pd.concat([combined_data, data], ignore_index=True)
    except Exception as e:
        print(f"Error reading file {file}: {e}")

# Save the merged file
combined_data.to_csv(output_file, index=False, encoding="utf-8", sep='\t')  # Save with tab separator
print(f"Merged file saved at: {output_file}")
