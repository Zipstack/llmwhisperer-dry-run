import sys
import os
import glob
import time
from dotenv import load_dotenv
from unstract.llmwhisperer.client import LLMWhispererClient, LLMWhispererClientException

EXTRACTION_MODE = "text"

def error_exit(error_message):
    print(error_message)
    sys.exit(1)

def get_files_to_process(path):
    try:
        files = []
        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            clean_path = path if path.endswith('/') else path + '/'
            for f in glob.iglob(clean_path + '*.pdf', recursive=False):
                files.append(f)
        return files
    except Exception as e:
        error_exit(e)

def extract_text_from_file(file_path, pages_list=None):
    llmw = LLMWhispererClient()
    try:
        result = llmw.whisper(
            file_path=file_path,
            processing_mode=EXTRACTION_MODE,
            force_text_processing=True,
            pages_to_extract=pages_list,
            timeout=2
        )
        print(f"LLMWhisperer status code: {result["status_code"]}")
        if result["status_code"] == 200:
            extracted_text = result["extracted_text"]
            return extracted_text
        if result["status_code"] == 202:
            print("Timeout occurred. Whisper request accepted.")
            print(f"Whisper hash: {result['whisper-hash']}")
            while True:
                print("Polling for whisper status...")
                status = llmw.whisper_status(whisper_hash=result["whisper-hash"])
                if status["status"] == "processing":
                    print("STATUS: processing...")
                elif status["status"] == "delivered":
                    print("STATUS: Already delivered!")
                    break
                elif status["status"] == "unknown":
                    print("STATUS: unknown...")
                    break
                elif status["status"] == "processed":
                    print("STATUS: processed!")
                    print("Let's retrieve the result of the extraction...")
                    resultx = llmw.whisper_retrieve(
                        whisper_hash=result["whisper-hash"]
                    )
                    return resultx["extracted_text"]
                time.sleep(2)
    except LLMWhispererClientException as e:
        error_exit(e)

def save_text_to_file(text, file_path, file_name):
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(file_path + "/" + file_name, "w") as text_file:
            text_file.write(text)
    except Exception as e:
        error_exit(e)

def main():
    load_dotenv()
    if len(sys.argv) < 2:
        error_exit("No file or directory name provided")

    files = get_files_to_process(sys.argv[1])
    for file in files:
        print(f"Extracting text from {file}...")
        extracted_text = extract_text_from_file(file)
        # extracted_text = "This is a test text extracted from a PDF file."
        file_path = os.path.dirname(file) + "/extracted_text"
        save_text_to_file(extracted_text, file_path, os.path.basename(file) + ".txt")

if __name__ == "__main__":
    main()
