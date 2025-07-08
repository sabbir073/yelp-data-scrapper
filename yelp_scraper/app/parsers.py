import re
from urllib.parse import urlparse, parse_qs, unquote
from selenium.webdriver.common.by import By
from .yelp_selectors import *

def extract_business_id(url):
    """
    Extract unique business ID from Yelp business URL
    """
    if not url or "yelp.com/biz/" not in url:
        return ""
    match = re.search(r'/biz/([^/?#]+)', url)
    return match.group(1) if match else ''

def extract_real_website(yelp_href):
    """
    Extract the actual website URL from Yelp's redirect link
    """
    if not yelp_href:
        return ""
    try:
        parsed = urlparse(yelp_href)
        qs = parse_qs(parsed.query)
        url = qs.get("url", [""])[0]
        return unquote(url)
    except:
        return ""

def safe_text(driver, xpath):
    """
    Safely extract text from an element
    """
    try:
        element = driver.find_element(By.XPATH, xpath)
        return element.text.strip() if element.text else ""
    except:
        return ""

def safe_attr(driver, xpath, attr):
    """
    Safely extract attribute from an element
    """
    try:
        element = driver.find_element(By.XPATH, xpath)
        return element.get_attribute(attr) or ""
    except:
        return ""

def safe_list(driver, xpath):
    """
    Safely extract list of texts from multiple elements
    """
    try:
        elements = driver.find_elements(By.XPATH, xpath.replace('/text()', ''))
        if '/text()' in xpath:
            return [el.text.strip() for el in elements if el.text]
        else:
            return [el.text.strip() for el in elements if el.text]
    except:
        return []

def try_multiple_selectors(driver, selectors, attr=None):
    """
    Try multiple selectors and return the first successful result
    """
    for selector in selectors:
        try:
            if attr:
                result = safe_attr(driver, selector, attr)
            else:
                result = safe_text(driver, selector)
            if result:
                return result
        except:
            continue
    return ""

def parse_business_data(driver, business_url):
    """
    Parse all business data from a business detail page
    """
    # Extract business ID
    biz_id = extract_business_id(business_url)
    
    # Extract basic information
    title = safe_text(driver, BUSINESS_TITLE)
    categories = ", ".join(safe_list(driver, BUSINESS_CATEGORIES))
    
    # Extract website (with redirect handling)
    website_href = safe_attr(driver, BUSINESS_WEBSITE, "href")
    website = extract_real_website(website_href)
    
    # Extract phone with fallback selectors
    phone = try_multiple_selectors(driver, [BUSINESS_PHONE] + ALTERNATIVE_SELECTORS['phone'])
    
    # Extract rating
    rating = safe_attr(driver, BUSINESS_RATING, "aria-label")
    
    # Extract reviews with fallback
    reviews = try_multiple_selectors(driver, [BUSINESS_REVIEWS] + ALTERNATIVE_SELECTORS['reviews'])
    
    # Extract address with fallback
    address = try_multiple_selectors(driver, [BUSINESS_ADDRESS] + ALTERNATIVE_SELECTORS['address'])
    
    # Extract hours
    hours = safe_text(driver, BUSINESS_HOURS)
    
    return {
        "ID": biz_id,
        "Title": title,
        "Description": categories,
        "Website": website,
        "Phone": phone,
        "Rating": rating,
        "Reviews": reviews,
        "Address": address,
        "Hours": hours
    } 