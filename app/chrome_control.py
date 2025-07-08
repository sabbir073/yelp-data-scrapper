from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from .config import CHROME_HEADLESS, CHROME_USER_AGENT

def setup_driver(headless=None):
    """
    Set up and configure Chrome WebDriver with anti-detection measures
    """
    if headless is None:
        headless = CHROME_HEADLESS
        
    options = Options()
    
    # Basic Chrome options
    if headless:
        options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Anti-detection measures
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f"--user-agent={CHROME_USER_AGENT}")
    
    # Additional options to avoid detection
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")  # Optional: speeds up loading
    
    try:
        driver = webdriver.Chrome(options=options)
        # Hide webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"❌ Error setting up Chrome driver: {e}")
        raise

def wait_for_element(driver, xpath, timeout=10):
    """
    Wait for an element to be present and return it
    """
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return element
    except Exception as e:
        print(f"❌ Element not found: {xpath}")
        return None

def safe_click(driver, element, delay=1):
    """
    Safely click an element with error handling
    """
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(delay)
        element.click()
        return True
    except Exception as e:
        print(f"❌ Error clicking element: {e}")
        return False

def switch_to_new_tab(driver, wait_time=3):
    """
    Switch to the most recently opened tab
    """
    try:
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(wait_time)
        return True
    except Exception as e:
        print(f"❌ Error switching to new tab: {e}")
        return False

def close_current_tab(driver, switch_to_main=True):
    """
    Close current tab and optionally switch back to main tab
    """
    try:
        driver.close()
        if switch_to_main and len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])
        return True
    except Exception as e:
        print(f"❌ Error closing tab: {e}")
        return False 