import requests
import subprocess

# URL of the file to be downloaded
url = 'https://arxiv.org/ftp/arxiv/papers/2104/2104.05314.pdf'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Open a local file with 'wb' (write binary) permission.
    with open('/home/rob/Documents/downloaded_file.pdf', 'wb') as file:
        file.write(response.content)
    print("Download complete!")
else:
    print("Failed to download the file.")


#ebook-convert test.pdf test.txt
result = subprocess.run(['ebook-convert', '/home/rob/Documents/downloaded_file.pdf', '/home/rob/Documents/pdf_to_txt.txt'], capture_output=True, text=True)
print(result.stdout)

# URL from the curl command
url = 'http://23.118.220.180:11434/api/generate'

# Read the contents of the file 'test.txt'
with open('/home/rob/Documents/pdf_to_txt.txt', 'r') as file:
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