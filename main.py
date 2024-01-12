import logging
import analytics
from text_extractor import *
from analytics import *

# Set logging level to INFO, ERROR, DEBUG
logginglevel= "DEBUG"
downloadfolder = r"downloads"

logging.basicConfig(level=logginglevel,filename='debug.log')

# Scrape from OpenAlex up to 25 papers
analytics.scrape_from_alex(downloadfolder, "25")
logging.debug('Completed AnalyticsScrapeFromAlex')

# convert pdfs to text
# analytics.download_and_convert(downloadfolder, "https://api.openalex.org/works")
# logging.debug('Completed AnalyticsDownloadAndConvert')

# Send to Mixtral for summarization
analytics.analyze_with_mixtral(downloadfolder)
logging.debug('Completed analyze_with_mixtral')