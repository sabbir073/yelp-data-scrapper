# Yelp Scraper

A modular, configurable web scraper for extracting business information from Yelp. The scraper reads search parameters from Google Sheets and writes results back to the same sheet.

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **Multi-page Scraping**: Automatically scrapes all available pages of search results
- **Anti-Detection**: Built-in measures to avoid bot detection
- **Google Sheets Integration**: Read search parameters and write results directly to Google Sheets
- **Configurable**: Environment-based configuration for easy customization
- **Error Handling**: Robust error handling and recovery mechanisms
- **CAPTCHA Detection**: Automatic CAPTCHA detection with manual intervention

## Project Structure

```
Yelp-Scraper/
├── app/
│   ├── chrome_control.py       # Selenium setup and browser control
│   ├── yelp_scraper.py         # Main Yelp scraping logic
│   ├── yelp_selectors.py       # XPath/CSS selectors
│   ├── parsers.py              # Data extraction and parsing
│   ├── sheets.py               # Google Sheets integration
│   ├── utils.py                # Utility functions (delays, screenshots, etc.)
│   ├── config.py               # Environment configuration
│   ├── main.py                 # CLI entry point
│   ├── api.py                  # FastAPI endpoints
│   └── main_api.py             # FastAPI entry point
├── credentials/
│   └── service_account.json    # Google service account credentials
├── .env                        # Environment variables (create from env.example)
├── env.example                 # Example environment file
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd Yelp-Scraper
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets API**
   - Create a Google Cloud project
   - Enable Google Sheets API and Google Drive API
   - Create a Service Account and download the JSON credentials
   - Place the credentials file in `credentials/service_account.json`

4. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your specific configuration
   ```

5. **Set up Google Sheet**
   - Create a Google Sheet named "Yelp Scraper" (or change in .env)
   - Add a worksheet named "input" with columns: `keyword` and `location`
   - Share the sheet with your Service Account email

## Configuration

Edit the `.env` file at the project root to customize the scraper behavior:

```env
# Google Sheets Configuration
GOOGLE_SHEET_NAME=Yelp Scraper
INPUT_WORKSHEET_NAME=input
OUTPUT_WORKSHEET_NAME=output
CREDENTIALS_PATH=credentials/service_account.json

# Selenium Configuration
CHROME_HEADLESS=False
CHROME_USER_AGENT_MAC=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
CHROME_USER_AGENT_WINDOWS=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
CHROME_USER_AGENT=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36

# Scraping Configuration
DEFAULT_WAIT_TIME=5
PAGE_LOAD_WAIT=8
TAB_SWITCH_WAIT=4
MAX_PAGES=10
```

## Usage

1. **Prepare your input data**
   - Fill the "input" worksheet with search keywords and locations
   - Example:
     ```
     keyword          | location
     restaurants      | San Francisco, CA
     coffee shops     | New York, NY
     ```

2. **Run the scraper (CLI)**
   ```bash
   python app/main.py
   ```

3. **Check results**
   - Results will be written to the "output" worksheet
   - Each run appends new results to existing data

## Output Format

The scraper extracts the following data for each business:

| Field | Description |
|-------|-------------|
| ID | Unique Yelp business identifier |
| Title | Business name |
| Description | Business categories |
| Website | Business website URL |
| Phone | Phone number |
| Rating | Star rating |
| Reviews | Number of reviews |
| Address | Business address |
| Hours | Operating hours |

## Advanced Features

### Anti-Detection Measures
- Random delays between actions
- Human-like typing simulation
- Browser fingerprint masking
- User agent rotation

### Error Handling
- Automatic retry mechanisms
- Graceful handling of missing elements
- CAPTCHA detection and manual intervention
- Screenshot capture for debugging

### Pagination
- Automatic detection of next page buttons
- Configurable maximum pages per search
- Progress tracking and reporting

## Troubleshooting

### Common Issues

1. **"No search parameters found"**
   - Check that your input worksheet has data
   - Verify column names are exactly "keyword" and "location"

2. **"Error authenticating with Google Sheets"**
   - Ensure credentials file is in the correct location
   - Verify Service Account has access to the Google Sheet

3. **"Chrome driver not found"**
   - Install ChromeDriver matching your Chrome version
   - Add ChromeDriver to your system PATH

4. **"No business listings found"**
   - Yelp may have changed their HTML structure
   - Check if you're being blocked (try with VPN)
   - Review selectors in `app/yelp_selectors.py`

### Debugging

- Enable screenshots by calling `take_screenshot()` in the code
- Check the console output for detailed error messages
- Use `CHROME_HEADLESS=False` to see the browser in action

## Troubleshooting: Stopping the FastAPI Server & Address Already in Use

If you see an error like:

```
ERROR:    [Errno 48] Address already in use
```

This means the server is already running or another process is using port 8000.

### How to Stop the Server
- If you started the server in a terminal, **press `Ctrl+C`** in that terminal to stop it.

### If the Error Persists
1. **Find the process using port 8000:**
   ```bash
   lsof -i :8000
   ```
   - Look for the `PID` (process ID) in the output.

2. **Kill the process:**
   ```bash
   kill <PID>
   ```
   Replace `<PID>` with the actual number from the previous step.

3. **Try running the server again:**
   ```bash
   uvicorn app.api:app --reload
   ```

---

## Running the FastAPI API Server

To use the Yelp Scraper as a web API, follow these steps:

### On macOS/Linux
1. **Activate your virtual environment** (if you have one):
   ```bash
   source venv/bin/activate
   ```
2. **Install dependencies** (if not already done):
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the FastAPI server** from your project root:
   ```bash
   uvicorn app.api:app --reload
   ```
   - The `--reload` flag auto-restarts the server on code changes (useful for development).

### On Windows
1. **Activate your virtual environment** (if you have one):
   ```bat
   venv\Scripts\activate
   ```
2. **Install dependencies** (if not already done):
   ```bat
   pip install -r requirements.txt
   ```
3. **Start the FastAPI server** from your project root:
   ```bat
   uvicorn app.api:app --reload
   ```

4. **Open your browser to the API docs:**
   [http://localhost:8000/docs](http://localhost:8000/docs)
   - This is the interactive Swagger UI where you can test all endpoints.

5. **Available Endpoints:**
   - `GET /health` — Health check
   - `POST /scrape` — Start a scrape (optionally with keyword/location)
   - `GET /results` — Get the latest results
   - `GET /status` — Get scrape status

6. **Example: Start a Scrape via Swagger UI**
   - Go to `/docs`
   - Click on `POST /scrape`
   - Click "Try it out"
   - Enter a JSON body, e.g.:
     ```json
     {
       "keyword": "Pasta",
       "location": "New York"
     }
     ```
   - Click "Execute"

7. **Stop the server**
   - Press `Ctrl+C` in the terminal where the server is running.

---

**Note:**
- You can also use tools like `curl` or Postman to interact with the API.
- The API will write results to your Google Sheet and return them via the `/results` endpoint. 