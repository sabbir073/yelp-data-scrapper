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
yelp_scraper/
├── app/
│   ├── chrome_control.py       # Selenium setup and browser control
│   ├── yelp_scraper.py         # Main Yelp scraping logic
│   ├── selectors.py            # XPath/CSS selectors
│   ├── parsers.py              # Data extraction and parsing
│   ├── sheets.py               # Google Sheets integration
│   ├── utils.py                # Utility functions (delays, screenshots, etc.)
│   ├── config.py               # Environment configuration
│   └── main.py                 # Entry point
├── credentials/
│   └── service_account.json    # Google Sheets API credentials
├── .env                        # Environment variables (create from env.example)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd yelp_scraper
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

Edit the `.env` file to customize the scraper behavior:

```env
# Google Sheets Configuration
GOOGLE_SHEET_NAME=Yelp Scraper
INPUT_WORKSHEET_NAME=input
OUTPUT_WORKSHEET_NAME=output
CREDENTIALS_PATH=credentials/service_account.json

# Selenium Configuration
CHROME_HEADLESS=False
CHROME_USER_AGENT=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...

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

2. **Run the scraper**
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
   - Review selectors in `app/selectors.py`

### Debugging

- Enable screenshots by calling `take_screenshot()` in the code
- Check the console output for detailed error messages
- Use `CHROME_HEADLESS=False` to see the browser in action

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Disclaimer

This tool is for educational purposes only. Please respect Yelp's Terms of Service and robots.txt file. Use responsibly and consider implementing rate limiting for production use. 