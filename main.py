import logging
import analytics
from datetime import datetime
from text_extractor import *
from analytics import *
import polars as pl

# Set logging level to INFO, ERROR, DEBUG
logginglevel= "DEBUG"
downloadfolder = r"downloads"
postprocessing = r"postprocessing"

current_date = datetime.now()
formatted_date = current_date.strftime("%Y-%m-%d")

logging.basicConfig(level=logginglevel,filename='debug.log')

# make necessary directories if missing
if not os.path.exists(downloadfolder):
    os.mkdir(downloadfolder)
if not os.path.exists(postprocessing):
    os.mkdir(postprocessing)

#List to store urls for PDFs

# Scrape from OpenAlex up to 25 papers
ScrapedList = analytics.scrape_from_alex("25", formatted_date)
logging.debug('Completed AnalyticsScrapeFromAlex')
print("returned " + str(ScrapedList.with_row_count()) + " from scrape")
has_pdf = ScrapedList.filter(
   ~pl.all_horizontal(pl.col('pdf_url').is_null())
)
print("returned " + str(has_pdf.with_row_count()) + " with pdf")

# Download from OpenAlex
ID_START = 21 # https://openalex.org/ is 21 chareacters long
for row in has_pdf.iter_rows(named=True):
    print(row['pdf_url'])
    analytics.download(row['pdf_url'], downloadfolder,row['id'][ID_START:])

# convert pdfs to text
counter = 0
for filename in os.listdir(downloadfolder):
    if filename.endswith(".pdf"):
        if filename.startswith("complete-"):
            continue

        counter += 1
        text_extractor = TextExtractor()
        input_path = os.path.join('downloads', filename)
        text_extractor.extract_text_from_pdf(input_path)
        text_extractor.save_txt(counter)

print("converted " + str(counter) + " pdfs to txt")
logging.debug('Completed AnalyticsDownloadAndConvert')

# Send to Mixtral for summarization
analytics.analyze_with_mixtral(postprocessing)
logging.debug('Completed analyze_with_mixtral')