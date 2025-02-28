import os
import pandas as pd

# Define repository root dynamically
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Define input folder and output file path
results_folder = os.path.join(repo_path, "data", "translations", "results-counter")
output_file = os.path.join(results_folder, "all-results-counter.csv")

# Get a sorted list of all relevant files
result_files = sorted(
    [os.path.join(results_folder, f) for f in os.listdir(results_folder) if f.startswith("checked_result_") and f.endswith(".csv")]
)

# Create an empty DataFrame to merge data
combined_data = pd.DataFrame()

# Flag to control first file processing
is_first_file = True

# Process each file
for file in result_files:
    try:
        print(f"Reading file: {file}")
        # Skip header alignment for the first file
        data = pd.read_csv(file)
        if not is_first_file:
            data.columns = combined_data.columns  # Ensure header consistency
        combined_data = pd.concat([combined_data, data], ignore_index=True)
        is_first_file = False
    except Exception as e:
        print(f"Error reading file {file}: {e}")

# Save the merged file
combined_data.to_csv(output_file, index=False, encoding="utf-8")
print(f"Merged file saved at: {output_file}")
