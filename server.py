from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
import json
import csv

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # with open("data.json", "r") as data_file:
    #     data = json.load(data_file)
    # Read data from the CSV file
    def read_csv_data(file_path):
        data = []
        with open(file_path, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)
        return data

    data = read_csv_data("latest_oa_ai_works.csv")
    return templates.TemplateResponse("index.html", {"request": request, "items": data})


# Define a /summary endpoint
@app.get("/get_summary/{pdf_url}", response_class=HTMLResponse)
async def get_summary(request: Request, pdf_url: str):
    return templates.TemplateResponse(
        "summary.html", {"request": request, "pdf_url": pdf_url}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)