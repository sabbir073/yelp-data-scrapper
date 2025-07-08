import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Sheets Configuration
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'Yelp Scraper')
INPUT_WORKSHEET_NAME = os.getenv('INPUT_WORKSHEET_NAME', 'input')
OUTPUT_WORKSHEET_NAME = os.getenv('OUTPUT_WORKSHEET_NAME', 'output')
CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH', 'credentials/service_account.json')

# Selenium Configuration
CHROME_HEADLESS = os.getenv('CHROME_HEADLESS', 'False').lower() == 'true'
CHROME_USER_AGENT = os.getenv('CHROME_USER_AGENT', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

# Scraping Configuration
DEFAULT_WAIT_TIME = int(os.getenv('DEFAULT_WAIT_TIME', '5'))
PAGE_LOAD_WAIT = int(os.getenv('PAGE_LOAD_WAIT', '8'))
TAB_SWITCH_WAIT = int(os.getenv('TAB_SWITCH_WAIT', '4'))
MAX_PAGES = int(os.getenv('MAX_PAGES', '10'))  # Maximum pages to scrape per search

# Yelp Configuration
YELP_BASE_URL = 'https://www.yelp.com' 