import pprint
import polars as pl
import requests

from datetime import datetime, timedelta
yesterday = datetime.now() - timedelta(1)
date_string = datetime.strftime(yesterday, '%Y-%m-%d')

PER_PAGE = 100
OPEN_ALEX_WORKS_URL = 'https://api.openalex.org/works'
SORT_STRING = 'cited_by_count:desc'
TOPIC_STRING = 'artificial%20intelligence'
FILTER_SRING = f"fulltext.search:{TOPIC_STRING},primary_location.is_oa:True,from_publication_date:{date_string}"
# Make the GET request
response = requests.get(f"{OPEN_ALEX_WORKS_URL}?sort={SORT_STRING}\&filter={FILTER_SRING}&per-page={PER_PAGE}")
print(response.url)

# Check if the request was successful
if response.status_code == 200:
    replyjson = response.json()
    meta = replyjson['meta']
    pprint.pprint(meta)
    results = replyjson['results']

    top_keys = ['id', 'title']
    best_loc_keys = ['pdf_url','landing_page_url']
    data = {k: [] for k in top_keys+best_loc_keys}
    for result in results: 
        for k in top_keys:
            data[k].append(result[k])
        for k in best_loc_keys:
            data[k].append(result['best_oa_location'][k])
else:
    print(f"Failed to fetch data: HTTP {response.status_code}")

df = pl.DataFrame(data)

df.write_csv('latest_oa_ai_works.csv')