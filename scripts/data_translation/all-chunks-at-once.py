import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Abstract example demonstrating automated translation using Selenium.
# Replace URL and XPath elements with actual elements from a translation service you have permission to automate.
# Ensure that automating translations does NOT violate the service's terms of service or licensing agreements.

# Paths relative to the repository root
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
chunk_folder = os.path.join(repo_path, "scripts", "data_preprocessing", "chunks-counter")
output_folder = os.path.join(repo_path, "data", "translations", "results-counter")
driver_path = os.path.join(repo_path, "chromedriver.exe")
pause_between_requests = 2  # Pause between translation requests (in seconds)

# Selenium Setup (Abstract Example)
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.get("https://example.com/translate")  # Abstract URL for demonstration


def process_chunk(chunk_file, output_file):
    if os.path.exists(output_file):
        print(f"File {output_file} already processed, skipping...")
        return

    # Load chunk data
    data = pd.read_csv(chunk_file)
    translations = []

    start_time = time.time()
    print(f"Start processing file: {chunk_file}")

    # Translate each sentence
    for index, row in data.iterrows():
        text = row["Text"]

        try:
            # Wait for input box
            input_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="inputArea"]'))  # Abstract XPath
            )
            input_box.clear()
            time.sleep(1)

            # Enter text
            input_box.send_keys(text)

            # Click translate button
            translate_button = driver.find_element(By.XPATH, '//button[@id="translateButton"]')  # Abstract XPath
            translate_button.click()

            # Wait for translation
            previous_translation = ""
            for _ in range(20):
                time.sleep(1)
                output_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@id="outputArea"]'))  # Abstract XPath
                )
                translation = output_box.text.strip()
                if translation and translation != previous_translation:
                    break
                previous_translation = translation
            else:
                print(f"Translation did not update for text: {text}")
                translations.append("Translation error")
                continue

            translations.append(translation)
            print(f"Translated: {text} -> {translation}")

            # Pause between requests
            time.sleep(pause_between_requests)

        except Exception as e:
            print(f"Error translating line {index}: {e}")
            translations.append("Translation error")

    # Save translations
    data["Translated_Text"] = translations
    data.to_csv(output_file, index=False, encoding="utf-8")

    elapsed = time.time() - start_time
    print(f"File {chunk_file} processed in {elapsed // 60:.0f} minutes. Result saved in {output_file}.")


# Main processing loop
if __name__ == "__main__":
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get list of chunk files
    chunk_files = sorted(
        [os.path.join(chunk_folder, f) for f in os.listdir(chunk_folder) if f.startswith("chunk_") and f.endswith(".csv")],
        key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split("_")[1])
    )

    for i, chunk_file in enumerate(chunk_files):
        output_file = os.path.join(output_folder, f"result_{i}.csv")

        if os.path.exists(output_file):
            print(f"File {output_file} already processed, skipping...")
            continue

        process_chunk(chunk_file, output_file)

    driver.quit()
    print("Processing completed.")
