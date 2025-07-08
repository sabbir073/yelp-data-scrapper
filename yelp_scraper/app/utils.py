import time
import random
import os
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from .config import DEFAULT_WAIT_TIME, PAGE_LOAD_WAIT, TAB_SWITCH_WAIT
from selenium.webdriver.support.ui import WebDriverWait

def random_delay(min_seconds=1.0, max_seconds=3.0):
    """
    Add a random delay to avoid detection
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def human_like_delay():
    """
    Add a human-like delay with some randomness
    """
    base_delay = random.uniform(2, 5)
    time.sleep(base_delay)

def scroll_page(driver, scroll_pause_time=1):
    """
    Scroll the page to load all content
    """
    try:
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait to load page
            time.sleep(scroll_pause_time)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
    except Exception as e:
        print(f"⚠️  Error during scrolling: {e}")

def take_screenshot(driver, filename=None):
    """
    Take a screenshot for debugging purposes
    """
    try:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        # Create screenshots directory if it doesn't exist
        os.makedirs("screenshots", exist_ok=True)
        filepath = os.path.join("screenshots", filename)
        
        driver.save_screenshot(filepath)
        print(f"📸 Screenshot saved: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"❌ Error taking screenshot: {e}")
        return None

def clear_input_field(driver, element):
    """
    Clear an input field thoroughly to remove default values
    """
    try:
        element.click()
        element.send_keys(Keys.CONTROL + "a")  # Select all text
        element.send_keys(Keys.BACKSPACE)       # Delete selected text
        time.sleep(0.5)
        element.clear()
        return True
    except Exception as e:
        print(f"❌ Error clearing input field: {e}")
        return False

def wait_for_page_load(driver, timeout=10):
    """
    Wait for page to fully load
    """
    try:
        # Wait for document ready state
        WebDriverWait(driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        return True
    except Exception as e:
        print(f"⚠️  Page load timeout: {e}")
        return False

def simulate_human_typing(driver, element, text, min_delay=0.1, max_delay=0.3):
    """
    Simulate human-like typing with random delays
    """
    try:
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(min_delay, max_delay))
        return True
    except Exception as e:
        print(f"❌ Error during human-like typing: {e}")
        return False

def check_for_captcha(driver):
    """
    Check if a CAPTCHA is present on the page
    """
    captcha_selectors = [
        "//div[contains(@class,'captcha')]",
        "//iframe[contains(@src,'captcha')]",
        "//div[contains(text(),'captcha')]",
        "//div[contains(text(),'verify')]"
    ]
    
    for selector in captcha_selectors:
        try:
            if driver.find_element_by_xpath(selector):
                return True
        except:
            continue
    
    return False

def handle_captcha(driver):
    """
    Handle CAPTCHA if detected
    """
    if check_for_captcha(driver):
        print("🚨 CAPTCHA detected! Please solve it manually.")
        take_screenshot(driver, "captcha_detected.png")
        
        # Wait for user to solve CAPTCHA
        input("Press Enter after solving the CAPTCHA...")
        return True
    
    return False 