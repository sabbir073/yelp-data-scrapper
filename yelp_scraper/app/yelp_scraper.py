import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .chrome_control import setup_driver, wait_for_element, safe_click, switch_to_new_tab, close_current_tab
from .yelp_selectors import *
from .parsers import parse_business_data
from .utils import random_delay, human_like_delay, clear_input_field, wait_for_page_load, handle_captcha
from .config import YELP_BASE_URL, DEFAULT_WAIT_TIME, PAGE_LOAD_WAIT, TAB_SWITCH_WAIT, MAX_PAGES

def perform_search(driver, keyword, location):
    """
    Perform a search on Yelp with the given keyword and location
    """
    try:
        driver.get(YELP_BASE_URL)
        time.sleep(DEFAULT_WAIT_TIME)
        
        # Wait for search elements to be present
        search_desc = wait_for_element(driver, SEARCH_DESCRIPTION_INPUT)
        search_loc = wait_for_element(driver, SEARCH_LOCATION_INPUT)
        
        if not search_desc or not search_loc:
            print("❌ Search elements not found")
            return False
        
        # Fill in search inputs
        clear_input_field(driver, search_desc)
        search_desc.send_keys(keyword)
        random_delay(0.5, 1)
        
        clear_input_field(driver, search_loc)
        search_loc.send_keys(location)
        random_delay(0.5, 1)
        
        # Dismiss autofill dropdown if present
        search_loc.send_keys(Keys.TAB)
        random_delay(0.5, 1)
        
        # Submit search
        search_loc.send_keys(Keys.ENTER)
        
        # Wait for search results to load
        time.sleep(PAGE_LOAD_WAIT)
        
        # Check if we got redirected to a different page
        current_url = driver.current_url
        print(f"Current URL after search: {current_url}")
        
        if "search" not in current_url.lower():
            print("⚠️  Detected potential redirect, attempting to continue...")
            time.sleep(3)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during search: {e}")
        return False

def find_business_listings(driver):
    """
    Find business listings on the current page
    """
    listings = []
    
    for selector in BUSINESS_LISTING_SELECTORS:
        try:
            listings = driver.find_elements(By.XPATH, selector)
            if listings:
                print(f"🔎 Found {len(listings)} listings using selector: {selector}")
                return listings, selector
        except:
            continue
    
    return [], None

def scrape_business_page(driver, business_url):
    """
    Scrape data from a single business page
    """
    try:
        print(f"📄 Opening: {business_url}")
        driver.execute_script("window.open(arguments[0]);", business_url)
        
        if not switch_to_new_tab(driver, TAB_SWITCH_WAIT):
            return None
        
        # Wait for page to load
        wait_for_page_load(driver)
        
        # Check for CAPTCHA
        if handle_captcha(driver):
            # Wait a bit more after CAPTCHA
            time.sleep(3)
        
        # Parse business data
        data = parse_business_data(driver, business_url)
        
        print(f"✅ Scraped: {data['Title']}")
        
        # Close tab and return to main tab
        close_current_tab(driver, switch_to_main=True)
        random_delay(1, 2)
        
        return data
        
    except Exception as e:
        print(f"❌ Error processing business page: {e}")
        # Try to close any open tabs and return to main
        try:
            if len(driver.window_handles) > 1:
                close_current_tab(driver, switch_to_main=True)
        except:
            pass
        return None

def find_next_page(driver):
    """
    Find and click the next page button
    """
    for selector in NEXT_PAGE_SELECTORS:
        try:
            next_button = driver.find_element(By.XPATH, selector)
            if next_button.is_enabled() and next_button.is_displayed():
                print(f"➡️  Found next page button: {selector}")
                if safe_click(driver, next_button, delay=2):
                    time.sleep(PAGE_LOAD_WAIT)
                    return True
        except:
            continue
    
    return False

def scrape_yelp_all_pages(driver, keyword, location):
    """
    Scrape all pages of Yelp search results
    """
    # Perform initial search
    if not perform_search(driver, keyword, location):
        return []
    
    all_results = []
    page_num = 1
    
    while page_num <= MAX_PAGES:
        print(f"\n📄 Processing page {page_num}...")
        
        # Check for CAPTCHA
        if handle_captcha(driver):
            time.sleep(3)
        
        # Find business listings on current page
        listings, selector = find_business_listings(driver)
        
        if not listings:
            print(f"❌ No business listings found on page {page_num}")
            break
        
        # Process listings on current page
        page_results = []
        for i in range(len(listings)):
            # Re-fetch list to avoid stale references
            listings = driver.find_elements(By.XPATH, selector)
            if i >= len(listings):
                break
            
            try:
                link = listings[i].get_attribute("href")
                if not link or "yelp.com/biz/" not in link:
                    continue
                
                # Scrape business data
                data = scrape_business_page(driver, link)
                if data:
                    page_results.append(data)
                
            except Exception as e:
                print(f"❌ Error processing listing {i} on page {page_num}: {e}")
                continue
        
        # Add page results to all results
        all_results.extend(page_results)
        print(f"✅ Completed page {page_num} with {len(page_results)} results")
        
        # Check for next page
        if not find_next_page(driver):
            print(f"🏁 No more pages found. Reached the end at page {page_num}")
            break
        
        page_num += 1
        human_like_delay()
    
    print(f"🎉 Total results collected: {len(all_results)}")
    return all_results 