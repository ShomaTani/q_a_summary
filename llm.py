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


def fetch_questions(sheet_url):
    sheet = gc.open_by_url(sheet_url).sheet1
    headers = sheet.row_values(1)
    if not headers:
        return []
    if "質問" not in headers:
        return []
    records = sheet.get_all_records()
    questions = []
    if "回答" in headers:
        for rec in records:
            answer = rec.get("回答")
            if answer is None or str(answer).strip() == "":
                q = rec.get("質問")
                if q is not None:
                    questions.append(str(q).strip())

    else:
        for rec in records:
            q = rec.get("質問")
            if q is not None:
                questions.append(str(q).strip())

    return questions


def strip_text(s: str) -> dict:
    text = s.strip()
    if text.startswith("```json") and text.endswith("```"):
        text = text[7:-3].strip()
    elif text.startswith("```") and text.endswith("```"):
        text = text[3:-3].strip()
    return text


def classify_and_summarize(question, num, pdf_file_obj=None):
    prompt = f"""
    質問を分類して、類似質問を「○○に関する技術的質問」、「ステップ○○でのバグ報告」、「運用相談」などにまとめ、各分類の質問を講師が答えられる、かつ重要な要素を逃さないように一つの質問に要約して以下の評価基準に則って優先度順に{num}個のみを表示してください。
    講師による解答の必要性と講義との関係性を評価するときは、アップロードされていれば、講義資料のPDFを参考にしてください。
    -類似質問の数
    -LLMではなく講師による回答の必要性
    -講義との関連性
    -ある程度の一般性（個人の機器トラブルなど以外）

    
    質問：{question}
    出力形式はそのままJSONとして読み込めるようにJSONのみで、
    {{
        "分類": "分類名",
        "類似質問数": "数字",
        "講師回答の必要性": "高/中/低",
        "講義との関連性": "高/中/低",
        "一般性": "高/中/低",
        "要約": "要約内容"
        "分類される質問": "質問内容1, 質問内容2, ..."
    }}
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, pdf_file_obj] if pdf_file_obj else [prompt],
        config=types.GenerateContentConfig(max_output_tokens=10000, temperature=0.1),
    )
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


def load_pdf(lecture_pdf):
    pdf_file_obj = None
    if lecture_pdf is not None:
        with open("temp_lecture.pdf", "wb") as f:
            f.write(lecture_pdf.getbuffer())
        pdf_file_obj = client.files.upload(file="temp_lecture.pdf")
    return pdf_file_obj


record = fetch_questions(
    "https://docs.google.com/spreadsheets/d/1m_D7vPU_iLgtzHvVrtvUPIxM4Jjh7swoJWF2s8F6vR4/edit?gid=0#gid=0"
)
# response = classify_and_summarize("record",5)
# print(response)

print(record)
