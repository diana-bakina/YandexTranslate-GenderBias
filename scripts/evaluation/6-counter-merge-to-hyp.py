import pandas as pd

# Paths to files
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
combined_file = os.path.join(repo_path, "data", "translations", "results-counter", "checked_results_counter.csv")
output_feminine = os.path.join(repo_path, "data", "translations", "results-counter", "hyp_feminine_ru.txt")
output_masculine = os.path.join(repo_path, "data", "translations", "results-counter", "hyp_masculine_ru.txt") 

# Loading the combined file
data = pd.read_csv(combined_file)

# Splitting data by gender
feminine_data = data[data["Type"] == "Feminine"]["Translated_Text"]
masculine_data = data[data["Type"] == "Masculine"]["Translated_Text"]

# Saving data to text files
feminine_data.to_csv(output_feminine, index=False, header=False, encoding="utf-8")
masculine_data.to_csv(output_masculine, index=False, header=False, encoding="utf-8")

print(f"Feminine translations saved to: {output_feminine}")
print(f"Masculine translations saved to: {output_masculine}")

