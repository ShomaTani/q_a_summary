import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment")
print(os.environ.get("GEMINI_API_KEY"))

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file(
    filename="service_account.json", scopes=SCOPES
)

gc = gspread.authorize(creds)


def fetch_sheet(sheet_url):
    sheet = gc.open_by_url(sheet_url).sheet1
    return sheet.get_all_records()


def strip_text(s: str) -> dict:
    text = s.strip()
    if text.startswith("```json") and text.endswith("```"):
        text = text[7:-3].strip()
    elif text.startswith("```") and text.endswith("```"):
        text = text[3:-3].strip()
    return text


def classify_and_summarize(test):
    prompt = f"""
    質問を分類して、類似質問を「○○に関する技術的質問」、「ステップ○○でのバグ報告」、「運用相談」などにまとめ、要約して以下の評価基準に則って優先度順に10個表示してください。
    -類似質問の数
    -講師回答の必要性
    -講義との関連性
    -ある程度の一般性（個人の機器トラブルなど以外）

    
    質問：{test}
    出力形式はそのままJSONとして読み込めるようにJSONのみで、
    {{
        "分類": "分類名",
        "類似質問数": "数字",
        "講師回答の必要性": "高/中/低",
        "講義との関連性": "高/中/低",
        "一般性": "高/中/低",
        "要約": "要約内容"
    }}
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(max_output_tokens=500, temperature=0.1),
    )
    print(response.text)
    text = strip_text(response.text)
    print(text)
    return json.loads(text)


def parse_json(obj: str) -> dict:
    if isinstance(obj, (dict, list)):
        return obj
    else:
        text = obj.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "error": "JSONの読み込みに失敗しました。入力が正しい形式であるか確認してください。"
        }
    except Exception as e:
        return {"error": f"予期しないエラーが発生しました: {e}"}


def build_dataframe(results: list[dict]) -> pd.DataFrame:
    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results)
    # df = df.rename(columns={
    #     "分類": "Category",
    #     "類似質問数": "Similar Questions Count",
    #     "講師回答の必要性": "Instructor Response Necessity",
    #     "講義との関連性": "Lecture Relevance",
    #     "一般性": "Generality",
    #     "要約": "Summary",
    #     "original": "Original Question"
    # })
    return df


# classify_and_summarize("このコードは何をしますか？")
