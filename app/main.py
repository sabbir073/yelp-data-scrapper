#!/usr/bin/env python3
"""
Yelp Scraper - Main Entry Point
Scrapes business information from Yelp based on search parameters in Google Sheets
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.chrome_control import setup_driver
from app.yelp_scraper import scrape_yelp_all_pages
from app.sheets import read_input_sheet, write_to_output_sheet
from app.config import MAX_PAGES
from app.utils import deduplicate_results

def main():
    """
    Main function that orchestrates the entire scraping process
    """
    print("🚀 Starting Yelp Scraper...")
    print(f"📊 Maximum pages per search: {MAX_PAGES}")
    
    try:
        # Read search parameters from Google Sheets
        print("\n📖 Reading search parameters...")
        search_params = read_input_sheet()
        
        if not search_params:
            print("❌ No search parameters found. Please check your input sheet.")
            return
        
        print(f"✅ Found {len(search_params)} search parameters")
        
        # Set up Chrome driver
        print("\n🔧 Setting up Chrome driver...")
        driver = setup_driver()
        
        # Process each search parameter
        all_results = []
        for i, row in enumerate(search_params, 1):
            keyword = row.get("keyword", "")
            location = row.get("location", "")
            
            if not keyword or not location:
                print(f"⚠️  Skipping row {i}: missing keyword or location")
                continue
            
            print(f"\n🔍 [{i}/{len(search_params)}] Scraping for: '{keyword}' in '{location}'")
            
            try:
                # Scrape all pages for this search
                results = scrape_yelp_all_pages(driver, keyword, location)
                all_results.extend(results)
                
                print(f"✅ Completed search {i}: {len(results)} results")
                
            except Exception as e:
                print(f"❌ Error processing search {i}: {e}")
                continue
        
        # Write all results to Google Sheets
        if all_results:
            print(f"\n📝 Writing {len(all_results)} total results to Google Sheets...")
            unique_results = deduplicate_results(all_results, key="ID")
            print(f"📝 After deduplication: {len(unique_results)} unique results")
            write_to_output_sheet(unique_results)
            print("✅ All results written successfully!")
        else:
            print("❌ No results to write")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return 1
    
    finally:
        # Clean up
        try:
            if 'driver' in locals():
                print("\n🧹 Cleaning up...")
                driver.quit()
                print("✅ Driver closed successfully")
        except Exception as e:
            print(f"⚠️  Error closing driver: {e}")
    
    print("\n🎉 Yelp Scraper completed successfully!")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 