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
summary_dir    = r"summaries"

current_date = datetime.now()
formatted_date = current_date.strftime("%Y-%m-%d")

logging.basicConfig(level=logginglevel,filename='debug.log')

# make necessary directories if missing
if not os.path.exists(downloadfolder):
    os.mkdir(downloadfolder)
if not os.path.exists(postprocessing):
    os.mkdir(postprocessing)
if not os.path.exists(summary_dir):
    os.mkdir(summary_dir)

#List to store urls for PDFs

# Scrape from OpenAlex up to 25 papers
ScrapedList = analytics.scrape_from_alex("25", formatted_date)
logging.debug('Completed AnalyticsScrapeFromAlex')
print("returned: \n" + str(ScrapedList.with_row_count()) + "\nfrom scrape")
has_pdf = ScrapedList.filter(
   ~pl.all_horizontal(pl.col('pdf_url').is_null())
)
# Saving this table because it could be useful for front-end UI
ScrapedList.write_csv(f"{formatted_date}_oa_ai_works.csv")
num_pdfs=has_pdf.select(pl.count())[0,0]
print(str(num_pdfs) + " have pdfs")

# Download from OpenAlex
ID_START = 21 # https://openalex.org/ is 21 chareacters long
for row in has_pdf.iter_rows(named=True):
    print(row['pdf_url'])
    analytics.download(row['pdf_url'], downloadfolder,row['id'][ID_START:])

# convert pdfs to text
PDF_LEN = 4
count = 0
for filename in os.listdir(downloadfolder):
    if filename.endswith(".pdf"):
        text_extractor = TextExtractor()
        input_path = os.path.join('downloads', filename)
        text_extractor.extract_text_from_pdf(input_path)
        text_extractor.save_txt(filename[:-PDF_LEN])
        count +=1

# count may not match number of pdfs because they may fail to be downloaded
print("converted " + str(count) + " pdfs to txt")
logging.debug('Completed AnalyticsDownloadAndConvert')

# only do 5 because of time contraints and mixtral's speed
to_sum = has_pdf.select(pl.head("id", 5)) 
# Send to Mixtral for summarization
for row in to_sum.iter_rows(named=True):
    analytics.analyze_with_mixtral(postprocessing,row['id'][ID_START:], summary_dir)
logging.debug('Completed analyze_with_mixtral')