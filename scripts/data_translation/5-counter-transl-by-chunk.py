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
        print(f"File {output_file} has already been processed, skipping...")
        return

    # Loading chunk data
    data = pd.read_csv(chunk_file)
    translations = []
    total_texts = len(data)

    start_time = time.time()
    print(f"Start processing file: {chunk_file}")

    # Translating each sentence
    for index, row in data.iterrows():
        text = row["Text"]

        try:
            # Wait for input box
            input_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="inputArea"]'))  # Abstract XPath
            )

            # Clear input field
            input_box.clear()
            time.sleep(1)  # Allow time for clearing

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
                translation = "Translation error"

            translations.append(translation)

            # Display progress
            elapsed = time.time() - start_time
            remaining_time = (elapsed / (index + 1)) * (total_texts - (index + 1))
            print(
                f"Progress: {index + 1}/{total_texts}. Elapsed: {elapsed // 60:.0f} min. Remaining: {remaining_time // 60:.0f} min.")

            # Pause between requests
            time.sleep(pause_between_requests)

        except Exception as e:
            print(f"Error translating line {index}: {e}")
            translations.append("Translation error")

    # Save translations to DataFrame and file
    data["Translated_Text"] = translations
    data.to_csv(output_file, index=False, encoding="utf-8")

    total_elapsed = time.time() - start_time
    print(f"File {chunk_file} processed in {total_elapsed // 60:.0f} minutes. Result saved in {output_file}.")


# Main processing routine
if __name__ == "__main__":
    # Ensure the results folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get the list of chunk files
    chunk_files = sorted(
        [os.path.join(chunk_folder, f) for f in os.listdir(chunk_folder) if
         f.startswith("counter_chunk_") and f.endswith(".csv")],
        key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split("_")[-1])
    )

    # Ask user to specify the chunk number
    try:
        chunk_number = int(input(f"Enter the chunk number (from 0 to {len(chunk_files) - 1}): "))
        if chunk_number < 0 or chunk_number >= len(chunk_files):
            print("Invalid chunk number.")
            driver.quit()
            exit()

        # Process the specified chunk
        chunk_file = chunk_files[chunk_number]
        output_file = os.path.join(output_folder, f"result_{chunk_number}.csv")
        process_chunk(chunk_file, output_file)

    except ValueError:
        print("Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Close browser after completion
    driver.quit()
    print("Processing completed.")
