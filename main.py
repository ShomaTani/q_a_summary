import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

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

load_dotenv()
client = genai.Client(api_key="GEMINI_API_KEY")

def classify_and_summarise(test):
    prompt = f"""
    質問を分類して、類似質問を「○○に関する技術的質問」、「ステップ○○でのバグ報告」、「運用相談」などにまとめ、要約して以下の評価基準に則って優先度順に表示してください。
    -類似質問の数
    -講師回答の必要性
    -講義との関連性
    -ある程度の一般性（個人の機器トラブルなど以外）

    
    質問：{test}
    出力形式はJSONで、
    {
        "分類": "分類名",
        "類似質問数": 数字,
        "講師回答の必要性": "高/中/低",
        "講義との関連性": "高/中/低",
        "一般性": "高/中/低",
        "要約": "要約内容"
    }
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[{"role":"user", "content": prompt}],
        config=types.GenerateContentConfig(
            max_output_tokens=500,
            temperature=0.1
        )
    )
    return response.choices[0].message.content
    
print(classify_and_summarise(rows))