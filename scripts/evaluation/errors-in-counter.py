# This script uses the 'accuracy_metric' file, which is licensed under the Creative Commons Attribution-ShareAlike 3.0 License.

import csv
from accuracy_metric import accuracy_metric
import os

# Define repository root dynamically
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

masculine_reference_path = os.path.join(repo_path, "data", "sentences", "test", "geneval-sentences-masculine-test.en_ru.ru")
feminine_reference_path = os.path.join(repo_path, "data", "sentences", "test", "geneval-sentences-feminine-test.en_ru.ru")
masculine_hypothesis_path = os.path.join(repo_path, "data", "translations", "results-counter", "hyp_masculine_ru.txt")
feminine_hypothesis_path = os.path.join(repo_path, "data", "translations", "results-counter", "hyp_feminine_ru.txt")
csv_report_path = os.path.join(repo_path, "data", "translations", "results-counter", "counterfactual_error_report.csv")

# Reading files for subsequent analysis
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]

# Performing analysis for the male set
_, metric_decisions_masculine = accuracy_metric(
    masculine_hypothesis_path, masculine_reference_path, feminine_reference_path
)

# Performing analysis for the female set
_, metric_decisions_feminine = accuracy_metric(
    feminine_hypothesis_path, feminine_reference_path, masculine_reference_path
)

# Detecting errors
errors = []
masculine_texts = read_file(masculine_reference_path)
feminine_texts = read_file(feminine_reference_path)
masculine_hypotheses = read_file(masculine_hypothesis_path)
feminine_hypotheses = read_file(feminine_hypothesis_path)

for idx, (decision_m, decision_f) in enumerate(zip(metric_decisions_masculine, metric_decisions_feminine)):
    if decision_m == "Incorrect" or decision_f == "Incorrect":
        errors.append({
            "index": idx,
            "masculine_original": masculine_texts[idx],
            "feminine_original": feminine_texts[idx],
            "masculine_translation": masculine_hypotheses[idx],
            "feminine_translation": feminine_hypotheses[idx],
            "masculine_decision": decision_m,
            "feminine_decision": decision_f,
        })

# Saving the error report to CSV
with open(csv_report_path, 'w', encoding='utf-8', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=[
        "Index", "Masculine Original", "Feminine Original",
        "Masculine Translation", "Feminine Translation",
        "Masculine Decision", "Feminine Decision"
    ])
    writer.writeheader()
    for error in errors:
        writer.writerow({
            "Index": error['index'],
            "Masculine Original": error['masculine_original'],
            "Feminine Original": error['feminine_original'],
            "Masculine Translation": error['masculine_translation'],
            "Feminine Translation": error['feminine_translation'],
            "Masculine Decision": error['masculine_decision'],
            "Feminine Decision": error['feminine_decision']
        })

# Output the result
print(f"Analysis completed. Errors found: {len(errors)}. The report is saved in {csv_report_path}.")
