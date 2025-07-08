import gspread
from google.oauth2.service_account import Credentials
from .config import GOOGLE_SHEET_NAME, INPUT_WORKSHEET_NAME, OUTPUT_WORKSHEET_NAME, CREDENTIALS_PATH

def get_google_sheets_client():
    """
    Create and return authenticated Google Sheets client
    """
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"❌ Error authenticating with Google Sheets: {e}")
        raise

def read_input_sheet():
    """
    Read search parameters from the input worksheet
    """
    try:
        client = get_google_sheets_client()
        sheet = client.open(GOOGLE_SHEET_NAME).worksheet(INPUT_WORKSHEET_NAME)
        records = sheet.get_all_records()
        
        if not records:
            print("⚠️  No data found in input sheet")
            return []
            
        print(f"📖 Read {len(records)} search parameters from input sheet")
        return records
        
    except Exception as e:
        print(f"❌ Error reading input sheet: {e}")
        raise

def write_to_output_sheet(all_results):
    """
    Write scraped results to the output worksheet
    """
    if not all_results:
        print("❌ No results to write")
        return
        
    try:
        client = get_google_sheets_client()
        spreadsheet = client.open(GOOGLE_SHEET_NAME)
        
        # Try to get existing output sheet
        try:
            sheet = spreadsheet.worksheet(OUTPUT_WORKSHEET_NAME)
            existing_data = sheet.get_all_values()
            
            if existing_data:
                print(f"📊 Found existing data with {len(existing_data)-1} results")
                # Get headers from existing data
                headers = existing_data[0]
                
                # Prepare new rows (skip headers since they already exist)
                new_rows = []
                for result in all_results:
                    row = [result.get(header, "") for header in headers]
                    new_rows.append(row)
                
                # Append new data to existing sheet
                if new_rows:
                    sheet.append_rows(new_rows)
                    print(f"✅ Successfully appended {len(new_rows)} new results to output sheet")
                else:
                    print("❌ No new results to append")
            else:
                # Empty sheet, write headers and data
                headers = list(all_results[0].keys())
                rows_to_write = [headers]
                for result in all_results:
                    row = [result.get(header, "") for header in headers]
                    rows_to_write.append(row)
                
                sheet.update(values=rows_to_write)
                print(f"✅ Successfully wrote {len(all_results)} results to new output sheet")
                
        except gspread.WorksheetNotFound:
            # Create output sheet if it doesn't exist
            sheet = spreadsheet.add_worksheet(title=OUTPUT_WORKSHEET_NAME, rows=1000, cols=20)
            
            # Write headers and data to new sheet
            headers = list(all_results[0].keys())
            rows_to_write = [headers]
            for result in all_results:
                row = [result.get(header, "") for header in headers]
                rows_to_write.append(row)
            
            sheet.update(values=rows_to_write)
            print(f"✅ Successfully created output sheet and wrote {len(all_results)} results")
            
    except Exception as e:
        print(f"❌ Error writing to output sheet: {e}")
        raise 