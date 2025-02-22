# This is an abstract example demonstrating how to automate text translation using Selenium.
# It uses an abstract URL and XPath elements as placeholders.
# Replace the URL and XPath with the actual elements from the translation service you plan to use.
# Ensure that automating translations does not violate the terms of service or licensing agreements of the translation service.

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Paths relative to the repository root
repo_path = os.path.dirname(os.path.abspath(__file__))
chunk_folder = os.path.join(repo_path, "..", "data_preprocessing", "chunks-context")
output_folder = os.path.join(repo_path, "..", "..", "data", "translations", "results-context")
driver_path = os.path.join(repo_path, "..", "..", "chromedriver.exe")

# Selenium setup (abstract example)
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.get("https://example.com/translate")  # Abstract URL for demonstration

def translate_text_example(text):
    try:
        # Wait for the input text box to be present
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="inputArea"]'))  # Abstract XPath
        )
        input_box.clear()
        input_box.send_keys(text)

        # Click the translate button (abstract XPath)
        translate_button = driver.find_element(By.XPATH, '//button[@id="translateButton"]')
        translate_button.click()

        previous_translation = ""
        translation = ""
        
        # Wait for translation to appear or change, retrying several times
        for _ in range(20):  # Retry up to 20 times
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

        return translation

    except Exception as e:
        print(f"Error during translation: {e}")
        return "Translation error"


def process_chunk(chunk_file, output_file):
    if os.path.exists(output_file):
        print(f"File {output_file} already processed, skipping...")
        return

    # Loading chunk data
    with open(chunk_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]

    translations = []

    start_time = time.time()
    print(f"Starting file processing: {chunk_file}")

    # Translating each sentence
    for index, line in enumerate(lines):
        translation = translate_text_example(line)
        translations.append(f"{line}\t{translation}")
        print(f"Translated ({index + 1}/{len(lines)}): {line} -> {translation}")
        time.sleep(2)  # Pause between requests

    # Saving translations to a file with a tab separator
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write("Original\tTranslation\n")
        f_out.write("\n".join(translations))

    elapsed = time.time() - start_time
    print(f"File {chunk_file} processed in {elapsed // 60:.0f} minutes. Result saved to {output_file}.")


# Main process handling all chunk files
if __name__ == "__main__":
    # Ensure the results folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Sorting chunk files
    chunk_files = sorted(
        [os.path.join(chunk_folder, f) for f in os.listdir(chunk_folder) if f.startswith("chunk_") and f.endswith(".csv")],
        key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split("_")[1])
    )

    # Processing each chunk file
    for chunk_file in chunk_files:
        output_file = os.path.join(output_folder, f"result_{os.path.basename(chunk_file)}")
        process_chunk(chunk_file, output_file)

    # Closing the browser after completion
    driver.quit()
    print("Processing completed.")
