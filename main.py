import logging
import analytics
from datetime import datetime
from text_extractor import *
from analytics import *

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
print("returned " + str(len(ScrapedList)) + " from scrape")


# Download from OpenAlex
for url in ScrapedList:
    print(url)
    analytics.download(url, downloadfolder)

# convert pdfs to text
# analytics.download_and_convert(downloadfolder, "https://api.openalex.org/works")
# logging.debug('Completed AnalyticsDownloadAndConvert')

# Send to Mixtral for summarization
analytics.analyze_with_mixtral(downloadfolder)
logging.debug('Completed analyze_with_mixtral')