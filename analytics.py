import requests
import subprocess
from pathlib import Path
import os

# Constants
BASE_DIRECTORY = Path(__file__).resolve().parent

DOWNLOADED_FILE_NAME = 'downloaded_file.pdf'
PDF_TO_TEXT_FILE_NAME = 'pdf_to_txt.txt'
DOWNLOADED_FILE_PATH = os.path.join(BASE_DIRECTORY, DOWNLOADED_FILE_NAME)
PDF_TO_TEXT_FILE_PATH = os.path.join(BASE_DIRECTORY, PDF_TO_TEXT_FILE_NAME)

# URL of the file to be downloaded
url = 'https://arxiv.org/ftp/arxiv/papers/2104/2104.05314.pdf'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Open a local file with 'wb' (write binary) permission.
    with open(DOWNLOADED_FILE_PATH, 'wb') as file:
        file.write(response.content)
    print("Download complete!")
else:
    print("Failed to download the file.")

# ebook-convert test.pdf test.txt
result = subprocess.run(['ebook-convert', DOWNLOADED_FILE_PATH, PDF_TO_TEXT_FILE_PATH], capture_output=True, text=True)
print(result.stdout)

# URL from the curl command
url = 'http://23.118.220.180:11434/api/generate'

# Read the contents of the file 'test.txt'
with open(PDF_TO_TEXT_FILE_PATH, 'r') as file:
    file_contents = file.read()

# Prepare the JSON data payload
data = {
    "model": "mixtral",
    "prompt": f"Can you summarize this paper in one bullet point? {file_contents}",
    "stream": False
}

# Make the POST request
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    print("Success!")
    print(response.json())  # Assuming the response is JSON, adjust if needed
else:
    print("Error:", response.status_code)
    print(response.text)
