import os
import re
import requests
import subprocess
import pprint


def split_contentdisposition(astring):
    # return the stuff after = sign
    value = astring.split("=")[-1]
    return re.sub(r'[^A-Za-z0-9-_\.]', '', value)

def download_and_convert(download_directory, pdf_url):

    downloadfilename = os.path.join(download_directory,"downloaded_file.pdf")
    convertedfilename = os.path.join(download_directory,"pdf_to_text.txt")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Send a GET request to the URL
    response = requests.get(pdf_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code in [200] :
        if 'Content-Disposition' in response.headers:
            header = response.headers['Content-Disposition']
            print("content-disposition is "+header)
            content_disposition = split_contentdisposition(header)
            downloadfilename = os.path.join(download_directory,content_disposition)
        with open(downloadfilename, 'wb') as file:
            file.write(response.content)
        print(f"successfully downloaded {pdf_url} to {downloadfilename}")
    else:
        print("error downloading "+pdf_url)
    
    # result = subprocess.run(['ebook-convert', downloadfilename, convertedfilename], capture_output=True, text=True)
    # print(result.stdout)
    
    return downloadfilename, convertedfilename 

    
def analyze_with_mixtral(download_directory): 

    # URL from the curl command
    url = 'http://23.118.220.180:11434/api/generate'
    convertedfilename = os.path.join(download_directory,"pdf_to_text.txt")
    pdfsummary = os.path.join(download_directory,"pdf_summary.txt")
    promptcommand = "Can you summarize this paper in one paragraph?"
    # Read the contents of the file 'test.txt'
    with open(convertedfilename, 'r') as file:
        file_contents = file.read()

    # Prepare the JSON data payload
    data = {
        "model": "mixtral",
        "prompt": f"{promptcommand} {file_contents}",
        "stream": False
    }
    
    # Make the POST request
    response = requests.post(url, json=data)
    
    # Check the response
    if response.status_code == 200:
        print("Success!")
        responsejson = response.json()
        context = responsejson['context']
        summary = responsejson['response']
        with open(pdfsummary, 'w') as file:
            file.write(summary)
        print(f"successfully summarized {convertedfilename} to {pdfsummary}") 
    else:
        raise requests.HTTPError("error generating "+pdfsummary)



def scrape_from_alex(download_directory:str, results_per_page:str):
    import requests
    from datetime import datetime
    import json

    #make download directory if missing
    if not os.path.exists(download_directory):
        os.mkdir(download_directory)

    date_string = '2024-01-10'
    per_page = results_per_page
    # Make the GET request
    response = requests.get(f"https://api.openalex.org/works?sort=cited_by_count:desc\&filter=fulltext.search:artificial%20intelligence,primary_location.is_oa:True,from_publication_date:{date_string}&per-page={per_page}")
    print(response.url)
    
    # Check if the request was successful
    if response.status_code == 200:
        replyjson = response.json()
        meta = replyjson['meta']
        pprint.pprint(meta)
        results = replyjson['results']
        with open('latest_oa_ai_works.txt', 'w') as file:
            for result in results: 
                pdf_url = result['best_oa_location']['pdf_url']
                landing_url = result["primary_location"]["landing_page_url"]
                id = result['id']
                print(id,pdf_url, landing_url)
                print(id,pdf_url, landing_url, file=file)
                if pdf_url:
                    download_and_convert(download_directory,pdf_url)
                    
    else:
        print(f"Failed to fetch data: HTTP {response.status_code}")


