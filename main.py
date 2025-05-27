import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    'service_account.json', scope)
gc = gspread.authorize(creds)

spreadsheet_id = '1gUXLRZQjD4M9a5w9m256CRtMAbyWNdr8psfOl_rplIs'
sheet = gc.open('Q_A_test').sheet1
rows = sheet.get_all_records()

with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
    
print(rows)