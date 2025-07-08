from fastapi import FastAPI, BackgroundTasks, Query
from pydantic import BaseModel
from typing import List, Optional
import threading
from .main import main as run_full_scrape
from .sheets import read_input_sheet, write_to_output_sheet
from .yelp_scraper import scrape_yelp_all_pages
from .chrome_control import setup_driver
from .utils import deduplicate_results

app = FastAPI(title="Yelp Scraper API")

# In-memory storage for results (for demo; use DB for production)
SCRAPE_RESULTS = []
SCRAPE_STATUS = {"running": False, "message": "Idle"}

class ScrapeRequest(BaseModel):
    keyword: Optional[str] = None
    location: Optional[str] = None
    max_pages: Optional[int] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/results")
def get_results():
    return {"count": len(SCRAPE_RESULTS), "results": SCRAPE_RESULTS}

@app.get("/status")
def get_status():
    return SCRAPE_STATUS

@app.post("/scrape")
def start_scrape(
    background_tasks: BackgroundTasks,
    req: ScrapeRequest
):
    if SCRAPE_STATUS["running"]:
        return {"status": "busy", "message": SCRAPE_STATUS["message"]}
    SCRAPE_STATUS["running"] = True
    SCRAPE_STATUS["message"] = "Scraping in progress..."
    background_tasks.add_task(scrape_task, req)
    return {"status": "started", "message": "Scraping started in background."}

def scrape_task(req: ScrapeRequest):
    global SCRAPE_RESULTS
    try:
        driver = setup_driver()
        all_results = []
        if req.keyword and req.location:
            # Scrape for a single keyword/location
            results = scrape_yelp_all_pages(driver, req.keyword, req.location)
            all_results.extend(results)
        else:
            # Scrape for all from Google Sheets
            rows = read_input_sheet()
            for row in rows:
                keyword = row.get("keyword", "")
                location = row.get("location", "")
                if not keyword or not location:
                    continue
                results = scrape_yelp_all_pages(driver, keyword, location)
                all_results.extend(results)
        unique_results = deduplicate_results(all_results, key="ID")
        SCRAPE_RESULTS.clear()
        SCRAPE_RESULTS.extend(unique_results)
        write_to_output_sheet(unique_results)
        SCRAPE_STATUS["message"] = f"Scraping complete. {len(unique_results)} unique results."
    except Exception as e:
        SCRAPE_STATUS["message"] = f"Error: {e}"
    finally:
        SCRAPE_STATUS["running"] = False
        try:
            driver.quit()
        except:
            pass 